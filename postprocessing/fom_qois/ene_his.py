def ene_his():
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

    with open('ene_his', 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[0:4] for x in list_of_words]
    for i in data:
        i[0] = i[0].replace(',', '')
    data = np.array(data, dtype=float)
#   idx1 = mypostpro.find_nearest(data[:, 0], 0)
#   idx2 = mypostpro.find_nearest(data[:, 0], 500000)
#   print(idx1, idx2)
#   data[idx2+1:, 1] += 1000
#   np.savetxt('ene', data)
#   1/o

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 1], data[:, 2])
    ax.set(ylabel=r'$\frac{1}{2}\|u\|^2_{L^2}$',
           xlabel=r'$t$',
           title='Energy History')
    fig.savefig('ene_his')
    np.savetxt('ene_his.csv', data[:, [1, 2]], delimiter=',', header='t, ene', comments="")
    return


if __name__ == '__main__':
    import sys
    ene_his()
