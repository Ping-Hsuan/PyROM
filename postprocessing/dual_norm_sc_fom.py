import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker

setup.style(1)
colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
N = str(sys.argv[2])
print("---------------------------------------------")
target_dir = '/dual_norm_sc_fom'

setup.checkdir(target_dir)

anchor = setup.find_anchor()
root = os.getcwd()
#'^.*_(.*)rom_.*$'
solver = checker.rom_checker(root, '.*/(.*)rom_info')

tpath = './dual_norm_sc_fom/'

# compute the dual_norm_scaled
angle = np.loadtxt(root+'/dual_norm/angle.dat')
residual = np.loadtxt(root+'/dual_norm/erri_N'+N+'.dat')
fom_norm = np.loadtxt(root+'/fom_norm/fom_norm.dat')
print(fom_norm)
# find the index associated to the anchor point
idx = (np.where(angle == anchor))
print(idx)
print(angle[idx])
dual_norm_scaled = residual/fom_norm[idx]

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N = $'+N}

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\triangle^{scaled}$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 5, dtype=int))

ax.semilogy(angle, dual_norm_scaled, **plot_params)
ax.legend(loc=0)

print("---------------------------------------------")
fig.savefig(tpath+'dual_norm_scaled_N'+N+'.png')
print(tpath+'dual_norm_scaled.png saved successfully')
np.savetxt(tpath+'angle.dat', angle)
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'erri_N'+N+'.dat', dual_norm_scaled)
print(tpath+'dual_norm_scaled.dat saved successfully')
print("---------------------------------------------")
