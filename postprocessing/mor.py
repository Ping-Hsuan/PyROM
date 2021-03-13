class ROM:

    def __init__(self, fpath, field):
        import re
        self.fpath = fpath
        self.fname = self.fpath.split('/')[-1]
        if field == 't':
            self.field = field.upper()
        else:
            self.field = field
        self.info = {}

        match = re.match(r"(.*)s_(.*)_(.*)nb_(.*)_(.*)_(.*)_.*", self.fname)
        # Number of snapshots
        self.info['K'] = int(match.groups()[0])
        # Types of ROM
        if match.groups()[1] == 'rom':
            self.info['method'] = 'GROM'
        elif match.groups()[1] == 'crom':
            self.info['method'] = 'CROM'
        elif match.groups()[1] == 'lrom':
            self.info['method'] = 'LROM'
        # Number of POD modes
        self.info['nb'] = int(match.groups()[2])
        # Start from 0 or ic
        self.info['init'] = (match.groups()[3])
        # norm when doing POD
        self.info['POD_norm'] = (match.groups()[4])

    def get_coef(self):
        import numpy as np
        field = self.field
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

    def coef_mean(self, T0):
        import numpy as np
        field = self.field

        avg_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            avg_coef[j] = np.sum(self.outputs[field][j, T0:]) \
                        / num_sample

        self.outputs[field+'a'] = avg_coef
        return

    def coef_variance(self, T0):
        import numpy as np
        field = self.field

        var_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            var_coef[j] = np.sum((self.outputs[field][j, T0:]
                                 - self.outputs[field+'a'][j])**2) \
                                 / (num_sample-1)

        self.outputs[field+'v'] = var_coef
        return

