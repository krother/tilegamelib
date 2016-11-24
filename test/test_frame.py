
from tilegamelib.screen import Screen
from tilegamelib.frame import Frame
from tilegamelib.vector import Vector
from pygame import Rect, image
from test_data import RESOLUTION, BACKGROUND_IMAGE, TILE, DEMIBOLD_BIG
from util import next_frame, graphictest
from unittest import TestCase, main

CYAN = (0, 255, 255)


class FrameTests(TestCase):

    def setUp(self):
        self.screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        self.frame = Frame(self.screen, Rect(50, 50, 100, 100))

    @graphictest
    def test_blit(self):
        """image drawn into frame, then cleared."""
        bitmap = image.load(TILE).convert()
        dest = Rect(32, 16, 32, 32)
        source = Rect(0, 0, 32, 32)
        self.frame.blit(bitmap, dest, source)
        next_frame()
        self.frame.clear()

    @graphictest
    def test_text(self):
        """Text drawn into frame, then cleared."""
        self.frame.print_text('Hello Frame', Vector(50,50), \
            DEMIBOLD_BIG, CYAN )
        next_frame()
        self.frame.clear()

    def test_get_dest_rect(self):
        """Adds rectangle values to frame position."""
        rect = Rect(10, 20, 20, 31)
        dest = self.frame.get_dest_rect(rect)
        self.assertEqual(dest, Rect(60, 70, 20, 31))

     
if __name__ == "__main__":
    main()
