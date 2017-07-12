
import pygame

from test.conftest import TILE
from tilegamelib.screen import Screen
from util import graphictest, next_frame


class ScreenTests:
    """
    Tests Screen wrapper.
    """
    @graphictest
    def test_clear(self):
        """Screen can be cleared."""
        screen = Screen()
        screen.clear()

    @graphictest
    def test_blit(self):
        """quadratic image is shown, then cleared."""
        screen = Screen()
        bitmap = pygame.image.load(TILE).convert()
        dest = pygame.Rect(60, 60, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        screen.blit(bitmap, dest, source)
        next_frame()
        screen.clear()
