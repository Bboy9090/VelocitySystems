# Phoenix Key / BootForge
## Universal Enterprise System

**Version:** 1.0.0  
**Status:** PRODUCTION-READY  
**Doctrine:** The Forge — Build nothing that cannot be repaired

---

## 🔱 WHAT THIS IS

Phoenix Key / BootForge is a **sovereign, offline-capable recovery and deployment system** designed for environments where trust, control, and durability are mandatory.

**This is not a tool. This is an institution.**

---

## 🏗️ ARCHITECTURE

### Core Principle: Single Canon

There is exactly one source of truth for:
- Licensing
- Entitlement
- Audit state
- Enforcement logic

**Location:** `/core`

### Structure

```
phoenix_key/
├── core/              # Canonical authority (THE LAW)
│   ├── license/      # Sign, verify, revoke, grace
│   ├── entitlement/  # Feature matrix, enforcement
│   ├── audit/        # Logging, sealing
│   └── env/          # Environment config
├── api/              # Flask backend (calls /core)
├── cli/              # Command-line tool (calls /core)
├── usb/              # Bootable runtime (calls /core)
├── build/            # Provenance, signing
└── docs/             # Enterprise doctrine
```

---

## 🔐 TRUST MODEL

### Key Hierarchy

```
Root Signing Key (offline)
  └── License Issuer Key (rotatable)
       └── Environment Keys (scoped)
            └── License Tokens (user-level)
```

### License Verification

- **Offline-capable** — No internet required
- **Deterministic** — Same input → same output
- **Revocable** — Issuer or license can be revoked
- **Graceful** — Expired licenses degrade, never brick

---

## 📋 LICENSING TIERS

### 🟢 Free

- Core recovery tools
- GParted, TestDisk, SMART Check
- Single seat
- Offline always allowed

### 🔵 Pro ($9-19/month)

- All tools unlocked
- OS installers
- Mac tools
- Automation enabled
- Up to 5 seats

### 🟣 Enterprise (Custom)

- Everything in Pro
- Organizations & teams
- Bulk operations
- Audit export
- SLA support
- 1000+ seats

---

## 🚀 QUICK START

### Development

```bash
# Install dependencies
pip install flask python-dotenv

# Set environment
export LICENSE_SIGNING_KEY=$(openssl rand -hex 32)
export PHOENIX_ENV=DEV

# Run API
cd phoenix_key/api
python3 phoenix_api.py
```

### Production

```bash
# Generate production keys (offline)
openssl genpkey -algorithm Ed25519 -out root_key.pem

# Set production environment
export PHOENIX_ENV=PROD
export LICENSE_SIGNING_KEY=<production_key_hex>

# Run with systemd
systemctl start phoenix-key-api
```

---

## 📚 DOCUMENTATION

- **[Enterprise Doctrine](docs/ENTERPRISE_DOCTRINE.md)** — Canon law
- **[Enterprise Readiness](docs/ENTERPRISE_READINESS.md)** — Checklist
- **[API Documentation](api/README.md)** — Endpoints
- **[CLI Documentation](cli/README.md)** — Command reference

---

## 🔒 SECURITY

### What We Log

- Actions
- Commands invoked
- License validations
- Privilege escalations

### What We Never Log

- User data
- Credentials
- File contents
- Personal identifiers

**Audit logs are append-only, tamper-evident, and exportable offline.**

---

## 🎯 ENTERPRISE FEATURES

### Canonical Enforcement

Every surface (UI, API, CLI, USB) calls `/core`:

```python
from core.core import get_core

core = get_core()
lic = core.authorize(token, "clonezilla", actor="user@example.com")
# Proceeds or raises PermissionError
```

### Audit Trail

Every action is logged with:
- Timestamp
- Actor
- Action
- Result
- Hash chain

### Binary Provenance

Every artifact includes:
- Build ID
- Git commit
- Core hash
- Entitlement matrix hash
- Signing status

---

## 🌐 DEPLOYMENT

### Replit (Development)

- Full UI/UX development
- API testing
- Live preview

### Native Build (Production)

- Hardware access
- USB flashing
- System integration

### Hybrid Workflow

1. Develop in Replit
2. Build in GitHub Actions
3. Deploy to production
4. Flash to USB

---

## 📊 STATUS

### ✅ Complete

- Canonical core modules
- License system
- Audit logging
- Binary provenance
- Enterprise doctrine
- API integration
- Stripe billing

### 🔄 In Progress

- Production key generation
- Legal documentation
- Enterprise contracts
- Support system

---

## 🔥 THE DOCTRINE

**Build nothing that cannot be repaired.**

This single principle unifies:
- BootForge (repairable infrastructure)
- Reforge OS (repairable systems)
- Phoenix Key (repairable identity)
- REFORGE Engine (repairable simulation)

**One doctrine. Multiple expressions.**

---

## 📞 SUPPORT

**For Individuals:**  
[Contact information]

**For Enterprises:**  
[Enterprise contact]

**For Governments:**  
[Government contact]

---

**Phoenix Key / BootForge**  
*Where verified systems are certified for return to service.*

**REIGNITE. REBUILD. REBOOT.**
