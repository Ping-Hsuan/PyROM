def style(num_fig):
    import matplotlib.pyplot as plt

    if num_fig == 1:
        plt.style.use('report_1fig')
    elif num_fig == 2:
        plt.style.use('report')
    elif num_fig == 3:
        plt.style.use('report_3fig')
    elif num_fig == 4:
        plt.style.use('report_4fig')
    return


def color(idx):
    import matplotlib.cm as cm
    import numpy as np
    if idx == 0:
        colors = cm.tab10(np.linspace(0, 1, 10))
    elif idx == 1:
        colors = cm.tab20(np.linspace(0, 1, 20))
    return colors


def text():
    import matplotlib

    matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need.  ..
    r'\sisetup{detect-all}',   # ...this to force siunitx to actually use you  r fonts
    r'\usepackage{helvet}',    # set the normal font here
    r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
    r'\sansmath'               # <- tricky! -- gotta actually tell tex to use  !
    ]

    return


def checkdir(target_dir):
    import os

    isExist = os.path.exists(os.getcwd()+target_dir)
    if isExist:
        pass
    else:
        os.mkdir(os.getcwd()+target_dir)

    return


def gtfpath(target_dir, pt1):
    import re
    import os
    filenames = []
    root = []
    for root, dirs, files in os.walk('.'+target_dir, topdown=False):
        for name in files:
            if re.match(pt1, name):
#               print(os.path.join(root, name))
                filenames.append(os.path.join(root, name))
    return root, filenames


def create_dict(filenames, pt):
    import re
    dict = {}
    for fname in filenames:
        match = re.match(pt, fname)
        if match:
            if match.groups()[0] not in dict:
                dict[match.groups()[0]] = []
            dict[match.groups()[0]].append(fname)

    return dict


def find_anchor():
    import os
    import re
    root = os.getcwd()
    sp1 = (root.split('/'))
    for element in sp1:
        z = re.match(r"theta_(\d+)", element)
        if z:
            anchor = float(((z.groups())[0]))
    return anchor
