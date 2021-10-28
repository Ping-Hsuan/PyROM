def mysave(fig, tdir, data, feature, header, N=None, fd=None):
    import numpy as np
    if N:
        if fd:
            fig.savefig(tdir+feature+'_N'+N+'_'+fd+'.png')
            np.savetxt(tdir+feature+'_N'+N+'_'+fd+'.csv', data, delimiter=',', header=header, comments="")
        else:
            fig.savefig(tdir+feature+'_N'+N+'.png')
            np.savetxt(tdir+feature+'_N'+N+'.csv', data, delimiter=',', header=header, comments="")
    else:
        if fd:
            fig.savefig(tdir+feature+'_'+fd+'.png')
            np.savetxt(tdir+feature+'_'+fd+'.csv', data, delimiter=',', header=header, comments="")
        else:
            fig.savefig(tdir+feature+'.png')
            np.savetxt(tdir+feature+'.csv', data, delimiter=',', header=header, comments="")
