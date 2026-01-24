// GPU-Driven Implementation

#include "gpu_driven.h"
#include "buffer.h"
#include <cstdio>

bool GPUDrivenManager::createIndirectDrawBuffer(VkDevice device,
                                               VkPhysicalDevice physicalDevice,
                                               uint32_t maxDraws,
                                               GPUDrivenResources& resources) {
    VkDeviceSize bufferSize = sizeof(VkDrawIndexedIndirectCommand) * maxDraws;
    
    VkBufferCreateInfo bufferInfo{};
    bufferInfo.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
    bufferInfo.size = bufferSize;
    bufferInfo.usage = VK_BUFFER_USAGE_INDIRECT_BUFFER_BIT | VK_BUFFER_USAGE_STORAGE_BUFFER_BIT;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    
    if (vkCreateBuffer(device, &bufferInfo, nullptr, &resources.indirectDrawBuffer) != VK_SUCCESS) {
        fprintf(stderr, "Failed to create indirect draw buffer\n");
        return false;
    }
    
    VkMemoryRequirements memRequirements;
    vkGetBufferMemoryRequirements(device, resources.indirectDrawBuffer, &memRequirements);
    
    VkMemoryAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
    allocInfo.allocationSize = memRequirements.size;
    allocInfo.memoryTypeIndex = BufferManager::findMemoryType(physicalDevice,
                                                              memRequirements.memoryTypeBits,
                                                              VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
    
    if (vkAllocateMemory(device, &allocInfo, nullptr, &resources.indirectDrawMemory) != VK_SUCCESS) {
        fprintf(stderr, "Failed to allocate indirect draw buffer memory\n");
        vkDestroyBuffer(device, resources.indirectDrawBuffer, nullptr);
        return false;
    }
    
    vkBindBufferMemory(device, resources.indirectDrawBuffer, resources.indirectDrawMemory, 0);
    resources.drawCount = maxDraws;
    
    return true;
}

void GPUDrivenManager::recordIndirectDraw(VkCommandBuffer cmd,
                                        VkBuffer indexBuffer,
                                        VkBuffer vertexBuffer,
                                        VkBuffer instanceBuffer,
                                        uint32_t indexCount,
                                        uint32_t instanceCount) {
    VkBuffer vertexBuffers[] = {vertexBuffer, instanceBuffer};
    VkDeviceSize offsets[] = {0, 0};
    vkCmdBindVertexBuffers(cmd, 0, 2, vertexBuffers, offsets);
    vkCmdBindIndexBuffer(cmd, indexBuffer, 0, VK_INDEX_TYPE_UINT32);
    vkCmdDrawIndexedIndirect(cmd, indexBuffer, 0, instanceCount, sizeof(VkDrawIndexedIndirectCommand));
}

void GPUDrivenResources::destroy(VkDevice device) {
    if (indirectDrawBuffer != VK_NULL_HANDLE) {
        vkDestroyBuffer(device, indirectDrawBuffer, nullptr);
    }
    if (indirectDrawMemory != VK_NULL_HANDLE) {
        vkFreeMemory(device, indirectDrawMemory, nullptr);
    }
}
