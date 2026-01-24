// Character Abilities System
// Special moves and attacks for Kai-Jax characters

#pragma once

#include "character.h"
#include <string>
#include <functional>

enum class AbilityType {
    OFFENSIVE,
    DEFENSIVE,
    UTILITY,
    ULTIMATE
};

struct Ability {
    std::string name;
    std::string description;
    AbilityType type;
    float energyCost;
    float cooldown;
    float currentCooldown;
    std::function<void(KaijuCharacter&, KaijuCharacter*)> execute;
    
    bool canUse(const KaijuCharacter& character) const {
        return character.stats.energy >= energyCost && currentCooldown <= 0.0f;
    }
    
    void update(float deltaTime) {
        if (currentCooldown > 0.0f) {
            currentCooldown -= deltaTime;
        }
    }
};

class AbilityManager {
public:
    static Ability createIceShard(KaijuCharacter& character);
    static Ability createIceWall(KaijuCharacter& character);
    static Ability createFireBlast(KaijuCharacter& character);
    static Ability createFireDash(KaijuCharacter& character);
    static Ability createCosmicBeam(KaijuCharacter& character);
    static Ability createCosmicRift(KaijuCharacter& character);
    
    static void updateAbilities(std::vector<Ability>& abilities, float deltaTime);
};
