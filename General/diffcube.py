import numpy as np
import time
import sys
import ntpath

# Reads two cube files, substracts the scalar in second
# from the one in first,
# writes difference to a new cube file, retaining the cell
# and atomic positions from the first file.
#
# Run as
#
# python diffcube.py cube1 cube2
#


class cube:
    def __init__(self,Comment=None,Natoms=None,Origin=None,Nxyz=None, \
                 Voxel=None,Zatoms=None,Matoms=None,Patoms=None,Data=None):
        self.Comment = Comment
        self.Natoms  = Natoms
        self.Origin  = Origin
        self.Nxyz    = Nxyz
        self.Voxel   = Voxel
        self.Zatoms  = Zatoms
        self.Matoms  = Matoms
        self.Patoms  = Patoms
        self.Data    = Data


def read_cube(fname):
    f = open(fname, 'r')
    Comment = [None]*2
    Comment[0] = f.readline()
    Comment[1] = f.readline()
    line = f.readline().split()
    Natoms = int(line[0])
    Origin = np.array([ float(x) for x in line[1::] ])
    Nxyz = []
    Voxel = np.empty((3, 3))
    for i in range(3):
        n, x, y, z = [ float(s) for s in f.readline().split() ]
        Nxyz.append(int(n))
        Voxel[i] = np.array([x, y, z])

    Zatoms = np.empty(Natoms, int)
    Matoms = np.empty(Natoms)
    Patoms = np.empty((Natoms, 3))
    for i in range(Natoms):
        line = f.readline().split()
        Zatoms[i] = int(line[0])
        Matoms[i] = float(line[1])
        Patoms[i] = [ float(s) for s in line[2:] ]

    Data = np.array([ float(s) for s in f.read().split() ]).reshape(Nxyz)
    f.close()
    return cube(Comment=Comment,Natoms=Natoms,Origin=Origin,Nxyz=Nxyz,Voxel=Voxel, \
                Zatoms=Zatoms, Matoms=Matoms, Patoms=Patoms, Data=Data)

def write_cube(fname, d):
    f = open(fname, 'w')
    if d.Comment is None:
        f.write('Cube file written with io_cube on ' + time.strftime('%c'))
        f.write('\nOUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z\n')
    else:
        f.write(d.Comment[0])
        f.write(d.Comment[1])
    if d.Origin is None:
        d.Origin = np.zeros(3)
    f.write(('{0:5}{1:12.6f}{2:12.6f}{3:12.6f}\n').format(d.Natoms, *d.Origin))
    for i in range(3):
        n = d.Data.shape[i]
        r = d.Voxel[i]
        f.write(('{0:5}{1:12.6f}{2:12.6f}{3:12.6f}\n').format(n, *r))

    p = d.Patoms
    n = d.Zatoms
    m = d.Matoms
    for Z, M, (x, y, z) in zip(n, m, p):
        f.write(('{0:5}{1:12.6f}{2:12.6f}{3:12.6f}{4:12.6f}\n').format(Z, M, x, y, z))
    index = 1
    for x in range(d.Nxyz[0]):
        for y in range(d.Nxyz[1]):
            for z in range(d.Nxyz[2]):
                f.write((' {: .6E}').format(d.Data[x,y,z]))
                if (index%6) == 0:
                    f.write('\n')
                index=index+1
    f.close()

if __name__=='__main__':
    cube1 = sys.argv[1]
    cube2 = sys.argv[2]
    d1 = read_cube(cube1)
    d2 = read_cube(cube2)
    # The data in files should be of the same size and shape
    if d1.Data.shape != d1.Data.shape:
        sys.exit("ERROR: Data size mismatch in the files.")
    d3 = d1
    d3.Data = d1.Data - d2.Data
    head, tail1 = ntpath.split(cube1)
    head, tail2 = ntpath.split(cube2)
    if tail1.endswith(('.cube','.Cube','.CUBE')):
        f1=tail1.rsplit( ".", 1 )[ 0 ]
    else:
        f1 = tail1
    if tail2.endswith(('.cube','.Cube','.CUBE')):
        f2=tail2.rsplit( ".", 1 )[ 0 ]
    else:
        f2 = tail2
    write_cube(f1+'-'+f2+'.cube',d3)
