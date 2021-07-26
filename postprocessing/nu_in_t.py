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
N = str(sys.argv[3])
K = int(sys.argv[4])
print("---------------------------------------------")

target_dir = '/nu_'+str(N)
setup.checkdir(target_dir)

search_dir = './'+model+'_info/nu'
anchor = setup.find_anchor()
if (len(sys.argv)) < 6:
    if int(sys.argv[4]) == 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+N+'nb_ic.*_'+str(int(anchor-90))+'_nu$')
    elif int(sys.argv[4]) > 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+N+'nb_zero.*_'+str(int(anchor-90))+'_*nu$')
else:
    if int(sys.argv[4]) == 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+N+'nb_ic.*_'+str(int(anchor-90))+'_.*_nu$')
    elif int(sys.argv[4]) > 1:
        root, filenames = setup.gtfpath(search_dir, '^.*_(.*)rom_'+N+'nb_zero.*_'+str(int(anchor-90))+'_.*_*nu$')

files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0

i = 0
tpath = './nu/'

for nb, fnames in dict_final:
    if nb == N:
        for fname in fnames:

            forleg = fname.split('_')
            if model == 'lrom':
                deg = int(forleg[-3])
                rbf = forleg[-2]
                rbf = str(int(float(rbf.replace('p', '.'))*100))
            else:
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
                solver = 'G-ROM'
            elif match_rom.groups()[0] == 'c':
                solver = 'C-ROM'
            elif match_rom.groups()[0] == 'l':
                solver = 'L-ROM with '+rbf+'% filtering'

            nuss = mypostpro.read_nuss(fname)
            nuss[:, 2] = nuss[:, 2]/40
            avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(K))
            print(avgidx1)
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
            ax.set_ylabel('Nu'+r'$(t,\theta_g=$'+str(deg+90)+r'$)$')
#           print(r'$\text{Nu}(t,\theta_g='+str(deg+90)+'$)')
            ax.set_ylim([0, 4])
            ax.axes.grid(True, axis='y')
#           ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
#                  borderaxespad=0, frameon=False)
            ax.legend(loc=0)
            if model == 'lrom':
                s1 = '.'+target_dir+'/'+'nu_in_time_N'+str(nb)+'_'+str(deg+90)+'_'+rbf+'.png'
            else:
                s1 = '.'+target_dir+'/'+'nu_in_time_N'+str(nb)+'_'+str(deg+90)+'.png'
            fig.savefig(s1)
            plt.close(fig)

