import numpy as np
import numpy.linalg as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import re
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import pod
import setup

setup.style(1)
colors = setup.color(0)
setup.text()

# adjust markersize
mpl.rcParams['lines.markersize'] = 3
mpl.rcParams['lines.linewidth'] = 1

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
isExist = os.path.exists(os.getcwd()+'/gram_analysis/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/gram_analysis/')

ifrom = [True, False]
ifrom[1] = input("Thermal?:")
if ifrom[1] == 'T':
    ifrom[1] = True
else:
    ifrom[1] = False

tpath = './gram_analysis/'

gu = np.loadtxt('./ops/bu')
lsu = int(np.sqrt(len(gu)))
tmp = np.reshape(gu, (lsu, lsu))
gu = tmp[1:, 1:]
print(gu.shape)
Numax = LA.matrix_rank(gu)
print("gu rank:", Numax)
xdata = np.linspace(1, len(gu), len(gu))

print("Solving gu's eigenvalues...")
vu, wu = LA.eig(gu)
vu = vu.real
vu[::-1].sort()
np.savetxt(tpath+'veig.dat', vu)
print(LA.inv(gu))

gu = np.loadtxt('./ops/bt')
lsu = int(np.sqrt(len(gu)))
tmp = np.reshape(gu, (lsu, lsu))
gu = tmp[1:, 1:]
bt = gu
Numax = LA.matrix_rank(gu)
print("gu rank:", Numax)
xdata = np.linspace(1, len(gu), len(gu))

print("Solving gu's eigenvalues...")
vu, wu = LA.eig(gu)
vu = vu.real
vu[::-1].sort()
np.savetxt(tpath+'teig.dat', vu)

print(LA.inv(gu))
gu = np.loadtxt('./ops/at')
lsu = int(np.sqrt(len(gu)))
tmp = np.reshape(gu, (lsu, lsu))
at = tmp[1:, 1:]

vu, wu = LA.eig((1/5e-3)*bt+0.0071*at)
print(vu)
