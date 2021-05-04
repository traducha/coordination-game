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

    for line in [2, 1, -1, -2, -3]:
        plt.axhline(line, linestyle='--', linewidth=0.7)
        plt.axvline(line, linestyle='--', linewidth=0.7)
    plt.axhline(0, linestyle='-', color='black', linewidth=0.8)
    plt.axvline(0, linestyle='-', color='black', linewidth=0.8)

    x = np.linspace(-3.5, 2.5, 30)
    plt.plot(x, linear(x, 1, 0), linestyle='--', linewidth=0.6)
    x = np.linspace(-3.5, 0, 30)
    plt.plot(x, linear(x, 1, 1), color=const.REDISH)
    x = np.linspace(-3.5, -1, 30)
    plt.plot(x, linear(x, 0, -1), color=const.VIOLET)
    plt.scatter(-2, -1, marker="o")

    plt.fill_between([-1000000000, 0], -3.5, [-3.5, 1], color=const.GREEN, alpha=0.35)

    plt.xlim([-3.5, 2.5])
    plt.ylim([-3.5, 2.5])

    plt.text(-0.95, 1.3, "prisoner's\ndilemma", fontsize=7.5)
    plt.text(0.05, 1.3, "chicken\ngame", fontsize=7.5)
    plt.text(-0.95, 0.5, "stag hunt", fontsize=7.5)
    plt.text(0.05, 0.3, "harmony\ngame", fontsize=7.5)
    plt.text(1.05, 1.6, "leader\ngame", fontsize=7.5)
    plt.text(-0.8, -0.95, "    battle\nof sexes", fontsize=7.5)
    plt.text(1.1, -1.4, "deadlock", fontsize=7.5)

    plt.text(-3.1, -2.38, "strategy C", fontsize=8, rotation=45, color=const.REDISH)
    plt.text(-3.4, -2.1, "strategy D", fontsize=8, rotation=45, color=const.REDISH)
    plt.text(-3.4, -0.9, "complex\ncoordination\ngame", fontsize=8, color=const.VIOLET)
    plt.text(-2.4, -2.8, "generic coordination\ngame area", fontsize=8, color=const.GREEN_DARK)

    plt.figtext(0.02, 0.02, "R=1\nP=0", fontsize=9)

    plt.xlabel("S")
    plt.ylabel("T")

    plt.savefig("diagram.pdf")
    plt.show()
    plt.close()


if __name__ == "__main__":
    plot()
