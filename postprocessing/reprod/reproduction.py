import sys
import os
import yaml
sys.path.append('/home/pht2/Developer/PyROM/code/post_pro/')
import aux1
from reprod.mor import ROM

# This python script is used to plot "reproduction" results
# What you should do before running this script:
# 1. Specify the reproduction.yaml in the directory you put the logfile
# 2. Run the grep_data script.
# Once the two steps above are doen, simple call this script
# It will done the postprocessing for you

# Extract user specify features
with open('reproduction.yaml') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)

info['method'] = sys.argv[1]

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


if (info['features']['dual_norm']):
    rom.get_dual_wN()
    aux1.plt_erri_wN(rom, tpath)

if (info['features']['mrelerr_h1']):
    rom.get_mrelerr('mrelerr_h1')
    aux1.plt_mrelerr_wN(rom, tpath, 'mrelerr_h1')

if (info['features']['mrelerr_l2']):
    rom.get_mrelerr('mrelerr_l2')
    aux1.plt_mrelerr_wN(rom, tpath, 'mrelerr_l2')

if (info['features']['mabserr_l2']):
    rom.get_mabserr('mabserr_l2')
    aux1.plt_mabserr_wN(rom, tpath, 'mabserr_l2')

if (info['features']['mabserr_h1']):
    rom.get_mabserr('mabserr_h1')
    aux1.plt_mabserr_wN(rom, tpath, 'mabserr_h1')

if (info['features']['rom_norm']):
    rom.get_rom_norm()
    aux1.plt_rom_norm_w_N(rom, tpath)

if (info['features']['tke'][0]):
    rom.get_tke()
    for nb in info['features']['tke'][1:]:
        aux1.plt_tke_in_t(rom, nb, tpath)

if (info['features']['romu'][0] and info['ifrom(1)']):
    rom.field = 'u'
    for nb in info['features']['romu'][1:]:
        rom.get_coef(nb)
        rom.compute_momentum()
        aux1.plt_coef_in_t(rom, nb, tpath)

if (info['features']['romt'][0] and info['ifrom(2)']):
    rom.field = 'T'
    for nb in info['features']['romt'][1:]:
        rom.get_coef(nb)
        rom.compute_momentum()
        aux1.plt_coef_in_t(rom, nb, tpath)

if (info['features']['mtke'][0]):
    rom.get_mtke()
    aux1.plt_mtke(rom, tpath)
1/o
#subprocess.run(["python3", "nu_first_second_momentum_wN.py", tpath, model, theta_g, T0])
