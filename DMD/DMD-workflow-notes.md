# How to reproduce real time DMD pipeline from scratch?
## JDFTx
[JDFTx](https://jdftx.org) is the first principles code that is used to do SCF, phonon, and wannier calculations before running 
the DMD calculations. The JDFTx source code is available from [github](https://github.com/shankar1729/jdftx/tags). You can download 
it to directly to the cluster, for example, the following command,
   
```wget https://github.com/shankar1729/jdftx/archive/refs/tags/v1.7.0.tar.gz```
  
will download the version 1.7 of the code. The tar ball can be unarchived and decompressed using the following command, 

```tar -xvzpf v1.7.0.tar.gz```. 

Once uziped change to the main directory, ```/home/PATH_TO_CODE/jdftx-1.7.0```, replace PATH_TO_CODE with actual path relative to your home directory.
From inside the main directory if you issue command ```ls```, you will see something very similar to the following:   
```Dockerfile  fluid1D  generate_tarball.sh  jdftx```.   

Here you can issue the command, ```mkdir build```, to create the build directory 
where the compiled code or executables would be saved. Now using command ```cd build``` change to the build directory. Inside the build directory
using a text editor of your choice create a text file (```make.sh``` for example, name is really not important) and save the following script in it and issue ```sh make.sh```. 

```cmake
# for UCSC lux cluster using gcc compilers

module load openmpi/gcc/64/1.10.7

#Configure:
CC=mpicc CXX=mpicxx cmake \
   -D EnableMKL=yes \
   -D MKL_PATH="/cm/shared/apps/intel/mkl" \
   -D EnableScaLAPACK=yes \
   -D GSL_PATH="/cm/shared/apps/gsl/2.6" \
   -D ForceFFTW=yes \
   -D FFTW3_PATH="/cm/shared/apps/fftw/fftw-3.3.8" \
   -D EnableLibXC=yes \
   -D LIBXC_PATH="/home/YOUR_USERNAME/Programs/lib/libxc-6.0.0" \
   -D EnableProfiling=yes \
   ../jdftx/

make -j8
```

```cmake
# for stampede2 using intel compilers

module load intel/18.0.2 impi/18.0.2 gsl/2.6

#Configure:
CC=mpicc CXX=mpicxx cmake \
   -D EnableMKL=yes \
   -D MKL_PATH="$TACC_MKL_DIR" \
   -D EnableScaLAPACK=yes \
   -D GSL_PATH="$TACC_GSL_DIR" \
   -D ForceFFTW=yes \
   -D FFTW3_PATH="$TACC_FFTW3_PATH" \
   -D EnableLibXC=yes \
   -D LIBXC_PATH="/home/YOUR_USERNAME/Programs/lib/libxc-6.0.0" \
   -D EnableProfiling=yes \
   ../jdftx/

make -j8
```

There are several bits in the above script which are specific to the HPC platform that you are working with. For example
```module load openmpi/gcc/64/1.10.7``` tells cmake which compilers to use. In this case it instructors to use ```gcc```. Moreover the exact module 
```openmpi/gcc/64/1.10.7``` may not be available. You may want to use ```module avail``` command to check which ```openmpi``` or ```impi``` modules
are available and change accordingly. 

The other platform dependent bits are values of ```MKL_PATH```, ```GSL_PATH```, and ```FFTW3_PATH``` and would need to be changed.
So far the four applications, ```gcc``` or ```icc```, ```MKL```, ```GSL```, and ```FFTW3```, we have discussed are very common to scientific computing
and most HPC platforms will have them already. You would not need to install them. Just find out how to correctly access them. The ```LibXC``` library, 
however, is not usually available on most platforms and you may need to build it yourself and then provide its path to the cmake script above. 

Although a basic compilation can be done without some of the optional libraries but the DMD calculations are computationally expensive and would 
need an optimally customized build. The above script does just that. Also these are condensed instructions to get one started quickly. For comprehensive
information on how to build a fully customized JDFTx code please consult the [JDFTx](https://jdftx.org/Compiling.html) documentation from the developers.

**Note:** For DMD calculations a separate code FynWann is also needed. FynWann uses JDFTx as a library and would give a compile time error if original JDFTx is not
compiled with the profiling option enabled, ```EnableProfiling=yes```.

### Building Libxc
Libxc is a library of exchange-correlation functionals for density functional theory. You can get the library from [Gitlab](https://gitlab.com/libxc/libxc/-/releases), for example, using the ```wget``` command from within the cluster;   
```wget https://gitlab.com/libxc/libxc/-/archive/6.0.0/libxc-6.0.0.tar.gz```.   
Next decompress it with,    
```tar -xvfz libxc-6.0.0.tar.gz```.
After that change to the main directory ```/PATH_TO_LIBRARY/libxc-6.0.0```. If you do not see the ```configure``` file in the main directory, you can create one by issuing:   

```autoreconf -i```.

After that you can issue the following commands in order to build the directroy:

```
CFLAGS="$CFLAGS -std=gnu99" ./configure --enable-shared --prefix="/PATH_TO_LIBRARY/libxc-6.0.0"
make
make check
make install
```   
**Note 1:** The libxc has some code which requires to be compiled with C99 standard, that is why without the compiler flag ```-std=gnu99``` libxc would not compile.   
**Note 2:** JDFTx is built both as an executable and a library (shared object). That is why it is required that libxc is built as a shared object as well otherwise you will have problem compiling JDFTx with libxc. That is why the configure option ```--enable-shared``` is very important.  

### FeynWann

FeynWann is another code which works with JDFTx (and needs compiled JDFTx to compile) to perform important energy calculations and inialiazations for
the DMD calculations. The code is not publically available yet. If you are working on the project you will have private access to it. Download the code and save it at the same location where your JDFTx ```build``` direcotry is. Make a new directory, say, ```build-FeynWann```, and change to it. Inside this directroy save the following script to a file ```make-FeynWann.sh```. 

```cmake
#!/bin/bash
# for building FeynWann on lux
module load openmpi/gcc/64/1.10.7

CC=mpicc CXX=mpicxx cmake \
 -D JDFTX_BUILD="../build" \
 -D JDFTX_SRC="../jdftx" \
 -D ForceFFTW=yes \
 -D FFTW3_PATH="/PATH_TO_LIBRARY/fftw-3.3.8" \
 -D EnableMKL=yes \
 -D MKL_PATH="/PATH_TO_MKL/mkl" \
 -D EnableScaLAPACK=yes \
 -D GSL_PATH="/PATH_TO_LIBRARY/gsl/" \
 -D EnablePETSc=yes \
 -D PETSC_PATH="/PATH_TO_LIBRARY/petsc-3.18.4-build" \
 -D MPISafeWrite=no \
../FeynWann

make -j4
```
### PETSc 
The PETSc library optionally used by FeynWann may not be available on some systems. Here is how to install. Download it from [here](https://petsc.org/release/install/download/#recommended-obtain-release-version-with-git). Inside the main directory make a new directory called ```build``` and run the configure command with following options,

```./configure --prefix=/PATH_TO_LIBRARY/petsc-3.18.4/build --with-blaslapack-dir=/PATH_TO_MKL/mkl --with-mpi-dir=/PATH_TO_OPENMPI/openmpi/gcc/64/1.10.7```.

The configure command prints the next command to run, if there is no problem with the configure options. Run those commands in sequence one after the other to complete the PETSc installation. 

The above setup is required for first of the two parts of DMD simualtions. This part helps obtain the electronic and phonon structure at the Kohn-Sham level and necessary initializations for the DMD calculations. At this stage it is best to run through an example calculation to obtain the electronic and phonon structure using JDFTx. 
## GaAs
### Electronic band structure
We take the example of GaAs for this purpose and first compute its electronic structure. There are two algorithms to find the converged electronic ground state. We first perform SCF and then use the variational minimize - this helps obtain a fully coverged ground state relatively quickly. For the SCF calculations you need input file - very later convenience - split into two files, ```common.in``` and ```scf.in```. 

```
# save this in common.in

lattice face-centered Cubic 10.6829
ion-species Ga_nv3_nocorecorr.upf
ion-species As_nv5_nocorecorr.upf
elec-cutoff 17

ion Ga 0.00 0.00 0.00  0
ion As 0.25 0.25 0.25  0

elec-n-bands 34
converge-empty-states yes
spintype spin-orbit

elec-ex-corr mgga-x-scan mgga-c-scan
```

```
# save this in scf.in

include common.in

kpoint-folding 16 16 16    #Use a Brillouin zone mesh

initial-state totalE.$VAR

electronic-scf energyDiffThreshold 1e-8

dump-name totalE.$VAR
dump Init Symmetries
dump End State
```
These two ```.in``` files specify the structure and other simulations parameters. Along with these two files, you also need to specify either the path to the directory which has pseudopotentials or save the pseudopotential files in the same directory. The pseudpotentials used in this example are available from here, ![Ga](pseudos/Ga_nv3_nocorecorr.upf) and ![As](pseudos/As_nv5_nocorecorr.upf). Here is typical script to run the above SCF calculation with JDFTx. 
```
#!/bin/bash
#SBATCH -p cpuq
#SBATCH --account=cpuq
#SBATCH -N 8
#SBATCH -t 24:00:00
#SBATCH --ntasks-per-node=8
#SBATCH -J jdftx

module load openmpi/gcc/64/1.10.7

pwd; hostname; date

echo "Running program on $SLURM_JOB_NUM_NODES nodes with $SLURM_NTASKS total tasks"
echo  "with each node getting $SLURM_NTASKS_PER_NODE tasks."

MPICMD="mpirun -np $SLURM_NTASKS"
DIRJ="/PATH_TO_EXECUTABLE/JDFTx/jdftx-1.7.0/build"
${MPICMD} ${DIRJ}/jdftx -i scf.in > scf.out
```
After doing the SCF convergence, we repeat the ground state covergence with a different, slower but more reliable, algorithm called ```electronic minimize``` to do the final convergence. It uses the SCF converged state and further converges it. Here is the input for this step,

```
# save the following in totalE.in
include common.in

kpoint-folding 24 24 24    #Use a Brillouin zone mesh

initial-state totalE.$VAR

electronic-minimize energyDiffThreshold 1e-11

dump-name totalE.$VAR
dump End State EigStats BandEigs ElecDensity Vscloc
```
And repeat the calculations by just changing this line in the above batch script,

```${MPICMD} ${DIRJ}/jdftx -i totalE.in > totalE.out```

Once this calculation has converged, the electronic band structure can be calculated. Before doing the 
electronic band structure calculations we must list the high symmetry points in the Brillouin zone to decide
the path along which we want to calculate the band structure. Save the following high symmetry points for GaAs in a file, for
example, ```bandstruct.kpoints.in```, 

```
kpoint 0.000 0.000 0.000     Gamma
kpoint 0.000 0.500 0.500     X
kpoint 0.250 0.750 0.500     W
kpoint 0.500 0.500 0.500     L
kpoint 0.000 0.000 0.000     Gamma
kpoint 0.375 0.750 0.375     K
```
Now to generate k-points along this path run the following, 

```/PATH_TO_EXECUTABLE/JDFTx/jdftx-1.7.0/jdftx/scripts/bandstructKpoints bandstruct.kpoints.in 0.01 bandstruct```

This script will generate two files, ```bandstruct.kpoints``` and ```bandstruct.plot```. The first file has the k-points 
aloing the specified path and the second file has the script to plot the calculated bands. 
Now you can use the following input to run jdftx for bandstructure calculations,

```
# Save the following in bandstruct.in
include common.in
include bandstruct.kpoints

dump-name bandstruct.$VAR
dump End BandEigs Spin

electronic-minimize energyDiffThreshold 1e-11
fix-electron-potential totalE.$VAR
```
Once this is done, you can open the ```bandstruct.plot``` file to modify it a little to make a nice looking band structure plot, 
here is the example, 

```gnuplot
#!/usr/bin/gnuplot -persist
set term pngcairo
set output "GaAs-band.png"

set xtics ( "Gamma" 0,  "X" 142,  "W" 213,  "L" 284,  "Gamma" 458,  "K" 642 )
unset key
nRows = real(system("awk '$1==\"kpoint\" {nRows++} END {print nRows}' bandstruct.kpoints"))
nCols = real(system("wc -c < bandstruct.eigenvals")) / (8*nRows)
formatString = system(sprintf("echo '' | awk 'END { str=\"\"; for(i=0; i<%d; i++) str = str \"%%\" \"lf\"; print str}'", nCols))
set xzeroaxis               #Add dotted line at zero energy
set ylabel "E - VBM [eV]"   #Add y-axis label
set yrange [*:10]           #Truncate bands very far from VBM

plot for [i=1:nCols] "bandstruct.eigenvals" binary format=formatString u 0:((column(i) - 0.180239)*27.21) w l lw 2
```
The above gnuplot scritp will make a figure that looks like the one shown below, 
![Bands](figs/GaAs-band-4x4x4.png)


### Phonon Dispersion
Similarly the phonon dispersion for the same system can be calculated. Although one needs a bigger simulation cell for 
a proper phonon calculation. A supercell made of 4x4x4 unit cells is reasonable cell for this system. Use the following 
jdftx input to calculate force matrix, 

```
include totalE.in          #Full specification of the unit cell calculation
initial-state totalE.$VAR  #Start from converged unit cell state
dump-only                  #Don't reconverge unit cell state

phonon supercell 4 4 4     #Calculate force matrix in a 4x4x4 supercell
```

After the above calculation, the phonon dispersion can be caculated using the following python scrip, 

```python
# save the following to PhononDispersion.py:
import numpy as np
from scipy.interpolate import interp1d

#Read the phonon cell map and force matrix:
cellMap = np.loadtxt("phonon.phononCellMap")[:,0:3].astype(np.int)
forceMatrix = np.fromfile("phonon.phononOmegaSq", dtype=np.float64)
nCells = cellMap.shape[0]
nModes = int(np.sqrt(forceMatrix.shape[0] / nCells))
#Read the k-point path:
kpointsIn = np.loadtxt('bandstruct.kpoints', skiprows=2, usecols=(1,2,3))
nKin = kpointsIn.shape[0]
#--- Interpolate to a 10x finer k-point path:
nInterp = 10
xIn = np.arange(nKin)
x = (1./nInterp)*np.arange(1+nInterp*(nKin-1)) #same range with 10x density
kpoints = interp1d(xIn, kpointsIn, axis=0)(x)
nK = kpoints.shape[0]

#Calculate dispersion from force matrix:
#--- Fourier transform from real to k space:
forceMatrixTilde = np.tensordot(np.exp((2j*np.pi)*np.dot(kpoints,cellMap.T)), forceMatrix, axes=1)
#--- Diagonalize:
omegaSq, normalModes = np.linalg.eigh(forceMatrixTilde)

#Plot phonon dispersion:
import matplotlib.pyplot as plt
meV = 1e-3/27.2114
plt.plot(np.sqrt(omegaSq)/meV)
plt.xlim([0,nK-1])
plt.ylim([0,None])
plt.ylabel("Phonon energy [meV]")
#--- If available, extract k-point labels from bandstruct.plot:
try:
    import subprocess as sp
    kpathLabels = sp.check_output(['awk', '/set xtics/ {print}', 'bandstruct.plot']).split()
    kpathLabelText = [ label.split('"')[1] for label in kpathLabels[3:-2:2] ]
    kpathLabelPos = [ nInterp*int(pos.split(',')[0]) for pos in kpathLabels[4:-1:2] ]
    plt.xticks(kpathLabelPos, kpathLabelText)
except:
    print ('Warning: could not extract labels from bandstruct.plot')
#plt.xticks ( "Gamma" 0,  "X" 71,  "W" 107,  "L" 143,  "Gamma" 230,  "K" 322 )
plt.xticks ([nInterp*0,nInterp*142,nInterp*213,nInterp*284,nInterp*458, nInterp*642],[r"$\Gamma$", "X", "W", "L", r"$\Gamma$", "K"])
plt.savefig("phononDispersion-4x4x4.png", format="png", bbox_inches="tight")
plt.show()
```


![Phonon](figs/phononDispersion.png)
