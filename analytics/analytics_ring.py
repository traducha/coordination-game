# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np


def find_steady(config=None):
    R = config['R']
    P = config['P']
    S = config['S']
    T = config['T']
    alpha = (T-S)/(R-S)
    beta = (P-S)/(R-S)
    if alpha > beta:
        k_star = 1.0 / (1.0 - alpha)
    else:
        k_star = 2.0 / (2.0 - (alpha + beta))
    n_min = k_star * (k_star + 1.0)
    return k_star, n_min


def plot_ring():
    conf = {"R": 1, "P": 0, "S": None, "T": None}
    res_k = []
    res_n = []
    for T in np.linspace(-2, 0.95, 300):
        conf['T'] = T
        res_in_k = []
        res_in_n = []
        for S in np.linspace(-3, 0, 300):
            conf['S'] = S
            k, n = find_steady(config=conf)
            if T-S<1:
                res_in_k.append(5)
            else:
                res_in_k.append(k)
            res_in_n.append(n)
        res_k.append(res_in_k)
        res_n.append(res_in_n)

    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(res_k, cmap='jet', origin='lower', extent=[-3, 0, -2, 0.95], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    cbar.set_clim(0, 1)

    plt.title('k*')
    plt.axhline(1, linestyle='-', color='black')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.tight_layout()
    plt.savefig('k_star2.pdf')
    plt.show()
    plt.close()

    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(res_n, cmap='jet', origin='lower', extent=[-3, 0, -2, 0.95], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    cbar.set_clim(0, 1)

    plt.title('N min')
    plt.axhline(1, linestyle='-', color='black')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.tight_layout()
    plt.savefig('n_min2.pdf')
    plt.show()


if __name__ == '__main__':
    # conf = {
    #     "R": 1,
    #     "P": 0,
    #     "S": -1,
    #     "T": -1,
    # }
    # print(find_steady(config=conf))
    plot_ring()

