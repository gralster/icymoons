#!/bin/sh
read filepath
echo $filepath
> $filepath/forces.txt
nhydrogen=24
ncentral=12
lines=$(($nhydrogen+$ncentral+5))
grep -A $lines "Symmetrised Forces" $filepath/castep.castep >> f.txt
sed -i '/Symmetrised/,/x/d' f.txt
cut -c 21- f.txt
for i in {1..$lines..1}; do
	
