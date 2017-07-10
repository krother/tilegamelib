
from unittest import main
from unittest import TestCase

import pygame

from data import BACKGROUND_IMAGE
from data import RESOLUTION
from data import TILE
from tilegamelib.screen import Screen
from util import graphictest
from util import next_frame


class ScreenTests(TestCase):
    """
    Tests Screen wrapper.
    """
    def test_attribute(self):
        """Screen has a resolution attribute."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        self.assertEqual(screen.resolution, RESOLUTION)

    @graphictest
    def test_clear(self):
        """Screen can be cleared."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        screen.clear()

    @graphictest
    def test_blit(self):
        """quadratic image is shown, then cleared."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        bitmap = pygame.image.load(TILE).convert()
        dest = pygame.Rect(60, 60, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        screen.blit(bitmap, dest, source)
        next_frame()
        screen.clear()


if __name__ == "__main__":
    main()
