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
    t_line = []
    s_line = []
    for T in np.linspace(-2, 0.85, 300):
        conf['T'] = T
        res_in_k = []
        res_in_n = []
        s_trans = None
        for S in np.linspace(-3, 0, 300):
            conf['S'] = S
            k, n = find_steady(config=conf)
            if (0-S)/(1-S) >= 1 or (T-S)/(1-S) <= 0 or (T-S)/(1-S) >= 1:
                res_in_k.append(-100)
                res_in_n.append(-200)
            else:
                res_in_k.append(k)
                res_in_n.append(n)
            if k <= 8 and s_trans is None:
                s_trans = S
                t_line.append(T)
                s_line.append(s_trans)
        res_k.append(res_in_k)
        res_n.append(res_in_n)

    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(res_k, cmap='jet', origin='lower', extent=[-3, 0, -2, 0.85], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    plt.clim(0, 27)
    # cbar.set_clim(0, 26)

    plt.ylim([-2, 1])
    plt.title('k*')

    t_list = list(np.linspace(-2, 1, 40))
    s_list8 = [-3.0, -2.923076923076923, -2.769230769230769, -2.5384615384615383, -2.3846153846153846, -2.1538461538461537, -2.0, -1.7692307692307692, -1.6153846153846154, -1.3846153846153846, -1.2307692307692306, -1.0769230769230769, -0.8461538461538458, -0.6153846153846154, -0.46153846153846123]
    plt.plot(s_list8, t_list[40-len(s_list8):], linestyle='--', color='black')
    plt.plot(s_line, t_line, linestyle='-', color='black')
    # plt.axhline(1, linestyle='-', color='black')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.tight_layout()
    plt.savefig('k_star2.pdf')
    plt.show()
    plt.close()

    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(res_n, cmap='jet', origin='lower', extent=[-3, 0, -2, 0.85], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    plt.clim(0, 700)
    # cbar.set_clim(0, 1)

    plt.ylim([-2, 1])
    plt.title('N min')
    # plt.axhline(1, linestyle='-', color='black')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.tight_layout()
    plt.savefig('n_min2.pdf')
    plt.show()


def plot_t_const():
    conf = {"R": 1, "P": 0, "S": None, "T": -1}
    res_k = []
    res_n = []
    t_line = []
    s_line = []

    S_list = np.linspace(-11, -1.1, 300)
    for S in S_list:
        conf['S'] = S
        k, n = find_steady(config=conf)
        if (0-S)/(1-S) >= 1 or (conf['T']-S)/(1-S) <= 0 or (conf['T']-S)/(1-S) >= 1:
            res_k.append(-100)
            res_n.append(-200)
        else:
            res_k.append(k)
            res_n.append(n)

    fig = plt.figure(figsize=(4, 3.5))
    plt.plot(S_list, res_k)
    # plt.ylim([-2, 1])

    plt.xlabel('S')
    plt.ylabel('k*')
    plt.tight_layout()
    plt.savefig('k_star_on_S.pdf')
    plt.show()
    plt.close()

    fig = plt.figure(figsize=(4, 3.5))
    plt.plot(S_list, res_n)
    # plt.ylim([-2, 1])

    plt.xlabel('S')
    plt.ylabel('Nmin')
    plt.tight_layout()
    # plt.savefig('k_star2.pdf')
    plt.show()

if __name__ == '__main__':
    # plot_ring()
    plot_t_const()
