// Window Implementation
// Windows-only for now (Linux/macOS can be added)

#include "window.h"
#include <cstdio>

#ifdef _WIN32

static LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CLOSE:
        PostQuitMessage(0);
        return 0;
    case WM_DESTROY:
        return 0;
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

bool Window::create(const char* title) {
    HINSTANCE hInstance = GetModuleHandle(nullptr);
    instance = hInstance;
    
    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = "EngineWindow";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    
    if (!RegisterClass(&wc)) {
        fprintf(stderr, "Failed to register window class\n");
        return false;
    }
    
    handle = CreateWindowEx(
        0,
        "EngineWindow",
        title,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        width, height,
        nullptr,
        nullptr,
        hInstance,
        nullptr
    );
    
    if (!handle) {
        fprintf(stderr, "Failed to create window\n");
        return false;
    }
    
    ShowWindow((HWND)handle, SW_SHOW);
    return true;
}

void Window::destroy() {
    if (handle) {
        DestroyWindow((HWND)handle);
    }
}

void Window::pollEvents() {
    MSG msg;
    while (PeekMessage(&msg, nullptr, 0, 0, PM_REMOVE)) {
        if (msg.message == WM_QUIT) {
            shouldClose = true;
        }
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
}

#else
// Linux/macOS stubs
bool Window::create(const char* title) {
    fprintf(stderr, "Window creation not implemented for this platform\n");
    return false;
}

void Window::destroy() {}
void Window::pollEvents() {}
#endif
