# REFORGE OS — API Boundaries

## Core Principle

APIs expose **analysis and classification**, never execution.

---

## ✅ Allowed API Domains

### `/device/analyze`
- Input: device metadata
- Output: security state, capability class

### `/ownership/verify`
- Input: attestations, documentation hashes
- Output: confidence score

### `/legal/classify`
- Input: device + region
- Output: permitted / conditional / prohibited

### `/route/authority`
- Input: classification result
- Output: OEM / carrier / court pathways

### `/audit/log`
- Input: action labels
- Output: immutable audit receipt

---

## ❌ Forbidden API Domains (Never Implement)

- `/execute`
- `/bypass`
- `/unlock`
- `/root`
- `/jailbreak`
- `/apply`

**If an endpoint would change a device, it does not belong.**

---

## API Design Principles

1. **Analysis only** — no execution endpoints
2. **Classification** — legal status determination
3. **Routing** — external authority guidance
4. **Logging** — immutable audit trails

---

**APIs are interfaces, not instruments.**