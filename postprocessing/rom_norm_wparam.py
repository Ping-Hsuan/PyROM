import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker
import aux

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

target_dir = '/rom_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/rom_norm'
if model == 'all':
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
else:
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_ic_h10_(?!.*-90|.*-80|.*-70).*$')
if T0 == 1:
    files_dict = setup.create_dict(filenames, '^.*_ic_h10_(-?\d+)_.*$')
elif T0 >= 1:
    files_dict = setup.create_dict(filenames, '^.*_zero_h10_(-?\d+)_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

color_ctr = 0
tpath = root+'/'

angles = []
rom_norm = []
for angle, fnames in dict_final:
    for fname in fnames:
        with open(fname, 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                         and k != 'norm:'] for line in list_of_lines][:-1]
        data = [x[-1] for x in list_of_words]
        if not data:
            data = [1e8 for i in range(9)]
        data = np.array(data).astype(np.float64)
        rom_norm.append(data)
        angles.append(int(angle)+90)

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*nb.*$')

data = np.column_stack((angles, rom_norm))
data = data[data[:, 0].argsort()]

# fix the h1 norm
for j in range(data.shape[0]):
    data[j, 3] = np.sqrt(data[j, 1]**2+data[j, 2]**2)
    data[j, 6] = np.sqrt(data[j, 4]**2+data[j, 5]**2)
    data[j, 9] = np.sqrt(data[j, 7]**2+data[j, 8]**2)

fig1, ax = plt.subplots(1, tight_layout=True)
fom1 = np.loadtxt('./fom_norm/fom_h10norm.dat')
fom2 = np.loadtxt('./fom_norm/fom_l2norm.dat')
fom3 = np.loadtxt('./fom_norm/fom_h1norm.dat')
ax.plot(data[:, 0], fom1, 'k-o', mfc="None", label=r'FOM $H^1_0$ norm')
ax.plot(data[:, 0], fom2, 'k-x', mfc="None", label=r'FOM $L^2$ norm')
ax.plot(data[:, 0], fom3, 'k-v', mfc="None", label=r'FOM $H^1$ norm')
aux.plot_rom_norm_wparam(data[:, 0], data[:, 7], data[:, 8], data[:, 9], ax, 'uT')
ax.set_title('Norm of total field comparison between \n FOM and '+solver+' with '+r'$N='+N+'$')
plt.legend(loc=0)
ax.set_ylim([0, 50])
ymin, ymax = ax.get_ylim()
ax.plot(int(anchor), ymin, 'ro', label='Anchor point')
plt.legend(loc=1, ncol=4, fontsize=8)
fig1.savefig('.'+target_dir+'rom_norm_'+mode+'.png')

fig2, ax = plt.subplots(1, tight_layout=True)
fom1 = np.loadtxt('./fom_norm/fom_u_h10norm.dat')
fom2 = np.loadtxt('./fom_norm/fom_u_l2norm.dat')
fom3 = np.loadtxt('./fom_norm/fom_u_h1norm.dat')
ax.plot(data[:, 0], fom1, 'k-o', mfc="None", label=r'FOM $H^1_0$ norm')
ax.plot(data[:, 0], fom2, 'k-x', mfc="None", label=r'FOM $L^2$ norm')
ax.plot(data[:, 0], fom3, 'k-v', mfc="None", label=r'FOM $H^1$ norm')
aux.plot_rom_norm_wparam(data[:, 0], data[:, 1], data[:, 2], data[:, 3], ax, 'u')
ax.set_title('Norm of velocity field comparison between \n FOM and '+solver+' with '+r'$N='+N+'$')
plt.legend(loc=0)
ax.set_ylim([0, 45])
ymin, ymax = ax.get_ylim()
ax.plot(int(anchor), ymin, 'ro', label='Anchor point')
plt.legend(loc=1, ncol=4, fontsize=8)
fig2.savefig('.'+target_dir+'vel_rom_norm_'+mode+'.png')

fig3, ax = plt.subplots(1, tight_layout=True)
fom1 = np.loadtxt('./fom_norm/fom_T_h10norm.dat')
fom2 = np.loadtxt('./fom_norm/fom_T_l2norm.dat')
fom3 = np.loadtxt('./fom_norm/fom_T_h1norm.dat')
ax.plot(data[:, 0], fom1, 'k-o', mfc="None", label=r'FOM $H^1_0$ norm')
ax.plot(data[:, 0], fom2, 'k-x', mfc="None", label=r'FOM $L^2$ norm')
ax.plot(data[:, 0], fom3, 'k-v', mfc="None", label=r'FOM $H^1$ norm')
aux.plot_rom_norm_wparam(data[:, 0], data[:, 4], data[:, 5], data[:, 6], ax, 'T')
ax.set_title('Norm of temperature field comparison between \n FOM and '+solver+' with '+r'$N='+N+'$')
ax.set_ylim([0, 25])
ymin, ymax = ax.get_ylim()
ax.plot(int(anchor), ymin, 'ro', label='Anchor point')
plt.legend(loc=1, ncol=4, fontsize=8)
fig3.savefig('.'+target_dir+'temp_rom_norm_'+mode+'.png')

print("---------------------------------------------")
if mode == 'all':
    np.savetxt('.'+target_dir+'rom_u_h10norm_N'+N+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'rom_u_l2norm_N'+N+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'rom_u_h1norm_N'+N+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'rom_T_h10norm_N'+N+'.dat', data[:, 4])
    np.savetxt('.'+target_dir+'rom_T_l2norm_N'+N+'.dat', data[:, 5])
    np.savetxt('.'+target_dir+'rom_T_h1norm_N'+N+'.dat', data[:, 6])
    np.savetxt('.'+target_dir+'angle.dat', data[:, 0])
    np.savetxt('.'+target_dir+'rom_h10norm_N'+N+'.dat', data[:, 7])
    np.savetxt('.'+target_dir+'rom_l2norm_N'+N+'.dat', data[:, 8])
    np.savetxt('.'+target_dir+'rom_h1norm_N'+N+'.dat', data[:, 9])
    fig.savefig('.'+target_dir+'rom_norm.png')
else:
    np.savetxt('.'+target_dir+'rom_u_h10norm_N'+N+'_'+mode+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'rom_u_l2norm_N'+N+'_'+mode+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'rom_u_h1norm_N'+N+'_'+mode+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'rom_T_h10norm_N'+N+'_'+mode+'.dat', data[:, 4])
    np.savetxt('.'+target_dir+'rom_T_l2norm_N'+N+'_'+mode+'.dat', data[:, 5])
    np.savetxt('.'+target_dir+'rom_T_h1norm_N'+N+'_'+mode+'.dat', data[:, 6])
    np.savetxt('.'+target_dir+'angle_'+mode+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'rom_h10norm_N'+N+'_'+mode+'.dat', data[:, 7])
    np.savetxt('.'+target_dir+'rom_l2norm_N'+N+'_'+mode+'.dat', data[:, 8])
    np.savetxt('.'+target_dir+'rom_h1norm_N'+N+'_'+mode+'.dat', data[:, 9])

