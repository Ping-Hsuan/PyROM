import numpy as np
import sys
import os
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import online
import csv
import yaml
import math
from figsetup.style import style
from figsetup.text import text
from figsetup.color import color
from hg.helpers import est_nu_1st2nd
from hg.helpers import get_FOM_nu_1st2nd
from hg.helpers import plt_est_erri
from hg.helpers import plt_est_mnu
from hg.helpers import plt_est_stdnu
from hg.helpers import plt_est_mnuerr
from hg.helpers import plt_est_rom_mfldrelerr
from hg.helpers import plt_est_proj_mfldrelerr
from hg.helpers import est_mean_fld_relerr
from hg.helpers import est_mtke
from hg.helpers import get_optmtke
from hg.helpers import get_FOM_mtke
from hg.helpers import plt_est_mtke
from hg.helpers import est_mtfluc
from hg.helpers import get_FOM_mtfluc
from hg.helpers import plt_est_mtfluc

style(1)
text()
colors = color(0)

print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print('Crrent directory is:', os.chdir(str(sys.argv[1])))
model = str(sys.argv[2])
ncand = int(sys.argv[3])
mode = str(sys.argv[4])
print('The model is:', model)
print("---------------------------------------------")

if len(sys.argv) >= 6:
    pt = '_sc_'+str(sys.argv[5])
else:
    pt = ''

with open('../hg_'+model+'_off/train_info'+pt+'.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)
data = []
for i, key in enumerate(features.keys()):
    data.append(features[key])

# make it list
P_test = [int(item) for item in features['Ptrain']]
#P_test = np.array(features['Ptrain'], dtype=int)

print("POD-hGreedy information:")
print("Iteration: ", data[0])
print("Anchor points: ", data[1])
print("N: ", data[2])
print("K: ", data[3])
print("---------------------------------------------")
Itr_list = data[0]
anch_list = data[1]
N_list = data[2]
K_list = data[3]
model_list = data[6]
fd = data[7]

mnurelerr = []

with open('./online.yaml') as f:
    onlfeature = yaml.load(f, Loader=yaml.FullLoader)

for itr in Itr_list:
    P_train = np.array(anch_list[0:itr], dtype=int)
    P_test_anchor = online.get_ncand_param(P_test, P_train, ncand,
                                     N_list[:itr], model_list, mode, fd, pt)
    print(P_test_anchor)
    print("ncand anchor points for each test parameter", P_test_anchor)

    param, erri_all, opt_erri = online.get_opterri_param(P_test, P_train, N_list[:itr],
                                  P_test_anchor, model_list, mode, fd, pt)
    plt_est_erri(itr, ncand, param, erri_all, opt_erri, P_train, features, model)

    if (onlfeature['mnu']):
        param, merr_all, m_all, std_all = est_nu_1st2nd(features, P_train, N_list[:itr], model_list, mode, fd)
        opt_merr_nu, opt_m_nu, opt_std_nu = online.get_optqoi(merr_all, m_all, std_all, P_test, P_train, P_test_anchor, model_list, pt)
        fom_m_list, fom_std_list = get_FOM_nu_1st2nd(P_test)
        plt_est_mnu(itr, ncand, param, m_all, opt_m_nu, P_train, features, model, fom_m_list)
        plt_est_stdnu(itr, ncand, param, std_all, opt_std_nu, P_train, features, model, fom_std_list)
        plt_est_mnuerr(itr, ncand, param, merr_all, opt_merr_nu, P_train, features, model)

    if (onlfeature['mrelerr_h1']):
        param, flderr_rom_all, flderr_proj_all = est_mean_fld_relerr(features, P_train, N_list[:itr], model_list, mode, fd)
        opt_flderr_rom, opt_flderr_proj = online.get_optflderr(flderr_rom_all, flderr_proj_all, P_test, P_train, P_test_anchor, model_list, pt)
        plt_est_rom_mfldrelerr(itr, ncand, param, opt_flderr_rom, P_train, features, model)
        plt_est_proj_mfldrelerr(itr, ncand, param, opt_flderr_proj, P_train, features, model)

    if (onlfeature['mtke']):
        param, mtke = est_mtke(features, P_train, N_list[:itr], model_list, mode, fd)
        opt_mtke = get_optmtke(mtke, P_test, P_train, P_test_anchor, model_list)
        fom_mtke = get_FOM_mtke(P_test)
        plt_est_mtke(itr, ncand, param, mtke, opt_mtke, P_train, features, model, fom_mtke)

    if (onlfeature['mtfluc']):
        param, mtfluc = est_mtfluc(features, P_train, N_list[:itr], model_list, mode, fd)
        opt_mtfluc = get_optmtke(mtfluc, P_test, P_train, P_test_anchor, model_list)
        fom_mtfluc = get_FOM_mtfluc(P_test)
        plt_est_mtfluc(itr, ncand, param, mtfluc, opt_mtfluc, P_train, features, model, fom_mtfluc)
