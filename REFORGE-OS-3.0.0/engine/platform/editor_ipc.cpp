#include "editor_ipc.h"
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#endif

namespace reforge::platform {

EditorIPC::EditorIPC() {
}

EditorIPC::~EditorIPC() {
    destroySharedMemory();
}

bool EditorIPC::init(const std::string& name) {
    const size_t size = 1024 * 1024; // 1MB shared memory
    return createSharedMemory(name, size);
}

void EditorIPC::processMessages() {
    if (!m_sharedMemory) return;
    
    IPCMessage msg;
    while (receiveFromEditor(msg)) {
        switch (msg.type) {
            case IPCMessageType::LoadLevel:
                // Handle load level
                break;
            case IPCMessageType::HotReloadAsset:
                // Handle hot reload
                break;
            case IPCMessageType::Pause:
                // Handle pause
                break;
            case IPCMessageType::Step:
                // Handle step
                break;
            case IPCMessageType::SetTimeScale:
                // Handle time scale
                break;
        }
    }
}

bool EditorIPC::sendToEditor(const IPCMessage& msg) {
    if (!m_sharedMemory) return false;
    
    // Write to shared memory (would use proper message queue in production)
    std::memcpy(m_sharedMemory, &msg, sizeof(msg));
    return true;
}

bool EditorIPC::receiveFromEditor(IPCMessage& msg) {
    if (!m_sharedMemory) return false;
    
    // Read from shared memory (would use proper message queue in production)
    std::memcpy(&msg, m_sharedMemory, sizeof(msg));
    return msg.type != IPCMessageType(0);
}

bool EditorIPC::createSharedMemory(const std::string& name, size_t size) {
    m_sharedMemorySize = size;
    
    #ifdef _WIN32
        std::string mapName = "Local\\" + name;
        m_fileMapping = CreateFileMappingA(INVALID_HANDLE_VALUE, nullptr, PAGE_READWRITE, 0, static_cast<DWORD>(size), mapName.c_str());
        if (!m_fileMapping) return false;
        
        m_sharedMemory = MapViewOfFile(m_fileMapping, FILE_MAP_ALL_ACCESS, 0, 0, size);
        if (!m_sharedMemory) {
            CloseHandle(m_fileMapping);
            return false;
        }
    #else
        std::string shmName = "/" + name;
        m_shmFd = shm_open(shmName.c_str(), O_CREAT | O_RDWR, 0666);
        if (m_shmFd == -1) return false;
        
        if (ftruncate(m_shmFd, size) == -1) {
            close(m_shmFd);
            return false;
        }
        
        m_sharedMemory = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, m_shmFd, 0);
        if (m_sharedMemory == MAP_FAILED) {
            close(m_shmFd);
            return false;
        }
    #endif
    
    // Initialize to zero
    std::memset(m_sharedMemory, 0, size);
    
    return true;
}

void EditorIPC::destroySharedMemory() {
    if (m_sharedMemory) {
        #ifdef _WIN32
            UnmapViewOfFile(m_sharedMemory);
            if (m_fileMapping) {
                CloseHandle(m_fileMapping);
            }
        #else
            munmap(m_sharedMemory, m_sharedMemorySize);
            if (m_shmFd != -1) {
                close(m_shmFd);
            }
        #endif
        m_sharedMemory = nullptr;
    }
}

} // namespace reforge::platform
