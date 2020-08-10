import numpy as np


def setops(N, msg):
    if msg == 'u':
        a = seta('./au', N)
        b = setb('./bu', N)
        c = setc('./cu', N)
    elif msg == 't':
        a = seta('./at', N)
        b = setb('./bt', N)
        c = setc('./ct', N)
    return a, b, c


def seta(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.sqrt(len(t)))
    t = np.reshape(t, (lb, lb))
    a = t[1:N+1, 1:N+1]
    return a


def setb(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.sqrt(len(t)))
    t = np.reshape(t, (lb, lb))
    b = t[1:N+1, 1:N+1]
    return b


def setc(fname, N):
    t = np.loadtxt(fname)
    lb = int(np.floor((len(t))**(1/3)))
    t = np.reshape(t, (lb, lb+1, lb+1))
    c = t[0:N, 0:N+1, 0:N+1]
    return c
