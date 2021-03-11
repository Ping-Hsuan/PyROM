import numpy as np


class Snapshot:

    def __init__(self, ops_path, field):
        self.ops_path = ops_path
        self.field = field

    def coef(self, K):
        field = self.field
        self.outputs = {}
        self.outputs[field+'k'] = np.loadtxt(self.ops_path+field+'k')
        self.outputs[field+'k'] = np.reshape(np.array(self.outputs[field+'k']).
                                             astype(np.float64),
                                             (-1, K), order='F')
        return self.outputs[field+'k']

    def extrema(self):
        field = self.field
        self.outputs[field+'max'] = np.loadtxt(self.ops_path+field+'max')
        self.outputs[field+'min'] = np.loadtxt(self.ops_path+field+'min')
        return self.outputs[field+'min'], self.outputs[field+'max']

    def mean(self):
        key = self.field + 'as'
        self.outputs[key] = np.loadtxt(self.ops_path+key)
        return self.outputs[key]

    def var(self):
        key = self.field + 'vs'
        self.outputs[key] = np.loadtxt(self.ops_path+key)
        return self.outputs[key]
