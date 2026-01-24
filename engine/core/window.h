// Window Management
// Platform-agnostic window creation

#pragma once

#ifdef _WIN32
#include <windows.h>
typedef HWND WindowHandle;
typedef HINSTANCE WindowInstance;
#else
typedef void* WindowHandle;
typedef void* WindowInstance;
#endif

struct Window {
    WindowHandle handle = nullptr;
    WindowInstance instance = nullptr;
    uint32_t width = 1920;
    uint32_t height = 1080;
    bool shouldClose = false;
    
    bool create(const char* title);
    void destroy();
    void pollEvents();
};
