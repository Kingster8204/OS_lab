#include <iostream>
#include <thread>
#include <semaphore.h>
#include <vector>
#include <queue>
#include <random>
#include <chrono>
#include<mutex>

using namespace std;

// Constants
#define BUFFER_SIZE 5
#define MAX_ITEMS 10

// Shared Resources
queue<int> buffer;
sem_t sem_empty; // Semaphore for empty slots
sem_t sem_full;  // Semaphore for filled slots
mutex mtx;       // Mutex for critical section

// Shared variables
int totalProduced = 0;  // Total items produced
int totalConsumed = 0;  // Total items consumed
bool stop = false;

// Random number generator
random_device rd;
mt19937 gen(rd());
uniform_int_distribution<> dis(1, 5);  // Random delay between 1 and 5 milliseconds

// Producer Function
void producer(int id) {
    while (true) {
        this_thread::sleep_for(chrono::milliseconds(dis(gen)));  // Random delay

        // Stop condition
        if (stop) break;

        int item;

        // Produce an item
        sem_wait(&sem_empty); // Wait for an empty slot
        mtx.lock();           // Lock the buffer

        if (totalProduced >= MAX_ITEMS) {
            stop = true;
            mtx.unlock();
            sem_post(&sem_empty); // Signal other threads
            break;
        }

        item = totalProduced; // Produce a unique item
        buffer.push(item);
        totalProduced++;
        cout << "Producer " << id << " produced: " << item << endl;

        mtx.unlock();    // Unlock the buffer
        sem_post(&sem_full); // Signal a filled slot
    }
}

// Consumer Function
void consumer(int id) {
    while (true) {
        this_thread::sleep_for(chrono::milliseconds(dis(gen)));  // Random delay

        // Stop condition
        if (stop && totalConsumed >= MAX_ITEMS) break;

        sem_wait(&sem_full);  // Wait for a filled slot
        mtx.lock();           // Lock the buffer

        if (buffer.empty() && stop) {
            mtx.unlock();
            sem_post(&sem_full); // Signal other threads
            break;
        }

        int item = buffer.front();
        buffer.pop();
        totalConsumed++;
        cout << "Consumer " << id << " consumed: " << item << endl;

        mtx.unlock();    // Unlock the buffer
        sem_post(&sem_empty); // Signal an empty slot
    }
}

int main() {
    int prodCount, consCount;
    cout << "Enter number of producers: ";
    cin >> prodCount;
    cout << "Enter number of consumers: ";
    cin >> consCount;

    // Initialize semaphores
    sem_init(&sem_empty, 0, BUFFER_SIZE); // Buffer size empty slots
    sem_init(&sem_full, 0, 0);           // No filled slots initially

    // Create producer and consumer threads
    vector<thread> producers, consumers;
    for (int i = 0; i < prodCount; ++i) {
        producers.emplace_back(producer, i + 1);
    }
    for (int i = 0; i < consCount; ++i) {
        consumers.emplace_back(consumer, i + 1);
    }

    // Wait for threads to finish
    for (auto& t : producers) {
        t.join();
    }
    for (auto& t : consumers) {
        t.join();
    }

    // Clean up semaphores
    sem_destroy(&sem_empty);
    sem_destroy(&sem_full);

    cout << "Total items produced: " << totalProduced << endl;
    cout << "Total items consumed: " << totalConsumed << endl;

    return 0;
}
