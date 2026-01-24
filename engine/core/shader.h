// Shader Management
// Compiles and loads shaders

#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>

class ShaderManager {
public:
    static VkShaderModule createShaderModule(VkDevice device, const std::vector<uint32_t>& code);
    static std::vector<uint32_t> compileGLSL(const std::string& source, const std::string& stage);
    static std::vector<uint32_t> loadSPIRV(const std::string& path);
};
