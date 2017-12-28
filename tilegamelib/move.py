
from .vector import RIGHT, ZERO_VECTOR, Vector


class Move:
    """
    Moves a tile over a certain amount of steps in one direction.
    """
    def __init__(self, frame, tile, start_vector=ZERO_VECTOR, direction=RIGHT,
            steps=0, when_finished=None):
        self.frame = frame
        self.tile = tile
        self.start_vector = Vector(start_vector)
        self.current_vector = Vector(start_vector)
        self.steps = steps
        self.direction = direction
        self.finished = False
        self.callback = when_finished

    def move(self):
        if self.steps > 0:
            self.current_vector += self.direction
            self.steps -= 1
        if self.steps <= 0:
            self.finished = True
            if self.callback:
                self.callback()

    def draw(self):
        self.tile.draw(self.frame, self.current_vector)
