import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker

# This script is used to plot ROM absolute error and
# Proejction error with N at a given theta_g

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

target_dir = '/abserr/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/rom_abserr'
root, filenames = setup.gtfpath(search_dir, '^.*_h10_'+deg+'_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

N_list = []
data = []
merr_rom = []
merr_proj = []
for nb, fnames in dict_final:
    for fname in fnames:
        solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
        data = reader.reader(fname)
        data = np.array(data).astype(np.float64)
        merr_rom.append(data[0])
        merr_proj.append(data[1])
        N_list.append(int(nb))

data = np.column_stack((N_list, merr_rom, merr_proj))
data = data[data[:, 0].argsort()]

if len(N_list) == 1:
    pass
else:
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylabel=r'$\|u_{avg} - \widehat{u}_{avg}\|_{H^1}$', xlabel=r'$N$',
           xlim=[0, max(data[:, 0])], title='Absolute error in the ' +
           r'mean flow at $\theta_g='+str(int(deg)+90)+'$')

    plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                    'label': solver}
    plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                    'label': 'Projection'}
    ax.semilogy(data[:, 0], data[:, 1], **plot_params1)
    ax.semilogy(data[:, 0], data[:, 2], **plot_params2)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'abserr_theta_'+str(int(deg)+90)+'.png')
    print("---------------------------------------------")

np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'rom_abserr_theta_'+str(int(deg)+90)+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'proj_abserr_theta_'+str(int(deg)+90)+'.dat', data[:, 2])
