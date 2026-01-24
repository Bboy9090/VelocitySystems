cmake_minimum_required(VERSION 3.20)
project(Engine VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Dependencies
find_package(Vulkan REQUIRED)

# GLM (header-only, fetch if not found)
if(NOT TARGET glm::glm)
    include(FetchContent)
    FetchContent_Declare(
        glm
        GIT_REPOSITORY https://github.com/g-truc/glm.git
        GIT_TAG 0.9.9.8
    )
    FetchContent_MakeAvailable(glm)
endif()

# Core engine
add_library(engine_core STATIC
    core/vulkan_device.cpp
    core/render_graph.cpp
    core/job_system.cpp
    core/window.cpp
    core/render_pass.cpp
    core/pipeline.cpp
    core/shader.cpp
    core/buffer.cpp
    core/mesh.cpp
    core/uniform_buffer.cpp
    core/descriptor_set.cpp
    core/depth_buffer.cpp
    core/texture.cpp
    core/mesh_loader.cpp
    core/material.cpp
    core/instancing.cpp
    core/gpu_driven.cpp
    core/profiler.cpp
    core/character.cpp
    core/character_roster.cpp
    core/character_abilities.cpp
)

target_link_libraries(engine_core
    PUBLIC
        Vulkan::Vulkan
        glm::glm
)

target_include_directories(engine_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# Windows-specific
if(WIN32)
    target_link_libraries(engine_core PRIVATE user32)
endif()

# Engine executable
add_executable(engine
    core/engine_main.cpp
)

target_link_libraries(engine
    PRIVATE
        engine_core
)
