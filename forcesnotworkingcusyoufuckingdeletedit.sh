
#!/bin/sh
read filepath
echo $filepath
> $filepath/steps.txt
>$filepath/f.txt


theline=`grep -n "Total number of ions in cell" $filepath/castep.castep`
n=`echo $theline | cut -f 2 -d ":" | cut -f 2 -d "=" | cut -f 2 -d " " `
nhydrogen=24
ncentral=12
lines=$(($n+5)) #5 to include header
grep -A $lines "* Forces *" $filepath/castep.castep >> f.txt
sed -i '/* Forces */,/x/d' f.txt
x=`grep -n "H" $filepath/forces.txt` #| awk BEGIN'{print $5}'` #cut -c 25-33 f.txt`
#x=`cut -c 1- f.txt`
#z=`cut -c 52-60 f.txt`
echo $x
#echo $y
#echo $z
total=`grep "Final energy, E" $filepath/castep.castep| wc -l`
echo $total
echo $n
echo $(($total/$n))
for i in {1..$n}; do
  echo ${`seq 1 $(($total/$n))`[$i]} >> $filepath/steps.txt
  xbit=`echo $x | cut -f $i -d " "`
  ybit=`echo $y | cut -f $i -d " "`
  zbit=`echo $z | cut -f $i -d " "`
  echo "$xbit^2+ $ybit^2 + $zbit^2" | bc >> $filepath/forces.txt #not square rooted but woteva
  #echo $num
done
