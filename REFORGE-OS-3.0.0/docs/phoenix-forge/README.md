# REFORGE OS + Phoenix Forge
## Shadow Genius Bar System Documentation

**Version:** 1.0.0  
**Status:** COMPLETE DOCUMENTATION PACKAGE

---

## OVERVIEW

This documentation package contains the complete specification for the REFORGE OS + Phoenix Forge Shadow Genius Bar system.

**Reforge OS** is the operating system that certifies device truth.  
**Phoenix Forge** is where verified systems are certified for return to service.

---

## DOCUMENTATION STRUCTURE

### 1. Architecture
- **[SHADOW_GENIUS_ARCHITECTURE.md](./SHADOW_GENIUS_ARCHITECTURE.md)**
  - Complete system architecture
  - Platform-specific engines (SGDE-A, SGDE-Android, SGDE-W, SGDE-C)
  - Gate enforcement model
  - Risk engine categories
  - Health scoring outputs

### 2. Public Credibility Kit
- **[PUBLIC_CREDIBILITY_KIT.md](./PUBLIC_CREDIBILITY_KIT.md)**
  - Homepage copy
  - How it works
  - Why we refuse repairs
  - Why stress beats benchmarks
  - Sample Device Health Certificate
  - Platform coverage

### 3. Enterprise Pitch Deck
- **[ENTERPRISE_PITCH_DECK.md](./ENTERPRISE_PITCH_DECK.md)**
  - 10-12 slide enterprise pitch
  - Problem statement
  - Solution overview
  - Platform coverage
  - Productized services
  - SLAs & compliance
  - Integrations

### 4. API Schema
- **[API_SCHEMA.md](./API_SCHEMA.md)**
  - Complete API documentation
  - Core principles
  - API objects
  - Endpoints
  - Authentication
  - Error responses

- **[openapi.yaml](./openapi.yaml)**
  - OpenAPI 3.0 specification
  - Machine-readable API definition
  - Ready for code generation

### 5. Pricing & Packaging
- **[PRICING_PACKAGING.md](./PRICING_PACKAGING.md)**
  - Tier structure (Individual, Business, Enterprise, Insurer)
  - Platform-specific pricing
  - Certificate types
  - Add-on services
  - Volume discounts
  - SLAs
  - Payment terms

---

## QUICK START

### For Developers

1. **Review Architecture**
   - Start with `SHADOW_GENIUS_ARCHITECTURE.md`
   - Understand gate enforcement model
   - Review platform-specific engines

2. **API Integration**
   - Read `API_SCHEMA.md` for endpoint details
   - Use `openapi.yaml` for code generation
   - Test against staging environment

3. **Implementation**
   - Follow gate enforcement model
   - Implement SGDE modules per platform
   - Integrate Phoenix Forge certification

### For Business Development

1. **Enterprise Sales**
   - Use `ENTERPRISE_PITCH_DECK.md` as slide deck
   - Customize for specific prospects
   - Reference `PRICING_PACKAGING.md` for pricing

2. **Public Materials**
   - Use `PUBLIC_CREDIBILITY_KIT.md` for website copy
   - Generate sample certificates
   - Publish "Why we refuse repairs" page

3. **Customer Education**
   - Share "Why stress beats benchmarks"
   - Explain gate enforcement model
   - Show sample certificates

---

## KEY CONCEPTS

### Gate Enforcement

Every session moves through gated states. Technicians cannot skip forward.

```
INTAKE → CONSENT → DIAGNOSTICS → TRUST GATE
     → STRESS TESTS → DECISION → REPAIR
     → POST-VALIDATION → CERTIFICATE → CLOSE
```

**Each gate requires specific evidence.**  
Not checkboxes. Evidence.

### Decision Layer

System outputs **ONLY** one:

- ✅ **SAFE** — Proceed with confidence
- ⚠️ **RISK** — Proceed with disclosed risk
- ⛔ **STOP** — Do not proceed

**No "maybe."**  
**No override without logging.**

### Phoenix Forge Certification

Immutable, hash-verified Device Health Certificates that include:

- Trust status summary
- Professional Readiness Index (0-100)
- Feature availability matrix
- Permanent limitations (disclosed upfront)
- What we will NOT guarantee

**If it isn't certified, it isn't claimed.**

---

## PLATFORM SUPPORT

### Apple (SGDE-A)
- macOS trust verification
- iOS device assessment
- Calibration state tracking
- Pairing integrity validation

### Android (SGDE-Android)
- Bootloader state verification
- OEM security profiling
- Account lock assessment
- Modem & radio stability

### Windows (SGDE-W)
- Firmware & Secure Boot validation
- TPM & encryption state
- Driver coherence assessment
- Thermal & power truth

### Game Consoles (SGDE-C)
- Firmware & ban-risk assessment
- Hardware pairing verification
- Thermal stability validation
- Network trust evaluation

---

## CERTIFICATION TIERS

### 🟢 Tier I — Intake & Ethics
- Consent accuracy
- Stop conditions
- No repairs

### 🔵 Tier II — Diagnostics & Stress
- SGDE mastery
- Stress execution
- Correct decisions

### 🔴 Tier III — Repair Authority
- Platform judgment
- Risk disclosure
- Override discipline
- Refusal competence

**Certs expire. Overrides are loud. Revocation is real.**

---

## INTEGRATION POINTS

### API Access
- Read-only by default
- Evidence access only
- No repair triggers
- No bypass controls

### External Systems
- **Ticketing:** ServiceNow, Jira
- **Asset Management:** Intune, Jamf
- **Insurers:** Claim attachments
- **Vendors:** Pre/post validation

---

## NEXT STEPS

### Implementation
1. Build SGDE modules per platform
2. Implement gate enforcement
3. Create Phoenix Forge certificate generator
4. Integrate with existing REFORGE OS infrastructure

### Business Development
1. Customize pitch deck for prospects
2. Set up staging environment for demos
3. Create sample certificates
4. Launch public website

### Operations
1. Train staff on certification tiers
2. Set up immutable ledger
3. Configure gate enforcement
4. Establish SLAs

---

## SUPPORT

**Questions?**  
Contact: [Support contact]

**API Issues?**  
See: [API_SCHEMA.md](./API_SCHEMA.md)

**Business Inquiries?**  
See: [ENTERPRISE_PITCH_DECK.md](./ENTERPRISE_PITCH_DECK.md)

---

**REFORGE OS + Phoenix Forge**  
*Where verified systems are certified for return to service.*
