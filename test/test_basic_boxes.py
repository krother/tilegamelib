#!/usr/bin/env python

import pygame

from tilegamelib.basic_boxes import DictBox, ImageBox, TextBox


class TestBasicBoxes:

    def test_text_box(self, frame):
        """Display hello world text box."""
        tb = TextBox(frame, "Hello World")
        tb.draw()
        pygame.display.update()

    def test_image_box(self, frame):
        """Display image with colorful boxes."""
        ib = ImageBox(frame, "test_data/test_tile.png")
        ib.draw()
        pygame.display.update()

    def test_dict_box(self, frame):
        """Display data from a dictionary."""
        dict_data = {
            'Level': '20',
            'Name': 'Zeratul',
            'HP': '400'
        }
        db = DictBox(frame, dict_data)
        db.draw()
        pygame.display.update()

    # @showdoc
    # def test_life_display(self):
    #     """Display image with decreasing lives."""
    #     factory = TEST_GAME_CONTEXT.tile_factory
    #     lifes = LifeDisplay(frame, factory, 10, 'g')
    #     for i in range(10):
    #         lifes.draw()
    #         pygame.display.update()
    #         lifes.lose_one()
    #         time.sleep(SHORT_DELAY)
