// Job System Implementation
// Basic thread pool with work-stealing

#include "job_system.h"
#include <algorithm>
#include <thread>

void JobSystem::init() {
    running = true;
    queues.resize(WORKER_COUNT);
    queueMutexes.resize(WORKER_COUNT);
    
    for (uint32_t i = 0; i < WORKER_COUNT; i++) {
        workers.emplace_back(&JobSystem::workerThread, this, i);
    }
}

void JobSystem::shutdown() {
    running = false;
    cv.notify_all();
    
    for (auto& worker : workers) {
        if (worker.joinable()) {
            worker.join();
        }
    }
}

void JobSystem::submit(Job job) {
    if (job.counter) {
        job.counter->count.fetch_add(1, std::memory_order_relaxed);
    }
    
    // Simple round-robin distribution
    static thread_local uint32_t nextQueue = 0;
    uint32_t queueIndex = nextQueue % WORKER_COUNT;
    nextQueue++;
    
    {
        std::lock_guard<std::mutex> lock(queueMutexes[queueIndex]);
        queues[queueIndex].push(job);
    }
    
    cv.notify_one();
}

void JobSystem::wait(JobCounter& counter) {
    while (counter.count.load(std::memory_order_acquire) > 0) {
        // Try to steal work while waiting
        Job stolen = stealJob();
        if (stolen.fn) {
            stolen.fn();
            if (stolen.counter) {
                stolen.counter->count.fetch_sub(1, std::memory_order_release);
            }
        } else {
            std::this_thread::yield();
        }
    }
}

void JobSystem::workerThread(uint32_t id) {
    while (running) {
        Job job;
        bool found = false;
        
        // Try local queue first
        {
            std::lock_guard<std::mutex> lock(queueMutexes[id]);
            if (!queues[id].empty()) {
                job = queues[id].front();
                queues[id].pop();
                found = true;
            }
        }
        
        // Try to steal from other queues
        if (!found) {
            job = stealJob();
            found = (job.fn != nullptr);
        }
        
        if (found) {
            job.fn();
            if (job.counter) {
                job.counter->count.fetch_sub(1, std::memory_order_release);
            }
        } else {
            // Wait for work
            std::unique_lock<std::mutex> lock(cvMutex);
            cv.wait(lock, [this] { return !running || hasWork(); });
        }
    }
}

Job JobSystem::stealJob() {
    // Try to steal from random queues
    static thread_local uint32_t stealOffset = 0;
    stealOffset = (stealOffset + 1) % WORKER_COUNT;
    
    for (uint32_t i = 0; i < WORKER_COUNT; i++) {
        uint32_t queueIndex = (stealOffset + i) % WORKER_COUNT;
        
        std::lock_guard<std::mutex> lock(queueMutexes[queueIndex]);
        if (!queues[queueIndex].empty()) {
            Job job = queues[queueIndex].front();
            queues[queueIndex].pop();
            return job;
        }
    }
    
    return Job{};
}

bool JobSystem::hasWork() {
    for (uint32_t i = 0; i < WORKER_COUNT; i++) {
        std::lock_guard<std::mutex> lock(queueMutexes[i]);
        if (!queues[i].empty()) {
            return true;
        }
    }
    return false;
}

bool JobSystem::hasWork() {
    for (uint32_t i = 0; i < WORKER_COUNT; i++) {
        std::lock_guard<std::mutex> lock(queueMutexes[i]);
        if (!queues[i].empty()) {
            return true;
        }
    }
    return false;
}
