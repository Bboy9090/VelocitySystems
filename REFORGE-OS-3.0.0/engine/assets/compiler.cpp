#include "compiler.h"
#include <fstream>
#include <cstring>
#include <xxhash.h>

namespace reforge::assets {

AssetCompiler::AssetCompiler() {
}

bool AssetCompiler::compileMesh(const std::string& sourcePath, const std::string& outputPath) {
    // Read source mesh (would parse FBX/OBJ/etc here)
    std::ifstream source(sourcePath, std::ios::binary);
    if (!source.is_open()) {
        return false;
    }
    
    // For now, create a minimal valid asset
    AssetHeader header;
    header.magic = ASSET_MAGIC;
    header.version = ASSET_VERSION;
    header.tableOffset = sizeof(AssetHeader);
    header.dataOffset = sizeof(AssetHeader) + sizeof(BlobTable);
    
    MeshData meshData;
    meshData.vertexCount = 0;
    meshData.indexCount = 0;
    
    BlobTable table;
    table.count = 1;
    table.entries[0].type = ASSET_MESH;
    table.entries[0].offset = header.dataOffset;
    table.entries[0].size = sizeof(MeshData);
    
    // Write asset
    std::ofstream output(outputPath, std::ios::binary);
    if (!output.is_open()) {
        return false;
    }
    
    output.write(reinterpret_cast<const char*>(&header), sizeof(header));
    output.write(reinterpret_cast<const char*>(&table), sizeof(BlobTable));
    output.write(reinterpret_cast<const char*>(&meshData), sizeof(meshData));
    
    // Compute hash
    output.seekp(0);
    std::vector<char> fileData(static_cast<size_t>(output.tellp()));
    output.seekp(0);
    output.read(fileData.data(), fileData.size());
    
    header.hash = computeHash(fileData.data(), fileData.size());
    
    output.seekp(0);
    output.write(reinterpret_cast<const char*>(&header), sizeof(header));
    
    return true;
}

bool AssetCompiler::compileTexture(const std::string& sourcePath, const std::string& outputPath) {
    // Similar to mesh compilation
    return false; // Placeholder
}

uint64_t AssetCompiler::computeHash(const void* data, size_t size) {
    XXH64_hash_t hash = XXH64(data, size, 0);
    return static_cast<uint64_t>(hash);
}

} // namespace reforge::assets
