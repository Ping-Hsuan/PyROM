import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
import aux

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
    rom_norm = []
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': r'$N = $'+str(nb)+', ' +
                   r'$\theta^*_g = '+str(int(anchor))+'$'}
    if nb == N:
        for fname in fnames:

            solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
            angle.append(checker.angle_checker(fname, solver))

            with open(fname, 'r') as f:
                k = f.read()
            list_of_lines = k.split('\n')
            list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                             and k != 'norm:'] for line in list_of_lines][:-1]
            data = [x[-1] for x in list_of_words]
            data = np.array(data).astype(np.float64)
            rom_norm.append(data)

        data = np.column_stack((angle, rom_norm))
        data = data[data[:, 0].argsort()]

        # fix the h1 norm
        for j in range(data.shape[0]):
            data[j, 3] = np.sqrt(data[j, 1]**2+data[j, 2]**2)
            data[j, 6] = np.sqrt(data[j, 4]**2+data[j, 5]**2)
            data[j, 9] = np.sqrt(data[j, 7]**2+data[j, 8]**2)

        fig, ax = plt.subplots(1, tight_layout=True)
        aux.plot_rom_norm(data[:, 0], data[:, 7], data[:, 8], data[:, 9], ax, 'uT')
        fig.savefig(tpath+'rom_norm.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'rom_h10norm_N'+N+'.dat', data[:, 7])
        np.savetxt(tpath+'rom_l2norm_N'+N+'.dat', data[:, 8])
        np.savetxt(tpath+'rom_h1norm_N'+N+'.dat', data[:, 9])
        print("---------------------------------------------")

        fig, ax = plt.subplots(1, tight_layout=True)
        aux.plot_rom_norm(data[:, 0], data[:, 1], data[:, 2], data[:, 3], ax, 'u')
        fig.savefig(tpath+'rom_u_norm.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'rom_u_h10norm_N'+N+'.dat', data[:, 1])
        np.savetxt(tpath+'rom_u_l2norm_N'+N+'.dat', data[:, 2])
        np.savetxt(tpath+'rom_u_h1norm_N'+N+'.dat', data[:, 3])
        print("---------------------------------------------")

        fig, ax = plt.subplots(1, tight_layout=True)
        aux.plot_rom_norm(data[:, 0], data[:, 4], data[:, 5], data[:, 6], ax, 'T')
        fig.savefig(tpath+'rom_T_norm.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'rom_T_h10norm_N'+N+'.dat', data[:, 4])
        np.savetxt(tpath+'rom_T_l2norm_N'+N+'.dat', data[:, 5])
        np.savetxt(tpath+'rom_T_h1norm_N'+N+'.dat', data[:, 6])
        print("---------------------------------------------")


