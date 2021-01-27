import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import re
import os
import subprocess
import operator
import sys


print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
print("---------------------------------------------")

for root, dirs, files in os.walk("./crom/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            pass
    for name in dirs:
        pass
filenames = [name for name in files if re.match('^.*_(.*)rom_.*$', name)]

def create_dir(fname):
    # get the absolute error in ROM
    isExist = os.path.exists(os.getcwd()+fname)
    if isExist:
        print("The target directory "+fname+" exist")
        pass
    else:
        os.mkdir(os.getcwd()+fname)
        print("Create the target"+fname+" directory successfully")
    print("---------------------------------------------")


data_tpath = ['./rom_abserr/', './fom_norm/', './nu/', './romu/', './romt/', './proj_relerr/', './dual_norm/']
data_mkdir = ['/rom_abserr/', '/fom_norm/', '/nu/', '/romu/', '/romt/', '/proj_relerr/', '/dual_norm/']
data_fname = ['_rom_abserr', '_fom_norm', '_nu', '_romu', '_romt', '_projrelerr', '_dn']
data_pattern = [r'^\sh1\serror:', r'^\sFOM\sh1\snorm:', r'\snus', r'\sromu', r'\sromt', r'\srelative\sh1\serror:', r'(residual in h1 norm:\s\s+)(\d\.\d+E?-?\d+)']
]

for (tpath, mkdir, label, pattern) in zip(data_tpath, data_mkdir, data_fname, data_pattern):
    create_dir(mkdir)
    for fname in filenames:
        forleg = fname.split('_')

        match_rom = re.match('^.*_(.*)rom_.*$', fname)
        assert match_rom is not None

        # write out absolute error in ROM
        ft = open(tpath+fname+label, 'w')
        with open(root+fname, 'r') as f:
            for line in f:
                if re.search(pattern, line):
                    ft.write(line)
        ft.close()

