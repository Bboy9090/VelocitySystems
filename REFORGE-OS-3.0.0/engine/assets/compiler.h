#pragma once

#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>

namespace reforge::assets {

// Asset file magic
constexpr uint32_t ASSET_MAGIC = 0x52464F52; // "RFOR"

// Asset version
constexpr uint32_t ASSET_VERSION = 1;

// Asset header
struct AssetHeader {
    uint32_t magic = ASSET_MAGIC;
    uint32_t version = ASSET_VERSION;
    uint64_t hash = 0;              // SHA-256 (first 64 bits)
    uint64_t tableOffset = 0;        // Offset to blob table
    uint64_t dataOffset = 0;         // Offset to data section
};

// Blob entry (chunk of data)
struct BlobEntry {
    uint64_t offset = 0;
    uint64_t size = 0;
    uint32_t type = 0;               // Asset type ID
    uint32_t flags = 0;
};

// Blob table
struct BlobTable {
    uint32_t count = 0;
    BlobEntry entries[1];           // Variable length
};

// Asset types
enum AssetType {
    ASSET_MESH = 1,
    ASSET_TEXTURE = 2,
    ASSET_MATERIAL = 3,
    ASSET_ANIMATION = 4,
    ASSET_SCENE = 5,
};

// Mesh data (SoA layout)
struct MeshData {
    uint64_t vertexCount = 0;
    uint64_t indexCount = 0;
    
    uint64_t positionsOffset = 0;    // float3[]
    uint64_t normalsOffset = 0;      // oct-encoded uint16[]
    uint64_t uvsOffset = 0;          // half2[]
    uint64_t tangentsOffset = 0;     // oct-encoded uint16[]
    uint64_t indicesOffset = 0;      // uint32[]
};

// Asset compiler (offline)
class AssetCompiler {
public:
    AssetCompiler();
    
    // Compile mesh from source
    bool compileMesh(const std::string& sourcePath, const std::string& outputPath);
    
    // Compile texture
    bool compileTexture(const std::string& sourcePath, const std::string& outputPath);
    
    // Compute hash
    uint64_t computeHash(const void* data, size_t size);

private:
    bool writeAsset(const std::string& path, const AssetHeader& header, const void* data, size_t dataSize);
};

} // namespace reforge::assets
