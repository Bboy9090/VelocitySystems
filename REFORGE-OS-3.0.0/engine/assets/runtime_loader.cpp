#include "runtime_loader.h"
#include <fstream>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#endif

namespace reforge::assets {

AssetFile::AssetFile(const std::string& path) {
    #ifdef _WIN32
        m_fileHandle = CreateFileA(path.c_str(), GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
        if (m_fileHandle == INVALID_HANDLE_VALUE) return;
        
        LARGE_INTEGER fileSize;
        GetFileSizeEx(m_fileHandle, &fileSize);
        m_size = fileSize.QuadPart;
        
        m_mapHandle = CreateFileMapping(m_fileHandle, nullptr, PAGE_READONLY, 0, 0, nullptr);
        if (!m_mapHandle) {
            CloseHandle(m_fileHandle);
            return;
        }
        
        m_data = MapViewOfFile(m_mapHandle, FILE_MAP_READ, 0, 0, 0);
    #else
        m_fd = open(path.c_str(), O_RDONLY);
        if (m_fd == -1) return;
        
        struct stat st;
        if (fstat(m_fd, &st) == -1) {
            close(m_fd);
            return;
        }
        m_size = st.st_size;
        
        m_data = mmap(nullptr, m_size, PROT_READ, MAP_PRIVATE, m_fd, 0);
        if (m_data == MAP_FAILED) {
            m_data = nullptr;
            close(m_fd);
        }
    #endif
    
    // Validate header
    if (m_data) {
        const AssetHeader* header = getHeader();
        if (header->magic != ASSET_MAGIC || header->version != ASSET_VERSION) {
            // Invalid asset file
            #ifdef _WIN32
                UnmapViewOfFile(m_data);
                CloseHandle(m_mapHandle);
                CloseHandle(m_fileHandle);
            #else
                munmap(m_data, m_size);
                close(m_fd);
            #endif
            m_data = nullptr;
        }
    }
}

AssetFile::~AssetFile() {
    if (m_data) {
        #ifdef _WIN32
            UnmapViewOfFile(m_data);
            CloseHandle(m_mapHandle);
            CloseHandle(m_fileHandle);
        #else
            munmap(m_data, m_size);
            close(m_fd);
        #endif
    }
}

const void* AssetFile::getBlob(uint32_t index) const {
    if (!isValid()) return nullptr;
    
    const AssetHeader* header = getHeader();
    const BlobTable* table = reinterpret_cast<const BlobTable*>(
        reinterpret_cast<const uint8_t*>(m_data) + header->tableOffset
    );
    
    if (index >= table->count) return nullptr;
    
    return reinterpret_cast<const uint8_t*>(m_data) + table->entries[index].offset;
}

size_t AssetFile::getBlobSize(uint32_t index) const {
    if (!isValid()) return 0;
    
    const AssetHeader* header = getHeader();
    const BlobTable* table = reinterpret_cast<const BlobTable*>(
        reinterpret_cast<const uint8_t*>(m_data) + header->tableOffset
    );
    
    if (index >= table->count) return 0;
    
    return table->entries[index].size;
}

AssetLoader::AssetLoader() {
}

AssetLoader::~AssetLoader() {
    m_cache.clear();
}

std::unique_ptr<AssetFile> AssetLoader::load(const std::string& path) {
    auto it = m_cache.find(path);
    if (it != m_cache.end()) {
        return std::make_unique<AssetFile>(path); // Return new instance
    }
    
    auto file = std::make_unique<AssetFile>(path);
    if (file->isValid()) {
        m_cache[path] = std::make_unique<AssetFile>(path);
    }
    
    return file;
}

const MeshData* AssetLoader::getMeshData(const AssetFile& file, uint32_t meshIndex) {
    return file.getBlobAs<MeshData>(meshIndex);
}

} // namespace reforge::assets
