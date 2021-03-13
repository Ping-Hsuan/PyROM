import numpy as np
import matplotlib.pyplot as plt
import re
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
plt_snap_minmax, plt_mean_in_t, add_std_in_t, plt_sample_mean_var
import mypostpro
from mor import ROM
from snapshot import Snapshot

colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
deg = str(int(sys.argv[3])-90)
N = str((sys.argv[4]))
print("---------------------------------------------")

field = 't'
target_dir = '/rom'+field+'_'+N
setup.checkdir(target_dir)
ops_path = '../ops/'

search_dir = './'+model+'_info/rom'+field
anchor = setup.find_anchor()
root, filenames = setup.gtfpath(search_dir,
                                '^.*_(.*)rom_.*_'+str(int(anchor-90)))
color_ctr = 0
tpath = root+'/'

for element in filenames:
    z = re.match(r"^.*_(\d+)nb_.*", element)
    if z.groups()[0] == N:
        fname = element

# Create ROM class with field specified
rom = ROM(fname, field)
rom.get_coef()
K = rom.info['K']
nb = rom.info['nb']
if rom.info['init'] == 'zero':
    T0 = mypostpro.find_nearest(rom.outputs['t'][0, :], 501)
elif rom.info['init'] == 'ic':
    T0 = 0
    rom.outputs['t'] += 500
rom.coef_mean(T0)
rom.coef_variance(T0)
print(rom.outputs['Ta'])
print(rom.outputs['Tv'])

# Create snapshot class
snap = Snapshot(ops_path, field)
fomu = snap.coef(rom.info['K'])
snap.outputs['t'] = np.linspace(500, 1000, rom.info['K'])
umax, umin = snap.extrema()
ul_bounds = [umax, umin]
uas = snap.mean()
uvs = snap.var()

print(f'Information K: {K}, N: {nb}, T0: {T0}')

dir_path = './rom'+field+'_'+N+'/'

# Plot rom coefficient
if rom.info['nb'] == 1:
    fig, ax = plt.subplots(1, squeeze=True, tight_layout=True)
    plt_romcoef_in_t(ax, 0, T0, rom)
    plt_snapcoef_in_t(ax, 0, T0, snap)
    plt_snap_minmax(ax, 0, T0, snap)
    plt_mean_in_t(ax, 0, T0, snap, rom)
    add_std_in_t(ax, 0, T0, snap, rom)
    ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
              borderaxespad=0, frameon=False)
else:
    # Number of coefficients you want
    num_coef_show = 4
    num_coef_show = min(num_coef_show, nb)
    fig, axs = plt.subplots(num_coef_show, sharex=True, squeeze=True, tight_layout=True)
    for n in range(num_coef_show):
        plt_romcoef_in_t(axs[n], n, T0, rom)
        plt_snapcoef_in_t(axs[n], n, T0, snap)
        plt_snap_minmax(axs[n], n, T0, snap)
        plt_mean_in_t(axs[n], n, T0, snap, rom)
        add_std_in_t(axs[n], n, T0, snap, rom)
        if n == 0:
            ax = axs[n]
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.51), ncol=4,
              borderaxespad=0, frameon=False)
fig.savefig(dir_path+'rom'+field+'_N'+N+'.png')

fig = plt_sample_mean_var(rom, snap)
fig.savefig(dir_path+field+'a_'+field+'v_N'+str(nb)+'.png')
plt.show()
