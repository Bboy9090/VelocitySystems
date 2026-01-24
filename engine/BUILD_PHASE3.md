# Phase 3 Build Instructions

## Prerequisites

1. **Vulkan SDK** installed
2. **Python 3** (for shader compiler)
3. **GLM** (fetched automatically by CMake)

## Step-by-Step Build

### 1. Compile Shaders (REQUIRED)

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

## Expected Output

- Window opens (1920x1080)
- **Two rotating objects:**
  - Triangle (center) - RGB gradient, rotating
  - Quad (right) - RGBY gradient, rotating
- Both objects rotate around Z-axis
- 3D perspective view
- 60 FPS smooth

## What Phase 3 Adds

### New Systems:
- ✅ Buffer manager (vertex/index/uniform)
- ✅ Mesh system (triangle, quad)
- ✅ Camera system (view/projection)
- ✅ Uniform buffer updates
- ✅ Descriptor sets

### Architecture:
- Staging buffers → Device-local buffers
- Per-frame uniform buffer updates
- Descriptor set binding
- Multiple objects in one frame

## Troubleshooting

### "Failed to load shaders"
- Run shader compiler
- Check `shaders/mesh.*.spv` exist

### "Failed to create buffer"
- Check GPU memory
- Verify Vulkan device supports required features

### Objects don't appear
- Check console for errors
- Verify uniform buffers created
- Check descriptor sets allocated

### Objects don't rotate
- Uniform buffer updates should happen each frame
- Check camera matrices
- Verify descriptor set rebinding

## Verification

- [ ] Shaders compiled
- [ ] Engine built
- [ ] Window opens
- [ ] Two objects visible
- [ ] Objects rotate
- [ ] No console errors

---

**Phase 3 Status: COMPLETE**
You have a working 3D renderer with vertex buffers and multiple objects.
