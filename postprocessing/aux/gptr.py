def gptr(model, N=None, T0=None, mode=None, fd=None):
    ptr = '^.*_'
    if N is not None:
        ptr = ptr+model+'_'+N+'nb'
    else:
        ptr = ptr+model+'_(\d+)nb'
    if T0 == 1:
        ptr = ptr+'_ic_h10_'
    elif T0 > 1:
        ptr = ptr+'_zero_h10_'
    if fd is not None:
        print(fd, model)
        if model != 'l-rom' and model != 'l-rom-df':
            raise Exception("fd only supported for l-rom or l-rom-df")
        else:
#           ptr = ptr+'re(-?\d+)_'+fd+'_.*'
            ptr = ptr+'theta(-?\d+)_ra(-?\d+)_'+fd+'_.*'
    else:
#       ptr = ptr+'re(-?\d+)_.*'
        ptr = ptr+'theta(-?\d+)_ra(-?\d+)_.*'
    return ptr
