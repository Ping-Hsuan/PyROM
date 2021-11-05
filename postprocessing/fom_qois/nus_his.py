def nus_his():
    import os
    import re
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()

    fname = os.path.split(os.getcwd())[-1]
    fname = fname.replace('_', '')
    res = re.split('(\d+)', fname)

#   data = np.loadtxt('nus_his')
    with open('nus_his', 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[0:] for x in list_of_words]
    data = np.array(data, dtype=float)

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 1], data[:, 2])
    ax.set(ylabel='Nu',
           xlabel=r'$t$',
           title='Nusselt Number History')
    fig.savefig('nus_his')
    return


if __name__ == '__main__':
    import sys
    nus_his()
