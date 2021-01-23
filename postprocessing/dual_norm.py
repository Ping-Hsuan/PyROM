import numpy as np
import numpy.linalg as LA
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import re
import os
import sys
import subprocess
import operator
from operator import itemgetter, attrgetter

plt.style.use('report')

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
isExist = os.path.exists(os.getcwd()+'/dual_norm/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/dual_norm/')
print(os.getcwd())
#os.chdir('./crom/')
#print(os.getcwd())

for root, dirs, files in os.walk("./crom/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))

filenames = [name for name in files if re.match('^.*_(.*)rom_.*$', name)]

dic_for_files = {}

for fname in filenames:
    match_nb = re.match('^.*_([0-9]*)nb_.*$', fname)
    if match_nb:
        if int(match_nb.groups()[0]) not in dic_for_files:
            dic_for_files[int(match_nb.groups()[0])] = []
        dic_for_files[int(match_nb.groups()[0])].append(fname)

colors = cm.Set1(np.linspace(0, 1, 9))
color_ctr = 0


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


dict_final = sorted(dic_for_files.items(), key=operator.itemgetter(0))

i = 0
pattern = re.compile(r'(residual in h1 norm:\s\s+)(\d\.\d+E?-?\d+)')
tpath = './dual_norm/'
fig, ax = plt.subplots(1, tight_layout=True)
for nb, fnames in dict_final:
    erri = []
    angle = []
    data = []
    for fname in fnames:
        forleg = fname.split('_')
        pl = 1

        match_rom = re.match('^.*_(.*)rom_.*$', fname)

        if match_rom.groups()[0] == '':
            solver = 'Galerkin ROM'
        elif match_rom.groups()[0] == 'c':
            solver = 'Constrained ROM'
        elif match_rom.groups()[0] == 'l':
            solver = 'Leray ROM'

        assert match_rom is not None

        with open(root+fname, 'r') as f:
            contents = f.read()
            matches = pattern.finditer(contents)
            for match in matches:
                print(match)
                dual_norm = match.group(2)

        erri.append(float(dual_norm))
        angle.append(int(forleg[-1])+90)

        with open(tpath+fname+'_dn', 'w') as f:
            f.write(dual_norm)

    data = np.column_stack((angle, erri))
    data = data[data[:, 0].argsort()]
    print(data[:, 0])
    print(data[:, 1])
    print(type(data[:, 0]))
    print(type(data[:, 1]))
    ax.semilogy(data[:, 0], data[:, 1], '-o', color=colors[i],
                mfc="None", label=r'$N = $'+str(nb))
    i += 1

ax.set_ylabel(r'$\triangle$')
ax.set_xlabel(r'$\theta_g$')
ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
ax.set_ylim([1e-2, 1])
ax.legend(loc=0, ncol=2)
fig.savefig(tpath+'online.png')
np.savetxt(tpath+'angle.dat', data[:, 0])
np.savetxt(tpath+'erri.dat', data[:, 1])
