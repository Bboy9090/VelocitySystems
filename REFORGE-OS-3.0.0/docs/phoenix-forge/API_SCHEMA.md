# REFORGE OS API Schema
## OpenAPI 3.0 Specification

**Version:** 1.0.0  
**Base URL:** `https://api.reforgeos.com/v1`  
**Authentication:** Bearer Token (JWT)

---

## CORE PRINCIPLES

- **Read-only by default**
- **No repair triggers**
- **No bypass controls**
- **Evidence only**

---

## API OBJECTS

### Session

```yaml
Session:
  type: object
  properties:
    id:
      type: string
      format: uuid
      description: Unique session identifier
    device:
      $ref: '#/components/schemas/Device'
    platform:
      type: string
      enum: [apple, android, windows, console]
    status:
      type: string
      enum: [intake, diagnostics, stress_tests, decision, repair, post_validation, certified, closed]
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time
    technician:
      $ref: '#/components/schemas/Technician'
    consent:
      $ref: '#/components/schemas/Consent'
```

### TrustState

```yaml
TrustState:
  type: object
  properties:
    platform:
      type: string
      enum: [apple, android, windows, console]
    identity:
      $ref: '#/components/schemas/IdentityState'
    sensors:
      $ref: '#/components/schemas/SensorMatrix'
    calibration:
      $ref: '#/components/schemas/CalibrationState'
    pairing:
      $ref: '#/components/schemas/PairingState'
    osTrust:
      $ref: '#/components/schemas/OSTrustState'
    score:
      type: integer
      minimum: 0
      maximum: 100
      description: Platform-specific trust score
```

### StressResult

```yaml
StressResult:
  type: object
  properties:
    sessionId:
      type: string
      format: uuid
    platform:
      type: string
      enum: [apple, android, windows, console]
    tests:
      type: array
      items:
        $ref: '#/components/schemas/StressTest'
    telemetry:
      $ref: '#/components/schemas/Telemetry'
    graphs:
      type: object
      properties:
        thermal:
          type: string
          format: uri
          description: Thermal curve graph URL
        performance:
          type: string
          format: uri
          description: Performance graph URL
    completedAt:
      type: string
      format: date-time
```

### RiskAssessment

```yaml
RiskAssessment:
  type: object
  properties:
    lockoutRisk:
      $ref: '#/components/schemas/RiskScore'
    featureLossRisk:
      $ref: '#/components/schemas/RiskScore'
    dataLossRisk:
      $ref: '#/components/schemas/RiskScore'
    irreversibilityRisk:
      $ref: '#/components/schemas/RiskScore'
    overall:
      type: string
      enum: [low, medium, high, critical]
    explanation:
      type: string
      description: Plain English explanation
```

### ReadinessIndex

```yaml
ReadinessIndex:
  type: object
  properties:
    platform:
      type: string
      enum: [apple, android, windows, console]
    composite:
      type: integer
      minimum: 0
      maximum: 100
      description: Overall readiness score
    subscores:
      type: object
      properties:
        cpuStability:
          type: integer
          minimum: 0
          maximum: 100
        gpuConsistency:
          type: integer
          minimum: 0
          maximum: 100
        thermalHeadroom:
          type: integer
          minimum: 0
          maximum: 100
        storageReliability:
          type: integer
          minimum: 0
          maximum: 100
        realTimePerformance:
          type: integer
          minimum: 0
          maximum: 100
    assessment:
      type: string
      description: Human-readable assessment
```

### Certificate

```yaml
Certificate:
  type: object
  properties:
    id:
      type: string
      format: uuid
    sessionId:
      type: string
      format: uuid
    device:
      $ref: '#/components/schemas/Device'
    type:
      type: string
      enum: [basic, post_repair, professional_readiness]
    trustStatus:
      $ref: '#/components/schemas/TrustStatusSummary'
    readinessIndex:
      $ref: '#/components/schemas/ReadinessIndex'
    featureAvailability:
      type: object
      description: Feature availability matrix
    permanentLimitations:
      type: array
      items:
        type: string
    whatWasDone:
      type: object
      properties:
        diagnostics:
          type: array
          items:
            type: string
        repairs:
          type: array
          items:
            type: string
    whatWeWillNotGuarantee:
      type: array
      items:
        type: string
    signature:
      $ref: '#/components/schemas/Signature'
    hash:
      type: string
      description: SHA-256 hash for verification
    createdAt:
      type: string
      format: date-time
```

### LedgerEntry

```yaml
LedgerEntry:
  type: object
  properties:
    id:
      type: string
      format: uuid
    sessionId:
      type: string
      format: uuid
    timestamp:
      type: string
      format: date-time
    event:
      type: string
      enum: [intake, consent, diagnostics, stress_tests, decision, repair_start, repair_end, post_validation, certificate_issued]
    data:
      type: object
      description: Event-specific data
    technician:
      type: string
      description: Technician ID
    previousHash:
      type: string
      description: Hash of previous entry (chain)
    hash:
      type: string
      description: SHA-256 hash of this entry
```

---

## API ENDPOINTS

### Sessions

#### POST /sessions

Create a new diagnostic session.

**Request Body:**
```yaml
CreateSessionRequest:
  type: object
  required:
    - device
    - platform
    - technicianId
  properties:
    device:
      $ref: '#/components/schemas/Device'
    platform:
      type: string
      enum: [apple, android, windows, console]
    technicianId:
      type: string
```

**Response:** `201 Created`
```json
{
  "session": { "$ref": "#/components/schemas/Session" }
}
```

#### GET /sessions/{sessionId}

Retrieve session details.

**Response:** `200 OK`
```json
{
  "session": { "$ref": "#/components/schemas/Session" }
}
```

#### POST /sessions/{sessionId}/consent

Record consent and unlock diagnostics.

**Request Body:**
```yaml
ConsentRequest:
  type: object
  required:
    - ownershipAcknowledged
    - dataBoundary
    - riskAcknowledged
  properties:
    ownershipAcknowledged:
      type: boolean
    dataBoundary:
      type: string
      enum: [view, no_view]
    riskAcknowledged:
      type: boolean
```

**Response:** `200 OK`
```json
{
  "session": { "$ref": "#/components/schemas/Session" },
  "unlocked": ["diagnostics"]
}
```

### Diagnostics

#### POST /sessions/{sessionId}/diagnostics

Run Shadow Genius Diagnostics Engine (SGDE).

**Response:** `200 OK`
```json
{
  "trustState": { "$ref": "#/components/schemas/TrustState" },
  "gateStatus": "passed" | "blocked",
  "blockReason": "string (if blocked)"
}
```

#### GET /sessions/{sessionId}/trust-state

Get current trust state.

**Response:** `200 OK`
```json
{
  "trustState": { "$ref": "#/components/schemas/TrustState" }
}
```

### Stress Tests

#### POST /sessions/{sessionId}/stress-tests

Start stress test suite.

**Request Body:**
```yaml
StressTestRequest:
  type: object
  properties:
    platform:
      type: string
      enum: [apple, android, windows, console]
    tests:
      type: array
      items:
        type: string
      description: Specific tests to run (optional, defaults to all)
```

**Response:** `202 Accepted`
```json
{
  "testId": "uuid",
  "status": "running",
  "estimatedDuration": "PT30M"
}
```

#### GET /sessions/{sessionId}/stress-tests/{testId}

Get stress test results.

**Response:** `200 OK`
```json
{
  "result": { "$ref": "#/components/schemas/StressResult" }
}
```

### Risk Assessment

#### GET /sessions/{sessionId}/risk-assessment

Get risk assessment for proposed action.

**Query Parameters:**
- `action` (required): Proposed action type

**Response:** `200 OK`
```json
{
  "assessment": { "$ref": "#/components/schemas/RiskAssessment" }
}
```

### Decision

#### POST /sessions/{sessionId}/decision

Record decision (SAFE / RISK / STOP).

**Request Body:**
```yaml
DecisionRequest:
  type: object
  required:
    - decision
  properties:
    decision:
      type: string
      enum: [safe, risk, stop]
    rationale:
      type: string
      description: Required for RISK or STOP
    override:
      type: boolean
      description: True if overriding system recommendation
    overrideRationale:
      type: string
      description: Required if override is true
```

**Response:** `200 OK`
```json
{
  "decision": "safe" | "risk" | "stop",
  "session": { "$ref": "#/components/schemas/Session" }
}
```

### Phoenix Forge Certification

#### POST /sessions/{sessionId}/certify

Generate Phoenix Forge Device Health Certificate.

**Response:** `201 Created`
```json
{
  "certificate": { "$ref": "#/components/schemas/Certificate" }
}
```

#### GET /certificates/{certificateId}

Retrieve certificate by ID.

**Response:** `200 OK`
```json
{
  "certificate": { "$ref": "#/components/schemas/Certificate" }
}
```

#### GET /certificates/{certificateId}/verify

Verify certificate hash.

**Response:** `200 OK`
```json
{
  "valid": true,
  "hash": "sha256:xxxx...",
  "verifiedAt": "2025-01-XXT..."
}
```

### Ledger

#### GET /sessions/{sessionId}/ledger

Get immutable ledger for session.

**Response:** `200 OK`
```json
{
  "entries": [
    { "$ref": "#/components/schemas/LedgerEntry" }
  ],
  "chainValid": true
}
```

### Health & Readiness

#### GET /health

Health check endpoint.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_ms": 12345
}
```

#### GET /readiness

Get system readiness index.

**Response:** `200 OK`
```json
{
  "platforms": {
    "apple": { "$ref": "#/components/schemas/ReadinessIndex" },
    "android": { "$ref": "#/components/schemas/ReadinessIndex" },
    "windows": { "$ref": "#/components/schemas/ReadinessIndex" },
    "console": { "$ref": "#/components/schemas/ReadinessIndex" }
  }
}
```

---

## AUTHENTICATION

### Bearer Token (JWT)

```http
Authorization: Bearer <token>
```

**Token Claims:**
- `sub`: User ID
- `tier`: Certification tier (I, II, III)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

---

## ERROR RESPONSES

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {},
    "correlationId": "uuid"
  }
}
```

### Common Error Codes

- `GATE_BLOCKED` — Cannot proceed past gate
- `INSUFFICIENT_AUTHORITY` — Tier level too low
- `SESSION_NOT_FOUND` — Invalid session ID
- `INVALID_STATE` — Session in wrong state
- `EVIDENCE_MISSING` — Required evidence not present

---

## RATE LIMITING

- **Default:** 100 requests/minute per API key
- **Burst:** 20 requests/second
- **Headers:**
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## VERSIONING

- **Current:** `v1`
- **Deprecation:** 12 months notice
- **Breaking changes:** New major version

---

**This API provides truth, not tools.**
