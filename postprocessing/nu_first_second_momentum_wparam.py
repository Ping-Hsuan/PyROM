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
print("---------------------------------------------")

target_dir = '/nu/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/nu'
root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_(.*\d+)_.*$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_(.*\d+)_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))


color_ctr = 0
tpath = root+'/'

merr_list = []
verr_list = []
sderr_list = []
angles = []
m_list = []
sd_list = []
fom_means = []
fom_stds = []

for angle, fnames in dict_final:
    # get the FOM data
    filename = '../../../../fom_nuss/nuss_fom_'+str(int(angle)+90)
    data = mypostpro.read_nuss(filename)
    data[:, 2] = data[:, 2]/40
    idx1 = mypostpro.find_nearest(data[:, 0], 0)
    idx2 = mypostpro.find_nearest(data[:, 0], 1000)
    nuss_fom = data[idx1:idx2, :]
    avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
    fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
    fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
    fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
    print('FOM data at deg '+str(int(angle)+90), ', Mean nu ', fom_mean, 'Std(Nu): ', fom_sd)
    fom_means.append(fom_mean)
    fom_stds.append(fom_sd)
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
    angles.append(int(angle)+90)
    m_list.append(rom_mean)
    sd_list.append(rom_sd)

data = np.column_stack((angles, merr_list, sderr_list, m_list,
                       sd_list, fom_means, fom_stds))
data = data[data[:, 0].argsort()]

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N='+N+'$, ' +
               r'$\theta^*_g = '+str(int(anchor))+'$'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[1e-4, 1], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
       r'\langle \widehat{\text{Nu}} \rangle_s|}' +
       r'{|\langle \text{Nu} \rangle_s|}$')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.semilogy(data[:, 0], data[:, 1], **plot_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'relmnu_N_'+N+'.png')
plt.close(fig)

plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}
FOM_params = {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'}
fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[1, 4], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel='Mean Nu')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 3], **plot_params)
ax.plot(data[:, 0], data[:, 5], **FOM_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'mnu_N_'+N+'.png')

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylim=[0, 0.3], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel='std(Nu)')
ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 4], **plot_params)
ax.plot(data[:, 0], data[:, 6], **FOM_params)
ax.legend(loc=1)
fig.savefig('.'+target_dir+'stdnu_N_'+N+'.png')

np.savetxt('.'+target_dir+'angle.dat', data[:, 0])
np.savetxt('.'+target_dir+'merr_N_'+N+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'sderr_N_'+N+'.dat', data[:, 2])
np.savetxt('.'+target_dir+'m_N_'+N+'.dat', data[:, 3])
np.savetxt('.'+target_dir+'sd_N_'+N+'.dat', data[:, 4])
