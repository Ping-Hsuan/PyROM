import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
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

target_dir = '/vel_dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/vel_dual_norm'
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

erri = []
angles = []
for angle, fnames in dict_final:
    for fname in fnames:
        data = reader.reader(fname)
        if not data:
            data = 1e8
        dual_norm = np.array(data).astype(np.float64)
        erri.append(float(dual_norm))
        angles.append(int(angle)+90)

data = np.column_stack((angles, erri))
data = data[data[:, 0].argsort()]

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

fig, ax = plt.subplots(1, tight_layout=True)
if model == 'l-rom' or model == 'l-rom_df':
    fd = fd.strip("0")
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)}
else:
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}
ax.set(ylabel=r'$\triangle(\theta_g;{\theta^*_g}='+str(int(anchor))+r')$',
       xlabel=r'$\theta_g$', ylim=[1e-2, 1],
       xticks=np.linspace(0, 180, 19, dtype=int))

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.semilogy(data[:, 0], data[:, 1], **plot_params)
ymin, ymax = ax.get_ylim()
ax.semilogy(int(anchor), ymin, 'ro', label='Anchor point')
ax.legend(loc=0)

print("---------------------------------------------")
if model == 'l-rom' or model == 'l-rom_df':
    fig.savefig('.'+target_dir+'vel_dual_norm_N'+N+'_'+fd+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'angle_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'vel_erri_N'+N+'_'+fd+'_'+mode+'.dat', data[:, 1])
else:
    fig.savefig('.'+target_dir+'vel_dual_norm_N'+N+'_'+mode+'.png')
    np.savetxt('.'+target_dir+'angle_list_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'vel_erri_N'+N+'_'+mode+'.dat', data[:, 1])
print("---------------------------------------------")

