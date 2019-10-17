from __future__ import print_function
from numpy import *
from scipy.interpolate import interp1d, make_interp_spline
import matplotlib.pyplot as plt
from ase.calculators.vasp import VaspChargeDensity
from ase.units import Ha,Bohr
import sys

# Reads CHG/CHGCAR and returns total charge and converts it into 'cube' format.
#
# Run as
#
# python chg2cube.py <CHG-file>
#

CHG_file = sys.argv[1]

a = VaspChargeDensity(CHG_file)

# ix is the quickest index while iz is the slowest index
# rho(ix:nx,iy:ny,iz:nz)

rho = a.chg[0]

n_atoms  = a.atoms[0].get_number_of_atoms()
nxyz = a.chg[0].shape[:]
dV = a.atoms[0].get_volume()/prod(rho.shape)
N = sum(rho*dV)  # total charge
print ('Total charge = ',N)
index = 1
f_cube = open(CHG_file+".cube","w+")
f_cube.write('{}\n'.format("CHG in cube format"))
f_cube.write('{}\n'.format("CHG"))
f_cube.write(('{:4d}'+'   {: .6f}'*3+'\n').format(n_atoms,0.0,0.0,0.0))
for i in range(3):
    vec = a.atoms[0].cell[i]/nxyz[i]
    f_cube.write(('{:4d}'+'   {: .6f}'*3+'\n').format(nxyz[i],vec[0],vec[1],vec[2]))
for i in range(n_atoms):
    n_atomic = a.atoms[0].get_atomic_numbers()[i]
    p_atom = a.atoms[0].get_positions()[i]
    f_cube.write(('{:4d}  {:3f}'+'   {: .6f}'*3+'\n').format(n_atomic,n_atomic,p_atom[0],p_atom[1],p_atom[2]))
for x in range(nxyz[0]):
    for y in range(nxyz[1]):
        for z in range(nxyz[2]):
            f_cube.write((' {: .6E}').format(rho[x,y,z]))
            if (index%6) == 0:
                f_cube.write('\n')
            index=index+1
f_cube.close()
