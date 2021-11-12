def parametric(model, N, T0, mode, fd=None, ifsetup=False):
    import os
    import yaml
    from aux.create_dir import create_dir
    from setup.setup_info import setup_info
    from dual_norm.dual_norm_wparam import dual_norm_wparam
    from dual_norm.vel_dual_norm_wparam import vel_dual_norm_wparam
    from dual_norm.temp_dual_norm_wparam import temp_dual_norm_wparam
    from mrelerr.mrelerr_wparam import mrelerr_wparam
    from mabserr.mabserr_wparam import mabserr_wparam
    from mrelerr.vel_mrelerr_wparam import vel_mrelerr_wparam
    from mabserr.vel_mabserr_wparam import vel_mabserr_wparam
    from mrelerr.temp_mrelerr_wparam import temp_mrelerr_wparam
    from mabserr.temp_mabserr_wparam import temp_mabserr_wparam
    from nu_1st_2nd_momentum.nu_1st2nd_momentum_wparam import nu_1st2nd_momentum_wparam
    # This python script is used to plot parametric results.
    # You must specify the model and the POD mdoe N.

    if ifsetup:
        setup_info(model, N)

    with open('./parametric.yaml') as f:
        ainfo = yaml.load(f, Loader=yaml.FullLoader)
    akey = list(ainfo['anchor'].keys())
    akey = [i.split('^', 1)[0] for i in akey]
    aval = list(ainfo['anchor'].values())
    aval = [i for i in aval]
    idx = akey.index(list(ainfo['train_set'].keys())[0])
    al = '_'.join([a + str(b) for a, b in zip(akey, aval)])
    tkey = list(ainfo['train_set'].keys())
    tval = list(ainfo['train_set'].values())
    tdir = './'+model+'_parameter_'+al
    create_dir(tdir)

    with open('./features.yaml') as f:
        features = yaml.load(f, Loader=yaml.FullLoader)
    fkey = list(features.keys())

    os.chdir(tdir)

    if 'dual_norm' in fkey:
        dual_norm_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd)
    if 'nu_1st2nd' in fkey:
        nu_1st2nd_momentum_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd, iffom=True)
    if 'vel_dual_norm' in fkey:
        vel_dual_norm_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd)
    if 'temp_dual_norm' in fkey:
        temp_dual_norm_wparam(model, N, T0, mode, idx, aval, tkey, tval, fd)
    for sol in ['', 'vel_', 'temp_']:
        for norm in ['h1', 'h10', 'l2']:
            if sol+'mrelerr_'+norm in fkey:
                mrelerr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)
            if sol+'mabserr_'+norm in fkey:
                mabserr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)
            if 'vel_mrelerr' in fkey:
                vel_mrelerr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)
            if 'vel_mabserr' in fkey:
                vel_mabserr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)
            if 'temp_mrelerr' in fkey:
                temp_mrelerr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)
            if 'temp_mabserr' in fkey:
                temp_mabserr_wparam(model, N, T0, mode, idx, aval, tkey, tval, norm, fd)

    #subprocess.run(["python3", "fom_norm.py", tdir, model, N, T0, mode])
    #subprocess.run(["python3", "rom_norm_wparam.py", tdir, model, N, T0, mode])

    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'rom', mode])
    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'fom', mode])
    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'romabserr', mode])
    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom', mode])
    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta', mode])
    #subprocess.run(["python3", "dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom_all', mode])

    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'rom', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'fom', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'romabserr', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom_all', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta', mode])
    #subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'domain', mode])

    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'rom', mode])
    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'fom', mode])
    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'romabserr', mode])
    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom', mode])
    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta', mode])
    #subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tdir, model, N, T0, 'eta_rom_all', mode])

if __name__ == '__main__':
    import sys
    parametric(*sys.argv[1:])
