// Render Pass Management
// Creates render pass and framebuffers for swapchain

#pragma once

#include <vulkan/vulkan.h>
#include <vector>

struct RenderPassResources {
    VkRenderPass renderPass = VK_NULL_HANDLE;
    std::vector<VkFramebuffer> framebuffers;
    
    void destroy(VkDevice device);
};

class RenderPassManager {
public:
    bool createRenderPass(VkDevice device, VkFormat swapchainFormat, VkFormat depthFormat);
    bool createFramebuffers(VkDevice device, 
                           const std::vector<VkImageView>& imageViews,
                           VkImageView depthImageView,
                           VkExtent2D extent);
    void destroy(VkDevice device);
    
    RenderPassResources resources;
};
