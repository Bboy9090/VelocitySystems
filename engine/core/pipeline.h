// Graphics Pipeline
// Creates pipeline for triangle rendering

#pragma once

#include <vulkan/vulkan.h>

struct PipelineResources {
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    VkPipeline pipeline = VK_NULL_HANDLE;
    
    void destroy(VkDevice device);
};

class PipelineManager {
public:
    bool createPipeline(VkDevice device, 
                       VkRenderPass renderPass,
                       VkShaderModule vertShader,
                       VkShaderModule fragShader,
                       VkDescriptorSetLayout descriptorSetLayout);
    void destroy(VkDevice device);
    
    PipelineResources resources;
};
