import sys
import subprocess
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
# This python script is used to plot parametric results.
# You must specify the model and the POD mdoe N.

tpath = sys.argv[1]
model = sys.argv[2]
N = sys.argv[3]
T0 = sys.argv[4]

subprocess.run(["python3", "dual_norm_wparam.py", tpath, model, N, T0])
subprocess.run(["python3", "relerr_wparam.py", tpath, model, N, T0])
subprocess.run(["python3", "abserr_wparam.py", tpath, model, N, T0])
subprocess.run(["python3", "rom_norm_wparam.py", tpath, model, N, T0])
subprocess.run(["python3", "nu_first_second_momentum_wparam.py", tpath, model, N, T0])
