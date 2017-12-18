
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
        pixel_pos = index * size
        self.box = Rect(pixel_pos[0], pixel_pos[1], size[0], size[1])

    def draw(self, frame, pos):
        """Draws the tile on the given position into the bitmap."""
        destrect = Rect(pos[0], pos[1], self.size[0], self.size[1])
        frame.blit(self.image, destrect, self.box)

    def __repr__(self):
        return "[Tile '{}' ({}x{})]".format(self.name, self.size[0], self.size[1])
