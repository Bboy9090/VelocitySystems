# Development Guide

## Prerequisites

- Node.js 20+ (use `.nvmrc` or `.node-version`)
- npm 10+
- Rust (stable)
- Python 3.14+ (for backend)

## Getting Started

### 1. Install Dependencies

```bash
cd "apps/Reforge os"
npm install
```

### 2. Environment Setup

Create a `.env` file in `apps/Reforge os/`:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8001
VITE_API_TIMEOUT=30000
VITE_API_RETRY_ATTEMPTS=3
VITE_API_RETRY_DELAY=1000

# Trapdoor Configuration
VITE_TRAPDOOR_BASE_URL=http://localhost:8001/api/trapdoor
VITE_TRAPDOOR_ENABLED=false

# Features
VITE_FEATURE_DEV_MODE=true
VITE_FEATURE_AUDIT_LOGGING=true
VITE_FEATURE_SHADOW_LOGS=false
VITE_FEATURE_BATCH_OPS=true

# Security
VITE_REQUIRE_AUTH=false
VITE_SESSION_TIMEOUT=3600000
VITE_MAX_RETRIES=3

# Logging
VITE_LOG_LEVEL=info
VITE_LOG_CONSOLE=true
VITE_LOG_REMOTE=false
```

### 3. Development Server

```bash
npm run dev
```

This will:
- Start the Vite dev server
- Launch the Tauri application
- Enable hot module replacement

## Code Quality

### Linting

```bash
# Check for linting errors
npm run lint

# Auto-fix linting errors
npm run lint:fix
```

### Formatting

```bash
# Format code
npm run format

# Check formatting
npm run format:check
```

### Type Checking

```bash
npm run typecheck
```

## Testing

### Unit Tests

```bash
# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

### E2E Tests

```bash
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

## Building

### Development Build

```bash
npm run build
```

### Production Build

```bash
npm run build:prod
```

## Project Structure

### Core Infrastructure

- `src/core/di/`: Dependency injection container
- `src/core/errors/`: Error handling infrastructure
- `src/core/logger/`: Logging system

### Services

- `src/services/api/`: API service layer
- `src/services/http/`: HTTP client

### Components

- `src/components/`: Reusable UI components
- `src/pages/`: Page-level components

### Hooks

- `src/hooks/`: Custom React hooks

## Best Practices

### 1. Type Safety
- Always use TypeScript types
- Avoid `any` types
- Use strict mode

### 2. Error Handling
- Use `AppError` for all errors
- Provide user-friendly messages
- Log errors appropriately

### 3. API Calls
- Use the `useApi` hook for API calls
- Handle loading and error states
- Implement retry logic where appropriate

### 4. Code Organization
- Follow the file structure
- Keep components small and focused
- Extract reusable logic into hooks

### 5. Testing
- Write tests for critical paths
- Test error cases
- Maintain good test coverage

## Git Workflow

### Pre-commit Hooks
- Automatic linting
- Type checking
- Tests

### Commit Messages
- Use conventional commits
- Be descriptive
- Reference issues

## Troubleshooting

### Common Issues

1. **Type errors**: Run `npm run typecheck`
2. **Lint errors**: Run `npm run lint:fix`
3. **Build failures**: Clear `node_modules` and reinstall
4. **Tauri issues**: Check Rust installation

### Getting Help

- Check documentation in `docs/`
- Review error logs
- Check GitHub issues
