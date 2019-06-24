#!/bin/sh
module add castep/18.1
python3 startup.py

echo 'kpoints_mp_grid' 2 2 2 >> castep.cell

echo 'task: geometryoptimisation' > castep.param
echo 'xc_functional: PBE' >>castep.param
echo 'cut_off_energy: 600' >>castep.param
echo 'WRITE_CELL_STRUCTURE: true' >>castep.param
#echo 'WRITE_GEOM: true' >> castep.param
#echo 'GEOM_MAX_ITER: 10' >> castep.param
echo 'MAX_SCF_cycles: 50' >> castep.param
>pressures.txt
echo '1' >> pressures.txt
castep.serial castep
mv castep-out.cell castep.cell
for i in {2..4..1}; do
  sed -i '/%BLOCK external_pressure/,$d' castep.cell
  echo '%BLOCK external_pressure' >> castep.cell
  echo '  GPA' >> castep.cell
  echo '     ' $i '0 0' >> castep.cell
  echo '     ' $i '0 ' >> castep.cell
  echo '     ' $i >> castep.cell
  echo '%ENDBLOCK external_pressure' >> castep.cell
  castep.serial castep
  mv castep-out.cell castep.cell
  echo $i >> pressures.txt
  echo "done"
done
