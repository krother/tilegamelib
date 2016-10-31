#! /usr/bin/python

from tilegamelib import Frame, TileFactory
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from tilegamelib.sounds import play_effect, MusicPlayer, CLOSE_TO_END
from tilegamelib.game import Game
from tilegamelib.basic_boxes import DictBox
from tilegamelib.draw_timer import draw_timer
from frutris_level import FrutrisLevel
from dropping_blocks import Diamond, FruitPair
from multiplets import MultipletCounter
from pygame import Rect
import pygame
from random import randint
import time


DROP_DELAY = 50
ONE_PLAYER_START_DELAY = 7
TWO_PLAYER_DELAY = 10
LEVEL_COUNTER_INIT = 5000
LEVEL_DROP_COUNTER_DECREASE = 5
LEVEL = open('data/emptybox.map').read()
MAX_FRUIT = 5


class FrutrisBox:
    def __init__(self, frame, tile_factory, level):
        self.frame = frame
        self.tile_factory = tile_factory
        self.level = FrutrisLevel(frame, tile_factory, level)
        self.moving_blocks = None
        self.insert_random_fruit_pair()
        self.drop_delay = DROP_DELAY
        self.drop_counter = self.drop_delay
        self._queued_command = None
        self._fast_drop = 0
        self.diamonds_queued = 0
        self.update_mode = self.update_drop
        self.counter = MultipletCounter()
        self.game_over = False

    def insert_diamond(self, column):
        self.moving_blocks = Diamond(self.frame, self.tile_factory, self.level, 2)

    def insert_fruit_pair(self, first, second):
        self.moving_blocks = FruitPair(self.frame, self.tile_factory, self.level, (first, second))

    def insert_random_fruit_pair(self):
        blocks = 'abcefg'
        first = blocks[randint(0, MAX_FRUIT)]
        second = blocks[randint(0, MAX_FRUIT)]
        self.insert_fruit_pair(first, second)

    @property
    def fast_drop(self):
        return self._fast_drop >= 2

    def insert_new_block(self):
        """Inserts a random block at top center."""
        if self.diamonds_queued > 0:
            self.insert_diamond(randint(1, 6))
            self.diamonds_queued -= 1
            play_effect('diamond_drop')
            self.update_mode = self.update_autodrop
        else:
            self.insert_random_fruit_pair()
            self.update_mode = self.update_drop

    def remove_blocks(self):
        """Find vanishing blocks."""
        multiplets = self.level.find_multiplets()
        if len(multiplets) > 0:
            self.counter.count(multiplets)
            self.moving_blocks = self.level.get_explosions(multiplets)
            play_effect('fruit_drop_after_vanish')
            self.update_mode = self.update_remove
        else:
            self.all_moves_finished()

    def all_moves_finished(self):
        """All explosions and drops finished."""
        # play_effect(self.counter.get_category())
        self.counter.reset()
        if self.level.box_overflow():
            self.game_over = True
        else:
            self.insert_new_block()

    def update_autodrop(self):
        """Drops fruit without user interaction."""
        self.moving_blocks = self.level.get_dropped_bricks()
        if self.moving_blocks.finished:
            self.remove_blocks()

    def update_drop(self):
        """Dropping fruit after some time."""
        self.handle_command()
        if self.moving_blocks.finished:
            self.drop_counter -= 1
            if self.drop_counter == 0 or self.fast_drop:
                self.drop_counter = self.drop_delay
                self.moving_blocks.drop()
                if self.moving_blocks.finished:
                    self.remove_blocks()
                    self._fast_drop = 0

    def update_remove(self):
        """Explosions or dropping finished."""
        self.moving_blocks = self.level.get_dropped_bricks()
        if self.moving_blocks:
            # play_effect('fruit_drop_after_vanish')
            self.update_mode = self.update_autodrop
        else:
            self.all_moves_finished()

    def draw(self):
        if self.moving_blocks.finished:
            self.update_mode()
        if not self.moving_blocks.finished:
            self.moving_blocks.move()
        self.level.draw()
        self.moving_blocks.draw()

    def store_command(self, direction):
        self._queued_command = direction

    def handle_command(self):
        if self._queued_command:
            direction = self._queued_command
            self._queued_command = None
            if direction == DOWN:
                self.moving_blocks.drop()
                self._fast_drop += 1
            else:
                self._fast_drop = 0
            if direction in (LEFT, RIGHT):
                self.moving_blocks.shift(direction)
            elif direction == UP:
                self.moving_blocks.rotate()


class FrutrisGame:

    def __init__(self, screen):
        self.level_counter = 1
        play_effect('frutris')
        self.screen = screen
        screen.clear()
        self.frame = Frame(self.screen, Rect(10, 10, 640, 512))
        self.tile_factory = TileFactory('data/tiles.conf')
        self.events = None
        self.frutris_box = FrutrisBox(self.frame, self.tile_factory, LEVEL)
        # frame = Frame(self.screen, Rect(660, 220, 200, 200))
        self.data = {
            'score': 0,
            'level': 1,
        }
        self.status_box = self.create_status_box()

        # Music
        self.music_counter = 50 # periodically check for expiring track
        self.current_music = ('a', 1)
        self.music = MusicPlayer()
        self.music.play_music('/home/krother/projects/frutris/frutris/music/a1.ogg')


    def choose_next_music(self):
        MUSIC = '/home/krother/projects/frutris/frutris/music/{}{}.ogg'
        LETTERS = 'aaaabbbbcccccccc'
        letter, number = self.current_music
        number = 3 - number
        stack_size = self.frutris_box.level.get_stack_size()
        letter = LETTERS[stack_size]
        #if len(self.players) >= 1:
        #    stack_size = self.players[0].get_stack_size()
        self.current_music = (letter, number)
        next_track = MUSIC.format(letter, number)
        print('NEXT TRACK: ', next_track)
        return next_track

    def update_music(self):
        self.music_counter -= 1
        if self.music_counter == 0:
            self.music_counter = 50
            if self.music.check_music_status() == CLOSE_TO_END:
                next_track = self.choose_next_music()
                self.music.next_music(next_track)

    @property
    def score(self):
        return self.data['score']

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 200))
        return DictBox(frame, self.data)

    def draw(self):
        self.data['score'] += self.frutris_box.counter.pull_score()
        self.frutris_box.draw()
        self.status_box.draw()
        if self.frutris_box.game_over:
            self.events.exit_signalled()
        self.update_music()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.frutris_box.store_command))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/frutris.conf', FrutrisGame)
    game.run()
