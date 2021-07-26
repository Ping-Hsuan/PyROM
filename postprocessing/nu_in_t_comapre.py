import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import operator
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro
import setup

colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
K = int(sys.argv[3])
print("---------------------------------------------")

N_list = [33, 47, 87]
target_dir = '/nu_compare'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/nu'
anchor = setup.find_anchor()
fs = []
for N in N_list:
    if int(sys.argv[3]) == 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+str(N)+'nb_ic.*_'+str(int(anchor-90))+'_nu$')
    elif int(sys.argv[3]) > 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+str(N)+'nb_zero.*_'+str(int(anchor-90))+'_*nu$')
    fs.append(filenames.pop())

files_dict = setup.create_dict(fs, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0

i = 0
tpath = './nu/'

fig, ax = plt.subplots(1, tight_layout=True)
# get the FOM data
filename = '../../../../fom_nuss/nuss_fom_'+str(int(anchor))
data = mypostpro.read_nuss(filename)
data[:, 2] = data[:, 2]/40
idx1 = mypostpro.find_nearest(data[:, 0], 0)
idx2 = mypostpro.find_nearest(data[:, 0], 1000)
avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
nuss_fom = data[avgidx1:idx2, :]
fom_mean = mypostpro.cmean(nuss_fom[:idx2], 2)
fom_var = mypostpro.cvar(nuss_fom[:idx2], fom_mean, 2)
fom_sd = mypostpro.csd(nuss_fom[:idx2], fom_mean, 2)
print('FOM data at deg '+str(int(anchor-90)), fom_mean, fom_var, fom_sd)
ax.plot(nuss_fom[:, 0], nuss_fom[:, 2], 'k-', mfc="None", label=r'FOM')

for nb, fnames in dict_final:
    for fname in fnames:

        forleg = fname.split('_')
        deg = int(forleg[-2])

        match_rom = re.match('^.*_(.*)rom_.*$', fname)

        assert match_rom is not None

        if match_rom.groups()[0] == '':
            solver = 'Galerkin ROM'
        elif match_rom.groups()[0] == 'c':
            solver = 'Constrained ROM'
        elif match_rom.groups()[0] == 'l':
            solver = 'Leray ROM'

        nuss = mypostpro.read_nuss(fname)
        nuss[:, 2] = nuss[:, 2]/40
        avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(K))
        rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
        rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
        rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
        if K == 1:
            nuss[:, 1] += 500
        else:
            pass

        ax.plot(nuss[:, 1], nuss[:, 2], '-', color=colors[color_ctr], mfc="None", label=solver+' with '+r'$N = $'+str(nb)+' anchor at '+r'$ \theta^*_g='+str(int(anchor))+'$')
        print('FOM mean(Nu):'+"%.2e"% fom_mean,'ROM mean(Nu):'+"%.2e"% rom_mean)
        print('FOM std(Nu):'+"%.2e"% fom_sd,'ROM std(Nu):'+"%.2e"% rom_sd)
#       ax.annotate('FOM std(Nu):'+"%.2e"% fom_sd, xy=(0, 0.2), xytext=(12, -12), va='top',
#                   xycoords='axes fraction', textcoords='offset points')
#       ax.annotate('ROM std(Nu):'+"%.2e"% rom_sd, xy=(0, 0.27), xytext=(12, -12), va='top',
#           xycoords='axes fraction', textcoords='offset points')
#       ax.annotate('FOM mean(Nu):'+"%.2e"% fom_mean, xy=(0.3, 0.2), xytext=(12, -12), va='top',
#                   xycoords='axes fraction', textcoords='offset points')
#       ax.annotate('ROM mean(Nu):'+"%.2e"% rom_mean, xy=(0.3, 0.27), xytext=(12, -12), va='top',
#           xycoords='axes fraction', textcoords='offset points')
        ax.set_xlabel(r'$t$')
        ax.set_ylabel('Nu'+r'$(t,\theta_g=$'+str(deg+90)+r'$)$')
        ax.set_ylim([0, 4])
        ax.axes.grid(True, axis='y')
        ax.legend(loc=0)
    color_ctr += 1
fig.savefig('.'+target_dir+'/'+'nu_in_time_compare'+'_'+str(deg+90)+'.png')
plt.close(fig)

