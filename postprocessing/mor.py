class ROM:

    def __init__(self, fpath):
        import re
        self.fpath = fpath
        self.fname = self.fpath.split('/')[-1]
        self.info = {}

        match = re.match(r"(.*)s_(.*)_(.*)nb_(.*)_(.*)_(.*)_.*", self.fname)
        # Number of snapshots
        self.info['K'] = int(match.groups()[0])
        # Types of ROM
        self.info['method'] = (match.groups()[1])
        # Number of POD modes
        self.info['nb'] = int(match.groups()[2])
        # Start from 0 or ic
        self.info['init'] = (match.groups()[3])
        # norm when doing POD
        self.info['POD_norm'] = (match.groups()[4])

    def get_coef(self, field):
        import numpy as np
        coef = []
        t = []
        with open(self.fpath, 'r') as f:
            for line in f:
                info = line.split()
                coef.append(info[2])
                t.append(info[1])

        self.outputs = {}
        self.outputs['t'] = np.reshape(np.array(t).astype(np.float64),
                                       (self.info['nb'], -1), order='F')
        self.outputs[field] = np.reshape(np.array(coef).astype(np.float64),
                                         (self.info['nb'], -1), order='F')
        return

    def coef_mean(self, T0, field):
        import numpy as np

        avg_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            avg_coef[j] = np.sum(self.outputs[field][j, T0:]) \
                        / num_sample

        self.outputs[field+'a'] = avg_coef
        return

    def coef_variance(self, T0, field):
        import numpy as np

        var_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            var_coef[j] = np.sum((self.outputs[field][j, T0:]
                                 - self.outputs[field+'a'][j])**2) \
                                 / (num_sample-1)

        self.outputs[field+'v'] = var_coef
        return

    def plot_coef_in_t(self, ax, i, fomcoef, minc, maxc, asnap, vsnap, T0, field):
        import numpy as np
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

