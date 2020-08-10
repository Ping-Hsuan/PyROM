import sys
sys.path.append('../')
from read_helpers.read_helpers import *


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
    t = read_mat(fname, N)
    a = t[1:N+1, 1:N+1]
    return a


def setb(fname, N):
    t = read_mat(fname, N)
    b = t[1:N+1, 1:N+1]
    return b


def setc(fname, N):
    t = read_tensor(fname, N)
    c = t[0:N, 0:N+1, 0:N+1]
    return c


def setbut(N,ldim):

    t = read_mat('./but_x', N)
    but_x = t[1:N+1, 1:N+1]

    t = read_mat('./but_y', N)
    but_y = t[1:N+1, 1:N+1]
    if (ldim == 2):
        return but_x, but_y
    else:
        t = read_mat('./but_z', N)
        but_z = t[1:N+1, 1:N+1]
        return but_x, but_y, but_z
