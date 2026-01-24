// Render Graph Implementation
// Simple pass execution with basic barriers

#include "render_graph.h"

void RenderGraph::init(VkDevice device) {
    this->device = device;
}

void RenderGraph::destroy() {
    passes.clear();
}

void RenderGraph::beginFrame() {
    passes.clear();
}

void RenderGraph::addPass(const std::string& name, std::function<void(VkCommandBuffer)> fn) {
    RenderPass pass;
    pass.name = name;
    pass.execute = fn;
    passes.push_back(pass);
}

void RenderGraph::execute(VkCommandBuffer cmd) {
    for (auto& pass : passes) {
        // Basic barrier before each pass
        VkMemoryBarrier2 barrier{ VK_STRUCTURE_TYPE_MEMORY_BARRIER_2 };
        barrier.srcStageMask = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
        barrier.dstStageMask = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
        barrier.srcAccessMask = VK_ACCESS_2_MEMORY_WRITE_BIT;
        barrier.dstAccessMask = VK_ACCESS_2_MEMORY_READ_BIT;
        
        VkDependencyInfo dep{ VK_STRUCTURE_TYPE_DEPENDENCY_INFO };
        dep.memoryBarrierCount = 1;
        dep.pMemoryBarriers = &barrier;
        vkCmdPipelineBarrier2(cmd, &dep);
        
        // Execute pass
        pass.execute(cmd);
    }
}
