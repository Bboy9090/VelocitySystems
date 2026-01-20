/**
 * Enterprise Logging Infrastructure
 * 
 * Centralized logging with levels, structured data, and remote capabilities
 */

export enum LogLevel {
  Debug = 'debug',
  Info = 'info',
  Warn = 'warn',
  Error = 'error',
}

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: string;
  metadata?: Record<string, unknown>;
  error?: Error;
  stack?: string;
}

export interface LoggerConfig {
  level: LogLevel;
  enableConsole: boolean;
  enableRemote: boolean;
  context?: string;
}

class Logger {
  private config: LoggerConfig;
  private logBuffer: LogEntry[] = [];
  private readonly maxBufferSize = 100;

  constructor(config: LoggerConfig) {
    this.config = config;
  }

  /**
   * Logs a debug message
   */
  debug(message: string, metadata?: Record<string, unknown>): void {
    this.log(LogLevel.Debug, message, metadata);
  }

  /**
   * Logs an info message
   */
  info(message: string, metadata?: Record<string, unknown>): void {
    this.log(LogLevel.Info, message, metadata);
  }

  /**
   * Logs a warning message
   */
  warn(message: string, metadata?: Record<string, unknown>): void {
    this.log(LogLevel.Warn, message, metadata);
  }

  /**
   * Logs an error message
   */
  error(message: string, error?: Error, metadata?: Record<string, unknown>): void {
    this.log(LogLevel.Error, message, metadata, error);
  }

  /**
   * Creates a child logger with additional context
   */
  child(context: string): Logger {
    return new Logger({
      ...this.config,
      context: this.config.context ? `${this.config.context}:${context}` : context,
    });
  }

  /**
   * Internal logging method
   */
  private log(
    level: LogLevel,
    message: string,
    metadata?: Record<string, unknown>,
    error?: Error
  ): void {
    // Check if we should log at this level
    if (!this.shouldLog(level)) {
      return;
    }

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: this.config.context,
      metadata,
      error,
      stack: error?.stack,
    };

    // Add to buffer
    this.addToBuffer(entry);

    // Console output
    if (this.config.enableConsole) {
      this.logToConsole(entry);
    }

    // Remote logging
    if (this.config.enableRemote) {
      this.logToRemote(entry).catch((err) => {
        // Fallback to console if remote logging fails
        console.error('Failed to log to remote:', err);
      });
    }
  }

  /**
   * Checks if we should log at the given level
   */
  private shouldLog(level: LogLevel): boolean {
    const levels = [LogLevel.Debug, LogLevel.Info, LogLevel.Warn, LogLevel.Error];
    const configLevelIndex = levels.indexOf(this.config.level);
    const messageLevelIndex = levels.indexOf(level);
    return messageLevelIndex >= configLevelIndex;
  }

  /**
   * Adds entry to buffer for batch processing
   */
  private addToBuffer(entry: LogEntry): void {
    this.logBuffer.push(entry);
    if (this.logBuffer.length > this.maxBufferSize) {
      this.logBuffer.shift();
    }
  }

  /**
   * Logs to console with appropriate formatting
   */
  private logToConsole(entry: LogEntry): void {
    const prefix = entry.context ? `[${entry.context}]` : '';
    const message = `${prefix} ${entry.message}`;

    switch (entry.level) {
      case LogLevel.Debug:
        console.debug(message, entry.metadata || '');
        break;
      case LogLevel.Info:
        console.info(message, entry.metadata || '');
        break;
      case LogLevel.Warn:
        console.warn(message, entry.metadata || '');
        break;
      case LogLevel.Error:
        console.error(message, entry.error || entry.metadata || '');
        if (entry.stack) {
          console.error(entry.stack);
        }
        break;
    }
  }

  /**
   * Sends log entry to remote logging service
   */
  private async logToRemote(entry: LogEntry): Promise<void> {
    // TODO: Implement remote logging service integration
    // This could be Sentry, LogRocket, or a custom endpoint
    try {
      // Example: await fetch('/api/logs', { method: 'POST', body: JSON.stringify(entry) });
    } catch (error) {
      // Silently fail - we don't want logging errors to break the app
    }
  }

  /**
   * Flushes the log buffer (useful for critical errors)
   */
  flush(): void {
    // Send all buffered logs to remote
    if (this.config.enableRemote) {
      this.logBuffer.forEach((entry) => {
        this.logToRemote(entry).catch(() => {
          // Ignore errors
        });
      });
    }
    this.logBuffer = [];
  }

  /**
   * Gets recent log entries
   */
  getRecentLogs(count: number = 10): LogEntry[] {
    return this.logBuffer.slice(-count);
  }
}

/**
 * Creates a logger instance
 */
export function createLogger(config: LoggerConfig): Logger {
  return new Logger(config);
}

/**
 * Default logger instance
 */
import { config } from '@config/environment';

export const logger = createLogger({
  level: config.logging.level,
  enableConsole: config.logging.enableConsole,
  enableRemote: config.logging.enableRemote,
  context: 'App',
});
