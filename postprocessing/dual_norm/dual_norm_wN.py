def dual_norm_wN(model, T0, anchor=None, fd=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    import operator
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
    import setup
    import yaml
    from mor import ROM
    from snapshot import Snapshot
    from aux.cffdic import cffdic
    from aux.gptr import gptr
    from aux.create_dir import create_dir
    from aux.sort import sort
    from setup.gtfpath import gtfpath
    from figsetup.style import style
    from figsetup.text import text

    style(1)
    text()
    T0 = int(T0)

#   print("---------------------------------------------")
#   print("This is the name of the program:", sys.argv[0])
#   print("Argument List:", str(sys.argv))
#   os.chdir(str(sys.argv[1]))
#   model = str(sys.argv[2])
#   deg = str(int(sys.argv[3])-90)
#   print("---------------------------------------------")

    if anchor is None:
        with open('../anchor.yaml') as f:
            features = yaml.load(f, Loader=yaml.FullLoader)
        akey = list(features.keys())
        aval = list(features.values())
        aval = [str(i) for i in aval]
        aval[0] = str(int(aval[0])-90)
    al = '_'.join(aval)

    target_dir = './dual_norm/'
    create_dir(target_dir)

    search_dir = '../'+model+'_info/dual_norm'
    root, filenames = gtfpath(search_dir, '^.*_h10_'+al+'_.*$')
    ptr = gptr(model, None, T0, None, fd)
    files_dict = cffdic(filenames, ptr, 0)
    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    roms = []
    for nb, fnames in dict_final:
        for fname in fnames:
            print(fname)
            rom = ROM(fname)
            rom.DTAR()
            rom.anchor('theta')
            print(rom.anchor('theta'))
            roms.append(rom)
    data = sort(roms, 'nb', 'dtar')
    solver = rom.info['method']
    anchor = str(int(rom.info['anchor']))
    print(rom.anchor('anchor'))
    1/o

    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$\theta^*_g = '+anchor+'$'}
    ax.set(ylabel=r'$\triangle(\theta_g='+str(int(deg)+90)+')$', xlabel=r'$N$',
            ylim=[10**np.floor(np.log10(min(data[:, 1]))), 1], xlim=[1, max(data[:, 0])])
    ax.semilogy(data[:, 0], data[:, 1], **plot_params)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'dual_norm_theta_'+str(int(deg)+90)+'.png')
    print("---------------------------------------------")
    plt.show()
    header = tkey[0]+','+'dual_norm'
    np.savetxt('.'+target_dir+'N_list_'+str(int(deg)+90)+'.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_theta_'+str(int(deg)+90)+'.dat', data[:, 1])

if __name__ == '__main__':
    import sys
    dual_norm_wN(*sys.argv[1:])
