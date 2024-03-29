import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker

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

target_dir = '/temp_mabserr/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/temp_mabserr'
if model == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_ic_h10_(?!.*-90|.*-80|.*-70).*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))
print(dict_final)

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
        angles.append(int(angle)+90)

data = np.column_stack((angles, abserr_rom, abserr_proj))
data = data[data[:, 0].argsort()]

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                'label': solver+' with '+r'$N='+N+'$'}
plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                'label': 'Projection with '+r'$N='+N+'$'}

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(xlabel=r'$\theta_g$', ylabel=r'$\|u(\theta_g) -' +
       r'\tilde{u}(\theta_g;{\theta^*_g} =' + str(int(anchor))+')\|$',
       xticks=np.linspace(0, 180, 19, dtype=int),
       title='Absolute error in the mean temperature with \n ROM anchor at ' +
       r'$\theta^*_g='+str(int(anchor))+'$')

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 1], **plot_params1)
ax.plot(data[:, 0], data[:, 2], **plot_params2)
ymin, ymax = ax.get_ylim()
ax.plot(int(anchor), ymin, 'ro', label='Anchor point')
ax.legend(loc=0, ncol=1)

print("---------------------------------------------")
fig.savefig('.'+target_dir+'temp_abserr_N'+N+'_'+mode+'.png')
np.savetxt('.'+target_dir+'angle_list_'+mode+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'temp_rom_abserr_N'+N+'_'+mode+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'temp_proj_abserr_N'+N+'_'+mode+'.dat', data[:, 2])
print("---------------------------------------------")



