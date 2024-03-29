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

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
N = int(sys.argv[2])
isExist = os.path.exists(os.getcwd()+'/proj_relerr/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/proj_relerr/')

for root, dirs, files in os.walk("./proj_relerr/", topdown=False):
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

dict_final = sorted(dic_for_files.items(), key=operator.itemgetter(0))

root = os.getcwd()
sp1 = (root.split('/'))
for element in sp1:
    z = re.match(r"theta_(\d+)", element)
    if z:
        anchor = float(((z.groups())[0]))

tpath = './proj_relerr/'

for nb, fnames in dict_final:
    angle = []
    data = []
    merr_proj = []
    if nb == N:
        for fname in fnames:
            forleg = fname.split('_')
            pl = 1

            match_rom = re.match('^.*_(.*)rom_.*$', fname)
            assert match_rom is not None

            if match_rom.groups()[0] == '':
                solver = 'Galerkin ROM'
                angle.append(int(forleg[-3])+90)
            elif match_rom.groups()[0] == 'c':
                solver = 'Constrained ROM'
                angle.append(int(forleg[-3])+90)
            elif match_rom.groups()[0] == 'l':
                solver = 'Leray ROM'
                angle.append(int(forleg[-4])+90)


            with open(tpath+fname, 'r') as f:
                  k = f.read()
            list_of_lines = k.split('\n')
            list_of_words = [[k for k in line.split(' ') if k and k != 'dual' and k != 'norm:'] for line in list_of_lines][:-1]
            data = [x[-1] for x in list_of_words]
            data.pop(0)
            data = np.array(data).astype(np.float64)
            merr_proj.append(data)

        data = np.column_stack((angle, merr_proj))
        data = data[data[:, 0].argsort()]
        fig, ax = plt.subplots(1, tight_layout=True)
        ax.semilogy(data[:, 0], data[:, 1], 'k-o',
                    mfc="None", label=r'$N = $'+str(nb)+', '+r'$\theta^*_g = '+str(int(anchor))+'$')

        ax.set_ylabel(r'$\frac{\|u - \mathcal{P}u\|_{H^1}}{\|u\|_{H^1}}$')
        ax.set_xlabel(r'$\theta_g$')
        ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
        ax.set_ylim([1e-3, 1])
        ax.legend(loc=0, ncol=2)
        fig.savefig(tpath+'proj_relerr_N'+str(nb)+'.png')
        np.savetxt(tpath+'angle.dat', data[:, 0])
        np.savetxt(tpath+'proj_relerr_N'+str(nb)+'.dat', data[:, 1])

