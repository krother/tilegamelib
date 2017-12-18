"""
Direction vectors for moves, positions etc.
"""
import numpy as np

ZERO_VECTOR = np.array([0, 0])
UP = np.array([0, -1])
DOWN = np.array([0, 1])
LEFT = np.array([-1, 0])
RIGHT = np.array([1, 0])
UPLEFT = np.array([-1, -1])
DOWNLEFT = np.array([-1, 1])
UPRIGHT = np.array([1, -1])
DOWNRIGHT = np.array([1, 1])

for vec in [ZERO_VECTOR, UP, DOWN, LEFT, RIGHT,
            UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT]:
    vec.flags.writeable = False