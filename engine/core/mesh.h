// Mesh Management
// Vertex and index buffers

#pragma once

#include "buffer.h"
#include <glm/glm.hpp>
#include <vector>

struct Vertex {
    glm::vec3 position;
    glm::vec3 color;
    
    static VkVertexInputBindingDescription getBindingDescription();
    static std::vector<VkVertexInputAttributeDescription> getAttributeDescriptions();
};

struct Mesh {
    Buffer vertexBuffer;
    Buffer indexBuffer;
    uint32_t indexCount = 0;
    
    void destroy(VkDevice device);
};

class MeshManager {
public:
    static bool createMesh(VkDevice device,
                          VkPhysicalDevice physicalDevice,
                          VkCommandPool commandPool,
                          VkQueue queue,
                          const std::vector<Vertex>& vertices,
                          const std::vector<uint32_t>& indices,
                          Mesh& mesh);
    
    static Mesh createTriangle(VkDevice device,
                              VkPhysicalDevice physicalDevice,
                              VkCommandPool commandPool,
                              VkQueue queue);
    
    static Mesh createQuad(VkDevice device,
                          VkPhysicalDevice physicalDevice,
                          VkCommandPool commandPool,
                          VkQueue queue);
};
