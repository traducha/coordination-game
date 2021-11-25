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


def linear(x_list, a, b):
    return [a*x+b for x in x_list]


def plot():
    fig = plt.figure(figsize=(4.2, 4))

    for line in [2, 1, -1, -2, -3, -4]:
        plt.axhline(line, linestyle='--', linewidth=0.7)
        plt.axvline(line, linestyle='--', linewidth=0.7)
    plt.axhline(0, linestyle='-', color='black', linewidth=0.8)
    plt.axvline(0, linestyle='-', color='black', linewidth=0.8)

    # x = np.linspace(-4.5, 0, 30)
    # plt.plot(x, linear(x, 1, 1), color=const.REDISH)

    plt.text(-3.9, -0.9, "horizontal", fontsize=10, color=const.VIOLET)
    x = np.linspace(-4, 0, 30)
    plt.plot(x, linear(x, 0, -1), color=const.VIOLET, alpha=1)

    plt.text(-1.95, 0.2, "vertical", fontsize=10, rotation=-90, color=const.VIOLET)
    plt.plot([-2, -2], [-3, 1], color=const.VIOLET, alpha=1)

    plt.text(-3.7, 0.2, "diagonal", fontsize=10, rotation=-45, color=const.VIOLET)
    x = np.linspace(-4, 0, 30)
    plt.plot(x, linear(x, -1, -3), color=const.VIOLET, alpha=1)

    plt.text(-0.8, 0.2, "stag hunt", fontsize=10, rotation=-45, color=const.VIOLET)
    x = np.linspace(-1, 0, 30)
    plt.plot(x, linear(x, -1, 0), color=const.VIOLET, alpha=1)

    plt.fill_between([-4.5, 0], -4.5, [-3.5, 1], color=const.GREEN, alpha=0.35)
    plt.fill_between([-4.5, 0], 1, [-3.5, 1], color=const.BLUE, alpha=0.35)

    plt.xlim([-4.5, 0.5])
    plt.xticks(np.arange(-4, 1, step=1))
    plt.ylim([-3.5, 1.5])
    plt.yticks(np.arange(-3, 2, step=1))

    for i in range(1, 10):
        plt.plot((i/-10.0, i/-10.0), (0, 1), color='black', alpha=0.06)
        plt.plot((-1, 0), (i/10.0, i/10.0), color='black', alpha=0.06)

    plt.text(-4.1, -3.38, "L0: A is risk-dominant", fontsize=10, rotation=45, color=const.GREEN_DARK)
    plt.text(-4.4, -3.1, "L1: B is risk-dominant", fontsize=10, rotation=45, color=const.BLUE)
    # plt.text(-3.4, -3.4, "general coordination game area", fontsize=10, color=const.GREEN_DARKER)

    for S1 in np.linspace(-2, 0, 11)[1:]:
        S2 = -4.0 - S1
        plt.scatter(S1, -1, marker="|", color=const.VIOLET)
        plt.scatter(S2, -1, marker="|", color=const.VIOLET)

    for T1 in np.linspace(-1, -3, 11)[1:]:
        T1 = round(T1, 2)
        T2 = round(-2.0 - T1, 2)
        S1 = round(-T1 - 3.0, 2)
        S2 = round(-T2 - 3.0, 2)
        plt.scatter(S1, T1, marker="x", color=const.VIOLET, s=18)
        plt.scatter(S2, T2, marker="x", color=const.VIOLET, s=18)

    for T1 in np.linspace(0, 0.45, 10):
        T1 = round(T1, 2)
        S1 = -T1
        T2 = 1-T1
        S2 = -T2
        plt.scatter(S1, T1, marker="x", color=const.VIOLET, s=15)
        plt.scatter(S2, T2, marker="x", color=const.VIOLET, s=15)

    for T1 in np.linspace(-1, -3, 11)[1:]:
        T1 = round(T1, 2)
        T2 = round(-2.0 - T1, 2)
        plt.scatter(-2, T1, marker="_", color=const.VIOLET)
        plt.scatter(-2, T2, marker="_", color=const.VIOLET)


    plt.xlabel(r"$S$", fontsize=11)
    plt.ylabel(r"$T$", fontsize=11)
    plt.tight_layout()

    plt.savefig("plots/diagram.png")
    plt.show()
    plt.close()


if __name__ == "__main__":
    plot()
