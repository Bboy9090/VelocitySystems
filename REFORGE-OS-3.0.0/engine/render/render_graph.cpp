#include "render_graph.h"
#include <algorithm>
#include <unordered_set>

namespace reforge::render {

RenderGraph::RenderGraph(VkDevice device, VkPhysicalDevice physicalDevice)
    : m_device(device)
    , m_physicalDevice(physicalDevice)
{
}

RenderGraph::~RenderGraph() {
    // Resources are owned externally
}

ResourceHandle RenderGraph::createResource(const char* name, VkImage image, VkFormat format, VkExtent3D extent) {
    RenderGraphResource res;
    res.name = name;
    res.image = image;
    res.format = format;
    res.extent = extent;
    res.currentState.layout = VK_IMAGE_LAYOUT_UNDEFINED;
    res.isSwapchain = false;
    
    m_resources.push_back(res);
    return static_cast<ResourceHandle>(m_resources.size() - 1);
}

ResourceHandle RenderGraph::createSwapchainResource(const char* name, VkImage* images, uint32_t count, VkFormat format, VkExtent2D extent) {
    // Swapchain resources are handled separately at execute time
    RenderGraphResource res;
    res.name = name;
    res.format = format;
    res.extent = { extent.width, extent.height, 1 };
    res.currentState.layout = VK_IMAGE_LAYOUT_UNDEFINED;
    res.isSwapchain = true;
    
    m_resources.push_back(res);
    return static_cast<ResourceHandle>(m_resources.size() - 1);
}

void RenderGraph::addPass(const char* name, RenderPassNode pass) {
    pass.name = name;
    m_passes.push_back(pass);
}

void RenderGraph::compile() {
    // Topological sort of passes based on resource dependencies
    m_executionOrder.clear();
    std::vector<bool> visited(m_passes.size(), false);
    std::vector<bool> tempMark(m_passes.size(), false);
    
    auto visit = [&](uint32_t i, auto& self) -> void {
        if (tempMark[i]) {
            // Cycle detected
            return;
        }
        if (visited[i]) return;
        
        tempMark[i] = true;
        
        // Visit dependencies
        for (uint32_t j = 0; j < m_passes.size(); ++j) {
            if (i == j) continue;
            
            // Check if pass j writes to something pass i reads
            for (ResourceHandle read : m_passes[i].reads) {
                for (ResourceHandle write : m_passes[j].writes) {
                    if (read == write) {
                        self(j, self);
                    }
                }
            }
        }
        
        tempMark[i] = false;
        visited[i] = true;
        m_executionOrder.push_back(i);
    };
    
    for (uint32_t i = 0; i < m_passes.size(); ++i) {
        if (!visited[i]) {
            visit(i, visit);
        }
    }
    
    std::reverse(m_executionOrder.begin(), m_executionOrder.end());
}

void RenderGraph::execute(VkCommandBuffer cmd, uint32_t swapchainIndex) {
    // Update swapchain resource
    for (auto& res : m_resources) {
        if (res.isSwapchain) {
            res.swapchainIndex = swapchainIndex;
        }
    }
    
    // Execute passes in order
    for (uint32_t passIdx : m_executionOrder) {
        RenderPassNode& pass = m_passes[passIdx];
        
        // Transition reads
        for (ResourceHandle read : pass.reads) {
            insertBarrier(cmd, read, pass.targetState);
        }
        
        // Transition writes
        for (ResourceHandle write : pass.writes) {
            insertBarrier(cmd, write, pass.targetState);
        }
        
        // Execute pass
        if (pass.execute) {
            pass.execute(cmd, pass.userData);
        }
    }
}

void RenderGraph::transition(ResourceHandle resource, VkImageLayout newLayout, VkAccessFlags2 newAccess, VkPipelineStageFlags2 newStage) {
    if (resource >= m_resources.size()) return;
    
    RenderGraphResource& res = m_resources[resource];
    res.targetState.layout = newLayout;
    res.targetState.access = newAccess;
    res.targetState.stage = newStage;
}

void RenderGraph::insertBarrier(VkCommandBuffer cmd, ResourceHandle resource, const ResourceState& newState) {
    if (resource >= m_resources.size()) return;
    
    RenderGraphResource& res = m_resources[resource];
    
    if (res.currentState.layout == newState.layout &&
        res.currentState.access == newState.access &&
        res.currentState.stage == newState.stage) {
        return; // No transition needed
    }
    
    VkImageMemoryBarrier2 barrier{ VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER_2 };
    barrier.oldLayout = res.currentState.layout;
    barrier.newLayout = newState.layout;
    barrier.srcAccessMask = res.currentState.access;
    barrier.dstAccessMask = newState.access;
    barrier.srcStageMask = res.currentState.stage;
    barrier.dstStageMask = newState.stage;
    barrier.image = res.image;
    barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    barrier.subresourceRange.baseMipLevel = 0;
    barrier.subresourceRange.levelCount = 1;
    barrier.subresourceRange.baseArrayLayer = 0;
    barrier.subresourceRange.layerCount = 1;
    
    VkDependencyInfo depInfo{ VK_STRUCTURE_TYPE_DEPENDENCY_INFO };
    depInfo.imageMemoryBarrierCount = 1;
    depInfo.pImageMemoryBarriers = &barrier;
    
    vkCmdPipelineBarrier2(cmd, &depInfo);
    
    // Update state
    res.currentState = newState;
}

} // namespace reforge::render
