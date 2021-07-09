# -*- coding: utf-8 -*-
import multiprocessing as mp
from pprint import pprint
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, read_stationary_generic, plot_over_two_params
from main import get_stationary_state_sample
import constants as const
from config import config_values


def error_callback(error):
    raise error


@run_with_time
def main(configuration, proc=48, directory=None):
    res = []
    async_res = []

    def callback(_conf):
        def append_result(arg):
            conv_time, left_nums, active_nums = arg
            res.append({
                'conf': _conf,
                'convergence_time': conv_time,
                'active_density': active_nums,
                'left_fraction': left_nums,
            })
        return append_result

    with mp.Pool(processes=proc) as pool:

        for S in np.linspace(-1, 1, 40):
            conf = dict(configuration, S=S)
            async_res.append(pool.apply_async(get_stationary_state_sample, kwds={**conf}, callback=callback(conf),
                             error_callback=error_callback))

        for a_res in async_res:
            a_res.wait()

    save_stationary_generic(configuration, res, directory=directory)
    res, conf = read_stationary_generic(configuration, directory=directory)
    # plot_over_two_params(res, 'S', 'T', conf)


if __name__ == '__main__':
    T = float(sys.argv[1])
    processes = int(sys.argv[2])
    dir_name = str(sys.argv[3])
    print(T, processes, dir_name)

    for update_type in [const.BEST_RESPONSE]:
        config = dict(config_values, update_str_type=update_type, T=T)
        print('Configuration: ')
        pprint(config)
        main(config, proc=processes, directory=dir_name)
