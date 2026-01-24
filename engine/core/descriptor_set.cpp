// Descriptor Set Implementation

#include "descriptor_set.h"
#include "buffer.h"
#include "uniform_buffer.h"
#include "texture.h"
#include <cstdio>

bool DescriptorSetManager::createDescriptorSetLayout(VkDevice device, DescriptorSetResources& resources, bool includeTexture) {
    std::vector<VkDescriptorSetLayoutBinding> bindings;
    
    // Uniform buffer binding
    VkDescriptorSetLayoutBinding uboLayoutBinding{};
    uboLayoutBinding.binding = 0;
    uboLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    uboLayoutBinding.descriptorCount = 1;
    uboLayoutBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    uboLayoutBinding.pImmutableSamplers = nullptr;
    bindings.push_back(uboLayoutBinding);
    
    // Texture binding (optional)
    if (includeTexture) {
        VkDescriptorSetLayoutBinding samplerLayoutBinding{};
        samplerLayoutBinding.binding = 1;
        samplerLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
        samplerLayoutBinding.descriptorCount = 1;
        samplerLayoutBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
        samplerLayoutBinding.pImmutableSamplers = nullptr;
        bindings.push_back(samplerLayoutBinding);
    }
    
    VkDescriptorSetLayoutCreateInfo layoutInfo{};
    layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutInfo.bindingCount = static_cast<uint32_t>(bindings.size());
    layoutInfo.pBindings = bindings.data();
    
    if (vkCreateDescriptorSetLayout(device, &layoutInfo, nullptr, &resources.layout) != VK_SUCCESS) {
        fprintf(stderr, "Failed to create descriptor set layout\n");
        return false;
    }
    
    return true;
}

bool DescriptorSetManager::createDescriptorPool(VkDevice device,
                                               uint32_t maxSets,
                                               VkDescriptorPool& pool,
                                               bool includeTexture) {
    std::vector<VkDescriptorPoolSize> poolSizes;
    
    VkDescriptorPoolSize uboPoolSize{};
    uboPoolSize.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    uboPoolSize.descriptorCount = maxSets;
    poolSizes.push_back(uboPoolSize);
    
    if (includeTexture) {
        VkDescriptorPoolSize samplerPoolSize{};
        samplerPoolSize.type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
        samplerPoolSize.descriptorCount = maxSets;
        poolSizes.push_back(samplerPoolSize);
    }
    
    VkDescriptorPoolCreateInfo poolInfo{};
    poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
    poolInfo.poolSizeCount = static_cast<uint32_t>(poolSizes.size());
    poolInfo.pPoolSizes = poolSizes.data();
    poolInfo.maxSets = maxSets;
    
    if (vkCreateDescriptorPool(device, &poolInfo, nullptr, &pool) != VK_SUCCESS) {
        fprintf(stderr, "Failed to create descriptor pool\n");
        return false;
    }
    
    return true;
}

bool DescriptorSetManager::createDescriptorSets(VkDevice device,
                                               VkDescriptorPool descriptorPool,
                                               const DescriptorSetResources& layoutResources,
                                               const std::vector<Buffer>& uniformBuffers,
                                               const std::vector<Texture>& textures,
                                               DescriptorSetResources& resources) {
    std::vector<VkDescriptorSetLayout> layouts(uniformBuffers.size(), layoutResources.layout);
    
    VkDescriptorSetAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    allocInfo.descriptorPool = descriptorPool;
    allocInfo.descriptorSetCount = static_cast<uint32_t>(uniformBuffers.size());
    allocInfo.pSetLayouts = layouts.data();
    
    resources.sets.resize(uniformBuffers.size());
    if (vkAllocateDescriptorSets(device, &allocInfo, resources.sets.data()) != VK_SUCCESS) {
        fprintf(stderr, "Failed to allocate descriptor sets\n");
        return false;
    }
    
    for (size_t i = 0; i < uniformBuffers.size(); i++) {
        std::vector<VkWriteDescriptorSet> descriptorWrites;
        
        // Uniform buffer
        VkDescriptorBufferInfo bufferInfo{};
        bufferInfo.buffer = uniformBuffers[i].buffer;
        bufferInfo.offset = 0;
        bufferInfo.range = uniformBuffers[i].size;
        
        VkWriteDescriptorSet uboWrite{};
        uboWrite.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
        uboWrite.dstSet = resources.sets[i];
        uboWrite.dstBinding = 0;
        uboWrite.dstArrayElement = 0;
        uboWrite.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
        uboWrite.descriptorCount = 1;
        uboWrite.pBufferInfo = &bufferInfo;
        descriptorWrites.push_back(uboWrite);
        
        // Texture (if provided)
        if (!textures.empty() && i < textures.size() && textures[i].imageView != VK_NULL_HANDLE) {
            VkDescriptorImageInfo imageInfo{};
            imageInfo.imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
            imageInfo.imageView = textures[i].imageView;
            imageInfo.sampler = textures[i].sampler;
            
            VkWriteDescriptorSet samplerWrite{};
            samplerWrite.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
            samplerWrite.dstSet = resources.sets[i];
            samplerWrite.dstBinding = 1;
            samplerWrite.dstArrayElement = 0;
            samplerWrite.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
            samplerWrite.descriptorCount = 1;
            samplerWrite.pImageInfo = &imageInfo;
            descriptorWrites.push_back(samplerWrite);
        }
        
        vkUpdateDescriptorSets(device, static_cast<uint32_t>(descriptorWrites.size()), descriptorWrites.data(), 0, nullptr);
    }
    
    return true;
}

void DescriptorSetResources::destroy(VkDevice device) {
    if (layout != VK_NULL_HANDLE) {
        vkDestroyDescriptorSetLayout(device, layout, nullptr);
    }
    // Descriptor sets are freed when pool is destroyed
}
