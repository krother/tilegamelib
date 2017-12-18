
import numpy as np
from pygame import Rect

from .config import config


class Frame:
    """
    Rectangular piece of the screen.
    Manages relative positions of objects.
    """
    def __init__(self, screen, rect, font=config.DEMIBOLD_BIG):
        """
        rect - position and size of the frame in pixels (x, y, x, y)
        """
        self.screen = screen
        self.rect = rect
        self.font = font

    @property
    def position(self):
        return np.array([self.rect[0], self.rect[1]])

    @property
    def size(self):
        return np.array([self.rect.width, self.rect.height])

    def get_dest_rect(self, rect):
        """Calculate absolute position of the given rect."""
        pos = self.position + np.array([rect[0], rect[1]])
        return Rect(pos[0], pos[1], rect.width, rect.height)

    def blit(self, bitmap, rect, sourcerect):
        """Copies graphics on the screen (quick)."""
        destrect = self.get_dest_rect(rect)
        self.screen.blit(bitmap, destrect, sourcerect)

    def print_text(self, text, pos, font=config.DEMIBOLD_BIG, color=config.BLUE):
        """Writes text on the screen."""
        font = font or self.font
        color = color or self.color
        rendered = font.render(text, 1, color)
        pos = self.pos + pos
        self.screen.display.blit(rendered, tuple(pos))

    def clear(self):
        """Clears the area in the frame."""
        self.screen.blit(self.screen.background, self.rect,
            Rect(0, 0, self.rect.width, self.rect.height))

    def __repr__(self):
        return "[Frame '%s']" % (str(self.rect))
