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
isExist = os.path.exists(os.getcwd()+'/gram_analysis/')
if isExist:
    pass
else:
    os.mkdir(os.getcwd()+'/gram_analysis/')

tpath = './gram_analysis/'
g = np.loadtxt('./ops/gcomb')

ls = int(np.sqrt(len(g)))
g = np.reshape(g, (ls, ls))
Nmax = (LA.matrix_rank(g))

xdata = np.linspace(1, len(g), len(g))

print("Solving gcomb's eigenvalues...")
v, w = LA.eig(g)
v = v.real
print(max(v.imag))

v[::-1].sort()
ene_accum = list(accumulate(v))
fene_accum = list(accumulate(v[1:]))
print("Store fluctuation energy ratio in fluc_ene.dat")
np.savetxt(tpath+'fluc_ene.dat', fene_accum/fene_accum[-1])

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata[1:], fene_accum/fene_accum[-1], 'b-o', label=r'$H^{1}$'+'-POD')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([2, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'ene_in_flucf.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, v, 'b-o', label=r'$H^{1}$'+'-POD')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([1, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig.png')
ax.set_xlim([100, 1000])
ax.set_ylim([1e-12, 1e-4])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())
fig.savefig(tpath+'gram_eig_zoom_loglog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, v/ene_accum[-1], 'b-o', label=r'$H^{1}$'+'-POD')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\sum^N_{i=1}\lambda_i}$',rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
fig.savefig(tpath+'ene_permode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, v/ene_accum[0], 'b-o', label=r'$H^{1}$'+'-POD')
ax.axhline(y=0.01, color='k', linestyle='-')
ax.legend()
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\frac{\lambda_N}{\lambda_1}$', rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
fig.savefig(tpath+'ene_to1stmode.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, np.sqrt(ene_accum[-1]-ene_accum)/np.sqrt(ene_accum[-1]), 'b-o')
ax.axhline(y=1e-4, color='k', linestyle='-')
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\displaystyle\sqrt{\frac{\sum_{i>N}\lambda_i}{\sum_{i=1}\lambda_i}}$', rotation=90)
ax.set_xticks([1, 10, 100, 1000])
ax.set_ylim([1e-8, 1])
ax.legend()
fig.savefig(tpath+'Nmax.png')
fig.clf()

plt.style.use('report')
fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(xdata, v, 'b-o', label=r'$H^{1}$'+'-POD')
n_list = np.linspace(100, len(g), 50)
ax.semilogy(n_list, np.exp(-3.5*(n_list/100)+2), 'k-', label=r'$e^{(-3.5)}$')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xlim([100, len(g)])
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xticks(np.linspace(100, len(g), 5))
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig_zoom_semilog.png')
fig.clf()

fig, ax = plt.subplots(1, tight_layout=True)
ax.loglog(xdata, v, 'b-o', label=r'$H^{1}$'+'-POD')
ax.legend()
ax.set_ylabel(r'$\lambda_N$')
ax.set_xlabel(r'$N$')
ax.set_xticks([1, 10, 100, 1000])
ax.set_xlim([1, 1000])
ax.set_ylim([1e-12, 1e7])
fig.savefig(tpath+'gram_eig_2fig.png')

print('---------------------------------------')
print('POD modes information in the following:')
print('---------------------------------------')
print("gu rank:", Nmax)
Nflux = np.argmax(fene_accum/fene_accum[-1] > 0.9) + 2
print("90% fluctuating energy in u with N = ", Nflux)
print("95% fluctuating energy in u with N = ", np.argmax(fene_accum/fene_accum[-1] > 0.95) + 2)
print("99% fluctuating energy in u with N = ", np.argmax(fene_accum/fene_accum[-1] > 0.99) + 2)
N_g90pt = np.argmax((ene_accum/ene_accum[-1]) > 0.9) + 1
print("N: %3d contains %4.4f in total energy" % (N_g90pt, ene_accum[N_g90pt-1]/ene_accum[-1]))
N_l1pt = np.argmax(v/ene_accum[-1] < 0.01) + 1
print("N: %3d contains less than %4.4f in total energy" % (N_l1pt, v[N_l1pt-1]/ene_accum[-1]))
N_l1pfm = np.argmax(v/ene_accum[0] < 0.01) + 1
print("N: %3d contains less than %4.4f of the energy of the first mode" % (N_l1pfm, v[N_l1pfm-1]/ene_accum[0]))
N_max = np.argmax(np.sqrt(ene_accum[-1]-ene_accum)/np.sqrt(ene_accum[-1]) < 1e-4) + 1
print("N_max,vel: ", N_max)
print("Minimum Nu to be used is: ", N_g90pt)
print("Maximum Nu to be used is: ", N_max)
print("N = ", max(N_l1pt,N_g90pt), " is suggested")
