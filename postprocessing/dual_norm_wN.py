import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
from mor import ROM
from snapshot import Snapshot
from aux import sort

setup.style(1)
colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
deg = str(int(sys.argv[3])-90)
print("---------------------------------------------")

target_dir = '/dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/dual_norm'
root, filenames = setup.gtfpath(search_dir, '^.*_h10_'+deg+'_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

roms = []
for nb, fnames in dict_final:
    for fname in fnames:
        rom = ROM(fname)
        rom.DTAR()
        rom.anchor('theta')
        roms.append(rom)
data = sort(roms, 'nb', 'dtar')
solver = rom.info['method']
anchor = str(int(rom.info['anchor']))

if len(data[:, 0]) == 1:
    pass
else:
    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$\theta^*_g = '+anchor+'$'}
    ax.set(ylabel=r'$\triangle(\theta_g='+str(int(deg)+90)+')$', xlabel=r'$N$',
            ylim=[10**np.floor(np.log10(min(data[:, 1]))), 1], xlim=[1, max(data[:, 0])])
    ax.semilogy(data[:, 0], data[:, 1], **plot_params)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'dual_norm_theta_'+str(int(deg)+90)+'.png')
    print("---------------------------------------------")
plt.show()
np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'erri_theta_'+str(int(deg)+90)+'.dat', data[:, 1])
