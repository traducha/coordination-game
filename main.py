# -*- coding: utf-8 -*-
import csv
import glob
import igraph as ig
import logging as log
from matplotlib import pyplot as plt
import numpy as np
import os
import time


# network initialization - random regular lattice
# allow node overlap - nodes are just indexed, for every node keep the list of groups of layers that are connected
# e.g [(1,2), (3,4), 5] - layers 1 and 2 are connected and 3 and 4, but 5 is separate from all
# allow any edge overlap (at first for 2 layers) - start with identical nets and rewire a certain fraction of links
# allow an arbitrary number of layers in simulations


# game played pay-off matrix
# cooperation game with b><1
# 1,1   0,-b
# -b,0  2,2

# update dynamics and evalution of the strategy
# player looks at all neighbors in one of the layers (random one, always one, both at once?)
# and chooses the best strategy, i.e. the highest payoff last round (if the pay-off is bigger than his)
# synchronous update (?) everyone plays with all the neigs on all layers and then update strategies and then reset gains
# or one by one?




