"""
Calculate and remove center of mass
displacement for an MD trajectory.
Usually needed when zero frequency component in VDOS indicates
if there is a drift present.
"""

from __future__ import print_function
import numpy as np
import sys

# Reads merged unwrapped xyz file
#
# Run as
#
# python comdisp.py <unwrapped_merge.xyz>
#
# the output is written to xdatcar_cm_removed.xyz

fname_xyz = sys.argv[1]
xCM = 0.0
yCM = 0.0
zCM = 0.0
xcm = []
ycm = []
zcm = []
with open(fname_xyz,'r') as f_obj:
    while True:
        line = f_obj.readline().split()
        if not line:
            break
        Natoms = int(line[0])
        frame = int(f_obj.readline().split()[0])
        x_frame = 0.0
        y_frame = 0.0
        z_frame = 0.0
        for i in range(Natoms):
            x,y,z = [float(s) for s in f_obj.readline().split()[1:]]
            x_frame += x
            y_frame += y
            z_frame += z
        xcm.append(x_frame/Natoms)
        ycm.append(y_frame/Natoms)
        zcm.append(z_frame/Natoms)
        xCM += x_frame
        yCM += y_frame
        zCM += z_frame
xCM = xCM/(Natoms*frame)
yCM = yCM/(Natoms*frame)
zCM = zCM/(Natoms*frame)
print('# Reference CM =',xCM,yCM,zCM)
f_in = open (fname_xyz,'r')
f_out= open ('xdatcar_cm_removed.xyz','w')
for i in range(frame):
    dx = xCM - xcm[i]
    dy = yCM - ycm[i]
    dz = zCM - zcm[i]
    line = f_in.readline()
    f_out.write(line)
    line = f_in.readline()
    f_out.write(line)
    for j in range(Natoms):
        line = f_in.readline().split()
        el   = line[0]
        x,y,z = [float(s) for s in line[1:]]
        f_out.write(('{0:4}{1:14.8f}{2:14.8f}{3:14.8f}\n').format(el, x+dx, y+dy, z+dz))
f_in.close()
f_out.close()
