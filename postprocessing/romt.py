import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import re
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
import myplot
import mypostpro

colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
deg = str(int(sys.argv[3])-90)
N = str((sys.argv[4]))
print("---------------------------------------------")

target_dir = '/romt_'+N
setup.checkdir(target_dir)
ops_path = '../ops/'

search_dir = './'+model+'_info/romt'
anchor = setup.find_anchor()
root, filenames = setup.gtfpath(search_dir,
                                '^.*_(.*)rom_.*_'+str(int(anchor-90)))

color_ctr = 0
tpath = root+'/'

romt = []
t_grid = []

for element in filenames:
    z = re.match(r"^.*_(\d+)nb_.*", element)
    if z.groups()[0] == N:
        fname = element

with open(fname, 'r') as f:
    for line in f:
        info = line.split()
        romt.append(info[2])
        t_grid.append(info[1])

K_match = re.match(r"^.*(\d\d\d)s_.*", fname)
nb_match = re.match(r"^.*_(\d+)nb_.*", fname)
K = int(K_match.groups()[0])
nb = int(nb_match.groups()[0])
T = int(len(romt)/nb)

t_grid = np.reshape(np.array(t_grid).astype(np.float64),
                    (nb, T), order='F')
sp1 = fname.split('_')
for element in sp1:
    if re.match(r"zero", element):
        T0 = mypostpro.find_nearest(t_grid[0, :], 501)
    elif re.match(r"ic", element):
        T0 = 0
        t_grid += 500

print(f'Information K: {K}, N: {nb}, T:{T}, T0: {T0}')
romt = np.reshape(np.array(romt).astype(np.float64),
                  (nb, T), order='F')
fomt = np.loadtxt(ops_path+'tk')
fomt = np.reshape(np.array(fomt).astype(np.float64),
                  (int(len(fomt)/K), K), order='F')
tmax = np.loadtxt(ops_path+'tmax')
tmin = np.loadtxt(ops_path+'tmin')
ul_bounds = [tmax, tmin]

tas = np.loadtxt(ops_path+'tas')
tvs = np.loadtxt(ops_path+'tvs')
ta = np.zeros((nb,))
tv = np.zeros((nb,))

for j in range(nb):
    ta[j] = np.sum(romt[j, T0:])/len(romt[0, T0:])
    tv[j] = np.sum((romt[j, T0:]-ta[j])**2)/(len(romt[0, T0:])-1)

i = 0
rom_params = {'c': 'b', 'mfc': 'None', 'label': 'Snapshot'}
snap_params = {'c': 'k', 'mfc': 'None', 'label': 'Snapshot'}
avgsnap_params = {'c': 'k', 'linestyle': '--', 'label': 'Snapshot avg'}
avgrom_params = {'c': 'k', 'linestyle': '--', 'label': 'ROM avg'}

if min(4, nb) == 1:
    fig, ax = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    ax.set(xlabel=r'$t$', ylabel=r'$T_{'+str(i+1)+'}(t)$')

    myplot.rom_coef(ax, t_grid[i, T0:], np.linspace(500, 1000, K),
                    romt[i, T0:], fomt[i+1, :],
                    rom_params, snap_params)
    myplot.rom_minmax(ax, tmax[i], tmin[i],
                      t_grid[i, T0], t_grid[i, -1])
    myplot.coef_avg(ax, ta[i], tas[i+1], t_grid[i, T0], t_grid[i, -1])

    ax.annotate('Snap std:'+"%.2e"% tvs[i+1], xy=(0, 0.2), xytext=(12, -12), va='top',
             xycoords='axes fraction', textcoords='offset points')
    ax.annotate('ROM std:'+"%.2e"% tv[i], xy=(0, 0.27), xytext=(12, -12), va='top',
             xycoords='axes fraction', textcoords='offset points')

    ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
           borderaxespad=0, frameon=False)
else:
    fig, axs = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    for i in range(min(4, nb)):
        axs[i].set(xlabel=r'$t$', ylabel=r'$T_{'+str(i+1)+'}(t)$')

        myplot.rom_coef(axs[i], t_grid[i, T0:], np.linspace(500, 1000, K),
                        romt[i, T0:], fomt[i+1, :],
                        rom_params, snap_params)
        myplot.rom_minmax(axs[i], tmax[i], tmin[i],
                          t_grid[i, T0], t_grid[i, -1])
        myplot.coef_avg(axs[i], ta[i], tas[i+1], t_grid[i, T0], t_grid[i, -1])

        axs[i].annotate('Snap std:'+"%.2e"% tvs[i+1], xy=(0.2, -0.1), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
        axs[i].annotate('ROM std:'+"%.2e"% tv[i], xy=(-0.1, -0.1), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
        if i == 0:
            ax = axs[i]

    ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.51), ncol=4,
           borderaxespad=0, frameon=False)

fig.savefig('./romt_'+N+'/romt_N'+N+'.png')

POD_modes = [np.linspace(1, nb, nb, dtype=int),
             np.linspace(1, nb, nb, dtype=int)]
data = [ta, tv]
refs = [tas, tvs]
ylabels = [r'$\langle T_{n} \rangle_s$', r'$V_s(T_n)$']
params = [{'c': 'b', 'marker': 'o', 'mfc': 'None', 'label': 'ROM'},
          {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'}]

fig, axs = plt.subplots(2, sharex=True, tight_layout=True)
for i in range(2):
    axs[i].plot(POD_modes[i], data[i], **params[0])
    axs[i].plot(POD_modes[i], refs[i][1:nb+1], **params[1])
    axs[i].legend(loc=0)
    axs[i].set_ylabel(ylabels[i])
    axs[i].set_xlabel(r'$n$')
    axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))
    if i == 1:
        axs[i].set_yscale('log')

fig.savefig('./romt_'+N+'/ta_tv_N'+N+'.png')
