
class AnimatedTile:
    """
    Loop through a sequence of tiles.
    """
    def __init__(self, tiles, tile_factory, frame, pos, delay=5):
        self.tiles = list(tiles)
        self.tile_factory = tile_factory
        self.frame = frame
        self.pos = pos * 32
        self.tile = None
        self.delay_max = delay
        self.delay = 0
        self.move()

    @property
    def finished(self):
        if self.tiles or self.delay > 0:
            return False
        return True

    def move(self):
        if not self.finished:
            if self.delay == 0:
                tile = self.tiles.pop(0)
                self.tile = self.tile_factory.get(tile)
                self.delay = self.delay_max
            else:
                self.delay -= 1
            self.draw()

    def draw(self):
        self.tile.draw(self.frame, self.pos)
