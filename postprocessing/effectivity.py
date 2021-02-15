import numpy as np
import matplotlib.pyplot as plt
import re
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader

setup.style(1)
colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
N = str(sys.argv[2])
print("---------------------------------------------")
target_dir = '/effectivity'

setup.checkdir(target_dir)

root = os.getcwd()
match_rom = re.match('^.*/(.*)rom_info$', root)
assert match_rom is not None

if match_rom.groups()[0] == '':
    solver = 'Galerkin ROM'
elif match_rom.groups()[0] == 'c':
    solver = 'Constrained ROM'
elif match_rom.groups()[0] == 'l':
    solver = 'Leray ROM'

tpath = './effectivity/'

# compute the effectivity
angle = np.loadtxt(root+'/dual_norm/angle.dat')
residual = np.loadtxt(root+'/dual_norm/erri_N'+N+'.dat')
rom_abserr = np.loadtxt(root+'/rom_abserr/rom_abserr_N'+N+'.dat')
effectivity = residual/rom_abserr

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N = $'+N}

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\eta$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 5, dtype=int))

ax.semilogy(angle, effectivity, **plot_params)
ax.legend(loc=0)

print("---------------------------------------------")
fig.savefig(tpath+'effectivity_N'+N+'.png')
print(tpath+'effectivity.png saved successfully')
np.savetxt(tpath+'angle.dat', angle)
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'effectivity_N'+N+'.dat', effectivity)
print(tpath+'effectivity.dat saved successfully')
print("---------------------------------------------")
