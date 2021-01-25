# -*- coding: utf-8 -*-
from pprint import pprint
from datetime import datetime
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_trajectory, read_trajectory, plot_trajectory
from main_new import run_trajectory
import constants as const
from config import config_values


@run_with_time
def main(configuration):
    convergence_t, time_steps, active_nums, left_nums = run_trajectory(multi=True, **configuration)
    save_trajectory(configuration, time_steps, active_nums, left_nums, convergence_t)
    res, conf = read_trajectory(configuration)
    plot_trajectory(res, conf)


if __name__ == '__main__':
    for k in [4, 8, 16, 32]:
        for b in [0.5, 1, 1.5]:
            for update_type in [const.UNCOND_IMITATION, const.REPLICATOR, const.BEST_RESPONSE]:
                conf = dict(config_values, av_degree=k, b=b, update_str_type=update_type)
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Configuration: ')
                pprint(conf)
                main(conf)
