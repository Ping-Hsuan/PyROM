def set_ax(ax, feature, itr):
    param = r'$Ra$'
    t1 = 'POD-$h$Greedy, online stage:'
    if itr == '1':
        tt = str(itr)+'st iteration'
    elif itr == '2':
        tt = str(itr)+'nd iteration'
    elif itr == '3':
        tt = str(itr)+'rd iteration'
    else:
        tt = str(itr)+'th iteration'
    if feature == 'rom_fldrelerr':
        ax.set(xlabel=param,
               ylabel=r'$\frac{\|\langle \bf{u} - \bf{\tilde{u}} \rangle\|_{H^1}}{\|\langle \bf{u} \rangle\|_{H^1}}$',
               ylim=[1e-3, 0.5], title=t1+'\n Comparison of the relative error in predicted mean flow at '+tt)
    elif feature == 'dual_norm':
        ax.set(xlabel=param, ylabel=r'$\triangle$', title=t1+'\n Comparison of the dual norm at '+tt, ylim=[1e-4, 1])
        ax.set_yscale('log')
    elif feature == 'nu_merr':
        ax.set(xlabel=param, title=t1+'\n Comparison of the relative error in mean Nu at '+tt, ylim=[1e-4, 1])
        ax.set_yscale('log')
    elif feature == 'nu_m':
        ax.set(xlabel=param, title=t1+'\n Comparison of the predicted mean Nu at '+tt, ylim=[3.25, 6.25])
    elif feature == 'nu_std':
        ax.set(xlabel=param, title=t1+'\n Comparison of the predicted std(Nu) at '+tt, ylim=[0, 0.12])
    elif feature == 'mtke':
        ax.set(xlabel=param, title=t1+'\n Comparison of the predicted mean TKE at '+tt, ylim=[0, 0.5])
    elif feature == 'mtfluc':
        ax.set(xlabel=param, title=t1+'\n Comparison of the predicted mean temperature fluctuation at '+tt, ylim=[0, 1])
