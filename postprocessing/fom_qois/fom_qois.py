def fom_qois(params, feature):
    import numpy as np
    from aux.mypostpro import read_nuss
    from aux.mypostpro import find_nearest
    from aux.mypostpro import cmean
    from aux.mypostpro import cvar
    from aux.mypostpro import cstd

    if feature == 'nu_1st2nd':
        fom_means = []
        fom_stds = []
        for param in params:
            # get the FOM data
            filename = '../../fom_nuss/nus_fom_'+str(param)
            data = read_nuss(filename)
            if (param == 10000):
                data[:, 2] = data[:, 2]/40
            else:
                data[:, 2] = data[:, 2]
            idx1 = find_nearest(data[:, 0], 0)
            idx2 = find_nearest(data[:, 0], 1000)
            nuss_fom = data[idx1:idx2, :]
            avgidx1 = find_nearest(data[:, 0], 501)
            fom_mean = cmean(nuss_fom[avgidx1:idx2], 2)
            fom_var = cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
            fom_sd = cstd(nuss_fom[avgidx1:idx2], fom_mean, 2)
            fom_means.append(fom_mean)
            fom_stds.append(fom_sd)
            print('FOM data at deg ' + str(param), ', Mean nu ', fom_mean, 'Std(Nu): ', fom_sd)
        data = np.column_stack((params, fom_means, fom_stds))
        data = data[data[:, 0].argsort()]
        return data
