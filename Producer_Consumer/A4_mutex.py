import threading
import time
import random

# Shared buffer
buffer = []
MAX_BUFFER_SIZE = 5
buffer_lock = threading.Lock()  # Mutex for synchronizing access to the buffer
items_produced = 10  # Total items to be produced/consumed

# Producer function
def producer(producer_id):
    for i in range(items_produced):
        time.sleep(random.uniform(0.1, 0.5))  # Simulate production time
        item = random.randint(1, 100)  # Produce an item

        with buffer_lock:
            while len(buffer) >= MAX_BUFFER_SIZE:
                buffer_lock.release()  # Release the lock for consumers
                time.sleep(0.1)  # Wait a bit before trying again
                buffer_lock.acquire()  # Acquire the lock again

            buffer.append(item)  # Add the produced item to the buffer
            print(f"Producer {producer_id} produced: {item}")

        # Notify consumers that an item has been produced
        time.sleep(0.1)  # Simulate time between productions

# Consumer function
def consumer(consumer_id):
    for i in range(items_produced):
        time.sleep(random.uniform(0.1, 0.5))  # Simulate consumption time

        with buffer_lock:
            while len(buffer) == 0:
                buffer_lock.release()  # Release the lock for producers
                time.sleep(0.1)  # Wait a bit before trying again
                buffer_lock.acquire()  # Acquire the lock again

            item = buffer.pop(0)  # Remove an item from the buffer
            print(f"Consumer {consumer_id} consumed: {item}")

        # Notify producers that an item has been consumed
        time.sleep(0.1)  # Simulate time between consumptions

if __name__ == "_main_":
    # Create producer and consumer threads
    num_producers = 2
    num_consumers = 2

    producers = [threading.Thread(target=producer, args=(i,)) for i in range(num_producers)]
    consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(num_consumers)]
    
    # Start the threads
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    
    # Wait for all threads to finish
    for p in producers:
        p.join()
    for c in consumers:
        c.join()
    
    print("All items have been produced and consumed.")