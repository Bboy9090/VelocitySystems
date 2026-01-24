// Engine Main Loop
// Frame-bounded. Deterministic. Profiled.

#include "vulkan_device.h"
#include "render_graph.h"
#include "job_system.h"
#include "window.h"
#include "render_pass.h"
#include "pipeline.h"
#include "shader.h"
#include "mesh.h"
#include "camera.h"
#include "uniform_buffer.h"
#include "descriptor_set.h"
#include "depth_buffer.h"
#include "texture.h"
#include "mesh_loader.h"
#include "material.h"
#include "instancing.h"
#include "gpu_driven.h"
#include "profiler.h"
#include "character.h"
#include "character_roster.h"
#include "stubs.h"
#include <cstdio>
#include <vulkan/vulkan.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <vector>

class Engine {
public:
    bool init() {
        if (!window.create("Engine")) {
            return false;
        }
        
        if (!vulkan.init(window.handle, window.instance)) {
            return false;
        }
        
        // Create depth buffer
        if (!DepthBufferManager::createDepthResources(vulkan.device,
                                                      vulkan.physical,
                                                      vulkan.swapchainExtent,
                                                      depthBuffer)) {
            return false;
        }
        
        VkFormat depthFormat = DepthBufferManager::findDepthFormat(vulkan.physical);
        
        // Create render pass (with depth)
        if (!renderPassManager.createRenderPass(vulkan.device, vulkan.swapchainFormat, depthFormat)) {
            depthBuffer.destroy(vulkan.device);
            return false;
        }
        
        // Create framebuffers (with depth)
        if (!renderPassManager.createFramebuffers(vulkan.device, 
                                                  vulkan.swapchainImageViews,
                                                  depthBuffer.depthImageView,
                                                  vulkan.swapchainExtent)) {
            depthBuffer.destroy(vulkan.device);
            return false;
        }
        
        // Create descriptor set layout (with texture support)
        if (!DescriptorSetManager::createDescriptorSetLayout(vulkan.device, descriptorSetLayout, true)) {
            return false;
        }
        
        // Create descriptor pool (with texture support)
        if (!DescriptorSetManager::createDescriptorPool(vulkan.device,
                                                        static_cast<uint32_t>(vulkan.swapchainImages.size()),
                                                        descriptorPool,
                                                        true)) {
            descriptorSetLayout.destroy(vulkan.device);
            return false;
        }
        
        // Create uniform buffers
        if (!UniformBufferManager::createUniformBuffers(vulkan.device,
                                                       vulkan.physical,
                                                       static_cast<uint32_t>(vulkan.swapchainImages.size()),
                                                       uniformBuffers)) {
            vkDestroyDescriptorPool(vulkan.device, descriptorPool, nullptr);
            descriptorSetLayout.destroy(vulkan.device);
            return false;
        }
        
        // Create texture for descriptor sets
        std::vector<Texture> textures(vulkan.swapchainImages.size(), texture);
        
        // Create descriptor sets (with textures)
        if (!DescriptorSetManager::createDescriptorSets(vulkan.device,
                                                        descriptorPool,
                                                        descriptorSetLayout,
                                                        uniformBuffers,
                                                        textures,
                                                        descriptorSets)) {
            for (auto& buffer : uniformBuffers) {
                buffer.destroy(vulkan.device);
            }
            vkDestroyDescriptorPool(vulkan.device, descriptorPool, nullptr);
            descriptorSetLayout.destroy(vulkan.device);
            return false;
        }
        
        // Create instancing data
        std::vector<InstanceData> instances;
        for (int i = 0; i < 10; i++) {
            InstanceData inst;
            inst.model = glm::translate(glm::mat4(1.0f), glm::vec3((i % 5 - 2) * 1.5f, (i / 5 - 1) * 1.5f, 0.0f));
            inst.color = glm::vec4(1.0f, 0.5f + i * 0.05f, 0.5f, 1.0f);
            instances.push_back(inst);
        }
        
        if (!InstancingManager::createInstanceBuffer(vulkan.device,
                                                    vulkan.physical,
                                                    vulkan.commandPool,
                                                    vulkan.graphicsQueue,
                                                    instances,
                                                    instanceBuffer)) {
            printf("Warning: Failed to create instance buffer\n");
        }
        
        // Initialize profiler
        Profiler::init();
        
        // Create Kai-Jax character roster
        iceFireTeam = CharacterRoster::createIceFireTeam(vulkan.device,
                                                        vulkan.physical,
                                                        vulkan.commandPool,
                                                        vulkan.graphicsQueue);
        
        cosmicTeam = CharacterRoster::createCosmicTeam(vulkan.device,
                                                      vulkan.physical,
                                                      vulkan.commandPool,
                                                      vulkan.graphicsQueue);
        
        printf("Kai-Jax Roster Created:\n");
        printf("  Team 1: %s (%zu members)\n", iceFireTeam.name.c_str(), iceFireTeam.members.size());
        printf("  Team 2: %s (%zu members)\n", cosmicTeam.name.c_str(), cosmicTeam.members.size());
        
        // Load shaders (try multiple paths)
        std::vector<std::string> vertPaths = {
            "shaders/mesh.vert.spv",
            "../shaders/mesh.vert.spv",
            "../../shaders/mesh.vert.spv"
        };
        
        std::vector<std::string> fragPaths = {
            "shaders/mesh.frag.spv",
            "../shaders/mesh.frag.spv",
            "../../shaders/mesh.frag.spv"
        };
        
        std::vector<uint32_t> vertCode, fragCode;
        for (const auto& path : vertPaths) {
            vertCode = ShaderManager::loadSPIRV(path);
            if (!vertCode.empty()) break;
        }
        
        for (const auto& path : fragPaths) {
            fragCode = ShaderManager::loadSPIRV(path);
            if (!fragCode.empty()) break;
        }
        
        if (vertCode.empty() || fragCode.empty()) {
            fprintf(stderr, "Failed to load shaders.\n");
            fprintf(stderr, "Run: python tools/compile_shaders.py shaders\n");
            return false;
        }
        
        VkShaderModule vertShader = ShaderManager::createShaderModule(vulkan.device, vertCode);
        VkShaderModule fragShader = ShaderManager::createShaderModule(vulkan.device, fragCode);
        
        if (vertShader == VK_NULL_HANDLE || fragShader == VK_NULL_HANDLE) {
            return false;
        }
        
        // Create pipeline
        if (!pipelineManager.createPipeline(vulkan.device,
                                           renderPassManager.resources.renderPass,
                                           vertShader, fragShader,
                                           descriptorSetLayout.layout)) {
            vkDestroyShaderModule(vulkan.device, vertShader, nullptr);
            vkDestroyShaderModule(vulkan.device, fragShader, nullptr);
            return false;
        }
        
        // Clean up shader modules
        vkDestroyShaderModule(vulkan.device, vertShader, nullptr);
        vkDestroyShaderModule(vulkan.device, fragShader, nullptr);
        
        // Create meshes
        triangle = MeshManager::createTriangle(vulkan.device,
                                              vulkan.physical,
                                              vulkan.commandPool,
                                              vulkan.graphicsQueue);
        
        quad = MeshManager::createQuad(vulkan.device,
                                      vulkan.physical,
                                      vulkan.commandPool,
                                      vulkan.graphicsQueue);
        
        // Try to load OBJ mesh (optional - will use quad if fails)
        std::vector<std::string> objPaths = {
            "models/cube.obj",
            "../models/cube.obj",
            "../../models/cube.obj"
        };
        
        bool meshLoaded = false;
        for (const auto& path : objPaths) {
            Mesh testMesh = MeshLoader::loadOBJMesh(vulkan.device,
                                                    vulkan.physical,
                                                    vulkan.commandPool,
                                                    vulkan.graphicsQueue,
                                                    path);
            if (testMesh.indexCount > 0) {
                loadedMesh = testMesh;
                printf("Loaded mesh from: %s (%u indices)\n", path.c_str(), loadedMesh.indexCount);
                meshLoaded = true;
                break;
            }
        }
        
        // If no OBJ loaded, use quad
        if (!meshLoaded) {
            loadedMesh = quad;
            printf("Using quad mesh (OBJ not found)\n");
        }
        
        // Create texture (checkerboard pattern)
        if (!TextureManager::createTexture(vulkan.device,
                                          vulkan.physical,
                                          vulkan.commandPool,
                                          vulkan.graphicsQueue,
                                          "textures/checker.png",
                                          texture)) {
            printf("Warning: Failed to create texture, continuing without texture\n");
        }
        
        // Setup camera
        camera.aspect = (float)vulkan.swapchainExtent.width / (float)vulkan.swapchainExtent.height;
        camera.position = glm::vec3(0.0f, 0.0f, 3.0f);
        
        renderGraph.init(vulkan.device);
        jobSystem.init();
        
        return true;
    }
    
    void shutdown() {
        jobSystem.shutdown();
        
        instanceBuffer.destroy(vulkan.device);
        // Cleanup characters
        for (auto& member : iceFireTeam.members) {
            member.mesh.destroy(vulkan.device);
        }
        for (auto& member : cosmicTeam.members) {
            member.mesh.destroy(vulkan.device);
        }
        
        texture.destroy(vulkan.device);
        triangle.destroy(vulkan.device);
        quad.destroy(vulkan.device);
        // Only destroy loadedMesh if it's different from quad
        if (loadedMesh.indexCount > 0) {
            // Check if it's actually a different mesh (simple check)
            if (loadedMesh.vertexBuffer.buffer != quad.vertexBuffer.buffer) {
                loadedMesh.destroy(vulkan.device);
            }
        }
        
        depthBuffer.destroy(vulkan.device);
        
        Profiler::shutdown();
        
        for (auto& buffer : uniformBuffers) {
            buffer.destroy(vulkan.device);
        }
        
        vkDestroyDescriptorPool(vulkan.device, descriptorPool, nullptr);
        descriptorSets.destroy(vulkan.device);
        descriptorSetLayout.destroy(vulkan.device);
        
        pipelineManager.destroy(vulkan.device);
        renderPassManager.destroy(vulkan.device);
        renderGraph.destroy();
        vulkan.destroy();
        window.destroy();
    }
    
    void run() {
        Profiler::beginFrame();
        
        while (!window.shouldClose) {
            PROFILE_FRAME();
            window.pollEvents();
            
            // Schedule frame jobs
            JobCounter frameCounter;
            
            PhysicsData physicsData;
            AnimationData animData;
            AIData aiData;
            RenderData renderData;
            
            Job job1, job2, job3, job4;
            job1.fn = [&]() { updatePhysics(&physicsData); };
            job1.counter = &frameCounter;
            job2.fn = [&]() { updateAnimation(&animData); };
            job2.counter = &frameCounter;
            job3.fn = [&]() { updateAI(&aiData); };
            job3.counter = &frameCounter;
            job4.fn = [&]() { updateRenderPrep(&renderData); };
            job4.counter = &frameCounter;
            
            jobSystem.submit(job1);
            jobSystem.submit(job2);
            jobSystem.submit(job3);
            jobSystem.submit(job4);
            
            // Wait for jobs
            jobSystem.wait(frameCounter);
            
            // Update uniform buffer
            static float rotation = 0.0f;
            rotation += 0.01f;
            
            // Update instance buffer (rotate instances)
            if (instanceBuffer.buffer != VK_NULL_HANDLE) {
                std::vector<InstanceData> updatedInstances;
                for (int i = 0; i < 10; i++) {
                    InstanceData inst;
                    float angle = rotation + i * 0.1f;
                    inst.model = glm::rotate(glm::translate(glm::mat4(1.0f), glm::vec3((i % 5 - 2) * 1.5f, (i / 5 - 1) * 1.5f, 0.0f)), angle, glm::vec3(0.0f, 0.0f, 1.0f));
                    inst.color = glm::vec4(1.0f, 0.5f + i * 0.05f, 0.5f, 1.0f);
                    updatedInstances.push_back(inst);
                }
                InstancingManager::updateInstanceBuffer(vulkan.device, instanceBuffer, updatedInstances);
            }
            
            glm::mat4 model = glm::rotate(glm::mat4(1.0f), rotation, glm::vec3(0.0f, 0.0f, 1.0f));
            UniformBufferManager::updateUniformBuffer(vulkan.device,
                                                     uniformBuffers[vulkan.currentImageIndex],
                                                     camera,
                                                     model);
            
            // Render
            VkCommandBuffer cmd = vulkan.beginFrame();
            
            // Begin render pass
            VkClearValue clearValues[2];
            clearValues[0].color = {0.0f, 0.0f, 0.0f, 1.0f};
            clearValues[1].depthStencil = {1.0f, 0};
            
            VkRenderPassBeginInfo renderPassInfo{};
            renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
            renderPassInfo.renderPass = renderPassManager.resources.renderPass;
            renderPassInfo.framebuffer = renderPassManager.resources.framebuffers[vulkan.currentImageIndex];
            renderPassInfo.renderArea.offset = {0, 0};
            renderPassInfo.renderArea.extent = vulkan.swapchainExtent;
            renderPassInfo.clearValueCount = 2;
            renderPassInfo.pClearValues = clearValues;
            
            vkCmdBeginRenderPass(cmd, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);
            
            // Set viewport and scissor
            VkViewport viewport{};
            viewport.x = 0.0f;
            viewport.y = 0.0f;
            viewport.width = (float)vulkan.swapchainExtent.width;
            viewport.height = (float)vulkan.swapchainExtent.height;
            viewport.minDepth = 0.0f;
            viewport.maxDepth = 1.0f;
            vkCmdSetViewport(cmd, 0, 1, &viewport);
            
            VkRect2D scissor{};
            scissor.offset = {0, 0};
            scissor.extent = vulkan.swapchainExtent;
            vkCmdSetScissor(cmd, 0, 1, &scissor);
            
            // Bind pipeline
            vkCmdBindPipeline(cmd, VK_PIPELINE_BIND_POINT_GRAPHICS, pipelineManager.resources.pipeline);
            
            // Bind descriptor set
            vkCmdBindDescriptorSets(cmd,
                                   VK_PIPELINE_BIND_POINT_GRAPHICS,
                                   pipelineManager.resources.pipelineLayout,
                                   0, 1,
                                   &descriptorSets.sets[vulkan.currentImageIndex],
                                   0, nullptr);
            
            // Draw triangle
            VkBuffer vertexBuffers[] = {triangle.vertexBuffer.buffer};
            VkDeviceSize offsets[] = {0};
            vkCmdBindVertexBuffers(cmd, 0, 1, vertexBuffers, offsets);
            vkCmdBindIndexBuffer(cmd, triangle.indexBuffer.buffer, 0, VK_INDEX_TYPE_UINT32);
            vkCmdDrawIndexed(cmd, triangle.indexCount, 1, 0, 0, 0);
            
            // Draw loaded mesh (or quad if no OBJ loaded)
            glm::mat4 meshModel = glm::translate(glm::mat4(1.0f), glm::vec3(-1.0f, 0.0f, 0.0f));
            meshModel = glm::rotate(meshModel, rotation, glm::vec3(0.0f, 1.0f, 0.0f));
            UniformBufferManager::updateUniformBuffer(vulkan.device,
                                                    uniformBuffers[vulkan.currentImageIndex],
                                                    camera,
                                                    meshModel);
            
            vkCmdBindDescriptorSets(cmd,
                                   VK_PIPELINE_BIND_POINT_GRAPHICS,
                                   pipelineManager.resources.pipelineLayout,
                                   0, 1,
                                   &descriptorSets.sets[vulkan.currentImageIndex],
                                   0, nullptr);
            
            vertexBuffers[0] = loadedMesh.vertexBuffer.buffer;
            vkCmdBindVertexBuffers(cmd, 0, 1, vertexBuffers, offsets);
            vkCmdBindIndexBuffer(cmd, loadedMesh.indexBuffer.buffer, 0, VK_INDEX_TYPE_UINT32);
            vkCmdDrawIndexed(cmd, loadedMesh.indexCount, 1, 0, 0, 0);
            
            // End render pass
            vkCmdEndRenderPass(cmd);
            
            vulkan.endFrame();
            vulkan.present();
        }
    }
    
private:
    Window window;
    VulkanDevice vulkan;
    RenderPassManager renderPassManager;
    PipelineManager pipelineManager;
    RenderGraph renderGraph;
    JobSystem jobSystem;
    
    // Meshes
    Mesh triangle;
    Mesh quad;
    Mesh loadedMesh;
    
    // Texture
    Texture texture;
    
    // Depth buffer
    DepthBufferResources depthBuffer;
    
    // Camera
    Camera camera;
    
    // Uniform buffers
    std::vector<Buffer> uniformBuffers;
    DescriptorSetResources descriptorSetLayout;
    VkDescriptorPool descriptorPool = VK_NULL_HANDLE;
    DescriptorSetResources descriptorSets;
    
    // Instancing
    Buffer instanceBuffer;
    
    // Kai-Jax teams
    Team iceFireTeam;
    Team cosmicTeam;
};

int main() {
    Engine engine;
    if (!engine.init()) {
        fprintf(stderr, "Failed to initialize engine\n");
        return 1;
    }
    
    engine.run();
    engine.shutdown();
    return 0;
}
