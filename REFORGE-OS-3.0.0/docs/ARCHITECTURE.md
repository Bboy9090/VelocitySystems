# REFORGE OS - Enterprise Architecture

## Overview

REFORGE OS is an enterprise-grade device analysis and compliance platform built with modern technologies and best practices.

## Technology Stack

### Frontend
- **Framework**: React 18.2+ with TypeScript
- **Build Tool**: Vite 7.3+
- **Desktop Framework**: Tauri 1.5+
- **Styling**: Tailwind CSS 3.3+
- **State Management**: React Hooks (Context API)

### Backend
- **Rust**: Tauri backend for system integration
- **Python**: FastAPI backend for business logic
- **API**: RESTful API with OpenAPI documentation

### Development Tools
- **TypeScript**: Strict type checking
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Vitest**: Unit and integration testing
- **Playwright**: End-to-end testing
- **Husky**: Git hooks for quality gates

## Architecture Principles

### 1. Separation of Concerns
- **Core**: Infrastructure (logging, errors, DI)
- **Services**: Business logic and API clients
- **Components**: UI components
- **Pages**: Page-level components
- **Hooks**: Reusable React hooks
- **Utils**: Utility functions
- **Types**: TypeScript type definitions
- **Config**: Configuration management

### 2. Dependency Injection
- Lightweight DI container for service management
- Singleton and transient service registration
- Testable and mockable services

### 3. Error Handling
- Standardized error types with error codes
- Context-aware error messages
- User-friendly error messages
- Retry logic for transient failures

### 4. Logging
- Structured logging with levels
- Context-aware logging
- Remote logging support
- Log buffering for batch processing

### 5. Configuration Management
- Environment-based configuration
- Type-safe configuration
- Validation on startup
- Feature flags support

## File Structure

```
apps/Reforge os/
├── src/
│   ├── core/              # Core infrastructure
│   │   ├── di/            # Dependency injection
│   │   ├── errors/        # Error handling
│   │   └── logger/        # Logging
│   ├── config/            # Configuration
│   ├── services/          # Business logic
│   │   ├── api/           # API services
│   │   └── http/          # HTTP client
│   ├── components/        # UI components
│   ├── pages/             # Page components
│   ├── hooks/             # React hooks
│   ├── utils/             # Utilities
│   ├── types/             # TypeScript types
│   └── styles/            # Stylesheets
├── src-tauri/             # Tauri backend
├── assets/                # Static assets
├── tests/                 # Test files
└── docs/                  # Documentation
```

## API Architecture

### Service Layer
- **ForgeWorksApiService**: Core device analysis APIs
- **TrapdoorApiService**: Admin/secret room APIs
- **CustodialClosetApiService**: Solutions database APIs

### HTTP Client
- Centralized HTTP client with retry logic
- Automatic error handling and conversion
- Request/response interceptors
- Timeout management

## Security

### Authentication
- API key authentication
- Ownership confidence headers
- Session management

### Data Protection
- No sensitive data in logs
- Encrypted shadow logs
- Secure credential storage

## Testing Strategy

### Unit Tests
- Service layer tests
- Utility function tests
- Hook tests

### Integration Tests
- API integration tests
- Component integration tests

### E2E Tests
- User flow tests
- Critical path tests

## Deployment

### Build Process
1. Type checking
2. Linting
3. Testing
4. Building
5. Packaging

### Environments
- **Development**: Local development
- **Staging**: Pre-production testing
- **Production**: Live environment

## Performance

### Optimization
- Code splitting
- Lazy loading
- Tree shaking
- Minification

### Monitoring
- Error tracking
- Performance metrics
- User analytics

## Future Enhancements

- [ ] State management library (Zustand/Redux)
- [ ] GraphQL API support
- [ ] Real-time updates (WebSockets)
- [ ] Offline support
- [ ] Progressive Web App features
- [ ] Micro-frontend architecture
