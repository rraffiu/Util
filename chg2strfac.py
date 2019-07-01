from numpy import *
from ase.calculators.vasp import VaspChargeDensity
from ase.units import Ha,Bohr
import sys

# Read charge density from a file in Vasp CHGCAR format, and write the Fourier transformed
# density to a file in Vasp STRFAC format.
#
# Run as
#
# python chg_fft.py <filename> <encut>
#
# where <filename> is the input charge density and <encut> is the energy cutoff (in eV)
# for the transformed density to be written to the output file.

fname = sys.argv[1]
encut = float(sys.argv[2])
Gcut = sqrt(2*encut/Ha)/Bohr

a = VaspChargeDensity(fname)
chg = a.chg[0]
B = 2*pi*linalg.inv(a.atoms[0].cell).T
dV = a.atoms[0].get_volume()/prod(chg.shape)
N = sum(chg*dV)

chg_fft = fft.fftn(chg)*dV

nmax = [int(x) for x in Gcut/linalg.norm(B, axis=1)]

with open(fname+".fft", "w") as f:
    for bi in B:
        f.write("%12.6f%12.6f%12.6f\n" % tuple(bi))

    for i in range(-nmax[0],nmax[0]+1):
        for j in range(-nmax[1],nmax[1]+1):
            for k in range(-nmax[2],nmax[2]+1):
                Gijk = linalg.norm(i*B[0] + j*B[1] + k*B[2])
                if Gijk<Gcut:
                    f.write("%6d%6d%6d%18g%15g\n" % (i,j,k,real(chg_fft[i,j,k]), imag(chg_fft[i,j,k])))
