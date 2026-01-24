// Character Roster Management
// Team composition and character selection

#pragma once

#include "character.h"
#include <vector>
#include <string>

struct Team {
    std::string name;
    std::vector<KaijuCharacter> members;
    ElementType primaryElement;
    
    float getTeamPower() const;
    bool isAlive() const;
};

class CharacterRoster {
public:
    static Team createIceFireTeam(VkDevice device,
                                 VkPhysicalDevice physicalDevice,
                                 VkCommandPool commandPool,
                                 VkQueue queue);
    
    static Team createCosmicTeam(VkDevice device,
                               VkPhysicalDevice physicalDevice,
                               VkCommandPool commandPool,
                               VkQueue queue);
    
    static void updateTeam(Team& team, float deltaTime);
    static void renderTeam(VkCommandBuffer cmd,
                          const Team& team,
                          VkPipeline pipeline,
                          VkPipelineLayout pipelineLayout,
                          VkDescriptorSet descriptorSet);
};
