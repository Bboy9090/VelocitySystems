// Mesh Implementation

#include "mesh.h"
#include "buffer.h"
#include <cstdio>
#include <cstring>

VkVertexInputBindingDescription Vertex::getBindingDescription() {
    VkVertexInputBindingDescription bindingDescription{};
    bindingDescription.binding = 0;
    bindingDescription.stride = sizeof(Vertex);
    bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
    return bindingDescription;
}

std::vector<VkVertexInputAttributeDescription> Vertex::getAttributeDescriptions() {
    std::vector<VkVertexInputAttributeDescription> attributeDescriptions(2);
    
    // Position
    attributeDescriptions[0].binding = 0;
    attributeDescriptions[0].location = 0;
    attributeDescriptions[0].format = VK_FORMAT_R32G32B32_SFLOAT;
    attributeDescriptions[0].offset = offsetof(Vertex, position);
    
    // Color
    attributeDescriptions[1].binding = 0;
    attributeDescriptions[1].location = 1;
    attributeDescriptions[1].format = VK_FORMAT_R32G32B32_SFLOAT;
    attributeDescriptions[1].offset = offsetof(Vertex, color);
    
    return attributeDescriptions;
}

bool MeshManager::createMesh(VkDevice device,
                            VkPhysicalDevice physicalDevice,
                            VkCommandPool commandPool,
                            VkQueue queue,
                            const std::vector<Vertex>& vertices,
                            const std::vector<uint32_t>& indices,
                            Mesh& mesh) {
    VkDeviceSize vertexBufferSize = sizeof(Vertex) * vertices.size();
    VkDeviceSize indexBufferSize = sizeof(uint32_t) * indices.size();
    
    // Staging buffers
    Buffer vertexStaging, indexStaging;
    
    if (!BufferManager::createBuffer(device, physicalDevice, vertexBufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                                    VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                                    vertexStaging)) {
        return false;
    }
    
    if (!BufferManager::createBuffer(device, physicalDevice, indexBufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                                    VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                                    indexStaging)) {
        vertexStaging.destroy(device);
        return false;
    }
    
    // Copy data to staging
    memcpy(vertexStaging.mapped, vertices.data(), vertexBufferSize);
    memcpy(indexStaging.mapped, indices.data(), indexBufferSize);
    
    // Create device-local buffers
    if (!BufferManager::createBuffer(device, physicalDevice, vertexBufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                                    VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
                                    mesh.vertexBuffer)) {
        vertexStaging.destroy(device);
        indexStaging.destroy(device);
        return false;
    }
    
    if (!BufferManager::createBuffer(device, physicalDevice, indexBufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_INDEX_BUFFER_BIT,
                                    VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
                                    mesh.indexBuffer)) {
        vertexStaging.destroy(device);
        indexStaging.destroy(device);
        mesh.vertexBuffer.destroy(device);
        return false;
    }
    
    // Copy to device
    BufferManager::copyBuffer(device, commandPool, queue,
                             vertexStaging.buffer, mesh.vertexBuffer.buffer, vertexBufferSize);
    BufferManager::copyBuffer(device, commandPool, queue,
                             indexStaging.buffer, mesh.indexBuffer.buffer, indexBufferSize);
    
    // Cleanup staging
    vertexStaging.destroy(device);
    indexStaging.destroy(device);
    
    mesh.indexCount = static_cast<uint32_t>(indices.size());
    return true;
}

Mesh MeshManager::createTriangle(VkDevice device,
                                VkPhysicalDevice physicalDevice,
                                VkCommandPool commandPool,
                                VkQueue queue) {
    std::vector<Vertex> vertices = {
        {{0.0f, -0.5f, 0.0f}, {1.0f, 0.0f, 0.0f}},
        {{0.5f, 0.5f, 0.0f}, {0.0f, 1.0f, 0.0f}},
        {{-0.5f, 0.5f, 0.0f}, {0.0f, 0.0f, 1.0f}}
    };
    
    std::vector<uint32_t> indices = {0, 1, 2};
    
    Mesh mesh;
    if (!createMesh(device, physicalDevice, commandPool, queue, vertices, indices, mesh)) {
        return Mesh{};
    }
    
    return mesh;
}

Mesh MeshManager::createQuad(VkDevice device,
                            VkPhysicalDevice physicalDevice,
                            VkCommandPool commandPool,
                            VkQueue queue) {
    std::vector<Vertex> vertices = {
        {{-0.5f, -0.5f, 0.0f}, {1.0f, 0.0f, 0.0f}},
        {{0.5f, -0.5f, 0.0f}, {0.0f, 1.0f, 0.0f}},
        {{0.5f, 0.5f, 0.0f}, {0.0f, 0.0f, 1.0f}},
        {{-0.5f, 0.5f, 0.0f}, {1.0f, 1.0f, 0.0f}}
    };
    
    std::vector<uint32_t> indices = {0, 1, 2, 2, 3, 0};
    
    Mesh mesh;
    if (!createMesh(device, physicalDevice, commandPool, queue, vertices, indices, mesh)) {
        return Mesh{};
    }
    
    return mesh;
}

void Mesh::destroy(VkDevice device) {
    vertexBuffer.destroy(device);
    indexBuffer.destroy(device);
}
