#!/bin/bash
# call from root bash srcipts/ts.sh database_name amount
# run robot tests arg times and count the successes and fails
fail=0
succ=0
START=1
END=${2}
for (( c=$START; c<=$END; c++ ))
do
   poetry run invoke robots ${1}
   if [ $? -eq 0 ]
   then 
      succ=$((succ + 1))
   else
      fail=$((fail + 1))
   fi

done

echo $succ
echo $fail