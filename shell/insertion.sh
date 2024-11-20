echo "Enter the number of elements:"
read n

echo "Enter the elements:"
for ((i=0; i<n; i++)); do
    read arr[i]
done

# Insertion Sort Algorithm
for ((i=1; i<n; i++)); do
    key=${arr[i]}
    j=$((i-1))
    
    # Move elements of arr[0..i-1], that are greater than key, to one position ahead
    while [ $j -ge 0 ] && [ ${arr[j]} -gt $key ]; do
        arr[$((j+1))]=${arr[j]}
        j=$((j-1))
    done
    arr[$((j+1))]=$key
done

echo "Sorted Array using Insertion Sort: ${arr[*]}"
