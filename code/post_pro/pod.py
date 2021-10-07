from itertools import accumulate
import numpy as np


def cfer(pod_eig):
    # compute fluctuation energy ratio for each N
    # sum^N_{i=2} \lambda_i / sum^K_{i=2} \lambda_i
    fene = list(accumulate(pod_eig[1:]))
    fer = fene/fene[-1]
    return fer


def cetfl(pod_eig):
    # compute fluctuation energy ratio for each N
    # sum^N_{i=2} \lambda_i / sum^K_{i=2} \lambda_i
    fene = list(accumulate(pod_eig[1:]))
    etfl = pod_eig[1:]/fene[-1]
    return etfl


def catt(pod_eig, N):
    # compute the ratio of each POD mode to total POD modes
    # \lambda_N / sum^K_{i=1} \lambda_i
    total = np.sum(pod_eig)
    att = np.sum(pod_eig[:N])/total
    return att


def cett(pod_eig):
    # compute the ratio of each POD mode to total POD modes
    # \lambda_N / sum^K_{i=1} \lambda_i
    total = np.sum(pod_eig)
    ett = pod_eig/total
    return ett


def cetf(pod_eig):
    # compute the ratio of each POD mode to first POD mode
    # \lambda_N / \lambda_1
    etf = pod_eig/pod_eig[0]
    return etf


def ceps(pod_eig):
    # compute the epsilon which is defined as
    # epsilon = ( sum_{i>N} \lambda_i / sum^K_{i} \lambda_i )
    ene = list(accumulate(pod_eig))
    total = np.sum(pod_eig)
    eps = np.sqrt(total-ene)/np.sqrt(total)
    return eps


def cene(pod_eig):
    # compute sum_{i>N} \lambda_i
    ene = list(accumulate(pod_eig))
    return ene


def N_fergp(fer, percent):
    # Compute N such that fer
    # is greater than given percentage
    N = np.argmax(fer > percent) + 2
    return N


def N_egpint(ene, percent):
    # Compute the number of modes required to contain
    # given percentage of the total energy
    N = np.argmax((ene/ene[-1]) > percent) + 1
    return N


def N_ettlp(ett, percent):
    # Compute the first POD modes that is less than
    # given percentage of the total energy
    N = np.argmax(ett < percent) + 1
    return N


def N_etflp(etf, percent):
    # Compute the first POD modes that is less than
    # given percentage of the first POD mode
    N = np.argmax(etf < percent) + 1
    return N


def N_etfllp(etfl, percent):
    # Compute the first POD modes that is less than
    # given percentage of the fluct energy
    N = np.argmax(etfl < percent) + 1
    return N


def N_epslp(eps, percent):
    # Compute the N_max based on the eps with the given percent
    N = np.argmax(eps < percent) + 1
    return N


def compare_eig(thetas, ifrom, colors):
    import matplotlib.pyplot as plt
    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        veig = np.loadtxt(path+'veig.dat')
        xdata = np.linspace(1, len(veig), len(veig))
        ax1.loglog(xdata, veig, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$\lambda_{N,vel}$')
        ax1.set_ylim([1e-8, 1e5])
        ax1.set_xlim([1, 300])
        ax1.grid(b=True)
        if (ifrom[1]):
            teig = np.loadtxt(path+'teig.dat')
            xdata = np.linspace(1, len(teig), len(teig))
            ax2.loglog(xdata, teig, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$\lambda_{N,temp}$')
            ax2.set_ylim([1e-8, 1e5])
            ax2.set_xlim([1, 300])
            ax2.grid(b=True)
        color_ctr += 1
    fig1.savefig('veig_compare.png')
    if (ifrom[1]):
        fig2.savefig('teig_compare.png')

    # Plot eig in semilog plot
    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        veig = np.loadtxt(path+'veig.dat')
        xdata = np.linspace(1, len(veig), len(veig))
        ax1.semilogy(xdata, veig, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$\lambda_{N,vel}$')
        ax1.set_ylim([1e-8, 1e5])
        ax1.set_xlim([1, 300])
        ax1.grid(b=True)
        if (ifrom[1]):
            teig = np.loadtxt(path+'teig.dat')
            xdata = np.linspace(1, len(teig), len(teig))
            ax2.semilogy(xdata, teig, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$\lambda_{N,temp}$')
            ax2.set_ylim([1e-8, 1e5])
            ax2.set_xlim([1, 300])
            ax2.grid(b=True)
        color_ctr += 1
    fig1.savefig('veig_compare_semi.png')
    if (ifrom[1]):
        fig2.savefig('teig_compare_semi.png')
    return


def compare_fer(thetas, ifrom, colors):
    import matplotlib.pyplot as plt
    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        vfer = np.loadtxt(path+'vfer.dat')
        xdata = np.linspace(1, len(vfer), len(vfer))
        ax1.plot(xdata, vfer, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$r_{2,vel}$')
        ax1.set_ylim([0.4, 1.1])
        ax1.set_xlim([0, 100])
        ax1.set_yticks([0.4, 0.6, 0.8, 0.9, 0.95, 1.0])
        ax1.axhline(y=0.9, color='tab:pink', linestyle='--')
        ax1.axhline(y=0.95, color='tab:pink', linestyle='--')
        ax1.grid(b=True)
        if (ifrom[1]):
            tfer = np.loadtxt(path+'tfer.dat')
            xdata = np.linspace(1, len(tfer), len(tfer))
            ax2.plot(xdata, tfer, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$r_{2,temp}$')
            ax2.set_ylim([0.4, 1.1])
            ax2.set_xlim([0, 100])
            ax2.set_yticks([0.4, 0.6, 0.8, 0.9, 0.95, 1.0])
            ax2.axhline(y=0.9, color='tab:pink', linestyle='--')
            ax2.axhline(y=0.95, color='tab:pink', linestyle='--')
            ax2.grid(b=True)
        color_ctr += 1

    fig1.savefig('vfer_compare.png')
    if (ifrom[1]):
        fig2.savefig('tfer_compare.png')
    return


def compare_ett(thetas, ifrom, colors):
    import matplotlib.pyplot as plt
    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        vett = np.loadtxt(path+'vett.dat')
        xdata = np.linspace(1, len(vett), len(vett))
        ax1.plot(xdata, vett, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$\lambda_{N,vel}/\sum_i \lambda_{i,vel}$')
        ax1.set_ylim([-0.1, 1.1])
        ax1.set_xlim([0, 30])
        ax1.axhline(y=1e-2, color='tab:pink', linestyle='--')
        ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        if (ifrom[1]):
            tett = np.loadtxt(path+'tett.dat')
            xdata = np.linspace(1, len(tett), len(tett))
            ax2.plot(xdata, tett, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$\lambda_{N,temp}/\sum_i \lambda_{i,temp}$')
            ax2.set_ylim([-0.1, 1.1])
            ax2.set_xlim([0, 30])
            ax2.axhline(y=1e-2, color='tab:pink', linestyle='--')
            ax2.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        color_ctr += 1

    fig1.savefig('vett_compare.png')
    if (ifrom[1]):
        fig2.savefig('tett_compare.png')
    return


def compare_etfl(thetas, ifrom, colors):
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
    import sys
    sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
    import pod

    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    Nvel_list = []
    Ntemp_list = []
    r2vel_list = []
    r2temp_list = []
    r1vel_list = []
    r1temp_list = []
    strvel_list = []
    strtemp_list = []
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        vetfl = np.loadtxt(path+'vetfl.dat')
        vfer = np.loadtxt(path+'vfer.dat')
        veig = np.loadtxt(path+'veig.dat')
        xdata = np.linspace(2, len(vetfl)+1, len(vetfl))
        ax1.plot(xdata, vetfl, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$r_{3,vel}$')
        ax1.set_ylim([-0.02, 0.15])
        ax1.set_xlim([0, 50])
        ax1.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.14])
        ax1.axhline(y=0.01, color='tab:pink', linestyle='--')
        ax1.grid(b=True)
        if (ifrom[1]):
            tetfl = np.loadtxt(path+'tetfl.dat')
            teig = np.loadtxt(path+'teig.dat')
            tfer = np.loadtxt(path+'tfer.dat')
            xdata = np.linspace(2, len(tetfl)+1, len(tetfl))
            ax2.plot(xdata, tetfl, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$r_{3,temp}$')
            ax2.set_ylim([-0.02, 0.15])
            ax2.set_xlim([0, 50])
            ax2.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.14])
            ax2.axhline(y=0.01, color='tab:pink', linestyle='--')
            ax2.grid(b=True)
        for percent in [0.01]:
            Nu_l1pt = pod.N_etfllp(vetfl, percent)
            Nvel_list.append(Nu_l1pt)
            r1vel_list.append(pod.catt(veig, Nu_l1pt))
            r2vel_list.append(vfer[Nu_l1pt-1])
            if (ifrom[1]):
                Nt_l1pt = pod.N_etfllp(tetfl, percent)
                Ntemp_list.append(Nt_l1pt)
                r1temp_list.append(pod.catt(teig, Nt_l1pt))
                r2temp_list.append(tfer[Nt_l1pt-1])
        strvel_list.append(r'$r_2$= '+str(vfer[Nu_l1pt-1])[:4]+' for '+r'$\theta_g=$ '+str(theta))
        strtemp_list.append(r'$r_2$= '+str(tfer[Nt_l1pt-1])[:4]+' for '+r'$\theta_g=$ '+str(theta))
        color_ctr += 1

    textstr1 = '\n'.join(strvel_list)
    textstr2 = '\n'.join(strtemp_list)
    offsetbox = TextArea(textstr1)
    xy = (max(Nvel_list)+5, 0.01)
    ab = AnnotationBbox(offsetbox, xy,
                        xybox=(-30, 60),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="-> ,head_length=.1, head_width=.1"))
    ax1.add_artist(ab)

    offsetbox = TextArea(textstr2)
    xy = (max(Ntemp_list)+5, 0.01)
    ab = AnnotationBbox(offsetbox, xy,
                        xybox=(-30, 60),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="-> ,head_length=.1, head_width=.1"))
    ax2.add_artist(ab)
    print(Nvel_list)
    print(Ntemp_list)
    print(r1vel_list)
    print(r1temp_list)
    print(r2vel_list)
    print(r2temp_list)

    fig1.savefig('vetfl_compare.png')
    if (ifrom[1]):
        fig2.savefig('tetfl_compare.png')


def compare_etf(thetas, ifrom, colors):
    import matplotlib.pyplot as plt
    color_ctr = 0
    fig1, ax1 = plt.subplots(1, tight_layout=True)
    if (ifrom[1]):
        fig2, ax2 = plt.subplots(1, tight_layout=True)
    for theta in thetas:
        path = '../theta_'+str(theta)+'/gram_analysis/'
        vetf = np.loadtxt(path+'vetf.dat')
        xdata = np.linspace(1, len(vetf), len(vetf))
        ax1.plot(xdata, vetf, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
        ax1.legend(loc=0)
        ax1.set_xlabel(r'$N$')
        ax1.set_ylabel(r'$\lambda_{N,vel}/\lambda_{1,vel}$')
        ax1.set_ylim([-0.1, 1.1])
        ax1.set_xlim([0, 30])
        ax1.axhline(y=1e-2, color='tab:pink', linestyle='--')
        ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        if (ifrom[1]):
            tetf = np.loadtxt(path+'tetf.dat')
            xdata = np.linspace(1, len(tetf), len(tetf))
            ax2.plot(xdata, tetf, '-o', color=colors[color_ctr], label=r'$\theta_g=$ '+str(theta))
            ax2.legend(loc=0)
            ax2.set_xlabel(r'$N$')
            ax2.set_ylabel(r'$\lambda_{N,temp}/\lambda_{1,temp}$')
            ax2.set_ylim([-0.1, 1.1])
            ax2.set_xlim([0, 30])
            ax2.axhline(y=1e-2, color='tab:pink', linestyle='--')
            ax2.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        color_ctr += 1

    fig1.savefig('vetf_compare.png')
    if (ifrom[1]):
        fig2.savefig('tetf_compare.png')
    return
