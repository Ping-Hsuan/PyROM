def rdatatoarray(dic, feature, T0=None):
    import numpy as np
    from aux.reader import reader
    from aux.mypostpro import read_nuss
    from aux.mypostpro import find_nearest
    from aux.mypostpro import cmean
    from aux.mypostpro import cvar
    from aux.mypostpro import cstd
    if feature == 'dual_norm':
        d1 = []
        d2 = []
        for angle, fnames in dic:
            for fname in fnames:
                data = reader(fname)
                if not data:
                    data = 1e8
                dual_norm = np.array(data).astype(np.float64)
                d1.append(int(angle))
                d2.append(float(dual_norm))

        data = np.column_stack((d1, d2))
        data = data[data[:, 0].argsort()]

    elif feature == 'mrelerr' or feature == 'mabserr':
        angles = []
        mrelerr_proj = []
        mrelerr_rom = []
        for angle, fnames in dic:
            for fname in fnames:
                data = reader(fname)
                if not data:
                    data.append(1e8)
                    data.append(1e8)
                data = np.array(data).astype(np.float64)
                mrelerr_rom.append(data[0])
                mrelerr_proj.append(data[1])
                angles.append(int(angle))

        data = np.column_stack((angles, mrelerr_rom, mrelerr_proj))
        data = data[data[:, 0].argsort()]
    elif feature == 'nu_1st2nd':
        if T0 is None:
            raise Exception("T0 is required to compute nu 1st and 2nd momentum")
        else:
            angles = []
            m_list = []
            sd_list = []
            for angle, fnames in dic:
                for fname in fnames:
                    nuss = read_nuss(fname)
                    nuss[:, 2] = nuss[:, 2]/40
                    avgidx1 = find_nearest(nuss[:, 1], T0)
                    rom_mean = cmean(nuss[avgidx1:-1, :], 2)
                    rom_var = cvar(nuss[avgidx1:-1, :], rom_mean, 2)
                    rom_sd = cstd(nuss[avgidx1:-1, :], rom_mean, 2)
                angles.append(int(angle))
                m_list.append(rom_mean)
                sd_list.append(rom_sd)
        data = np.column_stack((angles, m_list, sd_list))
        data = data[data[:, 0].argsort()]
    return data
