# REFORGE OS — Unified Platform Architecture

**Hardware + Infrastructure Only**

This document describes the complete unified platform architecture, synthesizing Bobby's Workshop, BootForge USB, and ForgeWorks into REFORGE OS.

---

## Platform Overview

REFORGE OS is a **compliance-first, hardware-anchored platform** for device diagnostics, repair intelligence, and lawful recovery routing.

**Core Principle**: We provide analysis and routing, never execution of circumvention.

---

## Three-Layer Architecture

### Layer 1: Bobby's Workshop (Public UX Layer)

**Purpose**: Trust, Education, UX, Community, Reports

**Components**:
- Device analysis dashboards
- Legal classifications
- Guided repair intelligence (non-circumventing)
- Customer-facing transparency
- Certification & training

**Technology Stack**:
- Frontend: React/TypeScript (from Bobby's Workshop 3.0)
- UI Framework: Tailwind CSS
- Desktop: Tauri (cross-platform)

**From Sources**:
- Bobby's Workshop UI/UX components
- Dashboard designs
- Workflow visualization
- Educational content

---

### Layer 2: ForgeWorks Core (Compliance Spine)

**Purpose**: Device analysis, ownership verification, legal classification, audit logging

**Components**:
- Device detection & enumeration (BootForge USB foundation)
- Status evaluation
- Ownership verification
- Jurisdiction-aware legal classification
- External authority routing
- Immutable audit logging

**Technology Stack**:
- Backend: Rust (BootForge USB core)
- Services: Microservices architecture
- Database: SQLite (local) + Postgres (cloud)
- APIs: REST + WebSocket

**From Sources**:
- BootForge USB enumeration library
- Device detection logic
- USB communication protocols
- Platform orchestration (from BootForge Platform)

---

### Layer 3: Pandora Codex (Internal Vault)

**Purpose**: R&D knowledge, risk modeling, classification logic

**Components**:
- Historical exploit knowledge (for risk classification only)
- Grey-zone understanding (for legal interpretation)
- Risk scoring algorithms
- Device capability classification

**Access**: Enterprise/Research tier only, hardware-serial bound

**From Sources**:
- Pandora Codex knowledge base
- Risk assessment frameworks
- Legal interpretation logic

---

## Hardware Integration

### ForgeCore Diagnostic Bridge

**Role**: Hardware trust anchor

**Capabilities**:
- Device enumeration
- Diagnostic data collection
- Secure element authentication
- License tier verification
- Audit log anchoring

**Integration Points**:
- USB enumeration (BootForge USB library)
- Secure element handshake (ForgeWorks Core)
- Device analysis (Bobby's Workshop UI)

### Smart Thermal Platform

**Role**: Repair tool integration

**Capabilities**:
- Temperature-controlled repair operations
- Profile management
- Safety monitoring

**Integration Points**:
- Guided repair workflows (Bobby's Workshop)
- Safety compliance (ForgeWorks Core)

---

## Infrastructure Components

### Device Detection Service

**Source**: BootForge USB + Bobby's Workshop device detection

**Functions**:
- Cross-platform USB enumeration
- Device classification (iOS/Android/Unknown)
- Capability detection
- Real-time monitoring

**Technology**:
- Rust (BootForge USB core)
- libusb/rusb integration
- Platform-specific APIs (Windows SetupAPI, Linux udev, macOS IOKit)

### Ownership Verification Service

**Functions**:
- Ownership attestation
- Authorization documentation
- Legal basis verification

**Storage**: Encrypted, audit-logged

### Legal Classification Service

**Functions**:
- Jurisdiction detection
- Legal status classification
- Risk assessment
- Precedent mapping

**Input**: Pandora Codex knowledge (classification logic only)

**Output**: Legal pathways, authorization requirements

### Audit Logging Service

**Functions**:
- Immutable log creation
- Timestamped entries
- Hardware-serial binding
- Export capabilities

**Storage**: Local + cloud sync (optional)

### External Routing Service

**Functions**:
- OEM pathway identification
- Carrier unlock eligibility
- Court order processing
- Executor documentation routing

**Output**: Compliance-ready documentation

---

## Data Flow Architecture

```
┌─────────────────────────────────────────┐
│   ForgeCore Hardware (USB Connected)    │
│  • Device Detection                      │
│  • Diagnostic Collection                 │
│  • Secure Element Auth                   │
└─────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────┐
│     ForgeWorks Core Services            │
│  • Device Analysis Service               │
│  • Ownership Verification                │
│  • Legal Classification                  │
│  • Audit Logging                         │
│  • External Routing                      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
┌──────────────────┐   ┌──────────────────┐
│ Bobby's Workshop │   │ Pandora Codex    │
│   (Public UI)    │   │  (Internal R&D)  │
│                  │   │                  │
│ • Dashboards     │   │ • Risk Models    │
│ • Reports        │   │ • Classification │
│ • Workflows      │   │ • Precedents     │
└──────────────────┘   └──────────────────┘
```

---

## Service Architecture

### Microservices Layout

```
services/
├── device-analysis/          # BootForge USB integration
│   ├── enumeration/
│   ├── classification/
│   └── diagnostics/
│
├── ownership-verification/   # ForgeWorks Core
│   ├── attestation/
│   ├── documentation/
│   └── verification/
│
├── legal-classification/     # ForgeWorks Core
│   ├── jurisdiction/
│   ├── risk-assessment/
│   └── routing/
│
├── audit-logging/            # ForgeWorks Core
│   ├── log-creation/
│   ├── storage/
│   └── export/
│
└── external-routing/         # ForgeWorks Core
    ├── oem-paths/
    ├── carrier-eligibility/
    └── documentation/
```

---

## Technology Stack (Synthesized)

### Backend

- **Core**: Rust (BootForge USB foundation)
- **Services**: Rust microservices
- **APIs**: REST (FastAPI-equivalent in Rust) + WebSocket
- **Database**: SQLite (local) + Postgres (cloud)
- **Messaging**: Internal message bus

### Frontend

- **Framework**: React + TypeScript (Bobby's Workshop 3.0)
- **UI**: Tailwind CSS
- **Desktop**: Tauri (from Bobby's Workshop)
- **State**: Zustand/Redux

### Hardware Integration

- **USB**: libusb/rusb (BootForge USB)
- **Secure Element**: Microchip ATECC608B SDK
- **PD Control**: TI TPS6598x driver
- **Thermal Control**: STM32F0 firmware

---

## Deployment Architecture

### Local Deployment

- Desktop application (Tauri)
- Local SQLite database
- Direct hardware access
- Offline capability

### Cloud Deployment (Optional)

- Web dashboard
- Cloud Postgres database
- API gateway
- Hardware-limited features

### Hybrid Deployment

- Desktop for hardware operations
- Cloud for analytics & reporting
- Sync between platforms

---

## Security Architecture

### Hardware Security

- **Secure Element**: Per-unit provisioning
- **Firmware Signing**: Cryptographic signatures
- **Anti-Tamper**: Physical protection

### Software Security

- **Audit Logs**: Immutable, cryptographically signed
- **Access Control**: Role-based + hardware binding
- **Data Encryption**: At-rest and in-transit
- **Secure Storage**: Credentials never stored

---

## Compliance Architecture

### Legal Compliance

- **Jurisdiction Awareness**: Region-specific rules
- **Risk Classification**: Automatic assessment
- **Authorization Gates**: Required before actions
- **Documentation**: Compliance-ready reports

### Regulatory Compliance

- **GDPR**: Data minimization, right to deletion
- **CCPA**: Privacy controls
- **Export Control**: Classification & controls
- **Industry Standards**: ISO 9001, SOC 2 (planned)

---

## Integration Points from Source Repositories

### From BootForge USB

- ✅ USB enumeration core (`src/enumerate/`)
- ✅ Device type detection (`src/types.rs`)
- ✅ Platform-specific enrichment (Windows/Linux/macOS)
- ✅ USB device information structures

### From Bobby's Workshop

- ✅ UI/UX components
- ✅ Dashboard designs
- ✅ Workflow visualization
- ✅ Device detection UI (`probeDevice.ts` concepts)
- ✅ Real-time monitoring

### From Bobby's Workshop 3.0

- ✅ React/TypeScript frontend
- ✅ Tauri desktop integration
- ✅ Service architecture patterns
- ✅ API structures

### From Pandora Codex (Internal)

- ✅ Risk classification logic
- ✅ Legal interpretation frameworks
- ✅ Device capability knowledge
- ✅ Precedent mapping (never ships publicly)

---

## Platform Evolution

### Phase 1: Foundation ✅

- USB enumeration (BootForge USB)
- Basic device detection
- Hardware BOM finalized

### Phase 2: Core Services (In Progress)

- Device analysis service
- Ownership verification
- Legal classification
- Audit logging

### Phase 3: Integration

- UI integration (Bobby's Workshop)
- Workflow automation
- Cloud services (optional)

### Phase 4: Ecosystem

- Certification program
- Third-party integrations
- Enterprise features

---

## Key Architectural Principles

1. **Hardware-First**: Hardware anchors trust and access
2. **Compliance-Embedded**: Legal checks in every layer
3. **Analysis-Only**: No execution of circumvention
4. **Audit-Everything**: Immutable logs for all actions
5. **Modular Design**: Services can evolve independently
6. **Clear Boundaries**: Public vs internal strictly enforced

---

**Document Version**: 1.0  
**Status**: ARCHITECTURE FINAL  
**Last Updated**: Unified Platform Architecture