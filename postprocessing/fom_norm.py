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
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
print("---------------------------------------------")

isExist = os.path.exists(os.getcwd()+'/fom_norm/')
if isExist:
    print("The target directory exist")
    pass
else:
    os.mkdir(os.getcwd()+'/fom_norm/')
    print("Create the target directory successfully")
print("---------------------------------------------")

for root, dirs, files in os.walk("./crom/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            pass
#           print(os.path.join(root, name))
    for name in dirs:
        pass
#       print(os.path.join(root, name))
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

i = 0
tpath = './fom_norm/'
fig, ax = plt.subplots(1, tight_layout=True)

for nb, fnames in dict_final:
    angle = []
    data = []
    merr_proj = []
    for fname in fnames:
        forleg = fname.split('_')

        match_rom = re.match('^.*_(.*)rom_.*$', fname)
        assert match_rom is not None

        if match_rom.groups()[0] == '':
            solver = 'Galerkin ROM'
        elif match_rom.groups()[0] == 'c':
            solver = 'Constrained ROM'
        elif match_rom.groups()[0] == 'l':
            solver = 'Leray ROM'

        # write out projection error information
        ft = open(tpath+fname+'_fom_norm', 'w')
        with open(root+fname, 'r') as f:
            for line in f:
                if re.search(r'^\sFOM\sh1\snorm:', line):
                    ft.write(line)
        ft.close()

        with open(tpath+fname+'_fom_norm', 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                         and k != 'norm:'] for line in list_of_lines][:-1]
        data = [x[-1] for x in list_of_words]
        data.pop(0)
        data = np.array(data).astype(np.float64)
        merr_proj.append(data)
        angle.append(int(forleg[-1])+90)
        print(fname)

    data = np.column_stack((angle, merr_proj))
    nb = int(match_nb.groups()[0])
    data = data[data[:, 0].argsort()]
    ax.plot(data[:, 0], data[:, 1], '-o', color=colors[i],
                mfc="None", label=r'$N = $'+str(nb))
    i += 1

ax.set_ylabel(r'$\|u\|_{H^1}$')
ax.set_xlabel(r'$\theta_g$')
ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig(tpath+'fom_norm.png')
print(tpath+'fom_norm.png saved successfully')
np.savetxt(tpath+'angle.dat', data[:, 0])
print(tpath+'angle.dat saved successfully')
np.savetxt(tpath+'fom_norm.dat', data[:, 1])
print(tpath+'fom_norm.dat saved successfully')
print("---------------------------------------------")
