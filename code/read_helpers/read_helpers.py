import numpy as np


def read_mat(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.sqrt(len(t)))
    t1 = np.reshape(t, (lb, lb))
    t = t1[1:N+1, 1:N+1]
    return t


def read_tensor(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.floor((len(t))**(1/3)))
    t1 = np.reshape(t, (lb, lb+1, lb+1))
    t = t1[0:N, 0:N+1, 0:N+1]
    return t


def read_vector(fname):
    t = np.loadtxt(fname)
    return t
