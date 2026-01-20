/**
 * Enterprise Dependency Injection Container
 * 
 * Lightweight DI container for managing service dependencies
 */

type ServiceFactory<T> = () => T;
type ServiceIdentifier<T = unknown> = string | symbol | (new (...args: any[]) => T);

interface ServiceRegistration<T> {
  factory: ServiceFactory<T>;
  singleton: boolean;
  instance?: T;
}

/**
 * Dependency Injection Container
 */
export class Container {
  private services = new Map<ServiceIdentifier, ServiceRegistration<unknown>>();

  /**
   * Registers a service with a factory function
   */
  register<T>(
    identifier: ServiceIdentifier<T>,
    factory: ServiceFactory<T>,
    singleton: boolean = true
  ): void {
    this.services.set(identifier, {
      factory,
      singleton,
    });
  }

  /**
   * Registers a singleton service instance
   */
  registerInstance<T>(identifier: ServiceIdentifier<T>, instance: T): void {
    this.services.set(identifier, {
      factory: () => instance,
      singleton: true,
      instance,
    });
  }

  /**
   * Resolves a service by identifier
   */
  resolve<T>(identifier: ServiceIdentifier<T>): T {
    const registration = this.services.get(identifier);

    if (!registration) {
      throw new Error(`Service not found: ${String(identifier)}`);
    }

    // Return existing instance if singleton
    if (registration.singleton && registration.instance) {
      return registration.instance as T;
    }

    // Create new instance
    const instance = registration.factory() as T;

    // Store instance if singleton
    if (registration.singleton) {
      registration.instance = instance;
    }

    return instance;
  }

  /**
   * Checks if a service is registered
   */
  has(identifier: ServiceIdentifier): boolean {
    return this.services.has(identifier);
  }

  /**
   * Clears all registered services (useful for testing)
   */
  clear(): void {
    this.services.clear();
  }
}

/**
 * Global container instance
 */
export const container = new Container();

/**
 * Decorator for injecting dependencies (for future use with class-based services)
 */
export function inject<T>(identifier: ServiceIdentifier<T>) {
  return function (target: any, propertyKey: string | symbol | undefined, parameterIndex: number) {
    // This is a placeholder for future decorator-based injection
    // For now, we use manual resolution
  };
}
