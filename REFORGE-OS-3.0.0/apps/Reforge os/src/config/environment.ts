/**
 * Enterprise Configuration Management
 * 
 * Centralized configuration with environment variable support,
 * validation, and type safety.
 */

export enum Environment {
  Development = 'development',
  Staging = 'staging',
  Production = 'production',
  Test = 'test',
}

export interface AppConfig {
  environment: Environment;
  api: {
    baseUrl: string;
    timeout: number;
    retryAttempts: number;
    retryDelay: number;
  };
  trapdoor: {
    baseUrl: string;
    enabled: boolean;
  };
  features: {
    devMode: boolean;
    auditLogging: boolean;
    shadowLogs: boolean;
    batchOperations: boolean;
  };
  security: {
    requireAuth: boolean;
    sessionTimeout: number;
    maxRetries: number;
  };
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    enableConsole: boolean;
    enableRemote: boolean;
  };
}

/**
 * Validates and loads configuration from environment variables
 */
function loadConfig(): AppConfig {
  const env = (import.meta.env.MODE || 'development') as Environment;
  
  // Validate environment
  if (!Object.values(Environment).includes(env)) {
    throw new Error(`Invalid environment: ${env}`);
  }

  return {
    environment: env,
    api: {
      baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001',
      timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000', 10),
      retryAttempts: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS || '3', 10),
      retryDelay: parseInt(import.meta.env.VITE_API_RETRY_DELAY || '1000', 10),
    },
    trapdoor: {
      baseUrl: import.meta.env.VITE_TRAPDOOR_BASE_URL || 'http://localhost:8001/api/trapdoor',
      enabled: import.meta.env.VITE_TRAPDOOR_ENABLED === 'true',
    },
    features: {
      devMode: import.meta.env.VITE_FEATURE_DEV_MODE !== 'false',
      auditLogging: import.meta.env.VITE_FEATURE_AUDIT_LOGGING !== 'false',
      shadowLogs: import.meta.env.VITE_FEATURE_SHADOW_LOGS === 'true',
      batchOperations: import.meta.env.VITE_FEATURE_BATCH_OPS !== 'false',
    },
    security: {
      requireAuth: import.meta.env.VITE_REQUIRE_AUTH === 'true',
      sessionTimeout: parseInt(import.meta.env.VITE_SESSION_TIMEOUT || '3600000', 10),
      maxRetries: parseInt(import.meta.env.VITE_MAX_RETRIES || '3', 10),
    },
    logging: {
      level: (import.meta.env.VITE_LOG_LEVEL || 'info') as AppConfig['logging']['level'],
      enableConsole: import.meta.env.VITE_LOG_CONSOLE !== 'false',
      enableRemote: import.meta.env.VITE_LOG_REMOTE === 'true',
    },
  };
}

/**
 * Singleton configuration instance
 */
export const config: AppConfig = loadConfig();

/**
 * Type guard to check if we're in production
 */
export const isProduction = (): boolean => config.environment === Environment.Production;

/**
 * Type guard to check if we're in development
 */
export const isDevelopment = (): boolean => config.environment === Environment.Development;

/**
 * Type guard to check if we're in test mode
 */
export const isTest = (): boolean => config.environment === Environment.Test;
