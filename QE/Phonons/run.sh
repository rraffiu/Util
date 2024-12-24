#!/bin/sh

PREFIX='w'
TMP_DIR='./tmp'

for q in `seq 1 29 ` ; do

cat > ph.$q.in << EOF
Phonons on a uniform grid
&inputph
  verbosity='debug'
  niter_ph=100
  alpha_mix(1)=0.5
  tr2_ph=1.0d-17
  prefix='$PREFIX'
  ldisp=.true.
  epsil=.false.
  lqdir=.true.
  outdir="$TMP_DIR/$q"
  fildyn  = '$PREFIX.dyn.xml'
  fildvscf = 'dvscf'
  nq1=8, nq2=8, nq3=8,
  start_q=$q
  last_q=$q
/
EOF
cat > submit.$q.pbs << EOF
#!/bin/bash
#PBS -l select=1:ncpus=2:mpiprocs=2
#PBS -N pbs
#PBS -l walltime=6:00:0
#PBS -k doe
#PBS -j oe
#PBS -P fusion
module purge
module load intel-oneapi-compilers/2023.2.1-gcc-12.3.0-sdo2
module load intel-oneapi-mkl
module load hdf5/1.14.2-oneapi-2023.2.1-woz5
cd \$PBS_O_WORKDIR
export OMP_NUM_THREADS=1
time mpirun /home/ullarafi/apps/parallel-qe-7.0-hdf5/bin/ph.x -i ph.$q.in > ph.$q.out
EOF
mkdir $TMP_DIR/$q
cp -r $TMP_DIR/$PREFIX.* $TMP_DIR/$q
echo "  running the phonon calculation for q =  $q "
qsub submit.$q.pbs
done
