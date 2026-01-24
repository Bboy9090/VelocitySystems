// Texture Management
// Image loading and texture creation

#pragma once

#include <vulkan/vulkan.h>
#include <string>

struct Texture {
    VkImage image = VK_NULL_HANDLE;
    VkDeviceMemory memory = VK_NULL_HANDLE;
    VkImageView imageView = VK_NULL_HANDLE;
    VkSampler sampler = VK_NULL_HANDLE;
    uint32_t width = 0;
    uint32_t height = 0;
    
    void destroy(VkDevice device);
};

class TextureManager {
public:
    static bool createTexture(VkDevice device,
                            VkPhysicalDevice physicalDevice,
                            VkCommandPool commandPool,
                            VkQueue queue,
                            const std::string& path,
                            Texture& texture);
    
    static bool createTextureFromData(VkDevice device,
                                     VkPhysicalDevice physicalDevice,
                                     VkCommandPool commandPool,
                                     VkQueue queue,
                                     const uint8_t* pixels,
                                     uint32_t width,
                                     uint32_t height,
                                     Texture& texture);
    
private:
    static void transitionImageLayout(VkDevice device,
                                     VkCommandPool commandPool,
                                     VkQueue queue,
                                     VkImage image,
                                     VkFormat format,
                                     VkImageLayout oldLayout,
                                     VkImageLayout newLayout);
    
    static void copyBufferToImage(VkDevice device,
                                 VkCommandPool commandPool,
                                 VkQueue queue,
                                 VkBuffer buffer,
                                 VkImage image,
                                 uint32_t width,
                                 uint32_t height);
};
