def grep_files(src_dir, N=None):
    import os
    import re

    if N is None:
        ptr = '^.*_(.*)rom_.*$'
    else:
        ptr = '^.*_(.*)rom_'+N+'nb_.*$'
    # re.match('^.*_(.*)rom_(?!.*-90|.*-80|.*-70).*$'

    filenames = []
    for root, dirs, files in os.walk(os.path.join('.', src_dir),
                                     topdown=False):
        for name in files:
            if re.match(ptr, name):
                filenames.append(name)
        for name in dirs:
            pass

    return root, filenames
