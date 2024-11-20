import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time  # Time left for the process to complete
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def priority_preemptive(processes):
    current_time = 0
    completed = 0
    gantt = []
    active_process = None
    start_time = None

    while completed != len(processes):
        # Get all available processes (arrived and not completed)
        available_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        if available_processes:
            # Select the process with the highest priority (lowest priority value)
            highest_priority_process = min(available_processes, key=lambda x: x.priority)

            # Record the Gantt chart entry if the active process changes
            if active_process != highest_priority_process:
                if active_process and start_time is not None:
                    gantt.append((active_process.pid, start_time, current_time))
                active_process = highest_priority_process
                start_time = current_time

            # Execute the selected process for 1 time unit
            highest_priority_process.remaining_time -= 1
            current_time += 1

            # If the process finishes execution
            if highest_priority_process.remaining_time == 0:
                completed += 1
                highest_priority_process.completion_time = current_time
                highest_priority_process.turnaround_time = (
                    highest_priority_process.completion_time - highest_priority_process.arrival_time
                )
                highest_priority_process.waiting_time = (
                    highest_priority_process.turnaround_time - highest_priority_process.burst_time
                )

                print(
                    f"Process {highest_priority_process.pid}: Completion Time = {highest_priority_process.completion_time}, "
                    f"Turnaround Time = {highest_priority_process.turnaround_time}, Waiting Time = {highest_priority_process.waiting_time}"
                )
        else:
            # If no process is available, the CPU remains idle
            if active_process and start_time is not None:
                gantt.append((active_process.pid, start_time, current_time))
                active_process = None
                start_time = None
            current_time += 1

    # Add the last active process to the Gantt chart
    if active_process and start_time is not None:
        gantt.append((active_process.pid, start_time, current_time))

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
    Process(1, 0, 6, 2),
    Process(2, 1, 8, 1),
    Process(3, 2, 7, 3)
]

priority_preemptive(processes)
