#!/bin/sh
read filepath
nhydrogen=`grep "H" $filepath/castep.xyz| wc -l`
ncarbon=`grep "C" $filepath/castep.xyz| wc -l`
noxygen=`grep "O" $filepath/castep.xyz| wc -l`
ntotal=$(($nhydrogen+$noxygen+$ncarbon))
line
