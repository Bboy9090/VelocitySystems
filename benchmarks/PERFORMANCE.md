# Performance & Correctness Metrics
## Universal Core Benchmarks

This document defines performance targets and correctness guarantees for the Universal Core and both doctrines.

---

## Universal Core Performance Targets

### Audit System

**Append Latency**
- Target: < 5ms (p99)
- Measurement: Time from `audit.append()` call to record persisted
- Critical: Must not block execution

**Chain Verification**
- Target: < 1s for 1M records
- Measurement: Time to verify entire chain integrity
- Critical: Must complete for evidence export

**Merkle Root Computation**
- Target: < 500ms for 1M records
- Measurement: Time to compute Merkle root
- Critical: Required for evidence bundles

### Policy Engine

**Evaluation Latency**
- Target: < 50ms (p99)
- Measurement: Time from intent to decision
- Critical: User-facing operation

**Rule Matching**
- Target: < 10ms per rule
- Measurement: Time to match against rule set
- Critical: Scales with rule count

### Authority System

**Capability Check**
- Target: < 10ms (p99)
- Measurement: Time to verify capability
- Critical: Every action checks this

**Grant Operation**
- Target: < 20ms (p99)
- Measurement: Time to grant capability
- Critical: User-facing operation

**Expiry Processing**
- Target: < 100ms for 10K capabilities
- Measurement: Time to process all expiries
- Critical: Background operation

### Approval System

**Request Creation**
- Target: < 30ms (p99)
- Measurement: Time to create approval request
- Critical: User-facing operation

**Approval Resolution**
- Target: < 50ms (p99)
- Measurement: Time to approve/deny
- Critical: User-facing operation

### Export System

**Evidence Bundle Creation**
- Target: < 10s for 1M records
- Measurement: Time to create complete bundle
- Critical: Legal/regulatory requirement

**Bundle Verification**
- Target: < 2s for 1M records
- Measurement: Time to verify bundle integrity
- Critical: Evidence validation

---

## Doctrine-Specific Targets

### Velocity Systems

**One-Click Execution**
- Target: < 100ms end-to-end
- Measurement: Click to execution complete
- Critical: User experience

**UI Friction Score**
- Target: 0 (no blocking dialogs)
- Measurement: Number of confirmations required
- Critical: Speed-first philosophy

**Capability Persistence**
- Target: Instant (no expiry by default)
- Measurement: Capability lifetime
- Critical: Flow preservation

**Silent Audit**
- Target: < 5ms (hidden from user)
- Measurement: Audit write latency
- Critical: Must not slow execution

### Phoenix Forge

**Approval Time**
- Target: < 24h (human review)
- Measurement: Request to approval
- Critical: Governance requirement

**Justification Collection**
- Target: < 30s user time
- Measurement: Time to provide justification
- Critical: User experience

**Evidence Export**
- Target: < 5s for typical bundle
- Measurement: Export creation time
- Critical: Audit readiness

**Policy Enforcement**
- Target: < 50ms evaluation
- Measurement: Policy check time
- Critical: Every action

---

## Correctness Guarantees

### Audit System

**Integrity**
- ✅ Hash chain never breaks
- ✅ Records never modified
- ✅ Append-only enforced
- ✅ Merkle root always valid

**Completeness**
- ✅ Every action logged
- ✅ No silent failures
- ✅ All metadata captured
- ✅ Doctrine context preserved

### Policy Engine

**Consistency**
- ✅ Same intent → same decision
- ✅ Deterministic evaluation
- ✅ No race conditions
- ✅ Rule priority enforced

**Correctness**
- ✅ Matches declared rules
- ✅ No false positives
- ✅ No false negatives
- ✅ Conditions evaluated correctly

### Authority System

**Validity**
- ✅ Expired capabilities rejected
- ✅ Revoked capabilities rejected
- ✅ Expiry enforced correctly
- ✅ State transitions valid

**Completeness**
- ✅ All grants recorded
- ✅ All revocations recorded
- ✅ All expiries recorded
- ✅ History preserved

### Approval System

**State Management**
- ✅ No state corruption
- ✅ Transitions valid
- ✅ Expiry handled correctly
- ✅ Dual approval enforced

**Completeness**
- ✅ All requests recorded
- ✅ All resolutions recorded
- ✅ All expiries recorded
- ✅ History preserved

---

## Load Testing Scenarios

### Scenario 1: High-Volume Actions (Velocity)
- **Load**: 10K actions/minute
- **Target**: < 100ms p99 latency
- **Success Criteria**: No failures, all logged

### Scenario 2: Approval Workflow (Phoenix)
- **Load**: 1K approvals/hour
- **Target**: < 24h approval time
- **Success Criteria**: All approved, evidence complete

### Scenario 3: Evidence Export
- **Load**: 1M records
- **Target**: < 10s bundle creation
- **Success Criteria**: Valid bundle, integrity verified

### Scenario 4: Chain Verification
- **Load**: 10M records
- **Target**: < 30s verification
- **Success Criteria**: Integrity confirmed

---

## Monitoring & Alerting

### Critical Alerts
- Audit chain integrity violation
- Policy evaluation > 100ms
- Capability check > 50ms
- Evidence export failure
- Kill-switch activation

### Warning Alerts
- Audit append > 10ms
- Chain verification > 5s
- Expiry processing > 1s
- Bundle creation > 30s

### Performance Dashboards
- Real-time latency (p50, p95, p99)
- Throughput (actions/second)
- Error rates
- System health

---

## Benchmarking Tools

### Audit Benchmarks
```rust
// benchmark_audit_append.rs
// Measures append latency under load
```

### Policy Benchmarks
```rust
// benchmark_policy_evaluation.rs
// Measures evaluation time for various rule sets
```

### Authority Benchmarks
```rust
// benchmark_capability_check.rs
// Measures capability verification time
```

### Export Benchmarks
```rust
// benchmark_evidence_export.rs
// Measures bundle creation time
```

---

## Continuous Improvement

### Weekly Reviews
- Performance trends
- Target achievement
- Optimization opportunities
- Load pattern analysis

### Monthly Goals
- Reduce p99 latency by 10%
- Increase throughput by 20%
- Zero correctness violations
- 100% target achievement

---

**Remember**: Performance without correctness is useless. Correctness without performance is impractical. We need both.
