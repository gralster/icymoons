#!/bin/sh
#reads enthalpy from the output of a geometryoptimisatoin castep runs

read filepath
echo $filepath
> $filepath/minenth.txt
grep "LBFGS: Final Enthalpy" $filepath/castep.castep  >> f.txt
cut -c 29-45 f.txt >> $filepath/minenth.txt
rm f.txt
