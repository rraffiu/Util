'''Calculates mean sqaure displacement
from an MD trajectory.'''

import sys
import numpy as np
# Reads merged unwrapped xyz file
#
# Run as
#
# python msd.py <unwrapped_merge.xyz>  dt
#
# the output is written to msd.txt

def dict_of_elements(key, dic):
    try:
        dic[key] += 1
    except:
        dic[key] = 1


fname_xyz = sys.argv[1]
dt        = float(sys.argv[2])/1000.0  # dt in ps
# Read in the file to process
f_in = open(fname_xyz,'r')
f_out = open('msd.txt','w')

line = f_in.readline().split()
Natoms = int(line[0])
av_pos = np.zeros ((Natoms,3))
line = f_in.readline()

species = {}
first = True
while line:
    nsteps = int(line.split()[0])
    for i in range(Natoms):
        sym,x,y,z = f_in.readline().split()
        av_pos[i,:] += np.array([float(x),float(y),float(z)])
        if first:
            dict_of_elements(sym,species)
    first = False
    line = f_in.readline()
    line = f_in.readline()

av_pos = av_pos/nsteps

f_in.seek(0)

count = []
for i, key in enumerate(species):
    count.append(species[key])
    species[key] = i

nspecies = len(species)


f_out.write('# t(ps)  msd of ')
for j, key in enumerate(species):
    f_out.write('{:.2s} (A^2) '.format(key))
f_out.write('\n')

msd_av = [0.0]*nspecies
line = f_in.readline()
line = f_in.readline()

while line:
    nsteps = int(line.split()[0])
    msd_t = [0.0]*nspecies
    for i in range(Natoms):
        sym,x,y,z = f_in.readline().split()
        dx2 = (float(x) - av_pos[i,0])**2
        dy2 = (float(y) - av_pos[i,1])**2
        dz2 = (float(z) - av_pos[i,2])**2
        msd_t[species[sym]] += dx2 + dy2 + dz2
        msd_av[species[sym]] += dx2 + dy2 + dz2
    f_out.write(('{0:9.4f}  ').format(nsteps*dt))
    for j, key in enumerate(species):
        f_out.write(('{0:.6E}     ').format(msd_t[j]/count[j]))
    f_out.write('\n')
    line = f_in.readline()
    line = f_in.readline()

msd = [m/float(nsteps) for m in msd_av]   # time average
fmt = 'time averaged msd of {} = {:.6E} A^2'
#msd_all = 0.0
for i, key in enumerate(species):
    print(fmt.format(key, msd[i]/count[i]))
#    msd_all += msd[i]/count[i]
#print('msd averaged over all species = {} A^2'.format(msd_all/float(nspecies)))
f_in.close()
f_out.close()
