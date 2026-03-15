# VelocitySystems

**VelocitySystems** is a universal platform architecture that implements a doctrine-agnostic engine powering two opposing philosophies for access control, governance, and authority management: **Phoenix Forge** (governance-first) and **Velocity Systems** (speed-first).

**One Engine. Two Doctrines. Zero Compromise.**

This is not two products. This is one universal engine expressing two opposing philosophies at the surface—enabling organizations to choose speed early and add governance later, without data loss, rewrites, or migration.

Same steel. Different creeds.

## Mission

To solve the fundamental tension between organizational speed and governance architecturally, not operationally. VelocitySystems enables businesses to:

- **Start Fast**: Deploy with Velocity Systems for speed and iteration
- **Grow Safe**: Flip to Phoenix Forge doctrine when compliance demands arise
- **Never Lose**: Maintain complete immutable history through doctrine changes
- **Control Migration**: Own the narrative and timeline from speed to governance

**Mission Statement**: Build nothing that cannot be repaired. Create systems where speed and compliance are not opposites, but phases of the same journey—backed by immutable truth and seamless doctrine migration.

## Core Modules

### Universal Core (`/universal-core/`)
The shared engine that never diverges. Always records reality.

- **Audit System**: Immutable, hash-chained append-only logs with Merkle tree verification
- **Policy Engine**: Intent evaluation, decision logic, and rule-based authorization
- **Authority System**: Capability lifecycle management with expiry and revocation
- **Approval System**: Approval request workflows and resolution with dual-approval support
- **Export System**: Legal-grade evidence bundles for regulatory compliance
- **Prometheus Engine**: Doctrine-aware cognitive system with structured LLM integration
- **Kernel**: Central integration point binding all core systems

### Doctrine Layer (`/doctrines/`)
Where philosophy splits. Same engine, different interpretation.

- **Phoenix Forge**: Governance-first, fail-closed, capabilities expire, approvals required, audit surfaced
- **Velocity Systems**: Speed-first, fail-open, capabilities persist, approvals optional, audit silent

### Product Surfaces (`/products/`)
Customer-facing implementations with distinct branding and user experiences.

- **Phoenix Forge UI**: High-friction, consequence-aware interface
- **Velocity Systems UI**: Low-friction, speed-optimized interface

### Governance (`/governance/`)
Internal controls and operational safeguards.

- **Internal Charter**: Rules for operating both doctrines
- **Kill Switch**: Emergency stop mechanism with dual-key authorization
- **Truth Escrow**: Sealed evidence system (court order/regulator access only)

### Game Engine (`/engine/`)
Enterprise-grade real-time graphics engine with Vulkan 1.3, custom ECS architecture, and GPU-driven rendering.

### REFORGE-OS (`/REFORGE-OS-3.0.0/`)
Operating system infrastructure layer with Python APIs and comprehensive subsystems.

### Training & Operations
- **Training**: Masterclass structured learning (Apprentice → Sovereign progression)
- **Roadmap**: Mastery path documentation
- **Playbooks**: Operational procedures and incident response
- **Benchmarks**: Performance metrics and targets
- **Registry**: Prometheus prompt registry (immutable, canon-locked)

## Tech Stack

### Core Technologies
- **Rust**: Universal core, SDKs, governance mechanisms, policy engine, audit chains
- **C++20/23**: Game engine runtime with enterprise-grade graphics
- **TypeScript**: UI constraints, frontend components, SDK implementations
- **Python**: REFORGE-OS APIs and utilities
- **YAML**: Doctrine configuration files

### Frameworks & Libraries
- **Cargo**: Rust package management and build system
- **CMake 3.20+**: C++ build system for game engine
- **Vulkan 1.3**: Explicit GPU rendering with manual synchronization
- **GLM**: Graphics math library
- **Jolt Physics**: Deterministic physics simulation
- **Serde**: Rust serialization with JSON support
- **SHA-256**: Cryptographic hashing (sha2 crate)
- **UUID**: Unique identification (uuid crate v1.0+)

### Web & API
- **Express.js 5.2.1**: Web server framework
- **CORS 2.8.6**: Cross-origin resource sharing
- **WebSocket (ws 8.19.0)**: Real-time communication

### Architectural Patterns
- **ECS (Entity Component System)**: Custom data-oriented design
- **GPU-Driven Rendering**: Minimal CPU submission, explicit synchronization
- **Fiber-Based Job System**: Lock-free parallelism
- **Immutable Audit Chains**: Hash-linked append-only logs with integrity verification
- **Memory-Mapped Assets**: Zero-copy, no runtime parsing
- **Fixed-Timestep Physics**: Deterministic, replayable simulations

## Use Cases

### Phoenix Forge (Governance-First)

**Target Markets**: Regulated industries (healthcare, finance, government), enterprises with compliance requirements, audit-ready organizations, high legal exposure companies.

**Key Use Cases**:
1. **Compliance & Audit Readiness**: Generate legal-grade evidence that stands up in court or regulatory inquiries
2. **Access Control Governance**: Every action justified with full, immutable audit trails
3. **Risk Management**: Fail-closed by default, prevents human error through mandatory approvals
4. **Legal Protection**: Defensible evidence for lawsuits and regulatory compliance (HIPAA, PCI-DSS, FedRAMP)
5. **Identity & Capability Management**: Time-limited permissions with justification requirements
6. **Operational Control**: Explicit approvals required for all critical actions

**Value Proposition**: "Speed is temporary. Audits are permanent. We don't slow you down—we make you unbreakable."

### Velocity Systems (Speed-First)

**Target Markets**: Early-stage startups, research labs, field operations, high-trust teams, internal tools, low-risk environments.

**Key Use Cases**:
1. **Rapid Iteration**: Minimal friction for development, testing, and experimentation
2. **Field Operations**: Emergency response requiring instant action without approval overhead
3. **Development Workflows**: Internal tools with minimal ceremony for skilled operators
4. **Experimental Environments**: Lab research prioritizing speed over governance
5. **Skill-Based Access**: Trust in experienced operators to move fast and investigate later
6. **Fail-Open Scenarios**: Prefer investigating incidents after-the-fact rather than preventing upfront

**Value Proposition**: "Velocity is built for teams who value speed over ceremony. Don't let compliance slow down your best people."

### Doctrine Migration (The "Legend Move")

**Scenario**: A Velocity customer grows up, faces audits, needs compliance, or encounters regulatory requirements.

**Solution**: Flip doctrines without rewriting, migrating, or losing history.

**Process**:
1. **Shadow Mode**: Phoenix policies evaluate in parallel (read-only, no enforcement)
2. **Revelation**: Show what would require approval under Phoenix doctrine
3. **Partial Enforcement**: New actions require approval, legacy permissions grandfathered
4. **Full Flip**: Complete transition to Phoenix governance

**Benefits**:
- Same engine (no rewrite)
- Same data (no migration)
- Same history (no loss)
- One command (automated)
- Immediate audit readiness

### Cross-Cutting Applications

1. **Cognitive AI Systems** (Prometheus Engine): Doctrine-aware LLM integration with structured prompt execution, validation, and adversarial critique
2. **Game Development**: Enterprise-grade real-time graphics with deterministic physics and GPU-driven rendering
3. **Infrastructure & Operations**: OS-level repairs, device detection, firmware management, diagnostics and recovery
4. **Training & Mastery**: Structured progression from novice to sovereign with operational playbooks and performance benchmarking

## Architecture Overview

```
/platform
├── universal-core/          # Shared engine (never diverges)
│   ├── audit/              # Immutable audit chains
│   ├── policy/             # Policy evaluation engine
│   ├── authority/          # Capability management
│   ├── approval/           # Approval workflows
│   ├── export/             # Evidence export
│   ├── prometheus/         # Doctrine-aware cognitive engine
│   ├── kernel.rs           # Central integration
│   └── sdk/                # Rust & TypeScript SDKs
│
├── doctrines/              # Philosophy layer (where divergence happens)
│   ├── phoenix_forge/      # Governance-first doctrine
│   └── velocity_systems/   # Speed-first doctrine
│
├── products/               # Product surfaces
│   ├── phoenix-forge/      # UI, branding, messaging
│   └── velocity-systems/   # UI, branding, messaging
│
├── governance/             # Internal controls
│   ├── internal_charter.md # Governance rules
│   ├── kill_switch.rs      # Emergency stop
│   └── truth_escrow.rs     # Sealed evidence
│
├── training/               # Training & mastery
│   └── MASTERCLASS.md      # Structured learning path
│
├── playbooks/              # Operational procedures
│   └── OPERATIONAL_PLAYBOOK.md # Real-world ops & incidents
│
├── benchmarks/             # Performance metrics
│   └── PERFORMANCE.md      # Targets & correctness guarantees
│
├── roadmap/                # Mastery progression
│   └── MASTERY_PATH.md     # Apprentice → Sovereign
│
├── registry/               # Prompt registry
│   ├── prometheus-registry.rs # Immutable prompt storage
│   └── prompts/            # Canon-locked prompts
│
├── ops/                    # Operations
│   └── ci/                 # CI/CD infrastructure
│
└── docs/                   # Documentation
    ├── migration/          # Doctrine flip playbook
    ├── sales/              # Sales guides
    └── manifesto/          # Strategic documents
```

## Core Principles

### Universal Core (Never Diverges)

The core always:
- ✅ Logs everything (immutably)
- ✅ Hash-chains records
- ✅ Knows the truth
- ✅ Can verify reality

**Even Velocity cannot escape this.**

The engine always remembers—even if the product pretends not to care.

### Doctrine Layer (Where Philosophy Splits)

**Phoenix Forge**:
- Capabilities expire
- Approvals required
- Justifications mandatory
- Audit surfaced
- Fail-closed always

**Velocity Systems**:
- Capabilities persist
- Approvals optional
- Justifications hidden
- Audit silent by default
- Fail-open preferred

**Same engine. Different answers to the same questions.**

## Quick Start

### Building the Universal Core

```bash
cd universal-core
cargo build
```

### Using Phoenix Forge Doctrine

```rust
use universal_core::Kernel;

let mut kernel = Kernel::new("phoenix_forge".to_string(), Some(Duration::from_secs(86400)));
// Load Phoenix policies
kernel.load_policies(phoenix_policies);
```

### Using Velocity Systems Doctrine

```rust
let mut kernel = Kernel::new("velocity_systems".to_string(), None);
// Load Velocity policies
kernel.load_policies(velocity_policies);
```

## The Legend Move

Because one day:

A Velocity customer grows up → Gets audited → Gets sued → Gets regulated

And you say:

**"We can flip your doctrine. Same engine. Same data. Same history."**

No migration. No rewrite. No data loss.

**That's legendary.**

## Hard Rules (Do Not Break)

1. ❌ Never market them together publicly
2. ❌ Never let Velocity disable the core
3. ❌ Never let Phoenix pretend speed is free
4. ❌ Never fork the engine
5. ✅ Always let history exist, even if hidden

**Break these and the empire fractures.**

## Documentation

### Core Systems
- [Architecture Overview](ARCHITECTURE.md) - System-level understanding
- [System Overview](SYSTEM_OVERVIEW.md) - Complete system documentation

### Training & Mastery
- [Masterclass](training/MASTERCLASS.md) - Structured learning path (Apprentice → Sovereign)
- [Mastery Path](roadmap/MASTERY_PATH.md) - Progression roadmap
- [Operational Playbook](playbooks/OPERATIONAL_PLAYBOOK.md) - Real-world ops & incidents
- [Performance Benchmarks](benchmarks/PERFORMANCE.md) - Targets & metrics

### Governance & Operations
- [Internal Governance Charter](governance/internal_charter.md) - Rules for operating both doctrines
- [Doctrine Flip Playbook](docs/migration/doctrine_flip_playbook.md) - How to migrate between doctrines
- [CI/CD Infrastructure](ops/ci/README.md) - Core-first deployment strategy

### Sales & Strategy
- [Sales Guides](docs/sales/) - How to sell each product honestly
- [Why We Built Both](docs/manifesto/why_both.md) - Strategic manifesto

### Prometheus Engine
- [Prompt Registry](registry/prometheus-registry.rs) - Immutable prompt storage
- [Canon Prompts](registry/prompts/) - Doctrine-locked prompt schemas

## License

This is a strategic architecture demonstration. All rights reserved.

---

**You're not building apps. You're building a civilization with two religions that share the same laws of physics.**

That's not common. That's rare. That's legendary.
