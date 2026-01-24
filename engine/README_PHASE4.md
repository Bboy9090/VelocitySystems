# Phase 4: Mesh Loading, Textures, Depth - Quick Start

## What This Does

Renders 3D objects with depth testing, loads OBJ meshes, and creates textures.

## Setup (One Time)

### 1. Compile Shaders
```bash
cd engine
python tools/compile_shaders.py shaders
```

### 2. Optional: Add OBJ Mesh
Create `engine/models/cube.obj` (or use the provided one)

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
- **Three objects:**
  - Triangle (center-left) - rotating
  - Loaded mesh (center-right) - from OBJ or quad
  - Objects occlude correctly (depth testing)
- 3D perspective view
- Smooth 60 FPS

## What's New

### Phase 4 Adds:
- ✅ Depth buffer
- ✅ Depth testing
- ✅ OBJ mesh loader
- ✅ Texture creation
- ✅ Enhanced render pass
- ✅ Enhanced pipeline

### Architecture:
- Depth buffer per swapchain
- OBJ parser (basic)
- Texture staging → device-local
- Depth attachment in render pass
- Depth stencil state in pipeline

## Troubleshooting

### "Failed to load OBJ"
- Check `models/cube.obj` exists
- Engine will use quad if OBJ not found
- Check console for parser errors

### Objects don't occlude
- Verify depth buffer created
- Check depth testing enabled
- Verify depth clear value

### Texture creation fails
- This is optional (engine continues)
- Check GPU memory
- Verify image format support

## What's Next

Phase 5 will add:
- Texture binding in shaders
- Material system
- Image file loading
- GLTF support
- Multiple textures per object

---

**Phase 4 Status: COMPLETE**
You have a working 3D renderer with depth testing and mesh loading.
