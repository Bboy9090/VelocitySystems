// Render Graph
// Minimal but functional - pass list with barrier resolution

#pragma once

#include <vulkan/vulkan.h>
#include <string>
#include <vector>
#include <functional>

struct RenderPass {
    std::string name;
    std::function<void(VkCommandBuffer)> execute;
    std::vector<VkImage> inputImages;
    std::vector<VkImage> outputImages;
};

class RenderGraph {
public:
    void init(VkDevice device);
    void destroy();
    
    void beginFrame();
    void addPass(const std::string& name, std::function<void(VkCommandBuffer)> fn);
    void execute(VkCommandBuffer cmd);
    
private:
    VkDevice device = VK_NULL_HANDLE;
    std::vector<RenderPass> passes;
};
