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
mode = str(sys.argv[6])
print("---------------------------------------------")

target_dir = '/vel_dual_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/vel_dual_norm'
if model == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_ic_h10_(?!.*-90|.*-80|.*-70).*$')
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
ylims = [1e-4, 1e-1]

# scaled the dual norm with argv[4]
if sc == 'rom':
    # scaled with the rom_norm at training points
    sc_dir = './rom_norm/'
    scale = np.loadtxt(sc_dir+'rom_u_h1norm_N'+N+'_'+mode+'.dat')
    ylb = r'$\frac{\triangle_u(\theta_g)}{\|\langle \bf{u}_{ROM}(\theta_g) \rangle_g\|_{H^1}}$'
elif sc == 'fom':
    # scaled with the fom_norm at anchor point
    sc_dir = './fom_norm/'
    angles = np.loadtxt(sc_dir+'angle.dat')
    idx = np.where(angles == int(anchor))
    print('Scaled with fom norm anchored at:', angles[idx])
    tmp = np.loadtxt(sc_dir+'fom_u_h1norm.dat')
    scale = tmp[idx]
    ylb = r'$\frac{\triangle_u(\theta_g)}{\|\langle \bf{u}_{FOM}(\theta^*_g) \rangle_g\|_{H^1}}$'
elif sc == 'romabserr':
    # scaled with the rom_abserr, the result is so called the effectivity
    sc_dir = './vel_mabserr/'
    scale = np.loadtxt(sc_dir+'vel_rom_abserr_N'+N+'_'+mode+'.dat')
    print(scale)
    ylb = r'$\frac{\triangle_u(\theta_g)}{\|\langle \bf{u}_{FOM}-u_{ROM} \rangle_g\|_{H^1}}$'
elif sc == 'eta':
    # scaled with the effectivity
    sc_dir = './vel_mabserr/'
    abserr = np.loadtxt(sc_dir+'vel_rom_abserr_N'+N+'_'+mode+'.dat')
    angle = np.loadtxt('./vel_dual_norm/angle_list_'+mode+'.dat')
    dual = np.loadtxt('./vel_dual_norm/vel_erri_N'+N+'_'+mode+'.dat')
    anchor = setup.find_anchor()
    idx = np.where(angle == int(anchor))
    print(idx)
    ylb = r'$\frac{\triangle_u(\theta_g)}{\eta_u(\theta^*_g)}$'
    effect = dual/abserr
    scale = effect[idx]
    print(scale)
    ylims = [1e-1, 1e3]
elif sc == 'eta_rom':
    # scaled with the rom_abserr
    # This is essentially the effectivity
    sc_dir = './vel_mabserr/'
    abserr = np.loadtxt(sc_dir+'vel_rom_abserr_N'+N+'_'+mode+'.dat')
    angle = np.loadtxt('./vel_dual_norm/angle_list_'+mode+'.dat')
    dual = np.loadtxt('./vel_dual_norm/vel_erri_N'+N+'_'+mode+'.dat')
    anchor = setup.find_anchor()
    idx = np.where(angle == int(anchor))
    print(idx)
    ylb = r'$\frac{\triangle_u(\theta_g)\|\langle \bf{u}_{ROM}(\theta^*_g) \rangle_g\|}{\eta_u(\theta^*_g)}$'
    effect = dual/abserr
    sc_dir = './rom_norm/'
    rom_norm = np.loadtxt(sc_dir+'rom_u_h1norm_N'+N+'_'+mode+'.dat')
    print(abserr)
    print(dual)
    print(effect)
    print(rom_norm)
    scale = effect[idx]*rom_norm[idx]
    print(scale)
    ylims = [1e-2, 1e3]
elif sc == 'eta_rom_all':
    # scaled with the rom_abserr
    # This is essentially the effectivity
    sc_dir = './vel_mabserr/'
    abserr = np.loadtxt(sc_dir+'vel_rom_abserr_N'+N+'_'+mode+'.dat')
    angle = np.loadtxt('./vel_dual_norm/angle_list_'+mode+'.dat')
    dual = np.loadtxt('./vel_dual_norm/vel_erri_N'+N+'_'+mode+'.dat')
    anchor = setup.find_anchor()
    idx = np.where(angle == int(anchor))
    print(idx)
    ylb = r'$\frac{\triangle_u(\theta_g)\|\langle \bf{u}_{ROM}(\theta_g) \rangle_g\|}{\eta_u(\theta^*_g)}$'
    effect = dual/abserr
    sc_dir = './rom_norm/'
    rom_norm = np.loadtxt(sc_dir+'rom_u_h1norm_N'+N+'_'+mode+'.dat')
    print(abserr)
    print(dual)
    print(effect)
    print(rom_norm)
    scale = effect[idx]*rom_norm
    print(scale)
    ylims = [1e-2, 1e3]
elif sc == 'domain':
    # scaled with the domain length
    angle = np.loadtxt('./vel_dual_norm/angle_list_'+mode+'.dat')
    dual = np.loadtxt('./vel_dual_norm/vel_erri_N'+N+'_'+mode+'.dat')
    anchor = setup.find_anchor()
    idx = np.where(angle == int(anchor))
    ylb = r'$\frac{\triangle_u(\theta_g)}{|V|^{1/2}}$'
    domain = 40*np.sin(angle*np.pi/180)
    scale = np.sqrt(domain)
    ylims = [1e-2, 1e3]


# scaled the erri
data[:, 1] = data[:, 1]/scale
print(data[:, 1])

solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

fig, ax = plt.subplots(1, tight_layout=True)
plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$N='+N+'$'}
#ax.set(ylabel=ylb, xlabel=r'$\theta_g$', ylim=ylims,
#       xticks=np.linspace(0, 180, 19, dtype=int))
ax.set(ylabel=ylb, xlabel=r'$\theta_g$',
       xticks=np.linspace(0, 180, 19, dtype=int))

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.plot(data[:, 0], data[:, 1], **plot_params)
ax.legend(loc=0)

print("---------------------------------------------")
fig.savefig('.'+target_dir+'vel_dual_norm_N'+N+'_sc_'+sc+'.png')
np.savetxt('.'+target_dir+'vel_erri_N'+N+'_sc_'+sc+'.dat', data[:, 1])
print("---------------------------------------------")

