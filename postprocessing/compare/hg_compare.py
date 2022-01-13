def hg_compare(argv):
    import numpy as np
    import matplotlib.pyplot as plt
    import re
    import os
    import sys
    import pandas as pd
    from aux.helpers import find_files
    from figsetup.style import style
    from figsetup.text import text
    from figsetup.color import color
    from aux.create_dir import create_dir
    from compare.helpers import set_ax

    style(1)
    markers = ['o', 'v', '*', 'x']
    text()

    print("This is the name of the program:", sys.argv[0])
    print("Argument List:", str(sys.argv))
    os.chdir(str(sys.argv[1]))
    feature = str(sys.argv[2])
    ncand = str(sys.argv[3])
    itr = str(sys.argv[4])
    fname = feature+'_'+ncand+'_itr'+itr+'.csv'
    fnames = find_files(fname, './')

    ctr = 0
    fig, ax = plt.subplots(1, tight_layout=True)
    for f in fnames:
        data = pd.read_csv(f)
        ptr = re.split('/', f)
        for i in ptr:
            if 'online' in i:
                model = i.split('_')[1]
        ax.plot(data.iloc[:, 0], data.iloc[:, 1], 'b-', marker=markers[ctr], mfc='None', label=model)
        ctr += 1
    ax.legend(loc=0)
    set_ax(ax, feature, itr)

    if feature == 'nu_m':
        fom_mnu_p = []
        p = []
        fname = 'nus_mom.csv'
        fnames = find_files(fname, '../')
        for f in fnames:
            par = float(re.split('[/]',f)[1].split('_')[1])
            if par <= max(data.iloc[:, 0]) and par >= min(data.iloc[:, 0]):
                dd = pd.read_csv(f)
                p.append(par)
                fom_mnu_p.append(dd['mean'])
        p, fom_mnu_p = zip(*sorted(zip(p, fom_mnu_p)))
        ax.plot(p, fom_mnu_p, 'ko', label='FOM')
        ax.legend(loc=0)
    elif feature == 'nu_std':
        fom_nustd_p = []
        p = []
        fname = 'nus_mom.csv'
        fnames = find_files(fname, '../')
        for f in fnames:
            par = float(re.split('[/]',f)[1].split('_')[1])
            if par <= max(data.iloc[:, 0]) and par >= min(data.iloc[:, 0]):
                dd = pd.read_csv(f)
                p.append(par)
                fom_nustd_p.append(dd[' std'])
        p, fom_nustd_p = zip(*sorted(zip(p, fom_nustd_p)))
        ax.plot(p, fom_nustd_p, 'ko', label='FOM')
        ax.legend(loc=0)
    elif feature == 'mtke':
        list1 = []
        p = []
        fname = 'tmtke'
        fnames = find_files(fname, '../')
        for f in fnames:
            par = float(re.split('[/]',f)[1].split('_')[1])
            if par <= max(data.iloc[:, 0]) and par >= min(data.iloc[:, 0]):
                dd = np.loadtxt(f)
                p.append(par)
                list1.append(dd)
        p, fom_nustd_p = zip(*sorted(zip(p, list1)))
        ax.plot(p, list1, 'ko', label='FOM')
        ax.legend(loc=0)
    elif feature == 'mtfluc':
        list1 = []
        p = []
        fname = 'tmtfluc'
        fnames = find_files(fname, '../')
        for f in fnames:
            par = float(re.split('[/]',f)[1].split('_')[1])
            if par <= max(data.iloc[:, 0]) and par >= min(data.iloc[:, 0]):
                dd = np.loadtxt(f)
                p.append(par)
                list1.append(dd)
        p, fom_nustd_p = zip(*sorted(zip(p, list1)))
        ax.plot(p, list1, 'ko', label='FOM')
        ax.legend(loc=0)
    elif feature == 'rom_fldrelerr':
        fname = 'proj_fldrelerr'+'_'+ncand+'_itr'+itr+'.csv'
        fnames = find_files(fname, './')
        ctr = 0
        for f in fnames:
            data = pd.read_csv(f)
            ptr = re.split('/', f)
            for i in ptr:
                if 'online' in i:
                    model = i.split('_')[1]
            ax.plot(data.iloc[:, 0], data.iloc[:, 1], 'b--', marker=markers[ctr], mfc='None', label=model+' projection')
            ctr += 1
        ax.legend(loc=0)
        ax.set_yscale('log')
    tdir = './hg_compare/'
    create_dir(tdir)
    fig.savefig(tdir+feature+'_'+ncand+'_'+itr+'.png')

    return


if __name__ == '__main__':
    import sys
    hg_compare(sys.argv[1:])
