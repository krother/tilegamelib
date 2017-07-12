
from pygame import Rect


class Tile:
    """A tile is a quadratic piece of graphic that can be written
    anywhere on the screen.
    """
    def __init__(self, name, index, size, image):
        """
        Creates a new tile:
            name  - string identifier
            index - location in rows/columns on the image
            size  - x/y size of the tile
            image - bitmap where the tile is copied from.
        """
        self.name = name
        self.size = size
        self.image = image
        self.box = Rect(index.x * size.x, index.y * size.y, size.x, size.y)

    def draw(self, frame, pos):
        """Draws the tile on the given position into the bitmap."""
        destrect = Rect(pos.x, pos.y, self.size.x, self.size.y)
        frame.blit(self.image, destrect, self.box)

    def __repr__(self):
        return "[Tile '{}' ({}x{})]".format(self.name, self.size.x, self.size.y)
