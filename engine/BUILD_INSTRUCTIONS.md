# Build Instructions - Phase 1

## Prerequisites

### Windows
- Visual Studio 2019 or later (with C++ desktop development)
- CMake 3.20+
- Vulkan SDK (latest)
- Git

### Linux
- GCC 10+ or Clang 12+
- CMake 3.20+
- Vulkan SDK
- X11 development libraries

## Build Steps

### 1. Clone and Setup
```bash
cd engine
mkdir build
cd build
```

### 2. Configure
```bash
cmake ..
```

### 3. Build
```bash
cmake --build . --config Release
```

Or on Linux:
```bash
make -j$(nproc)
```

### 4. Run
```bash
./engine  # Linux
# or
Release\engine.exe  # Windows
```

## What You Should See

- Window opens (1920x1080, black background)
- Window title: "Engine"
- Window can be closed normally
- No crashes
- Console shows no errors (in Release mode)

## Troubleshooting

### "Vulkan not found"
- Install Vulkan SDK
- Set `VULKAN_SDK` environment variable
- On Windows: Add to PATH

### "Validation layers not found"
- Install Vulkan SDK
- Validation layers are optional (disabled in Release)

### Window doesn't open
- Check console for errors
- Verify graphics drivers support Vulkan
- Try running as administrator (Windows)

### Compilation errors
- Ensure C++20 support
- Check Vulkan SDK version (1.3+)
- Verify CMake found Vulkan

## Next Steps

Once this runs:
1. You have a working Vulkan window
2. Job system is functional
3. Render graph structure exists
4. Ready for Phase 2: Actual rendering
