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


T_list = np.linspace(0, 2, 40)
S_list = np.linspace(-1, 1, 40)

coop_mean = []
coop_std = []
active_mean = []
active_std = []
time_mean = []
time_std = []
names = ['coop_mean', 'coop_std', 'active_mean', 'active_std', 'time_mean', 'time_std']
names2 = ['cooperators', 'cooperators std', 'active links', 'active links std', 'therm. time', 'therm. time std']

for T in T_list:
    coop_mean_s = []
    coop_std_s = []
    active_mean_s = []
    active_std_s = []
    time_mean_s = []
    time_std_s = []

    for S in S_list:
        try:
            config = dict(config_values, update_str_type=const.REPLICATOR, T=T, S=S, av_degree=999)
            res, _ = read_stationary_generic(config, directory='repl_res_new999')
            coop_mean_s.append(np.mean(res['left_fraction']))
            coop_std_s.append(np.std(res['left_fraction']))
            active_mean_s.append(np.mean(res['active_density']))
            active_std_s.append(np.std(res['active_density']))
            time_mean_s.append(np.mean(res['convergence_time']))
            time_std_s.append(np.std(res['convergence_time']))
        except Exception:
            print('BAD', T, S)
            coop_mean_s.append(0.5)
            coop_std_s.append(0)
            active_mean_s.append(0.45)
            active_std_s.append(0)
            time_mean_s.append(0)
            time_std_s.append(0)

    coop_mean.append(coop_mean_s)
    coop_std.append(coop_std_s)
    active_mean.append(active_mean_s)
    active_std.append(active_std_s)
    time_mean.append(time_mean_s)
    time_std.append(time_std_s)

for i, param in enumerate([coop_mean, coop_std, active_mean, active_std, time_mean, time_std]):
    fig = plt.figure(figsize=(4, 3.5))
    im = plt.imshow(param, cmap='jet', origin='lower', extent=[-1, 1, 0, 2], interpolation='none')
    cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
    cbar.ax.tick_params()
    if i in [0, 1]:
        cbar.mappable.set_clim(0, 1)
    elif i in [2, 3]:
        cbar.mappable.set_clim(0, 0.5)

    plt.axvline(0, linestyle='--')
    plt.axhline(1, linestyle='--')

    plt.xlabel('S')
    plt.ylabel('T')
    plt.title(f'UI {names2[i]}')
    # plt.savefig(f'roca_UI_{names[i]}_k{config["av_degree"]}_new.pdf')
    plt.show()
    plt.close()





