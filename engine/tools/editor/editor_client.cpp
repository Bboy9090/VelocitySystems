// Editor Client (talks to engine via IPC)
// Can be killed without crashing engine

#include "ipc_protocol.h"
#include <iostream>

class EditorClient {
public:
    bool connect(const std::string& pipeName) {
        return transport.connect(pipeName);
    }
    
    void spawnEntity(const std::string& name, float3 pos, float3 rot) {
        struct SpawnCmd {
            char name[64];
            float3 position;
            float3 rotation;
        } cmd;
        
        strncpy(cmd.name, name.c_str(), sizeof(cmd.name) - 1);
        cmd.position = pos;
        cmd.rotation = rot;
        
        Message msg;
        msg.type = MessageType::SpawnEntity;
        msg.size = sizeof(cmd);
        memcpy(msg.data, &cmd, sizeof(cmd));
        
        transport.send(msg);
    }
    
    void setTransform(uint32_t entityID, float3 pos, float3 rot) {
        struct TransformCmd {
            uint32_t entityID;
            float3 position;
            float3 rotation;
        } cmd;
        
        cmd.entityID = entityID;
        cmd.position = pos;
        cmd.rotation = rot;
        
        Message msg;
        msg.type = MessageType::SetTransform;
        msg.size = sizeof(cmd);
        memcpy(msg.data, &cmd, sizeof(cmd));
        
        transport.send(msg);
    }
    
    void play() {
        Message msg;
        msg.type = MessageType::Play;
        msg.size = 0;
        transport.send(msg);
    }
    
    void pause() {
        Message msg;
        msg.type = MessageType::Pause;
        msg.size = 0;
        transport.send(msg);
    }
    
private:
    NamedPipeTransport transport;
};
