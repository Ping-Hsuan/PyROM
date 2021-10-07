import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
import yaml

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
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_*.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_*_h10_(?!.*-90|.*-80|.*-70).*$')
if model == 'l-rom' or model == 'l-rom_df':
    fd = str(sys.argv[6])
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_'+fd+'.*$')
    elif T0 > 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_'+fd+'.*$')
else:
    if T0 == 1:
#       files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_.*_(-?\d+)_dual_norm$')
    elif T0 > 1:
#       files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
        print(filenames)
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_.*_(-?\d+)_dual_norm$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))
print(dict_final)

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

with open('../g-rom/anchor.yaml') as f:
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

with open('../g-rom/train.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
tkey = list(features.keys())
tval = list(features.values())
print(tval[0])
print(data[:, 0])

ax.set(ylabel=r'$\triangle$', xlabel=r'$'+tkey[0]+'$', ylim=[1e-2, 1], xticks=tval[0])

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.semilogy(data[:, 0], data[:, 1], **plot_params)
ymin, ymax = ax.get_ylim()
ax.semilogy(aval[0], ymin, 'ro', label='Anchor point')
ax.legend(loc=0)

print("---------------------------------------------")
if model == 'l-rom' or model == 'l-rom_df':
    fig.savefig('.'+target_dir+'dual_norm_N'+N+'_'+fd+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'angle_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 1])
else:
    fig.savefig('.'+target_dir+'dual_norm_N'+N+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'angle_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_N'+N+'_'+mode+'.dat', data[:, 1])
print("---------------------------------------------")
