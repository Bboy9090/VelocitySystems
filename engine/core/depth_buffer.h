// Depth Buffer Management
// Depth testing for 3D rendering

#pragma once

#include <vulkan/vulkan.h>
#include <vector>

struct DepthBufferResources {
    VkImage depthImage = VK_NULL_HANDLE;
    VkDeviceMemory depthImageMemory = VK_NULL_HANDLE;
    VkImageView depthImageView = VK_NULL_HANDLE;
    
    void destroy(VkDevice device);
};

class DepthBufferManager {
public:
    static bool createDepthResources(VkDevice device,
                                    VkPhysicalDevice physicalDevice,
                                    VkExtent2D extent,
                                    DepthBufferResources& resources);
    
    static VkFormat findDepthFormat(VkPhysicalDevice physicalDevice);
    static bool hasStencilComponent(VkFormat format);
};
