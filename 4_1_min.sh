#!/bin/bash
max=10000000000000000000000
max2=""
temp=0
words=""
list=$(find ./data -name '*.csv')	
for file in $list
 do
	temp=$(wc ${file}| awk '{print $1}')
	words2=$(wc ${file}| awk '{print $4}')
	if [[ "$temp" -lt "$max" ]]
		then
		max=$temp
		max2=$words2
	fi	
done
actualsize=$(($(stat -c%s "$max2")/1024/1024))
sales=$(tail -n +1 "$max2" | wc -l)
echo "zip was : " + "$max2" ". The file-size was" "$actualsize"  "mb. The sales were :  $sales"


