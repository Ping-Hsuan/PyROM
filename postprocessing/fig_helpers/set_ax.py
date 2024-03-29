def set_ax(ax, feature, tkey, tval):
    import numpy as np
    if feature == 'dual_norm':
        ax.set(ylabel=r'$\Delta$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged residual at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mrelerr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle\|_{H^1}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0], title='Relative error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mabserr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}$', xticks=tval[0], title='Absolute error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')
    elif feature == 'mrelerr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1_0}}{\|\langle \bf{u} \rangle\|_{H^1_0}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0], title='Relative error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mabserr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1_0}$', xticks=tval[0], title='Absolute error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')
    elif feature == 'mrelerr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{L^2}}{\|\langle \bf{u} \rangle\|_{L^2}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0], title='Relative error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mabserr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{L^2}$', xticks=tval[0], title='Absolute error in the predicted and projected mean flow at '+r'$\mathcal{P}_{train}$')
    elif feature == 'mnurelerr':
        ax.set(ylim=[1e-4, 1], xticks=tval[0], xlabel=r'$'+tkey[0]+'$',
                ylabel=r'$\frac{|\langle Nu \rangle_s -' +
                r'\langle \tilde{Nu} \rangle_s|}' + r'{|\langle Nu \rangle_s|}$', title='Relative error in the predicted mean Nu at '+r'$\mathcal{P}_{train}$')

    elif feature == 'mnu':
        ax.set(ylim=[1, 4], xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='Mean Nu', title='FOM and predicted mean Nu at '+r'$\mathcal{P}_{train}$')
    elif feature == 'std_nu':
        ax.set(xticks=tval[0], xlabel=r'$'+tkey[0]+'$', ylabel='std(Nu)', title='FOM and predicted Std(Nu) at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_dual_norm':
        ax.set(ylabel=r'$\Delta_{\mathsf{vel}}$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged vel residual at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_dual_norm':
        ax.set(ylabel=r'$\Delta_{\mathsf{temp}}$', xlabel=r'$'+tkey[0]+'$', xticks=tval[0], title='Dual norm of the discrete time-averaged temp residual at '+r'$\mathcal{P}_{train}$')

    elif feature == 'vel_mrelerr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle u - \tilde{u} \rangle\|_{H^1}}{\|\langle u \rangle\|_{H^1}}$',
               xticks=tval[0], ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               title='Relative error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mabserr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{u} \rangle\|_{H^1}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')

    elif feature == 'temp_mrelerr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle T - \tilde{T} \rangle\|_{H^1}}{\|\langle T \rangle\|_{H^1}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0],
               title='Relative error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_mabserr_h1':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{T} \rangle\|_{H^1}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mrelerr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle u - \tilde{u} \rangle\|_{H^1_0}}{\|\langle u \rangle\|_{H^1_0}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0],
               title='Relative error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mabserr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{u} \rangle\|_{H^1_0}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')

    elif feature == 'temp_mrelerr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle T - \tilde{T} \rangle\|_{H^1_0}}{\|\langle T \rangle\|_{H^1_0}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0],
               title='Relative error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_mabserr_h10':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle T - \tilde{T} \rangle\|_{H^1_0}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mrelerr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle u - \tilde{u} \rangle\|_{L^2}}{\|\langle u \rangle\|_{L^2}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0],
               title='Relative error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')
    elif feature == 'vel_mabserr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle u - \tilde{u} \rangle\|_{L^2}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean velocity at '+r'$\mathcal{P}_{train}$')

    elif feature == 'temp_mrelerr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$',
               ylabel=r'$\frac{\|\langle T - \tilde{T} \rangle\|_{L^2}}{\|\langle T \rangle\|_{L^2}}$',
               ylim=[0, 0.5], yticks=np.linspace(0, 0.5, 6),
               xticks=tval[0],
               title='Relative error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    elif feature == 'temp_mabserr_l2':
        ax.set(xlabel=r'$'+tkey[0]+'$', ylabel=r'$\|\langle T - \tilde{T} \rangle\|_{L^2}$',
               xticks=tval[0], title='Absolute error in the predicted and projected mean temperature at '+r'$\mathcal{P}_{train}$')
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
