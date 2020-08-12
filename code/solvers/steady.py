import numpy as np
import math 


def mor_f(x, *data):
    
    vel, tmp, N, theta, mu, kappa = data
    x = np.reshape(x, (2*N, 1))
    but = math.sin(theta*math.pi/180)*vel.but_x + \
            math.cos(theta*math.pi/180)*vel.but_y

    t = np.zeros((N,N+1))
    for i in range(0,N):
        t = t + np.reshape(vel.c[:,:,i+1], (N, N+1)) * x[i]
    cu = t[:,1:N+1]
    cum = np.reshape(vel.c[:,0,:], (N,N+1))
    cur = np.reshape(vel.c[:,:,0], (N,N+1))

    F1 = -mu*np.linalg.inv(vel.b)@vel.a@x[0:N]
    F1 = F1 - np.linalg.inv(vel.b)@cu@x[0:N]
    F1 = F1 - mu*np.linalg.inv(vel.b)@vel.a0[1:N+1,0, None]
    F1 = F1 - np.linalg.inv(vel.b)@cum[:,1:N+1]@x[0:N]
    F1 = F1 - np.linalg.inv(vel.b)@cur[:,1:N+1]@x[0:N]
    F1 = F1 - np.linalg.inv(vel.b)@vel.c[:,0,0, None]
    tt = np.insert(x[N:], 0, 1)
    F1 = F1 - np.linalg.inv(vel.b)@but[1:N+1,:]@np.reshape(tt, (N+1, 1))

    t = np.zeros((N,N+1))
    for i in range(0,N):
        t = t + np.reshape(tmp.c[:,:,i+1], (N, N+1)) * x[i]
    ct = t[:,1:N+1]
    ctm = np.reshape(tmp.c[:,0,:], (N,N+1))
    ctr = np.reshape(tmp.c[:,:,0], (N,N+1))

    F2 = -kappa*np.linalg.inv(tmp.b)@tmp.a@x[N:]
    F2 = F2 - np.linalg.inv(tmp.b)@ct@x[N:]
    F2 = F2 - kappa*np.linalg.inv(tmp.b)@tmp.a0[1:N+1,0, None]
    F2 = F2 - np.linalg.inv(tmp.b)@ctm[:,1:N+1]@x[0:N]
    F2 = F2 - np.linalg.inv(tmp.b)@ctr[:,1:N+1]@x[N:]
    F2 = F2 - np.linalg.inv(tmp.b)@tmp.c[:,0,0, None]

    F = np.append(F1, F2)
    return F
