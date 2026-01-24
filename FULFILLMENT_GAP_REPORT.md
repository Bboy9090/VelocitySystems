## What this repo *promises* (as written)

### Universal Legend Status (Phoenix Forge + Velocity Systems)
- A shared **Universal Core** that “never lies”:
  - Immutable audit log (hash-chained)
  - Policy evaluation engine
  - Capability lifecycle (grant/expiry/revoke)
  - Approval workflow
  - Evidence export bundles
  - “Prometheus” doctrine-aware cognitive engine
- A **doctrine layer** that can “flip” philosophy without rewriting/migrating.
- Product surfaces under `products/` that present different UX/branding.

### Bobby Dev Panel (Pandora Codex)
- A desktop UI (Tauri) that wraps backend modules into an “enterprise” app.
- Android diagnostics/control via ADB.
- iOS support via `libimobiledevice` tooling (detection + dossier).

---

## What it *actually does today* (based on code)

### ✅ Universal Core (Rust)
- **Builds successfully** (crate target fixed; compiles).
- Implements real data structures and logic for:
  - **Audit**: append-only records with hash chaining + verification + Merkle tree helpers
  - **Policy**: intent + rule evaluation skeleton
  - **Authority**: capabilities, expiry, revoke mechanisms
  - **Approval**: request + resolution structures
  - **Export**: evidence bundle structures
  - **Kernel**: ties the above together in a single orchestration surface
- **Prometheus** exists, but:
  - `PrometheusExecutor::generate_output()` is explicitly a **placeholder** (“would call LLM”)
  - critique/refinement/checklist steps are present, but not powered by a real model

### ✅ Bobby Dev Panel (Python backend)
- **Android via ADB**: real commands for dossier, logs, debloat (with device/OEM limitations).
- **Evidence / history / export**: real local hashing + SQLite + HTML/CSV/JSON export.
- Some modules are intentionally **simplified** (per `bobby_dev_panel/REALITY_CHECK.md`), e.g. CPU stress, sensor “dead” detection, “AI” (statistics).

### ⚠️ Desktop App (Tauri + React)
- UI exists and calls Rust commands.
- Rust commands:
  - **Device listing**: Android (`adb`) + iOS (`idevice_id`, `ideviceinfo`) are implemented.
  - Most “actions” ultimately call Python modules via subprocess.
- iOS is **not “full parity”** with Android:
  - Dossier/report have iOS branches, but many advanced modules are Android-only or require privileged access.

---

## What’s missing to fully fulfill the “promises”

### Universal Core
- **Real tests**: `cargo test` runs but there are currently **0 tests**, so correctness is not proven.
- **Prometheus LLM integration**:
  - Add a real model connector (local or API) and deterministic execution modes.
  - Add audit logging of prompts/inputs/outputs + redaction rules.
- **Policy ingestion**:
  - Current doctrine policy files are YAML; core policy engine needs a loader/parser and validation for those YAML rules.
- **“Doctrine flip” automation**:
  - The playbook exists in docs; a real implementation needs migration tooling, shadow evaluation, and UI/admin workflow.

### Bobby Dev Panel (device reality)
- **Android**:
  - Replace simplified CPU stress logic with a real stress mechanism.
  - Replace placeholder sensor testing with real per-sensor value sampling.
  - Clarify which Warhammer/debloat operations are “no-root” vs “root-required”, OEM-by-OEM.
- **iOS**:
  - Define scope explicitly:
    - “No-jailbreak” iOS via `libimobiledevice` is mostly **info/backup/log access** (varies).
    - Anything resembling “shell / deep modification” requires privileged access and is outside safe/normal support.
  - Wire UI flows to iOS-capable code paths and add feature gating when tools aren’t present.

### Desktop packaging
- **Embedded Python runtime** (if you want “works everywhere”):
  - Bundle a Python runtime + pinned deps, or enforce system Python with a preflight installer.
- **Installer readiness**:
  - Add icons, signing/notarization (macOS), Windows signing, and CI build scripts.

---

## Safety / compliance note

This repo should stay aligned to **diagnostics, repair, and authorized maintenance**. Anything intended to bypass security controls, unlock devices without authorization, or enable unauthorized access should not be shipped (and shouldn’t be pushed to a public repo).

