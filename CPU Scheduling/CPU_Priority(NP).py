import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def priority_non_preemptive(processes):
    # Sort processes by arrival time, then by priority
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    current_time = 0
    gantt = []

    while processes:
        # Get all processes that have arrived by the current time
        available_processes = [p for p in processes if p.arrival_time <= current_time]

        if available_processes:
            # Select the process with the highest priority (lowest priority value)
            process = min(available_processes, key=lambda x: x.priority)
            processes.remove(process)

            # Start executing the selected process
            start_time = current_time
            current_time += process.burst_time

            # Calculate process completion, turnaround, and waiting times
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time

            # Add to the Gantt chart
            gantt.append((process.pid, start_time, current_time))

            # Print process details
            print(f"Process {process.pid}: Completion Time = {process.completion_time}, "
                  f"Turnaround Time = {process.turnaround_time}, Waiting Time = {process.waiting_time}")
        else:
            # If no processes are available, the CPU remains idle
            current_time += 1

    # Draw Gantt chart after all processes are completed
    draw_gantt_chart(gantt)

def draw_gantt_chart(gantt):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Process ID')

    # Extract unique processes for y-ticks
    unique_processes = sorted(set(g[0] for g in gantt))
    gnt.set_yticks([i + 1 for i in range(len(unique_processes))])
    gnt.set_yticklabels([f'P{pid}' for pid in unique_processes])

    # Draw bars for each process in the Gantt chart
    for pid, start, end in gantt:
        gnt.broken_barh([(start, end - start)], (unique_processes.index(pid) + 0.6, 0.8), facecolors='tab:blue')

    plt.show()

# Example Usage
processes = [
    Process(1, 0, 6, 1),
    Process(2, 1, 8, 3),
    Process(3, 2, 7, 2)
]

priority_non_preemptive(processes)
