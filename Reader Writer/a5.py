import threading
import time
import random

read_count = 0
mutex = threading.Semaphore(1)
write_lock = threading.Semaphore(1)
database = {'hours': 0, 'minutes': 0, 'seconds': 0}
iterations = 5

def reader(reader_id):
    global read_count
    for _ in range(iterations):
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            write_lock.acquire()
        mutex.release()

        print(f"Reader {reader_id} reads: {database['hours']}:{database['minutes']}:{database['seconds']}")
        time.sleep(random.uniform(0.1, 0.5))

        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            write_lock.release()
        mutex.release()
        time.sleep(random.uniform(0.1, 0.5))

def writer(writer_id):
    global database
    for _ in range(iterations):
        write_lock.acquire()

        database['hours'] = random.randint(0, 23)
        database['minutes'] = random.randint(0, 59)
        database['seconds'] = random.randint(0, 59)
        print(f"Writer {writer_id} updates time to: {database['hours']}:{database['minutes']}:{database['seconds']}")
        time.sleep(random.uniform(0.1, 0.5))

        write_lock.release()
        time.sleep(random.uniform(0.1, 0.5))

num_readers = 3
num_writers = 2
reader_threads = [threading.Thread(target=reader, args=(i+1,)) for i in range(num_readers)]
writer_threads = [threading.Thread(target=writer, args=(i+1,)) for i in range(num_writers)]

for t in reader_threads + writer_threads:
    t.start()

for t in reader_threads + writer_threads:
    t.join()

print("All readers and writers have finished.")
