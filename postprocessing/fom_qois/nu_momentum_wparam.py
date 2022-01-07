def nu_momentum_wparam():
    import numpy as np
    import yaml
    import pandas as pd
    import matplotlib.pyplot as plt

    # get the FOM data
    with open('fom.yaml') as f:
        features = yaml.load(f, Loader=yaml.FullLoader)
    dic = features['train_set']
    for i, key in enumerate(dic.keys()):
        print(key+": ", dic[key])
        param = key
    fom_means = []
    fom_stds = []
    params = []
    for tp in dic[key]:
        # get the FOM data
#       filename = param+str(tp)+'/nus_mom.csv'
        filename = param+str(tp)+'/theta_90/nus_mom.csv'
        data = pd.read_csv(filename)
        fom_mean, fom_sd = [data[i].to_numpy() for i in data.columns]
        fom_means.append(fom_mean)
        fom_stds.append(fom_sd)
        params.append(float(tp))
    data = np.column_stack((params, fom_means, fom_stds))
    data = data[data[:, 0].argsort()]
    
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 0], data[:, 1], 'k-o', label='FOM')
    ax.set(xlabel=param)
    ax.set_title('FOM Mean Nu with '+r'$'+param+'$')
    ax.legend(loc=0)
    fig.savefig('mnus_wparam.png')
    fig.clf()
    fig, ax = plt.subplots(1, tight_layout=True)
    ax.plot(data[:, 0], data[:, 2], 'k-o', label='FOM')
    ax.set(xlabel=param)
    ax.set_title('FOM Std(Nu) with '+r'$'+param+'$')
    ax.legend(loc=0)
    fig.savefig('stdnus_wparam.png')
    return


if __name__ == '__main__':
    import sys
    nu_momentum_wparam()
