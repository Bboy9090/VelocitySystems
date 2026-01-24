// Instancing Implementation

#include "instancing.h"
#include "buffer.h"
#include <cstdio>
#include <cstring>
#include <vector>

bool InstancingManager::createInstanceBuffer(VkDevice device,
                                           VkPhysicalDevice physicalDevice,
                                           VkCommandPool commandPool,
                                           VkQueue queue,
                                           const std::vector<InstanceData>& instances,
                                           Buffer& instanceBuffer) {
    VkDeviceSize bufferSize = sizeof(InstanceData) * instances.size();
    
    if (bufferSize == 0) {
        return false;
    }
    
    // Staging buffer
    Buffer stagingBuffer;
    if (!BufferManager::createBuffer(device, physicalDevice, bufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                                    VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                                    stagingBuffer)) {
        return false;
    }
    
    memcpy(stagingBuffer.mapped, instances.data(), bufferSize);
    
    // Device-local buffer
    if (!BufferManager::createBuffer(device, physicalDevice, bufferSize,
                                    VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                                    VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
                                    instanceBuffer)) {
        stagingBuffer.destroy(device);
        return false;
    }
    
    BufferManager::copyBuffer(device, commandPool, queue,
                             stagingBuffer.buffer, instanceBuffer.buffer, bufferSize);
    
    stagingBuffer.destroy(device);
    return true;
}

void InstancingManager::updateInstanceBuffer(VkDevice device,
                                            Buffer& instanceBuffer,
                                            const std::vector<InstanceData>& instances) {
    if (instanceBuffer.mapped && instanceBuffer.size >= sizeof(InstanceData) * instances.size()) {
        memcpy(instanceBuffer.mapped, instances.data(), sizeof(InstanceData) * instances.size());
    }
}
