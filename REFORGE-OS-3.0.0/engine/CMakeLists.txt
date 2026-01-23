cmake_minimum_required(VERSION 3.20)
project(REFORGE_ENGINE VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
if(MSVC)
    add_compile_options(/W4 /WX /permissive- /Zc:__cplusplus)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Werror)
    add_compile_options(-march=native -mtune=native)
endif()

# Release flags
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_definitions(NDEBUG)
    if(MSVC)
        add_compile_options(/O2 /Ob2 /DNDEBUG)
    else()
        add_compile_options(-O3 -DNDEBUG -flto)
    endif()
endif()

# Dependencies
find_package(Vulkan REQUIRED)
find_package(glfw3 REQUIRED)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/core
    ${CMAKE_CURRENT_SOURCE_DIR}/render
    ${CMAKE_CURRENT_SOURCE_DIR}/physics
    ${CMAKE_CURRENT_SOURCE_DIR}/ecs
    ${CMAKE_CURRENT_SOURCE_DIR}/jobs
    ${CMAKE_CURRENT_SOURCE_DIR}/assets
    ${CMAKE_CURRENT_SOURCE_DIR}/animation
    ${CMAKE_CURRENT_SOURCE_DIR}/platform
)

# Core library
add_library(reforge_core STATIC
    core/memory.cpp
    core/math.cpp
    core/log.cpp
)

# Render library
add_library(reforge_render STATIC
    render/vulkan_device.cpp
    render/vulkan_swapchain.cpp
    render/render_graph.cpp
    render/gpu_culling.cpp
    render/indirect_draw.cpp
)

# Physics library
add_library(reforge_physics STATIC
    physics/jolt_world.cpp
    physics/deterministic_sync.cpp
)

# ECS library
add_library(reforge_ecs STATIC
    ecs/registry.cpp
    ecs/transform_system.cpp
)

# Jobs library
add_library(reforge_jobs STATIC
    jobs/job_system.cpp
    jobs/fiber_pool.cpp
)

# Assets library
add_library(reforge_assets STATIC
    assets/compiler.cpp
    assets/runtime_loader.cpp
)

# Animation library
add_library(reforge_animation STATIC
    animation/gpu_skinning.cpp
    animation/sample.cpp
)

# Platform library
add_library(reforge_platform STATIC
    platform/window.cpp
    platform/input.cpp
)

# Main executable
add_executable(reforge_engine
    main.cpp
)

target_link_libraries(reforge_engine
    reforge_core
    reforge_render
    reforge_physics
    reforge_ecs
    reforge_jobs
    reforge_assets
    reforge_animation
    reforge_platform
    Vulkan::Vulkan
    glfw
)

# Link libraries
if(UNIX AND NOT APPLE)
    target_link_libraries(reforge_engine pthread dl)
endif()
