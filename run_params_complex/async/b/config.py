# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": 8,
    "payoff_type": const.COMPLEX,
    "b": None,  # necessary for the complex payoff matrix
    "update_str_type": None,
    "loop_type": const.ASYNC,
    "loop_length": 1000,
    "number_of_loops": 1000000,
    "check_frozen": True,
    "sample_size": 50,
}
