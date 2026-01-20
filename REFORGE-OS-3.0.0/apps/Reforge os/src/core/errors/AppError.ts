/**
 * Enterprise Error Handling Infrastructure
 * 
 * Standardized error types with context, codes, and recovery strategies
 */

export enum ErrorCode {
  // Network Errors
  NETWORK_ERROR = 'NETWORK_ERROR',
  TIMEOUT_ERROR = 'TIMEOUT_ERROR',
  CONNECTION_REFUSED = 'CONNECTION_REFUSED',

  // API Errors
  API_ERROR = 'API_ERROR',
  API_UNAUTHORIZED = 'API_UNAUTHORIZED',
  API_FORBIDDEN = 'API_FORBIDDEN',
  API_NOT_FOUND = 'API_NOT_FOUND',
  API_VALIDATION_ERROR = 'API_VALIDATION_ERROR',
  API_SERVER_ERROR = 'API_SERVER_ERROR',

  // Business Logic Errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  BUSINESS_RULE_VIOLATION = 'BUSINESS_RULE_VIOLATION',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED',

  // System Errors
  CONFIGURATION_ERROR = 'CONFIGURATION_ERROR',
  UNKNOWN_ERROR = 'UNKNOWN_ERROR',
}

export interface ErrorContext {
  [key: string]: unknown;
}

export interface ErrorMetadata {
  code: ErrorCode;
  message: string;
  context?: ErrorContext;
  originalError?: Error;
  timestamp: string;
  recoverable: boolean;
  retryable: boolean;
  userMessage?: string;
}

/**
 * Base application error class
 */
export class AppError extends Error {
  public readonly code: ErrorCode;
  public readonly context?: ErrorContext;
  public readonly originalError?: Error;
  public readonly timestamp: string;
  public readonly recoverable: boolean;
  public readonly retryable: boolean;
  public readonly userMessage?: string;

  constructor(metadata: ErrorMetadata) {
    super(metadata.message);
    this.name = 'AppError';
    this.code = metadata.code;
    this.context = metadata.context;
    this.originalError = metadata.originalError;
    this.timestamp = metadata.timestamp;
    this.recoverable = metadata.recoverable;
    this.retryable = metadata.retryable;
    this.userMessage = metadata.userMessage;

    // Maintain proper stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AppError);
    }
  }

  /**
   * Creates a user-friendly error message
   */
  getUserMessage(): string {
    return this.userMessage || this.message;
  }

  /**
   * Serializes error for logging/transmission
   */
  toJSON(): ErrorMetadata {
    return {
      code: this.code,
      message: this.message,
      context: this.context,
      originalError: this.originalError ? {
        name: this.originalError.name,
        message: this.originalError.message,
        stack: this.originalError.stack,
      } as unknown as Error : undefined,
      timestamp: this.timestamp,
      recoverable: this.recoverable,
      retryable: this.retryable,
      userMessage: this.userMessage,
    };
  }
}

/**
 * Network-related errors
 */
export class NetworkError extends AppError {
  constructor(message: string, originalError?: Error, context?: ErrorContext) {
    super({
      code: ErrorCode.NETWORK_ERROR,
      message,
      context,
      originalError,
      timestamp: new Date().toISOString(),
      recoverable: true,
      retryable: true,
      userMessage: 'Network connection failed. Please check your internet connection and try again.',
    });
    this.name = 'NetworkError';
  }
}

/**
 * Timeout errors
 */
export class TimeoutError extends AppError {
  constructor(message: string = 'Request timeout', context?: ErrorContext) {
    super({
      code: ErrorCode.TIMEOUT_ERROR,
      message,
      context,
      timestamp: new Date().toISOString(),
      recoverable: true,
      retryable: true,
      userMessage: 'The request took too long to complete. Please try again.',
    });
    this.name = 'TimeoutError';
  }
}

/**
 * API errors
 */
export class ApiError extends AppError {
  public readonly statusCode?: number;

  constructor(
    message: string,
    statusCode?: number,
    code: ErrorCode = ErrorCode.API_ERROR,
    context?: ErrorContext,
    originalError?: Error
  ) {
    super({
      code,
      message,
      context: { ...context, statusCode },
      originalError,
      timestamp: new Date().toISOString(),
      recoverable: statusCode ? statusCode < 500 : true,
      retryable: statusCode ? statusCode >= 500 : false,
      userMessage: getApiUserMessage(statusCode, message),
    });
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

/**
 * Validation errors
 */
export class ValidationError extends AppError {
  public readonly field?: string;

  constructor(message: string, field?: string, context?: ErrorContext) {
    super({
      code: ErrorCode.VALIDATION_ERROR,
      message,
      context: { ...context, field },
      timestamp: new Date().toISOString(),
      recoverable: true,
      retryable: false,
      userMessage: field ? `${field}: ${message}` : message,
    });
    this.name = 'ValidationError';
    this.field = field;
  }
}

/**
 * Business rule violation errors
 */
export class BusinessRuleError extends AppError {
  constructor(message: string, context?: ErrorContext) {
    super({
      code: ErrorCode.BUSINESS_RULE_VIOLATION,
      message,
      context,
      timestamp: new Date().toISOString(),
      recoverable: false,
      retryable: false,
      userMessage: message,
    });
    this.name = 'BusinessRuleError';
  }
}

/**
 * Gets user-friendly message for API errors
 */
function getApiUserMessage(statusCode: number | undefined, defaultMessage: string): string {
  if (!statusCode) {
    return defaultMessage;
  }

  switch (statusCode) {
    case 400:
      return 'Invalid request. Please check your input and try again.';
    case 401:
      return 'You are not authorized to perform this action. Please log in.';
    case 403:
      return 'You do not have permission to access this resource.';
    case 404:
      return 'The requested resource was not found.';
    case 429:
      return 'Too many requests. Please wait a moment and try again.';
    case 500:
    case 502:
    case 503:
    case 504:
      return 'Server error. Please try again later.';
    default:
      return defaultMessage;
  }
}

/**
 * Error handler utility
 */
export class ErrorHandler {
  /**
   * Handles an error and converts it to an AppError if needed
   */
  static handle(error: unknown, context?: ErrorContext): AppError {
    if (error instanceof AppError) {
      return error;
    }

    if (error instanceof Error) {
      // Try to extract more information from the error
      if (error.message.includes('timeout') || error.name === 'AbortError') {
        return new TimeoutError(error.message, context, error);
      }

      if (error.message.includes('network') || error.message.includes('fetch')) {
        return new NetworkError(error.message, error, context);
      }

      return new AppError({
        code: ErrorCode.UNKNOWN_ERROR,
        message: error.message,
        context,
        originalError: error,
        timestamp: new Date().toISOString(),
        recoverable: false,
        retryable: false,
      });
    }

    return new AppError({
      code: ErrorCode.UNKNOWN_ERROR,
      message: 'An unknown error occurred',
      context,
      timestamp: new Date().toISOString(),
      recoverable: false,
      retryable: false,
    });
  }
}
