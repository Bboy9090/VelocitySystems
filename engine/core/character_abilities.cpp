// Character Abilities Implementation

#include "character_abilities.h"
#include "character.h"
#include <cstdio>

Ability AbilityManager::createIceShard(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Ice Shard";
    ability.description = "Launch a sharp ice projectile";
    ability.type = AbilityType::OFFENSIVE;
    ability.energyCost = 15.0f;
    ability.cooldown = 2.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        if (target) {
            target->takeDamage(20.0f);
            printf("%s used Ice Shard on %s!\n", caster.name.c_str(), target->name.c_str());
        }
    };
    return ability;
}

Ability AbilityManager::createIceWall(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Ice Wall";
    ability.description = "Create a defensive barrier";
    ability.type = AbilityType::DEFENSIVE;
    ability.energyCost = 25.0f;
    ability.cooldown = 5.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        // Temporary damage reduction
        printf("%s created an Ice Wall!\n", caster.name.c_str());
    };
    return ability;
}

Ability AbilityManager::createFireBlast(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Fire Blast";
    ability.description = "Explosive fire attack";
    ability.type = AbilityType::OFFENSIVE;
    ability.energyCost = 20.0f;
    ability.cooldown = 3.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        if (target) {
            target->takeDamage(30.0f);
            printf("%s used Fire Blast on %s!\n", caster.name.c_str(), target->name.c_str());
        }
    };
    return ability;
}

Ability AbilityManager::createFireDash(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Fire Dash";
    ability.description = "Quick dash with fire trail";
    ability.type = AbilityType::UTILITY;
    ability.energyCost = 10.0f;
    ability.cooldown = 4.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        // Movement boost
        caster.stats.speed *= 2.0f;
        printf("%s used Fire Dash!\n", caster.name.c_str());
    };
    return ability;
}

Ability AbilityManager::createCosmicBeam(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Cosmic Beam";
    ability.description = "Powerful cosmic energy attack";
    ability.type = AbilityType::OFFENSIVE;
    ability.energyCost = 30.0f;
    ability.cooldown = 5.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        if (target) {
            target->takeDamage(40.0f);
            printf("%s used Cosmic Beam on %s!\n", caster.name.c_str(), target->name.c_str());
        }
    };
    return ability;
}

Ability AbilityManager::createCosmicRift(KaijuCharacter& character) {
    Ability ability;
    ability.name = "Cosmic Rift";
    ability.description = "Ultimate: Open a rift in space";
    ability.type = AbilityType::ULTIMATE;
    ability.energyCost = 50.0f;
    ability.cooldown = 15.0f;
    ability.currentCooldown = 0.0f;
    ability.execute = [](KaijuCharacter& caster, KaijuCharacter* target) {
        if (target) {
            target->takeDamage(60.0f);
            printf("%s used COSMIC RIFT on %s! ULTIMATE!\n", caster.name.c_str(), target->name.c_str());
        }
    };
    return ability;
}

void AbilityManager::updateAbilities(std::vector<Ability>& abilities, float deltaTime) {
    for (auto& ability : abilities) {
        ability.update(deltaTime);
    }
}
