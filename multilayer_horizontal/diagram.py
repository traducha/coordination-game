# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os
import constants as const


COLORS = [const.GREEN, const.YELLOW]
COLORS2 = [const.GREEN_DARK, const.ORANGE]
COLORS3 = [const.REDISH, const.BLUE]

PARETO = '#fde725'
NON_PARETO = '#443983'


def linear(x_list, a, b):
    return [a*x+b for x in x_list]


def plot():
    fig = plt.figure(figsize=(4.2, 4))

    plt.plot([-2.8, -2.8], [-0.2, 2], linestyle='-', color='#333333', linewidth=0.7)
    plt.plot([-2.8, 2], [-0.2, -0.2], linestyle='-', color='#333333', linewidth=0.7)
    plt.plot([-1.2, -1.2], [-1.8, 2], linestyle='-', color='#333333', linewidth=0.7)
    plt.plot([-1.2, 2], [-1.8, -1.8], linestyle='-', color='#333333', linewidth=0.7)

    for line in [2, 1, 0, -1, -2, -3, -4]:
        plt.axhline(line, linestyle=':', linewidth=0.7, color='gray')
        plt.axvline(line, linestyle=':', linewidth=0.7, color='gray')


    # x = np.linspace(-4.5, 0, 30)
    # plt.plot(x, linear(x, 1, 1), color=const.REDISH)

    # plt.text(-3.95, -0.9, "horizontal", fontsize=10, color='#333333')
    # x = np.linspace(-4, 0, 30)
    # plt.plot(x, linear(x, 0, -1), color=const.VIOLET, alpha=1, linewidth=0.7)
    #
    # plt.text(-1.94, 0.8, "vertical", fontsize=10, rotation=-90, color='#333333')
    # plt.plot([-2, -2], [-3, 1], color=const.VIOLET, alpha=1, linewidth=0.7)

    plt.text(-3.95, 0.5, "diagonal", fontsize=10, rotation=-45, color='#333333')
    x = np.linspace(-4, 0, 30)
    plt.plot(x, linear(x, -1, -3), color='black', alpha=1, linewidth=0.7)

    plt.text(-1.05, 0.63, "stag hunt", fontsize=10, rotation=-45, color='#333333')
    x = np.linspace(-1, 0, 30)
    plt.plot(x, linear(x, -1, 0), color=const.VIOLET, alpha=1, linewidth=0.7)

    plt.fill_between([-4.5, 0], -4.5, [-3.5, 1], color=PARETO, alpha=0.55)
    plt.fill_between([-4.5, 0], 1, [-3.5, 1], color=NON_PARETO, alpha=0.45)

    plt.xlim([-4.5, 0.5])
    plt.xticks(np.arange(-4, 1, step=1))
    plt.ylim([-3.5, 1.5])
    plt.yticks(np.arange(-3, 2, step=1))

    plt.scatter(-2.8, -0.2, marker="o", color='#7ad151', s=60)  # , facecolor='none')
    plt.scatter(-1.2, -1.8, marker="o", color='#7ad151', s=60)  # , facecolor='none')

    # for i in range(1, 10):
    #     plt.plot((i/-10.0, i/-10.0), (0, 1), color='black', alpha=0.06)
    #     plt.plot((-1, 0), (i/10.0, i/10.0), color='black', alpha=0.06)

    plt.text(-3.9, -1.88, "A is risk-dominant", fontsize=10, rotation=45, color='black')
    plt.text(-4.2, -1.55, "B is risk-dominant", fontsize=10, rotation=45, color='black')

    # for S1 in np.linspace(-2, 0, 11)[1:]:
    #     S2 = -4.0 - S1
    #     plt.scatter(S1, -1, marker="o", color=const.VIOLET, s=18)
    #     plt.scatter(S2, -1, marker="o", color=const.VIOLET, s=18)

    for T1 in np.linspace(-1, -3, 11)[1:]:
        T1 = round(T1, 2)
        T2 = round(-2.0 - T1, 2)
        S1 = round(-T1 - 3.0, 2)
        S2 = round(-T2 - 3.0, 2)
        plt.scatter(S1, T1, marker="o", color='black', s=18)
        plt.scatter(S2, T2, marker="o", color='black', s=18)

    for T1 in np.linspace(0, 0.45, 10):
        T1 = round(T1, 2)
        S1 = -T1
        T2 = 1-T1
        S2 = -T2
        plt.scatter(S1, T1, marker="o", color='black', s=6)
        plt.scatter(S2, T2, marker="o", color='black', s=6)

    # for T1 in np.linspace(-1, -3, 11)[1:]:
    #     T1 = round(T1, 2)
    #     T2 = round(-2.0 - T1, 2)
    #     plt.scatter(-2, T1, marker="o", color=const.VIOLET, s=18)
    #     plt.scatter(-2, T2, marker="o", color=const.VIOLET, s=18)

    plt.text(-1.15, -1.68, r"$(S^{I}, T^{I})$", fontsize=10, color='black')
    plt.text(-2.75, -0.08, r"$(S^{II}, T^{II})$", fontsize=10, color='black')

    plt.text(-2.125, 1.15, r"$\Delta S$", fontsize=10, color='black')
    plt.text(0.15, -1.1, r"$\Delta T$", fontsize=10, color='black')

    plt.plot([0.3, 0.3], [-0.25, -0.85], linestyle='-', color='#333333', linewidth=0.7)
    plt.plot([0.3, 0.3], [-1.15, -1.75], linestyle='-', color='#333333', linewidth=0.7)
    plt.scatter(0.3, -0.28, marker="^", color='#333333', s=20)
    plt.scatter(0.3, -1.72, marker="v", color='#333333', s=20)
    plt.scatter(0.3, -1.15, marker="_", color='#333333', s=20)
    plt.scatter(0.3, -0.85, marker="_", color='#333333', s=20)

    plt.plot([-2.725, -2.2], [1.23, 1.23], linestyle='-', color='#333333', linewidth=0.7)
    plt.plot([-1.8, -1.275], [1.23, 1.23], linestyle='-', color='#333333', linewidth=0.7)
    plt.scatter(-2.725, 1.23, marker="<", color='#333333', s=20)
    plt.scatter(-1.275, 1.23, marker=">", color='#333333', s=20)
    plt.scatter(-2.2, 1.23, marker="|", color='#333333', s=20)
    plt.scatter(-1.8, 1.23, marker="|", color='#333333', s=20)


    plt.xlabel(r"$S$", fontsize=11)
    plt.ylabel(r"$T$", fontsize=11)
    plt.tight_layout()

    plt.savefig("diagram.pdf")
    plt.show()
    plt.close()


if __name__ == "__main__":
    plot()
