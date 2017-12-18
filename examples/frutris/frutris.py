#! /usr/bin/python

from random import randint

from pygame import Rect

from tilegamelib import Frame
from tilegamelib import Game
from tilegamelib.basic_boxes import DictBox
from tilegamelib.config import config
from tilegamelib.sounds import CLOSE_TO_END
from tilegamelib.sounds import MusicPlayer
from tilegamelib.sounds import play_effect
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP

from examples.frutris.dropping_blocks import Diamond
from examples.frutris.dropping_blocks import FruitPair
from examples.frutris.frutris_level import FrutrisLevel
from examples.frutris.multiplets import MultipletCounter

START_DROP_DELAY = 50
MIN_DROP_DELAY = 5
DROP_DELAY_DECREASE_PER_LEVEL = 5
ONE_PLAYER_START_DELAY = 7
TWO_PLAYER_DELAY = 10
LEVEL_COUNTER_INIT = 5000
LEVEL = open(config.DATA_PATH + '/emptybox.map').read()
MAX_FRUIT = 5


class FrutrisBox:
    def __init__(self, game, level):
        self.game = game
        self.level = FrutrisLevel(game, level)
        self.moving_blocks = None
        self.insert_random_fruit_pair()
        self.drop_delay = START_DROP_DELAY
        self.drop_counter = self.drop_delay
        self._queued_command = None
        self._fast_drop = 0
        self.diamonds_queued = 0
        self.update_mode = self.update_drop
        self.counter = MultipletCounter()
        self.game_over = False

    def make_blocks_drop_faster(self):
        """Called when level increases"""
        if self.drop_delay > MIN_DROP_DELAY:
            self.drop_delay -= DROP_DELAY_DECREASE_PER_LEVEL

    def insert_diamond(self, column):
        self.moving_blocks = Diamond(self.game, self.level, 2)

    def insert_fruit_pair(self, first, second):
        self.moving_blocks = FruitPair(self.game, self.level, (first, second))

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
        if self._queued_command is not None:
            direction = self._queued_command
            self._queued_command = None
            if direction is DOWN:
                self.moving_blocks.drop()
                self._fast_drop += 1
            else:
                self._fast_drop = 0
            if direction is LEFT or direction is RIGHT:
                self.moving_blocks.shift(direction)
            elif direction is UP:
                self.moving_blocks.rotate()


class FrutrisGame:

    def __init__(self):
        config.FRAME = Rect(250, 10, 640, 512)
        self.game = Game()
        self.level_counter = LEVEL_COUNTER_INIT
        play_effect('frutris')
        self.frutris_box = FrutrisBox(self.game, LEVEL)
        # frame = Frame(self.screen, Rect(660, 220, 200, 200))
        self.data = {
            'score': 0,
            'level': 1,
        }
        self.status_box = self.create_status_box()

        # Music
        self.music_counter = 50  # periodically check for expiring track
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

    def update_level(self):
        self.level_counter -= 1
        if self.level_counter == 0:
            self.data['level'] += 1
            self.level_counter = LEVEL_COUNTER_INIT
            self.frutris_box.make_blocks_drop_faster()

    @property
    def score(self):
        return self.data['score']

    def create_status_box(self):
        frame = Frame(self.game.screen, Rect(660, 20, 200, 200))
        return DictBox(frame, self.data)

    def draw(self):
        self.data['score'] += self.frutris_box.counter.pull_score()
        self.frutris_box.draw()
        self.status_box.draw()
        if self.frutris_box.game_over:
            self.game.exit()
        self.update_level()
        self.update_music()

    def run(self):
        self.game.event_loop(figure_moves=self.frutris_box.store_command, draw_func=self.draw)


class OnePlayerGame(FrutrisGame):

    def bla(self):
        play_effect('menu_select_game_1')
        play_effect('game_over')
        play_effect('highscores_normal')


class TwoPlayerGame(FrutrisGame):

    def bla(self):
        self.status_box = StatusBox(self, array([300,100]), array([200,500]))
        self.status_box['player1_score'] = 0
        self.status_box['player2_score'] = 0
        self.players.append(FrutrisBox(self, (50, 0)))
        self.players.append(FrutrisBox(self, (500, 0)))
        self.delay = TWO_PLAYER_DELAY
        play_effect('menu_select_game_2')

    def message(self, sender, msg_type, *params):
        if msg_type == 'diamond_to_opponent'\
           and self.mode == 'two player game':
            opp = self.players[0]==sender and self.players[1] or self.players[0]
            opp.diamonds_queued += params[0]
        elif msg_type == 'add_points':
            field = 'player2_score'
            if sender == self.players[0]:
                field = 'player1_score'
            self.status_box[field] += params[0] * self.status_box.get('level',1)

    def win(self):
        play_effect('winner_first')
        play_effect('winner_second')


class MainGame:

    def one_player_game(self):
        self.game_class = OnePlayerGame()
        self.game_class.run()

    def two_player_game(self):
        game = TwoPlayerGame(self.screen)
        game.run()


if __name__ == '__main__':
    game = MainGame()
    game.one_player_game()
