import re
def reader(fname):
    with open(fname, 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[-1] for x in list_of_words]
    return data


def erri_w_theta(model, anchor, N, mode, *argv):
    import numpy as np
    if len(argv) == 0:
        fname = 'erri_N'+N+'_'+mode+'.dat'
    else:
        if str(argv[0]) == 'fom':
            fname = 'erri_N'+N+'_sc_fom_'+mode+'.dat'
        elif str(argv[0]) == 'romabserr':
            fname = 'erri_N'+N+'_sc_romabserr_'+mode+'.dat'
        elif str(argv[0]) == 'rom':
            fname = 'erri_N'+N+'_sc_rom_'+mode+'.dat'
        elif str(argv[0]) == 'eta_rom':
            fname = 'erri_N'+N+'_sc_eta_rom_'+mode+'.dat'

    print(fname)
    filename = '../theta_'+str(anchor)+'/'+model+'_parameter_'+str(anchor)+'/dual_norm/angle_list_'+mode+'.dat'
    angle = np.loadtxt(filename)
    filename = '../theta_'+str(anchor)+'/'+model+'_parameter_' + \
               str(anchor)+'/'+'dual_norm/'+fname
    erri = np.loadtxt(filename)

    return angle, erri


def erri_w_param(model, anchor, N, mode, *argv):
    import pandas as pd
    if len(argv) == 0:
        fname = 'dual_norm_N'+str(N)+'.csv'
    else:
        if str(argv[0]) == 'fom':
            fname = 'erri_N'+N+'_sc_fom_'+mode+'.dat'
        elif str(argv[0]) == 'romabserr':
            fname = 'erri_N'+N+'_sc_romabserr_'+mode+'.dat'
        elif str(argv[0]) == 'rom':
            fname = 'erri_N'+N+'_sc_rom_'+mode+'.dat'
        elif str(argv[0]) == 'eta_rom':
            fname = 'erri_N'+N+'_sc_eta_rom_'+mode+'.dat'

#   filename = '../ra_'+str(anchor)+'_theta_90/'+model+'_parameter_theta90_Ra'+str(anchor)+'/dual_norm/'+fname
#   filename = '../re'+str(anchor)+'/'+model+'_parameter_Re'+str(anchor)+'/dual_norm/'+fname
    filenames = find_files(fname, '../')
    for f in filenames:
#       if 'Re'+str(anchor) in re.split('[/_]', f):
        if all(x in f for x in ['Ra'+str(anchor), model, str(N)]):
#       if 'Ra'+str(anchor) in re.split('[/_]', f):
            print(f)
            filename = f
    data = pd.read_csv(filename)

    return [data[i].to_numpy() for i in data.columns]


def erri_leray_w_param(model, anchor, N, mode, pt, *argv):
    import pandas as pd
    if len(argv) == 0:
        fname = 'dual_norm_N'+str(N)+'_0'+pt+'.csv'
    else:
        if str(argv[0]) == 'fom':
            fname = 'erri_N'+N+'_sc_fom_'+mode+'.dat'
        elif str(argv[0]) == 'romabserr':
            fname = 'erri_N'+N+'_sc_romabserr_'+mode+'.dat'
        elif str(argv[0]) == 'rom':
            fname = 'erri_N'+N+'_sc_rom_'+mode+'.dat'
        elif str(argv[0]) == 'eta_rom':
            fname = 'erri_N'+N+'_sc_eta_rom_'+mode+'.dat'

#   filename = '../ra_'+str(anchor)+'_theta_90/'+model+'_parameter_theta90_Ra'+str(anchor)+'/dual_norm/'+fname
    print(fname)
    filenames = find_files(fname, '../')
    for f in filenames:
#       if 'Re'+str(anchor) in re.split('[/_]', f):
#       if 'Ra'+str(anchor) in re.split('[/_]', f):
        if all(x in f for x in ['Ra'+str(anchor), model, str(N)]):
            print(f)
            filename = f
    data = pd.read_csv(filename)
#   filename = '../ra_'+str(anchor)+'_theta_90/'+model+'_parameter_ra_'+str(anchor)+'/dual_norm/param_list_'+mode+'.dat'
#   angle = np.loadtxt(filename)
#   filename = '../ra_'+str(anchor)+'_theta_90/'+model+'_parameter_ra_' + \
#              str(anchor)+'/'+'dual_norm/'+fname
#   erri = np.loadtxt(filename)

    return [data[i].to_numpy() for i in data.columns]


def find_files(filename, search_path):
    import os
    result = []

# Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result
