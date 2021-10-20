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


T_list = np.linspace(-5, 1, 40)

coop_mean = []
coop_std = []
active_mean = []
active_std = []
time_mean = []
time_std = []
for T in T_list:
    config = dict(config_values, update_str_type=const.REPLICATOR, T=T)
    res, _ = read_stationary_generic(config, directory='repl_long_res')
    res = sorted(res, key=lambda x: x['conf']['S'])

    coop_mean.append([np.mean(x['left_fraction']) for x in res])
    coop_std.append([np.std(x['left_fraction']) for x in res])
    active_mean.append([np.mean(x['active_density']) for x in res])
    active_std.append([np.std(x['active_density']) for x in res])
    time_mean.append([np.mean(x['convergence_time']) for x in res])
    time_std.append([np.std(x['convergence_time']) for x in res])

fig = plt.figure(figsize=(4, 3.5))
im = plt.imshow(coop_mean, cmap='jet', origin='lower', extent=[-6, 0, -5, 1], interpolation='none')
cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
cbar.ax.tick_params()
cbar.set_clim(0, 1)

plt.axvline(-2, linestyle='--')
plt.axvline(-1, linestyle='--')
plt.axvline(-3, linestyle='--')
plt.axvline(-4, linestyle='--')
plt.axvline(-5, linestyle='--')
plt.axhline(-1, linestyle='--')
plt.axhline(0, linestyle='--')
plt.axhline(-2, linestyle='--')
plt.axhline(-3, linestyle='--')
plt.axhline(-4, linestyle='--')

plt.xlabel('S')
plt.ylabel('T')
plt.title('RD cooperators')
# plt.savefig('RD_coop.pdf')
plt.show()





