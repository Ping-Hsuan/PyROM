import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import sys
import operator
from operator import itemgetter, attrgetter

plt.style.use('report')

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
print("---------------------------------------------")

isExist = os.path.exists(os.getcwd()+'/effectivity/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/effectivity/')
    print("Create the target directory successfully")
print("---------------------------------------------")

root = os.getcwd()
tpath = './effectivity/'

# compute the effectivity
angle = np.loadtxt(root+'/dual_norm/angle.dat')
residual = np.loadtxt(root+'/dual_norm/erri.dat')
rom_abserr = np.loadtxt(root+'/rom_abserr/rom_abserr.dat')
effectivity = residual/rom_abserr

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(angle, effectivity, 'k-o', mfc="None")
ax.set_ylabel(r'$\eta$')
ax.set_xlabel(r'$\theta_g$')
ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
#ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig(tpath+'effectivity.png')
print(tpath+'effectivity.png saved successfully')
np.savetxt(tpath+'angle.dat', angle)
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'effectivity.dat', effectivity)
print(tpath+'effectivity.dat saved successfully')
print("---------------------------------------------")
