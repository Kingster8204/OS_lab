#include <iostream>
#include <mutex>
#include <thread>
#include <condition_variable>
#include <queue>
#include <chrono>
#include <vector>
#include <random>

using namespace std;

#define MAX_SIZE 5
#define MAX_ITEM_COUNT 10

queue<int> buffer;
mutex mtx;
condition_variable notFull;
condition_variable notEmpty;

bool stop = false;
int totalItems = 0;  // To track total items produced

// Random number generator setup
random_device rd;
mt19937 gen(rd());
uniform_int_distribution<> dis(1, 5);  // Random delay between 1 and 5 milliseconds

void producer(int id) {
    int item = 0;
    while (!stop) {
        unique_lock<mutex> lock(mtx);

        // Wait until the buffer is not full
        notFull.wait(lock, [] { return buffer.size() < MAX_SIZE || stop; });

        if (stop || totalItems >= MAX_ITEM_COUNT) break;

        // Produce an item and simulate a random production time
        buffer.push(item);
        cout << "Producer - " << id << " Produced: " << item << endl;
        item++;
        totalItems++;

        // Random delay for production
        this_thread::sleep_for(chrono::milliseconds(dis(gen)));

        notEmpty.notify_one(); // Notify a consumer
    }
}

void consumer(int id) {
    while (!stop) {
        unique_lock<mutex> lock(mtx);

        // Wait until the buffer is not empty
        notEmpty.wait(lock, [] { return !buffer.empty() || stop; });

        if (stop && buffer.empty()) break;

        // Consume an item and simulate a random consumption time
        int item = buffer.front();
        buffer.pop();
        cout << "Consumer - " << id << " Consumed: " << item << endl;

        // Random delay for consumption
        this_thread::sleep_for(chrono::milliseconds(dis(gen)));

        notFull.notify_one(); // Notify a producer
    }
}

int main() {
    int ProdCount, ConsCount;
    cout << "Enter the no. of Producers: ";
    cin >> ProdCount;
    cout << "Enter the no. of Consumers: ";
    cin >> ConsCount;

    vector<thread> prod;  // Vector of producer threads
    vector<thread> cons;  // Vector of consumer threads

    // Create producer threads
    for (int i = 0; i < ProdCount; ++i) {
        prod.emplace_back(producer, i + 1);
    }

    // Create consumer threads
    for (int i = 0; i < ConsCount; ++i) {
        cons.emplace_back(consumer, i + 1);
    }

    // Wait for all threads to finish
    while (totalItems < MAX_ITEM_COUNT) {
        this_thread::sleep_for(chrono::milliseconds(100));
    }

    // Stop the threads
    {
        unique_lock<mutex> lock(mtx);
        stop = true;
    }

    notFull.notify_all();  // Wake up all producers
    notEmpty.notify_all(); // Wake up all consumers

    // Join producer threads
    for (auto& producers : prod) {
        producers.join();
    }

    // Join consumer threads
    for (auto& consumers : cons) {
        consumers.join();
    }

    cout << "Total items produced: " << totalItems << endl;
    return 0;
}
