import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
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

target_dir = '/dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/dual_norm'
if mode == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_*_h10_(?!.*-90|.*-80|.*-70).*$')
if model == 'l-rom' or model == 'l-rom_df':
    fd = str(sys.argv[6])
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_'+fd+'_dual_norm$')
    elif T0 > 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_'+fd+'_dual_norm$')
else:
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_dual_norm$')
    elif T0 > 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
        print(filenames)
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_dual_norm$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

erri = []
angles = []
for angle, fnames in dict_final:
    for fname in fnames:
        data = reader.reader(fname)
        if not data:
            data = 1e8
        dual_norm = np.array(data).astype(np.float64)
        erri.append(float(dual_norm))
        angles.append(int(angle))

data = np.column_stack((angles, erri))
data = data[data[:, 0].argsort()]

with open('../anchor.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
akey = list(features.keys())
aval = list(features.values())

#anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

fig, ax = plt.subplots(1, tight_layout=True)
if model == 'l-rom' or model == 'l-rom_df':
    fd = fd.strip("0")
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)}
else:
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': solver+' with '+r'$N='+N+'$'}

with open('../train.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
tkey = list(features.keys())
tval = list(features.values())
print(tval[0])
print(data[:, 0])

#ax.set(ylabel=r'$\triangle$', xlabel=r'$'+tkey[0]+'$', ylim=[1e-2, 1], xticks=tval[0], title='Dual norm of the discrete time-averaged residual at '+r'$\mathcal{P}_{train}$')
ax.set(ylabel=r'$\triangle$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged residual at '+r'$\mathcal{P}_{train}$')

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 1], **plot_params)
idx = np.where(data[:, 0] == aval[0])
ylim_exp = math.ceil(math.log10(min(data[:, 1])))-1
#f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
#g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
ax.set_ylim([10**ylim_exp, None])
#plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
#plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
ax.plot(aval[0], data[idx, 1], 'ro', label='Anchor point')
ax.legend(loc=0)

print("---------------------------------------------")
if model == 'l-rom' or model == 'l-rom_df':
    fig.savefig('.'+target_dir+'dual_norm_N'+N+'_'+fd+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'param_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 1])
else:
    fig.savefig('.'+target_dir+'dual_norm_N'+N+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'param_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_N'+N+'_'+mode+'.dat', data[:, 1])
print("---------------------------------------------")
