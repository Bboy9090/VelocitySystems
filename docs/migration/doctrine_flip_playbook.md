# Doctrine-Flip Migration Playbook
## Velocity ➜ Phoenix (Without Chaos)

This is how customers "grow up" inside your empire, not outside it.

## The Core Rule (Non-Negotiable)

**Doctrine is a lens, not a rewrite.**

History is never altered. Only how it is enforced and surfaced changes.

This preserves:
- Legal continuity
- Data integrity
- Credibility

## What Flipping a Doctrine Actually Does

| Layer | What Changes | What Never Changes |
|-------|-------------|-------------------|
| UI | Friction, warnings, approvals | Data |
| Defaults | Expiry, approvals | Audit chain |
| Policy | Allow → AllowWithApproval | Policy history |
| Messaging | Speed → Accountability | Events |
| Enforcement | Fail-open → Fail-closed | Evidence |

**No migrations. No schema changes. No reprocessing.**

## Flip Sequence (Safe, Ordered)

### Step 1: Shadow Governance (Silent)

Phoenix policies begin evaluating in parallel:
- No enforcement
- No UI exposure
- Decision deltas logged privately

**Output**: "Here's what would've required approval."

**Duration**: 1-2 weeks

**Customer Experience**: No change visible

### Step 2: Read-Only Revelation

Customer sees:
- Risk reports
- Expired-would-have-expired notices
- Silent approvals
- Policy compliance scores

**Still no blocking.**

**Duration**: 1 week

**Customer Experience**: "We're showing you what governance would look like"

### Step 3: Partial Enforcement

New actions require approval:
- Old persistent powers remain
- Expiry introduced only for new grants
- Existing capabilities grandfathered

**This avoids revolt.**

**Duration**: 2-4 weeks

**Customer Experience**: "New actions need approval, but your existing permissions work"

### Step 4: Full Doctrine Lock

All authority time-boxed:
- Dual approvals enforced
- Regulator mode available
- Complete Phoenix Forge experience

**No shock. No data loss. No lies.**

**Duration**: Permanent

**Customer Experience**: "You're now running Phoenix Forge"

## The Selling Line (Use Verbatim)

**"You don't lose speed. You gain survivability."**

## Technical Implementation

### 1. Load Phoenix Doctrine
```rust
let phoenix_doctrine = load_doctrine("phoenix_forge")?;
kernel.load_policies(phoenix_doctrine.policies);
```

### 2. Shadow Mode
```rust
let shadow_result = phoenix_policy_engine.evaluate(&context);
// Log delta but don't enforce
audit_log.append(..., "shadow_evaluation", ...);
```

### 3. Gradual Enforcement
```rust
if is_new_capability {
    enforce_phoenix_policy();
} else {
    // Grandfathered - allow
}
```

### 4. Full Flip
```rust
kernel.set_doctrine("phoenix_forge");
kernel.enforce_all_policies();
```

## Rollback Plan

If customer needs to revert:
1. Flip back to Velocity doctrine
2. All history preserved
3. No data loss
4. Audit trail shows flip events

## Success Metrics

- Zero data loss
- Zero downtime
- Customer satisfaction maintained
- Audit trail complete
- Legal continuity preserved

## Common Objections

**"This will slow us down"**
→ "Only new actions require approval. Existing permissions work."

**"We don't need this"**
→ "This is optional. You can stay in shadow mode indefinitely."

**"What if we want to go back?"**
→ "One command. All history preserved."

---

**Version**: 1.0  
**Last Updated**: 2024
