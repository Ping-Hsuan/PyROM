import sys
import subprocess


tpath = sys.argv[1]
N = sys.argv[2]
T0 = sys.argv[3]

subprocess.run(["python3", "dual_norm.py", tpath, N])
subprocess.run(["python3", "proj_relerr.py", tpath, N])
subprocess.run(["python3", "rom_abserr.py", tpath, N])
subprocess.run(["python3", "fom_norm.py", tpath, N])
subprocess.run(["python3", "effectivity.py", tpath, N])
subprocess.run(["python3", "dual_norm_scaled.py", tpath, N])
subprocess.run(["python3", "nu.py", tpath, N, T0])
subprocess.run(["python3", "romu.py", tpath, N])
subprocess.run(["python3", "romt.py", tpath, N])

