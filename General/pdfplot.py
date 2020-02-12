
 from __future__ import print_function
 import sys
 import ntpath
 import matplotlib
 import matplotlib.pyplot as plt
 import numpy as np
 from matplotlib import rcParams
 plt.rc('text', usetex=True)
 rcParams.update({'figure.autolayout': True})

 # Data for plotting
 fname = sys.argv[1]
 T,u_uncor,u_cor = np.loadtxt(fname,dtype='float',comments='#',unpack=True)

 fig, ax = plt.subplots()
 ln1, = ax.plot(T,u_uncor,'-or')
 ln2, = ax.plot(T,u_cor,'-db')
 ln1.set_label(r'\bf{with drift}')
 ln2.set_label(r'\bf{corrected}')
 ax.legend(fontsize=12)
 #plt.xticks((300,600,900,1200,1500,1800,2100,2400,2700,3000,3300), size=16)
 plt.xticks(size=16)
 plt.yticks(size=16)

 ax.set_xlabel(r'\bf{T (K)}',fontsize=16)
 ax.set_ylabel(r'\bf{MSD} (\AA$^2$)',fontsize=16)

 head, tail = ntpath.split(fname) # split path from file name
 fsave = tail.rsplit( ".", 1 )[ 0 ] # remove extention from file name
 fig.savefig(fsave+".pdf")
 plt.show(block=False)
