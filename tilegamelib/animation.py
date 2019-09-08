
class AnimatedTile:
    """
    Loop through a sequence of tiles.
    """
    def __init__(self, tile_sequence, tiles, delay=5, loop=False):
        self.tile_sequence = tile_sequence
        self.tiles = tiles
        self._tile_gen = self._next_tile_gen(tile_sequence, loop)
        self.delay_max = delay
        self.delay = 0
        self.finished = False
        self.update()

    def _next_tile_gen(self, sequence, loop):
        """Generates tiles"""
        i = 0
        while i < len(sequence):
            yield self.tiles[sequence[i]]
            i += 1
            if loop and i >= len(sequence):
                i = 0
        self.finished = True

    def update(self):
        if not self.finished:
            if self.delay == 0:
                self.tile = next(self._tile_gen)
                self.delay = self.delay_max
            else:
                self.delay -= 1

    def draw(self, *args):
        self.update()
        self.tile.draw(*args)
