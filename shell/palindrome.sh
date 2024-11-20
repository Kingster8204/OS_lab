echo "Enter String -:"
read str

n=${#str}
rev=""

for((i=n-1; i>=0; i--)); do
    rev="$rev${str:i:1}"
done

if [ "$str" == "$rev" ]; then
    echo "String is a Palindrome"
else
    echo "String is not a Palindrome"
fi
