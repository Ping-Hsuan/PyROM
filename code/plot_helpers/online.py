def get_ncand(P_test, P_train, ncand, N, model, scaled=''):
    import numpy as np

    P_test_anchor = []
    # Find out the nearest anchor(s) point to each testing parameter
    for i, test in enumerate(P_test):
        erri = []
        near_anch = []
        # distance between two parameters is used
        tmp = abs(test-P_train)
        for j in range(ncand):
            # find out the index corresponding to the closest anchor point
            minidx = np.argmin(tmp)
            near_anch.append(P_train[minidx])

            # do not revisit the same anchor again
#           aflag = test in P_train
#           print(aflag, test, P_train)
#           if aflag:
#               pass
#           else:
#               tmp[minidx] = 1e8

            dirs = '../theta_'+str(int(P_train[minidx]))+'/' + \
                   model+'_parameter_'+str(int(P_train[minidx]))+'/dual_norm/'
            fname = 'erri_N'+str(N[minidx])+scaled+'.dat'
            dual_norm = np.loadtxt(dirs+fname)
            data = np.array(dual_norm).astype(np.float64)
            erri.append(data[0])
        idx = erri.index(min(erri))

        P_test_anchor.append(near_anch[idx])
    return P_test_anchor


def get_opterri(P_test, P_train, N, P_test_anchor, ax, colors, model,
                scaled=''):
    import numpy as np
    # get erri with theta_g at each anchor points
    erri_his = []
    for i, train in enumerate(P_train):
        dirs = '../theta_'+str(train)+'/'+model+'_parameter_'+str(train) + \
               '/dual_norm/'
        filename = 'angle_list.dat'
        angle = np.loadtxt(dirs+filename)
        filename = 'erri_N'+str(N[i])+scaled+'.dat'
        erri = np.loadtxt(dirs+filename)

        erri_his.append(erri)
        ax.semilogy(angle, erri, '--o', color=colors[i], mfc="None",
                    label=r'\textit{it} = '+str(i+1))

    erri_comb = np.array(erri_his)
    erri_opt = []

    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        erri_opt.append(erri_comb[index, i])
    return erri_opt


def get_anchor_qoi(i, train, N, model):
    import numpy as np

    dirs = '../theta_'+str(train)+'/'+model+'_parameter_'+str(train)+'/nu/'
    filename = 'angle.dat'
    angle = np.loadtxt(dirs+filename)
    filename = 'merr_N'+str(N[i])+'.dat'
    merr = np.loadtxt(dirs+filename)
    filename = 'stderr_N'+str(N[i])+'.dat'
    sderr = np.loadtxt(dirs+filename)
    filename = 'mnu_N'+str(N[i])+'.dat'
    m = np.loadtxt(dirs+filename)
    filename = 'stdnu_N'+str(N[i])+'.dat'
    sd = np.loadtxt(dirs+filename)

    return angle, merr, sderr, m, sd


def get_optqoi(merr_all, m_all, sderr_all, sd_all, P_test, P_train,
               P_test_anchor, model, scaled=''):
    opt_merr_nu = []
    opt_stderr_nu = []
    opt_m_nu = []
    opt_std_nu = []
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        opt_merr_nu.append(merr_all[index, i])
        opt_stderr_nu.append(sderr_all[index, i])
        opt_m_nu.append(m_all[index, i])
        opt_std_nu.append(sd_all[index, i])
    return opt_merr_nu, opt_stderr_nu, opt_m_nu, opt_std_nu


def get_anchor_flderr(i, train, N, model):
    # return both the projection and rom fld relative errro
    import numpy as np

    dirs = '../theta_'+str(train)+'/'+model+'_parameter_'+str(train)+'/relerr/'
    filename = 'angle_list.dat'
    angle = np.loadtxt(dirs+filename)
    filename = 'rom_relerr_N'+str(N[i])+'.dat'
    fldrelerr_rom = np.loadtxt(dirs+filename)
    filename = 'proj_relerr_N'+str(N[i])+'.dat'
    fldrelerr_proj = np.loadtxt(dirs+filename)

    return angle, fldrelerr_rom, fldrelerr_proj


def get_optflderr(flderr_rom, flderr_proj, P_test, P_train,
                  P_test_anchor, model, scaled=''):

    opt_flderr_rom = []
    opt_flderr_proj = []
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        opt_flderr_rom.append(flderr_rom[index, i])
        opt_flderr_proj.append(flderr_proj[index, i])
    return opt_flderr_rom, opt_flderr_proj
