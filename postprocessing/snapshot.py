import numpy as np


class Snapshot:

    def __init__(self, ops_path, field):
        self.ops_path = ops_path
        if field == 't':
            self.field = field.upper()
        else:
            self.field = field

    def coef(self, K):
        field = self.field
        self.outputs = {}
        self.outputs[field+'k'] = np.loadtxt(self.ops_path+field.lower()+'k')
        self.outputs[field+'k'] = np.reshape(np.array(self.outputs[field+'k']).
                                             astype(np.float64),
                                             (-1, K), order='F')
        return self.outputs[field+'k']

    def extrema(self):
        field = self.field
        self.outputs[field+'max'] = np.loadtxt(self.ops_path+field.lower()+'max')
        self.outputs[field+'min'] = np.loadtxt(self.ops_path+field.lower()+'min')
        return self.outputs[field+'min'], self.outputs[field+'max']

    def mean(self):
        key = self.field.lower() + 'as'
        self.outputs[self.field+'as'] = np.loadtxt(self.ops_path+key)
        return self.outputs[self.field+'as']

    def var(self):
        key = self.field.lower() + 'vs'
        self.outputs[self.field+'vs'] = np.loadtxt(self.ops_path+key)
        return self.outputs[self.field+'vs']
