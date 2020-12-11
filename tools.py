# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import numpy as np
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
    R = conf['R']
    P = conf['P']
    S = conf['S']
    T = conf['T']
    up = conf['update_str_type']
    loo = conf['loop_type']
    le = conf['loop_length']
    num = conf['number_of_loops']
    che = int(conf['check_frozen'])
    sam = conf['sample_size']
    return f'n{n}_k{k}_b{b}_R{R}_P{P}_T{T}_S{S}_pay{pay}_up{up}_loo{loo}_len{le}_num{num}_che{che}_sam{sam}'


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


def save_stationary_over_param(config, results, parameter, directory='results'):
    os.makedirs(directory, exist_ok=True)

    to_write = {'config': config,
                'results': results,
                'parameter': parameter}

    f_name = f'{directory}/stationary_over_param_{config_into_suffix(config)}.json'
    with open(f_name, 'w') as out_file:
        json.dump(to_write, out_file, indent=4)


def save_stationary_generic(config, results, directory='results'):
    os.makedirs(directory, exist_ok=True)

    to_write = {'config': config,
                'results': results}

    f_name = f'{directory}/stationary_generic_{config_into_suffix(config)}.json'
    with open(f_name, 'w') as out_file:
        json.dump(to_write, out_file, indent=4)


def read_stationary_over_param(config, directory='results'):
    f_name = f'{directory}/stationary_over_param_{config_into_suffix(config)}.json'
    with open(f_name, 'r') as in_file:
        from_file = json.load(in_file)
    return from_file['results'], from_file['parameter'], from_file['config']


def read_stationary_generic(config, directory='results'):
    f_name = f'{directory}/stationary_generic_{config_into_suffix(config)}.json'
    with open(f_name, 'r') as in_file:
        from_file = json.load(in_file)
    return from_file['results'], from_file['config']


#################################
#           plotting            #
#################################


def plot_trajectory(res, config, directory='plots'):
    os.makedirs(directory, exist_ok=True)

    plt.figure(figsize=(4, 3))
    plt.plot(res['time_steps'], res['left_fraction'], color=const.REDISH, label=r'$\alpha$')
    plt.plot(res['time_steps'], res['active_density'], color=const.GREEN_BRIGHT, label=r'$\rho$')
    plt.axvline(res['convergence_time'], color='black', linestyle='--')
    plt.ylim([0, 1])
    plt.legend()
    plt.xlabel('MC times steps')
    plt.title(f"Trajectory for N={config['num_nodes']}, k={config['av_degree']}"
              + (f", b={config['b']}" if config['payoff_type'] == const.COMPLEX else ''))
    plt.tight_layout()

    plot_name = f'{directory}/trajectory_{config_into_suffix(config)}.pdf'
    plt.savefig(plot_name)
    plt.close()


def plot_over_param(res, param, config, directory='plots'):
    os.makedirs(directory, exist_ok=True)
    fig = plt.figure(figsize=(4, 3))

    averages = []
    deviations = []
    for key, value in res.items():
        averages.append((float(key), np.mean(value['convergence_time']), np.mean(value['active_density']),
                         np.mean(value['left_fraction'])))
        deviations.append((float(key), np.std(value['convergence_time']), np.std(value['active_density']),
                           np.std(value['left_fraction'])))

        for i in range(config['sample_size']):
            # plt.plot(float(key), value['convergence_time'][i], color=const.BLUE, marker='o', markerfacecolor='none')
            # plt.plot(float(key), value['active_density'][i], color=const.GREEN_BRIGHT, marker='o',
            #          markerfacecolor='none', alpha=0.2)
            plt.plot(float(key), value['left_fraction'][i], color=const.REDISH, marker='o', markerfacecolor='none',
                     alpha=0.2)

    averages.sort(key=lambda element: element[0])
    deviations.sort(key=lambda element: element[0])
    averages = list(zip(*averages))
    deviations = list(zip(*deviations))

    plt.plot(averages[0], averages[3], color=const.REDISH, label=r'$\alpha$')
    plt.plot(averages[0], averages[2], color=const.GREEN_BRIGHT, label=r'$\rho$')

    # plt.errorbar(averages[0], averages[3], yerr=deviations[3], markerfacecolor='none', color=const.REDISH)
    # plt.errorbar(averages[0], averages[2], yerr=deviations[2], markerfacecolor='none', color=const.GREEN_BRIGHT)

    plt.legend()
    plt.xlabel(param)
    plt.title(f"Frozen state for N={config['num_nodes']}"
              + (f", k={config['av_degree']}" if config['av_degree'] is not None else '')
              + (f", b={config['b']}" if config['b'] is not None else ''))

    left, bottom, width, height = [0.58, 0.3, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(averages[0], averages[1], color=const.BLUE, label=r'$\tau$')
    # ax2.errorbar(averages[0], averages[1], yerr=deviations[1], markerfacecolor='none', color=const.BLUE)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    plt.tight_layout()
    plot_name = f'{directory}/stationary_over_{param}_{config_into_suffix(config)}.pdf'
    plt.savefig(plot_name)
    plt.close()


def plot_over_two_params(res, param_x, param_y, config, directory='plots'):  # TODO edit plotting
    os.makedirs(directory, exist_ok=True)
    fig = plt.figure(figsize=(4, 3))

    averages = []
    deviations = []
    for key, value in res.items():
        averages.append((float(key), np.mean(value['convergence_time']), np.mean(value['active_density']),
                         np.mean(value['left_fraction'])))
        deviations.append((float(key), np.std(value['convergence_time']), np.std(value['active_density']),
                           np.std(value['left_fraction'])))

        for i in range(config['sample_size']):
            # plt.plot(float(key), value['convergence_time'][i], color=const.BLUE, marker='o', markerfacecolor='none')
            # plt.plot(float(key), value['active_density'][i], color=const.GREEN_BRIGHT, marker='o',
            #          markerfacecolor='none', alpha=0.2)
            plt.plot(float(key), value['left_fraction'][i], color=const.REDISH, marker='o', markerfacecolor='none',
                     alpha=0.2)

    averages.sort(key=lambda element: element[0])
    deviations.sort(key=lambda element: element[0])
    averages = list(zip(*averages))
    deviations = list(zip(*deviations))

    plt.plot(averages[0], averages[3], color=const.REDISH, label=r'$\alpha$')
    plt.plot(averages[0], averages[2], color=const.GREEN_BRIGHT, label=r'$\rho$')

    # plt.errorbar(averages[0], averages[3], yerr=deviations[3], markerfacecolor='none', color=const.REDISH)
    # plt.errorbar(averages[0], averages[2], yerr=deviations[2], markerfacecolor='none', color=const.GREEN_BRIGHT)

    plt.legend()
    plt.xlabel(param_x)
    plt.title(f"Frozen state for N={config['num_nodes']}"
              + (f", k={config['av_degree']}" if config['av_degree'] is not None else '')
              + (f", b={config['b']}" if config['b'] is not None else ''))

    left, bottom, width, height = [0.58, 0.3, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(averages[0], averages[1], color=const.BLUE, label=r'$\tau$')
    # ax2.errorbar(averages[0], averages[1], yerr=deviations[1], markerfacecolor='none', color=const.BLUE)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    plt.tight_layout()
    plot_name = f'{directory}/stationary_over_{param}_{config_into_suffix(config)}.pdf'
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
        "R": 1,  # parameters for the general payoff matrix
        "P": 0,
        "S": 0.5,
        "T": -1,
        "update_str_type": const.REPLICATOR,
        "loop_type": const.ASYNC,
        "loop_length": 100,
        "number_of_loops": 1000000,
        "check_frozen": False,
        "sample_size": 50,
    }
    print(config_into_suffix(config_values))



