// Editor IPC Protocol
// Headless-first. Killable. No shared state.

#pragma once

#include <cstdint>
#include <vector>
#include <string>

// Message types
enum class MessageType : uint32_t {
    Ping,
    Pong,
    LoadLevel,
    SaveLevel,
    SpawnEntity,
    DestroyEntity,
    SetTransform,
    GetTransform,
    SetComponent,
    GetComponent,
    Play,
    Pause,
    Step,
    Quit,
};

struct Message {
    MessageType type;
    uint32_t size;
    uint8_t data[];
};

// IPC Transport (platform-specific)
class IPCTransport {
public:
    virtual ~IPCTransport() = default;
    virtual bool send(const Message& msg) = 0;
    virtual bool receive(Message& msg) = 0;
    virtual void close() = 0;
};

// Named pipe (Windows) / Unix socket (Linux/macOS)
class NamedPipeTransport : public IPCTransport {
public:
    bool connect(const std::string& name);
    bool send(const Message& msg) override;
    bool receive(Message& msg) override;
    void close() override;
    
private:
    void* handle = nullptr;
};
