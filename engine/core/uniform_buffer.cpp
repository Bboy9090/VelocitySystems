// Uniform Buffer Implementation

#include "uniform_buffer.h"
#include <cstdio>
#include <cstring>

bool UniformBufferManager::createUniformBuffers(VkDevice device,
                                               VkPhysicalDevice physicalDevice,
                                               uint32_t swapchainImageCount,
                                               std::vector<Buffer>& uniformBuffers) {
    uniformBuffers.resize(swapchainImageCount);
    
    VkDeviceSize bufferSize = sizeof(UniformBufferObject);
    
    for (size_t i = 0; i < swapchainImageCount; i++) {
        if (!BufferManager::createBuffer(device, physicalDevice, bufferSize,
                                        VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
                                        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                                        uniformBuffers[i])) {
            // Cleanup on failure
            for (size_t j = 0; j < i; j++) {
                uniformBuffers[j].destroy(device);
            }
            return false;
        }
    }
    
    return true;
}

void UniformBufferManager::updateUniformBuffer(VkDevice device,
                                               Buffer& uniformBuffer,
                                               const Camera& camera,
                                               const glm::mat4& model) {
    UniformBufferObject ubo{};
    ubo.model = model;
    ubo.view = camera.getViewMatrix();
    ubo.proj = camera.getProjectionMatrix();
    ubo.proj[1][1] *= -1; // Flip Y for Vulkan
    
    memcpy(uniformBuffer.mapped, &ubo, sizeof(ubo));
}
