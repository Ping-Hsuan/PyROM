import numpy as np
import matplotlib.pyplot as plt
import os
import operator
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro
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
    target_dir = '/mrelerr/'
    setup.checkdir(target_dir)
    f1 = 0.05
    f2 = 0.06

    search_dir = './'+model+'_info/mrelerr'
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_mrelerr$')
    elif T0 >= 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_mrelerr$')
    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    color_ctr = 0
    tpath = root+'/'

    fws = []
    mrelerr_proj = []
    mrelerr_rom = []
    for fw, fnames in dict_final:
        for fname in fnames:
            data = reader.reader(fname)
            if not data:
                data.append(1e8)
                data.append(1e8)
            data = np.array(data).astype(np.float64)
            mrelerr_rom.append(data[0])
            mrelerr_proj.append(data[1])
            fws.append(float(fw))

    data = np.column_stack((fws, mrelerr_rom, mrelerr_proj))
    data = data[data[:, 0].argsort()]

    anchor = setup.find_anchor()
    solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

    plot_params1 = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                    'label': solver+' with '+r'$N='+N+'$'}
    plot_params2 = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                    'label': 'Projection with '+r'$N='+N+'$'}

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(xlabel=r'$\delta$', ylabel=r'$\frac{\|u(\theta_g) -' +
           r'\tilde{u}(\theta_g;{\theta^*_g} =' +
           str(int(anchor))+r')\|_{H^1}}{\|u(\theta_g)\|_{H^1}}$',
           ylim=[0, 1], yticks=np.linspace(0, 1, 11),
           xticks=1/2**np.linspace(0, 10, 11, dtype=int),
           title='Relative error in the mean flow at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' +
           r'$\theta^*_g='+str(int(anchor))+'$')

    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.semilogx(data[:, 0], data[:, 1], **plot_params1)
    ax.semilogx(data[:, 0], data[:, 2], **plot_params2)
    ax.legend(loc=0, ncol=1)
    fig.savefig('.'+target_dir+'relerr_N'+N+'_'+str(angle)+'.png')
    print("---------------------------------------------")

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(xlabel=r'$\delta$', ylabel=r'$\frac{\|u(\theta_g) -' +
           r'\tilde{u}(\theta_g;{\theta^*_g} =' +
           str(int(anchor))+r')\|_{H^1}}{\|u(\theta_g)\|_{H^1}}$',
           ylim=[0, 1], yticks=np.linspace(0, 1, 11),
           title='Relative error in the mean flow with \n ROM anchor at ' +
           r'$\theta^*_g='+str(int(anchor))+'$')
    ax.plot(data[:, 0], data[:, 1], **plot_params1)
    ax.plot(data[:, 0], data[:, 2], **plot_params2)
    ax.set_xlim([f1, f2])
    ax.legend(loc=0, ncol=1)
    fig.savefig('.'+target_dir+'relerr_N'+N+'_focus.png')

    np.savetxt('.'+target_dir+'fws_list.dat', data[:, 0])
    np.savetxt('.'+target_dir+'rom_relerr_N'+N+'_'+str(angle)+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'proj_relerr_N'+N+'_'+str(angle)+'.dat', data[:, 2])
    print("---------------------------------------------")
    plt.clf()

