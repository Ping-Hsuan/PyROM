def set_pltparams(feature, solver, N, T0, fd=None):
    plot_params = {'c': 'None', 'marker': 'o', 'mfc': 'None', 'label': None}
    if feature == 'dual_norm' or feature == 'mnurelerr':
        plot_params['c'] = 'k'
    elif feature == 'rom_mrelerr' or feature == 'nu_1st2nd':
        plot_params['c'] = 'b'
    elif feature == 'proj_mrelerr' or feature == 'proj_mabserr':
        plot_params['c'] = 'k'
        plot_params['label'] = 'Projection with '+r'$N='+N+'$'
    elif feature == 'rom_mabserr':
        plot_params['c'] = 'b'
    elif feature == 'FOM':
        plot_params['c'] = 'k'
        plot_params['label'] = 'FOM'
    if fd:
        if solver == 'L-ROM':
            fd = fd.replace('p', '.')
            plot_params['label'] = solver+' with '+r'$N='+N+'$ and '+str(fd)+' percentage filtered'
        elif solver == 'L-ROM-DF':
            fd = fd.replace('p', '.')
            plot_params['label'] = solver+' with '+r'$N='+N+'$ and filter width '+r'$\delta=$'+str(fd)
        else:
            raise Exception("fd only supported for l-rom or l-rom_df")
    else:
        if plot_params['label'] is None:
           plot_params['label'] = solver+' with '+r'$N='+N+'$'
    return plot_params
