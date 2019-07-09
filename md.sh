#!/bin/sh
#reads data from .castep output file.
read filepath

timestep=0.0005

> $filepath/finale.txt
grep "Final energy, E" $filepath/castep.castep  >> f.txt
awk '{print $5}' f.txt >> $filepath/finale.txt
rm f.txt  # remove helper files

echo "done finale.txt"

> $filepath/press.txt
grep "  Pressure:   " $filepath/castep.castep  >> f.txt
awk '{print $3}' f.txt >> $filepath/press.txt
rm f.txt  # remove helper files

echo "done press.txt"

> $filepath/minenth.txt
grep "LBFGS: Final Enthalpy" $filepath/castep.castep  >> f.txt
cut -c 29-45 f.txt >> $filepath/minenth.txt
rm f.txt

echo "done minenth.txt"

> $filepath/temp.txt
grep "x        Temperature:" $filepath/castep.castep  >> f.txt
awk '{print $3}' f.txt >> $filepath/temp.txt
rm f.txt  # remove helper files

echo "done temp.txt"

> $filepath/calctime.txt
grep "Total time " $filepath/castep.castep  >> g.txt
cut -c 23-31 g.txt >> $filepath/calctime.txt
rm g.txt # remove helper files

echo "done calctime.txt"

> $filepath/iter.txt
grep "... finished MD iteration" $filepath/castep.castep  >> f.txt
awk '{print $5}' f.txt >> $filepath/iter.txt
rm f.txt # remove helper files

echo "done iter.txt"

>$filepath/samplediter.txt
len=`wc -l $filepath/iter.txt | awk '{print $1}'`
samplerate=10
for ((i=1;i<=$len;i=$((i+$samplerate)))); do
  echo $i >> $filepath/samplediter.txt
done

echo "done samplediter.txt"

> f.txt
> $filepath/forces.txt
theline=`grep "Total number of ions in cell" $filepath/castep.castep`
n=`echo $theline | cut -f 2 -d ":" | cut -f 2 -d "=" | cut -f 2 -d " " `
lines=$(($n+5)) #5 to include header
grep -A $lines "Forces" $filepath/castep.castep >> f.txt
sed -i '/Forces/,/x/d' f.txt
x=`awk '{print $4}' f.txt`
y=`awk '{print $5}' f.txt`
z=`awk '{print $6}' f.txt`
nlines=`wc -l f.txt | awk '{print $1}'`
nsteps=$(($nlines/($n+2)+1))
ndata=$((n*nsteps))
for ((i=1;i<=$n;i++)); do
  >$filepath/$i.txt
done
for ((i=0;i<=$ndata;i++)); do
  xbit=`echo $x | cut -d " " -f $i`
  ybit=`echo $y | cut -d " " -f $i`
  zbit=`echo $z | cut -d " " -f $i`
  #echo "($xbit^2)+ ($ybit^2) + ($zbit^2)" | bc
  echo "sqrt(($xbit^2+ $ybit^2 + $zbit^2))" | bc >> $filepath/$(($i%$n+1)).txt
done

echo "done all forces"

echo "finished"
