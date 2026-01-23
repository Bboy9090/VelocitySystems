#pragma once

#include <cstdint>

namespace reforge::physics {

// Fixed timestep physics (deterministic)
constexpr double FIXED_DELTA_TIME = 1.0 / 60.0; // 60 Hz

// Physics world state
struct PhysicsState {
    // Rigid body transforms
    struct RigidBody {
        float position[3];
        float rotation[4]; // quaternion
        float linearVelocity[3];
        float angularVelocity[3];
    };
    
    RigidBody* bodies = nullptr;
    uint32_t bodyCount = 0;
};

// Deterministic physics step
class DeterministicPhysics {
public:
    DeterministicPhysics();
    ~DeterministicPhysics();
    
    // Step physics (fixed timestep)
    void step(double deltaTime);
    
    // Get current state
    const PhysicsState& getState() const { return m_state; }
    
    // Add rigid body
    uint32_t addRigidBody(const float* position, const float* rotation);
    
    // Apply impulse
    void applyImpulse(uint32_t bodyId, const float* impulse, const float* point);

private:
    PhysicsState m_state;
    uint32_t m_nextBodyId = 0;
    
    // Jolt integration (forward declare)
    void* m_joltWorld = nullptr;
    
    void integrate(double dt);
};

// Animation sync (reads physics, never writes)
class AnimationSync {
public:
    // Sample animation at time
    void sample(uint32_t entityId, double time, float* outTransform);
    
    // Apply root motion as impulse (not teleport)
    void applyRootMotion(uint32_t entityId, const float* deltaTransform, DeterministicPhysics& physics);
};

} // namespace reforge::physics
