# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np

import constants as const
from config import config_values
from tools import read_stationary_generic


T_list = np.linspace(0, 2, 40)

coop_mean = []
coop_std = []
active_mean = []
active_std = []
time_mean = []
time_std = []
for T in T_list:
    config = dict(config_values, update_str_type=const.UNCOND_IMITATION, T=T, av_degree=512)
    res, _ = read_stationary_generic(config, directory='imitation_res512')
    res = sorted(res, key=lambda x: x['conf']['S'])

    coop_mean.append([np.mean(x['left_fraction']) for x in res])
    coop_std.append([np.std(x['left_fraction']) for x in res])
    active_mean.append([np.mean(x['active_density']) for x in res])
    active_std.append([np.std(x['active_density']) for x in res])
    time_mean.append([np.mean(x['convergence_time']) for x in res])
    time_std.append([np.std(x['convergence_time']) for x in res])

fig = plt.figure(figsize=(4, 3.5))
im = plt.imshow(active_mean, cmap='jet', origin='lower', extent=[-1, 1, 0, 2], interpolation='none')
cbar = fig.colorbar(im, fraction=0.0467, pad=0.04)
cbar.ax.tick_params()
cbar.set_clim(0, 1)

plt.axvline(0, linestyle='--')
plt.axhline(1, linestyle='--')


plt.xlabel('S')
plt.ylabel('T')
plt.title('UI active links')
# plt.savefig('roca_UI_active512.pdf')
plt.show()





