# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "network_size": 1000,
    "average_degree": 8,
    "payoff_matrix": const.COMPLEX,
    "b": 1,  # necessary for the complex payoff matrix
    "update_type": const.UNCOND_IMITATION,
    "loop_length": 100,
    "loop_type": const.ASYNC
}
