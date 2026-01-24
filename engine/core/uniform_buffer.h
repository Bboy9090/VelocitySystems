// Uniform Buffer Management
// Camera matrices, etc.

#pragma once

#include "buffer.h"
#include "camera.h"
#include <vulkan/vulkan.h>
#include <vector>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

struct UniformBufferObject {
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};

class UniformBufferManager {
public:
    static bool createUniformBuffers(VkDevice device,
                                   VkPhysicalDevice physicalDevice,
                                   uint32_t swapchainImageCount,
                                   std::vector<Buffer>& uniformBuffers);
    
    static void updateUniformBuffer(VkDevice device,
                                   Buffer& uniformBuffer,
                                   const Camera& camera,
                                   const glm::mat4& model);
};
