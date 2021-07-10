from itertools import accumulate
import numpy as np


def cfer(pod_eig):
    # compute fluctuation energy ratio for each N
    # sum^N_{i=2} \lambda_i / sum^K_{i=2} \lambda_i
    fene = list(accumulate(pod_eig[1:]))
    fer = fene/fene[-1]
    return fer


def cett(pod_eig):
    # compute the ratio of each POD mode to total POD modes
    # \lambda_N / sum^K_{i=1} \lambda_i
    total = np.sum(pod_eig)
    ett = pod_eig/total
    return ett


def cetf(pod_eig):
    # compute the ratio of each POD mode to first POD mode
    # \lambda_N / \lambda_1
    etf = pod_eig/pod_eig[0]
    return etf


def ceps(pod_eig):
    # compute the epsilon which is defined as
    # epsilon = ( sum_{i>N} \lambda_i / sum^K_{i} \lambda_i )
    ene = list(accumulate(pod_eig))
    total = np.sum(pod_eig)
    eps = np.sqrt(total-ene)/np.sqrt(total)
    return eps


def cene(pod_eig):
    # compute sum_{i>N} \lambda_i
    ene = list(accumulate(pod_eig))
    return ene


def N_fergp(fer, percent):
    # Compute N such that fer
    # is greater than given percentage
    N = np.argmax(fer > percent) + 2
    return N


def N_egpint(ene, percent):
    # Compute the number of modes required to contain
    # given percentage of the total energy
    N = np.argmax((ene/ene[-1]) > percent) + 1
    return N


def N_ettlp(ett, percent):
    # Compute the first POD modes that is less than
    # given percentage of the total energy
    N = np.argmax(ett < percent) + 1
    return N


def N_etflp(etf, percent):
    # Compute the first POD modes that is less than
    # given percentage of the first POD mode
    N = np.argmax(etf < percent) + 1
    return N


def N_epslp(eps, percent):
    # Compute the N_max based on the eps with the given percent
    N = np.argmax(eps < percent) + 1
    return N
