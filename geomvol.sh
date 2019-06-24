#!/bin/bash -l
#$ -S /bin/bash
#$-N geom
#$ -A UKCP_ED_P
#$ -P Free
#$-wd /home/mmm0542/Scratch/output
#$-l h_rt=1:00:00
#$-pe mpi 16
#$-j y

#runs geometry optimisation over increasing VOLUME
module add openmpi
module add castep/18.1
cores=16
#python3 startup.py #creates .cell file
>volumes.txt #initialise output file
#modify settings
echo 'kpoints_mp_grid' 4 4 4  >> castep.cell
#create .param file
echo 'task: geotryoptimisation' > castep.param
echo 'xc_functional: PBE' >>castep.param
echo 'cut_off_energy: 950' >>castep.param
#echo 'basis_precision = MEDIUM' >> castep.param
echo 'WRITE_CELL_STRUCTURE: true' >>castep.param
echo 'WRITE_GEOM: true' >> castep.param
#echo 'GEOM_ENERGY_TOL : 0.001 eV' >> castep.param
#echo 'elec_energy_tol : 1.0e-8 eV' >>castep.param
echo 'elec_method : dm' >>castep.param
echo 'mixing_scheme : Pulay'>> castep.param
echo 'GEOM_MAX_ITER: 70' >> castep.param
#echo 'MAX_SCF_cycles: 50' >> castep.param
#echo 'fix_vol : true'>> castep.param
echo 'continuation : default' >> castep.param
#castep.serial castep
#mv castep-out.cell castep.cell
for i in {1..51..5}; do
  sed -i '/%BLOCK lattice_cart/,/%ENDBLOCK lattice_cart/d' castep.cell # delete previous pressure
  #write new pressure settings
  echo '%BLOCK lattice_cart' >> castep.cell
  echo '     ' $i'     ''0''     ''0' >> castep.cell
  echo '     ' '0''     '$i'     ''0 ' >> castep.cell
  echo '     ' '0''     ''0''     '$i >> castep.cell
  echo '%ENDBLOCK lattice_cart' >> castep.cell
  echo $i
  mpirun -n $cores castep.mpi castep #run castep
  cp castep-out.cell castep.cell
  mv castep-out.cell castep-out$i.cell
  echo $i >> volumes.txt
  echo "done"
done
