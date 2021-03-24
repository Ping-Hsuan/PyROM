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
sc = str(sys.argv[5])
print("---------------------------------------------")

target_dir = '/dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/dual_norm'
root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

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

anchor = setup.find_anchor()
data = np.column_stack((angles, erri))
data = data[data[:, 0].argsort()]

# scaled the dual norm with argv[4]
if sc == 'rom':
    # scaled with the rom_norm
    sc_dir = './rom_norm/'
    scale = np.loadtxt(sc_dir+'rom_h1norm_N'+N+'.dat')
    ylb = r'$\frac{\triangle(\theta_g)}{\|u_{ROM}(\theta_g)\|_{H^1}}$'
elif sc == 'fom':
    # scaled with the fom_norm at anchor point
    sc_dir = '../'+model+'_info/fom_norm/'
    angles = np.loadtxt(sc_dir+'angle.dat')
    idx = np.where(angles == int(anchor))
    print('Scaled with fom norm anchored at:', angles[idx])
    tmp = np.loadtxt(sc_dir+'fom_h1norm.dat')
    scale = tmp[idx]
    ylb = r'$\frac{\triangle(\theta_g)}{\|u_{FOM}(\theta^*_g)\|_{H^1}}$'
elif sc == 'romabserr':
    # scaled with the rom_abserr
    sc_dir = './abserr/'
    scale = np.loadtxt(sc_dir+'rom_abserr_N'+N+'.dat')
    print(scale)
    ylb = r'$\frac{\triangle(\theta_g)}{\|u_{FOM}-u_{ROM}\|_{H^1}}$'

# scaled the erri
data[:, 1] = data[:, 1]/scale

solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

fig, ax = plt.subplots(1, tight_layout=True)
plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N='+N+'$'}
ax.set(ylabel=ylb, xlabel=r'$\theta_g$', ylim=[1e-4, 1e-1],
       xticks=np.linspace(0, 180, 19, dtype=int))

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.semilogy(data[:, 0], data[:, 1], **plot_params)
ax.legend(loc=0)

print("---------------------------------------------")
fig.savefig('.'+target_dir+'dual_norm_N'+N+'_sc_'+sc+'.png')
np.savetxt('.'+target_dir+'erri_N'+N+'_sc_'+sc+'.dat', data[:, 1])
print("---------------------------------------------")

