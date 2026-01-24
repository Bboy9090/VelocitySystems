// Physics + Animation Sync Model
// Deterministic. Fixed timestep. Replayable.

#pragma once

#include <cstdint>

class PhysicsWorld;
class AnimationSystem;

// Fixed timestep: 60Hz = 16.666ms
constexpr float PHYSICS_DT = 1.0f / 60.0f;
constexpr int MAX_SUBSTEPS = 4;

class PhysicsAnimationSync {
public:
    void init(PhysicsWorld* phys, AnimationSystem* anim);
    void update(float deltaTime);
    
    // Deterministic replay
    void saveState(uint8_t* buffer, size_t size);
    void loadState(const uint8_t* buffer, size_t size);
    
private:
    PhysicsWorld* physics;
    AnimationSystem* animation;
    float accumulator = 0.0f;
    uint64_t frameNumber = 0;
};
