import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import sys
import operator

plt.style.use('report')

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
deg = str(int(sys.argv[2])-90)
print("---------------------------------------------")

isExist = os.path.exists(os.getcwd()+'/dual_norm/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/dual_norm/')

for root, dirs, files in os.walk("./dual_norm/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))

filenames = [name for name in files if re.match('^.*_h10_'+deg+'_.*$', name)]

dic_for_files = {}

for fname in filenames:
    match_nb = re.match('^.*_([0-9]*)nb_.*$', fname)
    if match_nb:
        if int(match_nb.groups()[0]) not in dic_for_files:
            dic_for_files[int(match_nb.groups()[0])] = []
        dic_for_files[int(match_nb.groups()[0])].append(fname)

colors = cm.Set1(np.linspace(0, 1, 9))
color_ctr = 0

dict_final = {k: v for k, v in sorted(dic_for_files.items(), key=operator.itemgetter(0))}

i = 0
tpath = './dual_norm/'

erri = []
N_list = []
data = []
for nb in dict_final:
    fname = (dict_final.get(nb)).pop()

    match_rom = re.match('^.*_(.*)rom_.*$', fname)
    assert match_rom is not None

    if match_rom.groups()[0] == '':
        solver = 'Galerkin ROM'
    elif match_rom.groups()[0] == 'c':
        solver = 'Constrained ROM'
    elif match_rom.groups()[0] == 'l':
        solver = 'Leray ROM'

    with open(tpath+fname, 'r') as f:
          k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k and k != 'dual' and k != 'norm:'] for line in list_of_lines][:-1]
    data = [x[-1] for x in list_of_words]
    dual_norm = np.array(data).astype(np.float64)

    erri.append(float(dual_norm))
    N_list.append(nb)

data = np.column_stack((N_list, erri))
data = data[data[:, 0].argsort()]

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(data[:, 0], data[:, 1], 'k-o',
            mfc="None")
ax.set_ylabel(r'$\triangle(\theta_g='+str(int(deg)+90)+')$')
ax.set_xlabel(r'$N$')
ax.set_xlim([1, max(data[:, 0])])
ax.set_ylim([1e-2, 1])
ax.legend(loc=0, ncol=2)

print("---------------------------------------------")
fig.savefig(tpath+'dual_norm_theta_'+str(int(deg)+90)+'.png')
np.savetxt(tpath+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt(tpath+'erri_theta_'+str(int(deg)+90)+'.dat', data[:, 1])
print("---------------------------------------------")

