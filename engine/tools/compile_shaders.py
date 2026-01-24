#!/usr/bin/env python3
# Shader Compiler
# Compiles GLSL to SPIR-V using glslc (from Vulkan SDK)

import subprocess
import sys
import os

def compile_shader(input_path, output_path, stage):
    """Compile GLSL shader to SPIR-V"""
    glslc_path = "glslc"  # Should be in PATH from Vulkan SDK
    
    cmd = [
        glslc_path,
        input_path,
        "-fshader-stage=" + stage,
        "-o", output_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Compiled: {input_path} -> {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {input_path}:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: glslc not found. Install Vulkan SDK and add to PATH.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: compile_shaders.py [shader_dir]")
        sys.exit(1)
    
    shader_dir = sys.argv[1]
    
    # Compile all shaders found
    shaders = [
        ("triangle.vert", "triangle.vert.spv", "vertex"),
        ("triangle.frag", "triangle.frag.spv", "fragment"),
        ("mesh.vert", "mesh.vert.spv", "vertex"),
        ("mesh.frag", "mesh.frag.spv", "fragment"),
        ("textured.vert", "textured.vert.spv", "vertex"),
        ("textured.frag", "textured.frag.spv", "fragment"),
    ]
    
    for shader_in, shader_out, stage in shaders:
        in_path = os.path.join(shader_dir, shader_in)
        out_path = os.path.join(shader_dir, shader_out)
        if os.path.exists(in_path):
            compile_shader(in_path, out_path, stage)
