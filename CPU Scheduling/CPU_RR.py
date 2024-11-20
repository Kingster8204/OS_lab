import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def round_robin(processes, time_quantum):
    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    queue = []
    current_time = 0
    gantt = []

    while processes or queue:
        # Add all processes that have arrived by the current time to the queue
        while processes and processes[0].arrival_time <= current_time:
            queue.append(processes.pop(0))
        
        if queue:
            process = queue.pop(0)
            start_time = current_time

            if process.remaining_time <= time_quantum:
                # Process completes
                current_time += process.remaining_time
                process.remaining_time = 0
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                gantt.append((process.pid, start_time, current_time))
                
                print(f"Process {process.pid}: Completion Time = {process.completion_time}, "
                      f"Turnaround Time = {process.turnaround_time}, Waiting Time = {process.waiting_time}")
            else:
                # Process does not complete; add it back to the queue
                current_time += time_quantum
                process.remaining_time -= time_quantum
                queue.append(process)
                gantt.append((process.pid, start_time, current_time))
        else:
            # If no process is ready, increment time
            current_time += 1

    draw_gantt_chart(gantt)

def draw_gantt_chart(gantt):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Process ID')
    
    # Set y-ticks for processes
    gnt.set_yticks([i + 1 for i in range(len(gantt))])
    gnt.set_yticklabels([f'P{g[0]}' for g in gantt])

    # Draw bars for each process in the Gantt chart
    for idx, (pid, start, end) in enumerate(gantt):
        gnt.broken_barh([(start, end - start)], (idx + 0.6, 0.8), facecolors='tab:blue')

    plt.show()

# Example Usage
processes = [
    Process(1, 0, 5),  # Process 1: Arrival Time = 0, Burst Time = 5
    Process(2, 1, 3),  # Process 2: Arrival Time = 1, Burst Time = 3
    Process(3, 2, 1)   # Process 3: Arrival Time = 2, Burst Time = 1
]

time_quantum = 2
round_robin(processes, time_quantum)
