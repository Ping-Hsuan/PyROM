import sys
import subprocess


tpath = sys.argv[1]
theta = sys.argv[2]
T0 = sys.argv[3]

subprocess.run(["python3", "dual_norm_theta.py", tpath, theta])
subprocess.run(["python3", "relerr_theta.py", tpath, theta])
subprocess.run(["python3", "abserr_theta.py", tpath, theta])
subprocess.run(["python3", "mnu_theta.py", tpath, theta, T0])
