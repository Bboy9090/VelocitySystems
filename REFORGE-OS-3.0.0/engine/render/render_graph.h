#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>
#include <cstdint>

namespace reforge::render {

// Resource handle (opaque ID)
using ResourceHandle = uint32_t;
constexpr ResourceHandle INVALID_RESOURCE = UINT32_MAX;

// Resource state
struct ResourceState {
    VkImageLayout layout = VK_IMAGE_LAYOUT_UNDEFINED;
    VkAccessFlags2 access = 0;
    VkPipelineStageFlags2 stage = VK_PIPELINE_STAGE_2_NONE;
};

// Render pass node
struct RenderPassNode {
    std::string name;
    VkPipeline pipeline = VK_NULL_HANDLE;
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    std::vector<ResourceHandle> reads;
    std::vector<ResourceHandle> writes;
    void (*execute)(VkCommandBuffer, void*);
    void* userData = nullptr;
};

// Render graph resource
struct RenderGraphResource {
    std::string name;
    VkImage image = VK_NULL_HANDLE;
    VkImageView view = VK_NULL_HANDLE;
    VkFormat format = VK_FORMAT_UNDEFINED;
    VkExtent3D extent = {};
    ResourceState currentState;
    ResourceState targetState;
    bool isSwapchain = false;
    uint32_t swapchainIndex = 0;
};

// Render graph builder
class RenderGraph {
public:
    RenderGraph(VkDevice device, VkPhysicalDevice physicalDevice);
    ~RenderGraph();

    ResourceHandle createResource(const char* name, VkImage image, VkFormat format, VkExtent3D extent);
    ResourceHandle createSwapchainResource(const char* name, VkImage* images, uint32_t count, VkFormat format, VkExtent2D extent);

    void addPass(const char* name, RenderPassNode pass);
    
    void compile();
    void execute(VkCommandBuffer cmd, uint32_t swapchainIndex);

    void transition(ResourceHandle resource, VkImageLayout newLayout, VkAccessFlags2 newAccess, VkPipelineStageFlags2 newStage);

private:
    VkDevice m_device;
    VkPhysicalDevice m_physicalDevice;
    
    std::vector<RenderGraphResource> m_resources;
    std::vector<RenderPassNode> m_passes;
    std::vector<uint32_t> m_executionOrder; // Topologically sorted

    void resolveBarriers();
    void insertBarrier(VkCommandBuffer cmd, ResourceHandle resource, const ResourceState& newState);
};

} // namespace reforge::render
