# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import json
import time
import os

import constants as const


def run_with_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()

        minutes = (end_time - start_time) / 60.0
        if minutes <= 60:
            print(f'Function <{func.__name__}> finished in {round(minutes, 0)} min')
        else:
            print(f'Function <{func.__name__}> finished in {round(minutes / 60, 1)} h')
    return inner


def config_into_suffix(conf):
    n = conf['num_nodes']
    k = conf['av_degree']
    pay = conf['payoff_type']
    b = conf['b']
    up = conf['update_str_type']
    loo = conf['loop_type']
    le = conf['loop_length']
    num = conf['number_of_loops']
    che = int(conf['check_frozen'])
    return f'n{n}_k{k}_b{b}_pay{pay}_up{up}_loo{loo}_len{le}_num{num}_che{che}'


#########################################
#           reading, writing            #
#########################################


def save_trajectory(config, time_steps, active_nums, left_nums, convergence_time, directory='results'):
    os.makedirs(directory, exist_ok=True)
    results = {
        'convergence_time': convergence_time,
        'time_steps': time_steps,
        'active_density': active_nums,
        'left_fraction': left_nums,
    }

    to_write = {'config': config,
                'results': results}

    f_name = f'{directory}/trajectory_{config_into_suffix(config)}.json'
    with open(f_name, 'w') as out_file:
        json.dump(to_write, out_file, indent=4)


def read_trajectory(config, directory='results'):
    f_name = f'{directory}/trajectory_{config_into_suffix(config)}.json'
    with open(f_name, 'r') as in_file:
        from_file = json.load(in_file)
    return from_file['results'], from_file['config']


#################################
#           plotting            #
#################################


def plot_trajectory(res, config, directory='plots'):
    os.makedirs(directory, exist_ok=True)

    plt.figure(figsize=(4, 3))
    plt.plot(res['time_steps'], res['left_fraction'], color=const.REDISH, label=r'$\alpha$ fraction')
    plt.plot(res['time_steps'], res['active_density'], color=const.GREEN_BRIGHT, label=r'$\rho$')
    plt.axvline(res['convergence_time'], color='black', linestyle='--')
    plt.legend()
    plt.xlabel('MC times steps')
    plt.title(f"Trajectory for N={config['num_nodes']}, k={config['av_degree']}"
              + f", b={config['b']}" if config['payoff_type'] == const.COMPLEX else '')
    plt.tight_layout()

    plot_name = f'{directory}/trajectory_{config_into_suffix(config)}.pdf'
    plt.savefig(plot_name)
    plt.close()


##############################
#           tests            #
##############################


if __name__ == '__main__':
    config_values = {
        "num_nodes": 1000,
        "av_degree": 8,
        "payoff_type": const.COMPLEX,
        "b": 1,  # necessary for the complex payoff matrix
        "update_str_type": const.REPLICATOR,
        "loop_type": const.ASYNC,
        "loop_length": 100,
        "number_of_loops": 1000000,
        "check_frozen": False,
    }
    print(config_into_suffix(config_values))



