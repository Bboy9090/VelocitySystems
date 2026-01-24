// Material Implementation

#include "material.h"
#include "texture.h"
#include <cstdio>

Material MaterialManager::createDefaultMaterial() {
    Material mat;
    mat.diffuseColor = glm::vec3(1.0f, 1.0f, 1.0f);
    mat.metallic = 0.0f;
    mat.roughness = 0.5f;
    mat.hasTexture = false;
    return mat;
}

Material MaterialManager::createMaterialWithTexture(VkDevice device,
                                                   VkPhysicalDevice physicalDevice,
                                                   VkCommandPool commandPool,
                                                   VkQueue queue,
                                                   const std::string& texturePath) {
    Material mat = createDefaultMaterial();
    
    if (TextureManager::createTexture(device, physicalDevice, commandPool, queue, texturePath, mat.diffuseTexture)) {
        mat.hasTexture = true;
    }
    
    return mat;
}

void Material::destroy(VkDevice device) {
    if (hasTexture) {
        diffuseTexture.destroy(device);
    }
}
