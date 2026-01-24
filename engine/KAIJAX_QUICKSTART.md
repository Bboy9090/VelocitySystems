# Kai-Jax Character System - Quick Start

## Build & Run

```bash
cd engine
python tools/compile_shaders.py shaders
mkdir build && cd build
cmake ..
cmake --build . --config Release
./engine  # or Release\engine.exe
```

## What You'll See

- **Frost (Ice)** - Left side, blue glow, floating
- **Blaze (Fire)** - Right side, orange glow, floating  
- **Nova (Cosmic)** - Center, purple glow, larger scale
- All characters animate with idle floating
- Element-based glow effects active

## Character Controls (Future)

Currently characters auto-animate. Future additions:
- Input system for character movement
- Ability activation
- Combat interactions
- Team formation changes

## Adding More Characters

Edit `engine/core/engine_main.cpp` in `init()`:

```cpp
// Add to iceFireTeam
KaijuCharacter newChar = CharacterManager::createIceCharacter("Name", ...);
newChar.position = glm::vec3(x, y, z);
iceFireTeam.members.push_back(newChar);
```

## Character Customization

Each character has:
- `position` - Where they spawn
- `rotation` - Facing direction
- `scale` - Size multiplier
- `glowColor` - Element color (RGB)
- `glowIntensity` - Glow strength
- `stats` - Health, energy, speed, power

## Next Features to Add

1. **Character Models** - Replace quads with actual 3D models
2. **Animation System** - Walk, attack, ability animations
3. **Input System** - Keyboard/mouse controls
4. **Combat System** - Damage, abilities, effects
5. **UI System** - Health bars, energy meters
6. **Sound System** - Character voices, ability sounds

---

**Your Kai-Jax characters are ready to fight!**
