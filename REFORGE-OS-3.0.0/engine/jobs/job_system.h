#pragma once

#include <atomic>
#include <functional>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>

namespace reforge::jobs {

// Job counter (dependency tracking)
class JobCounter {
public:
    JobCounter() : m_count(0) {}
    
    void increment() {
        m_count.fetch_add(1, std::memory_order_relaxed);
    }
    
    void decrement() {
        if (m_count.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            // Last job completed
        }
    }
    
    bool isZero() const {
        return m_count.load(std::memory_order_acquire) == 0;
    }
    
    void wait() {
        while (!isZero()) {
            std::this_thread::yield();
        }
    }

private:
    std::atomic<uint32_t> m_count;
};

// Job definition
struct Job {
    std::function<void()> function;
    JobCounter* counter = nullptr;
    
    void execute() {
        if (function) {
            function();
        }
        if (counter) {
            counter->decrement();
        }
    }
};

// Job system (work-stealing, fiber-ready)
class JobSystem {
public:
    JobSystem(uint32_t workerCount = 0);
    ~JobSystem();

    void submit(Job job);
    void submit(Job job, JobCounter& counter);
    
    void wait(JobCounter& counter);
    void waitAll();
    
    void shutdown();

private:
    static constexpr uint32_t MAX_WORKERS = 16;
    
    uint32_t m_workerCount;
    std::vector<std::thread> m_workers;
    std::vector<std::queue<Job>> m_queues;
    std::vector<std::mutex> m_queueMutexes;
    
    std::atomic<bool> m_running;
    
    void workerLoop(uint32_t workerId);
    Job stealJob(uint32_t thiefId);
};

// Global job system instance
extern JobSystem* g_jobSystem;

// Initialize job system
void initJobSystem(uint32_t workerCount = 0);

// Shutdown job system
void shutdownJobSystem();

} // namespace reforge::jobs
