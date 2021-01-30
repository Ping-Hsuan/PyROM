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
os.chdir(str(sys.argv[1]))
print("---------------------------------------------")
N = str(sys.argv[2])

isExist = os.path.exists(os.getcwd()+'/dual_norm_scaled/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/dual_norm_scaled/')
    print("Create the target directory successfully")
print("---------------------------------------------")

root = os.getcwd()
sp1 = (root.split('/'))
for element in sp1:
    z = re.match(r"theta_(\d+)", element)
    if z:
        anchor = float(((z.groups())[0]))

tpath = './dual_norm_scaled/'

# compute the dual_norm_scaled
angle = np.loadtxt(root+'/dual_norm/angle.dat')
residual = np.loadtxt(root+'/dual_norm/erri_N'+N+'.dat')
effectivity = np.loadtxt(root+'/effectivity/effectivity_N'+N+'.dat')
# find the index associated to the anchor point
idx = (np.where(angle == anchor))
dual_norm_scaled = residual/effectivity[idx]

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(angle, dual_norm_scaled, 'k-o', mfc="None")
ax.set_ylabel(r'$\triangle^{scaled}$')
ax.set_xlabel(r'$\theta_g$')
ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
print("---------------------------------------------")
fig.savefig(tpath+'dual_norm_scaled_N'+N+'.png')
print(tpath+'dual_norm_scaled.png saved successfully')
np.savetxt(tpath+'angle.dat', angle)
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'dual_norm_scaled_N'+N+'.dat', dual_norm_scaled)
print(tpath+'dual_norm_scaled.dat saved successfully')
print("---------------------------------------------")
