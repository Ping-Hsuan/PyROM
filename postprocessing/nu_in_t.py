import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import operator
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro

plt.style.use('report_1fig')

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
K = int(sys.argv[3])
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

root = os.getcwd()
sp1 = (root.split('/'))
T0 = sys.argv[3]
for element in sp1:
    z = re.match(r"theta_(\d+)", element)
    if z:
        anchor = float(((z.groups())[0]))

i = 0
tpath = './nu/'

for nb, fnames in dict_final:
    if nb == N:
        for fname in fnames:

            forleg = fname.split('_')
            deg = int(forleg[-2])

            # get the FOM data
            filename = '../../../../fom_nuss/nuss_fom_'+str(deg+90)
            data = mypostpro.read_nuss(filename)
            data[:, 2] = data[:, 2]/40
            idx1 = mypostpro.find_nearest(data[:, 0], 0)
            idx2 = mypostpro.find_nearest(data[:, 0], 1000)
            avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
            nuss_fom = data[avgidx1:idx2, :]
            fom_mean = mypostpro.cmean(nuss_fom[:idx2], 2)
            fom_var = mypostpro.cvar(nuss_fom[:idx2], fom_mean, 2)
            fom_sd = mypostpro.csd(nuss_fom[:idx2], fom_mean, 2)
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
            avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(K))
            rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
            rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
            rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
            if K == 1:
                nuss[:, 1] += 500
            else:
                pass

            fig, ax = plt.subplots(1, tight_layout=True)
            ax.plot(nuss[:, 1], nuss[:, 2], 'b-', mfc="None", label=solver+' with '+r'$N = $'+str(nb)+' anchor at '+r'$ \theta^*_g='+str(int(anchor))+'$')
#           ax.hlines(y=rom_mean, xmin=nuss[0, 1], xmax=nuss[-1, 1], colors='b', linestyle='--', label='ROM mean Nu')
            ax.plot(nuss_fom[:, 0], nuss_fom[:, 2], 'k-', mfc="None", label=r'FOM') 
#           ax.hlines(y=fom_mean, xmin=nuss[0, 1], xmax=nuss[-1, 1], colors='k', linestyle='--', label='FOM mean Nu')
            ax.annotate('FOM std(Nu):'+"%.2e"% fom_sd, xy=(0, 0.2), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
            ax.annotate('ROM std(Nu):'+"%.2e"% rom_sd, xy=(0, 0.27), xytext=(12, -12), va='top',
                xycoords='axes fraction', textcoords='offset points')
            ax.annotate('FOM mean(Nu):'+"%.2e"% fom_mean, xy=(0.3, 0.2), xytext=(12, -12), va='top',
                        xycoords='axes fraction', textcoords='offset points')
            ax.annotate('ROM mean(Nu):'+"%.2e"% rom_mean, xy=(0.3, 0.27), xytext=(12, -12), va='top',
                xycoords='axes fraction', textcoords='offset points')
            ax.set_xlabel(r'$t$')
            ax.set_ylabel(r'$\text{Nu}(t,\theta_g='+str(deg+90)+')$')
            print(r'$\text{Nu}(t,\theta_g='+str(deg+90)+'$)')
            ax.set_ylim([0, 4])
            ax.axes.grid(True, axis='y')
#           ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
#                  borderaxespad=0, frameon=False)
            ax.legend(loc=0)

            fig.savefig('./nu/nu_in_time_N'+str(nb)+'_'+str(deg+90)+'.png')
            plt.close(fig)

