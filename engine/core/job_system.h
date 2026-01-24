// Job System
// Thread pool + work-stealing queues (fiber-based later)

#pragma once

#include <functional>
#include <thread>
#include <atomic>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>

struct JobCounter {
    std::atomic<uint32_t> count{0};
};

struct Job {
    std::function<void()> fn;
    JobCounter* counter = nullptr;
};

class JobSystem {
public:
    void init();
    void shutdown();
    
    void submit(Job job);
    void wait(JobCounter& counter);
    
private:
    void workerThread(uint32_t id);
    Job stealJob();
    bool hasWork();
    
    std::vector<std::thread> workers;
    std::vector<std::queue<Job>> queues;
    std::vector<std::mutex> queueMutexes;
    
    std::atomic<bool> running{false};
    std::condition_variable cv;
    std::mutex cvMutex;
    
    static constexpr uint32_t WORKER_COUNT = 4; // Will use hardware_concurrency - 1 later
};
