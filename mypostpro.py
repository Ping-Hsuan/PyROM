def cnuss_err(fmean,fvar,rmean,rvar):
    mean_err = abs(fmean-rmean)/abs(fmean)
    var_err = abs(rvar-fvar)/abs(fvar)
    return mean_err, var_err
