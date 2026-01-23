#include "core/memory.h"
#include "render/render_graph.h"
#include "jobs/job_system.h"
#include "assets/runtime_loader.h"
#include "physics/deterministic_sync.h"
#include "platform/editor_ipc.h"

#include <iostream>
#include <chrono>

using namespace reforge;

int main(int argc, char* argv[]) {
    std::cout << "REFORGE Engine v1.0.0\n";
    std::cout << "The Forge Doctrine: Build nothing that cannot be repaired.\n\n";
    
    // Initialize job system
    jobs::initJobSystem();
    
    // Initialize editor IPC (optional)
    platform::EditorIPC editor;
    if (editor.init("reforge_engine")) {
        std::cout << "Editor IPC initialized\n";
    }
    
    // Frame loop
    auto lastTime = std::chrono::high_resolution_clock::now();
    bool running = true;
    
    while (running) {
        auto currentTime = std::chrono::high_resolution_clock::now();
        auto deltaTime = std::chrono::duration<double>(currentTime - lastTime).count();
        lastTime = currentTime;
        
        // Process editor messages
        editor.processMessages();
        
        // Fixed timestep physics
        static double accumulator = 0.0;
        accumulator += deltaTime;
        while (accumulator >= physics::FIXED_DELTA_TIME) {
            // Step physics
            accumulator -= physics::FIXED_DELTA_TIME;
        }
        
        // Render frame
        // (Vulkan setup would go here)
        
        // Frame end
    }
    
    // Shutdown
    jobs::shutdownJobSystem();
    
    return 0;
}
