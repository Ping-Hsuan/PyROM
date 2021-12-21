def conv_compare(argv):
    import yaml
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text
    from aux.create_dir import create_dir

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
        tpath = os.path.join(dir1, feature, fname)
        data = pd.read_csv(tpath)
        ax.plot(data.iloc[:, 0], data.iloc[:, 1], '-o', label=solver)
    ax.legend(loc=0)
    anc_lb = ''
    for key, value in info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)
    title = 'Relative error in the predicted mean flow at '+'$'+anc_lb+'$'
    ax.set(xlabel=r'$N$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle\|_{H^1}}$',
           ylim=[0, 0.7], title=title)
    tdir = './compare/'
    create_dir(tdir)
    fig.savefig(tdir+feature+'_conv_compare.png')
    return


if __name__ == '__main__':
    import sys
    conv_compare(sys.argv[1:])
