// Material System
// Texture binding and material properties

#pragma once

#include "texture.h"
#include <vulkan/vulkan.h>
#include <glm/glm.hpp>

struct Material {
    Texture diffuseTexture;
    glm::vec3 diffuseColor = glm::vec3(1.0f);
    float metallic = 0.0f;
    float roughness = 0.5f;
    
    bool hasTexture = false;
    
    void destroy(VkDevice device);
};

class MaterialManager {
public:
    static Material createDefaultMaterial();
    static Material createMaterialWithTexture(VkDevice device,
                                            VkPhysicalDevice physicalDevice,
                                            VkCommandPool commandPool,
                                            VkQueue queue,
                                            const std::string& texturePath);
};
