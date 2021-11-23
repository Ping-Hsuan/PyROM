import re
import sys
from reprod.mor import ROM
from snapshot import Snapshot
sys.path.append('/home/pht2/Developer/PyROM/code/plot_helpers/')
import setup_old


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


def plt_coef_in_t(rom, nb, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
    plt_snap_minmax, plt_mean_in_t, add_mean_in_t, add_std_in_t, plt_sample_mean_var
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
    from snapshot import Snapshot
    import os

    setup_old.style(1)
    setup_old.text()

    field = rom.field
    sub_dir = os.path.join(tdir, 'rom'+field+'_'+str(nb))
    checkdir(sub_dir)

    # Create snapshot class
    # Need to modify the ops_path so that it does not depends on the position
    ops_path = './ops/'
    snap = Snapshot(ops_path, field)
    snap.coef(rom.info['K'])
    ds = (rom.info['Tf']-rom.info['T0']+1)/rom.info['K']
    snap.outputs['t'] = np.linspace(rom.info['T0']-1+ds, rom.info['Tf'], rom.info['K'])
    umax, umin = snap.extrema()
    snap.mean()
    snap.var()

    K = rom.info['K']
    T0 = rom.info['T0']
    J0 = rom.info['J0']
    print(f'Information K: {K}, N: {nb}, T0: {T0}, J0: {J0}')

    # Plot rom coefficient
    if nb == 1:
        fig, ax = plt.subplots(1, squeeze=True, tight_layout=True)
        plt_romcoef_in_t(ax, 0, T0, rom)
        plt_snapcoef_in_t(ax, 0, T0, snap)
        plt_snap_minmax(ax, 0, T0, snap)
        add_mean_in_t(ax, 0, T0, snap, rom)
        add_std_in_t(ax, 0, T0, snap, rom)
        ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
                  borderaxespad=0, frameon=False)
    else:
        N_list = [0, int(nb/2)-1, nb-4]
        # Number of coefficients you want
        for N0 in N_list:
            num_coef_show = 4
            num_coef_show = min(num_coef_show, nb)
            fig, axs = plt.subplots(num_coef_show, sharex=True, squeeze=True, tight_layout=True)
            for n in range(num_coef_show):
                plt_romcoef_in_t(axs[n], n+N0, T0, rom)
                plt_snapcoef_in_t(axs[n], n+N0, T0, snap)
                plt_snap_minmax(axs[n], n+N0, T0, snap)
                add_mean_in_t(axs[n], n+N0, T0, snap, rom)
                add_std_in_t(axs[n], n+N0, T0, snap, rom)
                if n == 0:
                    ax = axs[n]
            ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.51), ncol=4,
                      borderaxespad=0, frameon=False)
            if rom.info['method'] == 'cp-rom':
                print(rom.fnames['rom'+field])
                s1 = 'rom'+field+'_N'+str(nb)+'_'+str(N0)+'.png'
            else:
                s1 = 'rom'+field+'_N'+str(nb)+'_'+str(N0)+'.png'
            output = os.path.join(sub_dir, s1)
            fig.savefig(output)

    fig = plt_sample_mean_var(rom, snap, nb)
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


def plt_erri_wN(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from reprod.fig_helpers import set_ax
    from reprod.fig_helpers import set_pltparams
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, 'dual_norm')
    checkdir(sub_dir)

    # Create filename
    fname1 = 'dual_norm'
    data = np.column_stack((rom.nbs, rom.erris))
    output = os.path.join(sub_dir, fname1)
    if rom.info['method'] == 'l-rom':
        output += '_'+rom.info['perc']
    elif rom.info['method'] == 'l-rom-df':
        output += '_'+rom.info['fwidth']
    output += '.csv'
    np.savetxt(output, data, delimiter=',', header='N, dual_norm', comments="")

    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = set_pltparams('dual_norm', rom)
    ax.semilogy(rom.nbs, rom.erris, **plot_params)
    set_ax(ax, rom, 'dual_norm')
    plt.legend()

    output = os.path.join(sub_dir, fname1)
    fig.savefig(output)
    plt.close(fig)

    return


def plt_mrelerr_wN(rom, tdir, feature):
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import math
    from reprod.fig_helpers import set_ax
    from reprod.fig_helpers import set_pltparams
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, feature)
    checkdir(sub_dir)

    plot_params1 = set_pltparams('rom_'+feature, rom)
    plot_params2 = set_pltparams('proj_'+feature, rom)

    fig1, ax1 = plt.subplots(1, tight_layout=True)
    set_ax(ax1, rom, 'rom_'+feature)
    ax1.semilogy(rom.nbs, rom.rom_relerr, **plot_params1)
    ylim_exp = math.ceil(math.log10(min(rom.rom_relerr)))-1
#   ax1.set_ylim([10**ylim_exp, 1])
    ax1.set_ylim([1e-2, 1])
    ax1.legend(loc=0, ncol=1)

    fig2, ax2 = plt.subplots(1, tight_layout=True)
    set_ax(ax2, rom, 'proj_'+feature)
    ax2.semilogy(rom.nbs, rom.proj_relerr, **plot_params2)
    ylim_exp = math.ceil(math.log10(min(rom.proj_relerr)))-1
    ax2.set_ylim([10**ylim_exp, 1])
    ax2.legend(loc=0, ncol=1)

    # Create filename
    fname1 = feature
    fname2 = feature+'_rom'
    fname3 = feature+'_proj'
    data = np.column_stack((rom.nbs, rom.rom_relerr, rom.proj_relerr))
    output = os.path.join(sub_dir, fname1)
    if rom.info['method'] == 'l-rom':
        output += '_'+rom.info['perc']
    elif rom.info['method'] == 'l-rom-df':
        output += '_'+rom.info['fwidth']
    output += '.csv'
    np.savetxt(output, data, delimiter=',', header='N, rom_mrelerr, proj_mrelerr', comments="")

    output = os.path.join(sub_dir, fname2)
    fig1.savefig(output)
    plt.close(fig1)
    output = os.path.join(sub_dir, fname3)
    fig2.savefig(output)
    plt.close(fig2)
    return


def reader(fname):
    with open(fname, 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[-1] for x in list_of_words]
    return data


def plt_mabserr_wN(rom, tdir, feature):
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from reprod.fig_helpers import set_ax
    from reprod.fig_helpers import set_pltparams
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()

    # Create subdirectory
    sub_dir = os.path.join(tdir, feature)
    checkdir(sub_dir)

    plot_params1 = set_pltparams('rom_'+feature, rom)
    plot_params2 = set_pltparams('proj_'+feature, rom)

    fig1, ax1 = plt.subplots(1, tight_layout=True)
    set_ax(ax1, rom, 'rom_'+feature)
    ax1.plot(rom.nbs, rom.rom_abserr, **plot_params1)
    ax1.legend(loc=0, ncol=1)

    fig2, ax2 = plt.subplots(1, tight_layout=True)
    set_ax(ax2, rom, 'proj_'+feature)
    ax2.plot(rom.nbs, rom.proj_abserr, **plot_params2)
    ax2.legend(loc=0, ncol=1)

    # Create filename
    fname1 = feature
    fname2 = feature+'_rom'
    fname3 = feature+'_proj'
    data = np.column_stack((rom.nbs, rom.rom_abserr, rom.proj_abserr))
    output = os.path.join(sub_dir, fname1)
    if rom.info['method'] == 'l-rom':
        output += '_'+rom.info['perc']
    elif rom.info['method'] == 'l-rom-df':
        output += '_'+rom.info['fwidth']
    output += '.csv'
    np.savetxt(output, data, delimiter=',', header='N, rom_mabserr, proj_mabserr', comments="")

    output = os.path.join(sub_dir, fname2)
    fig1.savefig(output)
    plt.close(fig1)
    output = os.path.join(sub_dir, fname3)
    fig2.savefig(output)
    plt.close(fig2)
    return


def plt_rom_norm_w_N(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    setup_old.style(1)
    setup_old.text()

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


def plt_tke_in_t(rom, nb, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
    plt_snap_minmax, plt_mean_in_t, add_std_in_t, plt_sample_mean_var
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
    from snapshot import Snapshot
    import os

    setup_old.style(1)
    setup_old.text()

    sub_dir = os.path.join(tdir, 'tke')
    checkdir(sub_dir)

    K = rom.info['K']
    T0 = rom.info['T0']
    J0 = rom.info['J0']
    print(f'Information K: {K}, N: {nb}, T0: {T0}, J0: {J0}')

    rom_params = {'c': 'b', 'mfc': 'None'}
    rom_params['label'] = rom.info['method'].upper()
    xlabel = r'$t$'
    ylabel = 'tke'+r'$(t)$'

    fig, ax = plt.subplots(1, squeeze=True, tight_layout=True)
    ax.set(ylabel=ylabel, xlabel=xlabel)
    ax.semilogy(rom.tke[str(nb)]['t'], rom.tke[str(nb)]['tke'],
            **rom_params)
    ax.legend(loc='upper left', bbox_to_anchor= (0.0, 1.11), ncol=4,
              borderaxespad=0, frameon=False)
    output = os.path.join(sub_dir, 'tke_N'+str(nb)+'.png')
    fig.savefig(output)
    plt.close(fig)


def plt_mtke(rom, tdir):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    from myplot import plt_romcoef_in_t, plt_snapcoef_in_t, \
    plt_snap_minmax, plt_mean_in_t, add_std_in_t, plt_sample_mean_var
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/postprocessing/')
    from snapshot import Snapshot
    import os

    setup_old.style(1)
    setup_old.text()

    sub_dir = os.path.join(tdir, 'mtke')
    checkdir(sub_dir)

    rom_params = {'c': 'b','marker':'o'}
    rom_params['label'] = rom.info['method'].upper()
    xlabel = r'$N$'
    ylabel = r'$\langle TKE \rangle_s$'

    fig, ax = plt.subplots(1, squeeze=True, tight_layout=True)
    ax.set(ylabel=ylabel, xlabel=xlabel)
    ax.semilogy(rom.nbs, rom.mtke, **rom_params)
    mtke_fom = np.loadtxt('../qoi/tmtke')
    fom_params = {'c': 'k', 'marker': 'o','label':'FOM'}
    ax.semilogy(rom.nbs, mtke_fom*np.ones(len(rom.nbs)), **fom_params)
    ax.legend(loc=0)
    output = os.path.join(sub_dir, 'mtke.png')
    fig.savefig(output)
    plt.close(fig)
