import sys
import subprocess


tpath = sys.argv[1]
theta = sys.argv[2]
T0 = sys.argv[3]

subprocess.run(["python3", "dual_norm_wN.py", tpath, theta])
subprocess.run(["python3", "relerr_wN.py", tpath, theta])
subprocess.run(["python3", "abserr_wN.py", tpath, theta])
subprocess.run(["python3", "rom_norm_wN.py", tpath, theta])
subprocess.run(["python3", "nu_first_second_momentum_wN.py", tpath, theta, T0])
