#include "memory.h"

namespace reforge::core {

StackAllocator::StackAllocator(size_t size)
    : m_size(size)
    , m_top(0)
{
    m_memory = static_cast<uint8_t*>(aligned_alloc(size, CACHE_LINE_SIZE));
}

StackAllocator::~StackAllocator() {
    if (m_memory) {
        aligned_free(m_memory);
    }
}

void* StackAllocator::allocate(size_t size, size_t alignment) {
    size_t aligned_top = (m_top + alignment - 1) & ~(alignment - 1);
    if (aligned_top + size > m_size) {
        return nullptr; // Out of memory
    }
    void* ptr = m_memory + aligned_top;
    m_top = aligned_top + size;
    return ptr;
}

void StackAllocator::reset() {
    m_top = 0;
}

} // namespace reforge::core
