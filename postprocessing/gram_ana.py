import numpy as np
import numpy.linalg as LA
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import re
from itertools import accumulate
from matplotlib.ticker import ScalarFormatter, NullFormatter
import os
import sys

plt.style.use('report_3fig')

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]


print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())

gu = np.loadtxt('../ops/gu')
gt = np.loadtxt('../ops/gt')

lsu = int(np.sqrt(len(gu)))
gu = np.reshape(gu, (lsu, lsu))
Numax = (LA.matrix_rank(gu))

lst = int(np.sqrt(len(gt)))
gt = np.reshape(gt, (lst, lst))
Ntmax = (LA.matrix_rank(gt))

xdata = np.linspace(1, len(gu), len(gu))

print("Solving gu's eigenvalues...")
vu, wu = LA.eig(gu)
vu = vu.real
print(max(vu.imag))
print("Solving gt's eigenvalues...")
vt, wt = LA.eig(gt)
vt = vt.real
print(max(vt.imag))

vu[::-1].sort()
ene_accum_v = list(accumulate(vu))
fene_accum_v = list(accumulate(vu[1:]))
print("Store fluctuation energy ratio in velr.dat")
np.savetxt('velr.dat', fene_accum_v/fene_accum_v[-1])

vt[::-1].sort()
ene_accum_t = list(accumulate(vt))
fene_accum_t = list(accumulate(vt[1:]))
print("Store fluctuation energy ratio in tmpr.dat")
np.savetxt('tmpr.dat', fene_accum_t/fene_accum_t[-1])

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata[1:], fene_accum_v/fene_accum_v[-1], 'b-o', label=r'$H^{1}$'+'-POD, vel')
ax.loglog(xdata[1:], fene_accum_t/fene_accum_t[-1], 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([2, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig('ene_in_flucf.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
ax.loglog(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([1, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig('gram_eig.png')
ax.set_xlim([100, 1000])
ax.set_ylim([1e-12, 1e-4])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())
fig.savefig('gram_eig_zoom_loglog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu/ene_accum_v[-1], 'b-o', label=r'$H^{1}$'+'-POD, vel')
ax.loglog(xdata, vt/ene_accum_t[-1], 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\sum^N_{i=1}\lambda_i}$',rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
fig.savefig('ene_permode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu/ene_accum_v[0], 'b-o', label=r'$H^{1}$'+'-POD, vel')
ax.loglog(xdata, vt/ene_accum_t[0], 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\lambda_1}$', rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
fig.savefig('ene_to1stmode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, np.sqrt(ene_accum_v[-1]-ene_accum_v)/np.sqrt(ene_accum_v[-1]), 'b-o', label='Velocity')
ax.loglog(xdata, np.sqrt(ene_accum_t[-1]-ene_accum_t)/np.sqrt(ene_accum_t[-1]), 'r-o', label='Temp')
ax.axhline(y=1e-4, color='k', linestyle='-')
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\sqrt{\frac{\sum_{i>N}\lambda_i}{\sum_{i=1}\lambda_i}}$', rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
ax.legend()
fig.savefig('Nmax.png')
fig.clf()

plt.style.use('report')
fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
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
fig.savefig('gram_eig_zoom_semilog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, vu, 'b-o', label=r'$H^{1}$'+'-POD, vel')
ax.loglog(xdata, vt, 'r-o', label=r'$H^{1}$'+'-POD, temp')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([1, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig('gram_eig_2fig.png')

print('---------------------------------------')
print('POD modes information in the following:')
print('---------------------------------------')
print("gu rank:", Numax)
print("gt rank:", Ntmax)
Nuflux = np.argmax(fene_accum_v/fene_accum_v[-1] > 0.9) + 2
Ntflux = np.argmax(fene_accum_t/fene_accum_t[-1] > 0.9) + 2
print("90% fluctuating energy in u with N = ", Nuflux)
print("90% fluctuating energy in temp with N = ", Ntflux)
Nu_g90pt = np.argmax(vu/ene_accum_v[-1] > 0.9) + 1
Nt_g90pt = np.argmax(vt/ene_accum_t[-1] > 0.9) + 1
print("N_vel: %3d contains %4.4f in total energy" % (Nu_g90pt, vu[Nu_g90pt-1]/ene_accum_v[-1]))
print("N_temp: %3d contains %4.4f in total energy" % (Nt_g90pt, vt[Nt_g90pt-1]/ene_accum_t[-1]))
Nu_l1pt = np.argmax(vu/ene_accum_v[-1] < 0.01) + 1
Nt_l1pt = np.argmax(vt/ene_accum_t[-1] < 0.01) + 1
print("N_vel: %3d contains less than %4.4f in total energy" % (Nu_l1pt, vu[Nu_l1pt-1]/ene_accum_v[-1]))
print("N_temp: %3d contains less than %4.4f in total energy" % (Nt_l1pt, vt[Nt_l1pt-1]/ene_accum_t[-1]))
Nu_l1pfm = np.argmax(vu/ene_accum_v[0] < 0.01) + 1
Nt_l1pfm = np.argmax(vt/ene_accum_t[0] < 0.01) + 1
print("N_vel: %3d contains less than %4.4f of the energy of the first mode" % (Nu_l1pfm, vu[Nu_l1pfm-1]/ene_accum_v[0]))
print("N_temp: %3d contains less than %4.4f of the energy of the first mode" % (Nt_l1pfm, vt[Nt_l1pfm-1]/ene_accum_t[0]))
Nu_max = np.argmax(np.sqrt(ene_accum_v[-1]-ene_accum_v)/np.sqrt(ene_accum_v[-1]) < 1e-4) + 1
Nt_max = np.argmax(np.sqrt(ene_accum_t[-1]-ene_accum_t)/np.sqrt(ene_accum_t[-1]) < 1e-4) + 1
print("N_max,vel: ", Nu_max)
print("N_max,temp: ", Nt_max)
print("Minimum Nu to be used is: ", Nu_g90pt)
print("Minimum Nt to be used is: ", Nt_g90pt)
print("Maximum Nu to be used is: ", Nu_max)
print("Maximum Nt to be used is: ", Nt_max)
print("N = ", max(Nu_l1pt, Nt_l1pt), " is suggested")
