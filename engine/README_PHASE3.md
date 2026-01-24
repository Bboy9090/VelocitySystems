# Phase 3: Vertex Buffers & Meshes - Quick Start

## What This Does

Renders two 3D objects (triangle and quad) using vertex/index buffers, with a camera system and uniform buffers for transformations.

## Setup (One Time)

### 1. Compile Shaders
```bash
cd engine
python tools/compile_shaders.py shaders
```

This creates:
- `shaders/mesh.vert.spv`
- `shaders/mesh.frag.spv`

### 2. Build Engine
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

### 3. Run
```bash
./engine  # Linux
Release\engine.exe  # Windows
```

## Expected Result

- Window opens
- **Two rotating objects:**
  - Triangle (center) - RGB gradient
  - Quad (right) - RGBY gradient
- Both rotate around Z-axis
- 3D perspective view
- Smooth 60 FPS

## What's New

### Phase 3 Adds:
- ✅ Vertex buffers
- ✅ Index buffers
- ✅ Uniform buffers (camera matrices)
- ✅ Descriptor sets
- ✅ Multiple objects
- ✅ 3D transformations
- ✅ Camera system

### Architecture:
- Buffer manager (staging → device-local)
- Mesh manager (vertex/index creation)
- Camera system (view/projection)
- Uniform buffer updates per-frame
- Descriptor set binding

## Troubleshooting

### "Failed to load shaders"
- Run shader compiler first
- Check `shaders/mesh.*.spv` exist

### Objects don't appear
- Check console for Vulkan errors
- Verify uniform buffers created
- Check descriptor sets allocated

### Objects don't rotate
- Verify uniform buffer updates
- Check camera matrices correct
- Verify descriptor set binding

## What's Next

Phase 4 will add:
- OBJ/GLTF mesh loading
- Texture support
- Depth buffer
- Material system
- Multiple pipelines

---

**Phase 3 Status: COMPLETE**
You have a working 3D renderer with multiple objects.
