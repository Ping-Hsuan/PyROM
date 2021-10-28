def dual_norm_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import operator
    import math
    from setup.gtfpath import gtfpath
    from aux.create_dir import create_dir
    from aux.cffdic import cffdic
    from aux.rdatatoarray import rdatatoarray
    from aux.gptr import gptr
    from figsetup.style import style
    from figsetup.text import text
    from fig_helpers.set_ax import set_ax
    from fig_helpers.set_pltparams import set_pltparams
    from save_helpers.mysave import mysave

    style(1)
    text()

    T0 = int(T0)
    print(model, N, T0, mode, fd)

    target_dir = './dual_norm/'
    create_dir(target_dir)

    search_dir = '../'+model+'_info/dual_norm'
    if mode == 'all':
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    else:
        root, filenames = gtfpath(search_dir, '^.*_'+N+'nb_*_h10_(?!.*-90|.*-80|.*-70).*$')
    ptr = gptr(model, N, T0, mode, fd)
    files_dict = cffdic(filenames, ptr, idx)
    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))
    
    data = rdatatoarray(dict_final, 'dual_norm')

    solver = model.upper()
    plot_params = set_pltparams('dual_norm', solver, N, T0, fd)

    fig, ax = plt.subplots(1, tight_layout=True)
    set_ax(ax, 'dual_norm', tkey, tval)
    ax.plot(data[:, 0], data[:, 1], **plot_params)
    aidx = np.where(data[:, 0] == aval[idx])
    ylim_exp = math.ceil(math.log10(min(data[:, 1])))-1
    ax.set_ylim([10**ylim_exp, None])
    ax.plot(aval[idx], data[aidx, 1], 'ro', label='Anchor point')
    ax.legend(loc=0)
    #f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
    #g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    #plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
    #plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    
    header = tkey[0]+','+'dual_norm'
    mysave(fig, target_dir, data, 'dual_norm', header, N, fd)

if __name__ == '__main__':
    import sys
    dual_norm_wparam(sys.argv[1:])
