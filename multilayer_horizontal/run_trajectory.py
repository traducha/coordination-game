# -*- coding: utf-8 -*-
from pprint import pprint
from datetime import datetime
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_trajectory, read_trajectory, plot_trajectory_multi, log
from main import run_trajectory
import constants as const
from config import config_values


@run_with_time
def main(configuration):
    convergence_t, time_steps, active_nums, left_nums = run_trajectory(multi=True, **configuration)

    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Convergance time = {convergence_t}')
    final_value = 'Final values'
    for i in range(len(active_nums[-1])):
        final_value += f', layer {i} active edges = {active_nums[-1][i]} and cooperators = {left_nums[-1][i]}'
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} ' + final_value)

    save_trajectory(configuration, time_steps, active_nums, left_nums, convergence_t)
    res, conf = read_trajectory(configuration)
    plot_trajectory_multi(res, conf)


if __name__ == '__main__':
    update_rule = const.REPLICATOR
    for shared_nodes_ratio in [0, 0.5, 1]:
        multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=shared_nodes_ratio)
        conf = dict(config_values, multilayer=multi_conf, update_str_type=update_rule)
        log.info(f'Configuration: ')
        pprint(conf)
        main(conf)
