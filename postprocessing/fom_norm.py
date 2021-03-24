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
model = str(sys.argv[2])
N = str(sys.argv[3])
T0 = int(sys.argv[4])
print("---------------------------------------------")
target_dir = '/fom_norm/'

setup.checkdir(target_dir)

search_dir = './'+model+'_info/fom_norm/'
root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')

dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

angles = []
data = []
fom_norm = []
for angle, fnames in dict_final:
    for fname in fnames:

        solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

        with open(fname, 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                         and k != 'norm:'] for line in list_of_lines][:-1]
        data = [x[-1] for x in list_of_words]
        data = np.array(data).astype(np.float64)
        data = np.reshape(data, (-1, 2), order='F')
        fom_norm.append(data[:, 0])
        angles.append(int(angle)+90)

data = np.column_stack((angles, fom_norm))
data = data[data[:, 0].argsort()]
plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None'}

# fix the h1 norm
for j in range(data.shape[0]):
    data[j, 3] = np.sqrt(data[j, 1]**2+data[j, 2]**2)
    data[j, 6] = np.sqrt(data[j, 4]**2+data[j, 5]**2)
    data[j, 9] = np.sqrt(data[j, 7]**2+data[j, 8]**2)

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||(u, T)\|_{*}$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 19, dtype=int),
       title='Norm of the velocity and temperature')
ax.plot(data[:, 0], data[:, 7], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 8], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 9], 'k-o', mfc="None", label=r'$H^1$')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+search_dir+'fom_h1norm.png')
np.savetxt('.'+search_dir+'angle.dat', data[:, 0])
np.savetxt('.'+search_dir+'fom_h10norm.dat', data[:, 7])
np.savetxt('.'+search_dir+'fom_l2norm.dat', data[:, 8])
np.savetxt('.'+search_dir+'fom_h1norm.dat', data[:, 9])
print("---------------------------------------------")
plt.close(fig)

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||u\|_{*}$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 19, dtype=int),
       title='Norm of the velocity')
ax.plot(data[:, 0], data[:, 1], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 2], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 3], 'k-o', mfc="None", label=r'$H^1$')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+search_dir+'fom_u_norm.png')
np.savetxt('.'+search_dir+'angle.dat', data[:, 0])
np.savetxt('.'+search_dir+'fom_u_h10norm.dat', data[:, 1])
np.savetxt('.'+search_dir+'fom_u_l2norm.dat', data[:, 2])
np.savetxt('.'+search_dir+'fom_u_h1norm.dat', data[:, 3])
print("---------------------------------------------")

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||T\|_{*}$', xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 19, dtype=int),
       title='Norm of the temperature')
ax.plot(data[:, 0], data[:, 4], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 5], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 6], 'k-o', mfc="None", label=r'$H^1$')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+search_dir+'fom_T_h1norm.png')
np.savetxt('.'+search_dir+'angle.dat', data[:, 0])
np.savetxt('.'+search_dir+'fom_T_h10norm.dat', data[:, 4])
np.savetxt('.'+search_dir+'fom_T_l2norm.dat', data[:, 5])
np.savetxt('.'+search_dir+'fom_T_h1norm.dat', data[:, 6])
print("---------------------------------------------")
