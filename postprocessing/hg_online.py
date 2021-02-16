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
colors = setup.color(0)
setup.text()


print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Current directory is:', os.chdir(str(sys.argv[1])))
model = str(sys.argv[2])
ncand = int(sys.argv[3])
ntest = 19
print('The model is:', model)
print("---------------------------------------------")

P_train_max = [0, 180, 140, 90, 160, 120, 170, 30, 150, 50]
N_max = [1, 1, 1, 60, 1, 24, 1, 1, 1, 46]
K_list = [500, 500, 500, 693, 500, 603, 500, 500, 500, 570]

if len(sys.argv) >= 5:
    pt = '_sc_'+str(sys.argv[4])
else:
    pt = ''


with open('../hg_'+model+'_off'+pt+'/train_info.csv', newline='') as f:
     reader = csv.reader(f)
     data = list(reader)

# make it list
P_test = np.linspace(0, 180, 19, dtype=int)

data[0] = [int(i) for i in data[0]]
P_train_max = [int(i) for i in data[1]]
N_max = data[2]
K_list = data[3]

mdual = []
mnurelerr = []
mdual_1st = []
mnurelerr_1st = []
mdual_2nd = []
mnurelerr_2nd = []

for itr in data[0]:
    P_train = P_train_max[0:itr]
    P_test_anchor = online.get_ncand(P_test, P_train, ncand, N_max[:itr])

    fig, ax = plt.subplots(1, tight_layout=True)
    erri_opt = online.get_opterri(P_test, P_train, N_max[:itr],
                                  P_test_anchor, ax, colors)

    mdual.append(max(erri_opt))
    mdual_1st.append(max(erri_opt[:5]))
    mdual_2nd.append(max(erri_opt[5:]))

    ax.set(xlabel=r'$\theta_g$', ylabel=r'$\triangle$',
           xticks=np.linspace(0, 180, 5, dtype=int),
           ylim=[1e-3, 1e1])

    ax.semilogy(P_test, erri_opt, 'k-', mfc="None", label='est')
    ax.legend(loc=1, ncol=5, fontsize=10)

    plt.savefig('online_erri_L'+str(itr)+'.png')
    plt.cla()

#    merr_his = []
#    sderr_his = []
#    m_his = []
#    sd_his = []
#
#    diff = []
#
#    k = 0
#    for i in P_train:
#        dirs = '../theta_'+str(i)+'/crom_info/nu/'
#        filename = 'angle.dat'
#        angle = np.loadtxt(dirs+filename)
#        filename = 'merr_N'+str(N_max[k])+'.dat'
#        merr = np.loadtxt(dirs+filename)
#        filename = 'sderr_N'+str(N_max[k])+'.dat'
#        sderr = np.loadtxt(dirs+filename)
#        filename = 'm_N'+str(N_max[k])+'.dat'
#        m = np.loadtxt(dirs+filename)
#        filename = 'sd_N'+str(N_max[k])+'.dat'
#        sd = np.loadtxt(dirs+filename)
#
#        merr_his.append(merr)
#        sderr_his.append(sderr)
#        m_his.append(m)
#        sd_his.append(sd)
#        
#        plt.figure(1)
#        plt.semilogy(angle, merr, '--o', color=colors[k], label=r'\textit{it} = '+str(k+1))
#        plt.figure(2)
#        plt.semilogy(angle, sderr,'--o',color=colors[k],mfc="None",label=r'\textit{it} = '+str(k+1))
#
#        plt.figure(3)
#        plt.plot(angle, m,'--o',color=colors[k],mfc="None",label=r'\textit{it} = '+str(k+1))
#        plt.figure(4)
#        plt.plot(angle, sd,'--o',color=colors[k],mfc="None",label=r'\textit{it} = '+str(k+1))
#        diff.append(abs(np.linspace(0,180,19,dtype=int)-i))
#        k += 1 
#
#    merr_comb=(((np.array(merr_his))))
#    m_comb=(((np.array(m_his))))
#    sderr_comb=(((np.array(sderr_his))))
#    sd_comb=(((np.array(sd_his))))
#
#    k = 0
#    opt_merr_nu = []
#    opt_stderr_nu = []
#    opt_m_nu = []
#    opt_std_nu = []
#    fom_m_list = []
#    fom_sd_list = []
#    for i in input_paras:
#        index = (P_train.index(near_anch[ncand_list[k], k]))
#        opt_merr_nu.append(merr_comb[index, k])
#        opt_stderr_nu.append(sderr_comb[index, k])
#        opt_m_nu.append(m_comb[index, k])
#        opt_std_nu.append(sd_comb[index, k])
#        filename = '../../../fom_nuss/nuss_fom_'+str(i)
#        data = mypost.read_nuss(filename); data[:,2] = data[:,2]/40
#        idx1 = find_nearest(data[:,0], 0)
#        idx2 = find_nearest(data[:,0], 1000)
#        nuss_fom = data[idx1:idx2,:]
#        avgidx1 = find_nearest(data[:,0], 501)
#        fom_mean = mypost.cmean(nuss_fom[avgidx1:idx2],2)
#        fom_var = mypost.cvar(nuss_fom[avgidx1:idx2],fom_mean,2)
#        fom_sd = mypost.csd(nuss_fom[avgidx1:idx2],fom_mean,2)
#        if num == 7:
#            print((near_anch[ncand_list[k], k]))
#            print(i,sd_comb[index, k], fom_sd, sderr_comb[index, k])
#
#        fom_m_list.append(fom_mean); fom_sd_list.append(fom_sd)
#        k=k+1
#
#    plt.figure(1)
#    print(np.max(opt_merr_nu))
#    plt.semilogy(angle, opt_merr_nu,'k-',mfc="None",label='est')
#    plt.figure(2)
#    plt.semilogy(angle, opt_stderr_nu,'k-',mfc="None",label='est')
#    mnurelerr.append(max(opt_merr_nu))
#    mnurelerr_1st.append(max(opt_merr_nu[:5]))
#    mnurelerr_2nd.append(max(opt_merr_nu[5:]))
#
#    plt.figure(3)
#    plt.plot(angle, opt_m_nu,'k-',mfc="None",label='est')
#    plt.plot(angle, fom_m_list,'k--o',mfc="None",label='FOM')
#
#    plt.figure(4)
#    plt.plot(angle, opt_std_nu,'k-',mfc="None",label='est')
#    plt.plot(angle, fom_sd_list,'k--o',mfc="None",label='FOM')
#
#    plt.figure(1)
#    plt.xlabel(r'$\theta_g$')
#    plt.ylabel(r'$|\langle \text{Nu} \rangle_s - \langle \widehat{\text{Nu}} \rangle_s|/|\langle \text{Nu} \rangle_s|$')
#    plt.legend(loc=0, ncol=5, fontsize=10)
#    plt.xticks(np.linspace(0, 180, 19, dtype=int), rotation=45)
#    ax = plt.figure(1).gca()
#    plt.ylim([1e-5, 1e1])
#    ax = plt.axes()
#    ax.axes.grid(True,axis='y')
#    plt.tight_layout()
#    plt.savefig('online_merr_'+'L'+str(L)+'.png')
#    plt.cla()
#
#    plt.figure(2)
#    plt.xlabel(r'$\theta_g$')
#    plt.ylabel(r'$|\sigma_s - \widehat{\sigma_s}|/ \sigma_s$')
#    plt.legend(loc=0, ncol=2, fontsize=10)
#    plt.xticks(np.linspace(0, 120, 13, dtype=int), rotation=45)
#    ax = plt.figure(2).gca()
#    plt.ylim([1e-2, 1e3])
#    plt.xlim([0, 120])
#    ax = plt.axes()
#    ax.axes.grid(True,axis='y')
#    plt.tight_layout()
#    plt.savefig('online_sderr_'+'L'+str(L)+'.png')
#    plt.cla()
#
#    plt.figure(3)
#    plt.xlabel(r'$\theta_g$')
#    plt.ylabel(r'$\langle \text{Nu} \rangle_s$')
#    plt.legend(loc=0, ncol=2, fontsize=10)
#    plt.xticks(np.linspace(0,180,5,dtype=int))
#    ax = plt.figure(3).gca()
#    plt.ylim([0, 4])
#    ax = plt.axes()
#    ax.axes.grid(True,axis='y')
#    plt.tight_layout()
#    plt.savefig('online_mean_'+'L'+str(L)+'.png')
#    plt.cla()
#
#    plt.figure(4)
#    plt.xlabel(r'$\theta_g$')
#    plt.ylabel(r'$\sigma_s$')
#    plt.legend(loc=0, ncol=2, fontsize=10)
#    plt.ylim([-0.01, 0.15])
#    plt.xticks(np.linspace(0,180,5,dtype=int))
#    ax = plt.figure(4).gca()
#    ax = plt.axes()
#    ax.axes.grid(True,axis='y')
#    plt.tight_layout()
#    plt.savefig('online_std_'+'L'+str(L)+'.png')
#    plt.cla()
#np.savetxt('mnurelerr_1st', mnurelerr_1st)
#np.savetxt('mnurelerr_2nd', mnurelerr_2nd)
