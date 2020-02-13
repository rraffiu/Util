#!/usr/tce/bin/python
"""
Calculate and remove center of mass
displacement for an MD trajectory.
Usually needed when zero frequency component in VDOS indicates
if there is a drift present.
"""

from __future__ import print_function
import numpy as np
import sys
import pandas as pd

# Reads merged unwrapped xyz file
#
# Run as
#
# python comdisp.py <unwrapped_merge.xyz>
#
# the output is written to xdatcar_cm_removed.xyz

fname_xyz = sys.argv[1]
el_dict = {}
# Read in the database
df = pd.read_csv('elements.csv',index_col=2)
# Read in the file to process
f_in = open(fname_xyz,'r')
f_out = open('test.xyz','w')
# Build dictionary of unique elements with atomic masses
# from the first frame.
line = f_in.readline().split()
Natoms = int(line[0])
line = f_in.readline()
for i in range(Natoms):
    sym,x,y,z = f_in.readline().split()
    try:
        el = df.loc[sym]
    except:
        sys.exit("ERROR: Incorrect symbol ("+sym+") or no data available for this element.")
    Amass = float(el.loc['AtomicMass'])
    el_dict[sym] = Amass

del df         # Dataframe is no more needed
f_in.seek(0)  # Rewind the file to process

#
coord = []
rcm_past = [0.0,0.0,0.0]
first = True

while True:
    line = f_in.readline()
    if not line:
        break
    f_out.write(line)
    Natoms = int(line.split()[0])
    line = f_in.readline()
    f_out.write(line)
    frame = int(line.split()[0])

    x_frame = y_frame = z_frame = Mtot = 0.0
    # First calculate the CoM
    for i in range(Natoms):
        sym,x,y,z = f_in.readline().split()
        coord.append([str(sym),float(x),float(y),float(z)])
        am = el_dict.get(sym,"")
        Mtot    += am
        x_frame += am*float(x)
        y_frame += am*float(y)
        z_frame += am*float(z)
    rcm_current = [x_frame/Mtot,y_frame/Mtot,z_frame/Mtot]

    print(frame, rcm_current[0],rcm_current[1],rcm_current[2])

    x_frame = y_frame = z_frame = 0.0
    # Update the coordinates
    for j in range(Natoms):
        if first:
            rcm_current = [0.0,0.0,0.0]
            first = False
        x = coord[j][1] - (rcm_current[0] - rcm_past[0])
        y = coord[j][2] - (rcm_current[1] - rcm_past[1])
        z = coord[j][3] - (rcm_current[2] - rcm_past[2])
        el = coord[j][0]
        f_out.write(('{0:4}{1:14.8f}{2:14.8f}{3:14.8f}\n').format(el, x, y, z))
        atm = el_dict.get(el,"")
        x_frame += atm*x
        y_frame += atm*y
        z_frame += atm*z
    rcm_past = [x_frame/Mtot,y_frame/Mtot,z_frame/Mtot]
    coord = []
f_in.close()
f_out.close()
