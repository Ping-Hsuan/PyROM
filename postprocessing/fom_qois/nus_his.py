def nus_his(T0=None, Tf=None):
    import os
    import re
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text
    from aux.mypostpro import find_nearest

    style(1)
    text()

    fname = os.path.split(os.getcwd())[-1]
    fname = fname.replace('_', '')

#   data = np.loadtxt('nus_his')
    with open('nus_his', 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[0:] for x in list_of_words]
    data = np.array(data, dtype=float)

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 0], data[:, 1])
    ax.set(ylabel='Nu',
           xlabel=r'$t$',
           title='Nusselt Number History')
    fig.savefig('nus_his')
    np.savetxt('nus_his.csv', data, delimiter=',', header='t, Nu', comments="")
    if T0 is not None and Tf is not None:
        J0 = find_nearest(data[:, 0], int(T0))
        Jf = find_nearest(data[:, 0], int(Tf))
        ax.set_xlim([data[J0, 0], data[Jf, 0]])
        fig.savefig('nus_his_'+T0+'_'+Tf)
    return


if __name__ == '__main__':
    import sys
    nus_his(*sys.argv[1:])
