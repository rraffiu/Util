#!bin/bash

# produce a merged wrapped xdatcar from multiple
# xdatcar files (trajectory): xdatcar_merged
merge_xdat.pl xdatcar. 4 10

# uwrap the merged xdatcar file
unwrap_xdatcar.x  xdatcar_merged

# convert unwraped_merged_xdatcar to xyz format
xdatcar2xyz.x xdatcar_merged_unwrapped

# remove any drift of the center of mass
python rm_cm_drift.py xdatcar_merged_unwrapped.xyz

# calculate the VACF
cat > vacf.in << EOF
xdatcar_cm_removed.xyz
vacf.dat    # output file
82.683      # Time step in atomic units
5           # Window space (in terms of iterations)
3           # Window length (in ps)
Cu          # Atom type to track
EOF
VACF.x < vacf.in

# calculate the VDOS
cat > vdos.in << EOF
vacf.dat  # input vacf data
256       # number of atoms
vdos.dat  # output file
5         # npad (don't know what it is but source says 15 is reasonable)
8         # min no. of time steps used to sample the shortest osc. (16 is reasonable)
EOF
VDOS-smooth.x < vdos.in

# calculate thermal properties including msd, output is saved to msd.dat
cat > msd.in << EOF
256       # number of atoms
0.5       # min cut off frequency in THz
200       # max cut off frequency in THz
2300       # temperature in K
63.546    # atomic mass in amu (not in a.u.)
vdos.dat  # vdos data file
msd.dat   # output file name
EOF
thermal.x < msd.in
