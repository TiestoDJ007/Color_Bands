#!/usr/bin/env bash
for dir in $(ls *)
do
[ -d $dir ] && echo $dir
cd $dir
cd SO
mpirun -np 16 vasp_std > log
cd ..
mkdir SCF
cp SO/CONTCAR SCF/POSCAR
cp SO/{INCAR,KPOINTS,POTCAR}  SCF/
sed -i s/IBRION[[:space:]]=[[:space:]]2/IBRION = -1/g SCF/INCAR
sed -i s/NSW[[:space:]]=[[:space:]]200/NSW = 1/g SCF/INCAR
cd SCF
mpirun -np 16 vasp_std > log
cd ..
mkdir Band
cd Band
cp ../KPOINTS_band KPOINTS
cp ../SCF/{INCAR,POSCAR,POTCAR,CHGCAR} ../Band/
sed -i s/ICHARG[[:space:]]=[[:space:]]2/ICHARG = 11/g INCAR
mpirun -np 16 vasp_std > log
cd ..
mkdir DOS
cd DOS
mkdir {STEP_1,STEP_2}
cp ../SCF/{INCAR,POSCAR,POTCAR} STEP_1/
cp ../../KPOINTS_DOS STEP_1/
sed -i s/ISMEAR[[:space:]]=[[:space:]]0/ISMEAR = -5/g STEP_1/INCAR
sed -i s/SIGMA[[:space:]]=[[:space:]]0.05/EMIN\\ \\=\\ \\-2\\\\n\\ \\EMAX\\ \\=\\ \\2/g STEP_1/INCAR
cd STEP_1
mpirun -np 16 vasp_std > log
cd ..
cp STEP_1/{CHGCAR,INCAR,KPOINTS,POSCAR,POTCAR} STEP_2/
sed -i /EMAX/aNEDOS\\ \\=\\ \\2001 STEP_2/INCAR
sed -i s/ICHARG[[:space:]]=[[:space:]]2/ICHARG = 11/g STEP_2/INCAR
cd STEP_2
mpirun -np 16 vasp_std > log
done