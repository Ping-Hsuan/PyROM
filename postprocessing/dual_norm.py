import numpy as np
import matplotlib.pyplot as plt
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

            solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
            angle.append(checker.angle_checker(fname, solver))

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

