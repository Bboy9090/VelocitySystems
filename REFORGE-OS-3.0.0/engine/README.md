# REFORGE Engine
## World-Class Universal Game Platform

**Version:** 1.0.0  
**Doctrine:** The Forge — Build nothing that cannot be repaired  
**Status:** FOUNDATION LOCKED

---

## PRIME DIRECTIVE

**This is not a game engine. This is a real-time simulation platform that ships a game as its first product.**

Every system is:
- **Explicit** — No driver guessing
- **Deterministic** — Same input → same output
- **Repairable** — Every component can be examined and fixed
- **Evidence-based** — Performance is measurable, not assumed

---

## ARCHITECTURE

### Core Stack (Locked)

- **Language:** C++20/23
- **Rendering:** Vulkan 1.3 (explicit barriers, no magic)
- **ECS:** Custom SoA (EnTT as starting point only)
- **Physics:** Jolt Physics (deterministic)
- **Jobs:** Custom fiber-based scheduler
- **Assets:** Offline compile, memory-mapped, hash-addressed
- **Tools:** Rust (asset pipeline, editor, validators)

### Principles

1. **No allocation in hot paths**
2. **No virtual calls per entity per frame**
3. **No exceptions in runtime**
4. **No RTTI**
5. **Every frame measurable (Tracy)**
6. **GPU-driven rendering (zero CPU draw submission)**
7. **Deterministic physics (fixed timestep)**
8. **Offline asset compilation (no runtime parsing)**

---

## STRUCTURE

```
engine/
├── core/           # Foundation (memory, math, platform)
├── render/         # Vulkan render graph
├── physics/        # Jolt integration
├── ecs/            # Entity Component System (SoA)
├── jobs/           # Fiber-based job system
├── assets/         # Asset compiler + runtime loader
├── animation/      # GPU-driven skinning
└── platform/       # Window, input, audio

tools/              # Rust toolchain
├── asset_pipeline/ # Offline compiler
├── editor/         # Headless-first editor
└── validators/     # Asset validation

game/               # First product
├── content/        # Game assets
├── systems/        # Game-specific ECS systems
└── rules/          # Game logic
```

---

## MILESTONES

### Milestone 1: The Frame ✅
- Window
- Vulkan device
- Swapchain
- Render loop
- Job system online
- Stable frame pacing

### Milestone 2: The World
- ECS
- Transform system
- Camera
- Basic renderable mesh
- Deterministic update

### Milestone 3: The Toolchain
- Asset import
- Bake
- Load
- Validate

### Milestone 4: The Game
- Only after fundamentals are perfect

---

## BUILD

```bash
# C++ Engine
cd engine
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)

# Rust Tools
cd tools
cargo build --release
```

---

## RULES (NON-NEGOTIABLE)

- No feature without a profile
- No system without ownership
- No abstraction without a benchmark
- If you can't explain where the time goes, you don't ship

---

**REFORGE Engine**  
*Where verified systems are certified for return to service.*
