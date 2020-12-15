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


def find_steady(config=None):
    d_x = 1.0
    d_t = 0.01
    x = 0.5
    i = 0
    while np.abs(d_x) > 1e-06:
        d_x = system(x, d_t, config=config)
        x = min(max(x + d_x, 0.0), 1.0)
        i += 1
        if i > 100000:
            print(config)
            break
    return x


def plot_repicator():
    conf = {"R": 1, "P": 0, "S": None, "T": None}
    res = []
    for T in np.linspace(0, 2, 50):
        conf['T'] = T
        res_in = []
        for S in np.linspace(-1, 1, 50):
            conf['S'] = S
            res_in.append(find_steady(config=conf))
        res.append(res_in)

    im = plt.imshow(res, cmap='jet', origin='lower', extent=[-1, 1, 0, 2], interpolation='none')
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cbar = plt.colorbar(im, norm=norm)
    # cbar.ax.tick_params(labelsize=9)

    plt.axvline(0, linestyle='--')
    plt.axhline(1, linestyle='--')

    plt.xlabel('S')
    plt.ylabel('T')
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

