#!/usr/bin/env python

from tilegamelib.frame import Frame
from tilegamelib.basic_boxes import TextBox, ImageBox, DictBox
from util import showdoc, TEST_GAME_CONTEXT, SHORT_DELAY
from unittest import TestCase, main
from pygame import Rect
import pygame
import time


class BasicBoxTests(TestCase):

    def setUp(self):
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100,100, 260,160))

    @showdoc
    def test_text_box(self):
        """Display hello world text box."""
        tb = TextBox(self.frame, "Hello World")
        tb.draw()
        pygame.display.update()

    @showdoc
    def test_image_box(self):
        """Display image with colorful boxes."""
        ib = ImageBox(self.frame, "test_data/tiles.xpm")
        ib.draw()
        pygame.display.update()

    @showdoc
    def test_dict_box(self):
        """Display data from a dictionary."""
        dict_data = {
            'Level':'20',
            'Name':'Zeratul',
            'HP':'400'
            }
        db = DictBox(self.frame, dict_data)
        db.draw()
        pygame.display.update()

    # @showdoc
    # def test_life_display(self):
    #     """Display image with decreasing lives."""
    #     factory = TEST_GAME_CONTEXT.tile_factory
    #     lifes = LifeDisplay(self.frame, factory, 10, 'g')
    #     for i in range(10):
    #         lifes.draw()
    #         pygame.display.update()
    #         lifes.lose_one()
    #         time.sleep(SHORT_DELAY)


if __name__ == "__main__":
    main()
