import re
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
from mor import ROM
from snapshot import Snapshot


def dual_norm():
    print('hello')
    return


def gtfpath(target_dir, pattern):
    import re
    import os
    fnames = []
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in files:
            if re.match(pattern, name):
                fnames.append(os.path.join(root, name))
    return fnames


def create_dict(filenames, pattern):
    import re
    file_dict = {}
    for fname in filenames:
        match = re.match(pattern, fname)
        if match:
            if match.groups()[0] not in file_dict:
                file_dict[match.groups()[0]] = []
            file_dict[match.groups()[0]].append(fname)

    return file_dict


def get_data(fnames, feature, info):
    if feature == 'romu':
        data = get_romu(fnames, feature, info)
    return data


def get_romu(fnames, feature, info):
    for element in fnames:
        z = re.match(r"^.*_(\d+)nb_.*", element)
        if z.groups()[0] == str(info['nb']):
            fname = element
    rom = ROM(fname, 'u')
    rom.get_coef()
    return rom


def plt_coef_in_t(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import setup
    from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
    plt_snap_minmax, plt_mean_in_t, add_std_in_t, plt_sample_mean_var
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
    from snapshot import Snapshot
    import os

    setup.text()

    field = rom.field

    sub_dir = os.path.join(tdir, 'rom'+field+'_'+str(rom.info['nb']))
    checkdir(sub_dir)

    # Create snapshot class
    # Need to modify the ops_path so that it does not depends on the position
    ops_path = './ops/'
    snap = Snapshot(ops_path, field)
    snap.coef(rom.info['K'])
    snap.outputs['t'] = np.linspace(500, 1000, rom.info['K'])
    umax, umin = snap.extrema()
    snap.mean()
    snap.var()

    K = rom.info['K']
    nb = rom.info['nb']
    T0 = rom.info['T0']
    print(f'Information K: {K}, N: {nb}, T0: {T0}')

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
    output = os.path.join(sub_dir, 'rom'+field+'_N'+str(rom.info['nb'])+'.png')
    fig.savefig(output)

    fig = plt_sample_mean_var(rom, snap)
    output = os.path.join(sub_dir, field+'a_'+field+'v_N'+str(nb)+'.png')
    fig.savefig(output)
    plt.show()


def checkdir(dir_path):
    import os

    isExist = os.path.exists(dir_path)
    if isExist:
        pass
    else:
        os.mkdir(dir_path)

    return