def grep_feature(filenames, feature, ptr, sdir, tdir):
    import os
    import re
    from aux.create_dir import create_dir

    fdir = os.path.join(tdir, feature)
    create_dir(fdir)

    for fname in filenames:
        target_dir = os.path.join(fdir, fname+'_'+feature)
        ft = open(target_dir, 'w')
        with open(os.path.join(sdir, fname), 'r') as f:
            for line in f:
                if re.search(ptr, line):
                    ft.write(line)
        ft.close()
    return
