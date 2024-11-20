echo "Enter the number of elements:"
read n

echo "Enter the elements:"
for ((i=0; i<n; i++)); do
    read arr[i]
done

# Selection Sort Algorithm
for ((i=0; i<n-1; i++)); do
    min_index=$i
    for ((j=i+1; j<n; j++)); do
        if [ ${arr[j]} -lt ${arr[min_index]} ]; then
            min_index=$j
        fi
    done
    # Swap the found minimum element with the first element
    temp=${arr[i]}
    arr[i]=${arr[min_index]}
    arr[min_index]=$temp
done

echo "Sorted Array using Selection Sort: ${arr[*]}"
