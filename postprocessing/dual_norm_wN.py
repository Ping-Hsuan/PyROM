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

erri = []
N_list = []
for nb, fnames in dict_final:
    for fname in fnames:
        data = reader.reader(fname)
        dual_norm = np.array(data).astype(np.float64)
        erri.append(float(dual_norm))
        N_list.append(int(nb))

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
data = np.column_stack((N_list, erri))
data = data[data[:, 0].argsort()]

if len(N_list) == 1:
    pass
else:
    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}
    ax.set(ylabel=r'$\triangle(\theta_g='+str(int(deg)+90)+')$', xlabel=r'$N$',
           ylim=[1e-2, 1], xlim=[1, max(data[:, 0])])
    ax.semilogy(data[:, 0], data[:, 1], **plot_params)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'dual_norm_theta_'+str(int(deg)+90)+'.png')
    print("---------------------------------------------")

np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'erri_theta_'+str(int(deg)+90)+'.dat', data[:, 1])
