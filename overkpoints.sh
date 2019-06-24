#!/bin/sh
#$ -N kpoints

#$ -V
#$ -cwd
#$ -l h_rt=1:00:00
#$ -pe mpi 16
#$ -j y
#runs castep multiple times on one cell file, changing kpoint sampling grid each time.
module add openmpi
module add castep/18.1
cores=16
#python3 startup.py
> kpoints.txt   #creates output file, overwriting. consider giving generic name to make easier
#.param file settings
echo 'task: singlepoint' > castep.param
echo 'xc_functional: PBE' >>castep.param
echo 'cut_off_energy: 400' >>castep.param
echo 'WRITE_CELL_STRUCTURE: true' >>castep.param
#.cell file settings
echo 'kpoints_mp_grid 2 2 2' >> castep.cell



for i in {3..50..1}; do #adjust start, end and step size here
	sed -i '/kpoints_mp_grid/d' castep.cell #delete old kpoints
	echo 'kpoints_mp_grid' $i $i $i >> castep.cell #write new kpoints
	echo $i
	mpirun -n $cores castep.mpi castep #run castep
 	echo $i >> kpoints.txt
	echo "done"
done
mkdir kpointconv
mv castep.castep kpointconv/castep.castep
mv kpoints.txt kpointconv/kpoints.txt
