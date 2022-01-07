def get_ncand(P_test, P_train, ncand, N, model, mode, scaled=''):
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
            if 0 in tmp:
                minidx = np.argmin(tmp)
                near_anch.append(P_train[minidx])
            else:
                minidx = np.argmin(tmp)
                near_anch.append(P_train[minidx])
                tmp[minidx] = 1e8

            # do not revisit the same anchor again
#           aflag = test in P_train
#           print(aflag, test, P_train)
#           if aflag:
#               pass
#           else:
#               tmp[minidx] = 1e8

            dirs = '../theta_'+str(int(P_train[minidx]))+'/' + \
                   model+'_parameter_'+str(int(P_train[minidx]))+'/dual_norm/'
            fname = 'erri_N'+str(N[minidx])+scaled+'_'+mode+'.dat'
            dual_norm = np.loadtxt(dirs+fname)
            data = np.array(dual_norm).astype(np.float64)
            erri.append(data[i])
        idx = erri.index(min(erri))
        P_test_anchor.append(near_anch[idx])
    return P_test_anchor


def get_ncand_param(P_test, P_train, ncand, N, model, mode, fd, scaled=''):
    import numpy as np
    import pandas as pd
    import reader
    import re

    P_test_anchor = []
    # Find out the nearest anchor(s) point to each testing parameter
    for i, test in enumerate(P_test):
        erri = []
        near_anch = []
        # distance between two parameters is used
        tmp = abs(test-P_train)
        for j in range(ncand):
            # find out the index corresponding to the closest anchor point
            if 0 in tmp:
                minidx = np.argmin(tmp)
                near_anch.append(P_train[minidx])
            else:
                minidx = np.argmin(tmp)
                near_anch.append(P_train[minidx])
                tmp[minidx] = 1e8

            # do not revisit the same anchor again
#           aflag = test in P_train
#           print(aflag, test, P_train)
#           if aflag:
#               pass
#           else:
#               tmp[minidx] = 1e8

            if model[minidx] == 'l-rom':
                fname = 'erri_N'+str(N[minidx])+'_'+fd[minidx].strip('0')+scaled+'_'+mode+'.dat'
            elif model[minidx] == 'l-rom-df':
                fname = 'dual_norm_N'+str(N[minidx])+'_0'+fd[minidx]+scaled+'.csv'
            else:
                fname = 'erri_N'+str(N[minidx])+scaled+'_'+mode+'.dat'
                fname = 'dual_norm_N'+str(N[minidx])+scaled+'.csv'
#           dual_norm = np.loadtxt(dirs+fname)
#           data = np.array(dual_norm).astype(np.float64)
            filenames = reader.find_files(fname, '../')
#           print(['Ra'+str(int(P_train[minidx])), model[minidx], str(N[minidx])])
            for f in filenames:
                if all(x in f for x in ['Ra'+str(int(P_train[minidx])), model[minidx], str(N[minidx])]):
#               if 'Ra'+str(int(P_train[minidx])) in re.split('[/_]', f) and model[minidx] in re.split('[/_]', f):
#               if 'Re'+str(int(P_train[minidx])) in re.split('[/_]', f):
                    filename = f
            data = pd.read_csv(filename)
            erri.append(data['dual_norm'][i])
        idx = erri.index(min(erri))
        P_test_anchor.append(near_anch[idx])
    return P_test_anchor


def get_opterri(P_test, P_train, N, P_test_anchor, ax, colors, model, mode,
                scaled=''):
    import numpy as np
    # get erri with theta_g at each anchor points
    erri_his = []
    for i, train in enumerate(P_train):
        dirs = '../theta_'+str(train)+'/'+model[i]+'_parameter_'+str(train) + \
               '/dual_norm/'
        filename = 'angle_list_'+mode+'.dat'
        angle = np.loadtxt(dirs+filename)
        filename = 'erri_N'+str(N[i])+scaled+'_'+mode+'.dat'
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


def get_opterri_param(P_test, P_train, N, P_test_anchor, ax, colors, model, mode, fd,
                scaled=''):
    import numpy as np
    import pandas as pd
    import reader
    import re
    # get erri with theta_g at each anchor points
    erri_his = []
    for i, train in enumerate(P_train):
        if model[i] == 'l-rom':
            fname = 'dual_norm_N'+str(N[i])+'_'+fd[i].strip('0')+scaled+'_'+mode+'.dat'
        elif model[i] == 'l-rom-df':
            fname = 'dual_norm_N'+str(N[i])+'_0'+fd[i]+scaled+'.csv'
        else:
            fname = 'dual_norm_N'+str(N[i])+scaled+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
#           if 'Ra'+str(train) in re.split('[/_]', f):
#           if 'Re'+str(train) in re.split('[/_]', f):
                filename = f
                print(filename)
        data = pd.read_csv(filename)

        erri_his.append(data.iloc[:, 1])
        ax.semilogy(data.iloc[:, 0], data.iloc[:, 1], '--o', color=colors[i], mfc="None",
                    label=r'\textit{it} = '+str(i+1))

    erri_comb = np.array(erri_his)
    erri_opt = []

    P_train = list(P_train)
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        erri_opt.append(erri_comb[index, i])
    return erri_opt


def get_anchor_qoi(i, train, N, model, mode):
    import numpy as np

    dirs = '../theta_'+str(train)+'/'+model+'_parameter_'+str(train)+'/nu/'
    filename = 'angle_'+mode+'.dat'
    angle = np.loadtxt(dirs+filename)
    filename = 'merr_N'+str(N[i])+'_'+mode+'.dat'
    merr = np.loadtxt(dirs+filename)
    filename = 'stderr_N'+str(N[i])+'_'+mode+'.dat'
    sderr = np.loadtxt(dirs+filename)
    filename = 'mnu_N'+str(N[i])+'_'+mode+'.dat'
    m = np.loadtxt(dirs+filename)
    filename = 'stdnu_N'+str(N[i])+'_'+mode+'.dat'
    sd = np.loadtxt(dirs+filename)

    return angle, merr, sderr, m, sd


def get_anchor_qoi_param(i, train, N, model, mode, fd):
    import numpy as np
    import pandas as pd
    import re
    import reader

    dirs = '../ra_'+str(train)+'_theta_90/'+model[i]+'_parameter_ra_'+str(train)+'/nu/'
    if model[i] == 'l-rom':
        fname = 'mnurelerr_N'+str(N[i])+'_'+fd[i].strip('0')+'_'+mode+'.csv'
    elif model[i] == 'l-rom-df':
        fname = 'mnurelerr_N'+str(N[i])+'_0'+fd[i]+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        param = data['Ra']
        merr = data['mnurelerr']

        fname = 'mnu_N'+str(N[i])+'_0'+fd[i]+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        m = data['mnu']
        
        fname = 'std_nu_N'+str(N[i])+'_0'+fd[i]+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        std = data['std_nu']
    else:
#       filename = 'param_'+mode+'.dat'
#       angle = np.loadtxt(dirs+filename)
#       filename = 'merr_N'+str(N[i])+'_'+mode+'.dat'
#       merr = np.loadtxt(dirs+filename)
#       filename = 'stderr_N'+str(N[i])+'_'+mode+'.dat'
#       sderr = np.loadtxt(dirs+filename)
#       filename = 'mnu_N'+str(N[i])+'_'+mode+'.dat'
#       m = np.loadtxt(dirs+filename)
#       filename = 'stdnu_N'+str(N[i])+'_'+mode+'.dat'
#       sd = np.loadtxt(dirs+filename)
        fname = 'mnurelerr_N'+str(N[i])+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        param = data['Ra']
        merr = data['mnurelerr']

        fname = 'mnu_N'+str(N[i])+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        m = data['mnu']
        
        fname = 'std_nu_N'+str(N[i])+'.csv'
        filenames = reader.find_files(fname, '../')
        for f in filenames:
#           if 'Ra'+str(train) in re.split('[/_]', f):
            if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
                filename = f
        data = pd.read_csv(filename)
        std = data['std_nu']

    return param, merr, m, std


def get_optqoi(merr_all, m_all, sd_all, P_test, P_train,
               P_test_anchor, model, scaled=''):
    opt_merr_nu = []
    opt_m_nu = []
    opt_std_nu = []
    P_train = list(P_train)
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        opt_merr_nu.append(merr_all[index, i])
        opt_m_nu.append(m_all[index, i])
        opt_std_nu.append(sd_all[index, i])
    return opt_merr_nu, opt_m_nu, opt_std_nu


def get_anchor_flderr(i, train, N, model, mode):
    # return both the projection and rom fld relative errro
    import numpy as np

    dirs = '../theta_'+str(train)+'/'+model+'_parameter_'+str(train)+'/mrelerr/'
    filename = 'angle_list_'+mode+'.dat'
    angle = np.loadtxt(dirs+filename)
    filename = 'rom_relerr_N'+str(N[i])+'_'+mode+'.dat'
    fldrelerr_rom = np.loadtxt(dirs+filename)
    filename = 'proj_relerr_N'+str(N[i])+'_'+mode+'.dat'
    fldrelerr_proj = np.loadtxt(dirs+filename)

    return angle, fldrelerr_rom, fldrelerr_proj


def get_anchor_flderr_param(i, train, N, model, mode, fd):
    # return both the projection and rom fld relative errro
    import numpy as np
    import pandas as pd
    import reader
    import re

    dirs = '../ra_'+str(train)+'_theta_90/'+model[i]+'_parameter_ra_'+str(train)+'/mrelerr/'
    dirs = '../re'+str(train)+'/'+model[i]+'_parameter_Re'+str(train)+'/mrelerr_h1/'
    if model[i] == 'l-rom':
        filename = 'param_list_'+mode+'.dat'
        angle = np.loadtxt(dirs+filename)
        filename = 'rom_relerr_N'+str(N[i])+'_'+fd[i]+'_'+mode+'.dat'
        fldrelerr_rom = np.loadtxt(dirs+filename)
        filename = 'proj_relerr_N'+str(N[i])+'_'+mode+'.dat'
        fldrelerr_proj = np.loadtxt(dirs+filename)
    elif model[i] == 'l-rom-df':
        fname = 'mrelerr_N'+str(N[i])+'_0'+fd[i]+'.csv'
    else:
        fname = 'mrelerr_N'+str(N[i])+'.csv'

    filenames = reader.find_files(fname, '../')
    for f in filenames:
        if all(x in f for x in ['Ra'+str(train), model[i], str(N[i])]):
#       if 'Ra'+str(train) in re.split('[/_]', f):
#       if 'Re'+str(train) in re.split('[/_]', f):
            filename = f
    data = pd.read_csv(filename)

    return [data[i].to_numpy() for i in data.columns]


def get_optflderr(flderr_rom, flderr_proj, P_test, P_train,
                  P_test_anchor, model, scaled=''):

    opt_flderr_rom = []
    opt_flderr_proj = []
    P_train = list(P_train)
    for i, test in enumerate(P_test):
        index = P_train.index(P_test_anchor[i])
        opt_flderr_rom.append(flderr_rom[index, i])
        opt_flderr_proj.append(flderr_proj[index, i])
    return opt_flderr_rom, opt_flderr_proj
