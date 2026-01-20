# Migration Guide: Upgrading to Enterprise Architecture

This guide helps you migrate existing code to use the new enterprise-grade infrastructure.

## Overview

The enterprise upgrade introduces:
- Centralized configuration management
- Dependency injection container
- Standardized error handling
- Structured logging
- Type-safe HTTP client
- Enterprise file structure

## Step 1: Update Imports

### Old API Service Usage

```typescript
// OLD
import { ForgeWorksAPI } from '../services/api';
const result = await ForgeWorksAPI.analyzeDevice(metadata);
```

### New API Service Usage

```typescript
// NEW
import { forgeWorksApi } from '@services/api/ApiService';
const result = await forgeWorksApi.analyzeDevice(metadata);
```

## Step 2: Error Handling

### Old Error Handling

```typescript
// OLD
try {
  const result = await apiCall();
} catch (error) {
  console.error('Error:', error);
  // Generic error handling
}
```

### New Error Handling

```typescript
// NEW
import { AppError, ErrorHandler } from '@core/errors/AppError';
import { logger } from '@core/logger/Logger';

try {
  const result = await apiCall();
} catch (error) {
  const appError = ErrorHandler.handle(error);
  logger.error('API call failed', appError);
  // Use appError.getUserMessage() for user-facing messages
}
```

## Step 3: Using the useApi Hook

### Old Pattern

```typescript
// OLD
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

const fetchData = async () => {
  setLoading(true);
  try {
    const result = await apiCall();
    setData(result);
  } catch (err) {
    setError(err);
  } finally {
    setLoading(false);
  }
};
```

### New Pattern

```typescript
// NEW
import { useApi } from '@hooks/useApi';
import { forgeWorksApi } from '@services/api/ApiService';

const [state, execute, reset] = useApi(
  () => forgeWorksApi.analyzeDevice(metadata),
  {
    onSuccess: (data) => {
      // Handle success
    },
    onError: (error) => {
      // Handle error
    },
  }
);

// state.data, state.loading, state.error
```

## Step 4: Configuration

### Old Configuration

```typescript
// OLD
const API_BASE = '/api/v1';
const API_TIMEOUT = 30000;
```

### New Configuration

```typescript
// NEW
import { config } from '@config/environment';

// Use config.api.baseUrl
// Use config.api.timeout
```

## Step 5: Logging

### Old Logging

```typescript
// OLD
console.log('Info:', data);
console.error('Error:', error);
```

### New Logging

```typescript
// NEW
import { logger } from '@core/logger/Logger';

logger.info('Operation completed', { metadata });
logger.error('Operation failed', error, { context });
```

## Step 6: File Structure

### Old Structure

```
src/
├── services/
│   └── api.ts
├── lib/
│   └── api-client.ts
└── utils/
    └── pdfExport.ts
```

### New Structure

```
src/
├── core/
│   ├── di/
│   ├── errors/
│   └── logger/
├── config/
│   └── environment.ts
├── services/
│   ├── api/
│   │   └── ApiService.ts
│   └── http/
│       └── HttpClient.ts
├── hooks/
│   └── useApi.ts
└── utils/
    └── pdfExport.ts
```

## Step 7: TypeScript Paths

Update imports to use path aliases:

```typescript
// OLD
import { Something } from '../../../core/errors/AppError';

// NEW
import { Something } from '@core/errors/AppError';
```

## Step 8: Environment Variables

### Old .env

```env
VITE_API_URL=http://localhost:8001
```

### New .env

```env
VITE_API_BASE_URL=http://localhost:8001
VITE_API_TIMEOUT=30000
VITE_API_RETRY_ATTEMPTS=3
VITE_LOG_LEVEL=info
# ... see docs/DEVELOPMENT.md for full list
```

## Step 9: Testing

### Old Test Setup

```typescript
// OLD - No standardized setup
```

### New Test Setup

```typescript
// NEW
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
// Tests use standardized setup from src/test/setup.ts
```

## Step 10: Build Configuration

The build system has been upgraded with:
- Production optimizations
- Code splitting
- Tree shaking
- Source maps (dev only)
- Asset optimization

No code changes needed - just run:

```bash
npm run build
```

## Common Patterns

### API Calls with Error Handling

```typescript
import { useApi } from '@hooks/useApi';
import { forgeWorksApi } from '@services/api/ApiService';
import { logger } from '@core/logger/Logger';

function MyComponent() {
  const [state, execute] = useApi(
    () => forgeWorksApi.analyzeDevice(metadata),
    {
      onError: (error) => {
        logger.error('Device analysis failed', error);
        // Show user-friendly error message
        showError(error.getUserMessage());
      },
    }
  );

  if (state.loading) return <Loading />;
  if (state.error) return <Error message={state.error.getUserMessage()} />;
  return <DataView data={state.data} />;
}
```

### Service Registration (Advanced)

```typescript
import { container } from '@core/di/Container';
import { forgeWorksApi } from '@services/api/ApiService';

// Register services
container.registerInstance('ForgeWorksApi', forgeWorksApi);

// Resolve services
const api = container.resolve<typeof forgeWorksApi>('ForgeWorksApi');
```

## Checklist

- [ ] Update all API service imports
- [ ] Replace error handling with AppError
- [ ] Replace console.log with logger
- [ ] Update configuration usage
- [ ] Migrate to useApi hook where applicable
- [ ] Update file structure
- [ ] Update environment variables
- [ ] Update tests
- [ ] Run type checking
- [ ] Run linting
- [ ] Test all functionality

## Need Help?

- Check [Architecture Guide](ARCHITECTURE.md)
- Check [Development Guide](DEVELOPMENT.md)
- Review existing migrated code
- Ask the development team
