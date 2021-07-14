import numpy as np
import numpy.linalg as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import re
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import os
import sys
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import pod
import setup

setup.style(1)
colors = setup.color(0)
setup.text()

# adjust markersize
mpl.rcParams['lines.markersize'] = 3
mpl.rcParams['lines.linewidth'] = 1

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
isExist = os.path.exists(os.getcwd()+'/gram_analysis/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/gram_analysis/')

ifrom = [True, False]
ifrom[1] = input("Thermal?:")
if ifrom[1] == 'T':
    ifrom[1] = True
else:
    ifrom[1] = False

tpath = './gram_analysis/'

gu = np.loadtxt('./ops/gu')
lsu = int(np.sqrt(len(gu)))
gu = np.reshape(gu, (lsu, lsu))
Numax = LA.matrix_rank(gu)
print("gu rank:", Numax)
xdata = np.linspace(1, len(gu), len(gu))

print("Solving gu's eigenvalues...")
vu, wu = LA.eig(gu)
vu = vu.real
vu[::-1].sort()
np.savetxt(tpath+'veig.dat', vu)

vfer = pod.cfer(vu)
np.savetxt(tpath+'vfer.dat', vfer)

vetfl = pod.cetfl(vu)
np.savetxt(tpath+'vetfl.dat', vetfl)

vett = pod.cett(vu)
np.savetxt(tpath+'vett.dat', vett)

vetf = pod.cetf(vu)
np.savetxt(tpath+'vetf.dat', vetf)

veps = pod.ceps(vu)
np.savetxt(tpath+'veps.dat', veps)

vene = pod.cene(vu)

if (ifrom[1]):
    gt = np.loadtxt('./ops/gt')
    lst = int(np.sqrt(len(gt)))
    gt = np.reshape(gt, (lst, lst))
    Ntmax = LA.matrix_rank(gt)
    print("gt rank:", Ntmax)

    print("Solving gt's eigenvalues...")
    vt, wt = LA.eig(gt)
    vt = vt.real
    vt[::-1].sort()
    np.savetxt(tpath+'teig.dat', vt)

    tfer = pod.cfer(vt)
    np.savetxt(tpath+'tfer.dat', tfer)

    tetfl = pod.cetfl(vt)
    np.savetxt(tpath+'tetfl.dat', tetfl)

    tett = pod.cett(vt)
    np.savetxt(tpath+'tett.dat', tett)

    tetf = pod.cetf(vt)
    np.savetxt(tpath+'tetf.dat', tetf)

    teps = pod.ceps(vt)
    np.savetxt(tpath+'teps.dat', teps)

    tene = pod.cene(vt)


print('---------------------------------------')
print('POD analysis in the following:')
print('---------------------------------------')

# Given the percentage, compute the number of modes
# so that the fluctuating energy > percentage
for percent in [0.9, 0.95, 0.99]:
    print("To has at least {:f} % of fluctuating energy".format(percent*100))
    Nu = pod.N_fergp(vfer, percent)
    print("N_vel has to be at least {:f}".format(Nu))
    if (ifrom[1]):
        Nt = pod.N_fergp(tfer, percent)
        print("N_temp has to be at least {:f}".format(Nt))

# Given the percentage, compute the number of modes
# so that it has percentage*total energy
for percent in [0.9]:
    print("To has at least {:f} % of total energy".format(percent*100))
    Nu_gpt = pod.N_egpint(vene, percent)
    print("N_vel has to be at least {:3d} and it has {:4.4f} % in total energy".format(Nu_gpt, (vene[Nu_gpt-1]/vene[-1])*100))
    if (ifrom[1]):
        Nt_gpt = pod.N_egpint(tene, percent)
        print("N_temp has to be at least {:3d} and it has {:4.4f} % in total energy".format(Nt_gpt, (tene[Nt_gpt-1]/tene[-1])*100))

# Given the percentage, compute which mode has energy
# less than percentage*total energy
for percent in [0.01]:
    Nu_l1pt = pod.N_ettlp(vett, percent)
    print("vel: mode {:3d} only has {:4.4f} % of total energy".format(Nu_l1pt, vett[Nu_l1pt-1]*100))
    if (ifrom[1]):
        Nt_l1pt = pod.N_ettlp(tett, percent)
        print("temp: mode {:3d} only has {:4.4f} % of total energy".format(Nt_l1pt, tett[Nt_l1pt-1]*100))

# Given the percentage, compute which mode has energy
# less than percentage*fluctuating energy
for percent in [0.01]:
    Nu_l1pt = pod.N_etfllp(vetfl, percent)
    print("vel mode {:3d} only has {:f} % of the fluctuating energy".format(Nu_l1pt, vetfl[Nu_l1pt-1]*100))
    if (ifrom[1]):
        Nt_l1pt = pod.N_etfllp(tetfl, percent)
        print("temp mode {:3d} only has {:f} % of the fluctuating energy".format(Nt_l1pt, tetfl[Nt_l1pt-1]*100))

# Given the percentage, compute which mode has energy
# less than percentage*first POD modes
for percent in [0.01]:
    Nu_l1pt = pod.N_etflp(vetf, percent)
    print("vel mode {:3d} only has {:f} % of the first POD modes".format(Nu_l1pt, vetf[Nu_l1pt-1]*100))
    if (ifrom[1]):
        Nt_l1pt = pod.N_etflp(tetf, percent)
        print("temp mode {:3d} only has {:f} % of the first POD modes".format(Nt_l1pt, tetf[Nt_l1pt-1]*100))

for percent in [1e-4]:
    Nu_max = pod.N_epslp(veps, percent)
    print("Maximum Nu to be used is: ", Nu_max)
    if (ifrom[1]):
        Nt_max = pod.N_epslp(teps, percent)
        print("Maximum Nt to be used is: ", Nt_max)

#print("N = ", max(max(Nu_l1pt,Nu_g90pt), max(Nt_l1pt,Nt_g90pt)), " is suggested")

# Pass the argument to a functions, check out how to pass multiple arguments in a clean way
fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogx(xdata[1:], vfer, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.semilogx(xdata[1:], tfer, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$r_2$')
ax.set_xlabel(r'$N$')
ax.set_xticks([2, 10, 100, 1000])
ax.set_xlim([1, 300])
ax.axhline(y=0.9, color='tab:pink', linestyle='--')
#ax.set_yticks([0.9, 0.95, 0.99, 1])
ax.set_ylim([0, 1])
fig.savefig(tpath+'ene_in_flucf.png')
fig.clf()


fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogx(xdata[1:], vetfl, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.semilogx(xdata[1:], tetfl, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$r_3$')
ax.set_xlabel(r'$N$')
ax.set_xticks([2, 10, 100, 1000])
ax.set_xlim([1, 300])
ax.axhline(y=0.01, color='tab:pink', linestyle='--')
#ax.set_yticks([0.9, 0.95, 0.99, 1])
ax.set_ylim([0, 1])
fig.savefig(tpath+'ene_in_etfl.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.loglog(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xlim([1, 300])
ax.set_ylim([1e-4, 1e7])
fig.savefig(tpath+'gram_eig.png')
ax.set_xlim([100, 1000])
ax.set_ylim([1e-12, 1e-4])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())
fig.savefig(tpath+'gram_eig_zoom_loglog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogx(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.semilogx(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xlim([1, 300])
#ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig_semi.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vett, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.loglog(xdata, tett, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\sum^N_{i=1}\lambda_i}$',rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
ax.set_xlim([1, 300])
fig.savefig(tpath+'ene_permode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vetf, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.loglog(xdata, tetf, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\lambda_1}$', rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
ax.set_xlim([1, 300])
fig.savefig(tpath+'ene_to1stmode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, veps, 'b-o', label='Velocity')
if (ifrom[1]):
    ax.loglog(xdata, teps, 'r-o', label='Temp')
ax.axhline(y=1e-4, color='k', linestyle='-')
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\sqrt{\frac{\sum_{i>N}\lambda_i}{\sum_{i=1}\lambda_i}}$', rotation=90)
ax.set_ylim([1e-8, 1])
ax.set_xlim([1, 300])
ax.legend()
fig.savefig(tpath+'Nmax.png')
fig.clf()

plt.style.use('report')
fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.semilogy(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
n_list = np.linspace(100, len(gu), 50)
ax.semilogy(n_list, np.exp(-3.5*(n_list/100)+2), 'k-', label=r'$e^{(-3.5)}$')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xlim([100, len(gu)])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xticks(np.linspace(100, len(gu), 5))
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig_zoom_semilog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
if (ifrom[1]):
    ax.loglog(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([1, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig_2fig.png')
