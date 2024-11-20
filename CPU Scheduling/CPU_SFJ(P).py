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

def sjf_preemptive(processes):
    current_time = 0
    completed = 0
    gantt = []
    n = len(processes)

    while completed != n:
        # Filter processes that have arrived and are not yet completed
        available_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if available_processes:
            # Select the process with the shortest remaining time
            shortest = min(available_processes, key=lambda x: x.remaining_time)
            start_time = current_time

            # Execute the process for 1 time unit
            current_time += 1
            shortest.remaining_time -= 1
            gantt.append((shortest.pid, start_time, current_time))

            # If the process finishes, update its details
            if shortest.remaining_time == 0:
                completed += 1
                shortest.completion_time = current_time
                shortest.turnaround_time = shortest.completion_time - shortest.arrival_time
                shortest.waiting_time = shortest.turnaround_time - shortest.burst_time

                print(f"Process {shortest.pid}: Completion Time = {shortest.completion_time}, "
                      f"Turnaround Time = {shortest.turnaround_time}, Waiting Time = {shortest.waiting_time}")
        else:
            # If no process is available, move to the next time unit
            current_time += 1

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
    for idx, (pid, start, end) in enumerate(gantt):
        gnt.broken_barh([(start, end - start)], (pid - 0.4, 0.8), facecolors='tab:blue')

    plt.show()

# Example Usage
processes = [
    Process(1, 0, 6),
    Process(2, 1, 8),
    Process(3, 2, 7)
]

sjf_preemptive(processes)
