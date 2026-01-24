# Phase 2 Build Instructions

## Prerequisites

1. **Vulkan SDK** installed
   - Download: https://vulkan.lunarg.com/
   - Verify: `glslc --version` works

2. **Python 3** (for shader compiler script)
   - Or compile shaders manually with glslc

## Step-by-Step Build

### 1. Compile Shaders (REQUIRED FIRST)

```bash
cd engine
python tools/compile_shaders.py shaders
```

This creates:
- `shaders/triangle.vert.spv`
- `shaders/triangle.frag.spv`

**Alternative (manual):**
```bash
glslc shaders/triangle.vert -fshader-stage=vertex -o shaders/triangle.vert.spv
glslc shaders/triangle.frag -fshader-stage=fragment -o shaders/triangle.frag.spv
```

### 2. Build Engine

```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### 3. Copy Shaders to Build Directory

```bash
# From build/ directory
cp ../shaders/*.spv .  # Linux
# or
copy ..\shaders\*.spv .  # Windows
```

**Or run from engine/ directory:**
```bash
cd ..
./build/engine  # Shaders will be found in shaders/
```

### 4. Run

```bash
./engine  # Linux
Release\engine.exe  # Windows
```

## Expected Output

- Window opens (1920x1080)
- **Colored triangle** visible:
  - Red at bottom
  - Green at top-right  
  - Blue at top-left
  - Smooth gradient between
- 60 FPS (or vsync rate)
- No console errors

## Troubleshooting

### "Failed to load shaders"
**Fix:**
1. Verify `.spv` files exist
2. Check file paths (run from correct directory)
3. Verify shaders compiled correctly

### "glslc not found"
**Fix:**
1. Install Vulkan SDK
2. Add to PATH: `VULKAN_SDK/bin`
3. Restart terminal

### Triangle doesn't appear
**Fix:**
1. Check console for Vulkan errors
2. Verify graphics drivers support Vulkan
3. Try running as administrator (Windows)
4. Check validation layer output

### Black screen
**Fix:**
1. Verify shaders loaded (check console)
2. Check render pass creation succeeded
3. Verify pipeline creation succeeded
4. Check for validation errors

## Verification Checklist

- [ ] Shaders compiled (`.spv` files exist)
- [ ] Engine built successfully
- [ ] Shaders in correct location
- [ ] Window opens
- [ ] Triangle visible
- [ ] No console errors

---

**If all checks pass, Phase 2 is complete.**
