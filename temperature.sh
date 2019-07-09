#!/bin/sh
#reads temperature and total time data from .castep output file.
read filepath
echo $filepath
> $filepath/temp.txt
grep "x        Temperature:" $filepath/castep.castep  >> f.txt
awk '{print $3}' f.txt >> $filepath/temp.txt
rm f.txt  # remove helper files
> $filepath/time.txt
grep "Total time " $filepath/castep.castep  >> g.txt
cut -c 23-31 g.txt >> $filepath/time.txt
rm g.txt # remove helper files
#rm castep.castep # not sure if this is a good idea but remember .castep is never overwritten!
