
#!/bin/sh
read filepath
echo $filepath
> $filepath/forces.txt
>f.txt


theline=`grep -n "Total number of ions in cell" $filepath/castep.castep`
n=`echo $theline | cut -f 2 -d ":" | cut -f 2 -d "=" | cut -f 2 -d " " `
nhydrogen=24
ncentral=12
lines=$(($n+5)) #5 to include header
grep -A $lines "Forces" $filepath/castep.castep >> f.txt
sed -i '/Forces/,/x/d' f.txt
#nano f.txt
x=`cut -c 25-33 f.txt`
y=`cut -c 46-54 f.txt`
z=`cut -c 67-84 f.txt`
#echo $x

for ((i=1;i<=$n;i++)); do
  echo $i
  xbit=`echo $x | awk "{print \$$i}" `
  ybit=`echo $y | awk '{print $i}'`
  zbit=`echo $z | awk '{print $i}'`
  echo $xbit
  echo "!"
  #echo `"$xbit^2" | bc`
  #echo `"$xbit^2+ $ybit^2 + $zbit^2" | bc `#>> $filepath/forces.txt #not square rooted but woteva
  #echo $num
done
