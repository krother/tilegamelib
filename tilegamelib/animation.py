
class AnimatedTile:
    """
    Loop through a sequence of tiles.
    """
    def __init__(self, tiles, tile_factory, frame, pos, delay=5, loop=False):
        self.tiles = list(tiles)
        self.tile_factory = tile_factory
        self.frame = frame
        self.pos = pos * 32
        self.tile = None
        self.delay_max = delay
        self.delay = 0
        self.loop = loop
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
                if self.loop:
                    self.tiles.append(tile)
            else:
                self.delay -= 1

    def draw(self, frame=None, destrect=None):
        self.tile.draw(frame or self.frame, destrect or self.pos)
