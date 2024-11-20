def is_safe(available, max_demand, allocation, need, num_processes, num_resources):
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        allocated_in_this_round = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                # Allocate resources and mark as finished
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                allocated_in_this_round = True

        # If no process was allocated in this round, the system is in an unsafe state
        if not allocated_in_this_round:
            return False, []

    return True, safe_sequence


def get_matrix_input(prompt, rows, num_resources):
    print(prompt)
    matrix = []
    for i in range(rows):
        matrix.append(list(map(int, input(f"Process {i}: ").split())))
    return matrix


def calculate_need(max_demand, allocation, num_processes, num_resources):
    return [
        [max_demand[i][j] - allocation[i][j] for j in range(num_resources)]
        for i in range(num_processes)
    ]


def main():
    # Get input for number of processes and resources
    num_processes = int(input("Enter number of processes: "))
    num_resources = int(input("Enter number of resources: "))

    # Get available resources
    available = list(map(int, input("Enter available resources (space-separated): ").split()))

    # Get maximum demand and allocation matrices
    max_demand = get_matrix_input("Enter max demand matrix:", num_processes, num_resources)
    allocation = get_matrix_input("Enter allocation matrix:", num_processes, num_resources)

    # Calculate the need matrix
    need = calculate_need(max_demand, allocation, num_processes, num_resources)

    # Check system safety
    safe, safe_sequence = is_safe(available, max_demand, allocation, need, num_processes, num_resources)

    if safe:
        print("System is in a safe state.")
        print("Safe sequence:", safe_sequence)
    else:
        print("System is in an unsafe state.")


if __name__ == "__main__":
    main()
