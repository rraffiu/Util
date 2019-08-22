"""
IO support for the qb@ll sys format.
"""

from ase.atoms import Atoms
from ase.units import Bohr

def write_sys(fileobj, atoms):
    """
    Function to write a sys file.

    fileobj: str or file object
        File to which output is written.
    atoms: Atoms object
        Atoms object specifying the atomic configuration.
    """
    fileobj.write('set cell  ')
    for i in range(3):
        d = atoms.cell[i]/Bohr
        fileobj.write(('{:6f}  {:6f}  {:6f}').format(*d))
    fileobj.write('  bohr\n')

    ch_sym = atoms.get_chemical_symbols()
    atm_nm = atoms.numbers
    a_pos  = atoms.positions
    an     = list(set(atm_nm))

    for i, s in enumerate(set(ch_sym)):
        fileobj.write(('species {}{} pseudopotenitalfile\n').format(s,an[i]))
    i = 1
    for S, Z, (x, y, z) in zip(ch_sym, atm_nm, a_pos):
        fileobj.write(('atom {0:5} {1:5}  {2:12.6f}{3:12.6f}{4:12.6f} bohr\n').format(S+str(i),S+str(Z), x, y, z))
        i +=1
