import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
from reader import erri_w_theta
import checker
import mypostpro
import re
import collections
import csv

setup.style(1)
colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Current directory is:', os.chdir(str(sys.argv[1])))
model = str(sys.argv[2])
print('The model is:', model)
print("---------------------------------------------")

if len(sys.argv) <= 3:
#   ylb = r'$\triangle$'
    ylb = 'Unscaled error indicator'
    tag = ''
    title = 'Unscaled error indicator'
else:
    if sys.argv[3] == 'fom':
#       ylb = r'$\frac{\triangle(\theta_g)}{\|u_{FOM}(\theta^*_g)\|_{H^1}}$'
        ylb = 'Scaled error indicator'
        tag = '_sc_fom'
        title = r'Error indicator scaled with $H^1$ norm of FOM solution'
    elif sys.argv[3] == 'relerr':
#       ylb = r'$\frac{\triangle(\theta_g) \|u(\theta_g)\|_{H^1}}' + \
#             r'{\|u_{FOM}({\theta_g})-u_{ROM}({\theta_g})\|_{H^1}}$'
        ylb = 'Scaled error indicator'
        tag = '_sc_relerr'
        title = r'Error indicator scaled with relative $H^1$ error'
    elif sys.argv[3] == 'romabserr':
#       ylb = r'$\frac{\triangle(\theta_g)}' + \
#             r'{\|u_{FOM}({\theta_g})-u_{ROM}({\theta_g})\|_{H^1}}$'
        ylb = 'Scaled error indicator'
        tag = '_sc_romabserr'
        title = r'Error indicator scaled with absolute $H^1$ error'
    elif sys.argv[3] == 'rom':
#       ylb = r'$\frac{\triangle(\theta_g)}{\|u_{ROM}(\theta_g)\|_{H^1}}$'
        ylb = 'Scaled error indicator'
        tag = '_sc_rom'
        title = r'Error indicator scaled with $H^1$ norm of ROM solution'

with open('train_info'+tag+'.csv', newline='') as f:
     reader = csv.reader(f)
     data = list(reader)

data[0] = [int(i) for i in data[0]]
P_train_max = data[1]
N_max = data[2]
K_list = data[3]
print("POD-hGreedy information:")
print("Iteration: ", data[0])
print("Anchor points: ", data[1])
print("N: ", data[2])
print("K: ", data[3])
print("---------------------------------------------")

color_ctr = 0

fig, ax = plt.subplots(1, tight_layout=True)

anchors = []
erri_his = []
erri_anchor = []
max_erri = []


for itr, anchor, N, K in zip(data[0], data[1], data[2], data[3]):

    ax.set(xlabel=r'$\theta_g$', ylabel=ylb,
           ylim=[1e-5, 1e1],
           xticks=np.linspace(0, 180, 19, dtype=int))

    print(itr, anchor, N, K)

    if len(sys.argv) <= 3:
        angle, erri = erri_w_theta(model, anchor, N)
    else:
        angle, erri = erri_w_theta(model, anchor, N, sys.argv[3])

    ax.semilogy(angle, erri, 'b--o')
    ax.set_title('iteration '+str(itr) +
                ', '+r'$\theta^*_{'+'g,'+str(itr)+'}$'+r'$='+anchor+'$')
    idx = np.where(angle == int(anchor))
    
    erri_anchor.append(erri[idx])
    anchors.append(int(anchor))
    ax.semilogy(anchors, erri_anchor, 'ro')

    erri_his.append(erri)
    erri_comb = np.array(erri_his)
    erri_min = np.amin(erri_comb, axis=0)

    ax.semilogy(angle, erri_min, 'k-', label='min')
    idxmax = np.argmax(erri_min)
    max_erri.append(erri_min[idxmax])

    candidate = str(int(angle[idxmax]))
    while candidate in P_train_max[:itr]:
        print('Skipping the same anchor point')
        erri_min[idxmax] = 1e-8
        idxmax = np.argmax(erri_min)
        candidate = str(int(angle[idxmax]))
        print('Next candidate', candidate)
    print('h-greedy, l=', itr, 'max erri:', erri_min[idxmax])
    print("The next anchor point is ", angle[idxmax])

    ax.legend(loc=0, ncol=1)
    ax.axes.grid(True, axis='y')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    fig.savefig('offline_erri_L'+str(itr)+tag+'.png')
    ax.clear()

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(xlabel='Iteration', ylabel=r'$\max{\triangle(\theta_g)}$',
       xlim=[0, max(data[0])+1], ylim=[1e-3, 1e0])
ax.semilogy(data[0], max_erri, 'k-o')

np.savetxt('iter'+tag+'.dat', data[0])
np.savetxt('max_erri'+tag+'.dat', max_erri)
fig.savefig('max_erri_w_iter'+tag+'.png')
