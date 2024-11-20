#include<iostream>
#include<semaphore.h>
#include<mutex>
#include<vector>
#include<thread>
#include<chrono>

using namespace std;

mutex mtx;
sem_t write_lock;
int read_count = 0;  // Keeps track of the number of readers

struct database{
    int hours;
    int minutes;
    int seconds;
    int data;
} database = {23, 59, 55, 0};

const int iterations = 5;

void incrementClock(){
    database.seconds++;
    if(database.seconds == 60){
        database.seconds = 0;
        database.minutes++;

        if(database.minutes == 60){
            database.minutes = 0;
            database.hours++;

            if(database.hours == 24){
                database.hours = 0;
            }
        }
    }
}

void reader(int id){
    for(int i = 0; i < iterations; i++){
        this_thread::sleep_for(chrono::milliseconds(800));
        mtx.lock();  // Lock to update read_count safely
        read_count++;
        if(read_count == 1){
            sem_wait(&write_lock);  // First reader blocks writers
        }
        mtx.unlock();  // Unlock after updating read_count

        cout << "Reader - " << id << " is Reading - " << database.data
             << " at (" << database.hours << "," << database.minutes << "," << database.seconds << ")" << endl;

        mtx.lock();  // Lock to update read_count safely
        read_count--;
        if(read_count == 0){  // Last reader releases the write lock
            sem_post(&write_lock);
        }
         // Unlock after updating read_count

        cout << "Reader - " << id << " : Exiting Critical Section" << endl;
        
        mtx.unlock(); 
        
    }
    
}

void writer(int id){
    for(int i = 0; i < iterations; i++){
        this_thread::sleep_for(chrono::milliseconds(800));
        sem_wait(&write_lock);  // Block writers if there are readers

        incrementClock();
        database.data++;  // Simulate writing data
        cout << "Writer - " << id << " is Writing : " << database.data
             << " at (" << database.hours << "," << database.minutes << "," << database.seconds << ")" << endl;

        sem_post(&write_lock);  // Release the write lock
    }
}

int main(){
    srand(time(0));

    sem_init(&write_lock, 0, 1);  // Initialize semaphore for write lock

    int read_num, write_num;

    cout << "Enter no. of Readers - ";
    cin >> read_num;
    cout << "Enter no. of Writers - ";
    cin >> write_num;

    vector<thread> readers, writers;

    // Create reader threads
    for(int i = 0; i < read_num; i++){
        readers.push_back(thread(reader, i + 1));
        
    }

    // Create writer threads
    for(int i = 0; i < write_num; i++){
        writers.push_back(thread(writer, i + 1));
    }

    // Join all reader threads
    for(auto& reads : readers){
        reads.join();
        cout<<endl;
    }

    // Join all writer threads
    for(auto& writs : writers){
        writs.join();
    }

    sem_destroy(&write_lock);  // Destroy semaphore after usage

    cout << "All readers and writers have finished.\n";

    return 0;
}
