import sys
sys.path.append('../')
from read_helpers.read_helpers import *


class setops_u:
    def __init__(self, dir_a, dir_b, dir_c, size):
        self.a = read_mat(dir_a, size)
        self.b = read_mat(dir_b, size)
        self.c = read_tensor(dir_c, size)
        self.size = size

class setops_new:
    def __init__(self, *arg, size):
        if len(arg) > 3:
            if 'but_x' in arg[3].split('/'):
                print('correct operator directory name')
                self.but_x = read_mat(arg[3], size)
            else: 
                print('operator directory name in argument '+str(3)+\
                        'is incorrect')
            if 'but_y' in arg[4].split('/'):
                print('correct operator directory name')
                self.but_y = read_mat(arg[4], size)
            else: 
                print('operator directory name in argument '+str(4)+ \
                        'is incorrect')
            self.a = read_mat(arg[0], size)
            self.b = read_mat(arg[1], size)
            self.c = read_tensor(arg[2], size)
            self.size = size
        else:
            self.a = read_mat(arg[0], size)
            self.b = read_mat(arg[1], size)
            self.c = read_tensor(arg[2], size)
            self.size = size

