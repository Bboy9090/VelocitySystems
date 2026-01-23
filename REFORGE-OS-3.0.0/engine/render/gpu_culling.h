#pragma once

#include <vulkan/vulkan.h>
#include <cstdint>

namespace reforge::render {

// GPU-driven culling (compute shader)
struct GPUCullData {
    // Input
    VkBuffer meshData;          // Mesh transforms, bounds
    VkBuffer cameraData;        // View frustum
    VkBuffer hiZBuffer;         // Hierarchical Z-buffer (optional)
    
    // Output
    VkBuffer visibleIndices;     // Visible mesh IDs
    VkBuffer drawCommands;      // VkDrawIndexedIndirectCommand
    VkBuffer drawCount;         // Atomic counter
    
    uint32_t maxDraws = 65536;
};

// GPU culling system
class GPUCulling {
public:
    GPUCulling(VkDevice device, VkPhysicalDevice physicalDevice);
    ~GPUCulling();
    
    void cull(const GPUCullData& data, VkCommandBuffer cmd);
    
    VkPipeline getCullPipeline() const { return m_cullPipeline; }
    VkPipelineLayout getPipelineLayout() const { return m_pipelineLayout; }

private:
    VkDevice m_device;
    VkPipeline m_cullPipeline;
    VkPipelineLayout m_pipelineLayout;
    VkDescriptorSetLayout m_descriptorLayout;
    
    void createPipeline();
};

} // namespace reforge::render
