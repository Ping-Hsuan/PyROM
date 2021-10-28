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
        if model != 'l-rom' or model != 'l-rom_df':
            raise Exception("fd only supported for l-rom or l-rom_df")
        else:
            ptr = ptr+'(-?\d+)_(-?\d+)_'+fd+'_.*'
    else:
        ptr = ptr+'(-?\d+)_(-?\d+)_.*'
    return ptr
