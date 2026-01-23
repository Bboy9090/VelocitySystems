#pragma once

#include <cstddef>
#include <cstdint>
#include <memory>
#include <new>

namespace reforge::core {

// Memory alignment
constexpr size_t CACHE_LINE_SIZE = 64;
constexpr size_t DEFAULT_ALIGNMENT = 16;

// Aligned allocation
inline void* aligned_alloc(size_t size, size_t alignment = DEFAULT_ALIGNMENT) {
    void* ptr = nullptr;
    #ifdef _WIN32
        ptr = _aligned_malloc(size, alignment);
    #else
        if (posix_memalign(&ptr, alignment, size) != 0) {
            return nullptr;
        }
    #endif
    return ptr;
}

inline void aligned_free(void* ptr) {
    #ifdef _WIN32
        _aligned_free(ptr);
    #else
        free(ptr);
    #endif
}

// Stack allocator (frame-bounded)
class StackAllocator {
public:
    explicit StackAllocator(size_t size);
    ~StackAllocator();

    void* allocate(size_t size, size_t alignment = DEFAULT_ALIGNMENT);
    void reset(); // Reset to beginning (frame end)
    size_t used() const { return m_top; }

private:
    uint8_t* m_memory;
    size_t m_size;
    size_t m_top;
};

// Pool allocator (fixed-size blocks)
template<size_t BlockSize, size_t BlockCount>
class PoolAllocator {
public:
    PoolAllocator() {
        for (size_t i = 0; i < BlockCount - 1; ++i) {
            m_blocks[i].next = &m_blocks[i + 1];
        }
        m_blocks[BlockCount - 1].next = nullptr;
        m_free = &m_blocks[0];
    }

    void* allocate() {
        if (!m_free) return nullptr;
        void* ptr = m_free;
        m_free = m_free->next;
        return ptr;
    }

    void deallocate(void* ptr) {
        Block* block = static_cast<Block*>(ptr);
        block->next = m_free;
        m_free = block;
    }

private:
    struct Block {
        alignas(BlockSize) uint8_t data[BlockSize];
        Block* next;
    };
    Block m_blocks[BlockCount];
    Block* m_free;
};

} // namespace reforge::core
