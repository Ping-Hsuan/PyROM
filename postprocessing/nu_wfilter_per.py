import numpy as np
import matplotlib.pyplot as plt
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

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
N = str(sys.argv[3])
T0 = int(sys.argv[4])
angle = int(sys.argv[5])
print("---------------------------------------------")

target_dir = '/nu/'
setup.checkdir(target_dir)
f1 = 1
f2 = 100

search_dir = './'+model+'_info/nu'
root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(\dp\d+)_nu$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(\dp\d+)_nu$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

filename = '../../../../fom_nuss/nuss_fom_'+str(int(angle))
data = mypostpro.read_nuss(filename)
data[:, 2] = data[:, 2]/40
idx1 = mypostpro.find_nearest(data[:, 0], 0)
idx2 = mypostpro.find_nearest(data[:, 0], 1000)
nuss_fom = data[idx1:idx2, :]
avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
print('FOM data at deg '+str(int(angle)), ', Mean nu ', fom_mean, 'Std(Nu): ', fom_sd)

merr_list = []
verr_list = []
sderr_list = []
fws = []
m_list = []
sd_list = []

for fw, fnames in dict_final:
    # get the FOM data
    for fname in fnames:

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
    fw = (float(fw.replace('p', '.'))*100)
    fws.append(float(fw))
    m_list.append(rom_mean)
    sd_list.append(rom_sd)

data = np.column_stack((fws, merr_list, sderr_list, m_list,
                       sd_list))
#                      sd_list, fom_means, fom_stds))
data = data[data[:, 0].argsort()]
print(data)

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

### Below are plotting
plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N='+N+'$'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[0, 1], xticks=np.linspace(1, 100, 21, dtype=int),
       xlabel='\# percentage filtered', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
       r'\langle \widehat{\text{Nu}} \rangle_s|}' +
       r'{|\langle \text{Nu} \rangle_s|}$',
       title='Relative error in the mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' +
       r'$\theta^*_g='+str(int(anchor))+'$')
ax.plot(data[:, 0], data[:, 1], **plot_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'relmnu_N'+N+'.png')

plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N='+N+'$'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[1, 4], xticks=np.linspace(1, 100, 21, dtype=int), xlabel=r'$\delta$', ylabel='Mean Nu',
       title='Mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at '+r'$\theta^*_g='+str(int(anchor))+'$')
ax.hlines(y=fom_mean, xmin=1, xmax=100, colors='k', label='FOM')
ax.plot(data[:, 0], data[:, 3], **plot_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'mnu_N'+N+'.png')

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[0, 0.3], xticks=np.linspace(1, 100, 21, dtype=int), xlabel=r'\# percentage filtered', ylabel='std(Nu)',
title='Std(Nu) at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' + r'$\theta^*_g='+str(int(anchor))+'$')
ax.hlines(y=fom_sd, xmin=1, xmax=100, colors='k', label='FOM')
ax.plot(data[:, 0], data[:, 4], **plot_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'stdnu_N'+N+'.png')

np.savetxt('.'+target_dir+'fws.dat', data[:, 0])
np.savetxt('.'+target_dir+'merr_N'+N+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'stderr_N'+N+'.dat', data[:, 2])
np.savetxt('.'+target_dir+'mnu_N'+N+'.dat', data[:, 3])
np.savetxt('.'+target_dir+'stdnu_N'+N+'.dat', data[:, 4])
