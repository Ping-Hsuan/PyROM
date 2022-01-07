def fom_compare(feature):
    import sys
    import re
    import pandas as pd
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text
    from aux.create_dir import create_dir
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import reader

    style(1)
    text()

    fnames = reader.find_files(feature+'.csv', './')
    param = [int(re.split('[/]', i)[1].split('_')[2]) for i in fnames]
    param, fnames = zip(*sorted(zip(param, fnames)))
    fig, ax = plt.subplots(1, tight_layout=True)
    for f in fnames:
        ptr = re.split('[/]', f)
        data = pd.read_csv(f)
        ax.plot(data.iloc[:, 0], data.iloc[:, 1], '-', label=ptr[1].replace('_', '='))
    ax.legend(loc=0)
    if 'nus' in ptr[-1].split('_'):
        title = 'Nu History'
        ax.set(xlabel=r'$t$', ylabel=r'Nu', ylim=[0, 80], title=title)
    elif 'ene' in ptr[-1].split('_'):
        title = 'Energy History'
        ax.set(xlabel=r'$t$', ylabel=r'$\frac{1}{2}\|u\|^2_{L^2}$', title=title)
    elif 'tene' in ptr[-1].split('_'):
        title = r'Squared $L^2$ Norm of Temperature History'
        ax.set(xlabel=r'$t$', ylabel=r'$\|T\|^2_{L^2}$', title=title)
    tdir = './fom_compare/'
    create_dir(tdir)
    fig.savefig(tdir+feature+'.png')
    return


if __name__ == '__main__':
    import sys
    fom_compare(*sys.argv[1:])
