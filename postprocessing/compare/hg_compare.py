def hg_compare(argv):
    import numpy as np
    import matplotlib.pyplot as plt
    import re
    import os
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import mypostpro
    import reader
    import pandas as pd
    from figsetup.style import style
    from figsetup.text import text
    from figsetup.color import color

    style(1)
    colors = color(0)
    text()

    print("This is the name of the program:", sys.argv[0])
    print("Argument List:", str(sys.argv))
    os.chdir(str(sys.argv[1]))
    itr = str(sys.argv[2])

    if len(sys.argv) >= 4:
        pt = '_sc_'+str(sys.argv[3])
    else:
        pt = ''
    fname = 'rom_fldrelerr_2_itr1.csv'
    fnames = reader.find_files(fname, './')
    print(fnames)

    color_ctr = 0
    fig, ax = plt.subplots(1, tight_layout=True)
    for f in fnames:
        if itr == 1:
            title = str(itr)+'st iteration'
        elif itr == 2:
            title = str(itr)+'nd iteration'
        elif itr == 3:
            title = str(itr)+'rd iteration'
        else:
            title = str(itr)+'th iteration'
        data = pd.read_csv(f)
        ptr = re.split('/', f)
        for i in ptr:
            if 'online' in i:
                model = i.split('_')[1]
        ax.plot(data.iloc[:, 0], data.iloc[:, 1], '-o', color=colors[color_ctr], label=model)
        color_ctr += 1
    ax.legend(loc=0)
    plt.show()
    1/o
    for path1 in paths:
        sp1 = (path1.split('/'))
        print(sp1)
        for element in sp1:
            z = re.match(r"^.*_(.*)rom_online$", element)
            if z:
                if (z.groups()[0]) == 'l':
                    lb = 'Leray ROM'
                elif (z.groups()[0]) == '':
                    lb = 'Galerkin ROM'
                elif (z.groups()[0]) == 'c':
                    lb = 'Constrained ROM'
        nu_m = np.loadtxt(path1)
        ax.plot(P_test, nu_m, '-o', color=colors[color_ctr], label=lb)
        color_ctr += 1


    fom_m_list = []
    fom_std_list = []
    for i, test in enumerate(P_test):
        filename = '../../fom_nuss/nuss_fom_'+str(test)
        data = mypostpro.read_nuss(filename)
        data[:, 2] = data[:, 2]/40
        idx1 = mypostpro.find_nearest(data[:, 0], 0)
        idx2 = mypostpro.find_nearest(data[:, 0], 1000)
        nuss_fom = data[idx1:idx2, :]
        avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
        fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
        fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
        fom_std = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)

        fom_m_list.append(fom_mean)
        fom_std_list.append(fom_std)

    ax.plot(P_test, fom_m_list, 'k-o', label='FOM')
    ax.legend(loc=0)
    ax.set(xlabel=r'$\theta_g$', xticks=np.linspace(0, 180, 19, dtype=int),
           ylabel='Mean Nu', ylim=[1, 4], title=title)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    fig.savefig('./nu_m_2'+pt+'_compare_itr'+itr+'.png')

    color_ctr = 0
    fig, ax = plt.subplots(1, tight_layout=True)
    for path in paths1:
        sp1 = (path.split('/'))
        print(sp1)
        for element in sp1:
            z = re.match(r"^.*_(.*)rom_online$", element)
            if z:
                if (z.groups()[0]) == 'l':
                    lb = 'Leray ROM'
                elif (z.groups()[0]) == '':
                    lb = 'Galerkin ROM'
                elif (z.groups()[0]) == 'c':
                    lb = 'Constrained ROM'
        nu_std = np.loadtxt(path)

        ax.plot(P_test, nu_std, '-o', color=colors[color_ctr], label=lb)

        color_ctr += 1

    ax.plot(P_test, fom_std_list, 'k-o', label='FOM')
    ax.legend(loc=0)
    ax.set(xlabel=r'$\theta_g$', xticks=np.linspace(0, 180, 19, dtype=int),
           ylabel='Std(Nu)', ylim=[0, 0.15], title=title)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    fig.savefig('./nu_std_2'+pt+'_compare_itr'+itr+'.png')

    color_ctr = 0
    fig, ax = plt.subplots(1, tight_layout=True)
    for path in paths2:
        sp1 = (path.split('/'))
        print(sp1)
        for element in sp1:
            z = re.match(r"^.*_(.*)rom_online$", element)
            if z:
                if (z.groups()[0]) == 'l':
                    lb = 'Leray ROM'
                elif (z.groups()[0]) == '':
                    lb = 'Galerkin ROM'
                elif (z.groups()[0]) == 'c':
                    lb = 'Constrained ROM'
        nu_merr = np.loadtxt(path)

        ax.semilogy(P_test, nu_merr, '-o', color=colors[color_ctr], label=lb)
        color_ctr += 1

    ax.legend(loc=0)
    ax.set(xlabel=r'$\theta_g$', xticks=np.linspace(0, 180, 19, dtype=int),
           ylabel='Relatvive error in mean Nu', ylim=[1e-4, 1e1], title=title)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    fig.savefig('./nu_merr_2'+pt+'_compare_itr'+itr+'.png')

    color_ctr = 0
    fig, ax = plt.subplots(1, tight_layout=True)
    for path in paths3:
        sp1 = (path.split('/'))
        print(sp1)
        for element in sp1:
            z = re.match(r"^.*_(.*)rom_online$", element)
            if z:
                if (z.groups()[0]) == 'l':
                    lb = 'Leray ROM'
                elif (z.groups()[0]) == '':
                    lb = 'Galerkin ROM'
                elif (z.groups()[0]) == 'c':
                    lb = 'Constrained ROM'
        rom_fldrelerr = np.loadtxt(path)

        ax.plot(P_test, rom_fldrelerr, '-o', color=colors[color_ctr], label=lb)
        color_ctr += 1

    ax.legend(loc=0)
    ax.set(xlabel=r'$\frac{\|u - \widehat{u}\|_{H^1}}{\|u\|_{H^1}}$', xticks=np.linspace(0, 180, 19, dtype=int),
           ylabel='Relatvive error in mean Nu', ylim=[0, 1], title=title)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    fig.savefig('./rom_fldrelerr_2'+pt+'_compare_itr'+itr+'.png')

    return


if __name__ == '__main__':
    import sys
    hg_compare(sys.argv[1:])
