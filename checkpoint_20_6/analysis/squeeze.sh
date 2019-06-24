#!/bin/sh
#reads volume from the output of a geometryoptimisatoin castep runs
read filepath
echo $filepath
>$filepath/optvol.txt
grep -n "LBFGS: Final Configuration:" $filepath/castep.castep > f.txt
filename='f.txt'
while read line; do
  number=`echo $line | cut -f 1 -d ":" f.txt`
done<$filename
for num in $number; do
  lin=`sed -n "$(($num + 16))p" < $filepath/castep.castep`
  vol=`echo $lin | cut -f 2 -d "="`
  vol=`echo $vol | cut -f 1 -d " "`
  echo $vol >>$filepath/optvol.txt
done
rm f.txt
