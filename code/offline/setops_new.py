import sys
sys.path.append('../')
from read_helpers.read_helpers import *


class setops_u:
    def __init__(self, dir_a, dir_b, dir_c, size):
        self.a = self.seta(dir_a, size)
        self.size = size
    def seta(self, fname, N):
        t = read_mat(fname, N)
        a = t[1:N+1, 1:N+1]
        return a


