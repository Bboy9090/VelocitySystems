// Mesh Loader Implementation
// Basic OBJ parser

#include "mesh_loader.h"
#include "mesh.h"
#include <fstream>
#include <sstream>
#include <cstdio>
#include <string>
#include <glm/glm.hpp>

bool MeshLoader::loadOBJ(const std::string& path,
                        std::vector<Vertex>& vertices,
                        std::vector<uint32_t>& indices) {
    std::ifstream file(path);
    if (!file.is_open()) {
        fprintf(stderr, "Failed to open OBJ file: %s\n", path.c_str());
        return false;
    }
    
    std::vector<glm::vec3> positions;
    std::vector<glm::vec3> normals;
    std::vector<glm::vec2> uvs;
    std::vector<std::string> faces;
    
    std::string line;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        
        std::istringstream iss(line);
        std::string type;
        iss >> type;
        
        if (type == "v") {
            glm::vec3 pos;
            iss >> pos.x >> pos.y >> pos.z;
            positions.push_back(pos);
        } else if (type == "vn") {
            glm::vec3 norm;
            iss >> norm.x >> norm.y >> norm.z;
            normals.push_back(norm);
        } else if (type == "vt") {
            glm::vec2 uv;
            iss >> uv.x >> uv.y;
            uvs.push_back(uv);
        } else if (type == "f") {
            std::string faceLine = line.substr(2);
            faces.push_back(faceLine);
        }
    }
    
    // Parse faces and create vertices
    std::vector<glm::vec3> vertexPositions;
    std::vector<glm::vec3> vertexColors;
    
    for (const auto& face : faces) {
        std::istringstream iss(face);
        std::vector<uint32_t> faceIndices;
        
        std::string vertex;
        while (iss >> vertex) {
            size_t slash1 = vertex.find('/');
            size_t slash2 = vertex.find('/', slash1 + 1);
            
            int posIdx = std::stoi(vertex.substr(0, slash1)) - 1;
            int uvIdx = -1;
            int normIdx = -1;
            
            if (slash1 != std::string::npos && slash2 != std::string::npos) {
                if (slash2 > slash1 + 1) {
                    uvIdx = std::stoi(vertex.substr(slash1 + 1, slash2 - slash1 - 1)) - 1;
                }
                if (slash2 < vertex.length() - 1) {
                    normIdx = std::stoi(vertex.substr(slash2 + 1)) - 1;
                }
            }
            
            if (posIdx >= 0 && posIdx < (int)positions.size()) {
                vertexPositions.push_back(positions[posIdx]);
                // Assign color based on position (simple gradient)
                glm::vec3 color = (positions[posIdx] + glm::vec3(1.0f)) * 0.5f;
                vertexColors.push_back(color);
                faceIndices.push_back(static_cast<uint32_t>(vertexPositions.size() - 1));
            }
        }
        
        // Triangulate (assume triangles for now)
        if (faceIndices.size() >= 3) {
            for (size_t i = 1; i < faceIndices.size() - 1; i++) {
                indices.push_back(faceIndices[0]);
                indices.push_back(faceIndices[i]);
                indices.push_back(faceIndices[i + 1]);
            }
        }
    }
    
    // Create vertices
    vertices.resize(vertexPositions.size());
    for (size_t i = 0; i < vertexPositions.size(); i++) {
        vertices[i].position = vertexPositions[i];
        vertices[i].color = vertexColors[i];
    }
    
    return true;
}

Mesh MeshLoader::loadOBJMesh(VkDevice device,
                            VkPhysicalDevice physicalDevice,
                            VkCommandPool commandPool,
                            VkQueue queue,
                            const std::string& path) {
    std::vector<Vertex> vertices;
    std::vector<uint32_t> indices;
    
    if (!loadOBJ(path, vertices, indices)) {
        return Mesh{};
    }
    
    Mesh mesh;
    if (!MeshManager::createMesh(device, physicalDevice, commandPool, queue, vertices, indices, mesh)) {
        return Mesh{};
    }
    
    return mesh;
}
