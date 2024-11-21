import threading
import time
import random

# Shared buffer
buffer = []
MAX_BUFFER_SIZE = 5
items_produced = 10  # Total items to be produced/consumed

# Semaphores
empty_slots = threading.Semaphore(MAX_BUFFER_SIZE)  # Count of empty slots in the buffer
full_slots = threading.Semaphore(0)  # Count of full slots in the buffer

# Producer function
def producer(producer_id):
    for i in range(items_produced):
        time.sleep(random.uniform(0.1, 0.5))  # Simulate production time
        item = random.randint(1, 100)  # Produce an item

        empty_slots.acquire()  # Wait for an empty slot
        buffer.append(item)  # Add the produced item to the buffer
        print(f"Producer {producer_id} produced: {item}")
        full_slots.release()  # Signal that an item has been produced

# Consumer function
def consumer(consumer_id):
    for i in range(items_produced):
        time.sleep(random.uniform(0.1, 0.5))  # Simulate consumption time

        full_slots.acquire()  # Wait for a full slot
        item = buffer.pop(0)  # Remove an item from the buffer
        print(f"Consumer {consumer_id} consumed: {item}")
        empty_slots.release()  # Signal that an item has been consumed

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