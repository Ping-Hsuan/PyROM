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
mode = str(sys.argv[5])
print("---------------------------------------------")

target_dir = '/nu/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/nu'
if model == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_ic_h10_(?!.*-90|.*-80|.*-70).*$')
if model == 'l-rom' or model == 'l-rom_df':
    fd = str(sys.argv[5])
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_'+fd+'.*$')
    elif T0 >= 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_'+fd+'.*$')
else:
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
    elif T0 >= 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
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

if model == 'l-rom' or model == 'l-rom_df':
    fd = fd.strip("0")
    plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)}
else:
    plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}
fig1, ax1 = plt.subplots(1, tight_layout=True)
ax1.set(ylim=[1e-4, 1], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
       r'\langle \widehat{\text{Nu}} \rangle_s|}' +
       r'{|\langle \text{Nu} \rangle_s|}$')
ax1.set_xticklabels(ax1.get_xticks(), rotation=45)
ax1.semilogy(data[:, 0], data[:, 1], **plot_params)
ymin, ymax = ax1.get_ylim()
ax1.semilogy(int(anchor), ymin, 'ro', label='Anchor point')
ax1.legend(loc=1)

FOM_params = {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'}
fig2, ax2 = plt.subplots(1, tight_layout=True)
ax2.set(ylim=[1, 4], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel='Mean Nu')
ax2.set_xticklabels(ax2.get_xticks(), rotation=45)
ax2.plot(data[:, 0], data[:, 3], **plot_params)
ax2.plot(data[:, 0], data[:, 5], **FOM_params)
ymin, ymax = ax2.get_ylim()
ax2.plot(int(anchor), ymin, 'ro', label='Anchor point')
ax2.legend(loc=1)

fig3, ax3 = plt.subplots(1, tight_layout=True)
ax3.set(ylim=[0, 0.3], xticks=np.linspace(0, 180, 19, dtype=int),
       xlabel=r'$\theta_g$', ylabel='std(Nu)')
ax3.set_xticklabels(ax3.get_xticks(), rotation=45)
ax3.plot(data[:, 0], data[:, 4], **plot_params)
ax3.plot(data[:, 0], data[:, 6], **FOM_params)
ymin, ymax = ax3.get_ylim()
ax3.plot(int(anchor), ymin, 'ro', label='Anchor point')
ax3.legend(loc=1)

if model == 'l-rom' or model == 'l-rom_df':
    fig1.savefig('.'+target_dir+'relmnu_N'+N+'_'+fd+'_'+mode+'.png')
    fig2.savefig('.'+target_dir+'mnu_N'+N+'_'+fd+'_'+mode+'.png')
    fig3.savefig('.'+target_dir+'stdnu_N'+N+'_'+fd+'_'+mode+'.png')

    np.savetxt('.'+target_dir+'angle_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'merr_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'stderr_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'mnu_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'stdnu_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 4])
else:
    fig1.savefig('.'+target_dir+'relmnu_N'+N+'_'+mode+'.png')
    fig2.savefig('.'+target_dir+'mnu_N'+N+'_'+mode+'.png')
    fig3.savefig('.'+target_dir+'stdnu_N'+N+'_'+mode+'.png')

    np.savetxt('.'+target_dir+'angle_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'merr_N'+N+'_'+mode+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'stderr_N'+N+'_'+mode+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'mnu_N'+N+'_'+mode+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'stdnu_N'+N+'_'+mode+'.dat', data[:, 4])
