#include "gpu_culling.h"
#include <cstring>

namespace reforge::render {

GPUCulling::GPUCulling(VkDevice device, VkPhysicalDevice physicalDevice)
    : m_device(device)
{
    createPipeline();
}

GPUCulling::~GPUCulling() {
    if (m_cullPipeline) {
        vkDestroyPipeline(m_device, m_cullPipeline, nullptr);
    }
    if (m_pipelineLayout) {
        vkDestroyPipelineLayout(m_device, m_pipelineLayout, nullptr);
    }
    if (m_descriptorLayout) {
        vkDestroyDescriptorSetLayout(m_device, m_descriptorLayout, nullptr);
    }
}

void GPUCulling::cull(const GPUCullData& data, VkCommandBuffer cmd) {
    // Bind pipeline
    vkCmdBindPipeline(cmd, VK_PIPELINE_BIND_POINT_COMPUTE, m_cullPipeline);
    
    // Bind descriptor sets (would be set up with actual buffers)
    // vkCmdBindDescriptorSets(cmd, VK_PIPELINE_BIND_POINT_COMPUTE, m_pipelineLayout, ...);
    
    // Dispatch compute
    // vkCmdDispatch(cmd, (data.maxDraws + 63) / 64, 1, 1);
}

void GPUCulling::createPipeline() {
    // Descriptor set layout
    VkDescriptorSetLayoutBinding bindings[] = {
        { 0, VK_DESCRIPTOR_TYPE_STORAGE_BUFFER, 1, VK_SHADER_STAGE_COMPUTE_BIT, nullptr }, // Mesh data
        { 1, VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, 1, VK_SHADER_STAGE_COMPUTE_BIT, nullptr }, // Camera
        { 2, VK_DESCRIPTOR_TYPE_STORAGE_BUFFER, 1, VK_SHADER_STAGE_COMPUTE_BIT, nullptr }, // Visible indices
        { 3, VK_DESCRIPTOR_TYPE_STORAGE_BUFFER, 1, VK_SHADER_STAGE_COMPUTE_BIT, nullptr }, // Draw commands
    };
    
    VkDescriptorSetLayoutCreateInfo dslci{ VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO };
    dslci.bindingCount = 4;
    dslci.pBindings = bindings;
    vkCreateDescriptorSetLayout(m_device, &dslci, nullptr, &m_descriptorLayout);
    
    // Pipeline layout
    VkPipelineLayoutCreateInfo plci{ VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO };
    plci.setLayoutCount = 1;
    plci.pSetLayouts = &m_descriptorLayout;
    vkCreatePipelineLayout(m_device, &plci, nullptr, &m_pipelineLayout);
    
    // Compute pipeline (shader would be loaded here)
    // VkComputePipelineCreateInfo cpci{ VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO };
    // cpci.stage = ...; // Load SPIR-V shader
    // cpci.layout = m_pipelineLayout;
    // vkCreateComputePipelines(m_device, VK_NULL_HANDLE, 1, &cpci, nullptr, &m_cullPipeline);
}

} // namespace reforge::render
