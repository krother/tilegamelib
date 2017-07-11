#!/usr/bin/env python

import pygame
from pygame import Rect

from tilegamelib.basic_boxes import DictBox, ImageBox, TextBox
from tilegamelib.frame import Frame
from util import TEST_GAME_CONTEXT, showdoc


class BasicBoxTests:

    def setUp(self):
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 160))

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
            'Level': '20',
            'Name': 'Zeratul',
            'HP': '400'
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
