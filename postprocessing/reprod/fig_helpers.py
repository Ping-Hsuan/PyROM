def set_ax(ax, rom, feature):
    import numpy as np
    anc_lb = ''
    for key, value in rom.info['parameters'].items():
        if key == 'theta':
            anc_lb += '\\'+str(key)+'^*_g='+str(value)
        else:
            anc_lb += str(key)+'^*='+str(value)
    ax.set(xlim=[1, max(rom.nbs)], xlabel=r'$N$')

    if feature == 'dual_norm':
        title = 'Dual norm of the discrete time-averaged residual at '
        ax.set(ylabel=r'$\Delta$', ylim=[10**np.floor(np.log10(min(rom.erris))), 1], title=title+'$'+anc_lb+'$')

    elif feature == 'rom_mrelerr_h1' or feature == 'rom_mrelerr':
        title = r'Relative $H^1$ error in the predicted mean flow at '
        ax.set(ylabel=r'$\frac{\|u - \tilde{u}\|_{H^1}}{\|u\|_{H^1}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'proj_mrelerr_h1' or feature == 'proj_mrelerr':
        title = r'Relative $H^1$ error in the prjected mean flow at '
        ax.set(ylabel=r'$\frac{\|u - \tilde{u}\|_{H^1}}{\|u\|_{H^1}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'rom_mrelerr_l2':
        title = r'Relative $L^2$ error in the predicted mean flow at '
        ax.set(ylabel=r'$\frac{\|u - \tilde{u}\|_{L^2}}{\|u\|_{L^2}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'proj_mrelerr_l2':
        title = r'Relative $L^2$ error in the prjected mean flow at '
        ax.set(ylabel=r'$\frac{\|u - \tilde{u}\|_{L^2}}{\|u\|_{L^2}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'rom_mabserr_h1' or feature == 'rom_mabserr':
        title = r'Absolute $H^1$ error in the predicted mean flow at '
        ax.set(ylabel=r'${\|u - \tilde{u}\|_{H^1}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'proj_mabserr_h1' or feature == 'proj_mabserr':
        title = r'Absolute $H^1$ error in the prjected mean flow at '
        ax.set(ylabel=r'${\|u - \tilde{u}\|_{H^1}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'rom_mabserr_l2':
        title = r'Absolute $L^2$ error in the predicted mean flow at '
        ax.set(ylabel=r'${\|u - \tilde{u}\|_{L^2}}$', title=title+'$'+anc_lb+'$')
    elif feature == 'proj_mabserr_l2':
        title = r'Absolute $L^2$ error in the prjected mean flow at '
        ax.set(ylabel=r'${\|u - \tilde{u}\|_{L^2}}$', title=title+'$'+anc_lb+'$')
    return


def set_pltparams(feature, rom):
    plot_params = {}
    solver = rom.info['method'].upper()
    if solver == 'L-ROM':
        fd = rom.info['perc'].replace('p', '.')
        fd = str(int(float(fd)*100))
        solver += ' with '+str(fd)+' percentage filtered'
    if solver == 'L-ROM-DF':
        fd = rom.info['fwidth'].replace('p', '.')
        solver += ' with filter wdith '+r'$\delta=$'+str(fd)
    plot_params['label'] = solver

    if feature == 'dual_norm' or feature == 'mnurelerr':
        plot_params.update({'c': 'k', 'marker': 'o', 'mfc': 'None'})
    elif feature == 'nu_1st2nd':
        plot_params.update({'c': 'b', 'marker': 'o', 'mfc': 'None'})
    elif feature == 'FOM':
        plot_params.update({'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'})
    elif 'mrelerr' in feature.split('_') or 'mabserr' in feature.split('_'):
        if 'rom' in feature.split('_'):
            plot_params.update({'c': 'b', 'marker': 'o', 'mfc': 'None'})
        elif 'proj' in feature.split('_'):
            plot_params.update({'c': 'k', 'marker': 'o', 'mfc': 'None',
                           'label': 'Projection'})
    return plot_params
