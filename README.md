# Universal Legend Status: Phoenix Forge & Velocity Systems

**One Engine. Two Doctrines. Zero Compromise.**

This is not two products. This is one universal engine expressing two opposing philosophies at the surface.

Same steel. Different creeds.

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
