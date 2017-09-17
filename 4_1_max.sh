#!/bin/bash
max=0
max2=""
temp=0
words=""
list=$(find ./data -name '*.csv')	
for file in $list; do
	temp=`wc ${file}| awk '{print $1}'`
	words2=`wc ${file}| awk '{print $4}'`
	if [[ "$temp" -gt "$max" ]]
		then
		max=$temp
		max2=$words2
	fi	
done
actualsize=$(stat -c%s "$max2")
sales=$(tail -n +1 "$max2" | wc -l)
echo "zip was : "  "$max2" "the file-size was" "$actualsize"  " the sales were : " "$sales" 

