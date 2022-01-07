def conv_compare(argv):
    import yaml
    import os
    import re
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text
    from aux.create_dir import create_dir
    sys.path.append('/home/pht2/Developer/PyROM/code/plot_helpers/')
    import reader

    style(1)
    text()
    models = []
    for i in range(len(argv)-1):
        models.append(argv[i])
    feature = argv[-1]

    fig, ax = plt.subplots(1, tight_layout=True)
    for model in models:
        dir1 = model+'_reproduction'
        with open('reproduction.yaml') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in info['parameters'].items():
            al = '_'.join([str(key), str(value)])
            dir1 = '_'.join([dir1, al])
        if model == 'l-rom':
            fd = info['perc'].replace('p', '.')
            fd = str(int(float(fd)*100))
            solver = model.upper()+' with '+str(fd)+' percentage filtered'
            fname = feature+'_'+info['perc']+'.csv'
        elif model == 'l-rom-df':
            fd = info['fwidth'].replace('p', '.')
            solver = model.upper()+r' with filter width $\delta=$ '+str(fd)
            fname = feature+'_'+info['fwidth']+'.csv'
        else:
            solver = model.upper()
            fname = feature+'.csv'
        tpath = reader.find_files(fname, './')
        print(tpath)
        for f in tpath:
            if model in re.split('[/_]', f):
                fn = f
#       tpath = os.path.join(dir1, feature, fname)
        data = pd.read_csv(fn)
        ax.plot(data.iloc[:, 0], data.iloc[:, 1], '-o', label=solver)
    ax.legend(loc=0)
    anc_lb = []
    for key, value in info['parameters'].items():
        if key == 'theta':
            anc_lb.append('\\'+str(key)+'^*_g='+str(value))
        else:
            anc_lb.append(str(key)+'^*='+str(value))
    anc_lb = ', '.join(anc_lb)
    if feature == 'mrelerr_h1':
       title = 'Relative error in the predicted mean flow at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle\|_{H^1}}$',
              ylim=[1e-3, 1], title=title)
       ax.set_yscale('log')
    elif feature == 'mtke':
       title = 'Predicted mean TKE at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'$\langle TKE \rangle_g$',
              title=title)
       ax.set_yscale('log')
       mtke_fom = np.loadtxt('../qoi/tmtke')
       fom_params = {'c': 'k', 'marker': 'o','label':'FOM'}
       ax.plot(data.iloc[:, 0], mtke_fom*np.ones(len(data.iloc[:, 0])), **fom_params)
    elif feature == 'dual_norm':
       title = 'Dual norm at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'$\triangle$', title=title, ylim=[1e-4, 1])
       ax.set_yscale('log')
    elif feature == 'mtfluc':
       title = 'Predicted mean fluctuation in temperature at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'$\langle T_{fluc} \rangle_s$', title=title)
       mtfluc_fom = np.loadtxt('../qoi/tmtfluc')
       fom_params = {'c': 'k', 'marker': 'o','label':'FOM'}
       ax.plot(data.iloc[:, 0], mtfluc_fom*np.ones(len(data.iloc[:, 0])), **fom_params)
    elif feature == 'mnu':
       filename = './fom/nus_mom.csv'
       fom = pd.read_csv(filename).to_numpy()
       title = 'Predicted mean Nu at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'$\langle Nu \rangle_s$', title=title)
       fom_params = {'c': 'k', 'marker': 'o','label':'FOM'}
       ax.plot(data.iloc[:, 0], fom[0][0]*np.ones(len(data.iloc[:, 0])), **fom_params)
    elif feature == 'stdnu':
       filename = './fom/nus_mom.csv'
       fom = pd.read_csv(filename).to_numpy()
       title = 'Predicted std(Nu) at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', ylabel=r'Std(Nu)', title=title)
       fom_params = {'c': 'k', 'marker': 'o','label':'FOM'}
       ax.plot(data.iloc[:, 0], fom[0][1]*np.ones(len(data.iloc[:, 0])), **fom_params)
    elif feature == 'mnu_err':
       title = 'Relative error in mean Nu at '+'$'+anc_lb+'$'
       ax.set(xlabel=r'$N$', title=title)
       ax.set_yscale('log')
    ax.legend(loc=0)
    tdir = './compare/'
    create_dir(tdir)
    fig.savefig(tdir+feature+'_conv_compare.png')
    return


if __name__ == '__main__':
    import sys
    conv_compare(sys.argv[1:])
