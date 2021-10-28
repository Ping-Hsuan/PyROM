def style(num_fig):
    import matplotlib.pyplot as plt

    if num_fig == 1:
        plt.style.use('report_1fig')
    elif num_fig == 2:
        plt.style.use('report_2fig')
    elif num_fig == 3:
        plt.style.use('report_3fig')
    elif num_fig == 4:
        plt.style.use('report_4fig')
    return
