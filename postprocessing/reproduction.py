import sys
import os
import yaml
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
import aux
from mor import ROM

# This python script is used to plot "reproduction" results
# What you should do before running this script:
# 1. Specify the reproduction.yaml in the directory you put the logfile
# 2. Run the grep_data script.
# Once the two steps above are doen, simple call this script
# It will done the postprocessing for you

# Extract user specify features
with open('reproduction.yaml') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)

# Setup the directory
setup_path = os.getcwd()
dir1 = info['method']+'_reproduction'
for key, value in info['parameters'].items():
    dir1 += '_'+str(key)+'_'+str(value)
tpath = os.path.join(setup_path, dir1)
isExist = os.path.exists(tpath)
if isExist:
    pass
else:
    os.mkdir(tpath)

# Start postprocessing
rom = ROM(info)
rom.get_data()

if (info['features']['romu'] and info['ifrom(1)']):
    rom.field = 'u'
    rom.get_coef()
    rom.compute_momentum()
    aux.plt_coef_in_t(rom, tpath)

if (info['features']['romt'] and info['ifrom(2)']):
    rom.field = 'T'
    rom.get_coef()
    rom.compute_momentum()
    aux.plt_coef_in_t(rom, tpath)

if (info['features']['dual_norm']):
    rom.get_dual_wN()
    aux.plt_erri_w_N(rom, tpath)

if (info['features']['mrelerr']):
    rom.get_mrelerr()
    aux.plt_mrelerr_w_N(rom, tpath)

if (info['features']['mabserr']):
    rom.get_mabserr()
    aux.plt_mabserr_w_N(rom, tpath)

if (info['features']['rom_norm']):
    rom.get_rom_norm()
    aux.plt_rom_norm_w_N(rom, tpath)
#subprocess.run(["python3", "nu_first_second_momentum_wN.py", tpath, model, theta_g, T0])
