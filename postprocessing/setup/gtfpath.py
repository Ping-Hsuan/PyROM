def gtfpath(target_dir, pt1):
    import re
    import os
    filenames = []
    root = []
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in files:
            if re.match(pt1, name):
                filenames.append(os.path.join(root, name))
    return root, filenames
