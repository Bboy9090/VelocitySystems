// GPU-Driven Rendering
// Indirect draw commands, culling, etc.

#pragma once

#include <vulkan/vulkan.h>
#include "buffer.h"

struct GPUDrivenResources {
    VkBuffer indirectDrawBuffer = VK_NULL_HANDLE;
    VkDeviceMemory indirectDrawMemory = VK_NULL_HANDLE;
    uint32_t drawCount = 0;
    
    void destroy(VkDevice device);
};

class GPUDrivenManager {
public:
    static bool createIndirectDrawBuffer(VkDevice device,
                                       VkPhysicalDevice physicalDevice,
                                       uint32_t maxDraws,
                                       GPUDrivenResources& resources);
    
    static void recordIndirectDraw(VkCommandBuffer cmd,
                                  VkBuffer indexBuffer,
                                  VkBuffer vertexBuffer,
                                  VkBuffer instanceBuffer,
                                  uint32_t indexCount,
                                  uint32_t instanceCount);
};
