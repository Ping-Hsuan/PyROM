import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import re
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro

#plt.style.use('report')

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
print("---------------------------------------------")
N = str((sys.argv[2]))
isExist = os.path.exists(os.getcwd()+'/romt/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/romt/')
    print("The target directory exist")
print("---------------------------------------------")
ops_path = '../ops/'

root = os.getcwd()
sp1 = (root.split('/'))
for element in sp1:
    z = re.match(r"theta_(\d+)", element)
    if z:
        anchor = float(((z.groups())[0]))

for root, dirs, files in os.walk("./romt/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            pass
#           print(os.path.join(root, name))
    for name in dirs:
        pass
#       print(os.path.join(root, name))

filenames = [name for name in files if re.match('^.*_(.*)rom_.*_'+str(int(anchor-90)), name)]

colors = cm.Set1(np.linspace(0, 1, 9))
color_ctr = 0

i = 0
tpath = './romt/'
romt = []
t_grid = []

for element in filenames:
    z = re.match(r"^.*_(\d+)nb_.*", element)
    if z.groups()[0] == N:
        fname = element
match_rom = re.match('^.*_(.*)rom_.*$', fname)
assert match_rom is not None

if match_rom.groups()[0] == '':
    solver = 'Galerkin ROM'
elif match_rom.groups()[0] == 'c':
    solver = 'Constrained ROM'
elif match_rom.groups()[0] == 'l':
    solver = 'Leray ROM'

with open(tpath+fname, 'r') as f:
    for line in f:
        info = line.split()
        romt.append(info[2])
        t_grid.append(info[1])

K_match = re.match(r"(\d\d\d)s_.*", fname)
nb_match = re.match(r"^.*_(\d+)nb_.*", fname)
K = int(K_match.groups()[0])
nb = int(nb_match.groups()[0])
T = int(len(romt)/nb)
sp1 = fname.split('_')
for element in sp1:
    if re.match(r"zero", element):
        T0 = K
    elif re.match(r"ic", element):
        T0 = 0
        t_grid = np.reshape(np.array(t_grid).astype(np.float64),
                            (nb, T), order='F')
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

if min(4, nb) == 1:
    fig, ax = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    ax.plot(t_grid[i, T0:], romt[i, T0:], 'b-', mfc="None", label='ROM')
    ax.plot(t_grid[i, T0:], fomt[i+1, :], 'k-', mfc="None", label='Snapshot')
    ax.hlines(y=tmax[i], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='r')
    ax.hlines(y=tmin[i], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='r')
    ax.hlines(y=tas[i+1], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='k', linestyle='--', label='Snapshot avg')
    ax.annotate('Snap std:'+"%.2e"% tvs[i+1], xy=(0, 0.2), xytext=(12, -12), va='top',
             xycoords='axes fraction', textcoords='offset points')
    ax.annotate('ROM std:'+"%.2e"% tv[i], xy=(0, 0.25), xytext=(12, -12), va='top',
             xycoords='axes fraction', textcoords='offset points')
    ax.set_xlabel(r'$t$')
    ax.legend(loc=0)
    ax.set_ylabel(r'$T_{'+str(i+1)+'}(t)$')
    fig.savefig('./romt/romt_N'+N+'.png')
else:
    fig, axs = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    for i in range(min(4, nb)):
        axs[i].plot(t_grid[i, T0:], romt[i, T0:], 'b-', mfc="None", label='ROM')
        axs[i].plot(t_grid[i, T0:], fomt[i+1, :], 'k-', mfc="None", label='Snapshot')
        axs[i].hlines(y=tmax[i], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='r')
        axs[i].hlines(y=tmin[i], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='r')
        axs[i].hlines(y=tas[i+1], xmin=t_grid[i, 0], xmax=t_grid[i, -1], colors='k', linestyle='--', label='Snapshot avg')
        axs[i].annotate('Snap std:'+"%.2e"% tvs[i+1], xy=(0, 0.2), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
        axs[i].annotate('ROM std:'+"%.2e"% tv[i], xy=(0, 0.25), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
        axs[i].set_xlabel(r'$t$')
        axs[i].legend(loc=0)
        axs[i].set_ylabel(r'$T_{'+str(i+1)+'}(t)$')
    fig.savefig('./romt/romt_N'+N+'.png')



fig, axs = plt.subplots(2, sharex=True, tight_layout=True)

POD_modes = [np.linspace(1, nb, nb, dtype=int), np.linspace(1, nb, nb, dtype=int)]
data = [ta, tv]
refs = [tas, tvs]
ylabels = [r'$\langle T_{n} \rangle_s$', r'$V_s(T_n)$']
for i in range(2):
    axs[i].plot(POD_modes[i], data[i], 'b-o', label='ROM')
    axs[i].plot(POD_modes[i], refs[i][1:nb+1], 'k-o', label='FOM')
    axs[i].legend(loc=0)
    axs[i].set_ylabel(ylabels[i])
    axs[i].set_xlabel(r'$n$')
    axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))
    if i == 1:
        axs[i].set_yscale('log')

fig.savefig('./romt/ta_tv_N'+N+'.png')
