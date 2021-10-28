def set_pltparams(feature, solver, N, T0, fd=None):
    if feature == 'dual_norm' or feature == 'mnurelerr':
        plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None'}
        if fd:
            fd = fd.strip("0")
            plot_params['label'] = solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)
        else:
            plot_params['label'] = solver+' with '+r'$N='+N+'$'

    elif feature == 'rom_mrelerr' or feature == 'nu_1st2nd':
        plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None'}
        if fd:
            fd = fd.strip("0")
            plot_params['label'] = solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)
        else:
            plot_params['label'] = solver+' with '+r'$N='+N+'$'
    elif feature == 'proj_mrelerr' or feature == 'proj_mabserr':
        plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None',
                       'label': 'Projection with '+r'$N='+N+'$'}

    elif feature == 'rom_mabserr':
        plot_params = {'c': 'b', 'marker': 'o', 'mfc': 'None'}
        if fd:
            fd = fd.strip("0")
            plot_params['label'] = solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)
        else:
            plot_params['label'] = solver+' with '+r'$N='+N+'$'
    elif feature == 'FOM':
        plot_params = {'c': 'k', 'marker': 'o', 'mfc': 'None', 'label': 'FOM'}
    return plot_params
