
import pygame
from pygame.rect import Rect

from .config import config


class Screen:
    """Manages a display window."""
    def __init__(self):
        self.rect = Rect(0, 0, config.RESOLUTION[0], config.RESOLUTION[1])
        self.display = pygame.display.set_mode(tuple(config.RESOLUTION))
        self.display = pygame.display.get_surface()
        self.background = pygame.image.load(config.BACKGROUND_IMAGE).convert()

    def blit(self, bitmap, destrect, sourcerect):
        """Draws something from the given bitmap on the screen."""
        self.display.blit(bitmap, destrect, sourcerect)

    def clear(self):
        """Wipes out everything."""
        if self.background:
            self.blit(self.background, self.rect, self.rect)
