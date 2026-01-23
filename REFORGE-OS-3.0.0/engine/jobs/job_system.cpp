#include "job_system.h"
#include <thread>

namespace reforge::jobs {

JobSystem* g_jobSystem = nullptr;

JobSystem::JobSystem(uint32_t workerCount)
    : m_running(true)
{
    if (workerCount == 0) {
        workerCount = std::max(1u, std::thread::hardware_concurrency() - 1);
    }
    m_workerCount = std::min(workerCount, MAX_WORKERS);
    
    m_queues.resize(m_workerCount);
    m_queueMutexes.resize(m_workerCount);
    
    for (uint32_t i = 0; i < m_workerCount; ++i) {
        m_workers.emplace_back(&JobSystem::workerLoop, this, i);
    }
}

JobSystem::~JobSystem() {
    shutdown();
}

void JobSystem::submit(Job job) {
    if (m_workerCount == 0) {
        job.execute();
        return;
    }
    
    // Round-robin distribution
    static thread_local uint32_t nextQueue = 0;
    uint32_t queueId = nextQueue % m_workerCount;
    nextQueue++;
    
    std::lock_guard<std::mutex> lock(m_queueMutexes[queueId]);
    m_queues[queueId].push(job);
}

void JobSystem::submit(Job job, JobCounter& counter) {
    counter.increment();
    job.counter = &counter;
    submit(job);
}

void JobSystem::wait(JobCounter& counter) {
    while (!counter.isZero()) {
        // Try to steal work while waiting
        Job stolen = stealJob(0); // Use main thread as "worker 0"
        if (stolen.function) {
            stolen.execute();
        } else {
            std::this_thread::yield();
        }
    }
}

void JobSystem::waitAll() {
    // Wait for all queues to be empty
    bool allEmpty = false;
    while (!allEmpty) {
        allEmpty = true;
        for (uint32_t i = 0; i < m_workerCount; ++i) {
            std::lock_guard<std::mutex> lock(m_queueMutexes[i]);
            if (!m_queues[i].empty()) {
                allEmpty = false;
            }
        }
        if (!allEmpty) {
            std::this_thread::yield();
        }
    }
}

void JobSystem::shutdown() {
    m_running = false;
    
    for (auto& worker : m_workers) {
        if (worker.joinable()) {
            worker.join();
        }
    }
}

void JobSystem::workerLoop(uint32_t workerId) {
    while (m_running) {
        Job job;
        bool found = false;
        
        // Try local queue first
        {
            std::lock_guard<std::mutex> lock(m_queueMutexes[workerId]);
            if (!m_queues[workerId].empty()) {
                job = m_queues[workerId].front();
                m_queues[workerId].pop();
                found = true;
            }
        }
        
        // Steal if local queue empty
        if (!found) {
            job = stealJob(workerId);
            found = (job.function != nullptr);
        }
        
        if (found) {
            job.execute();
        } else {
            std::this_thread::yield();
        }
    }
}

Job JobSystem::stealJob(uint32_t thiefId) {
    // Try to steal from other queues
    for (uint32_t i = 0; i < m_workerCount; ++i) {
        uint32_t victimId = (thiefId + i + 1) % m_workerCount;
        
        std::lock_guard<std::mutex> lock(m_queueMutexes[victimId]);
        if (!m_queues[victimId].empty()) {
            Job job = m_queues[victimId].front();
            m_queues[victimId].pop();
            return job;
        }
    }
    
    return Job{};
}

void initJobSystem(uint32_t workerCount) {
    if (!g_jobSystem) {
        g_jobSystem = new JobSystem(workerCount);
    }
}

void shutdownJobSystem() {
    if (g_jobSystem) {
        delete g_jobSystem;
        g_jobSystem = nullptr;
    }
}

} // namespace reforge::jobs
