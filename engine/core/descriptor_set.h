// Descriptor Set Management
// For uniform buffers and textures

#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include "buffer.h"

struct Texture; // Forward declaration

struct DescriptorSetResources {
    VkDescriptorSetLayout layout = VK_NULL_HANDLE;
    std::vector<VkDescriptorSet> sets;
    
    void destroy(VkDevice device);
};

class DescriptorSetManager {
public:
    static bool createDescriptorSetLayout(VkDevice device, DescriptorSetResources& resources, bool includeTexture = false);
    static bool createDescriptorSets(VkDevice device,
                                    VkDescriptorPool descriptorPool,
                                    const DescriptorSetResources& layoutResources,
                                    const std::vector<Buffer>& uniformBuffers,
                                    const std::vector<Texture>& textures,
                                    DescriptorSetResources& resources);
    static bool createDescriptorPool(VkDevice device,
                                    uint32_t maxSets,
                                    VkDescriptorPool& pool,
                                    bool includeTexture = false);
};
