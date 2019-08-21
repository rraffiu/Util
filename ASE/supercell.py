from ase.build import bulk
from ase.lattice.cubic import BodyCenteredCubic
from ase.units import Bohr

# To create a supcell of 3x3x3 conventional cubic cells
# a1 = bulk('W', 'bcc', a=3.165,cubic=True) *  (3, 3, 3)
# To save the coordinates in xyz format
# ase.io.write('W108.xyz',a1,'xyz')

# To create a supercell with surfaces [110][-110][001] of 4x2x3 cells.
# The atomic coordinates in this case are in atomic units. 
tungsten = BodyCenteredCubic(directions=\
[[1,1,0], [-1,1,0], [0,0,1]], size=(4,2,3), \
symbol='W', pbc=(1,1,1),  latticeconstant=3.165/Bohr)
print(tungsten.get_positions())
