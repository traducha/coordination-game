# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os

import constants as const

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)

rules_dicts = {
    const.UNCOND_IMITATION: 'imit',
    const.REPLICATOR: 'repl',
    const.BEST_RESPONSE: 'best',
}


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
    if conf.get('multilayer') is None:
        return f'n{n}_k{k}_b{b}_R{R}_P{P}_T{T}_S{S}_pay{pay}_up{up}_loo{loo}_len{le}_num{num}_che{che}_sam{sam}'
    else:
        num_lay = conf['multilayer']['num_layers']
        rewire = conf['multilayer']['to_rewire']
        shared_n = conf['multilayer']['shared_nodes_ratio']
        return (f'n{n}_k{k}_b{b}_R{R}_P{P}_T{T}_S{S}_pay{pay}_up{up}_loo{loo}_len{le}_num{num}_che{che}_sam{sam}'
                f'_lay{num_lay}_rew{rewire}_shar{shared_n}')


def payoff_matrix(_type, b=None, R=None, P=None, T=None, S=None):
    # pay_off[mine][co-player]
    if _type == const.GENERIC:
        if R is None or P is None or T is None or S is None:
            raise ValueError('The parameters R, P, T, and S must be provided for the generic payoff matrix.')
        return {const.LEFT: {const.LEFT: R, const.RIGHT: S}, const.RIGHT: {const.LEFT: T, const.RIGHT: P}}, \
               max([R, P, T, S]) - min([R, P, T, S])
    elif _type == const.COMPLEX:
        if b is None:
            raise ValueError('The parameter b must be provided for the complex payoff matrix.')
        return {const.LEFT: {const.LEFT: 1, const.RIGHT: 0}, const.RIGHT: {const.LEFT: -b, const.RIGHT: 2}}, \
               max([-b, 2]) - min([-b, 0])
    elif _type == const.SIMPLE:
        return {const.LEFT: {const.LEFT: 1, const.RIGHT: 0}, const.RIGHT: {const.LEFT: 0, const.RIGHT: 1}}, 1
    else:
        raise ValueError(f'Unrecognized matrix type: {_type}')


def get_max_min_payoff(_type, b=None, R=None, P=None, T=None, S=None):
    if _type == const.GENERIC:
        if R is None or P is None or T is None or S is None:
            raise ValueError('The parameters R, P, T, and S must be provided for the generic payoff matrix.')
        return max([R, P, T, S]), min([R, P, T, S])
    elif _type == const.COMPLEX:
        if b is None:
            raise ValueError('The parameter b must be provided for the complex payoff matrix.')
        return max([-b, 2]), min([-b, 0])
    elif _type == const.SIMPLE:
        return 1, 0
    else:
        raise ValueError(f'Unrecognized matrix type: {_type}')


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
    plt.plot(res['time_steps'], res['left_fraction'], color=const.GREEN_BRIGHT, label=r'$\alpha$')
    # plt.plot(res['time_steps'], res['active_density'], color=const.REDISH, label=r'$\rho$')
    plt.axvline(res['convergence_time'], color='black', linestyle='--')
    plt.ylim([0, 1])
    plt.legend()
    plt.xlabel('MC times steps')
    plt.title(f"Trajectory for N={config['num_nodes']}, k={config['av_degree']}"
              + (f", b={config['b']}" if config['payoff_type'] == const.COMPLEX else ''))
    plt.tight_layout()

    plot_name = f'{directory}/trajectory_{config_into_suffix(config)}.png'
    plt.savefig(plot_name)
    plt.close()


def plot_trajectory_multi(res, config, directory='plots'):
    os.makedirs(directory, exist_ok=True)

    plt.figure(figsize=(4, 3))
    for i, value in enumerate(zip(*res['left_fraction'])):
        plt.plot(res['time_steps'], value, label=f'layer {i} coop')
    for i, value in enumerate(zip(*res['active_density'])):
        plt.plot(res['time_steps'], value, label=f'layer {i} active', alpha=0.5)
    plt.axvline(res['convergence_time'], color='black', linestyle='--')
    plt.ylim([0, 1])
    plt.legend(fontsize=8)
    plt.xlabel('MC times steps')
    plt.title(f"Trajectory for N={config['num_nodes']}, k={config['av_degree']}")
    description = (f"edge overlap = {1-config['multilayer']['to_rewire']}, " +
                   f"node overlap = {config['multilayer']['shared_nodes_ratio']}\n")
    for i, lc in enumerate(config['multilayer']['layers_config']):
        if lc['b'] is not None:
            description += f"layer {i} has b={lc['b']}"
        else:
            description += f"layer {i} has R={lc['R']}, P={lc['P']}, T={lc['T']}, S={lc['S']}\n"
    plt.figtext(0.05, -0.02, description, fontsize=8)
    plt.gcf().subplots_adjust(top=0.92, bottom=0.3, right=0.98, left=0.09)
    # plt.tight_layout()

    plot_name = f'{directory}/trajectory_{config_into_suffix(config)}.png'
    plt.savefig(plot_name)
    plt.close()


def plot_over_param_multi(res, param, config, directory='plots'):
    return


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



