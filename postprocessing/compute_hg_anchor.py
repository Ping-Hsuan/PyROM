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

with open('train_info.csv', newline='') as f:
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

ylb = r'$triangle$'
if sys.argv[3] == 'fom':
    ylb = r'$\frac{\triangle}{\|u(\theta^*_g)\|_{H^1}}$'
elif sys.argv[3] == 'relerr':
    ylb = r'$\frac{\triangle \|u(\theta_g)\|_{H^1}}' + \
          r'{\|u({\theta_g})-\widehat{u}({\theta_g})\|_{H^1}}$'
elif sys.argv[3] == 'rom':
    ylb = r'$\frac{\triangle}{\|\widehat{u}(\theta_g)\|_{H^1}}$'

for itr, anchor, N, K in zip(data[0], data[1], data[2], data[3]):
    ax.set(xlabel=r'$\theta_g$', ylabel=ylb,
           ylim=[1e-5, 1e1],
           xticks=np.linspace(0, 180, 19, dtype=int))
    print(itr, anchor, N, K)

    angle, erri = erri_w_theta(model, anchor, N, sys.argv[3])
    ax.semilogy(angle, erri, 'b--o', label=r'\textit{it} = '+str(itr) +
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

    print('h-greedy, l=', itr, 'max erri:', erri_min[idxmax])
    print("The next anchor point is ", angle[idxmax])

    ax.legend(loc=0, ncol=5, fontsize=10)
    ax.axes.grid(True, axis='y')
    fig.savefig('offline_erri_L'+str(itr)+'.png')
    ax.clear()

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(xlabel='Iteration', ylabel=r'$\max{\triangle(\theta_g)}$',
       xlim=[0, max(data[0])+1], ylim=[1e-3, 1e0])
ax.semilogy(data[0], max_erri, 'k-o')

np.savetxt('iter.dat', data[0])
np.savetxt('max_erri.dat', max_erri)
fig.savefig('max_erri_w_iter.png')
