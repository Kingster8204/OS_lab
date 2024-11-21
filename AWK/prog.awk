BEGIN {
    FS = ","
    OFS = "|"
    print "Name                 ", "Percentage"
    print "---------------------", "----------"
}
{
    total =0;
    total_sub = 0;

    for(i=2; i<=NF; i++){
        total = total + $i;
        total_sub++;
    }

    percentage = total / total_sub

     printf "%-20s | %9.2f\n", $1, percentage;
}
END {
    printf "Processed" NR "Records"
}