// Character Implementation

#include "character.h"
#include "character_abilities.h"
#include "mesh.h"
#include "material.h"
#include <cstdio>
#include <cmath>

KaijuCharacter::KaijuCharacter(const std::string& charName, ElementType elem)
    : name(charName), element(elem) {
    setElementColors();
}

glm::mat4 KaijuCharacter::getModelMatrix() const {
    glm::mat4 model = glm::mat4(1.0f);
    model = glm::translate(model, position);
    model = glm::rotate(model, rotation.y, glm::vec3(0.0f, 1.0f, 0.0f));
    model = glm::rotate(model, rotation.x, glm::vec3(1.0f, 0.0f, 0.0f));
    model = glm::rotate(model, rotation.z, glm::vec3(0.0f, 0.0f, 1.0f));
    model = glm::scale(model, scale);
    return model;
}

void KaijuCharacter::update(float deltaTime) {
    animTime += deltaTime * animSpeed;
    
    // Idle animation - subtle floating
    position.y = 0.0f + std::sin(animTime) * 0.1f;
    
    // Element-specific effects
    switch (element) {
        case ElementType::ICE:
            glowIntensity = 0.8f + std::sin(animTime * 2.0f) * 0.2f;
            break;
        case ElementType::FIRE:
            glowIntensity = 1.0f + std::sin(animTime * 3.0f) * 0.3f;
            break;
        case ElementType::COSMIC:
            glowIntensity = 0.9f + std::sin(animTime * 1.5f) * 0.4f;
            break;
        default:
            break;
    }
}

void KaijuCharacter::setElementColors() {
    switch (element) {
        case ElementType::ICE:
            glowColor = glm::vec3(0.3f, 0.6f, 1.0f); // Blue
            stats.speed = 1.2f;
            stats.power = 0.9f;
            break;
        case ElementType::FIRE:
            glowColor = glm::vec3(1.0f, 0.5f, 0.2f); // Orange
            stats.speed = 1.0f;
            stats.power = 1.2f;
            break;
        case ElementType::COSMIC:
            glowColor = glm::vec3(0.6f, 0.3f, 1.0f); // Purple
            stats.speed = 0.9f;
            stats.power = 1.3f;
            break;
        case ElementType::VOID:
            glowColor = glm::vec3(0.1f, 0.1f, 0.2f); // Dark
            stats.speed = 1.1f;
            stats.power = 1.1f;
            break;
    }
}

void KaijuCharacter::useAbility(int abilityIndex) {
    // Ability system - consume energy
    float energyCost = 20.0f;
    if (stats.energy >= energyCost) {
        stats.energy -= energyCost;
        printf("%s used ability %d!\n", name.c_str(), abilityIndex);
    }
}

void KaijuCharacter::takeDamage(float amount) {
    stats.health = std::max(0.0f, stats.health - amount);
    if (stats.health <= 0.0f) {
        isVisible = false;
    }
}

void KaijuCharacter::heal(float amount) {
    stats.health = std::min(stats.maxHealth, stats.health + amount);
}

KaijuCharacter CharacterManager::createIceCharacter(const std::string& name, VkDevice device,
                                                   VkPhysicalDevice physicalDevice,
                                                   VkCommandPool commandPool,
                                                   VkQueue queue) {
    KaijuCharacter character(name, ElementType::ICE);
    
    // Create mesh (using quad for now, would load character model)
    character.mesh = MeshManager::createQuad(device, physicalDevice, commandPool, queue);
    
    // Set ice-specific properties
    character.scale = glm::vec3(1.2f, 1.2f, 1.2f);
    character.glowColor = glm::vec3(0.3f, 0.6f, 1.0f);
    character.glowIntensity = 1.0f;
    
    // Add ice abilities (stored as pointers for now)
    // Note: Full ability integration requires ability system initialization
    
    return character;
}

KaijuCharacter CharacterManager::createFireCharacter(const std::string& name, VkDevice device,
                                                     VkPhysicalDevice physicalDevice,
                                                     VkCommandPool commandPool,
                                                     VkQueue queue) {
    KaijuCharacter character(name, ElementType::FIRE);
    
    character.mesh = MeshManager::createQuad(device, physicalDevice, commandPool, queue);
    
    // Set fire-specific properties
    character.scale = glm::vec3(1.1f, 1.1f, 1.1f);
    character.glowColor = glm::vec3(1.0f, 0.5f, 0.2f);
    character.glowIntensity = 1.2f;
    
    // Add fire abilities (stored as pointers for now)
    
    return character;
}

KaijuCharacter CharacterManager::createCosmicCharacter(const std::string& name, VkDevice device,
                                                      VkPhysicalDevice physicalDevice,
                                                      VkCommandPool commandPool,
                                                      VkQueue queue) {
    KaijuCharacter character(name, ElementType::COSMIC);
    
    character.mesh = MeshManager::createQuad(device, physicalDevice, commandPool, queue);
    
    // Set cosmic-specific properties
    character.scale = glm::vec3(1.3f, 1.3f, 1.3f);
    character.glowColor = glm::vec3(0.6f, 0.3f, 1.0f);
    character.glowIntensity = 1.5f;
    
    // Add cosmic abilities (stored as pointers for now)
    
    return character;
}

void CharacterManager::updateCharacter(KaijuCharacter& character, float deltaTime) {
    if (!character.isAlive()) return;
    
    character.update(deltaTime);
    
    // Update abilities (when fully integrated)
    // AbilityManager::updateAbilities(character.abilities, deltaTime);
    
    // Regenerate energy
    character.stats.energy = std::min(character.stats.maxEnergy,
                                     character.stats.energy + deltaTime * 5.0f);
}

void CharacterManager::renderCharacter(VkCommandBuffer cmd,
                                      const KaijuCharacter& character,
                                      VkPipeline pipeline,
                                      VkPipelineLayout pipelineLayout,
                                      VkDescriptorSet descriptorSet) {
    if (!character.isVisible || !character.isAlive()) return;
    
    vkCmdBindPipeline(cmd, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline);
    vkCmdBindDescriptorSets(cmd, VK_PIPELINE_BIND_POINT_GRAPHICS, pipelineLayout,
                           0, 1, &descriptorSet, 0, nullptr);
    
    VkBuffer vertexBuffers[] = {character.mesh.vertexBuffer.buffer};
    VkDeviceSize offsets[] = {0};
    vkCmdBindVertexBuffers(cmd, 0, 1, vertexBuffers, offsets);
    vkCmdBindIndexBuffer(cmd, character.mesh.indexBuffer.buffer, 0, VK_INDEX_TYPE_UINT32);
    vkCmdDrawIndexed(cmd, character.mesh.indexCount, 1, 0, 0, 0);
}
