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
import setup
import reader

setup.style(1)
colors = setup.color(0)
setup.text()

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
deg = str(int(sys.argv[2]))
target_dir = '/nu'

setup.checkdir(target_dir)
root, filenames = setup.gtfpath(target_dir, '^.*_(.*)rom_.*_ic.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')

dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))
print(dict_final)

anchor = setup.find_anchor()

color_ctr = 0
tpath = root+'/'

merr_list = []
verr_list = []
sderr_list = []
N_list = []
m_list = []
sd_list = []
for nb, fnames in dict_final:
    for fname in fnames:

        match_rom = re.match('^.*_(.*)rom_.*$', fname)
        forleg = fname.split('_')

        assert match_rom is not None

        if match_rom.groups()[0] == '':
            solver = 'Galerkin ROM'
        elif match_rom.groups()[0] == 'c':
            solver = 'Constrained ROM'
        elif match_rom.groups()[0] == 'l':
            solver = 'Leray ROM'

        # get the FOM data
        filename = '../../../../fom_nuss/nuss_fom_'+deg
        data = mypostpro.read_nuss(filename)
        data[:, 2] = data[:, 2]/40
        idx1 = mypostpro.find_nearest(data[:, 0], 0)
        idx2 = mypostpro.find_nearest(data[:, 0], 1000)
        nuss_fom = data[idx1:idx2, :]
        avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
        fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
        fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
        fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
        print('FOM data at deg '+deg, fom_mean, fom_var, fom_sd)


        nuss = mypostpro.read_nuss(fname)
        nuss[:, 2] = nuss[:, 2]/40
        avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(sys.argv[3]))
        rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
        rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
        rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
        [mean_err, var_err, sd_err] = mypostpro.cnuss_err(fom_mean, fom_var, fom_sd, rom_mean, rom_var, rom_sd)

        merr_list.append(mean_err)
        verr_list.append(var_err)
        sderr_list.append(sd_err)
        N_list.append(int(nb))
        m_list.append(rom_mean)
        sd_list.append(rom_sd)

data = np.column_stack((N_list, merr_list, sderr_list, m_list, sd_list))
data = data[data[:, 0].argsort()]

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(data[:, 0], data[:, 1], 'k-o', mfc="None", label=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.set_ylim([1e-4, 1])
ax.set_xlim([1, max(data[:, 0])])
ax.set_xlabel(r'$\theta_g$')
ax.set_ylabel(r'$|\langle \text{Nu} \rangle_s - \langle \widehat{\text{Nu}} \rangle_s|/|\langle \text{Nu} \rangle_s|$')
ax.axes.grid(True, axis='y')
ax.legend(loc=1)
fig.savefig('./nu/relmnu_theta_'+deg+'.png')
plt.close(fig)

fig, ax = plt.subplots(1, tight_layout=True)
tmp = data[:, 4].reshape((len(N_list), ))
print(tmp.shape)
#ax.errorbar(data[:, 0], data[:, 3], yerr=tmp)
ax.plot(data[:, 0], data[:, 3], 'b-o', mfc="None", label=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.hlines(y=fom_mean, xmin=0, xmax=max(data[:, 0]), colors='k', label='FOM')
ax.set_xlim([1, max(data[:, 0])])
ax.set_ylim([1, 4])
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'Mean Nu')
ax.axes.grid(True, axis='y')
ax.legend(loc=1)
fig.savefig('./nu/mnu_theta_'+deg+'.png')

fig, ax = plt.subplots(1, tight_layout=True)
ax.plot(data[:, 0], data[:, 4], 'b-o', mfc="None", label=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.hlines(y=fom_sd, xmin=0, xmax=max(data[:, 0]), colors='k', label='FOM')
ax.set_ylim([0, 0.3])
ax.set_xlim([1, max(data[:, 0])])
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'std(Nu)')
ax.axes.grid(True, axis='y')
ax.legend(loc=1)
fig.savefig('./nu/stdnu_theta_'+deg+'.png')

np.savetxt('./nu/N_list_'+deg+'.dat', data[:, 0])
np.savetxt('./nu/merr_theta_'+deg+'.dat', data[:, 1])
np.savetxt('./nu/sderr_theta_'+deg+'.dat', data[:, 2])
np.savetxt('./nu/m_theta_'+deg+'.dat', data[:, 3])
np.savetxt('./nu/sd_theta_'+deg+'.dat', data[:, 4])

