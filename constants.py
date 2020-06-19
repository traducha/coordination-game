# -*- coding: utf-8 -*-

# colors for plotting
GOLD = '#D4AF37'
GREEN = '#5aa27c'

# strategies
LEFT = 'left'  # the left (or upper) one, risk-dominant in the complex matrix
RIGHT = 'right'  # the right (or lower) one, payoff-dominant in the complex matrix

# update rules
UNCOND_IMITATION = 'unconditional_imitation'
REPLICATOR = 'replicator_dynamics'
BEST_RESPONSE = 'best_response'

# payoff matrix
COMPLEX = 'complex'  # complex one with -b
SIMPLE = 'simple'  # simple one with 1,1 and 0,0

# loop type
ASYNC = 'not_synchronous'  # one node at a time
SYNC = 'synchronous'

