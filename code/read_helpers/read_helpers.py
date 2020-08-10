import numpy as np


def read_mat(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.sqrt(len(t)))
    t = np.reshape(t, (lb, lb))
    return t


def read_tensor(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.floor((len(t))**(1/3)))
    t = np.reshape(t, (lb, lb+1, lb+1))
    return t
