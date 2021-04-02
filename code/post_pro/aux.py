import re
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
from mor import ROM
from snapshot import Snapshot
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup


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


def plt_coef_in_t(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
    plt_snap_minmax, plt_mean_in_t, add_std_in_t, plt_sample_mean_var
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
    from snapshot import Snapshot
    import os

    setup.style(1)
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


def checkdir(dir_path):
    import os

    isExist = os.path.exists(dir_path)
    if isExist:
        pass
    else:
        os.mkdir(dir_path)

    return


def plt_erri_w_N(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    setup.style(1)
    setup.text()

    solver = rom.info['method'].upper()

    # Create subdirectory
    sub_dir = os.path.join(tdir, 'dual_norm')
    checkdir(sub_dir)

    # Create filename
    fname1 = 'dual_norm'
    fname2 = 'N_list'
    fname3 = 'erri'
    for key, value in rom.info['parameters'].items():
        fname1 += '_'+str(key)+'_'+str(value)
        fname2 += '_'+str(key)+'_'+str(value)
        fname3 += '_'+str(key)+'_'+str(value)

    fname2 += '.dat'
    fname3 += '.dat'

    fig, ax = plt.subplots(1, tight_layout=True)
    # Create label
    lb = solver + ' with '
    anc_lb = ''
    for key, value in rom.info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': lb+r'$'+anc_lb+'$'}

    ax.set(ylabel=r'$\triangle('+anc_lb+')$', xlabel=r'$N$',
           ylim=[10**np.floor(np.log10(min(rom.erris))), 1], xlim=[1, max(rom.nbs)])
    ax.semilogy(rom.nbs, rom.erris, **plot_params)
    plt.legend()

    output = os.path.join(sub_dir, fname1)
    fig.savefig(output)

    output = os.path.join(sub_dir, fname2)
    np.savetxt(output, rom.nbs)
    output = os.path.join(sub_dir, fname3)
    np.savetxt(output, rom.erris)
    return


def plt_mrelerr_w_N(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    setup.style(1)
    setup.text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, 'mrelerr')
    checkdir(sub_dir)

    solver = rom.info['method'].upper()
    plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                    'label': solver}
    plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                    'label': 'Projection'}
    # Create title
    title = 'Relative error in the mean flow at '
    anc_lb = ''
    for key, value in rom.info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(xlabel=r'$N$', ylabel=r'$\frac{\|u - \tilde{u}\|_{H^1}}{\|u\|_{H^1}}$',
           xlim=[0, max(rom.nbs)], title=title+'$'+anc_lb+'$')

    ax.semilogy(rom.nbs, rom.rom_relerr, **plot_params1)
    ax.semilogy(rom.nbs, rom.proj_relerr, **plot_params2)
    ax.legend(loc=0, ncol=1)

    # Create filename
    fname1 = 'mrelerr'
    fname2 = 'N_list'
    fname3 = 'rom_mrelerr'
    fname4 = 'proj_mrelerr'
    for key, value in rom.info['parameters'].items():
        fname1 += '_'+str(key)+'_'+str(value)
        fname2 += '_'+str(key)+'_'+str(value)
        fname3 += '_'+str(key)+'_'+str(value)
        fname4 += '_'+str(key)+'_'+str(value)

    fname2 += '.dat'
    fname3 += '.dat'
    fname4 += '.dat'

    output = os.path.join(sub_dir, fname1)
    fig.savefig(output)
    output = os.path.join(sub_dir, fname2)
    np.savetxt(output, rom.nbs)
    output = os.path.join(sub_dir, fname3)
    np.savetxt(output, rom.rom_relerr)
    output = os.path.join(sub_dir, fname4)
    np.savetxt(output, rom.proj_relerr)
    return


def reader(fname):
    with open(fname, 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[-1] for x in list_of_words]
    return data


def plt_mabserr_w_N(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    setup.style(1)
    setup.text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, 'mabserr')
    checkdir(sub_dir)

    solver = rom.info['method'].upper()
    plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                    'label': solver}
    plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                    'label': 'Projection'}
    # Create title
    title = 'Absolute error in the mean flow at '
    anc_lb = ''
    for key, value in rom.info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(xlabel=r'$N$', ylabel=r'$\|u - \tilde{u}\|_{H^1}$',
           xlim=[0, max(rom.nbs)], title=title+'$'+anc_lb+'$')

    ax.semilogy(rom.nbs, rom.rom_abserr, **plot_params1)
    ax.semilogy(rom.nbs, rom.proj_abserr, **plot_params2)
    ax.legend(loc=0, ncol=1)

    # Create filename
    fname1 = 'mabserr'
    fname2 = 'N_list'
    fname3 = 'rom_mabserr'
    fname4 = 'proj_mabserr'
    for key, value in rom.info['parameters'].items():
        fname1 += '_'+str(key)+'_'+str(value)
        fname2 += '_'+str(key)+'_'+str(value)
        fname3 += '_'+str(key)+'_'+str(value)
        fname4 += '_'+str(key)+'_'+str(value)

    fname2 += '.dat'
    fname3 += '.dat'
    fname4 += '.dat'

    output = os.path.join(sub_dir, fname1)
    fig.savefig(output)
    output = os.path.join(sub_dir, fname2)
    np.savetxt(output, rom.nbs)
    output = os.path.join(sub_dir, fname3)
    np.savetxt(output, rom.rom_relerr)
    output = os.path.join(sub_dir, fname4)
    np.savetxt(output, rom.proj_relerr)
    return


def plt_rom_norm_w_N(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    setup.style(1)
    setup.text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, 'rom_norm')
    checkdir(sub_dir)

    solver = rom.info['method'].upper()
    # Create title
    title = 'Norm of the predictied mean flow by '+solver+' at '
    anc_lb = ''
    for key, value in rom.info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)

    # Data transform
    data = np.column_stack((rom.nbs, rom.rom_norm))
    data = data[data[:, 0].argsort()]
    # fix the h1 norm
    for j in range(data.shape[0]):
        if (rom.info['ifrom(1)']):
            idx1 = 1
            data[j, idx1+2] = np.sqrt(data[j, idx1]**2+data[j, idx1+1]**2)
        if (rom.info['ifrom(2)']):
            idx2 = 4
            data[j, idx2+2] = np.sqrt(data[j, idx2]**2+data[j, idx2+1]**2)
        if (rom.info['ifrom(1)'] and rom.info['ifrom(2)']):
            idx3 = 7
            data[j, idx3+2] = np.sqrt(data[j, idx3]**2+data[j, idx3+1]**2)

    if (rom.info['ifrom(1)']):
        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(xlabel=r'$N$', ylabel=r'$\|\tilde{u}\|_{*}$',
               xlim=[0, max(rom.nbs)], title=title+'$'+anc_lb+'$')
        ax.plot(data[:, 0], data[:, idx1], 'b-o', mfc="None", label=r'$H^1_0$')
        ax.plot(data[:, 0], data[:, idx1+1], 'r-o', mfc="None", label=r'$L^2$')
        ax.plot(data[:, 0], data[:, idx1+2], 'k-o', mfc="None", label=r'$H^1$')
        ax.legend(loc=0)
        fname1 = 'rom_u_norm'
        fname2 = 'N_list'
        fname3 = 'rom_u_h10'
        fname4 = 'rom_u_l2'
        fname5 = 'rom_u_h1'
        for key, value in rom.info['parameters'].items():
            fname1 += '_'+str(key)+'_'+str(value)
            fname2 += '_'+str(key)+'_'+str(value)
            fname3 += '_'+str(key)+'_'+str(value)
            fname4 += '_'+str(key)+'_'+str(value)
            fname5 += '_'+str(key)+'_'+str(value)

        fname2 += '.dat'
        fname3 += '.dat'
        fname4 += '.dat'
        fname5 += '.dat'
        output = os.path.join(sub_dir, fname1)
        fig.savefig(output)
        output = os.path.join(sub_dir, fname2)
        np.savetxt(output, data[:, 0])
        output = os.path.join(sub_dir, fname3)
        np.savetxt(output, data[:, idx1])
        output = os.path.join(sub_dir, fname4)
        np.savetxt(output, data[:, idx1+1])
        output = os.path.join(sub_dir, fname5)
        np.savetxt(output, data[:, idx1+2])

    if (rom.info['ifrom(2)']):
        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(ylabel=r'$\||T\|_{*}$', xlabel=r'$N$', title=title)
        ax.plot(data[:, 0], data[:, idx2], 'b-o', mfc="None", label=r'$H^1_0$')
        ax.plot(data[:, 0], data[:, idx2+1], 'r-o', mfc="None", label=r'$L^2$')
        ax.plot(data[:, 0], data[:, idx2+2], 'k-o', mfc="None", label=r'$H^1$')
        ax.legend(loc=0)
        fname1 = 'rom_T_norm'
        fname2 = 'N_list'
        fname3 = 'rom_T_h10'
        fname4 = 'rom_T_l2'
        fname5 = 'rom_T_h1'
        for key, value in rom.info['parameters'].items():
            fname1 += '_'+str(key)+'_'+str(value)
            fname2 += '_'+str(key)+'_'+str(value)
            fname3 += '_'+str(key)+'_'+str(value)
            fname4 += '_'+str(key)+'_'+str(value)
            fname5 += '_'+str(key)+'_'+str(value)

        fname2 += '.dat'
        fname3 += '.dat'
        fname4 += '.dat'
        fname5 += '.dat'
        output = os.path.join(sub_dir, fname1)
        fig.savefig(output)
        output = os.path.join(sub_dir, fname2)
        np.savetxt(output, data[:, 0])
        output = os.path.join(sub_dir, fname3)
        np.savetxt(output, data[:, idx2])
        output = os.path.join(sub_dir, fname4)
        np.savetxt(output, data[:, idx2+1])
        output = os.path.join(sub_dir, fname5)
        np.savetxt(output, data[:, idx2+2])

    if (rom.info['ifrom(1)'] and rom.info['ifrom(2)']):
        fig, ax = plt.subplots(1, tight_layout=True)
        ax.set(ylabel=r'$\||(u, T)\|_{*}$', xlabel=r'$N$', title=title)
        ax.plot(data[:, 0], data[:, idx3], 'b-o', mfc="None", label=r'$H^1_0$')
        ax.plot(data[:, 0], data[:, idx3+1], 'r-o', mfc="None", label=r'$L^2$')
        ax.plot(data[:, 0], data[:, idx3+2], 'k-o', mfc="None", label=r'$H^1$')
        ax.legend(loc=0)
        fname1 = 'rom_norm'
        fname2 = 'N_list'
        fname3 = 'rom_h10'
        fname4 = 'rom_l2'
        fname5 = 'rom_h1'
        for key, value in rom.info['parameters'].items():
            fname1 += '_'+str(key)+'_'+str(value)
            fname2 += '_'+str(key)+'_'+str(value)
            fname3 += '_'+str(key)+'_'+str(value)
            fname4 += '_'+str(key)+'_'+str(value)
            fname5 += '_'+str(key)+'_'+str(value)

        fname2 += '.dat'
        fname3 += '.dat'
        fname4 += '.dat'
        fname5 += '.dat'

        output = os.path.join(sub_dir, fname1)
        fig.savefig(output)
        output = os.path.join(sub_dir, fname2)
        np.savetxt(output, data[:, 0])
        output = os.path.join(sub_dir, fname3)
        np.savetxt(output, data[:, idx3])
        output = os.path.join(sub_dir, fname4)
        np.savetxt(output, data[:, idx3+1])
        output = os.path.join(sub_dir, fname5)
        np.savetxt(output, data[:, idx3+2])
    return
