import numpy as np
import sys
import os
import matplotlib.pyplot as plt
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import online
from reader import erri_w_theta
import checker
import mypostpro
import collections
import csv

setup.style(1)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Current directory is:', os.chdir(str(sys.argv[1])))
model = str(sys.argv[2])
ntest = 19
print('The model is:', model)
print("---------------------------------------------")

if len(sys.argv) >= 5:
    pt = '_sc_'+str(sys.argv[4])
else:
    pt = ''

with open('../pg_'+model+'_off/train_info'+pt+'.csv', newline='') as f:
     reader = csv.reader(f)
     data = list(reader)

# make it list
P_test = np.linspace(0, 180, 19, dtype=int)

data[0] = [int(i) for i in data[0]]
P_train_max = [int(i) for i in data[1]]
N_max = data[2]
K_list = data[3]
print("POD-pGreedy information:")
print("Iteration: ", data[0])
print("Anchor points: ", data[1])
print("N: ", data[2])
print("K: ", data[3])
print("---------------------------------------------")

if len(data[0]) > 10:
    colors = setup.color(1)
else:
    colors = setup.color(0)

mdual = []
mnurelerr = []
mdual_1st = []
mnurelerr_1st = []
mdual_2nd = []
mnurelerr_2nd = []

for itr in data[0]:
    P_train = P_train_max[0:itr]
    merr_his = []
    sderr_his = []
    m_his = []
    sd_his = []

    for i, train in enumerate(P_train):
        angle, merr, sderr, m, sd = online.get_anchor_qoi(i, train,
                                                          N_max[:itr], model)
        merr_his.append(merr)
        sderr_his.append(sderr)
        m_his.append(m)
        sd_his.append(sd)

    merr_all = np.array(merr_his)
    m_all = np.array(m_his)
    sderr_all = np.array(sderr_his)
    sd_all = np.array(sd_his)

    fom_m_list = []
    fom_sd_list = []

    for i, test in enumerate(P_test):
        filename = '../../../fom_nuss/nuss_fom_'+str(test)
        data = mypostpro.read_nuss(filename)
        data[:, 2] = data[:, 2]/40
        idx1 = mypostpro.find_nearest(data[:, 0], 0)
        idx2 = mypostpro.find_nearest(data[:, 0], 1000)
        nuss_fom = data[idx1:idx2, :]
        avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
        fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
        fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
        fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)

        fom_m_list.append(fom_mean)
        fom_sd_list.append(fom_sd)

    fig1, ax1 = plt.subplots(1, tight_layout=True)
    fig2, ax2 = plt.subplots(1, tight_layout=True)
    fig3, ax3 = plt.subplots(1, tight_layout=True)
    fig4, ax4 = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax1.semilogy(angle, merr_all[i, :], **qoi_params)
        ax2.semilogy(angle, sderr_all[i, :], **qoi_params)
        ax3.plot(angle, m_all[i, :], **qoi_params)
        ax4.plot(angle, sd_all[i, :], **qoi_params)

    ax1.set(xlabel=r'$\theta_g$',
            ylabel=r'$\frac{|\langle \text{Nu} \rangle_s' +
            r'- \langle \widehat{\text{Nu}} \rangle_s|}' +
            r'{|\langle \text{Nu} \rangle_s|}$',
            xticks=np.linspace(0, 180, 19, dtype=int), ylim=[1e-5, 1e1])
    ax1.legend(loc=0, ncol=3)
    fig1.savefig('online_merr_'+'L'+str(itr)+pt+'.png')
    plt.close(fig1)

    ax2.set(xlabel=r'$\theta_g$',
            ylabel=r'$|\sigma_s - \widehat{\sigma_s}|/ \sigma_s$',
            xticks=np.linspace(0, 120, 13, dtype=int),
            ylim=[1e-2, 1e3], xlim=[0, 120])
    ax2.legend(loc=0, ncol=3)
    fig2.savefig('online_sderr_'+'L'+str(itr)+pt+'.png')
    plt.close(fig2)

    ax3.plot(angle, fom_m_list, 'k--o', mfc="None", label='FOM')
    ax3.set(xlabel=r'$\theta_g$', ylabel=r'$\langle \text{Nu} \rangle_s$',
            xticks=np.linspace(0, 180, 5, dtype=int), ylim=[0, 4])
    ax3.legend(loc=0, ncol=3)
    fig3.savefig('online_mean_'+'L'+str(itr)+pt+'.png')
    plt.close(fig3)

    ax4.plot(angle, fom_sd_list, 'k--o', mfc="None", label='FOM')
    ax4.set(xlabel=r'$\theta_g$', ylabel=r'$\sigma_s$',
            ylim=[-0.01, 0.15], xticks=np.linspace(0, 180, 5, dtype=int))
    ax4.legend(loc=0, ncol=3)
    fig4.savefig('online_std_'+'L'+str(itr)+pt+'.png')
    plt.close(fig4)

#np.savetxt('mnurelerr_1st'+pt+'_'+str(ncand), mnurelerr_1st)
#np.savetxt('mnurelerr_2nd'+pt+'_'+str(ncand), mnurelerr_2nd)
