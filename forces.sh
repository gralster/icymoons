
#!/bin/sh
read filepath
echo $filepath
> $filepath/forces.txt
>f.txt


theline=`grep -n "Total number of ions in cell" $filepath/castep.castep`
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
echo $ndata
for ((i=1;i<=$ndata;i++)); do
  xbit=`echo $x | cut -d " " -f $i`
  ybit=`echo $y | cut -d " " -f $i`
  zbit=`echo $z | cut -d " " -f $i`
  #echo "($xbit^2)+ ($ybit^2) + ($zbit^2)" | bc
  echo "sqrt(($xbit^2+ $ybit^2 + $zbit^2))" | bc >> $filepath/$(($i%$n+1)).txt
done
