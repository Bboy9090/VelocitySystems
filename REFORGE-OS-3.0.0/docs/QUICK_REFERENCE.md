# Quick Reference Guide

## Common Tasks

### Making an API Call

```typescript
import { useApi } from '@hooks/useApi';
import { forgeWorksApi } from '@services/api/ApiService';

const [state, execute] = useApi(
  () => forgeWorksApi.analyzeDevice(metadata),
  {
    onSuccess: (data) => console.log('Success:', data),
    onError: (error) => console.error('Error:', error),
  }
);
```

### Error Handling

```typescript
import { AppError, ErrorHandler } from '@core/errors/AppError';

try {
  // Your code
} catch (error) {
  const appError = ErrorHandler.handle(error);
  // Use appError.getUserMessage() for user-facing messages
}
```

### Logging

```typescript
import { logger } from '@core/logger/Logger';

logger.info('Operation started', { metadata });
logger.error('Operation failed', error, { context });
```

### Configuration

```typescript
import { config } from '@config/environment';

const apiUrl = config.api.baseUrl;
const timeout = config.api.timeout;
```

### Service Registration (Advanced)

```typescript
import { container } from '@core/di/Container';

container.register('MyService', () => new MyService());
const service = container.resolve<MyService>('MyService');
```

## File Locations

- **Core Infrastructure**: `src/core/`
- **Services**: `src/services/`
- **Components**: `src/components/`
- **Pages**: `src/pages/`
- **Hooks**: `src/hooks/`
- **Utils**: `src/utils/`
- **Types**: `src/types/`
- **Config**: `src/config/`

## Path Aliases

- `@/` → `src/`
- `@core/` → `src/core/`
- `@services/` → `src/services/`
- `@components/` → `src/components/`
- `@pages/` → `src/pages/`
- `@hooks/` → `src/hooks/`
- `@utils/` → `src/utils/`
- `@types/` → `src/types/`
- `@config/` → `src/config/`

## NPM Scripts

```bash
# Development
npm run dev              # Start dev server
npm run typecheck        # Type check
npm run lint             # Lint code
npm run format           # Format code

# Testing
npm run test             # Run tests
npm run test:coverage    # Coverage report
npm run test:e2e         # E2E tests

# Building
npm run build            # Build for production
npm run build:prod       # Production build
```

## Environment Variables

Key environment variables (see `.env.example`):
- `VITE_API_BASE_URL` - API base URL
- `VITE_API_TIMEOUT` - Request timeout
- `VITE_LOG_LEVEL` - Logging level
- `VITE_TRAPDOOR_ENABLED` - Enable trapdoor API

## Common Patterns

### Component with API Call

```typescript
import { useApi } from '@hooks/useApi';
import { forgeWorksApi } from '@services/api/ApiService';

function MyComponent() {
  const [state, execute] = useApi(
    () => forgeWorksApi.getOpsMetrics()
  );

  if (state.loading) return <Loading />;
  if (state.error) return <Error message={state.error.getUserMessage()} />;
  return <DataView data={state.data} />;
}
```

### Error Boundary

```typescript
import { ErrorHandler } from '@core/errors/AppError';

function ErrorBoundary({ error }: { error: unknown }) {
  const appError = ErrorHandler.handle(error);
  return <div>{appError.getUserMessage()}</div>;
}
```

## Best Practices

1. **Always use TypeScript types**
2. **Use AppError for errors**
3. **Use logger instead of console**
4. **Use useApi hook for API calls**
5. **Follow the file structure**
6. **Write tests for critical paths**

## Getting Help

- Check [Architecture Guide](ARCHITECTURE.md)
- Check [Development Guide](DEVELOPMENT.md)
- Check [Migration Guide](MIGRATION_GUIDE.md)
- Review existing code examples
