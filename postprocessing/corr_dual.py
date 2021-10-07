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
target_dir = '/corr_dual'

setup.checkdir(target_dir)

root = os.getcwd()
#solver = checker.rom_checker(root, '.*/(.*)rom_info')

tpath = './corr_dual/'

# compute the effectivity
angle = np.loadtxt(root+'/dual_norm/angle_list.dat')
residual = np.loadtxt(root+'/dual_norm/erri_N'+N+'.dat')
effect = np.loadtxt(root+'/effectivity/effectivity_N'+N+'.dat')
anchor = setup.find_anchor()
idx = np.where(angle == int(anchor))
print(anchor, idx)
corr_dual = residual/effect[idx]
print(corr_dual)

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': r'$N = $'+N}

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\eta$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 5, dtype=int))

ax.plot(angle, corr_dual, **plot_params)
ax.legend(loc=0)
ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

print("---------------------------------------------")
fig.savefig(tpath+'corr_dual_N'+N+'.png')
print(tpath+'corr_dual.png saved successfully')
np.savetxt(tpath+'angle.dat', angle)
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'corr_dual_N'+N+'.dat', corr_dual)
print(tpath+'corr_dual.dat saved successfully')
print("---------------------------------------------")
