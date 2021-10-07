import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


class PostMOR:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def coef_in_t(self, ax, i, fomcoef, minc, maxc, asnap, vsnap, T0, field):
        rom_params = {'c': 'b', 'mfc': 'None', 'label': 'Snapshot'}
        snap_params = {'c': 'k', 'mfc': 'None', 'label': 'Snapshot'}

        ax.set(xlabel=r'$t$', ylabel=r'$u_{'+str(i+1)+'}(t)$')

        ax.plot(self.outputs['t'][i, T0:], self.outputs[field][i, T0:],
                **rom_params)
        ax.plot(np.linspace(500, 1000, self.info['K']), fomcoef[i+1, :], **snap_params)

        tmin = self.outputs['t'][i, T0]
        tmax = self.outputs['t'][i, -1]
        ax.hlines(y=maxc[i], xmin=tmin, xmax=tmax, colors='r')
        ax.hlines(y=minc[i], xmin=tmin, xmax=tmax, colors='r')

        ax.hlines(y=asnap[i+1], xmin=tmin, xmax=tmax, colors='k',
                  linestyle='--', label='Snapshot avg')
        ax.hlines(y=self.outputs[field+'a'][i], xmin=tmin, xmax=tmax, colors='b',
                  linestyle='--', label='ROM avg')

        ax.annotate('Snap std:'+"%.2e"% vsnap[i+1], xy=(0, 0.2), xytext=(12, -12), va='top',
                    xycoords='axes fraction', textcoords='offset points')
        ax.annotate('ROM std:'+"%.2e"% self.outputs[field+'v'][i], xy=(0, 0.27), xytext=(12, -12), va='top',
                    xycoords='axes fraction', textcoords='offset points')
        return

