def text():
    '''Use sans-serif'''
    import matplotlib
    matplotlib.rcParams.update({"text.usetex": True, "font.family":
                                "sans-serif",
                                "font.sans-serif": ["Helvetica"]})
    return
