def nu_momentum(T0, Tf):
    import numpy as np
    from aux.mypostpro import find_nearest
    from aux.mypostpro import cmean
    from aux.mypostpro import cvar
    from aux.mypostpro import cstd
    import pandas as pd

    # get the FOM data
    filename = './nus_his.csv'
    data = pd.read_csv(filename).to_numpy()
    idx1 = find_nearest(data[:, 0], 0)
    idx2 = find_nearest(data[:, 0], int(Tf))
    nuss_fom = data[idx1:idx2, :]
    avgidx1 = find_nearest(data[:, 0], int(T0))
    print(avgidx1, data[avgidx1, 0])
    print(idx2, data[idx2, 0])
    fom_mean = cmean(nuss_fom[avgidx1:idx2], 1)
    fom_var = cvar(nuss_fom[avgidx1:idx2], fom_mean, 1)
    fom_sd = cstd(nuss_fom[avgidx1:idx2], fom_mean, 1)
    np.savetxt('nus_mom.csv', np.c_[fom_mean, fom_sd], delimiter=',', header='mean, std', comments="")
    return


if __name__ == '__main__':
    import sys
    nu_momentum(*sys.argv[1:])
