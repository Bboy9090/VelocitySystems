// Character Roster Implementation

#include "character_roster.h"
#include "character.h"
#include <cstdio>

Team CharacterRoster::createIceFireTeam(VkDevice device,
                                       VkPhysicalDevice physicalDevice,
                                       VkCommandPool commandPool,
                                       VkQueue queue) {
    Team team;
    team.name = "Ice & Fire";
    team.primaryElement = ElementType::ICE;
    
    // Ice character (left)
    KaijuCharacter iceChar = CharacterManager::createIceCharacter("Frost", device,
                                                                    physicalDevice,
                                                                    commandPool,
                                                                    queue);
    iceChar.position = glm::vec3(-2.0f, 0.0f, 0.0f);
    iceChar.rotation.y = 0.5f;
    team.members.push_back(iceChar);
    
    // Fire character (right)
    KaijuCharacter fireChar = CharacterManager::createFireCharacter("Blaze", device,
                                                                    physicalDevice,
                                                                    commandPool,
                                                                    queue);
    fireChar.position = glm::vec3(2.0f, 0.0f, 0.0f);
    fireChar.rotation.y = -0.5f;
    team.members.push_back(fireChar);
    
    return team;
}

Team CharacterRoster::createCosmicTeam(VkDevice device,
                                      VkPhysicalDevice physicalDevice,
                                      VkCommandPool commandPool,
                                      VkQueue queue) {
    Team team;
    team.name = "Cosmic Power";
    team.primaryElement = ElementType::COSMIC;
    
    // Cosmic character (center)
    KaijuCharacter cosmicChar = CharacterManager::createCosmicCharacter("Nova", device,
                                                                       physicalDevice,
                                                                       commandPool,
                                                                       queue);
    cosmicChar.position = glm::vec3(0.0f, 0.0f, 0.0f);
    cosmicChar.scale = glm::vec3(1.5f, 1.5f, 1.5f);
    team.members.push_back(cosmicChar);
    
    return team;
}

float Team::getTeamPower() const {
    float totalPower = 0.0f;
    for (const auto& member : members) {
        if (member.isAlive()) {
            totalPower += member.stats.power * (member.stats.health / member.stats.maxHealth);
        }
    }
    return totalPower;
}

bool Team::isAlive() const {
    for (const auto& member : members) {
        if (member.isAlive()) {
            return true;
        }
    }
    return false;
}

void CharacterRoster::updateTeam(Team& team, float deltaTime) {
    for (auto& member : team.members) {
        CharacterManager::updateCharacter(member, deltaTime);
    }
}

void CharacterRoster::renderTeam(VkCommandBuffer cmd,
                                const Team& team,
                                VkPipeline pipeline,
                                VkPipelineLayout pipelineLayout,
                                VkDescriptorSet descriptorSet) {
    for (const auto& member : team.members) {
        CharacterManager::renderCharacter(cmd, member, pipeline, pipelineLayout, descriptorSet);
    }
}
