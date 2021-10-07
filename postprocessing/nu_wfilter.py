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
    target_dir = '/nu/'
    setup.checkdir(target_dir)
    f1 = 0.05
    f2 = 0.06

    search_dir = './'+model+'_info/nu'
    root, filenames = setup.gtfpath(search_dir, '^.*_'+N+'nb_.*$')
    if T0 == 1:
        files_dict = setup.create_dict(filenames, '^.*_ic_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_nu$')
    elif T0 >= 1:
        files_dict = setup.create_dict(filenames, '^.*_zero_h10_'+str(int(angle-90))+'_(-?[+-]?([0-9]*[.])?[0-9]+)_nu$')
    dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))

    color_ctr = 0
    tpath = root+'/'

    filename = '../../../../fom_nuss/nuss_fom_'+str(int(angle))
    data = mypostpro.read_nuss(filename)
    data[:, 2] = data[:, 2]/40
    idx1 = mypostpro.find_nearest(data[:, 0], 0)
    idx2 = mypostpro.find_nearest(data[:, 0], 1000)
    nuss_fom = data[idx1:idx2, :]
    avgidx1 = mypostpro.find_nearest(data[:, 0], 501)
    fom_mean = mypostpro.cmean(nuss_fom[avgidx1:idx2], 2)
    fom_var = mypostpro.cvar(nuss_fom[avgidx1:idx2], fom_mean, 2)
    fom_sd = mypostpro.csd(nuss_fom[avgidx1:idx2], fom_mean, 2)
    print('FOM data at deg '+str(int(angle)), ', Mean nu ', fom_mean, 'Std(Nu): ', fom_sd)

    merr_list = []
    verr_list = []
    sderr_list = []
    fws = []
    m_list = []
    sd_list = []

    for fw, fnames in dict_final:
        # get the FOM data
        for fname in fnames:

            nuss = mypostpro.read_nuss(fname)
            nuss[:, 2] = nuss[:, 2]/40
            avgidx1 = mypostpro.find_nearest(nuss[:, 1], int(sys.argv[3]))
            rom_mean = mypostpro.cmean(nuss[avgidx1:-1, :], 2)
            rom_var = mypostpro.cvar(nuss[avgidx1:-1, :], rom_mean, 2)
            rom_sd = mypostpro.csd(nuss[avgidx1:-1, :], rom_mean, 2)
            [mean_err, var_err, sd_err] = mypostpro.cnuss_err(fom_mean, fom_var,
                                                              fom_sd, rom_mean,
                                                              rom_var, rom_sd)
        merr_list.append(mean_err)
        verr_list.append(var_err)
        sderr_list.append(sd_err)
        fws.append(float(fw))
        m_list.append(rom_mean)
        sd_list.append(rom_sd)

    data = np.column_stack((fws, merr_list, sderr_list, m_list,
                           sd_list))
    #                      sd_list, fom_means, fom_stds))
    data = data[data[:, 0].argsort()]
    print(data)

    anchor = setup.find_anchor()
    solver = checker.rom_checker(fname, '^.*_(.*)rom_.*$')

    ### Below are plotting
    plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[1e-4, 1], xticks=1/2**np.linspace(0, 10, 11, dtype=int),
           xlabel=r'$\delta$', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
           r'\langle \widehat{\text{Nu}} \rangle_s|}' +
           r'{|\langle \text{Nu} \rangle_s|}$',
           title='Relative error in the mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' +
           r'$\theta^*_g='+str(int(anchor))+'$')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.semilogx(data[:, 0], data[:, 1], **plot_params)
    ax.legend(loc=1)
    fig.savefig('.'+target_dir+'relmnu_N'+N+'_'+str(angle)+'.png')

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[1e-4, 1],
           xlabel=r'$\delta$', ylabel=r'$\frac{|\langle \text{Nu} \rangle_s -' +
           r'\langle \widehat{\text{Nu}} \rangle_s|}' +
           r'{|\langle \text{Nu} \rangle_s|}$',
           title='Relative error in the mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' +
           r'$\theta^*_g='+str(int(anchor))+'$')
    ax.plot(data[:, 0], data[:, 1], **plot_params)
    ax.set_xlim([f1, f2])
    ax.legend(loc=1)
    fig.savefig('.'+target_dir+'relmnu_N'+N+'_focus.png')
    plt.close(fig)

    plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None',
                   'label': solver+' with '+r'$N='+N+'$'}
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[1, 4], xticks=1/2**np.linspace(0, 10, 11, dtype=int),
           xlabel=r'$\delta$', ylabel='Mean Nu',
           title='Mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at '+r'$\theta^*_g='+str(int(anchor))+'$')
    ax.hlines(y=fom_mean, xmin=1/2**10, xmax=1, colors='k', label='FOM')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.semilogx(data[:, 0], data[:, 3], **plot_params)
    ax.legend(loc=1)
    fig.savefig('.'+target_dir+'mnu_N'+N+'_'+str(angle)+'.png')
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[1, 4], xlabel=r'$\delta$', ylabel='Mean Nu',
           title='Mean Nu at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at '+r'$\theta^*_g='+str(int(anchor))+'$')
    ax.plot(data[:, 0], data[:, 3], **plot_params)
    ax.hlines(y=fom_mean, xmin=1/2**10, xmax=1, colors='k', label='FOM')
    ax.legend(loc=1)
    ax.set_xlim([f1, f2])
    #ax.set_xticks(np.linspace(f1,f2,21))
    fig.savefig('.'+target_dir+'mnu_N'+N+'_focus.png')

    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[0, 0.3], xticks=1/2**np.linspace(0, 10, 11, dtype=int),
           xlabel=r'$\delta$', ylabel='std(Nu)',
    title='Std(Nu) at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' + r'$\theta^*_g='+str(int(anchor))+'$')
    ax.hlines(y=fom_sd, xmin=1/2**10, xmax=1, colors='k', label='FOM')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.semilogx(data[:, 0], data[:, 4], **plot_params)
    ax.legend(loc=1)
    fig.savefig('.'+target_dir+'stdnu_N'+N+'_'+str(angle)+'.png')
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.set(ylim=[0, 0.3], xlabel=r'$\delta$', ylabel='std(Nu)',
    title='Std(Nu) at '+r'$\theta_g=$'+str(angle)+'\n with ROM anchor at ' + r'$\theta^*_g='+str(int(anchor))+'$')
    ax.plot(data[:, 0], data[:, 4], **plot_params)
    ax.hlines(y=fom_sd, xmin=1/2**10, xmax=1, colors='k', label='FOM')
    ax.legend(loc=1)
    ax.set_xlim([f1, f2])
    fig.savefig('.'+target_dir+'stdnu_N'+N+'_focus.png')

    np.savetxt('.'+target_dir+'fws.dat', data[:, 0])
    np.savetxt('.'+target_dir+'merr_N'+N+'_'+str(angle)+'.dat', data[:, 1])
    np.savetxt('.'+target_dir+'stderr_N'+N+'_'+str(angle)+'.dat', data[:, 2])
    np.savetxt('.'+target_dir+'mnu_N'+N+'_'+str(angle)+'.dat', data[:, 3])
    np.savetxt('.'+target_dir+'stdnu_N'+N+'_'+str(angle)+'.dat', data[:, 4])
    plt.clf()
