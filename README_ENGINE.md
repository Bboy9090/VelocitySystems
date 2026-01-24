# Enterprise-Grade Game Engine Foundation

## The Stack (Locked)

### Core
- **C++20/23** - Engine runtime
- **Vulkan 1.3** - Explicit rendering
- **Jolt Physics** - Deterministic physics
- **Custom ECS** - Data-oriented design
- **Fiber-based Jobs** - Lock-free parallelism

### Tools (Rust)
- **Asset Compiler** - Offline-only, hash-addressed
- **Editor** - IPC-based, headless-first
- **Validators** - Pre-flight checks

## Architecture Principles

1. **Zero CPU draw submission** - GPU-driven rendering
2. **Fixed timestep physics** - Deterministic, replayable
3. **Memory-mapped assets** - No runtime parsing
4. **Frame-bounded execution** - No GC, no hidden threads
5. **Explicit synchronization** - No driver magic

## Build

```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```

## Tools

```bash
cd tools/asset_compiler
cargo build --release
./target/release/asset_compiler input.obj output.asset
```

## The Forge Doctrine

**Build nothing that cannot be repaired.**

This engine:
- Refuses unsafe operations
- Leaves evidence (profiles, manifests)
- Can be examined (no black boxes)
- Can be extended (no dead ends)

---

**This is not a prototype. This is the foundation.**
