# REFORGE OS — Service Architecture

**Microservices Design for Compliance-First Platform**

---

## Service Overview

REFORGE OS uses a microservices architecture to separate concerns and enable independent scaling. All services follow the **analysis-only, no execution** principle.

---

## Core Services

### 1. Device Analysis Service

**Purpose**: Device enumeration, classification, and diagnostic data collection

**Technology**: Rust (BootForge USB foundation)

**Endpoints**:
- `POST /device/enumerate` — Enumerate all connected devices
- `GET /device/:id` — Get device information
- `GET /device/:id/classify` — Classify device type
- `GET /device/:id/diagnostics` — Collect diagnostic data

**Data Sources**:
- BootForge USB enumeration
- Hardware diagnostic bridge (ForgeCore)
- Platform-specific APIs

**Compliance**:
- Read-only operations
- No device modification
- Audit logging required

---

### 2. Ownership Verification Service

**Purpose**: Verify device ownership and authorization

**Technology**: Rust + SQLite/Postgres

**Endpoints**:
- `POST /ownership/verify` — Verify ownership claim
- `POST /ownership/attest` — Submit ownership attestation
- `GET /ownership/:id/status` — Get verification status
- `GET /ownership/:id/documentation` — Get verification docs

**Data Storage**:
- Encrypted attestation records
- Hashed documentation
- Audit logs

**Compliance**:
- GDPR-compliant data handling
- Encryption at rest
- Audit trail required

---

### 3. Legal Classification Service

**Purpose**: Classify legal status and risk

**Technology**: Rust

**Endpoints**:
- `POST /legal/classify` — Classify device scenario
- `GET /legal/jurisdiction/:region/rules` — Get jurisdiction rules
- `POST /legal/risk-assessment` — Assess risk level
- `GET /legal/precedent/:scenario` — Get legal precedent info

**Data Sources**:
- Jurisdiction databases
- Legal precedent mapping
- Pandora Codex (classification logic only, internal)

**Compliance**:
- No legal advice provided
- Analysis and classification only
- External authority routing

---

### 4. Audit Logging Service

**Purpose**: Create immutable audit logs

**Technology**: Rust + SQLite/Postgres

**Endpoints**:
- `POST /audit/log` — Create audit log entry
- `GET /audit/:id` — Retrieve audit log
- `GET /audit/export` — Export audit logs (compliance)
- `POST /audit/sign` — Hardware-signed audit entry

**Features**:
- Immutable log storage
- Cryptographic signing
- Hardware anchoring (ForgeCore)
- Export capabilities

**Compliance**:
- Tamper-proof storage
- Timestamped entries
- Hardware-attested logs

---

### 5. External Routing Service

**Purpose**: Route to external authorities

**Technology**: Rust

**Endpoints**:
- `POST /route/oem` — Generate OEM request pathway
- `POST /route/carrier` — Generate carrier unlock pathway
- `POST /route/court` — Generate court order pathway
- `GET /route/authorization-checklist` — Get required docs

**Outputs**:
- Authorization checklists
- Contact information
- Documentation requirements
- Compliance-ready forms

**Compliance**:
- No execution of routing
- Information and guidance only
- External authority responsibility

---

## Service Communication

### Internal Message Bus

Services communicate via:
- **REST APIs** (synchronous operations)
- **Message Queue** (asynchronous operations)
- **WebSocket** (real-time updates)

### Service Discovery

- Service registry (etcd/Consul-style)
- Health checks
- Load balancing

---

## Data Flow Between Services

```
Device Analysis Service
    ↓ (device info)
Ownership Verification Service
    ↓ (ownership status)
Legal Classification Service
    ↓ (legal status)
External Routing Service (if needed)
    ↓ (all operations)
Audit Logging Service (every step)
```

---

## Hardware Integration Services

### ForgeCore Communication Service

**Purpose**: Interface with ForgeCore hardware

**Technology**: Rust (USB communication)

**Functions**:
- Hardware handshake
- License verification
- Audit log signing
- Diagnostic data collection

**Integration**:
- Direct USB communication
- Secure element access
- Firmware attestation

---

## Compliance Services

### Jurisdiction Detection Service

**Purpose**: Detect user jurisdiction

**Functions**:
- IP-based detection (optional)
- Manual selection
- Regional rule application

### Risk Assessment Service

**Purpose**: Assess operational risk

**Functions**:
- Scenario analysis
- Risk scoring
- Compliance checking

**Sources**:
- Legal classification service
- Pandora Codex (risk models, internal only)

---

## Service Deployment

### Local Deployment

- All services run locally
- SQLite databases
- Direct hardware access
- Offline capability

### Cloud Deployment (Optional)

- Cloud Postgres
- API gateway
- Load balancing
- Horizontal scaling

### Hybrid Deployment

- Local services for hardware operations
- Cloud services for analytics
- Sync between deployments

---

## Service Security

### Authentication

- Hardware-serial binding
- Role-based access control
- Multi-factor authentication

### Authorization

- Service-to-service authentication
- API key management
- OAuth 2.0 (optional, for cloud)

### Encryption

- TLS for all communications
- Encryption at rest
- Secure key management

---

## Service Monitoring

### Health Checks

- Service availability
- Hardware connectivity
- Database connectivity
- External service status

### Metrics

- Request rates
- Error rates
- Latency
- Hardware usage

### Logging

- Structured logging
- Log aggregation
- Error tracking
- Audit trail

---

## Service Dependencies

### Internal Dependencies

```
Device Analysis → Ownership Verification
Device Analysis → Legal Classification
All Services → Audit Logging
Legal Classification → External Routing
```

### External Dependencies

- Hardware (ForgeCore)
- Operating System (USB, file system)
- Optional: Cloud services (if cloud deployment)

---

## Service Versioning

- Semantic versioning (v1.0.0)
- API versioning (/v1/...)
- Backward compatibility maintained
- Deprecation notices provided

---

**Document Version**: 1.0  
**Status**: SERVICE ARCHITECTURE FINAL  
**Last Updated**: Unified Service Design