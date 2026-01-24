// Buffer Management
// Vertex buffers, index buffers, uniform buffers

#pragma once

#include <vulkan/vulkan.h>
#include <cstdint>

struct Buffer {
    VkBuffer buffer = VK_NULL_HANDLE;
    VkDeviceMemory memory = VK_NULL_HANDLE;
    VkDeviceSize size = 0;
    void* mapped = nullptr;
    
    void destroy(VkDevice device);
};

class BufferManager {
public:
    static bool createBuffer(VkDevice device,
                            VkPhysicalDevice physicalDevice,
                            VkDeviceSize size,
                            VkBufferUsageFlags usage,
                            VkMemoryPropertyFlags properties,
                            Buffer& buffer);
    
    static void copyBuffer(VkDevice device,
                          VkCommandPool commandPool,
                          VkQueue queue,
                          VkBuffer src,
                          VkBuffer dst,
                          VkDeviceSize size);
    
    static uint32_t findMemoryType(VkPhysicalDevice physicalDevice,
                                   uint32_t typeFilter,
                                   VkMemoryPropertyFlags properties);
};
