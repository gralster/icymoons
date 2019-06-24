#!/bin/sh
#reads final energy and total time data from .castep output file.
read filepath
echo $filepath
> $filepath/finale.txt
grep "Final energy, E" $filepath/castep.castep  >> f.txt
cut -c 32-47 f.txt >> $filepath/finale.txt
rm f.txt  # remove helper files
> $filepath/time.txt
grep "Total time " $filepath/castep.castep  >> g.txt
cut -c 23-31 g.txt >> $filepath/time.txt
rm g.txt # remove helper files
#rm castep.castep # not sure if this is a good idea but remember .castep is never overwritten!
