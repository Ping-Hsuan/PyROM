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
import yaml
import math

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
if mode == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*_h10_(?!.*-90|.*-80|.*-70).*$')
print(filenames)
if model == 'l-rom' or model == 'l-rom_df':
    fd = str(sys.argv[6])
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_'+fd+'_nu$')
    elif T0 >= 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_'+fd+'_nu$')
else:
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_nu$')
    elif T0 >= 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_nu$')
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
#   filename = '../../../../fom_nuss/nuss_fom_'+str(int(angle)+90)
    filename = '../../fom_nuss/nus_fom_'+str(int(angle))
    data = mypostpro.read_nuss(filename)
    if (angle == '10000'):
        data[:, 2] = data[:, 2]/40
    else:
        data[:, 2] = data[:, 2]
    idx1 = mypostpro.find_nearest(data[:, 0], 0)
    idx2 = mypostpro.find_nearest(data[:, 0], 1000)
    nuss_fom = data[idx1:idx2, :]
    avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
    fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
    fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
    fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
    print('FOM data at deg '+str(int(angle)), ', Mean nu ', fom_mean, 'Std(Nu): ', fom_sd)
    fom_means.append(fom_mean)
    fom_stds.append(fom_sd)
    for fname in fnames:

        nuss = mypostpro.read_nuss(fname)
        nuss[:, 2] = nuss[:, 2]/40
        avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(sys.argv[4]))
        rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
        rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
        rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
        [mean_err, var_err, sd_err] = mypostpro.cnuss_err(fom_mean, fom_var,
                                                          fom_sd, rom_mean,
                                                          rom_var, rom_sd)
    merr_list.append(mean_err)
    verr_list.append(var_err)
    sderr_list.append(sd_err)
    angles.append(int(angle))
    m_list.append(rom_mean)
    sd_list.append(rom_sd)

data = np.column_stack((angles, merr_list, sderr_list, m_list,
                       sd_list, fom_means, fom_stds))
data = data[data[:, 0].argsort()]

#anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

if model == 'l-rom' or model == 'l-rom_df':
    fd = fd.strip("0")
    plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)}
else:
    plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}

with open('../anchor.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
akey = list(features.keys())
aval = list(features.values())

with open('../train.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
tkey = list(features.keys())
tval = list(features.values())
print(tval[0])
print(data[:, 0])

fig1, ax1 = plt.subplots(1, tight_layout=True)
ax1.set(ylim=[1e-4, 1], xticks=tval[0], xlabel=r'$'+tkey[0]+'$',
        ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
        r'\langle \tilde{\text{Nu}} \rangle_s|}' + r'{|\langle \text{Nu} \rangle_s|}$', title='Relative error in the predicted mean Nu at '+r'$\mathcal{P}_{train}$')

ax1.set_xticklabels(ax1.get_xticks(), rotation=45)
ax1.semilogy(data[:, 0], data[:, 1], **plot_params)
idx = np.where(data[:, 0] == aval[0])
ylim_exp = math.ceil(math.log10(min(data[:, 1])))-1
ax1.set_ylim([10**ylim_exp, None])
ax1.semilogy(aval[0], data[idx, 1], 'ro', label='Anchor point')
ax1.legend(loc=1)

FOM_params = {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'}
fig2, ax2 = plt.subplots(1, tight_layout=True)
ax2.set(ylim=[1, 4], xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='Mean Nu', title='FOM and predicted mean Nu at '+r'$\mathcal{P}_{train}$')
ax2.set_xticklabels(ax2.get_xticks(), rotation=45)
ax2.plot(data[:, 0], data[:, 3], **plot_params)
ax2.plot(data[:, 0], data[:, 5], **FOM_params)
idx = np.where(data[:, 0] == aval[0])
ylim_exp = math.ceil(math.log10(min(data[:, 3])))-1
ax2.set_ylim([10**ylim_exp, None])
ax2.plot(aval[0], data[idx, 3], 'ro', label='Anchor point')
ax2.legend(loc=1)

fig3, ax3 = plt.subplots(1, tight_layout=True)
ax3.set(ylim=[0, 0.3], xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='std(Nu)', title='FOM and predicted Std(Nu) at '+r'$\mathcal{P}_{train}$')
ax3.set_xticklabels(ax3.get_xticks(), rotation=45)
ax3.plot(data[:, 0], data[:, 4], **plot_params)
ax3.plot(data[:, 0], data[:, 6], **FOM_params)
ymin, ymax = ax3.get_ylim()
ax3.plot(aval[0], ymin, 'ro', label='Anchor point')
ax3.legend(loc=1)

if model == 'l-rom' or model == 'l-rom_df':
    fig1.savefig('.'+target_dir+'relmnu_N'+N+'_'+fd+'_'+mode+'.png')
    fig2.savefig('.'+target_dir+'mnu_N'+N+'_'+fd+'_'+mode+'.png')
    fig3.savefig('.'+target_dir+'stdnu_N'+N+'_'+fd+'_'+mode+'.png')

    np.savetxt('.'+target_dir+'param_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'merr_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'stderr_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'mnu_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'stdnu_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 4])
else:
    fig1.savefig('.'+target_dir+'relmnu_N'+N+'_'+mode+'.png')
    fig2.savefig('.'+target_dir+'mnu_N'+N+'_'+mode+'.png')
    fig3.savefig('.'+target_dir+'stdnu_N'+N+'_'+mode+'.png')

    np.savetxt('.'+target_dir+'param_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'merr_N'+N+'_'+mode+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'stderr_N'+N+'_'+mode+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'mnu_N'+N+'_'+mode+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'stdnu_N'+N+'_'+mode+'.dat', data[:, 4])
