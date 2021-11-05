def udiff_his():
    import os
    import re
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.style import style
    from figsetup.text import text
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import mypostpro

    style(1)
    text()

    fname = os.path.split(os.getcwd())[-1]
    fname = fname.replace('_', '')
    res = re.split('(\d+)', fname)

    with open('udiff_his', 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[0:3] for x in list_of_words]
    for i in data:
        i[0] = i[0].replace(',', '')
    data = np.array(data, dtype=float)
#   idx1 = mypostpro.find_nearest(data[:, 0], 0)
#   idx2 = mypostpro.find_nearest(data[:, 0], 400000)
#   print(idx1, idx2)
#   data[idx1:idx2, 2] = data[idx1:idx2, 2]/(np.sqrt(0.0025)*10)
#   data[idx2:, 2] = data[idx2:, 2]/10
#   np.savetxt('udiff', data)
#   1/o

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 1], data[:, 2])
    ax.set_ylim([1e-3, 0.03])
    ax.set(ylabel=r'$\frac{\|\frac{u^n-u^{n-1}}{\Delta t}\|_{L^2}}{|\Omega|^{1/2}}$',
           xlabel=r'$t$',
           title='Rate of Change in Velocity History')
    fig.savefig('udiff_his')
    return


if __name__ == '__main__':
    import sys
    udiff_his()
