import numpy as np
import re
import os


class ROM:

    def __init__(self, fpath, field='u'):
        self.fpath = fpath
        print(self.fpath)
        self.fname = self.fpath.split('/')[-1]
        if field == 't':
            self.field = field.upper()
        else:
            self.field = field
        self.info = {}
        self.outputs = {}

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
        field = self.field
        coef = []
        t = []
        with open(self.fpath, 'r') as f:
            for line in f:
                info = line.split()
                coef.append(info[2])
                t.append(info[1])

        self.outputs['t'] = np.reshape(np.array(t).astype(np.float64),
                                       (self.info['nb'], -1), order='F')
        self.outputs[field] = np.reshape(np.array(coef).astype(np.float64),
                                         (self.info['nb'], -1), order='F')
        return

    def coef_mean(self, T0):
        field = self.field

        avg_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            avg_coef[j] = np.sum(self.outputs[field][j, T0:]) \
                        / num_sample

        self.outputs[field+'a'] = avg_coef
        return

    def coef_variance(self, T0):
        field = self.field

        var_coef = np.zeros((self.info['nb'],))
        num_sample = len(self.outputs[field][0, T0:])

        for j in range(self.info['nb']):
            var_coef[j] = np.sum((self.outputs[field][j, T0:]
                                 - self.outputs[field+'a'][j])**2) \
                                 / (num_sample-1)

        self.outputs[field+'v'] = var_coef
        return

    def DTAR(self):
        with open(self.fpath, 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
        dtar = [x[-1] for x in list_of_words]
        self.outputs['dtar'] = np.array(dtar).astype(np.float64)
        return

    def anchor(self, parameter):
        # Might need to change according to the parameter
        # Currently using theta
        root = os.getcwd()
        sp1 = (root.split('/'))
        for element in sp1:
            z = re.match(parameter+r"_(\d+)", element)
            if z:
                self.info['anchor'] = float(((z.groups())[0]))
        return
