import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import os
import sys
import operator

#plt.style.use('report')

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]

print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
os.chdir(str(sys.argv[1]))
deg = sys.argv[2]

N_list = np.loadtxt(os.getcwd()+'/rom_abserr/N_list_'+deg+'.dat')
fom_norm = np.loadtxt(os.getcwd()+'/fom_norm/fom_norm.dat')
rom_abserr = np.loadtxt(os.getcwd()+'/rom_abserr/rom_abserr_theta_'+deg+'.dat')
proj_relerr = np.loadtxt(os.getcwd()+'/proj_relerr/proj_relerr_theta_'+deg+'.dat')
dual_norm = np.loadtxt(os.getcwd()+'/dual_norm/erri_theta_'+deg+'.dat')

train_deg = np.linspace(0, 180, 19)
idx = np.where(train_deg == int(deg))
print(idx)

fig, ax = plt.subplots(1, tight_layout=True)
ax.semilogy(N_list, rom_abserr, 'b-o', label='Constrained ROM')
ax.semilogy(N_list, proj_relerr*fom_norm[idx], 'k-o', label='Projection')
#ax.semilogy(N_list, dual_norm, 'r-o', label='dual norm of the discrete time averaged residual')
ax.set_title(r'Comparison of the absolute $H^1$ error in the mean flow at $\theta_g='+deg+'$')
ax.set_xlabel(r'N')
ax.legend(loc=1)
fig.savefig(os.getcwd()+'/abserr_compare.png')

ax.semilogy(N_list, dual_norm, 'b--o', label='Dual norm')
ax.set_title(r'Comparison of the absolute $H^1$ error'+ 'in the mean flow \n at '+r'$\theta_g='+deg+'$ with dual norm')
ax.legend(loc=1)
fig.savefig(os.getcwd()+'/dual_abserr_compare.png')
