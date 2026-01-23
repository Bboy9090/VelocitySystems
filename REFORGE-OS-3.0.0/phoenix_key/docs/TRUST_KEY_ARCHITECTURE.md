# Phoenix Key / BootForge
## Trust & Key Architecture

**Version:** 1.0.0  
**Status:** DESIGNED AND LOCKED

---

## 🔑 KEY HIERARCHY

### Four-Tier Model

```
ROOT SIGNING KEY (offline)
  └── LICENSE ISSUER KEY(S) (rotatable)
       └── ENVIRONMENT KEYS (scoped)
            └── LICENSE TOKENS (user-level)
```

### 1. Root Signing Key

**Purpose:** Signs Issuer Keys only

**Properties:**
- Generated offline
- Stored offline (air-gapped)
- Used rarely
- Rotation extremely rare

**If compromised:**
→ Entire trust chain must be re-established

### 2. License Issuer Keys

**Purpose:** Sign licenses

**Properties:**
- One per major generation
- Stored in hardened environment
- Delegated by Root Key
- Can be revoked
- Can be rotated

**Why this exists:**
- Stripe compromise ≠ total collapse
- Operator mistake ≠ platform death

### 3. Environment Keys

**Purpose:** Bind licenses to environment intent

**Examples:**
- PROD
- STAGING
- AIRGAP
- OEM

**Rule:** A PROD key cannot issue AIRGAP licenses.

### 4. License Tokens

**Purpose:** Grant feature access

**Contains:**
- Tier
- Seats
- Capabilities
- Expiry
- Org ID
- Issuer ID
- Environment
- Signature

**Validated without internet.**

---

## 🔐 CRYPTOGRAPHIC CHOICES

| Use | Algorithm | Reason |
|-----|-----------|--------|
| Root / Issuer | Ed25519 | Modern, fast, safe |
| License Tokens | HMAC-SHA256 | Offline & deterministic |
| Audit Sealing | SHA-256 | Proven, portable |

**You do not invent crypto.**

---

## 🔄 KEY ROTATION

### Rotation Without Collapse

Each license includes:
```json
{
  "issuer_id": "issuer-2026-01",
  "env": "PROD"
}
```

**Verification:**
1. Read `issuer_id`
2. Load corresponding public key
3. Verify signature

**Old keys remain valid until revoked.**

---

## 🚫 REVOCATION MODEL

### What Can Be Revoked

- Issuer key
- License token
- Capability subset

### What Cannot

- Root key silently
- User's access to their data

### Revocation Delivery

- **Online:** Sync list
- **Offline:** Bundled revocation file
- **USB:** Manual import supported

**No phoning home required.**

---

## ⚠️ EMERGENCY KILL-SWITCH

### Emergency Revoke Key

**Separate from Root**

**Cold storage**

**Can invalidate:**
- Issuer keys
- Entire license generations

**Used only if:**
- Issuer fully compromised
- Legal mandate
- Catastrophic breach

**Every activation is auditable and public.**

---

## 🔒 OFFLINE SURVIVABILITY

A Phoenix Key USB must:

- Validate licenses with embedded public keys
- Honor expiry + grace
- Honor revocation bundles
- Never brick tools due to connectivity

**Offline is first-class, not fallback.**

---

## ✅ VERIFICATION FLOW

**ALL SURFACES:**

```
Load license token
  ↓
Read issuer_id
  ↓
Load public key
  ↓
Verify signature
  ↓
Check revocation
  ↓
Check expiry / grace
  ↓
Authorize features
```

**No shortcut. No UI override.**

---

## 🛡️ FAILURE MODES

| Failure | Behavior |
|---------|----------|
| Expired | Grace → degrade |
| Revoked | Feature lock |
| Unknown issuer | Reject |
| Missing license | Free tier |
| Clock skew | Grace tolerance |

**Nothing explodes. Nothing bricks.**

---

**This architecture is institution-grade.**
