'''Calculates mean sqaure displacement
an MD trajectory.'''

import sys

# Reads merged unwrapped xyz file
#
# Run as
#
# python msd.py <unwrapped_merge.xyz>
#
# the output is written to msd.txt

fname_xyz = sys.argv[1]
# Read in the file to process
f_in = open(fname_xyz,'r')
f_out = open('msd.txt','w')
# Build dictionary of unique elements
# and count them from the first frame.
line = f_in.readline().split()
Natoms = int(line[0])
line = f_in.readline()
species = {}
r_0 = []
for i in range(Natoms):
    sym,x,y,z = f_in.readline().split()
    r_0.append([float(x),float(y),float(z)])
    try:
        species[sym] += 1
    except:
        species[sym] = 1

count = []
for i, key in enumerate(species):
    count.append(species[key])
    species[key] = i

nspecies = len(species)
msd_t = [0.0]*nspecies

line = f_in.readline()
line = f_in.readline()

while line:
    nsteps = int(line.split()[0])
    for i in range(Natoms):
        sym,x,y,z = f_in.readline().split()
        dx2 = (float(x) - r_0[i][0])**2
        dy2 = (float(y) - r_0[i][1])**2
        dz2 = (float(z) - r_0[i][2])**2
        msd_t[species[sym]] += dx2 + dy2 + dz2
    line = f_in.readline()
    line = f_in.readline()

msd = [m/float(nsteps) for m in msd_t]   # time average
fmt = 'msd of {} = {} A^2'
msd_all = 0.0
for i, key in enumerate(species):
    print(fmt.format(key, msd[i]/count[i]))
    msd_all += msd[i]/count[i]
print('msd averaged over all species = {} A^2'.format(msd_all/float(nspecies)))
f_in.close()
f_out.close()
