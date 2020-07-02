# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": 80,
    "payoff_type": const.COMPLEX,
    "b": None,  # necessary for the complex payoff matrix
    "update_str_type": const.UNCOND_IMITATION,
    "loop_type": const.ASYNC,
    "loop_length": 100,
    "number_of_loops": 1000000,
    "check_frozen": True,
    "sample_size": 2,
}
