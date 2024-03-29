def cnuss_err(fmean,  fvar, fsd, rmean, rvar, rsd):
    mean_err = abs(fmean-rmean)/abs(fmean)
    var_err = abs(rvar-fvar)/abs(fvar)
    sd_err = abs(rsd-fsd)/abs(fsd)
    return mean_err,  var_err,  sd_err


def cmean(data, idx):
    import numpy as np
    mean = np.sum(data[:, idx])/len(data[:, idx])
    return mean


def cvar(data, mean, idx):
    import numpy as np
    var = np.sum((data[:, idx]-mean)**2)/(len(data[:, idx])-1)
    return var


def cstd(data, mean, idx):
    import numpy as np
    sigma = np.sqrt(cvar(data, mean, idx))
    return sigma


def read_nuss(fname):
    import numpy as np
    with open(fname,  'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k and
                     k != 'nuss' and k != 'nus'] for line
                     in list_of_lines][:-1]
    nuss = np.array(list_of_words).astype(np.float64)
    return nuss


def read_ei(fname):
    import numpy as np
    with open(fname,  'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k and
                     k != 'res:' and k != 'nus'] for line
                     in list_of_lines][:-1]
    ei = np.array(list_of_words).astype(np.float64)
    return ei


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    import re
    return [atoi(c) for c in re.split('(\d+)', text)]


def find_nearest(array, value):
    import numpy as np
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
