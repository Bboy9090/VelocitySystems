#include "deterministic_sync.h"
#include <cstring>
#include <cmath>

namespace reforge::physics {

DeterministicPhysics::DeterministicPhysics() {
    // Initialize Jolt Physics world
    // m_joltWorld = ...;
}

DeterministicPhysics::~DeterministicPhysics() {
    // Cleanup Jolt
}

void DeterministicPhysics::step(double deltaTime) {
    // Fixed timestep accumulation
    static double accumulator = 0.0;
    accumulator += deltaTime;
    
    while (accumulator >= FIXED_DELTA_TIME) {
        integrate(FIXED_DELTA_TIME);
        accumulator -= FIXED_DELTA_TIME;
    }
}

uint32_t DeterministicPhysics::addRigidBody(const float* position, const float* rotation) {
    uint32_t id = m_nextBodyId++;
    
    // Expand state if needed
    if (id >= m_state.bodyCount) {
        // Reallocate (would use custom allocator in production)
        m_state.bodyCount = id + 1;
    }
    
    PhysicsState::RigidBody& body = m_state.bodies[id];
    std::memcpy(body.position, position, 3 * sizeof(float));
    std::memcpy(body.rotation, rotation, 4 * sizeof(float));
    std::memset(body.linearVelocity, 0, 3 * sizeof(float));
    std::memset(body.angularVelocity, 0, 3 * sizeof(float));
    
    return id;
}

void DeterministicPhysics::applyImpulse(uint32_t bodyId, const float* impulse, const float* point) {
    if (bodyId >= m_state.bodyCount) return;
    
    PhysicsState::RigidBody& body = m_state.bodies[bodyId];
    
    // Apply linear impulse
    body.linearVelocity[0] += impulse[0];
    body.linearVelocity[1] += impulse[1];
    body.linearVelocity[2] += impulse[2];
    
    // Apply angular impulse (simplified)
    // In production, would compute torque from point
}

void DeterministicPhysics::integrate(double dt) {
    // Integrate all bodies
    for (uint32_t i = 0; i < m_state.bodyCount; ++i) {
        PhysicsState::RigidBody& body = m_state.bodies[i];
        
        // Integrate position
        body.position[0] += body.linearVelocity[0] * dt;
        body.position[1] += body.linearVelocity[1] * dt;
        body.position[2] += body.linearVelocity[2] * dt;
        
        // Apply gravity
        body.linearVelocity[1] -= 9.81f * dt; // -Y is up
        
        // Damping
        const float damping = 0.99f;
        body.linearVelocity[0] *= damping;
        body.linearVelocity[1] *= damping;
        body.linearVelocity[2] *= damping;
    }
}

void AnimationSync::sample(uint32_t entityId, double time, float* outTransform) {
    // Sample animation curve at time
    // Would read from animation data
    std::memset(outTransform, 0, 16 * sizeof(float)); // 4x4 matrix
    outTransform[0] = 1.0f; // Identity
    outTransform[5] = 1.0f;
    outTransform[10] = 1.0f;
    outTransform[15] = 1.0f;
}

void AnimationSync::applyRootMotion(uint32_t entityId, const float* deltaTransform, DeterministicPhysics& physics) {
    // Extract translation from delta transform
    float impulse[3] = {
        deltaTransform[12] * 10.0f, // Scale to impulse
        deltaTransform[13] * 10.0f,
        deltaTransform[14] * 10.0f
    };
    
    float point[3] = { 0.0f, 0.0f, 0.0f };
    physics.applyImpulse(entityId, impulse, point);
}

} // namespace reforge::physics
