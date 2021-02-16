import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import sys
import operator
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
target_dir = '/rom_norm'

setup.checkdir(target_dir)

root, filenames = setup.gtfpath(target_dir, '^.*_(.*)rom_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')

dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

anchor = setup.find_anchor()

color_ctr = 0
tpath = root+'/'

for nb, fnames in dict_final:
    angle = []
    data = []
    merr_rom = []
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': r'$N = $'+str(nb)+', ' +
                   r'$\theta^*_g = '+str(int(anchor))+'$'}
    if nb == N:
        for fname in fnames:

            solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
            angle = checker.angle_checker(fname, solver)

            with open(fname, 'r') as f:
                k = f.read()
            list_of_lines = k.split('\n')
            list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                             and k != 'norm:'] for line in list_of_lines][:-1]
            data = [x[-1] for x in list_of_words]
            data = np.array(data).astype(np.float64)
            merr_rom.append(data)

        data = np.column_stack((angle, merr_rom))
        data = data[data[:, 0].argsort()]

        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(xlabel=r'$\theta_g$', ylabel=r'$\|u\|_{H^1}$',
               xticks=np.linspace(0, 180, 5, dtype=int),
               ylim=[1e-2, 1])

        ax.plot(data[:, 0], data[:, 1], **plot_params)
        ax.legend(loc=0)

        print("---------------------------------------------")
        fig.savefig(tpath+'rom_norm.png')
        print(tpath+'rom_norm.png saved successfully')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        print(tpath+'angle.dat saved successfully')
        np.savetxt(tpath+'rom_norm_N'+N+'.dat', data[:, 1])
        print(tpath+'rom_norm.dat saved successfully')
        print("---------------------------------------------")
