# How to reproduce real time DMD pipeline from scratch?
## JDFTx
[JDFTx](https://jdftx.org) is the first principles code that is used to do SCF, phonon, and wanier calculations before running 
the DMD calculations. The JDFTx source code is available from [github](https://github.com/shankar1729/jdftx/tags).
Unzip the code after downloading and change to the main directory, ```/home/YOUR_USERNAME/jdftx-1.7.0```.
From inside the main directory if you issue command ```ls```, you will see something very similar to the following:
```Dockerfile  fluid1D  generate_tarball.sh  jdftx```. Here you can issue the command, ``` mkdir build```, to create the build directory 
where the compiled code or executables would be saved. Now using command ```cd build``` change to the build directory. Inside the build directory
using a text editor of your choice create a text file (```make.sh``` for example, name is really not important) and save the following script in it. 

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
