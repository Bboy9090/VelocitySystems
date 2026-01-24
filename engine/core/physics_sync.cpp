// Physics + Animation Sync Implementation
// Fixed timestep with accumulator pattern

#include "physics_sync.h"
#include "physics_world.h"
#include "animation_system.h"

void PhysicsAnimationSync::update(float deltaTime) {
    // Clamp delta to prevent spiral of death
    deltaTime = std::min(deltaTime, 0.1f);
    
    accumulator += deltaTime;
    
    // Run physics at fixed timestep
    int substeps = 0;
    while (accumulator >= PHYSICS_DT && substeps < MAX_SUBSTEPS) {
        // Update animation first (provides input to physics)
        animation->update(PHYSICS_DT);
        
        // Physics step (deterministic)
        physics->step(PHYSICS_DT);
        
        accumulator -= PHYSICS_DT;
        substeps++;
        frameNumber++;
    }
    
    // Interpolate for rendering (smooth visuals)
    float alpha = accumulator / PHYSICS_DT;
    physics->interpolate(alpha);
    animation->interpolate(alpha);
}

void PhysicsAnimationSync::saveState(uint8_t* buffer, size_t size) {
    // Serialize physics state
    physics->serialize(buffer, size);
    
    // Serialize animation state
    size_t physSize = physics->getStateSize();
    animation->serialize(buffer + physSize, size - physSize);
}

void PhysicsAnimationSync::loadState(const uint8_t* buffer, size_t size) {
    // Deserialize physics
    physics->deserialize(buffer, size);
    
    // Deserialize animation
    size_t physSize = physics->getStateSize();
    animation->deserialize(buffer + physSize, size - physSize);
}
