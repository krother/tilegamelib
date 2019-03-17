
from arcade.key import MOTION_UP, MOTION_DOWN, MOTION_LEFT, MOTION_RIGHT
from .vector import Vector

PLAYER_MOVES = {
        MOTION_UP: Vector(0, -1),
        MOTION_DOWN: Vector(0, 1),
        MOTION_LEFT: Vector(-1, 0),
        MOTION_RIGHT: Vector(1, 0),
}
