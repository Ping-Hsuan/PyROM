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
isExist = os.path.exists(os.getcwd()+'/romu/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/romu/')
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
tpath = './romu/'
romu = []
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

ft = open(tpath+fname+'_romu', 'w')
with open(root+fname, 'r') as f:
    for line in f:
        if re.search(r'\sromu', line):
            ft.write(line)
            info = line.split()
            romu.append(info[2])
            t_grid.append(info[1])
ft.close()

K_match = re.match(r"(\d\d\d)s_.*", fname)
nb_match = re.match(r"^.*_(\d+)nb_.*", fname)
K = int(K_match.groups()[0])
nb = int(nb_match.groups()[0])
T = int(len(romu)/nb)
romu = np.reshape(np.array(romu).astype(np.float64),
                  (nb, T), order='F')
t_grid = np.reshape(np.array(t_grid).astype(np.float64),
                    (nb, T), order='F')
fomu = np.loadtxt('uk')
fomu = np.reshape(np.array(fomu).astype(np.float64),
                  (int(len(fomu)/K), K), order='F')

if min(4, nb) == 1:
    fig, ax = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    ax.plot(t_grid[i, K:], romu[i, K:], 'b-', mfc="None", label='N = '+str(i))
    ax.plot(t_grid[i, K:], fomu[i+1, :], 'k-', mfc="None")
    ax.set_xlabel(r'$t$')
    ax.legend(loc=0)
    fig.savefig('./romu/romu.png')
else:
    fig, axs = plt.subplots(min(4, nb), sharex=True, squeeze=True, tight_layout=True)
    for i in range(min(4, nb)):
        axs[i].plot(t_grid[i, K:], romu[i, K:], 'b-', mfc="None", label='N = '+str(i))
        axs[i].plot(t_grid[i, K:], fomu[i+1, :], 'k-', mfc="None")
        axs[i].set_xlabel(r'$t$')
        axs[i].legend(loc=0)
    fig.savefig('./romu/romu.png')

uas = np.loadtxt('uas')
uvs = np.loadtxt('uvs')
ua = np.zeros((nb,))
uv = np.zeros((nb,))

for j in range(nb):
    ua[j] = np.sum(romu[j, K:])/len(romu[0, K:])
    uv[j] = np.sum((romu[j, K:]-ua[j])**2)/(len(romu[0, K:])-1)

fig, axs = plt.subplots(2, sharex=True, tight_layout=True)

POD_modes = [np.linspace(1, nb, nb, dtype=int), np.linspace(1, nb, nb, dtype=int)]
data = [ua, uv]
refs = [uas, uvs]
ylabels = [r'$\langle u_{n} \rangle_s$', r'$V_s(u_n)$']
for i in range(2):
    axs[i].plot(POD_modes[i], data[i], 'b-o', label='ROM')
    axs[i].plot(POD_modes[i], refs[i][1:nb+1], 'k-o', label='FOM')
    axs[i].legend(loc=0)
    axs[i].set_ylabel(ylabels[i])
    axs[i].set_xlabel(r'$n$')
    axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))
    if i == 1:
        axs[i].set_yscale('log')

fig.savefig('./romu/ua_uv.png')
