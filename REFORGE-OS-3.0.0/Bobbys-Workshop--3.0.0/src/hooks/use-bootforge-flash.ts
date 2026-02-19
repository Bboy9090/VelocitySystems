import { useState, useEffect, useCallback, useRef } from 'react';
import { toast } from 'sonner';
import { bootForgeAPI } from '@/lib/bootforge-api';
import { logger } from '@/lib/logger';
import type { RealtimeConnection } from '@/lib/realtime';
import type {
  BootForgeDevice,
  FlashJobConfig,
  FlashOperation,
  FlashProgress,
  RealTimeFlashUpdate,
} from '@/types/flash-operations';

export interface UseBootForgeFlashOptions {
  autoReconnect?: boolean;
  reconnectDelay?: number;
  maxReconnectAttempts?: number;
  enableNotifications?: boolean;
}

export function useBootForgeFlash(options: UseBootForgeFlashOptions = {}) {
  const {
    autoReconnect = true,
    reconnectDelay = 3000,
    maxReconnectAttempts = 5,
    enableNotifications = true,
  } = options;

  const [connectedDevices, setConnectedDevices] = useState<BootForgeDevice[]>([]);
  const [activeOperations, setActiveOperations] = useState<Map<string, FlashOperation>>(new Map());
  const [flashHistory, setFlashHistory] = useState<FlashOperation[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  
  const wsRef = useRef<RealtimeConnection | null>(null);
  const jobWsRefs = useRef<Map<string, RealtimeConnection>>(new Map());
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const scanDevices = useCallback(async () => {
    setIsScanning(true);
    try {
      const devices = await bootForgeAPI.scanDevices();
      setConnectedDevices(devices);
      
      if (enableNotifications) {
        toast.success(`Found ${devices.length} device(s)`, {
          description: devices.map(d => `${d.brand} ${d.model || d.serial}`).join(', '),
        });
      }
      
      return devices;
    } catch (error) {
      logger.error('BootForgeFlash', 'Device scan failed', error instanceof Error ? error : undefined);
      
      if (enableNotifications) {
        toast.error('Device scan failed', {
          description: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      
      return [];
    } finally {
      setIsScanning(false);
    }
  }, [enableNotifications]);

  const loadFlashHistory = useCallback(async () => {
    try {
      const history = await bootForgeAPI.getFlashHistory();
      setFlashHistory(history);
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to load flash history', error instanceof Error ? error : undefined);
    }
  }, []);

  const loadActiveOperations = useCallback(async () => {
    try {
      const operations = await bootForgeAPI.getActiveFlashOperations();
      const opsMap = new Map(operations.map(op => [op.id, op]));
      setActiveOperations(opsMap);
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to load active operations', error instanceof Error ? error : undefined);
    }
  }, []);

  const startFlash = useCallback(async (config: FlashJobConfig): Promise<FlashOperation | null> => {
    try {
      const operation = await bootForgeAPI.startFlashOperation(config);
      
      setActiveOperations(prev => {
        const next = new Map(prev);
        next.set(operation.id, operation);
        return next;
      });

      const jobWs = bootForgeAPI.createFlashWebSocket(operation.id);
      jobWsRefs.current.set(operation.id, jobWs);

      jobWs.onopen = () => {
        logger.info('BootForgeFlash', `Flash WebSocket connected for job ${operation.id}`);
      };

      jobWs.onmessage = (event) => {
        try {
          const update: RealTimeFlashUpdate = JSON.parse(event.data);
          handleFlashUpdate(update);
        } catch (error) {
          logger.error('BootForgeFlash', 'Failed to parse flash update', error instanceof Error ? error : undefined);
        }
      };

      jobWs.onerror = (error) => {
        logger.error('BootForgeFlash', `Flash WebSocket error for job ${operation.id}`, error instanceof Error ? error : undefined);
      };

      jobWs.onclose = () => {
        logger.info('BootForgeFlash', `Flash WebSocket closed for job ${operation.id}`);
        jobWsRefs.current.delete(operation.id);
      };

      if (enableNotifications) {
        toast.success('Flash operation started', {
          description: `Flashing ${config.deviceBrand} device`,
        });
      }

      return operation;
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to start flash operation', error instanceof Error ? error : undefined);
      
      if (enableNotifications) {
        toast.error('Failed to start flash', {
          description: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      
      return null;
    }
  }, [enableNotifications]);

  const pauseFlash = useCallback(async (jobId: string) => {
    try {
      const result = await bootForgeAPI.pauseFlashOperation(jobId);
      
      if (result.success) {
        setActiveOperations(prev => {
          const next = new Map(prev);
          const op = next.get(jobId);
          if (op) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                status: 'paused',
                pausedAt: Date.now(),
              },
            });
          }
          return next;
        });

        if (enableNotifications) {
          toast.info('Flash operation paused');
        }
      }
      
      return result;
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to pause flash operation', error instanceof Error ? error : undefined);
      
      if (enableNotifications) {
        toast.error('Failed to pause flash', {
          description: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      
      return { success: false, message: 'Failed to pause' };
    }
  }, [enableNotifications]);

  const resumeFlash = useCallback(async (jobId: string) => {
    try {
      const result = await bootForgeAPI.resumeFlashOperation(jobId);
      
      if (result.success) {
        setActiveOperations(prev => {
          const next = new Map(prev);
          const op = next.get(jobId);
          if (op) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                status: 'flashing',
                pausedAt: undefined,
              },
            });
          }
          return next;
        });

        if (enableNotifications) {
          toast.success('Flash operation resumed');
        }
      }
      
      return result;
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to resume flash operation', error instanceof Error ? error : undefined);
      
      if (enableNotifications) {
        toast.error('Failed to resume flash', {
          description: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      
      return { success: false, message: 'Failed to resume' };
    }
  }, [enableNotifications]);

  const cancelFlash = useCallback(async (jobId: string) => {
    try {
      const result = await bootForgeAPI.cancelFlashOperation(jobId);
      
      if (result.success) {
        setActiveOperations(prev => {
          const next = new Map(prev);
          const op = next.get(jobId);
          if (op) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                status: 'cancelled',
              },
            });
          }
          return next;
        });

        const jobWs = jobWsRefs.current.get(jobId);
        if (jobWs) {
          jobWs.close();
          jobWsRefs.current.delete(jobId);
        }

        if (enableNotifications) {
          toast.warning('Flash operation cancelled');
        }

        await loadFlashHistory();
      }
      
      return result;
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to cancel flash operation', error instanceof Error ? error : undefined);
      
      if (enableNotifications) {
        toast.error('Failed to cancel flash', {
          description: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      
      return { success: false, message: 'Failed to cancel' };
    }
  }, [enableNotifications, loadFlashHistory]);

  const handleFlashUpdate = useCallback((update: RealTimeFlashUpdate) => {
    const { jobId, type, data } = update;

    setActiveOperations(prev => {
      const next = new Map(prev);
      const op = next.get(jobId);
      
      if (!op) return prev;

      switch (type) {
        case 'status':
          if (data.status) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                status: data.status,
              },
            });
          }
          break;

        case 'progress':
          next.set(jobId, {
            ...op,
            progress: {
              ...op.progress,
              overallProgress: data.progress ?? op.progress.overallProgress,
              bytesTransferred: data.bytesTransferred ?? op.progress.bytesTransferred,
              transferSpeed: data.transferSpeed ?? op.progress.transferSpeed,
            },
          });
          break;

        case 'log':
          if (data.message) {
            next.set(jobId, {
              ...op,
              logs: [...op.logs, `[${new Date(update.timestamp).toLocaleTimeString()}] ${data.message}`],
            });
          }
          break;

        case 'warning':
          if (data.message) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                warnings: [...op.progress.warnings, data.message],
              },
            });
          }
          break;

        case 'error':
          if (data.message) {
            next.set(jobId, {
              ...op,
              progress: {
                ...op.progress,
                status: 'failed',
                error: data.message,
              },
            });

            if (enableNotifications) {
              toast.error('Flash operation failed', {
                description: data.message,
              });
            }
          }
          break;
      }

      if (data.status === 'completed') {
        if (enableNotifications) {
          toast.success('Flash operation completed', {
            description: `Successfully flashed ${op.progress.deviceBrand} device`,
          });
        }
        loadFlashHistory();
      }

      return next;
    });
  }, [enableNotifications, loadFlashHistory]);

  const connectDeviceMonitor = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      const ws = bootForgeAPI.createDeviceMonitorWebSocket();
      wsRef.current = ws;

      ws.onopen = () => {
        setWsConnected(true);
        reconnectAttemptsRef.current = 0;
        logger.info('BootForgeFlash', 'Device monitor WebSocket connected');
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (
            data?.type === 'connected' ||
            data?.type === 'disconnected' ||
            data?.type === 'device_connected' ||
            data?.type === 'device_disconnected'
          ) {
            scanDevices();
          }
        } catch (error) {
          logger.error('BootForgeFlash', 'Failed to parse device monitor message', error instanceof Error ? error : undefined);
        }
      };

      ws.onerror = (error) => {
        logger.error('BootForgeFlash', 'Device monitor WebSocket error', error instanceof Error ? error : undefined);
      };

      ws.onclose = () => {
        setWsConnected(false);
        logger.info('BootForgeFlash', 'Device monitor WebSocket closed');

        if (autoReconnect && reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++;
            connectDeviceMonitor();
          }, reconnectDelay);
        }
      };
    } catch (error) {
      logger.error('BootForgeFlash', 'Failed to create device monitor WebSocket', error instanceof Error ? error : undefined);
    }
  }, [autoReconnect, reconnectDelay, maxReconnectAttempts, scanDevices]);

  const disconnectDeviceMonitor = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setWsConnected(false);
  }, []);

  useEffect(() => {
    scanDevices();
    loadFlashHistory();
    loadActiveOperations();
    connectDeviceMonitor();

    return () => {
      disconnectDeviceMonitor();
      
      jobWsRefs.current.forEach(ws => ws.close());
      jobWsRefs.current.clear();
    };
  }, []);

  return {
    connectedDevices,
    activeOperations: Array.from(activeOperations.values()),
    flashHistory,
    isScanning,
    wsConnected,
    scanDevices,
    startFlash,
    pauseFlash,
    resumeFlash,
    cancelFlash,
    loadFlashHistory,
    connectDeviceMonitor,
    disconnectDeviceMonitor,
  };
}
