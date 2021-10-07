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
