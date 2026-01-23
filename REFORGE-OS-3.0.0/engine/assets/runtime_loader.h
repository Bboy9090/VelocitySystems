#pragma once

#include "compiler.h"
#include <cstdint>
#include <string>
#include <memory>

namespace reforge::assets {

// Memory-mapped asset file
class AssetFile {
public:
    AssetFile(const std::string& path);
    ~AssetFile();
    
    bool isValid() const { return m_data != nullptr; }
    
    const AssetHeader* getHeader() const {
        return reinterpret_cast<const AssetHeader*>(m_data);
    }
    
    const void* getBlob(uint32_t index) const;
    size_t getBlobSize(uint32_t index) const;
    
    template<typename T>
    const T* getBlobAs(uint32_t index) const {
        return reinterpret_cast<const T*>(getBlob(index));
    }

private:
    void* m_data = nullptr;
    size_t m_size = 0;
    
    #ifdef _WIN32
        void* m_fileHandle = nullptr;
        void* m_mapHandle = nullptr;
    #else
        int m_fd = -1;
    #endif
};

// Runtime asset loader
class AssetLoader {
public:
    AssetLoader();
    ~AssetLoader();
    
    // Load asset file
    std::unique_ptr<AssetFile> load(const std::string& path);
    
    // Get mesh data
    const MeshData* getMeshData(const AssetFile& file, uint32_t meshIndex);

private:
    std::unordered_map<std::string, std::unique_ptr<AssetFile>> m_cache;
};

} // namespace reforge::assets
