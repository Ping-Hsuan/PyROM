import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import re
import os
import subprocess
import operator
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
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
print("---------------------------------------------")
isExist = os.path.exists(os.getcwd()+'/romt/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/romt/')
    print("The target directory exist")
print("---------------------------------------------")

root = os.getcwd()
sp1 = (root.split('/'))
sp2 = (sp1.pop())
sp3 = sp2.split('_')
anchor = float(sp3.pop())

for root, dirs, files in os.walk("./rom/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            pass
#           print(os.path.join(root, name))
    for name in dirs:
        pass
#       print(os.path.join(root, name))

fname = [name for name in files if re.match('^.*_(.*)rom_.*_'+str(int(anchor-90)), name)]

colors = cm.Set1(np.linspace(0, 1, 9))
color_ctr = 0

i = 0
tpath = './romt/'
romt = []
t_grid = []

fname = fname.pop()
match_rom = re.match('^.*_(.*)rom_.*$', fname)
assert match_rom is not None

if match_rom.groups()[0] == '':
    solver = 'Galerkin ROM'
elif match_rom.groups()[0] == 'c':
    solver = 'Constrained ROM'
elif match_rom.groups()[0] == 'l':
    solver = 'Leray ROM'

ft = open(tpath+fname+'_romt', 'w')
with open(root+fname, 'r') as f:
    for line in f:
        if re.search(r'\sromt', line):
            ft.write(line)
            info = line.split()
            romt.append(info[2])
            t_grid.append(info[1])
ft.close()

K_match = re.match(r"(\d\d\d)s_.*", fname)
nb_match = re.match(r"^.*_(\d+)nb_.*", fname)
K = int(K_match.groups()[0])
nb = int(nb_match.groups()[0])
T = int(len(romt)/nb)
romt = np.reshape(np.array(romt).astype(np.float64),
                  (nb, T), order='F')
t_grid = np.reshape(np.array(t_grid).astype(np.float64),
                    (nb, T), order='F')
fomt = np.loadtxt('tk')
fomt = np.reshape(np.array(fomt).astype(np.float64),
                  (int(len(fomt)/K), K), order='F')
tmax = np.loadtxt('tmax')
tmin = np.loadtxt('tmin')
ul_bounds = [tmax, tmin]

if min(4, nb) == 1:
    fig, ax = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    ax.plot(t_grid[i, K:], romt[i, K:], 'b-', mfc="None", label='N = '+str(i))
    ax.plot(t_grid[i, K:], fomt[i+1, :], 'k-', mfc="None")
    ax.set_xlabel(r'$t$')
    ax.legend(loc=0)
    fig.savefig('./romt/romt.png')
else:
    fig, axs = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    for i in range(min(4, nb)):
        axs[i].plot(t_grid[i, K:], romt[i, K:], 'b-', mfc="None", label='N = '+str(i))
        axs[i].plot(t_grid[i, K:], fomt[i+1, :], 'k-', mfc="None")
        axs[i].hlines(y=tmax[i], xmin=t_grid[i, K], xmax=t_grid[i, -1], colors='r')
        axs[i].hlines(y=tmin[i], xmin=t_grid[i, K], xmax=t_grid[i, -1], colors='r')
        axs[i].set_xlabel(r'$t$')
        axs[i].legend(loc=0)
        axs[i].set_ylabel(r'$T_{'+str(i+1)+'}(t)$')
    fig.savefig('./romt/romt.png')

tas = np.loadtxt('tas')
tvs = np.loadtxt('tvs')
ta = np.zeros((nb,))
tv = np.zeros((nb,))

for j in range(nb):
    ta[j] = np.sum(romt[j, K:])/len(romt[0, K:])
    tv[j] = np.sum((romt[j, K:]-ta[j])**2)/(len(romt[0, K:])-1)

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

fig.savefig('./romt/ta_tv.png')
