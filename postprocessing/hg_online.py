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
import yaml
import math

setup.style(1)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Current directory is:', os.chdir(str(sys.argv[1])))
model = str(sys.argv[2])
ncand = int(sys.argv[3])
mode = str(sys.argv[4])
print('The model is:', model)
print("---------------------------------------------")

if len(sys.argv) >= 6:
    pt = '_sc_'+str(sys.argv[5])
else:
    pt = ''

with open('../hg_'+model+'_off/train_info'+pt+'.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
#with open('../hg_'+model+'_off_90/train_info'+pt+'.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)
data = []
for i, key in enumerate(features.keys()):
    data.append(features[key])

# make it list
P_test = [int(item) for item in features['Ptrain']]
#P_test = np.array(features['Ptrain'], dtype=int)

print("POD-hGreedy information:")
print("Iteration: ", data[0])
print("Anchor points: ", data[1])
print("N: ", data[2])
print("K: ", data[3])
print("---------------------------------------------")
Itr_list = data[0]
anch_list = data[1]
N_list = data[2]
K_list = data[3]
model_list = data[6]
fd = data[7]

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

for itr in Itr_list:
#   P_train = [int(item) for item in data[1][0:itr]]
    P_train = np.array(anch_list[0:itr], dtype=int)
#   P_test_anchor = online.get_ncand(P_test, P_train, ncand,
#                                    data[2][:itr], model, mode, pt)
    P_test_anchor = online.get_ncand_param(P_test, P_train, ncand,
                                     N_list[:itr], model_list, mode, fd, pt)
    print("ncand anchor points for each test parameter", P_test_anchor)

    fig, ax = plt.subplots(1, tight_layout=True)
#   erri_opt = online.get_opterri(P_test, P_train, data[2][:itr],
#                                 P_test_anchor, ax, colors, model, mode, pt)
    erri_opt = online.get_opterri_param(P_test, P_train, N_list[:itr],
                                  P_test_anchor, ax, colors, model_list, mode, fd, pt)

    mdual.append(max(erri_opt))
    mdual_1st.append(max(erri_opt[:5]))
    mdual_2nd.append(max(erri_opt[5:]))

    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\triangle$', ylim=[1e-3, 1e0], xticks=features['Ptrain'])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)

    ax.semilogy(P_test, erri_opt, 'k-', mfc="None", label=model.upper()+' est')
    ylim_exp = math.ceil(math.log10(min(erri_opt)))-1
    ax.set_ylim([10**ylim_exp, None])
    for k in P_train[:-1]:
        idx = list(P_test).index(k)
        ax.semilogy(k, erri_opt[idx], 'ro')
    k = P_train[-1]
    idx = list(P_test).index(k)
    ax.semilogy(k, erri_opt[idx], 'ro', label='Anchor points')

    ax.legend(loc=1, ncol=3, fontsize=10)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n Error esimates at '+r'$\mathcal{P}_{test}$')

    fig.savefig('online_erri_L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig)

    merr_his = []
    sderr_his = []
    m_his = []
    sd_his = []
    flderr_rom_his = []
    flderr_proj_his = []
 
    for i, train in enumerate(P_train):
#       angle, merr, sderr, m, sd = online.get_anchor_qoi(i, train,
#                                                         data[2][:itr], model, mode)
        angle, merr, sderr, m, sd = online.get_anchor_qoi_param(i, train,
                                                          N_list[:itr], model_list, mode, fd)
#       angle, flderr_rom, flderr_proj = online.get_anchor_flderr(i, train,
#                                                                 data[2][:itr], model, mode)
        angle, flderr_rom, flderr_proj = online.get_anchor_flderr_param(i, train,
                                                                  N_list[:itr], model_list, mode, fd)
        merr_his.append(merr)
        sderr_his.append(sderr)
        m_his.append(m)
        sd_his.append(sd)
        flderr_rom_his.append(flderr_rom)
        flderr_proj_his.append(flderr_proj)
    merr_all = np.array(merr_his)
    m_all = np.array(m_his)
    sderr_all = np.array(sderr_his)
    sd_all = np.array(sd_his)
    flderr_rom_all = np.array(flderr_rom_his)
    flderr_proj_all = np.array(flderr_proj_his)

    opt_merr_nu, opt_stderr_nu, opt_m_nu, opt_std_nu = \
        online.get_optqoi(merr_all, m_all, sderr_all, sd_all,
                          P_test, P_train, P_test_anchor, model_list, pt)
    opt_flderr_rom, opt_flderr_proj = \
        online.get_optflderr(flderr_rom_all, flderr_proj_all,
                             P_test, P_train, P_test_anchor, model_list, pt)

    fom_m_list = []
    fom_sd_list = []

    for i, test in enumerate(P_test):
#       filename = '../../../fom_nuss/nuss_fom_'+str(test)
        filename = '../fom_nuss/nus_fom_'+str(test)
        data = mypostpro.read_nuss(filename)
        if (str(test) == '10000'):
            data[:, 2] = data[:, 2]/40
        else:
            data[:, 2] = data[:, 2]
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
    fig5, ax5 = plt.subplots(1, tight_layout=True)
    fig6, ax6 = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax1.semilogy(angle, merr_all[i, :], **qoi_params)
        ax2.semilogy(angle, sderr_all[i, :], **qoi_params)
        ax3.plot(angle, m_all[i, :], **qoi_params)
        ax4.plot(angle, sd_all[i, :], **qoi_params)
        ax5.plot(angle, flderr_rom_all[i, :], **qoi_params)
        ax6.plot(angle, flderr_proj_all[i, :], **qoi_params)

    ax1.semilogy(angle, opt_merr_nu, 'k-o', mfc="None", label=model.upper()+' est')
    ax1.set(xlabel=r'$'+features['Param']+'$',
            ylabel=r'$\frac{|\langle \text{Nu} \rangle_s' +
            r'- \langle \tilde{\text{Nu}} \rangle_s|}' +
            r'{|\langle \text{Nu} \rangle_s|}$',
            ylim=[1e-5, 1e1], xticks=features['Ptrain'])

    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax1.semilogy(k, opt_merr_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax1.semilogy(k, opt_merr_nu[idx], 'ro', label='Anchor points')
    ax1.legend(loc=0, ncol=3)

    ylim_exp = math.ceil(math.log10(min(opt_merr_nu)))-1
    ax1.set_ylim([10**ylim_exp, None])
    ax1.set_xticklabels(ax.get_xticks(), rotation=45)
    ax1.set_title(r'POD-$h$Greedy, online stage:' +'\n relatie error in predicted mean Nu at '+r'$\mathcal{P}_{test}$')
    fig1.savefig('online_merr_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig1)
    print(max(opt_merr_nu))
    mnurelerr.append(max(opt_merr_nu))
    mnurelerr_1st.append(max(opt_merr_nu[:5]))
    mnurelerr_2nd.append(max(opt_merr_nu[5:]))
 
    ax2.semilogy(angle, opt_stderr_nu, 'k-o', mfc="None", label=model.upper()+' est')
    ax2.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$|\sigma_s - \widehat{\sigma_s}|/ \sigma_s$',
            ylim=[1e-2, 1e3], xticks=features['Ptrain'])
    ax2.set_xticklabels(ax.get_xticks(), rotation=45)
    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax2.semilogy(k, opt_stderr_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax2.semilogy(k, opt_stderr_nu[idx], 'ro', label='Anchor points')

    ax2.legend(loc=0, ncol=3)
    fig2.savefig('online_sderr_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig2)
 
    ax3.plot(angle, opt_m_nu, 'b-o', mfc="None", label=model.upper()+' est')
    ax3.plot(angle, fom_m_list, 'k-o', mfc="None", label='FOM')
    ax3.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\langle \text{Nu} \rangle_s$',
            ylim=[0, 4], xticks=features['Ptrain'])
    ax3.set_xticklabels(ax.get_xticks(), rotation=45)
    ax3.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted mean Nu at '+r'$\mathcal{P}_{test}$')

    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax3.plot(k, opt_m_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax3.plot(k, opt_m_nu[idx], 'ro', label='Anchor points')

    ylim_exp = math.ceil(math.log10(min(opt_m_nu)))-1
    ax3.set_ylim([10**ylim_exp, None])
    ax3.legend(loc=0, ncol=3)
    fig3.savefig('online_mean_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig3)
 
    ax4.plot(angle, opt_std_nu, 'b-o', mfc="None", label=model.upper()+' est')
    ax4.plot(angle, fom_sd_list, 'k-o', mfc="None", label='FOM')
    ax4.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\sigma_s$',
            ylim=[-0.01, 0.15], xticks=features['Ptrain'])
    ax4.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted Std(Nu) at '+r'$\mathcal{P}_{test}$')
    ax4.set_xticklabels(ax.get_xticks(), rotation=45)
    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax4.plot(k, opt_std_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax4.plot(k, opt_std_nu[idx], 'ro', label='Anchor points')

    ax4.legend(loc=0, ncol=3)
    fig4.savefig('online_std_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig4)

    ax5.plot(angle, opt_flderr_rom, 'k-o', mfc="None", label=model.upper()+' est')
    ax5.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle \|_{H^1}}$',
            ylim=[0, 1], xticks=features['Ptrain'])

    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax5.plot(k, opt_flderr_rom[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax5.plot(k, opt_flderr_rom[idx], 'ro', label='Anchor points')
    ax5.legend(loc=0, ncol=3)

    ylim_exp = math.ceil(math.log10(min(opt_flderr_rom)))-1
    ax5.set_ylim([10**ylim_exp, None])
    ax5.set_xticklabels(ax.get_xticks(), rotation=45)
    ax5.set_title(r'POD-$h$Greedy, online stage:'+'\n relative error in predicted mean flow at '+r'$\mathcal{P}_{test}$')

    fig5.savefig('online_fldrelerr_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig5)

    ax6.plot(angle, opt_flderr_proj, 'k-o', mfc="None", label=model.upper()+' est')
    ax6.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle \|_{H^1}}$',
            ylim=[0, 1], xticks=features['Ptrain'])
    for k in P_train[:-1]:
        idx = list(angle).index(k)
        ax6.plot(k, opt_flderr_proj[idx], 'ro')
    k = P_train[-1]
    idx = list(angle).index(k)
    ax6.plot(k, opt_flderr_proj[idx], 'ro', label='Anchor points')
    ax6.legend(loc=0, ncol=3)

    ylim_exp = math.ceil(math.log10(min(opt_flderr_proj)))-1
    ax6.set_ylim([10**ylim_exp, None])
    ax6.set_xticklabels(ax.get_xticks(), rotation=45)
    ax6.set_title(r'POD-$h$Greedy, online stage:'+'\n relative error in projected mean flow at '+r'$\mathcal{P}_{test}$')
    fig6.savefig('online_pfldrelerr_'+'L'+str(itr)+pt+'_'+str(ncand)+'.png')
    plt.close(fig6)

    np.savetxt('mnurelerr'+pt+'_'+str(ncand)+'_itr'+str(itr), mnurelerr)
    np.savetxt('mnurelerr_1st'+pt+'_'+str(ncand)+'_itr'+str(itr), mnurelerr_1st)
    np.savetxt('mnurelerr_2nd'+pt+'_'+str(ncand)+'_itr'+str(itr), mnurelerr_2nd)
    np.savetxt('nu_merr'+pt+'_'+str(ncand)+'_itr'+str(itr), opt_merr_nu)
    np.savetxt('nu_m'+pt+'_'+str(ncand)+'_itr'+str(itr), opt_m_nu)
    np.savetxt('nu_std'+pt+'_'+str(ncand)+'_itr'+str(itr), opt_std_nu)
    np.savetxt('rom_fldrelerr'+pt+'_'+str(ncand)+'_itr'+str(itr), opt_flderr_rom)
    np.savetxt('porj_fldrelerr'+pt+'_'+str(ncand)+'_itr'+str(itr), opt_flderr_proj)
