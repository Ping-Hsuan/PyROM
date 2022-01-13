def plt_est_erri(itr, ncand, param, erri_all, opt_erri, P_train, features, model):
    import math
    import matplotlib.pyplot as plt
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.plot(param, erri_all[i, :], **qoi_params)
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\triangle$', ylim=[1e-3, 1e0], xticks=features['Ptrain'])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)

    ax.semilogy(param, opt_erri, 'k-', mfc="None", label=model.upper()+' est')
    ylim_exp = math.ceil(math.log10(min(opt_erri)))-1
    ax.set_ylim([10**ylim_exp, None])
    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.semilogy(k, opt_erri[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.semilogy(k, opt_erri[idx], 'ro', label='Anchor points')

    ax.legend(loc=1, ncol=3, fontsize=10)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n Error esimates at '+r'$\mathcal{P}_{test}$')

    fig.savefig('online_erri_L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    return


def est_nu_1st2nd(features, P_train, N_list, model_list, mode, fd):
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import online
    import numpy as np
    merr_his = []
    m_his = []
    sd_his = []
    for i, train in enumerate(P_train):
#       angle, merr, sderr, m, sd = online.get_anchor_qoi(i, train,
#                                                         data[2][:itr], model, mode)
        angle, merr, m, sd = online.get_anchor_qoi_param(i, train,
                                                          N_list, model_list, mode, fd)
        idx = [angle.index(i) for i in features['Ptrain']]
        angle = np.asarray(angle)[idx]
        merr = np.asarray(merr)[idx]
        m = np.asarray(m)[idx]
        sd = np.asarray(sd)[idx]
        merr_his.append(merr)
        m_his.append(m)
        sd_his.append(sd)
    merr_all = np.array(merr_his)
    m_all = np.array(m_his)
    sd_all = np.array(sd_his)
    return angle, merr_all, m_all, sd_all


def get_FOM_nu_1st2nd(P_test):
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import re
    import pandas as pd
    from reader import find_files

    fom_m_list = []
    fom_sd_list = []

    for i, test in enumerate(P_test):
        fname = 'nus_mom.csv'
        filenames = find_files(fname, '../')
        filenames = find_files(fname, '../../')
        for f in filenames:
            if 'Ra_'+str(test) in re.split('[/]', f):
                filename = f
        data = pd.read_csv(filename)
        fom_mean = data['mean']
        fom_std = data[' std']

        fom_m_list.append(fom_mean)
        fom_sd_list.append(fom_std)
    return fom_m_list, fom_sd_list


def plt_est_mnu(itr, ncand, param, m_all, opt_m_nu, P_train, features, model, fom_m_list):
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.plot(param, m_all[i, :], **qoi_params)

    ax.plot(param, opt_m_nu, 'b-o', mfc="None", label=model.upper()+' est')
    ax.plot(param, fom_m_list, 'k-o', mfc="None", label='FOM')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\langle \textrm{Nu} \rangle_s$',
           ylim=[3, 6], xticks=features['Ptrain'])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted mean Nu at '+r'$\mathcal{P}_{test}$')

    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_m_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_m_nu[idx], 'ro', label='Anchor points')

    ax.legend(loc=0, ncol=3)
    fig.savefig('online_mean_'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    np.savetxt('nu_m'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_m_nu)), delimiter=',', header=features['Param']+', nu_m', comments="")


def plt_est_stdnu(itr, ncand, param, std_all, opt_std_nu, P_train, features, model, fom_std_list):
    import matplotlib.pyplot as plt
    import numpy as np
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.plot(param, std_all[i, :], **qoi_params)
    ax.plot(param, opt_std_nu, 'b-o', mfc="None", label=model.upper()+' est')
    ax.plot(param, fom_std_list, 'k-o', mfc="None", label='FOM')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\sigma_s$',
           xticks=features['Ptrain'])
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted Std(Nu) at '+r'$\mathcal{P}_{test}$')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_std_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_std_nu[idx], 'ro', label='Anchor points')

    ax.legend(loc=0, ncol=3)
    fig.savefig('online_std_'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    np.savetxt('nu_std'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_std_nu)), delimiter=',', header=features['Param']+', nu_std', comments="")


def plt_est_mnuerr(itr, ncand, param, merr_all, opt_merr_nu, P_train, features, model):
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.semilogy(param, merr_all[i, :], **qoi_params)

    ax.semilogy(param, opt_merr_nu, 'k-o', mfc="None", label=model.upper()+' est')
    ax.set(xlabel=r'$'+features['Param']+'$',
           ylabel=r'$\frac{|\langle \textrm{Nu} \rangle_s' +
           r'- \langle \tilde{\textrm{Nu}} \rangle_s|}' +
           r'{|\langle \textrm{Nu} \rangle_s|}$',
           ylim=[1e-5, 1e1], xticks=features['Ptrain'])

    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.semilogy(k, opt_merr_nu[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.semilogy(k, opt_merr_nu[idx], 'ro', label='Anchor points')
    ax.legend(loc=0, ncol=3)

    ylim_exp = math.ceil(math.log10(min(opt_merr_nu)))-1
    ax.set_ylim([10**ylim_exp, None])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:' + '\n relatie error in predicted mean Nu at '+r'$\mathcal{P}_{test}$')
    fig.savefig('online_merr_'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    print(f'Itr: {itr}, Max relative error in mean Nu: {max(opt_merr_nu)}')
    np.savetxt('nu_merr'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_merr_nu)), delimiter=',', header=features['Param']+', nu_merr', comments="")


def est_mean_fld_relerr(features, P_train, N_list, model_list, mode, fd):
    import numpy as np
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import online
    flderr_rom_his = []
    flderr_proj_his = []
    for i, train in enumerate(P_train):
        angle, flderr_rom, flderr_proj = online.get_anchor_flderr_param(i, train, N_list, model_list, mode, fd)
        idx = [angle.index(j) for j in features['Ptrain']]
        angle = np.asarray(angle)[idx]
        flderr_rom = np.asarray(flderr_rom)[idx]
        flderr_proj = np.asarray(flderr_proj)[idx]
        flderr_rom_his.append(flderr_rom)
        flderr_proj_his.append(flderr_proj)
    flderr_rom_all = np.array(flderr_rom_his)
    flderr_proj_all = np.array(flderr_proj_his)
    return angle, flderr_rom_all, flderr_proj_all


def plt_est_rom_mfldrelerr(itr, ncand, param, opt_flderr_rom, P_train, features, model):
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(1, tight_layout=True)

    ax.plot(param, opt_flderr_rom, 'k-o', mfc="None", label=model.upper()+' est')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle \|_{H^1}}$', ylim=[0, 0.7], xticks=features['Ptrain'])

    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_flderr_rom[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_flderr_rom[idx], 'ro', label='Anchor points')
    ax.legend(loc=0, ncol=3)

    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n relative error in predicted mean flow at '+r'$\mathcal{P}_{test}$')

    fig.savefig('online_fldrelerr_'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)

    print(f'Itr: {itr}, Max relative error in predicted mean flow: {max(opt_flderr_rom)}')

    np.savetxt('rom_fldrelerr'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_flderr_rom)), delimiter=',', header=features['Param']+', rom_fldrelerr', comments="")
    return


def plt_est_proj_mfldrelerr(itr, ncand, param, opt_flderr_proj, P_train, features, model):
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(1, tight_layout=True)

    ax.plot(param, opt_flderr_proj, 'k-o', mfc="None", label=model.upper()+' est')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle\bf{u} \rangle\|_{H^1}}$', ylim=[0, 0.1], xticks=features['Ptrain'])
    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_flderr_proj[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_flderr_proj[idx], 'ro', label='Anchor points')
    ax.legend(loc=0, ncol=3)

    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n relative error in projected mean flow at '+r'$\mathcal{P}_{test}$')
    fig.savefig('online_pfldrelerr_'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    print(f'Itr: {itr}, Max relative error in predicted mean flow: {max(opt_flderr_proj)}')

    np.savetxt('proj_fldrelerr'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_flderr_proj)), delimiter=',', header=features['Param']+', proj_fldrelerr', comments="")
    return


def get_anchor_mtke(i, train, N, model, mode, fd, feature):
    import pandas as pd
    import reader

    if model[i] == 'l-rom':
        fname = feature+'_N'+str(N[i])+'_'+fd[i].strip('0')+'_'+mode+'.csv'
    elif model[i] == 'l-rom-df':
        fname = feature+'_N'+str(N[i])+'_0'+fd[i]+'.csv'
    else:
        fname = feature+'_N'+str(N[i])+'.csv'
    filenames = reader.find_files(fname, '../')
    filenames = reader.find_files(fname, '../../')
    for f in filenames:
        if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
            filename = f
    data = pd.read_csv(filename)
    param = data['Ra'].tolist()
    data1 = data[feature].tolist()

    return param, data1


def est_mtke(features, P_train, N_list, model_list, mode, fd):
    import numpy as np
    list1 = []
    for i, train in enumerate(P_train):
        param, mtke = get_anchor_mtke(i, train, N_list, model_list, mode, fd, 'mtke')
        idx = [param.index(i) for i in features['Ptrain']]
        param = np.asarray(param)[idx]
        mtke = np.asarray(mtke)[idx]
        list1.append(mtke)
    mtke = np.array(list1)
    return param, mtke


def est_mtfluc(features, P_train, N_list, model_list, mode, fd):
    import numpy as np
    list1 = []
    for i, train in enumerate(P_train):
        param, mtke = get_anchor_mtke(i, train, N_list, model_list, mode, fd, 'mtfluc')
        idx = [param.index(i) for i in features['Ptrain']]
        param = np.asarray(param)[idx]
        mtfluc = np.asarray(mtke)[idx]
        list1.append(mtfluc)
    mtfluc = np.array(list1)
    return param, mtfluc


def get_FOM_mtke(P_test):
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import re
    import numpy as np
    from reader import find_files

    fom = []
    for i, test in enumerate(P_test):
        fname = 'tmtke'
        filenames = find_files(fname, '../')
        filenames = find_files(fname, '../../')
        for f in filenames:
            if 'Ra_'+str(test) in re.split('[/]', f):
                filename = f
        data = np.loadtxt(filename)
        fom.append(data)
    return fom


def get_FOM_mtfluc(P_test):
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import re
    import numpy as np
    from reader import find_files

    fom = []
    for i, test in enumerate(P_test):
        fname = 'tmtfluc'
        filenames = find_files(fname, '../')
        filenames = find_files(fname, '../../')
        for f in filenames:
            if 'Ra_'+str(test) in re.split('[/]', f):
                filename = f
        data = np.loadtxt(filename)
        fom.append(data)
    return fom


def get_optmtke(mtke, P_test, P_train, P_test_anchor, model):
    list1 = []
    P_train = list(P_train)
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        list1.append(mtke[index, i])
    return list1


def plt_est_mtke(itr, ncand, param, mtke, opt_mtke, P_train, features, model, fom_mtke):
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.plot(param, mtke[i, :], **qoi_params)

    ax.plot(param, opt_mtke, 'b-o', mfc="None", label=model.upper()+' est')
    ax.plot(param, fom_mtke, 'k-o', mfc="None", label='FOM')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\langle \textrm{TKE} \rangle_s$',
           ylim=[0, 0.5], xticks=features['Ptrain'])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted mean TKE at '+r'$\mathcal{P}_{test}$')

    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_mtke[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_mtke[idx], 'ro', label='Anchor points')

    ax.legend(loc=0, ncol=3)
    fig.savefig('online_mtke'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    np.savetxt('mtke'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_mtke)), delimiter=',', header=features['Param']+', mtke', comments="")


def plt_est_mtfluc(itr, ncand, param, mtfluc, opt_mtfluc, P_train, features, model, fom_mtfluc):
    import numpy as np
    import matplotlib.pyplot as plt
    from figsetup.color import color

    colors = color(0)

    fig, ax = plt.subplots(1, tight_layout=True)

    for i, train, in enumerate(P_train):
        qoi_params = {'c': colors[i], 'marker': 'o', 'mfc': 'None',
                      'linestyle': '--', 'label': r'\textit{it} = '+str(i+1)}
        ax.plot(param, mtfluc[i, :], **qoi_params)

    ax.plot(param, opt_mtfluc, 'b-o', mfc="None", label=model.upper()+' est')
    ax.plot(param, fom_mtfluc, 'k-o', mfc="None", label='FOM')
    ax.set(xlabel=r'$'+features['Param']+'$', ylabel=r'$\langle T_{fluc} \rangle_s$',
           ylim=[0, 1], xticks=features['Ptrain'])
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_title(r'POD-$h$Greedy, online stage:'+'\n predicted mean temperature fluctuation at '+r'$\mathcal{P}_{test}$')

    for k in P_train[:-1]:
        idx = list(param).index(k)
        ax.plot(k, opt_mtfluc[idx], 'ro')
    k = P_train[-1]
    idx = list(param).index(k)
    ax.plot(k, opt_mtfluc[idx], 'ro', label='Anchor points')

    ax.legend(loc=0, ncol=3)
    fig.savefig('online_mtfluc'+'L'+str(itr)+'_'+str(ncand)+'.png')
    plt.close(fig)
    np.savetxt('mtfluc'+'_'+str(ncand)+'_itr'+str(itr)+'.csv', np.column_stack((param, opt_mtfluc)), delimiter=',', header=features['Param']+', mtfluc', comments="")

