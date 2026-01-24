// Vulkan Device Management
// Instance → Physical Device → Logical Device → Swapchain

#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>

struct VulkanDevice {
    VkInstance instance = VK_NULL_HANDLE;
    VkPhysicalDevice physical = VK_NULL_HANDLE;
    VkDevice device = VK_NULL_HANDLE;
    VkQueue graphicsQueue = VK_NULL_HANDLE;
    uint32_t graphicsQueueFamily = UINT32_MAX;
    
    VkSurfaceKHR surface = VK_NULL_HANDLE;
    VkSwapchainKHR swapchain = VK_NULL_HANDLE;
    std::vector<VkImage> swapchainImages;
    std::vector<VkImageView> swapchainImageViews;
    VkFormat swapchainFormat = VK_FORMAT_UNDEFINED;
    VkExtent2D swapchainExtent = {0, 0};
    
    VkCommandPool commandPool = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> commandBuffers;
    
    VkSemaphore imageAvailableSemaphore = VK_NULL_HANDLE;
    VkSemaphore renderFinishedSemaphore = VK_NULL_HANDLE;
    VkFence inFlightFence = VK_NULL_HANDLE;
    
    uint32_t currentFrame = 0;
    uint32_t currentImageIndex = 0;
    
    bool init(void* windowHandle, void* windowInstance);
    void destroy();
    
    VkCommandBuffer beginFrame();
    void endFrame();
    void present();
    
private:
    bool createInstance();
    bool selectPhysicalDevice();
    bool createLogicalDevice();
    bool createSurface(void* windowHandle, void* windowInstance);
    bool createSwapchain();
    bool createCommandPool();
    bool createSyncObjects();
    
    bool checkValidationLayerSupport();
    std::vector<const char*> getRequiredExtensions();
};
