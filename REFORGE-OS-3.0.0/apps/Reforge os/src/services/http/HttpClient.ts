/**
 * Enterprise HTTP Client
 * 
 * Centralized HTTP client with retry logic, error handling, and interceptors
 */

import { config } from '@config/environment';
import { logger } from '@core/logger/Logger';
import { AppError, ErrorHandler, NetworkError, TimeoutError, ApiError, ErrorCode } from '@core/errors/AppError';

export interface RequestOptions extends RequestInit {
  timeout?: number;
  retries?: number;
  retryDelay?: number;
}

export interface HttpResponse<T = unknown> {
  data: T;
  status: number;
  statusText: string;
  headers: Headers;
}

/**
 * HTTP Client with enterprise features
 */
export class HttpClient {
  private baseUrl: string;
  private defaultTimeout: number;
  private defaultRetries: number;
  private defaultRetryDelay: number;

  constructor(
    baseUrl: string = config.api.baseUrl,
    defaultTimeout: number = config.api.timeout,
    defaultRetries: number = config.api.retryAttempts,
    defaultRetryDelay: number = config.api.retryDelay
  ) {
    this.baseUrl = baseUrl;
    this.defaultTimeout = defaultTimeout;
    this.defaultRetries = defaultRetries;
    this.defaultRetryDelay = defaultRetryDelay;
  }

  /**
   * Makes a GET request
   */
  async get<T = unknown>(endpoint: string, options?: RequestOptions): Promise<HttpResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'GET',
    });
  }

  /**
   * Makes a POST request
   */
  async post<T = unknown>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<HttpResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Makes a PUT request
   */
  async put<T = unknown>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<HttpResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Makes a PATCH request
   */
  async patch<T = unknown>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<HttpResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Makes a DELETE request
   */
  async delete<T = unknown>(endpoint: string, options?: RequestOptions): Promise<HttpResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'DELETE',
    });
  }

  /**
   * Core request method with retry logic
   */
  private async request<T = unknown>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<HttpResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    const timeout = options.timeout ?? this.defaultTimeout;
    const retries = options.retries ?? this.defaultRetries;
    const retryDelay = options.retryDelay ?? this.defaultRetryDelay;

    // Prepare headers
    const headers = this.prepareHeaders(options.headers);

    // Prepare request options
    const requestOptions: RequestInit = {
      ...options,
      headers,
    };

    // Execute request with retry logic
    let lastError: Error | undefined;
    
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const response = await this.executeRequest<T>(url, requestOptions, timeout);
        
        // Log successful request
        logger.debug('HTTP request successful', {
          url,
          method: options.method || 'GET',
          status: response.status,
          attempt: attempt + 1,
        });

        return response;
      } catch (error) {
        lastError = ErrorHandler.handle(error, { url, attempt: attempt + 1, retries });

        // Don't retry on client errors (4xx) except 429
        if (error instanceof ApiError && error.statusCode) {
          if (error.statusCode >= 400 && error.statusCode < 500 && error.statusCode !== 429) {
            throw error;
          }
        }

        // Don't retry if no more attempts
        if (attempt >= retries) {
          break;
        }

        // Log retry attempt
        logger.warn('HTTP request failed, retrying', {
          url,
          attempt: attempt + 1,
          error: lastError.message,
        });

        // Wait before retry
        await this.delay(retryDelay * (attempt + 1)); // Exponential backoff
      }
    }

    // All retries exhausted
    logger.error('HTTP request failed after all retries', {
      url,
      retries,
      error: lastError?.message,
    });

    throw lastError || new NetworkError('Request failed after all retries', undefined, { url });
  }

  /**
   * Executes a single HTTP request
   */
  private async executeRequest<T>(
    url: string,
    options: RequestInit,
    timeout: number
  ): Promise<HttpResponse<T>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle non-OK responses
      if (!response.ok) {
        const error = await this.parseErrorResponse(response);
        throw error;
      }

      // Parse response
      const data = await this.parseResponse<T>(response);

      return {
        data,
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
      };
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof ApiError) {
        throw error;
      }

      if (error instanceof Error && error.name === 'AbortError') {
        throw new TimeoutError(`Request timeout after ${timeout}ms`, { url });
      }

      throw ErrorHandler.handle(error, { url });
    }
  }

  /**
   * Parses error response from API
   */
  private async parseErrorResponse(response: Response): Promise<ApiError> {
    let errorData: unknown;
    let errorMessage = response.statusText;

    try {
      errorData = await response.json();
      if (typeof errorData === 'object' && errorData !== null) {
        const data = errorData as Record<string, unknown>;
        errorMessage = 
          (data.detail as string) ||
          (data.message as string) ||
          (data.error as string) ||
          errorMessage;
      }
    } catch {
      // If JSON parsing fails, use status text
    }

    // Determine error code based on status
    let errorCode = ErrorCode.API_ERROR;
    if (response.status === 401) {
      errorCode = ErrorCode.API_UNAUTHORIZED;
    } else if (response.status === 403) {
      errorCode = ErrorCode.API_FORBIDDEN;
    } else if (response.status === 404) {
      errorCode = ErrorCode.API_NOT_FOUND;
    } else if (response.status === 422) {
      errorCode = ErrorCode.API_VALIDATION_ERROR;
    } else if (response.status >= 500) {
      errorCode = ErrorCode.API_SERVER_ERROR;
    }

    return new ApiError(errorMessage, response.status, errorCode, { responseData: errorData });
  }

  /**
   * Parses successful response
   */
  private async parseResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('content-type');
    
    if (contentType?.includes('application/json')) {
      return response.json() as Promise<T>;
    }
    
    if (contentType?.includes('text/')) {
      return response.text() as unknown as T;
    }
    
    if (contentType?.includes('application/octet-stream') || contentType?.includes('application/pdf')) {
      return response.blob() as unknown as T;
    }

    // Default to JSON
    try {
      return await response.json() as T;
    } catch {
      return response.text() as unknown as T;
    }
  }

  /**
   * Prepares request headers
   */
  private prepareHeaders(customHeaders?: HeadersInit): HeadersInit {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...this.getAuthHeaders(),
    };

    // Merge custom headers
    if (customHeaders) {
      if (customHeaders instanceof Headers) {
        customHeaders.forEach((value, key) => {
          headers[key] = value;
        });
      } else if (Array.isArray(customHeaders)) {
        customHeaders.forEach(([key, value]) => {
          headers[key] = value;
        });
      } else {
        Object.assign(headers, customHeaders);
      }
    }

    return headers;
  }

  /**
   * Gets authentication headers
   */
  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {};

    // Add admin API key if available
    const adminKey = localStorage.getItem('admin_api_key') || import.meta.env.VITE_ADMIN_API_KEY;
    if (adminKey) {
      headers['X-API-Key'] = adminKey;
    }

    // Add ownership confidence if available
    const ownershipConfidence = localStorage.getItem('ownership_confidence');
    if (ownershipConfidence) {
      headers['X-Ownership-Confidence'] = ownershipConfidence;
    }

    return headers;
  }

  /**
   * Utility delay function
   */
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * Default HTTP client instance
 */
export const httpClient = new HttpClient();
