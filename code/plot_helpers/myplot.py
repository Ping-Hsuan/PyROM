import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


def plt_data_in_t(ax, n, T0, data, field, **params_kargs):
    ax.set(xlabel=r'$t$', ylabel=r'$u_{'+str(n+1)+'}(t)$')
    ax.plot(data.outputs['t'], data.outputs[field][n, T0:], **params_kargs)
    return


def plot_coef_avg(ax, rom_avg, snap_avg, tmax, tmin):
    ax.hlines(y=snap_avg, xmin=tmin, xmax=tmax, colors='k',
              linestyle='--', label='Snapshot avg')
    ax.hlines(y=rom_avg, xmin=tmin, xmax=tmax, colors='b',
              linestyle='--', label='ROM avg')
    return


def plt_romcoef_in_t(ax, n, T0, data):
    field = data.field
    rom_params = {'c': 'b', 'mfc': 'None'}
    rom_params['label'] = data.info['method'].upper()
    ax.set(xlabel=r'$t$', ylabel=r'$'+field+r'_{'+str(n+1)+'}(t)$')
    ax.plot(data.outputs['t'][n, T0:], data.outputs[field][n, T0:],
            **rom_params)
    return


def plt_snapcoef_in_t(ax, n, T0, data):
    field = data.field
    snap_params = {'c': 'k', 'mfc': 'None', 'label': 'Snapshot'}
    ax.set(xlabel=r'$t$', ylabel=r'$'+field+r'_{'+str(n+1)+'}(t)$')
    ax.plot(data.outputs['t'], data.outputs[field+'k'][n+1, :],
            **snap_params)
    return


def plt_snap_minmax(ax, n, T0, snap):
    field = snap.field
    tmin = snap.outputs['t'][0]
    tmax = snap.outputs['t'][-1]
    coef_max = snap.outputs[field+'max'][n]
    coef_min = snap.outputs[field+'min'][n]
    ax.hlines(y=coef_max, xmin=tmin, xmax=tmax, colors='r')
    ax.hlines(y=coef_min, xmin=tmin, xmax=tmax, colors='r')
    return


def plt_mean_in_t(ax, n, T0, snap, rom):
    sfield = snap.field
    rfield = rom.field
    tmin = snap.outputs['t'][0]
    tmax = snap.outputs['t'][-1]
    ax.hlines(y=snap.outputs[sfield+'as'][n+1], xmin=tmin, xmax=tmax,
              colors='k', linestyle='--', label='Snapshot avg')
    ax.hlines(y=rom.outputs[rfield+'a'][n], xmin=tmin, xmax=tmax, colors='b',
              linestyle='--', label=rom.info['method'].upper()+' avg')


def add_std_in_t(ax, n, T0, snap, rom):
    sfield = snap.field
    rfield = rom.field
    ax.annotate('Snap std:'+"%.2e" % snap.outputs[sfield+'vs'][n+1],
                xy=(0.2, -0.1), xytext=(12, -12), va='top',
                xycoords='axes fraction', textcoords='offset points')
    ax.annotate(rom.info['method']+' std:'+"%.2e" % rom.outputs[rfield+'v'][n],
                xy=(-0.1, -0.1), xytext=(12, -12), va='top',
                xycoords='axes fraction', textcoords='offset points')


def plt_sample_mean_var(rom, snap, nb):
    sfield = snap.field
    rfield = rom.field

    asnap = snap.outputs[sfield+'as']
    vsnap = snap.outputs[sfield+'vs']

    fig, axs = plt.subplots(2, sharex=True, tight_layout=True)

    POD_modes = [np.linspace(1, nb, nb, dtype=int),
                 np.linspace(1, nb, nb, dtype=int)]

    data = [rom.outputs[rfield+'a'], rom.outputs[rfield+'v']]
    refs = [asnap, vsnap]

    ylabels = [r'$\langle '+rfield+r'_{n} \rangle_s$', r'$V_s('+rfield+r'_n)$']
    params = [{'c': 'b', 'marker': 'o', 'mfc': 'None',
               'label': rom.info['method'].upper()},
              {'c': 'k', 'marker': 'x', 'mfc': 'None', 'label': 'FOM'}]
    for i in range(2):
        axs[i].plot(POD_modes[i], data[i], **params[0])
        axs[i].plot(POD_modes[i], refs[i][1:nb+1], **params[1])
        axs[i].legend(loc=0)
        axs[i].set_ylabel(ylabels[i])
        axs[i].set_xlabel(r'$n$')
        axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))
        if i == 1:
            axs[i].set_yscale('log')

    return fig
