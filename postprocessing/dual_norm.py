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

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
N = str(sys.argv[2])
print(os.getcwd())
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
    if nb == N:
        print(nb)
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
        ax.semilogy(data[:, 0], data[:, 1], 'k-o',
                    mfc="None", label=r'$N = $'+str(nb)+', '+r'$\theta^*_g = '+str(int(anchor))+'$')

        ax.set_ylabel(r'$\triangle(\theta_g)$')
        ax.set_xlabel(r'$\theta_g$')
        ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
        ax.set_ylim([1e-2, 1])
        ax.legend(loc=0, ncol=2)
        print(os.getcwd())
        fig.savefig(tpath+'online_N'+str(nb)+'.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'erri_N'+str(nb)+'.dat', data[:, 1])
        plt.close(fig)

