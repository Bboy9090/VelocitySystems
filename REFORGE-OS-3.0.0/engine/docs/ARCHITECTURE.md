# REFORGE Engine Architecture
## World-Class Universal Game Platform

**Version:** 1.0.0  
**Doctrine:** The Forge — Build nothing that cannot be repaired

---

## CORE PRINCIPLES

1. **Explicit over Implicit** — No driver guessing, no magic barriers
2. **Deterministic** — Same input → same output, every run
3. **Repairable** — Every component can be examined and fixed
4. **Evidence-based** — Performance is measurable, not assumed

---

## SYSTEM ARCHITECTURE

### Render Graph (Explicit Barriers)

```
Frame Begin
 ├─ Depth Prepass (Early Z)
 ├─ GBuffer Pass
 │   ├─ Reads: None
 │   └─ Writes: Albedo, Normal, Material, Depth
 ├─ Shadow Pass
 │   ├─ Reads: Depth
 │   └─ Writes: Shadow Maps
 ├─ Lighting Pass (Compute)
 │   ├─ Reads: GBuffer, Shadow Maps
 │   └─ Writes: Light Accumulation
 ├─ Transparency Pass
 │   ├─ Reads: Depth, Light Accumulation
 │   └─ Writes: Color
 ├─ Post-Processing
 │   ├─ Reads: Color, Depth
 │   └─ Writes: Final Image
 └─ Present
```

**Every transition is explicit. Every barrier is logged.**

### Job System (Fiber-Ready)

```
Main Thread (Orchestrator)
 ├─ Schedule Physics
 ├─ Schedule Animation
 ├─ Schedule AI
 ├─ Schedule Render Prep
 └─ Wait on Counters → Submit GPU

Worker Threads (Work-Stealing)
 ├─ Worker 0: Physics
 ├─ Worker 1: Animation
 ├─ Worker 2: AI
 └─ Worker N: Render Prep
```

**No blocking. No stalls. CPU stays hot.**

### GPU-Driven Rendering

```
1. Cull (Compute)
   └─ Frustum + Hi-Z → Visible IDs

2. Build (Compute)
   └─ Compact → VkDrawIndexedIndirectCommand

3. Draw (Graphics)
   └─ vkCmdDrawIndexedIndirectCount
```

**CPU never knows visibility. Ever.**

### Asset Pipeline

```
Source (FBX, PNG, etc.)
  ↓
Offline Compiler (Rust)
  ↓
Binary Asset (.rfor)
  ├─ Header (Magic, Version, Hash)
  ├─ Blob Table
  └─ Data (SoA layout)
  ↓
Runtime Loader
  └─ Memory-Mapped
```

**No parsing. No JSON. No reflection.**

### Physics + Animation Sync

```
Input
  ↓
Physics Step (Fixed 60 Hz)
  └─ Write: Rigid Transforms
  ↓
Animation Sample (GPU)
  └─ Read: Physics Transforms
  ↓
Skinning (Compute)
  └─ Output: Skinned Vertices
  ↓
Render
```

**Physics owns world. Animation reads, never writes.**

---

## PERFORMANCE TARGETS

- **Frame Time:** < 16.67ms (60 FPS minimum)
- **CPU Usage:** < 50% per core
- **GPU Usage:** > 90% (no stalls)
- **Memory:** < 2GB for base game
- **Determinism:** 100% (same input → same output)

---

## BUILD REQUIREMENTS

- **C++20** compiler (GCC 11+, Clang 14+, MSVC 2022+)
- **Vulkan 1.3** SDK
- **CMake 3.20+**
- **Rust 1.70+** (for tools)

---

## NEXT STEPS

1. Complete Vulkan device initialization
2. Implement render graph execution
3. Wire job system to frame loop
4. Build asset compiler
5. Integrate Jolt Physics

---

**REFORGE Engine**  
*Where verified systems are certified for return to service.*
