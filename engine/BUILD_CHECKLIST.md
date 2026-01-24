# Engine Build Checklist

## Phase 1: Foundation (Week 1-2)
- [ ] Vulkan instance + device
- [ ] Swapchain creation
- [ ] Basic render loop (clear color)
- [ ] Frame pacing stable (< 1ms variance)
- [ ] Tracy profiler integrated

## Phase 2: Core Systems (Week 3-4)
- [ ] Job system (fiber-based)
- [ ] ECS foundation (EnTT → custom SoA)
- [ ] Render graph scheduler
- [ ] Barrier resolution
- [ ] Memory allocator (VMA)

## Phase 3: Rendering (Week 5-6)
- [ ] GPU-driven culling
- [ ] Indirect draw pipeline
- [ ] GBuffer pass
- [ ] Lighting pass (clustered)
- [ ] Post-processing chain

## Phase 4: Content (Week 7-8)
- [ ] Asset compiler (Rust)
- [ ] Mesh loading (memory-mapped)
- [ ] Material system (bindless)
- [ ] Texture streaming
- [ ] Animation system

## Phase 5: Physics (Week 9-10)
- [ ] Jolt integration
- [ ] Fixed timestep sync
- [ ] Deterministic replay
- [ ] Collision filtering
- [ ] Raycasting

## Phase 6: Tools (Week 11-12)
- [ ] Editor IPC protocol
- [ ] Level editor (basic)
- [ ] Asset validator
- [ ] Build pipeline
- [ ] Profiling tools

## Milestone: First Playable
- [ ] Load level
- [ ] Render scene
- [ ] Physics working
- [ ] 60 FPS stable
- [ ] No crashes

## Quality Gates
- ✅ No allocations in hot paths
- ✅ No virtual calls per entity
- ✅ Frame time < 16.67ms (p99)
- ✅ Deterministic physics
- ✅ All assets validated offline

---

**This is not a sprint. This is a foundation.**
