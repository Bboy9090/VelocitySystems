# Operational Playbook
## Real-World Ops & Incidents

This playbook covers operational procedures for both Phoenix Forge and Velocity Systems.

---

## Incident Response Procedures

### Severity Levels

**P0 - System Down**
- Kill-switch activated
- All writes blocked
- Immediate response required

**P1 - Critical Function Broken**
- Core feature unavailable
- Workaround exists
- Response within 1 hour

**P2 - Degraded Performance**
- System functional but slow
- User impact moderate
- Response within 4 hours

**P3 - Minor Issue**
- Cosmetic or edge case
- Workaround available
- Response within 24 hours

---

## Common Incidents

### Incident: Audit Chain Integrity Violation

**Symptoms**:
- `verify_chain()` returns false
- Merkle root mismatch
- Hash chain broken

**Response (Phoenix)**:
1. Immediately stop all writes
2. Export current evidence bundle
3. Identify first violation point
4. Investigate root cause
5. Document in audit log
6. Restore from backup if needed

**Response (Velocity)**:
1. Same as Phoenix (core integrity is non-negotiable)
2. Access hidden audit
3. Export evidence
4. Investigate
5. Velocity UI may not show this, but core must be fixed

**Prevention**:
- Never modify audit records
- Always use append-only interface
- Verify chain integrity periodically

---

### Incident: Capability Over-Permissioning

**Symptoms**:
- User has broader access than intended
- Expired capabilities still active
- Revoked capabilities still working

**Response (Phoenix)**:
1. Identify over-permissioned users
2. Revoke excessive capabilities
3. Review approval history
4. Update policies
5. Document in audit

**Response (Velocity)**:
1. Same revocation process
2. May be discovered later (silent audit)
3. Fix and move on
4. Consider if this indicates need for Phoenix

**Prevention**:
- Regular capability audits
- Expiry enforcement
- Principle of least privilege

---

### Incident: Approval Bypass

**Symptoms**:
- Action executed without required approval
- Approval registry shows no record
- Policy violation

**Response (Phoenix)**:
1. This should never happen (fail-closed)
2. If it does, core bug
3. Stop all execution
4. Investigate core logic
5. Fix and verify

**Response (Velocity)**:
1. This is expected (approvals optional)
2. Verify it was intentional
3. Check if policy should change
4. Document decision

**Prevention**:
- Core enforcement (not UI-only)
- Policy engine testing
- Regular audits

---

### Incident: Truth Escrow Access Request

**Symptoms**:
- Court order received
- Regulatory inquiry
- Legal proceeding

**Response (Both)**:
1. Verify authorization (dual-key or court order)
2. Notify System Owners
3. Unseal escrow (if authorized)
4. Export evidence bundle
5. Document access in audit
6. Re-seal after access

**Prevention**:
- Regular escrow integrity checks
- Access logging
- Authorization verification

---

### Incident: Kill-Switch Activation

**Symptoms**:
- All writes blocked
- System read-only
- Emergency state

**Response**:
1. Verify reason (dual-key holders)
2. Assess situation
3. Fix root cause
4. Deactivate (dual-key + justification)
5. Document in audit

**Prevention**:
- Proper authorization
- Clear procedures
- Regular drills

---

## Daily Operations

### Morning Checklist
- [ ] Verify audit chain integrity
- [ ] Check for expired capabilities
- [ ] Review overnight approvals (Phoenix)
- [ ] Check system health metrics
- [ ] Review error logs

### Weekly Tasks
- [ ] Capability audit
- [ ] Policy review
- [ ] Performance metrics review
- [ ] Truth escrow integrity check
- [ ] Team training session

### Monthly Tasks
- [ ] Full system audit
- [ ] Doctrine compliance review
- [ ] Performance optimization
- [ ] Documentation update
- [ ] Team assessment

---

## Performance Monitoring

### Key Metrics

**Velocity Systems**:
- Action execution time (target: <100ms)
- UI friction score (target: minimal)
- Capability grant time (target: instant)
- Audit write latency (target: <10ms)

**Phoenix Forge**:
- Approval time (target: <24h)
- Policy evaluation time (target: <50ms)
- Evidence export time (target: <5s)
- Audit chain verification (target: <1s)

**Universal Core** (Both):
- Audit append latency (target: <5ms)
- Chain verification time (target: <1s)
- Merkle root computation (target: <500ms)
- Evidence bundle creation (target: <10s)

---

## Escalation Paths

### Level 1: Operator
- Handles routine operations
- Uses playbooks
- Escalates unknowns

### Level 2: Architect
- Designs solutions
- Handles complex incidents
- Trains operators

### Level 3: Master
- Owns doctrine decisions
- Handles kill-switch
- Manages truth escrow

### Level 4: Sovereign
- System ownership
- Strategic decisions
- Doctrine creation

---

## Communication Templates

### Incident Report
```
INCIDENT: [Title]
SEVERITY: [P0-P3]
DETECTED: [Timestamp]
RESPONDER: [Name]
SYMPTOMS: [Description]
ROOT CAUSE: [If known]
RESOLUTION: [Steps taken]
PREVENTION: [Future measures]
AUDIT REF: [Audit record ID]
```

### Status Update
```
STATUS: [Resolved/In Progress/Escalated]
UPDATE: [Current state]
NEXT STEPS: [Actions]
ETA: [If applicable]
```

---

## Recovery Procedures

### Data Loss Prevention
- Regular backups
- Audit chain preservation
- Evidence bundle exports
- Capability registry snapshots

### System Restoration
1. Stop all writes
2. Export current state
3. Restore from backup
4. Verify integrity
5. Resume operations
6. Document in audit

---

## Post-Incident Review

### Review Questions
1. What happened?
2. Why did it happen?
3. How was it detected?
4. How was it resolved?
5. What can we prevent?
6. What did we learn?

### Action Items
- [ ] Fix root cause
- [ ] Update playbooks
- [ ] Train team
- [ ] Update monitoring
- [ ] Document lessons

---

**Remember**: The core always records. Even if the product hides it, the truth exists.
