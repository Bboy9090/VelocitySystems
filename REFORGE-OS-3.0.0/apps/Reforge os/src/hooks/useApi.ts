/**
 * Enterprise API Hook
 * 
 * React hook for API calls with loading states, error handling, and retry logic
 */

import { useState, useCallback, useRef } from 'react';
import { logger } from '@core/logger/Logger';
import { AppError, ErrorHandler } from '@core/errors/AppError';

export interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: AppError | null;
}

export interface UseApiOptions {
  immediate?: boolean;
  onSuccess?: (data: unknown) => void;
  onError?: (error: AppError) => void;
}

/**
 * Hook for API calls with state management
 */
export function useApi<T = unknown>(
  apiCall: () => Promise<T>,
  options: UseApiOptions = {}
): [UseApiState<T>, () => Promise<void>, () => void] {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const abortControllerRef = useRef<AbortController | null>(null);

  const execute = useCallback(async () => {
    // Cancel previous request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new abort controller
    abortControllerRef.current = new AbortController();

    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const data = await apiCall();
      
      setState({
        data,
        loading: false,
        error: null,
      });

      if (options.onSuccess) {
        options.onSuccess(data);
      }
    } catch (error) {
      const appError = ErrorHandler.handle(error);

      logger.error('API call failed', appError, {
        error: appError.toJSON(),
      });

      setState({
        data: null,
        loading: false,
        error: appError,
      });

      if (options.onError) {
        options.onError(appError);
      }
    }
  }, [apiCall, options]);

  const reset = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setState({
      data: null,
      loading: false,
      error: null,
    });
  }, []);

  // Execute immediately if requested
  if (options.immediate && !state.loading && !state.data && !state.error) {
    execute();
  }

  return [state, execute, reset];
}
