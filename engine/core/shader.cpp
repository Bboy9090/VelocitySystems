// Shader Implementation
// For now, we'll use hardcoded SPIR-V or compile inline

#include "shader.h"
#include <cstdio>
#include <fstream>
#include <string>

VkShaderModule ShaderManager::createShaderModule(VkDevice device, const std::vector<uint32_t>& code) {
    VkShaderModuleCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    createInfo.codeSize = code.size() * sizeof(uint32_t);
    createInfo.pCode = code.data();
    
    VkShaderModule shaderModule;
    if (vkCreateShaderModule(device, &createInfo, nullptr, &shaderModule) != VK_SUCCESS) {
        fprintf(stderr, "Failed to create shader module\n");
        return VK_NULL_HANDLE;
    }
    
    return shaderModule;
}

std::vector<uint32_t> ShaderManager::loadSPIRV(const std::string& path) {
    std::ifstream file(path, std::ios::ate | std::ios::binary);
    if (!file.is_open()) {
        return {};
    }
    
    size_t fileSize = file.tellg();
    if (fileSize == 0) {
        fprintf(stderr, "Shader file is empty: %s\n", path.c_str());
        return {};
    }
    
    if (fileSize % sizeof(uint32_t) != 0) {
        fprintf(stderr, "Shader file size is not a multiple of 4 bytes: %s\n", path.c_str());
        return {};
    }
    
    std::vector<uint32_t> buffer(fileSize / sizeof(uint32_t));
    file.seekg(0);
    file.read(reinterpret_cast<char*>(buffer.data()), fileSize);
    file.close();
    
    return buffer;
}

std::vector<uint32_t> ShaderManager::compileGLSL(const std::string& source, const std::string& stage) {
    // Would use shaderc here - for now return empty
    // In production, you'd compile GLSL to SPIR-V
    return {};
}
