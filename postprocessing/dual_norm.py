import numpy as np
import matplotlib.pyplot as plt
import re
import os
import sys
import operator
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
target_dir = '/dual_norm'

setup.checkdir(target_dir)

root, filenames = setup.gtfpath(target_dir, '^.*_(.*)rom_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')

dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

anchor = setup.find_anchor()

color_ctr = 0
tpath = root+'/'

for nb, fnames in dict_final:
    erri = []
    angle = []
    data = []
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': r'$N = $'+str(nb)+', ' +
                   r'$\theta^*_g = '+str(int(anchor))+'$'}
    if nb == N:
        for fname in fnames:
            forleg = fname.split('_')
            pl = 1

            match_rom = re.match('^.*_(.*)rom_.*$', fname)
            assert match_rom is not None

            if match_rom.groups()[0] == '':
                solver = 'Galerkin ROM'
                angle.append(int(forleg[-3])+90)
            elif match_rom.groups()[0] == 'c':
                solver = 'Constrained ROM'
                angle.append(int(forleg[-3])+90)
            elif match_rom.groups()[0] == 'l':
                solver = 'Leray ROM'
                angle.append(int(forleg[-4])+90)

            data = reader.reader(fname)
            erri.append(np.array(data).astype(np.float64))

        data = np.column_stack((angle, erri))
        data = data[data[:, 0].argsort()]

        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(xlabel=r'$\theta_g$', ylabel=r'$\triangle(\theta_g)$',
               xticks=np.linspace(0, 180, 5, dtype=int),
               ylim=[1e-2, 1])

        ax.semilogy(data[:, 0], data[:, 1], **plot_params)
        ax.legend(loc=0)

        fig.savefig(tpath+'online_N'+str(nb)+'.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'erri_N'+str(nb)+'.dat', data[:, 1])

        plt.close(fig)

