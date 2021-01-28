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
import subprocess
import operator
from operator import itemgetter, attrgetter
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro

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
isExist = os.path.exists(os.getcwd()+'/nu/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/nu/')

for root, dirs, files in os.walk("./nu/", topdown=False):
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


i = 0
tpath = './nu/'

for nb, fnames in dict_final:
    merr_list = []
    verr_list = []
    sderr_list = []
    angle_list = []
    m_list = []
    sd_list = []
    for fname in fnames:

        forleg = fname.split('_')
        deg = int(forleg[-2])

        # get the FOM data
        filename = '../../../fom_nuss/nuss_fom_'+str(deg+90)
        data = mypostpro.read_nuss(filename)
        data[:, 2] = data[:, 2]/40
        idx1 = mypostpro.find_nearest(data[:, 0], 0)
        idx2 = mypostpro.find_nearest(data[:, 0], 1000)
        nuss_fom = data[idx1:idx2, :]
        avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
        fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
        fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
        fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
        print('FOM data at deg '+str(deg), fom_mean, fom_var, fom_sd)

        match_rom = re.match('^.*_(.*)rom_.*$', fname)

        assert match_rom is not None

        if match_rom.groups()[0] == '':
            solver = 'Galerkin ROM'
        elif match_rom.groups()[0] == 'c':
            solver = 'Constrained ROM'
        elif match_rom.groups()[0] == 'l':
            solver = 'Leray ROM'

        nuss = mypostpro.read_nuss(tpath+fname)
        nuss[:, 2] = nuss[:, 2]/40
        avgidx1 = mypostpro.find_nearest(nuss[:, 1], 501)
        rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
        rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
        rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
        [mean_err, var_err, sd_err] = mypostpro.cnuss_err(fom_mean, fom_var, fom_sd, rom_mean, rom_var, rom_sd)

        merr_list.append(mean_err)
        verr_list.append(var_err)
        sderr_list.append(sd_err)
        angle_list.append((deg+90))
        m_list.append(rom_mean)
        sd_list.append(rom_sd)

    data = np.column_stack((angle_list, merr_list, sderr_list, m_list, sd_list))
    data = data[data[:, 0].argsort()]
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.semilogy(data[:, 0], data[:, 1], 'k-o', mfc="None", label='Nu relative mean error')
    ax.set_ylim([1e-3, 10])
    ax.set_xticks(np.linspace(0, 180, 5, dtype=int))
    ax.set_xlabel(r'$\theta_g$')
    ax.axes.grid(True, axis='y')
    ax.legend(loc=0)

    np.savetxt('./nu/angle.dat', data[:, 0])
    np.savetxt('./nu/merr_N'+str(nb)+'.dat', data[:, 1])
    np.savetxt('./nu/sderr_N'+str(nb)+'.dat', data[:, 2])
    np.savetxt('./nu/m_N'+str(nb)+'.dat', data[:, 3])
    np.savetxt('./nu/sd_N'+str(nb)+'.dat', data[:, 4])
    fig.savefig('./nu/relmnu_N'+str(nb)+'.png')

