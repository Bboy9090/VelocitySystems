// Character System for Kai-Jax
// Anthropomorphic kaiju character management

#pragma once

#include "mesh.h"
#include "material.h"
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <string>
#include <vector>

enum class ElementType {
    ICE,      // Blue/White
    FIRE,     // Orange/Red
    COSMIC,   // Dark/Purple/Blue
    VOID      // Black/Dark
};

struct CharacterStats {
    float health = 100.0f;
    float maxHealth = 100.0f;
    float energy = 50.0f;
    float maxEnergy = 100.0f;
    float speed = 1.0f;
    float power = 1.0f;
};

class KaijuCharacter {
public:
    std::string name;
    ElementType element;
    CharacterStats stats;
    
    // Transform
    glm::vec3 position = glm::vec3(0.0f);
    glm::vec3 rotation = glm::vec3(0.0f);
    glm::vec3 scale = glm::vec3(1.0f);
    
    // Rendering
    Mesh mesh;
    Material material;
    bool isVisible = true;
    
    // Animation
    float animTime = 0.0f;
    float animSpeed = 1.0f;
    
    // Effects
    glm::vec3 glowColor = glm::vec3(1.0f);
    float glowIntensity = 1.0f;
    
    // Abilities (forward declared)
    std::vector<void*> abilities; // Will be Ability* when abilities.h is included
    
    KaijuCharacter(const std::string& charName, ElementType elem);
    
    glm::mat4 getModelMatrix() const;
    void update(float deltaTime);
    void setElementColors();
    
    // Character-specific methods
    void useAbility(int abilityIndex);
    void takeDamage(float amount);
    void heal(float amount);
    bool isAlive() const { return stats.health > 0.0f; }
};

class CharacterManager {
public:
    static KaijuCharacter createIceCharacter(const std::string& name, VkDevice device,
                                           VkPhysicalDevice physicalDevice,
                                           VkCommandPool commandPool,
                                           VkQueue queue);
    
    static KaijuCharacter createFireCharacter(const std::string& name, VkDevice device,
                                             VkPhysicalDevice physicalDevice,
                                             VkCommandPool commandPool,
                                             VkQueue queue);
    
    static KaijuCharacter createCosmicCharacter(const std::string& name, VkDevice device,
                                               VkPhysicalDevice physicalDevice,
                                               VkCommandPool commandPool,
                                               VkQueue queue);
    
    static void updateCharacter(KaijuCharacter& character, float deltaTime);
    static void renderCharacter(VkCommandBuffer cmd,
                               const KaijuCharacter& character,
                               VkPipeline pipeline,
                               VkPipelineLayout pipelineLayout,
                               VkDescriptorSet descriptorSet);
};
