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
deg = str(int(sys.argv[3])-90)
sc = str(sys.argv[4])
print("---------------------------------------------")

target_dir = '/dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/dual_norm'
root, filenames = setup.gtfpath(search_dir, '^.*_h10_'+deg+'_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

erri = []
N_list = []
for nb, fnames in dict_final:
    for fname in fnames:
        data = reader.reader(fname)
        dual_norm = np.array(data).astype(np.float64)
        erri.append(float(dual_norm))
        N_list.append(int(nb))

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')
data = np.column_stack((N_list, erri))
data = data[data[:, 0].argsort()]

# scaled the dual norm with argv[4]
if sc == 'rom':
    # scaled with the rom_norm
    sc_dir = './rom_norm/'
    scale = np.loadtxt(sc_dir+'rom_h1norm_theta_'+str(int(deg)+90)+'.dat')
    print(scale)
    ylb = r'$\frac{\triangle(\theta_g='+str(int(deg)+90) + \
          r')}{\|u_{ROM}(\theta_g)\|_{H^1}}$'
elif sc == 'fom':
    # scaled with the fom_norm at anchor point
    sc_dir = '../'+model+'_info/fom_norm/'
    angles = np.loadtxt(sc_dir+'angle.dat')
    idx = np.where(angles == int(deg)+90)
    print('Scaled with fom norm anchored at:', angles[idx])
    tmp = np.loadtxt(sc_dir+'fom_h1norm.dat')
    scale = tmp[idx]
    ylb = r'$\frac{\triangle(\theta_g='+str(int(deg)+90) + \
          r')}{\|u_{FOM}(\theta^*_g)\|_{H^1}}$'
elif sc == 'romabserr':
    # scaled with the rom_abserr
    sc_dir = './abserr/'
    scale = np.loadtxt(sc_dir+'rom_abserr_theta_'+str(int(deg)+90)+'.dat')
    ylb = r'$\frac{\triangle(\theta_g='+str(int(deg)+90) + \
          r')}{\|u_{FOM}-u_{ROM}\|_{H^1}}$'

# scaled the erri
data[:, 1] = data[:, 1]/scale

if len(N_list) == 1:
    pass
else:
    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}
    ax.set(ylabel=ylb, xlabel=r'$N$',
           ylim=[1e-4, 1e-1], xlim=[1, max(data[:, 0])])
    ax.semilogy(data[:, 0], data[:, 1], **plot_params)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'dual_norm_theta_'+str(int(deg)+90)+'_sc_'+sc+'.png')
    print("---------------------------------------------")

np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'erri_theta_'+str(int(deg)+90)+'_sc_'+sc+'.dat', data[:, 1])
