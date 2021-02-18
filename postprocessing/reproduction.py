import sys
import subprocess
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
# This python script is used to plot reproduction results
# You must the model and the parameter theta_g
# (for now only support for theta_g)

tpath = sys.argv[1]
model = sys.argv[2]
theta_g = sys.argv[3]
T0 = sys.argv[4]
N = sys.argv[5]

subprocess.run(["python3", "dual_norm_wN.py", tpath, model, theta_g])
subprocess.run(["python3", "romt.py", tpath, model, theta_g, N])
subprocess.run(["python3", "romu.py", tpath, model, theta_g, N])
subprocess.run(["python3", "relerr_wN.py", tpath, model, theta_g])
subprocess.run(["python3", "abserr_wN.py", tpath, model, theta_g])
subprocess.run(["python3", "rom_norm_wN.py", tpath, model, theta_g])
subprocess.run(["python3", "nu_first_second_momentum_wN.py", tpath, model, theta_g, T0])
