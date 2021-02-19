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
import checker

setup.style(1)
colors = setup.color(0)
setup.text()

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
deg = str(int(sys.argv[3]))
theta_g = str(int(sys.argv[3])-90)

target_dir = '/nu'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/nu'
if int(sys.argv[4]) == 1:
    root, filenames = setup.gtfpath(search_dir,
                                    '^.*_(.*)rom_.*_ic.*_.*_'+theta_g+'_nu$')
elif int(sys.argv[4]) > 1:
    root, filenames = setup.gtfpath(search_dir,
                                    '^.*_(.*)rom_.*_zero.*_.*_'+theta_g+'_nu$')

files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

anchor = setup.find_anchor()

color_ctr = 0
tpath = root+'/'

merr_list = []
verr_list = []
sderr_list = []
N_list = []
m_list = []
sd_list = []

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

for nb, fnames in dict_final:
    for fname in fnames:

        solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
        nuss = mypostpro.read_nuss(fname)
        nuss[:, 2] = nuss[:, 2]/40
        avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(sys.argv[3]))
        rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
        rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
        rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
        [mean_err, var_err, sd_err] = mypostpro.cnuss_err(fom_mean, fom_var,
                                                          fom_sd, rom_mean,
                                                          rom_var, rom_sd)
    merr_list.append(mean_err)
    verr_list.append(var_err)
    sderr_list.append(sd_err)
    N_list.append(int(nb))
    m_list.append(rom_mean)
    sd_list.append(rom_sd)

data = np.column_stack((N_list, merr_list, sderr_list, m_list, sd_list))
data = data[data[:, 0].argsort()]

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[1e-4, 1], xlim=[1, max(data[:, 0])],
       xlabel=r'$N$', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
       r'\langle \widehat{\text{Nu}} \rangle_s|}' +
       r'{|\langle \text{Nu} \rangle_s|}$')

ax.semilogy(data[:, 0], data[:, 1], **plot_params)
ax.legend(loc=1)

fig.savefig('./nu/relmnu_theta_'+deg+'.png')
plt.close(fig)

plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[1, 4], xlim=[1, max(data[:, 0])],
       xlabel=r'$N$', ylabel='Mean Nu')

ax.plot(data[:, 0], data[:, 3], **plot_params)
ax.hlines(y=fom_mean, xmin=0, xmax=max(data[:, 0]), colors='k', label='FOM')
ax.legend(loc=1)

fig.savefig('./nu/mnu_theta_'+deg+'.png')

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[0, 0.3], xlim=[1, max(data[:, 0])],
       xlabel=r'$N$', ylabel='std(Nu)')

ax.plot(data[:, 0], data[:, 4], **plot_params)
ax.hlines(y=fom_sd, xmin=0, xmax=max(data[:, 0]), colors='k', label='FOM')

ax.legend(loc=1)
fig.savefig('./nu/stdnu_theta_'+deg+'.png')

np.savetxt('./nu/N_list_'+deg+'.dat', data[:, 0])
np.savetxt('./nu/merr_theta_'+deg+'.dat', data[:, 1])
np.savetxt('./nu/sderr_theta_'+deg+'.dat', data[:, 2])
np.savetxt('./nu/m_theta_'+deg+'.dat', data[:, 3])
np.savetxt('./nu/sd_theta_'+deg+'.dat', data[:, 4])

