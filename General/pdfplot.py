
from __future__ import print_function
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
plt.rc('text', usetex=True)
rcParams.update({'figure.autolayout': True})

# Data for plotting
fname = sys.argv[1]
T = []
u1 = []
u2 = []
with open(fname,'r') as f:
    line = f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        x,y,z = [float(s) for s in line.split()]
        T.append(x)
        u1.append(y)
        u2.append(z)

Ta = np.asarray(T)
ucm = np.asarray(u1)
uncm = np.asarray(u2)

fig, ax = plt.subplots()
ln1, = ax.plot(Ta,ucm,'-or')
ln2, = ax.plot(Ta,uncm,'-db')
ln1.set_label(r'\bf{with drift}')
ln2.set_label(r'\bf{corrected}')
ax.legend(fontsize=12)
plt.xticks((300,600,900,1200,1500), size=16)
plt.yticks(size=16)

ax.set_xlabel(r'\bf{T (K)}',fontsize=16)
ax.set_ylabel(r'\bf{MSD} (\AA$^2$)',fontsize=16)

fig.savefig("test.pdf")
plt.show(block=False)
