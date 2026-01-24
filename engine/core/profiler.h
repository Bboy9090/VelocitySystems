// Profiling System
// Tracy integration and performance tracking

#pragma once

#include <string>

#ifdef TRACY_ENABLE
#include "tracy/Tracy.hpp"
#define PROFILE_FRAME() FrameMark
#define PROFILE_SCOPE(name) ZoneScopedN(name)
#define PROFILE_SCOPE_COLOR(name, color) ZoneScopedNC(name, color)
#else
#define PROFILE_FRAME()
#define PROFILE_SCOPE(name)
#define PROFILE_SCOPE_COLOR(name, color)
#endif

class Profiler {
public:
    static void init();
    static void shutdown();
    static void beginFrame();
    static void endFrame();
    static void markEvent(const std::string& name);
};
