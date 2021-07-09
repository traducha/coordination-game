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

trans_S = []
T_list = np.linspace(-2, 1, 40)

coop_mean = []
coop_std = []
active_mean = []
active_std = []
time_mean = []
time_std = []
for T in T_list:
    config = dict(config_values, update_str_type=const.BEST_RESPONSE, T=T, av_degree=8)
    res, _ = read_stationary_generic(config, directory='best_res')
    res = sorted(res, key=lambda x: x['conf']['S'])

    _trans_S = -3
    updated = False
    for _r in res:
        alpha = np.mean(_r['left_fraction'])
        if alpha > 0.5 and not updated:
            _trans_S = _r['conf']['S']
            updated = True
    trans_S.append(_trans_S)

    coop_mean.append([np.mean(x['left_fraction']) for x in res])
    coop_std.append([np.std(x['left_fraction']) for x in res])
    active_mean.append([np.mean(x['active_density']) for x in res])
    active_std.append([np.std(x['active_density']) for x in res])
    time_mean.append([np.mean(x['convergence_time']) for x in res])
    time_std.append([np.std(x['convergence_time']) for x in res])

print(trans_S)

fig = plt.figure(figsize=(4, 3.5))
im = plt.imshow(coop_mean, cmap='jet', origin='lower', extent=[-3, 0, -2, 1], interpolation='none')
cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
cbar.ax.tick_params()
cbar.set_clim(0, 1)

plt.axvline(-2, linestyle='--')
plt.axvline(-1, linestyle='--')
plt.axhline(-1, linestyle='--')
plt.axhline(0, linestyle='--')

plt.xlabel('S')
plt.ylabel('T')
plt.title('UI cooperators')
# plt.savefig('UI_coop_k32.pdf')
plt.show()





