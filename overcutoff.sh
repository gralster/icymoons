#!/bin/sh
#$ -N castep
#$ -V
#$ -cwd
#$ -l h_rt=1:00:00
#$ -pe mpi 16
#$ -j y
#runs castep multiple times on the same cell, changing the cut off energy each time
module add openmpi
module add castep/18.1
cores=16

#python3 startup.py
> cutoff.txt  # creates output file, consider changing name to generic "data" or smth

#modify settings
echo 'kpoints_mp_grid 8 8 8' >> castep.cell
echo 'task: singlepoint' > castep.param
echo 'xc_functional: PBE' >>castep.param
echo 'WRITE_CELL_STRUCTURE: true' >>castep.param
echo 'cut_off_energy: 200' >>castep.param

for i in {100..2000..50}; do # change start, stop, interval here
	sed -i '/cut_off_energy/d' castep.param #delete old cutoff
	echo 'cut_off_energy:' $i >>castep.param #write new cutoff
	echo $i
	mpirun -n $cores castep.mpi castep #run castep
	echo $i >> cutoff.txt
	echo "done"
done
mkdir cutoffconv
mv castep.castep cutoffconv/castep.castep
mv settings.txt cutoffconv/settings.txt
mv cutoff.txt cutoffconv/cutoff.txt
