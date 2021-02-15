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
target_dir = '/fom_norm'

setup.checkdir(target_dir)

root, filenames = setup.gtfpath(target_dir, '^.*_(.*)rom_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')

dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

for nb, fnames in dict_final:
    angle = []
    data = []
    merr_proj = []
    if nb == N:
        plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None'}
        for fname in fnames:

            solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
            angle.append(checker.angle_checker(fname, solver))

            with open(fname, 'r') as f:
                k = f.read()
            list_of_lines = k.split('\n')
            list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                             and k != 'norm:'] for line in list_of_lines][:-1]
            data = [x[-1] for x in list_of_words]
            data.pop(0)
            data = np.array(data).astype(np.float64)
            merr_proj.append(data)

        data = np.column_stack((angle, merr_proj))
        data = data[data[:, 0].argsort()]

        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(ylabel=r'$\||u\|_{H^1}$', xlabel=r'$\theta_g$',
               xticks=np.linspace(0, 180, 5, dtype=int))

        ax.plot(data[:, 0], data[:, 1], 'k-o', mfc="None")

        ax.legend(loc=0)

        print("---------------------------------------------")
        fig.savefig(tpath+'fom_norm.png')
        print(tpath+'fom_norm.png saved successfully')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        print(tpath+'angle.dat saved successfully')
        np.savetxt(tpath+'fom_norm.dat', data[:, 1])
        print(tpath+'fom_norm.dat saved successfully')
        print("---------------------------------------------")
