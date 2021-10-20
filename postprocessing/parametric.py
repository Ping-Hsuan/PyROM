import sys
import os
import subprocess
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import setup
# This python script is used to plot parametric results.
# You must specify the model and the POD mdoe N.

setup_path = sys.argv[1]
model = sys.argv[2]
N = sys.argv[3]
T0 = sys.argv[4]
theta_g = sys.argv[5]
mode = sys.argv[6]
if model == 'l-rom':
    fd = input("Enter filter percentage")

tpath = setup_path+'/'+model+'_parameter_ra_'+str(theta_g)
isExist = os.path.exists(tpath)
if isExist:
    pass
else:
    os.mkdir(tpath)

subprocess.run(["python3", "grep_data.py", setup_path, model, N])

if model != 'l-rom':
    subprocess.run(["python3", "dual_norm_wparam.py", tpath, model, N, T0, mode])
    subprocess.run(["python3", "relerr_wparam.py", tpath, model, N, T0, mode])
    subprocess.run(["python3", "abserr_wparam.py", tpath, model, N, T0, mode])
    subprocess.run(["python3", "nu_first_second_momentum_wparam.py", tpath, model, N, T0, mode])
else:
    subprocess.run(["python3", "dual_norm_wparam.py", tpath, model, N, T0, mode, fd])
    subprocess.run(["python3", "relerr_wparam.py", tpath, model, N, T0, mode, fd])
    subprocess.run(["python3", "abserr_wparam.py", tpath, model, N, T0, mode, fd])
    subprocess.run(["python3", "nu_first_second_momentum_wparam.py", tpath, model, N, T0, mode, fd])
#subprocess.run(["python3", "vel_dual_norm_wparam.py", tpath, model, N, T0, mode])
#subprocess.run(["python3", "temp_dual_norm_wparam.py", tpath, model, N, T0, mode])

#subprocess.run(["python3", "vel_relerr_wparam.py", tpath, model, N, T0, mode])
#subprocess.run(["python3", "temp_relerr_wparam.py", tpath, model, N, T0, mode])
#subprocess.run(["python3", "vel_abserr_wparam.py", tpath, model, N, T0, mode])
#subprocess.run(["python3", "temp_abserr_wparam.py", tpath, model, N, T0, mode])


#subprocess.run(["python3", "fom_norm.py", tpath, model, N, T0, mode])
#subprocess.run(["python3", "rom_norm_wparam.py", tpath, model, N, T0, mode])

#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'rom', mode])
#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'fom', mode])
#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'romabserr', mode])
#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom', mode])
#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta', mode])
#subprocess.run(["python3", "dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom_all', mode])

#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'rom', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'fom', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'romabserr', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom_all', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta', mode])
#subprocess.run(["python3", "vel_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'domain', mode])

#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'rom', mode])
#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'fom', mode])
#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'romabserr', mode])
#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom', mode])
#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta', mode])
#subprocess.run(["python3", "temp_dual_norm_scaled_wparam.py", tpath, model, N, T0, 'eta_rom_all', mode])
