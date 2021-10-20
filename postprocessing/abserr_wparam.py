import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
import math
import yaml

# This script is used to plot ROM absolute error and
# Proejction error with theta at a given N

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

target_dir = '/mabserr/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/mabserr'
if mode == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*_h10_(?!.*-90|.*-80|.*-70).*$')
if model == 'l-rom' or model == 'l-rom_df':
    fd = str(sys.argv[6])
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_'+fd+'_mabserr$')
    elif T0 >= 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_'+fd+'.*$')
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_'+fd+'_mabserr$')
else:
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_mabserr$')
    elif T0 >= 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_mabserr$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

angles = []
abserr_rom = []
abserr_proj = []
for angle, fnames in dict_final:
    for fname in fnames:
        data = reader.reader(fname)
        if not data:
            data.append(1e8)
            data.append(1e8)
        data = np.array(data).astype(np.float64)
        abserr_rom.append(data[0])
        abserr_proj.append(data[1])
        angles.append(int(angle))

data = np.column_stack((angles, abserr_rom, abserr_proj))
data = data[data[:, 0].argsort()]

with open('../anchor.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
akey = list(features.keys())
aval = list(features.values())

#anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                'label': solver+' with '+r'$N='+N+'$'}
plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                'label': 'Projection with '+r'$N='+N+'$'}

with open('../train.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
tkey = list(features.keys())
tval = list(features.values())
print(tval[0])
print(data[:, 0])

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}$', xticks=tval[0], title='Absolute error in the predicted mean flow at '+r'$\mathcal{P}_{train}$')

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 1], **plot_params1)
ax.plot(data[:, 0], data[:, 2], **plot_params2)
idx = np.where(data[:, 0] == aval[0])
ax.plot(aval[0], data[idx, 1], 'ro', label='Anchor point')
ax.legend(loc=0, ncol=1)

print("---------------------------------------------")
fig.savefig('.'+target_dir+'abserr_N'+N+'_'+mode+'.png')
np.savetxt('.'+target_dir+'param_list_'+mode+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'rom_abserr_N'+N+'_'+mode+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'proj_abserr_N'+N+'_'+mode+'.dat', data[:, 2])
print("---------------------------------------------")



