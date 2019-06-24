from numpy import *
from scipy.interpolate import interp1d, make_interp_spline
import matplotlib.pyplot as plt
from ase.calculators.vasp import VaspChargeDensity
from ase.units import Ha,Bohr
import sys

# Reads ELFCAR and converts it into 'cube' format.
#
# Run as
#
# python elf2cube.py <ELFCAR-file>
#

ELF_file = sys.argv[1]

a = VaspChargeDensity(ELF_file)

# ix is the quickest index while iz is the slowest index
# rho(ix:nx,iy:ny,iz:nz)

elf = a.chg[0]

n_atoms  = a.atoms[0].get_number_of_atoms()
nxyz = a.chg[0].shape[:]
index = 1
f_elf = open(ELF_file+".cube","w+")
f_elf.write('{}\n'.format("ELF in cube format"))
f_elf.write('{}\n'.format("ELF"))
f_elf.write(('{:4d}'+'   {: .6f}'*3+'\n').format(n_atoms,0.0,0.0,0.0))
for i in range(3):
    vec = a.atoms[0].cell[i]/nxyz[i]
    f_elf.write(('{:4d}'+'   {: .6f}'*3+'\n').format(nxyz[i],vec[0],vec[1],vec[2]))
for i in range(n_atoms):
    n_atomic = a.atoms[0].get_atomic_numbers()[i]
    p_atom = a.atoms[0].get_positions()[i]
    f_elf.write(('{:4d}  {:3f}'+'   {: .6f}'*3+'\n').format(n_atomic,n_atomic,p_atom[0],p_atom[1],p_atom[2]))
for z in range(nxyz[2]):
    for y in range(nxyz[1]):
        for x in range(nxyz[0]):
            f_elf.write((' {: .6f}').format(elf[x,y,z]))
            if (index%6) == 0:
                f_elf.write('\n')
            index=index+1
f_elf.close()

