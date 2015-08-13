
import numpy as np

class PacLevel:

    def __init__(self, level, pac_pos, ghost_positions):
        self.level = level
        self.pac_start_pos = pac_pos
        self.ghost_start_positions = ghost_positions
        self.dots_total = 0
        self.dots_left = level.level.count("a")

LEVELS = [
    PacLevel("""####################
#.aaaaaaaaaaaaaaaae#
#a#a#####aa#####a#a#
#a#aaaaaaccaaaaaa#a#
#a#a#####aa#####a#a#
#aaaaaaaaaaaaaaaaaa#
#a##a###afaa###a##a#
#a##a###afaa###a##a#
#aaaaaaaaaaaaaaaaaa#
#a#a###aa##aa##a##a#
#eaaaaaaaaaaaaaaaae#
####################""", np.array([1,1]), \
             [np.array([18,10])]
    ),
    PacLevel("""####################
#.aaaaaaaaaaaaaaaae#
#a#a#####aa#####a#a#
#a#aaaaaaccaaaaaa#a#
#a#a#####aa#####a#a#
#aaaaaaaaaaaaaaaaaa#
#a##a###afaa###a##a#
#a##a###afaa###a##a#
#aaaaaaaaaaaaaaaaaa#
#a#a###aa##aa##a##a#
#eaaaaaaaaaaaaaaaae#
####################""", np.array([1,1]), \
             [np.array([18,1]),np.array([18,10])]
    ),

    PacLevel("""####################
#.aaaaaaaaaaaaaaaae#
#a#a#####aa#####a#a#
#a#aaaaaaccaaaaaa#a#
#a#a#####aa#####a#a#
#aaaaaaaaaaaaaaaaaa#
#a##a###afaa###a##a#
#a##a###afaa###a##a#
#aaaaaaaaaaaaaaaaaa#
#a#a###aa##aa##a##a#
#eaaaaaaaaaaaaaaaae#
####################""", np.array([1,1]), \
             [np.array([18,1]),np.array([18,10]),np.array([1,10])]
    ),

    ]        

