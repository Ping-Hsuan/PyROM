import numpy as np


def plot_rom_norm_wparam(angle, h10norm, l2norm, h1norm, ax, label):
    if label == 'uT':
        ylb = r'$\||(u, T)\|_{'
        lst = '--'
        mk = 'o'
    elif label == 'u':
        ylb = r'$\||u\|_{'
        lst = '--'
        mk = 'x'
    elif label == 'T':
        ylb = r'$\||T\|_{'
        lst = '--'
        mk = 's'

    ax.set(xlabel=r'$\theta_g$', xticks=np.linspace(0, 180, 19, dtype=int))
    ax.plot(angle, h10norm, 'bo', linestyle=lst, mfc="None", label=r'ROM $H^1_0$ norm')
    ax.plot(angle, l2norm, 'bx', linestyle=lst, mfc="None", label=r'ROM $L^2$ norm')
    ax.plot(angle, h1norm, 'bv', linestyle=lst, mfc="None", label=r'ROM $H^1$ norm')
#   ax.plot(angle, h10norm, 'b', marker=mk, linestyle=lst, mfc="None", label=ylb+'H^1_0}$')
#   ax.plot(angle, l2norm, 'r', marker=mk, linestyle=lst, mfc="None", label=ylb+'L^2}$')
#   ax.plot(angle, h1norm, 'k', marker=mk, linestyle=lst, mfc="None", label=ylb+'H^1}$')
    ax.legend(loc=0, ncol=3)
    return


def store_rom_norm(h10norm, l2norm, h1norm, label):
    if label == 'uT':
        str1 = ''
    elif label == 'u':
        str1 = ''
    elif label == 'T':
        str1 = ''
    return


def sort(ROMs, key1, key2):
    data1 = []
    data2 = []
    for rom in ROMs:
        data1.append(rom.info[key1])
        data2.append(rom.outputs[key2])

    data = np.column_stack((data1, data2))
    data = data[data[:, 0].argsort()]
    return data
