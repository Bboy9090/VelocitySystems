# Architecture Overview

## The Universal Legend Stack

This architecture implements a **universal engine** that powers two opposing philosophies: **Phoenix Forge** (governance-first) and **Velocity Systems** (speed-first).

## Core Principle

**Never fork the engine. Fork how authority is interpreted.**

## Directory Structure

```
/platform
├── universal-core/          # Shared engine (NEVER diverges)
│   ├── audit/              # Immutable audit chains
│   │   ├── append.rs      # Append-only log writer
│   │   ├── verify.rs      # Chain integrity verification
│   │   └── merkle.rs      # Merkle tree for evidence
│   ├── policy/            # Policy evaluation
│   │   ├── engine.rs      # Policy engine
│   │   ├── decision.rs    # Decision logic
│   │   └── intent.rs      # Intent evaluation
│   ├── authority/         # Capability management
│   │   ├── capability.rs  # Capability lifecycle
│   │   ├── expiry.rs      # Expiry management
│   │   └── revoke.rs      # Revocation
│   ├── approval/          # Approval workflows
│   │   ├── request.rs     # Approval requests
│   │   └── resolution.rs  # Approval resolution
│   ├── export/            # Evidence export
│   │   ├── evidence.rs    # Evidence bundles
│   │   └── bundle.rs      # Bundle management
│   ├── kernel.rs          # Central integration
│   └── sdk/               # SDKs (Rust, TypeScript)
│
├── doctrines/             # Philosophy layer (divergence happens here)
│   ├── phoenix_forge/
│   │   ├── defaults.yaml      # Governance-first defaults
│   │   ├── policy_lawbook.yaml # Strict policies
│   │   ├── ui_constraints.ts   # High-friction UI
│   │   ├── risk_model.rs      # Reality-assuming risk model
│   │   └── messaging.md        # Brand voice
│   └── velocity_systems/
│       ├── defaults.yaml       # Speed-first defaults
│       ├── policy_lite.yaml    # Minimal policies
│       ├── ui_constraints.ts   # Low-friction UI
│       ├── risk_model.rs      # Trust-assuming risk model
│       └── messaging.md        # Brand voice
│
├── products/              # Product surfaces
│   ├── phoenix-forge/
│   │   ├── ui/            # React components
│   │   ├── branding/      # CSS themes
│   │   └── site/          # Marketing site
│   └── velocity-systems/
│       ├── ui/            # React components
│       ├── branding/      # CSS themes
│       └── site/          # Marketing site
│
├── governance/            # Internal controls
│   ├── internal_charter.md # Governance rules
│   ├── kill_switch.rs     # Emergency stop
│   └── truth_escrow.rs    # Sealed evidence
│
└── docs/                  # Documentation
    ├── migration/         # Doctrine flip playbook
    ├── sales/             # Sales guides
    └── manifesto/         # Strategic documents
```

## Data Flow

### Phoenix Forge Flow
1. User creates intent → **Requires justification**
2. Policy evaluation → **AllowWithApproval (default)**
3. Approval required → **Block until approved**
4. Execution → **Logged with full context**
5. Audit → **Surfaced to user**

### Velocity Systems Flow
1. User creates intent → **No justification required**
2. Policy evaluation → **Allow (default)**
3. Approval optional → **Proceed with warning**
4. Execution → **Logged (but not surfaced)**
5. Audit → **Silent by default**

### Universal Core (Both)
- **Always logs everything** (immutably)
- **Always maintains audit chain** (hash-linked)
- **Always can export evidence** (legal-grade)
- **Never alters history** (append-only)

## Doctrine Flip Process

1. **Shadow Mode**: Phoenix policies evaluate in parallel (no enforcement)
2. **Revelation**: Show what would require approval (read-only)
3. **Partial Enforcement**: New actions require approval (old permissions grandfathered)
4. **Full Flip**: Complete Phoenix doctrine (all policies enforced)

**No migration. No data loss. No rewrite.**

## Truth Escrow

Even when Velocity doesn't surface audit logs, the core still records everything. This is **truth escrowed**:

- Cannot be deleted
- Cannot be edited
- Cannot be accessed by normal admins
- Can only be unsealed by:
  - Court order
  - Regulator
  - System Owner (dual-key)

## Kill Switch

Emergency stop mechanism:
- Freezes all write actions
- Revokes all capabilities
- Forces read-only mode
- Seals truth escrow
- Emits self-audit (EXTREME severity)

Requires **dual-key** authorization.

## Key Design Decisions

1. **Single Engine**: One codebase, never forked
2. **Doctrine Layer**: Philosophy expressed as configuration
3. **Always Log**: Core never lies, even if product hides it
4. **Immutable History**: Append-only, hash-chained
5. **Evidence Export**: Legal-grade bundles on demand
6. **Doctrine Flip**: Same data, different interpretation

## Why This Works

- **Velocity customers** get speed without losing the option to flip
- **Phoenix customers** get governance without losing performance
- **Both** share the same audit trail, same evidence, same truth
- **You** control the narrative and the migration path

---

**This is not common. This is rare. This is legendary.**
