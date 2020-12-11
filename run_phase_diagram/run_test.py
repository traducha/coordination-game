# -*- coding: utf-8 -*-
from pprint import pprint
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, read_stationary_generic, plot_over_two_params
from main import get_stationary_state_sample
import constants as const
from config import config_values


@run_with_time
def main(configuration):
    res = []
    for T in np.linspace(-2, 1, 4):
        for S in np.linspace(-3, 0, 4):
            conf = dict(configuration, T=T, S=S)
            conv_time, left_nums, active_nums = get_stationary_state_sample(**conf)
            res.append({
                'conf': conf,
                'convergence_time': conv_time,
                'active_density': active_nums,
                'left_fraction': left_nums,
            })

    save_stationary_generic(configuration, res)
    res, conf = read_stationary_generic(configuration)
    # plot_over_two_params(res, 'S', 'T', conf)


if __name__ == '__main__':
    for update_type in [const.REPLICATOR]:
        config = dict(config_values, update_str_type=update_type, sample_size=2, number_of_loops=1000, loop_length=1000, b=2)
        print('Configuration: ')
        pprint(config)
        main(config)

# 48 min with 1000 loops (1loop 1000)
# 6 min with 10 loops (1loop 1000)
# 46 min with 100 loops (1loop 10000)
# 80 min with 10 loops (1loop 100000)

# 23 min with 1000 loops (1loop 1000) old algorithm (b=2 to distinguish)

# check the time with old algorithm and parallel in nurreduna (and synch algorithm?)

