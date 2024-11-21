BEGIN {
    FS = ","                  # Input field separator
    OFS = "|"                 # Output field separator (for readability in print)
    print "Name                 | Percentage | Grade"
    print "---------------------|------------|-------"
}
{
    total = 0;                # Initialize total marks
    total_sub = 0;            # Initialize subject count

    for (i = 2; i <= NF; i++) {
        total += $i;          # Add marks
        total_sub++;          # Increment subject count
    }

    percentage = total / total_sub;  # Calculate percentage

    # Determine grade based on percentage
    if (percentage > 90) {
        grade = "A";
    } else if (percentage >= 80 && percentage < 90) {
        grade = "B";
    } else if (percentage >= 70 && percentage < 80) {
        grade = "C";
    } else if (percentage >= 60 && percentage < 70) {
        grade = "D";
    } else if (percentage >= 50 && percentage < 60) {
        grade = "E";
    } else {
        grade = "F";
    }

    # Print Name, Percentage, and Grade with uniform width
    printf "%-20s | %10.2f | %-5s\n", $1, percentage, grade;
}
END {
    # Print total records processed
    printf "Processed %d Records\n", NR;
}
