import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import operator
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
import reader
import checker

setup.style(1)
colors = setup.color(0)
setup.text()

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
model = str(sys.argv[2])
N = str(sys.argv[3])
T0 = int(sys.argv[4])
print("---------------------------------------------")

angles = np.linspace(0, 180, 19, dtype=int)
for angle in angles:
    target_dir = '/dual_norm/'
    setup.checkdir(target_dir)

    search_dir = './'+model+'_info/dual_norm'
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_dual_norm$')
    elif T0 >= 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_dual_norm$')
    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    color_ctr = 0
    tpath = root+'/'

    erri = []
    fws = []
    for fw, fnames in dict_final:
        for fname in fnames:
            data = reader.reader(fname)
            if not data:
                data = 1e8
            dual_norm = np.array(data).astype(np.float64)
            erri.append(float(dual_norm))
            fws.append(float(fw))

    data = np.column_stack((fws, erri))
    data = data[data[:, 0].argsort()]

    anchor = setup.find_anchor()
    solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

    fig, ax = plt.subplots(1, tight_layout=True)
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}
    ax.set(ylabel=r'$\triangle(\theta_g;{\theta^*_g}='+str(int(anchor))+r')$',
           xlabel=r'$\delta$',
           title='Dual norm of the residual at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' +
           r'$\theta^*_g='+str(int(anchor))+'$')

    ax.plot(data[:, 0], data[:, 1], **plot_params)
    ax.legend(loc=0)

    print("---------------------------------------------")
    fig.savefig('.'+target_dir+'dual_norm_N'+N+'_'+str(angle)+'.png')
    np.savetxt('.'+target_dir+'fws.dat', data[:, 0])
    np.savetxt('.'+target_dir+'erri_N'+N+'_'+str(angle)+'.dat', data[:, 1])
    print("---------------------------------------------")

    plt.clf()
