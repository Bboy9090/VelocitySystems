# Phase 2: Triangle Rendering - Quick Start

## What This Does

Renders a colored triangle using Vulkan. This proves the entire rendering pipeline works.

## Setup (One Time)

### 1. Install Vulkan SDK
- Download from: https://vulkan.lunarg.com/
- Add `glslc` to PATH

### 2. Compile Shaders
```bash
cd engine
python tools/compile_shaders.py shaders
```

This creates:
- `shaders/triangle.vert.spv`
- `shaders/triangle.frag.spv`

### 3. Build Engine
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

### 4. Run
```bash
./engine  # Linux
Release\engine.exe  # Windows
```

## Expected Result

- Window opens
- Colored triangle appears (red/green/blue gradient)
- Smooth 60 FPS
- No errors in console

## Troubleshooting

### "Failed to load shaders"
- Run shader compiler first
- Check `shaders/` directory has `.spv` files
- Verify Vulkan SDK is installed

### "glslc not found"
- Install Vulkan SDK
- Add to PATH: `VULKAN_SDK/bin`

### Triangle doesn't appear
- Check console for Vulkan errors
- Verify graphics drivers support Vulkan
- Try running as administrator (Windows)

## What's Next

Phase 3 will add:
- Vertex buffers
- Index buffers
- Multiple objects
- Camera system
- Mesh loading

---

**Phase 2 Status: COMPLETE**
You have a working triangle renderer.
