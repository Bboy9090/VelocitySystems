// Instancing System
// GPU-driven instanced rendering

#pragma once

#include "buffer.h"
#include "mesh.h"
#include <vulkan/vulkan.h>
#include <vector>
#include <glm/glm.hpp>

struct InstanceData {
    glm::mat4 model;
    glm::vec4 color;
};

class InstancingManager {
public:
    static bool createInstanceBuffer(VkDevice device,
                                   VkPhysicalDevice physicalDevice,
                                   VkCommandPool commandPool,
                                   VkQueue queue,
                                   const std::vector<InstanceData>& instances,
                                   Buffer& instanceBuffer);
    
    static void updateInstanceBuffer(VkDevice device,
                                    Buffer& instanceBuffer,
                                    const std::vector<InstanceData>& instances);
};
