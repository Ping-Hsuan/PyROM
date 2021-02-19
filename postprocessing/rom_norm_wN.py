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
print("---------------------------------------------")

target_dir = '/rom_norm/'
setup.checkdir(target_dir)

search_dir = './'+model+'_info/rom_norm'
root, filenames = setup.gtfpath(search_dir, '^.*_h10_'+deg+'_.*$')
files_dict = setup.create_dict(filenames, '^.*_([0-9]*)nb_.*$')
dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))


color_ctr = 0
tpath = root+'/'

rom_norm = []
N_list = []
for nb, fnames in dict_final:
    for fname in fnames:
        with open(fname, 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k and k != 'dual'
                         and k != 'norm:'] for line in list_of_lines][:-1]
        data = [x[-1] for x in list_of_words]
        data = np.array(data).astype(np.float64)
        rom_norm.append(data)
        N_list.append(int(nb))

anchor = setup.find_anchor()
solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

data = np.column_stack((N_list, rom_norm))
data = data[data[:, 0].argsort()]

# fix the h1 norm
for j in range(data.shape[0]):
    data[j, 3] = np.sqrt(data[j, 1]**2+data[j, 2]**2)
    data[j, 6] = np.sqrt(data[j, 4]**2+data[j, 5]**2)
    data[j, 9] = np.sqrt(data[j, 7]**2+data[j, 8]**2)

plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
               'label': solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$'}

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||(u, T)\|_{*}$', xlabel=r'$N$',
       title=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.plot(data[:, 0], data[:, 7], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 8], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 9], 'k-o', mfc="None", label=r'$H^1$')
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+target_dir+'rom_h1norm.png')
np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
np.savetxt('.'+target_dir+'rom_h10norm_theta_'+str(int(deg)+90)+'.dat', data[:, 7])
np.savetxt('.'+target_dir+'rom_l2norm_theta_'+str(int(deg)+90)+'.dat', data[:, 8])
np.savetxt('.'+target_dir+'rom_h1norm_theta_'+str(int(deg)+90)+'.dat', data[:, 9])
print("---------------------------------------------")
plt.close(fig)

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||u\|_{*}$', xlabel=r'$N$',
       title=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.plot(data[:, 0], data[:, 1], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 2], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 3], 'k-o', mfc="None", label=r'$H^1$')
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+target_dir+'rom_u_norm.png')
np.savetxt('.'+target_dir+'rom_u_h10norm_theta_'+str(int(deg)+90)+'.dat', data[:, 1])
np.savetxt('.'+target_dir+'rom_u_l2nor_theta_'+str(int(deg)+90)+'m.dat', data[:, 2])
np.savetxt('.'+target_dir+'rom_u_h1nor_theta_'+str(int(deg)+90)+'m.dat', data[:, 3])
print("---------------------------------------------")

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(ylabel=r'$\||T\|_{*}$', xlabel=r'$N$',
       title=solver+' with '+r'$\theta^*_g = '+str(int(anchor))+'$')
ax.plot(data[:, 0], data[:, 4], 'b-o', mfc="None", label=r'$H^1_0$')
ax.plot(data[:, 0], data[:, 5], 'r-o', mfc="None", label=r'$L^2$')
ax.plot(data[:, 0], data[:, 6], 'k-o', mfc="None", label=r'$H^1$')
ax.legend(loc=0)
print("---------------------------------------------")
fig.savefig('.'+target_dir+'rom_T_h1norm.png')
np.savetxt('.'+target_dir+'rom_T_h10nor_theta_'+str(int(deg)+90)+'m.dat', data[:, 4])
np.savetxt('.'+target_dir+'rom_T_l2nor_theta_'+str(int(deg)+90)+'m.dat', data[:, 5])
np.savetxt('.'+target_dir+'rom_T_h1nor_theta_'+str(int(deg)+90)+'m.dat', data[:, 6])
print("---------------------------------------------")
