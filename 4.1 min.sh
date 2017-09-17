#!/bin/bash
max=10000000000000000000000
max2=""
temp=0
words=""
list=$(find . -name '/data/*.csv')	
for file in $list; do
	temp=`wc ${file}| awk '{print $1}'`
	words2=`wc ${file}| awk '{print $4}'`
	if [[ "$temp" -lt "$max" ]]
		then
		max=$temp
		max2=$words2
		echo "new max"
	fi	
done
actualsize=$(stat -c%s "$max2")
sales=$(tail -n +1 "$max2" | wc -l)
echo "zip was : " + "$max2" "the file-size was" "$actualsize"  " the sales were :  $sales"


