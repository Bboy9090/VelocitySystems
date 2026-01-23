#pragma once

#include <cstdint>
#include <string>

namespace reforge::platform {

// IPC message types
enum class IPCMessageType : uint32_t {
    LoadLevel = 1,
    HotReloadAsset = 2,
    Pause = 3,
    Step = 4,
    SetTimeScale = 5,
};

// IPC message
struct IPCMessage {
    IPCMessageType type;
    uint64_t payload; // Pointer or data
    uint32_t size;
};

// Editor IPC server (headless engine)
class EditorIPC {
public:
    EditorIPC();
    ~EditorIPC();
    
    // Initialize IPC (shared memory + message queue)
    bool init(const std::string& name);
    
    // Process messages (non-blocking)
    void processMessages();
    
    // Send message to editor
    bool sendToEditor(const IPCMessage& msg);
    
    // Receive message from editor
    bool receiveFromEditor(IPCMessage& msg);

private:
    void* m_sharedMemory = nullptr;
    size_t m_sharedMemorySize = 0;
    
    #ifdef _WIN32
        void* m_fileMapping = nullptr;
    #else
        int m_shmFd = -1;
    #endif
    
    bool createSharedMemory(const std::string& name, size_t size);
    void destroySharedMemory();
};

} // namespace reforge::platform
