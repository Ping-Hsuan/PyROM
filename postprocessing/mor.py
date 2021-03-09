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

    def coef(self):
        import numpy as np
        coef = []
        t = []
        with open(self.fpath, 'r') as f:
            for line in f:
                info = line.split()
                coef.append(info[2])
                t.append(info[1])

        t = np.reshape(np.array(t).astype(np.float64),
                       (self.info['nb'], -1), order='F')
        coef = np.reshape(np.array(coef).astype(np.float64),
                          (self.info['nb'], -1), order='F')
        return t, coef

    def coef_mean(self, coef, T0):
        import numpy as np
        ua = np.zeros((self.info['nb'],))
        for j in range(self.info['nb']):
            ua[j] = np.sum(coef[j, T0:])/len(coef[0, T0:])

        return ua

    def coef_variance(self, coef, T0, ua):
        import numpy as np
        uv = np.zeros((self.info['nb'],))
        for j in range(self.info['nb']):
            uv[j] = np.sum((coef[j, T0:]-ua[j])**2)/(len(coef[0, T0:])-1)

        return uv

