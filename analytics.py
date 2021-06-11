# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np


def system(x, d_t, config):
    R = config['R']
    P = config['P']
    S = config['S']
    T = config['T']

    d_x = (S+T-R-P) * x**3.0 + (2*P-2*S-T+R) * x**2.0 + (S-P) * x

    return d_x * d_t

def system2(x, d_t, config):
    """
    for UI and BR mean field, only for R=1, P=0
    :param x:
    :param d_t:
    :param config:
    :return:
    """
    R = 1
    P = 0
    S = config['S']
    T = config['T']

    d_x = np.heaviside(x + (S / (1.0-S-T)), 0) - x

    return d_x * d_t


def find_steady(config=None):
    d_x = 1.0
    d_t = 0.01
    x = 1.0/2.0
    i = 0
    while np.abs(d_x) > 1e-06:
        d_x = system2(x, d_t, config=config)
        x = min(max(x + d_x, 0.0), 1.0)
        i += 1
        if i > 100000:
            print(config)
            break
    return x


def plot_repicator():
    conf = {"R": 1, "P": 0, "S": None, "T": None}
    res = []
    for T in np.linspace(-2, 1, 100):
        conf['T'] = T
        res_in = []
        for S in np.linspace(-3, 0, 100):
            conf['S'] = S
            res_in.append(find_steady(config=conf))
        res.append(res_in)

    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(res, cmap='jet', origin='lower', extent=[-3, 0, -2, 1], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    cbar.set_clim(0, 1)

    plt.title('Mean field')
    plt.axvline(-1, linestyle='--')
    plt.axvline(-2, linestyle='--')
    plt.axhline(-1, linestyle='--')
    plt.axhline(0, linestyle='--')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.tight_layout()
    plt.savefig('mean_field.pdf')
    plt.show()


if __name__ == '__main__':
    # conf = {
    #     "R": 1,
    #     "P": 0,
    #     "S": -1,
    #     "T": -1,
    # }
    # print(find_steady(config=conf))
    plot_repicator()

