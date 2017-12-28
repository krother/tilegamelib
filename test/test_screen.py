
import pygame

from tilegamelib.screen import Screen
from util import next_frame


class TestScreen:
    """
    Tests Screen wrapper.
    """
    def test_clear(self):
        """Screen can be cleared."""
        screen = Screen()
        screen.clear()

    def test_blit(self, tile_bitmap):
        """quadratic image is shown, then cleared."""
        screen = Screen()
        dest = pygame.Rect(60, 60, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        screen.blit(tile_bitmap, dest, source)
        next_frame()
        screen.clear()
