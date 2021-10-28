def temp_mrelerr_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import operator
    from aux.cffdic import cffdic
    from aux.gptr import gptr
    from aux.create_dir import create_dir
    from setup.gtfpath import gtfpath
    from fig_helpers.set_ax import set_ax
    from fig_helpers.set_pltparams import set_pltparams
    from aux.rdatatoarray import rdatatoarray
    from save_helpers.mysave import mysave
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()
    T0 = int(T0)

    target_dir = './temp_mrelerr/'
    create_dir(target_dir)

    search_dir = '../'+model+'_info/temp_mrelerr'
    if mode == 'all':
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    else:
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_.*_h10_(?!.*-90|.*-80|.*-70).*$')

    ptr = gptr(model, N, T0, mode, fd)
    files_dict = cffdic(filenames, ptr, idx)

    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    data = rdatatoarray(dict_final, 'mrelerr')

    solver = model.upper()
    plot_params1 = set_pltparams('rom_mrelerr', solver, N, T0, fd)
    plot_params2 = set_pltparams('proj_mrelerr', solver, N, T0, fd)

    fig, ax = plt.subplots(1, tight_layout=True)
    set_ax(ax, 'temp_mrelerr', tkey, tval)

    ax.plot(data[:, 0], data[:, 1], **plot_params1)
    ax.plot(data[:, 0], data[:, 2], **plot_params2)

    aidx = np.where(data[:, 0] == aval[idx])
    ax.plot(aval[idx], data[aidx, 1], 'ro', label='Anchor point')

    ax.legend(loc=0, ncol=1)

    header = tkey[0]+','+'rom_mrelerr'+','+'proj_mrelerr'
    mysave(fig, target_dir, data, 'mrelerr', header, N, fd)


if __name__ == '__main__':
    import sys
    temp_mrelerr_wparam(*sys.argv[1:])
