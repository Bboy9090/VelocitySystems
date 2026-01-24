// Mesh Loader
// OBJ file loading (basic implementation)

#pragma once

#include "mesh.h"
#include <string>
#include <vector>

class MeshLoader {
public:
    static bool loadOBJ(const std::string& path,
                       std::vector<Vertex>& vertices,
                       std::vector<uint32_t>& indices);
    
    static Mesh loadOBJMesh(VkDevice device,
                           VkPhysicalDevice physicalDevice,
                           VkCommandPool commandPool,
                           VkQueue queue,
                           const std::string& path);
};
