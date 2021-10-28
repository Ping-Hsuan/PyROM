def nu_1st2nd_momentum_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd=None, iffom=False):
    import numpy as np
    import matplotlib.pyplot as plt
    import operator
    import math
    from aux.cffdic import cffdic
    from aux.gptr import gptr
    from aux.create_dir import create_dir
    from setup.gtfpath import gtfpath
    from fig_helpers.set_ax import set_ax
    from fig_helpers.set_pltparams import set_pltparams
    from aux.rdatatoarray import rdatatoarray
    from fom_qois.fom_qois import fom_qois
    from save_helpers.mysave import mysave
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()
    T0 = int(T0)

    target_dir = './nu/'
    create_dir(target_dir)

    search_dir = '../'+model+'_info/nu'
    if mode == 'all':
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    else:
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_.*_h10_(?!.*-90|.*-80|.*-70).*$')

    ptr = gptr(model, N, T0, mode, fd)
    files_dict = cffdic(filenames, ptr, idx)

    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    rom_data = rdatatoarray(dict_final, 'nu_1st2nd', T0)
    solver = model.upper()

    if iffom:
        params = [int(i[0]) for i in dict_final]
        fom_data = fom_qois(params, 'nu_1st2nd')

    fig1, ax1 = plt.subplots(1, tight_layout=True)
    set_ax(ax1, 'mnu', tkey, tval)
    plot_params = set_pltparams('nu_1st2nd', solver, N, T0, fd)
    ax1.plot(rom_data[:, 0], rom_data[:, 1], **plot_params)
    if iffom:
        FOM_params = set_pltparams('FOM', solver, N, T0, fd)
        ax1.plot(fom_data[:, 0], fom_data[:, 1], **FOM_params)
    aidx = np.where(rom_data[:, 0] == aval[idx])
    ylim_exp = math.ceil(math.log10(min(rom_data[:, 1])))-1
    ax1.set_ylim([10**ylim_exp, None])
    ax1.plot(aval[idx], rom_data[aidx, 1], 'ro', label='Anchor point')
    ax1.legend(loc=1)

    fig2, ax2 = plt.subplots(1, tight_layout=True)
    set_ax(ax2, 'std_nu', tkey, tval)
    plot_params = set_pltparams('nu_1st2nd', solver, N, T0, fd)
    ax2.plot(rom_data[:, 0], rom_data[:, 2], **plot_params)
    if iffom:
        ax2.plot(fom_data[:, 0], fom_data[:, 2], **FOM_params)
    ax2.plot(aval[idx], rom_data[aidx, 2], 'ro', label='Anchor point')
    ax2.legend(loc=1)

    if iffom:
        mnu_relerr = abs(fom_data[:, 1]-rom_data[:, 1])/abs(
                fom_data[:, 1])
        stdnu_relerr = abs(fom_data[:, 2]-rom_data[:, 2])/abs(
                fom_data[:, 2])

        fig3, ax3 = plt.subplots(1, tight_layout=True)
        set_ax(ax3, 'mnurelerr', tkey, tval)
        plot_params = set_pltparams('mnurelerr', solver, N, T0, fd)
        ax3.semilogy(fom_data[:, 0], mnu_relerr, **plot_params)
        aidx = np.where(fom_data[:, 0] == aval[idx])
        ylim_exp = math.ceil(math.log10(min(mnu_relerr)))-1
        ax3.set_ylim([10**ylim_exp, None])
        ax3.semilogy(aval[idx], mnu_relerr[aidx], 'ro', label='Anchor point')
        ax3.legend(loc=1)

        header = tkey[0]+','+'mnurelerr'
        mysave(fig3, target_dir, np.stack([fom_data[:, 0], mnu_relerr], axis=-1), 'mnurelerr', header, N, fd)

    header = tkey[0]+','+'mnu'
    mysave(fig1, target_dir, np.stack([rom_data[:, 0], rom_data[:, 1]], axis=-1), 'mnu', header, N, fd)

    header = tkey[0]+','+'std_nu'
    mysave(fig2, target_dir, np.stack([rom_data[:, 0], rom_data[:, 2]], axis=-1), 'std_nu', header, N, fd)

if __name__ == '__main__':
    import sys
    nu_1st2nd_momentum_wparam(*sys.argv[1:])
