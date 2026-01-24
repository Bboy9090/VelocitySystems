# Kai-Jax Character Abilities

## Ice Character (Frost)

### Ice Shard
- **Type:** Offensive
- **Energy Cost:** 15
- **Cooldown:** 2s
- **Effect:** Launch ice projectile, deals 20 damage
- **Description:** Sharp, fast ice attack

### Ice Wall
- **Type:** Defensive
- **Energy Cost:** 25
- **Cooldown:** 5s
- **Effect:** Create defensive barrier
- **Description:** Protective ice barrier

---

## Fire Character (Blaze)

### Fire Blast
- **Type:** Offensive
- **Energy Cost:** 20
- **Cooldown:** 3s
- **Effect:** Explosive fire attack, deals 30 damage
- **Description:** Powerful fire explosion

### Fire Dash
- **Type:** Utility
- **Energy Cost:** 10
- **Cooldown:** 4s
- **Effect:** Quick dash with speed boost
- **Description:** Mobility ability with fire trail

---

## Cosmic Character (Nova)

### Cosmic Beam
- **Type:** Offensive
- **Energy Cost:** 30
- **Cooldown:** 5s
- **Effect:** Powerful energy beam, deals 40 damage
- **Description:** High-damage cosmic attack

### Cosmic Rift (ULTIMATE)
- **Type:** Ultimate
- **Energy Cost:** 50
- **Cooldown:** 15s
- **Effect:** Open space rift, deals 60 damage
- **Description:** Ultimate ability - devastating attack

---

## Ability System Features

- ✅ Energy-based casting
- ✅ Cooldown system
- ✅ Ability types (Offensive/Defensive/Utility/Ultimate)
- ✅ Damage/healing effects
- ✅ Status effects (future)
- ✅ Visual effects (future)

---

## Using Abilities

Abilities are automatically assigned to characters on creation. To use:

```cpp
// In game loop
if (character.abilities[0].canUse(character)) {
    character.abilities[0].execute(character, target);
    character.stats.energy -= character.abilities[0].energyCost;
    character.abilities[0].currentCooldown = character.abilities[0].cooldown;
}
```

---

**Abilities are ready for integration with input system!**
