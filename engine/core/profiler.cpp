// Profiler Implementation

#include "profiler.h"
#include <cstdio>

void Profiler::init() {
    printf("Profiler initialized\n");
}

void Profiler::shutdown() {
    printf("Profiler shutdown\n");
}

void Profiler::beginFrame() {
    PROFILE_FRAME();
}

void Profiler::endFrame() {
    // Tracy handles this automatically
}

void Profiler::markEvent(const std::string& name) {
    PROFILE_SCOPE(name.c_str());
}
