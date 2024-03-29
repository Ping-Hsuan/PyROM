import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
from reader import erri_w_theta
from reader import erri_w_param
from reader import erri_leray_w_param
from figsetup.style import style
from figsetup.color import color
from figsetup.text import text
import checker
import mypostpro
import re
import collections
import csv
import yaml
import math
from hg_offline.helper import get_anchor_mabserr
from hg_offline.helper import get_anchor_mrelerr

style(1)
colors = color(0)
text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Current directory is:', os.chdir(str(sys.argv[1])))
mode = str(sys.argv[2])
print("---------------------------------------------")

if len(sys.argv) <= 3:
    ylb = r'$\Delta$'
#   ylb = 'Error indicator'
    tag = ''
    title = r'POD-$h$Greedy, offline stage: Error indicator'
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
    elif sys.argv[3] == 'eta_rom':
#       ylb = r'$\frac{\triangle(\theta_g)}{\|u_{ROM}(\theta_g)\|_{H^1}}$'
        ylb = 'Scaled error indicator'
        tag = '_sc_eta_rom'
        title = r'Error indicator scaled with effectivity and rom norm'

#with open('train_info'+tag+'.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)
with open('train_info.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)

print("POD-hGreedy information:")
data = []
for i, key in enumerate(features.keys()):
    print(key+": ", features[key])
    data.append(features[key])
print("---------------------------------------------")

color_ctr = 0

fig, ax = plt.subplots(1, tight_layout=True)

anchors = []
erri_his = []
erri_anchor = []
max_erri = []

for itr, anchor, N, K, model in zip(data[0], data[1], data[2], data[3], data[6]):

    print(itr, anchor, N, K, model, data[7])

    if len(sys.argv) <= 3:
#       angle, erri = erri_w_theta(model, anchor, N, mode)
        if model != 'l-rom' and model !='l-rom-df':
            angle, erri = erri_w_param(model, anchor, N, mode)
        else:
            angle, erri = erri_leray_w_param(model, anchor, N, mode, data[7][itr-1])
        if features['scaled'] == 'mabserr':
            param, mabserr_rom, mabserr_proj = get_anchor_mabserr(anchor, N, model, mode, data[7][itr-1])
            idx = np.where(param == anchor)
            erri = erri/mabserr_rom[idx]
            ylb = r'$\Delta$'
            title = 'POD-$h$Greedy, offline stage: \n'+r'Error indicator'+' at '+r'$\mathcal{P}_{train}$'+' scaled with absolute $H^1$ error'
        elif features['scaled'] == 'mrelerr':
            param, mrelerr_rom, mrelerr_proj = get_anchor_mrelerr(anchor, N, model, mode, data[7][itr-1])
            idx = np.where(param == anchor)
            erri = erri/mrelerr_rom[idx]
            ylb = r'$\Delta$'
            title = 'POD-$h$Greedy, offline stage: \n'+r'Error indicator'+' at '+r'$\mathcal{P}_{train}$'+' scaled with relative $H^1$ error'
        elif features['scaled'] == 'eff':
            param, mabserr_rom, mabserr_proj = get_anchor_mabserr(anchor, N, model, mode, data[7][itr-1])
            idx = np.where(param == anchor)
            scale = erri[idx]/mabserr_rom[idx]
            erri = erri/scale
            ylb = r'$\Delta$'
            title = r'POD-$h$Greedy, offline stage: Error indicator'+' at '+r'$\mathcal{P}_{train}$'+' scaled with effectivity'
        elif features['scaled'] is None:
            features['scaled'] = 'nosc'
    else:
#       angle, erri = erri_w_theta(model, anchor, N, mode, sys.argv[3])
        if model != 'l-rom':
            angle, erri = erri_w_param(model, anchor, N, mode, sys.argv[3])
        else:
            angle, erri = erri_leray_w_param(model, anchor, N, mode, data[7][itr-1], sys.argv[3])
    idx = [angle.index(i) for i in features['Ptrain']]
    angle = np.asarray(angle)[idx]
    erri = np.asarray(erri)[idx]
    ax.semilogy(angle, erri, '--o', color=colors[itr-1], mfc="None", label=r'$\mathsf{Iter} = $ '+str(itr))
    print(anchor)
    idx = np.where(angle == int(anchor))
    erri_anchor.append(erri[idx])
    anchors.append(int(anchor))
    anc = ax.semilogy(anchors, erri_anchor, 'ro', label='Anchor point')

    erri_his.append(erri)
    erri_comb = np.array(erri_his)
    erri_min = np.amin(erri_comb, axis=0)

    lmin = ax.semilogy(angle, erri_min, 'k-', label='min')
    idxmax = np.argmax(erri_min)
    max_erri.append(erri_min[idxmax])

    if (max(erri)/min(erri) >= 1e2) or (max(erri) < 0.1):
        ax.set_yscale('log')
        ylim_exp = math.ceil(math.log10(min(erri)))-1
#       ylim = [10**ylim_exp, 1e0]
        ylim = [1e-3, 1e0]
    else:
        ax.set_yscale('linear')
        ylim_exp = math.ceil(math.log10(min(erri)))-1
        ylim = [float(i) for i in features['yrange']]

    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=ylb,
           ylim=ylim, xticks=features['Ptrain'])
    ax.set_title(title)

    candidate = str(int(angle[idxmax]))
    while candidate in data[1][:itr]:
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
    fig.savefig('offline_erri_L'+str(itr)+'_'+features['scaled']+'.png')
    l = anc.pop(0)
    l.remove()
    lmin = lmin.pop(0)
    lmin.remove()

fig, ax = plt.subplots(1, tight_layout=True)
ax.set(xlabel='Iteration', ylabel=r'$\max{\Delta('+features['Param']+')}$',
       xlim=[0, max(data[0])+1], ylim=[1e-3, 1e0])
ax.semilogy(data[0], max_erri, 'k-o')

np.savetxt('iter'+tag+'.dat', data[0])
np.savetxt('max_erri_'+features['scaled']+'.dat', max_erri)
fig.savefig('max_erri_w_iter_'+features['scaled']+'.png')
