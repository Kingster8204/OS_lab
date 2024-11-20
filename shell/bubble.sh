arr=(10 8 20 100 12)
n=${#arr[@]}

echo "Original Array -: ${arr[*]}"

# Bubble sort algorithm
for ((i=0; i<n; i++)) do
    for ((j=0; j<n-i-1; j++)) do
        # Compare current element with next element
        if [ ${arr[j]} -gt ${arr[$((j+1))]} ]; then
            # Swap elements if they are in the wrong order
            temp=${arr[j]}
            arr[j]=${arr[$((j+1))]}  # Swap element
            arr[$((j+1))]=$temp  # Corrected line
        fi 
    done
done

echo "Sorted Array -: ${arr[*]}"
