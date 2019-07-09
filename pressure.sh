#!/bin/sh
#reads pressure and iteration data from .castep output file.
read filepath
echo $filepath
> $filepath/press.txt
grep "  Pressure:   " $filepath/castep.castep  >> f.txt
awk '{print $3}' f.txt >> $filepath/press.txt
rm f.txt  # remove helper files
> $filepath/iter.txt
grep "... finished MD iteration" $filepath/castep.castep  >> g.txt
awk '{print $5}' g.txt >> $filepath/iter.txt
rm g.txt # remove helper files
#rm castep.castep # not sure if this is a good idea but remember .castep is never overwritten!
