# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import time
import os

import constants as const
from config import config_values
from tools import run_with_time, save_stationary_generic, read_stationary_generic, plot_over_two_params


T_list = np.linspace(-2, 1, 40)
S_list = np.linspace(-3, 0, 40)

coop_mean = []
coop_std = []
active_mean = []
active_std = []
time_mean = []
time_std = []
names = ['coop_mean', 'coop_std', 'active_mean', 'active_std', 'time_mean', 'time_std']
names2 = ['cooperators', 'cooperators std', 'active links', 'active links std', 'therm. time', 'therm. time std']
short = {const.REPLICATOR: 'RD', const.BEST_RESPONSE: 'BR', const.UNCOND_IMITATION: 'UI'}

trans_S = []
for T in T_list:
    coop_mean_s = []
    coop_std_s = []
    active_mean_s = []
    active_std_s = []
    time_mean_s = []
    time_std_s = []

    _trans_S = -3
    updated = False

    for S in S_list:
        try:
            config = dict(config_values, update_str_type=const.UNCOND_IMITATION, T=T, S=S, av_degree=32)
            res, _ = read_stationary_generic(config, directory=f'imit_new_res32')
            alpha = np.mean(res['left_fraction'])
            coop_mean_s.append(alpha)
            coop_std_s.append(np.std(res['left_fraction']))
            active_mean_s.append(np.mean(res['active_density']))
            active_std_s.append(np.std(res['active_density']))
            time_mean_s.append(np.mean(res['convergence_time']))
            time_std_s.append(np.std(res['convergence_time']))

            if alpha > 0.7 and not updated:
                _trans_S = S
                updated = True
        except Exception:
            print('BAD', T, S)
            coop_mean_s.append(0.5)
            coop_std_s.append(0)
            active_mean_s.append(0.45)
            active_std_s.append(0)
            time_mean_s.append(0)
            time_std_s.append(0)

    trans_S.append(_trans_S)

    coop_mean.append(coop_mean_s)
    coop_std.append(coop_std_s)
    active_mean.append(active_mean_s)
    active_std.append(active_std_s)
    time_mean.append(time_mean_s)
    time_std.append(time_std_s)

print(trans_S)

for i, param in enumerate([coop_mean]):#, coop_std, active_mean, active_std, time_mean, time_std]):
    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(param, cmap='jet', origin='lower', extent=[-3, 0, -2, 1], interpolation='none')
    # plt.plot([-3, 0], [-2, 1], linestyle='--', color='black')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    if i in [0, 1]:
        cbar.mappable.set_clim(0, 1)
    elif i in [2, 3]:
        cbar.mappable.set_clim(0, 0.5)

    for w in range(int(min(T_list))+1, int(max(T_list))):
        plt.axhline(w, linestyle='--')
    for w in range(int(min(S_list))+1, int(max(S_list))):
        plt.axvline(w, linestyle='--')

    # plt.figtext(0.23, 0.8, 'b', fontsize=12, weight='bold')

    plt.xlabel('S')
    plt.ylabel('T')
    # plt.title(f'{short[config["update_str_type"]]} {names2[i]}, k={config["av_degree"]}')
    plt.title(r'$\alpha$')

    plt.tight_layout()
    # plt.savefig(f'{short[config["update_str_type"]]}_{names[i]}_k{config["av_degree"]}_new.png')
    plt.show()
    plt.close()





