import sys
import os
import subprocess
import operator
import yaml
#sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
import aux
from mor import ROM

# This python script is used to plot reproduction results
# You must the model and the parameter theta_g
# (for now only support for theta_g)

# Extract user specify features
with open('reproduction.yaml') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)

rom = ROM(info)
rom.get_data()
rom.field = 'u'
rom.get_coef()
rom.compute_momentum()
aux.plt_coef_in_t(rom)
1/o
setup_path = os.getcwd()
model = info['formulation']

dir1 = model+'_reproduction'
for key, value in info['parameters'].items():
    dir1 += '_'+str(key)+'_'+str(value)
T0 = info['T0']
N = info['nb']

tpath = os.path.join(setup_path, dir1)
isExist = os.path.exists(tpath)
if isExist:
    pass
else:
    os.mkdir(tpath)

for feature in info['features'].keys():
    search_dir = model+'_info'
    fnames = aux.gtfpath(search_dir, '^.*_h10_.*_'+feature)
#   files_dict = aux.create_dict(fnames, '^.*_([0-9]*)nb_.*$')
    # sort the dictionary key
#   dict_final = sorted(files_dict.items(), key=operator.itemgetter(0))
    data = aux.get_data(fnames, feature, info)

1/o
#subprocess.run(["python3", "grep_data.py", setup_path, model])
#subprocess.run(["python3", "romt.py", tpath, model, theta_g, N])
subprocess.run(["python3", "romu.py", tpath, model, theta_g, N])
#subprocess.run(["python3", "relerr_wN.py", tpath, model, theta_g])
#subprocess.run(["python3", "abserr_wN.py", tpath, model, theta_g])
#subprocess.run(["python3", "rom_norm_wN.py", tpath, model, theta_g])
#subprocess.run(["python3", "nu_first_second_momentum_wN.py", tpath, model, theta_g, T0])
