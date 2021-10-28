def set_ax(ax, feature, tkey, tval):
    import numpy as np
    if feature == 'dual_norm':
        ax.set(ylabel=r'$\Delta$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged residual at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mrelerr':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle\|_{H^1}}$',
               ylim=[0, 1], yticks=np.linspace(0, 1, 11),
               xticks=tval[0], title='Relative error in the predicted mean flow at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mabserr':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}$', xticks=tval[0], title='Absolute error in the predicted mean flow at '+r'$\mathcal{P}_{train}$')
    elif feature == 'mnurelerr':
        ax.set(ylim=[1e-4, 1], xticks=tval[0], xlabel=r'$'+tkey[0]+'$',
                ylabel=r'$\frac{|\langle Nu \rangle_s -' +
                r'\langle \tilde{Nu} \rangle_s|}' + r'{|\langle Nu \rangle_s|}$', title='Relative error in the predicted mean Nu at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mnu':
        ax.set(ylim=[1, 4], xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='Mean Nu', title='FOM and predicted mean Nu at '+r'$\mathcal{P}_{train}$')
    elif feature == 'std_nu':
        ax.set(ylim=[0, 0.3], xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='std(Nu)', title='FOM and predicted Std(Nu) at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_dual_norm':
        ax.set(ylabel=r'$\Delta_{\mathsf{vel}}$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged vel residual at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_dual_norm':
        ax.set(ylabel=r'$\Delta_{\mathsf{temp}}$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged temp residual at '+r'$\mathcal{P}_{train}$')

    elif feature == 'vel_mrelerr':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle u - \tilde{u} \rangle\|_{H^1}}{\|\langle u \rangle\|_{H^1}}$',
               ylim=[0, 1], yticks=np.linspace(0, 1, 11), xticks=tval[0],
               title='Relative error in the predicted mean velocity at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mabserr':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{u} \rangle\|_{H^1}$',
               xticks=tval[0], title='Absolute error in the predicted mean velocity at '+r'$\mathcal{P}_{train}$')

    elif feature == 'temp_mrelerr':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle T - \tilde{T} \rangle\|_{H^1}}{\|\langle T \rangle\|_{H^1}}$',
               ylim=[0, 1], yticks=np.linspace(0, 1, 11), xticks=tval[0],
               title='Relative error in the predicted mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_mabserr':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{T} \rangle\|_{H^1}$',
               xticks=tval[0], title='Absolute error in the predicted mean temperature at '+r'$\mathcal{P}_{train}$')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
