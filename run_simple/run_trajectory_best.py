# -*- coding: utf-8 -*-
from pprint import pprint
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
import constants as const
from tools import run_with_time, save_trajectory, log, plot_trajectory, read_trajectory
from main import run_trajectory
from config import config_values


@run_with_time
def main(configuration):
    while True:
        conv_time, time_steps, active_nums, left_nums = run_trajectory(multi=False, **configuration)
        # if 0.7 <= left_nums[-1] <= 0.9:
        break

    save_trajectory(configuration, time_steps, active_nums, left_nums, conv_time, directory='trajectories')
    res, _ = read_trajectory(configuration, directory='trajectories')

    # plot_trajectory(res, configuration, directory='trajectories')


if __name__ == '__main__':
    for k in [1, 2, 4, 5, 6, 7, 9, 10, 15]:
        conf = dict(config_values, av_degree=k, num_nodes=1000, update_str_type=const.BEST_RESPONSE,
                    loop_length=10, number_of_loops=50000)
        main(conf)
        print(k)
