def color(idx):
    import matplotlib.cm as cm
    import numpy as np
    if idx == 0:
        colors = cm.tab10(np.linspace(0, 1, 10))
    elif idx == 1:
        colors = cm.tab20(np.linspace(0, 1, 20))
    return colors
