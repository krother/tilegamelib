#! /usr/bin/python

from tilegamelib import Screen, Frame, TileFactory, TiledMap, Vector, Sprite
from tilegamelib import EventGenerator, EventListener
from tilegamelib.map_move import MapMove
from tilegamelib.move_group import MoveGroup
from tilegamelib.animation import AnimatedTile
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from tilegamelib.sounds import play_effect, MusicPlayer, CLOSE_TO_END
from tilegamelib.game import Game
from tilegamelib.basic_boxes import DictBox
from pygame import Rect, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE
import pygame
from random import randint
import time


DROP_DELAY = 70
ONE_PLAYER_START_DELAY = 10
TWO_PLAYER_DELAY = 10
LEVEL_COUNTER_INIT = 5000
LEVEL_DROP_COUNTER_DECREASE = 5
LEVEL = open('data/emptybox.map').read()


EXPLOSION = ['b.explo_1','b.explo_2','b.explo_3','b.explo_4','b.explo_5','b.explo_6', 'b.empty']


class FruitMultiplets:
    """Sets of fruits that vanish"""
    def __init__(self):
        self.multiplets = []

    def add_multiplet(self, multiplet):
        if len(multiplet) >= 4:
            self.multiplets.append(multiplet)

    def get_positions(self):
        result = set()
        for multi in self.multiplets:
            for pos in multi:
                result.add(pos)
        return result

    def get_category(self, previous=0):
        """
        Sophisticated method by Borris M. for 
        determining the kind of fruit vanish reaction
          previous - number of previous rounds of vanishing
        """
        n_vanish = previous + 1
        if n_vanish <= 3:
            if len(self.multiplets) == 1 and len(self.multiplets[0]) <= 6:
                return 'vanish%i' % len(self.multiplets[0])
            if len(self.multiplets) == 2: 
                return 'vanish%i_double' % (n_vanish)
            elif len(self.multiplets) == 3: 
                return 'vanish%i_triple' % (n_vanish)
        return 'vanish_mega'

    def __len__(self):
        return len(self.multiplets)


class FrutrisLevel:

    def __init__(self, tmap, level):
        self.tmap = tmap
        self.tmap.set_map(level)
        self.moves = None
    
    def insert(self, pos, fruit):
        self.tmap.set_tile(pos, fruit)
        self.tmap.cache_map()

    def is_pos_in_box(self, pos):
        if (0 <= pos.x < self.tmap.size.x\
            and 0 <= pos.y < self.tmap.size.y):
            return True

    def are_positions_empty(self, positions):
        for pos in positions:
            if self.tmap.at(pos) != '.':
                return False
        return True

    def trace_multiplets(self, pos, trace, char):
        """Recursively looks for quartets of identical bricks."""
        if not self.is_pos_in_box(pos): return 
        if self.tmap.at(pos) != char: return
        if pos in trace: return
        trace.add(pos)
        self.trace_multiplets(pos + LEFT, trace, char)
        self.trace_multiplets(pos + RIGHT, trace, char)
        self.trace_multiplets(pos + DOWN, trace, char)
        
    def find_multiplets(self):
        """Returns a list of multiplet positions"""
        multiplets = FruitMultiplets()
        for x in range(1, self.tmap.size.x - 1):
            for y in range(self.tmap.size.y):
                pos = Vector(x, y)
                if self.tmap.at(pos) == '.': continue
                if self.tmap.at(pos) == '#': continue
                found = set()
                char = self.tmap.at(pos)
                self.trace_multiplets(pos, found, char)
                multiplets.add_multiplet(found)
        return multiplets

    def drop_bricks(self):
        self.moves = MoveGroup()
        for x in range(self.tmap.size.x):
            pos = Vector(x, self.tmap.size.y - 1)
            while pos.y > 0:
                pos_above = pos + UP
                if self.tmap.at(pos) == '.' and self.tmap.at(pos_above) != '.':
                    self.moves.add(MapMove(self.tmap, pos_above, DOWN, speed=4))
                pos = pos_above

    def remove_multiplets(self, multiplets):
        self.moves = MoveGroup()
        for pos in multiplets.get_positions():
            self.tmap.set_tile(pos, '.')
            self.moves.add(AnimatedTile(EXPLOSION, self.tmap.tile_factory, self.tmap.frame, pos)) 
        self.tmap.cache_map()

    def remove_fruit(self):
        multiplets = self.find_multiplets()
        self.remove_multiplets(multiplets)
        
    def box_overflow(self):
        if self.get_stack_size() == self.tmap.size.y - 1:
            return True
 
    def get_stack_size(self):
        """Returns height of the fruit stack."""
        y = 0
        while y < self.tmap.size.y:
            for x in range(1, self.tmap.size.x - 1):
                char = self.tmap.at(Vector(x, y))
                if char != '.':
                    return self.tmap.size.y -y -1
            y += 1
        return 0

    def move(self):
        if self.moves and not self.moves.finished:
            self.moves.move()
        else:
            self.tmap.cache_map()
            self.drop_bricks()

    @property
    def finished(self):
        if self.moves:
            return self.moves.finished    
        return True

    def draw(self):
        self.tmap.draw()


class MovingBlocks:

    def __init__(self, level, sprites, chars):
        self.level = level
        self.sprites = sprites
        self.chars = chars

    def drop(self):
        newsprites = []
        newchars = []
        for sprite, char in zip(self.sprites, self.chars):
            newpos = sprite.pos + DOWN
            if self.level.tmap.at(newpos) == '.':
                sprite.add_move(DOWN)
                newsprites.append(sprite)
                newchars.append(char)
            else:
                self.level.insert(sprite.pos, char)
        self.sprites = newsprites

    def move(self):
        for s in self.sprites:
            s.move()

    def draw(self):
        for s in self.sprites:
            s.draw()

    @property
    def finished(self):
        for s in self.sprites:
            if not s.finished:
                return False
        return True


class Diamond(MovingBlocks):

    def __init__(self, frame, tile_factory, level, column):
        sprites = [Sprite(frame, tile_factory.get('d'), Vector(column + 1, 0), speed=4)]
        MovingBlocks.__init__(self, level, sprites, 'd')


class FruitPair(MovingBlocks):

    def __init__(self, frame, tile_factory, level, chars=('a', 'b')):
        sprites = [
            Sprite(frame, tile_factory.get(chars[0]), Vector(3, 0), speed=4),
            Sprite(frame, tile_factory.get(chars[1]), Vector(4, 0), speed=4),
            ]
        MovingBlocks.__init__(self, level, sprites, chars)

    def rotate(self):
        if len(self.sprites) != 2: return
        first, second = self.sprites
        if first.pos.x == second.pos.x:
            newpos = [first.pos + UP, second.pos + RIGHT]
            if self.level.are_positions_empty(newpos):
                first.add_move(UP)
                second.add_move(RIGHT)
        else:
            newpos = [first.pos, second.pos + DOWN + LEFT]
            if self.level.are_positions_empty(newpos):
                second.add_move(DOWN + LEFT)
                self.sprites = second, first
                self.chars = self.chars[1], self.chars[0]


    def get_shifted_positions(self, direction):
        return [sprite.pos + direction for sprite in self.sprites]
    
    def left_shift(self):
        new_positions = self.get_shifted_positions(LEFT)
        if self.level.are_positions_empty(new_positions):
            for sprite in self.sprites:
                sprite.add_move(LEFT)

    def right_shift(self):
        new_positions = self.get_shifted_positions(RIGHT)
        if self.level.are_positions_empty(new_positions):
            for sprite in self.sprites:
                sprite.add_move(RIGHT)
    

class FrutrisBox:
    def __init__(self, frame, tile_factory, level):
        self.frame = frame
        self.tile_factory = tile_factory
        tm = TiledMap(frame, tile_factory)
        self.level = FrutrisLevel(tm, level)
        self.moving = None

        self.drop_delay = DROP_DELAY
        self.drop_counter = self.drop_delay
        self.diamonds_queued = 0
        self.bonus_exponent = 0
        self.auto_drop_counter = 0
        self.update_mode = self.update_new_block
        self.game_over = False
    
    def insert_diamond(self, column):
        self.moving = Diamond(self.frame, self.tile_factory, self.level, 2)

    def insert_fruit_pair(self, first, second):
        self.moving = FruitPair(self.frame, self.tile_factory, self.level, (first, second))

    @property
    def finished(self):
        return self.level.finished and (not self.moving or self.moving.finished)

    def move(self):
        self.level.move()
        if not self.finished and self.moving:
            self.moving.move()

    def update_diamond(self):
        """Drops a diamond."""
        if self.finished:
            self.moving.drop()
        if self.finished:
            self.moving = None
            self.update_mode = self.update_new_block

    def update_drop(self):
        """Dropping fruit after some time."""
        self.drop_counter -= 1
        if self.drop_counter == 0 or self.auto_drop_counter >= 2:
            self.drop_counter = self.drop_delay
            self.moving.drop()
            if self.finished:
                self.update_mode = self.update_remove

    def insert_random_fruit_pair(self):
        blocks = 'abcefg'
        first = blocks[randint(0, 5)]
        second = blocks[randint(0, 5)]
        self.insert_fruit_pair(first, second)

    def update_new_block(self):
        """Inserts a random block at top center."""
        if self.diamonds_queued > 0:
            self.insert_diamond(randint(1, 6))
            self.diamonds_queued -= 1
            self.update_mode = self.update_diamond
            play_effect('diamond_drop')
        else:
            self.insert_random_fruit_pair()
            self.update_mode = self.update_drop
        
    def update_remove(self):
        """Remove quartets of blocks."""
        self.level.remove_fruit()

        if self.finished:
            self.level.drop_bricks()
            play_effect('fruit_drop_after_vanish')
        else:
            self.bonus_exponent += 1
            # play_effect(multiplets.get_vanish_classname)    
        if self.finished:
            self.bonus_exponent = 0
            if self.level.box_overflow():
                self.game_over = True
            self.update_mode = self.update_new_block

    def update(self):
        if self.finished:
            self.update_mode()

    def draw(self):
        self.level.draw()
        self.move()
        if self.moving:
            self.moving.draw()
        
    def left(self):
        self.auto_drop_counter = 0
        moveset = self.moving.left_shift()

    def right(self):
        self.auto_drop_counter = 0
        moveset = self.moving.right_shift()

    def up(self):
        self.auto_drop_counter = 0
        moveset = self.moving.rotate()
        
    def down(self):
        self.moving.drop()
        self.auto_drop_counter += 1
                                  

class FrutrisGame:

    def __init__(self, screen):
        self.level_counter = 1 #LEVEL_COUNTER_INIT
        play_effect('frutris')

        self.screen = screen
        self.frame = Frame(self.screen, Rect(10, 10, 640, 512))
        self.tile_factory = TileFactory('data/tiles.conf')

        self.frutris_box = None
        self.status_box = None
        self.events = None

        self.create_frutris()
        self.create_status_box()
        frame = Frame(self.screen, Rect(660, 220, 200, 200))
        self.score = 0

        #self.music_counter = 50
        #self.current_music = ('a', 1)

    def create_frutris(self):
        self.frutris_box = FrutrisBox(self.frame, self.tile_factory, LEVEL)

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 200))
        data = {
            'score': 0,
            'level': 1,
            }
        self.status_box = DictBox(frame, data)
        
    def update(self):
        self.frutris_box.update_mode()
        self.frutris_box.draw()
        self.status_box.draw()
        pygame.display.update()
        time.sleep(0.005)

    def exit(self):
        self.events.exit_signalled()

    def choose_next_music(self):
        letter, number = self.current_music
        number = 3 - number
        if len(self.players)>=1:
            stack_size = self.players[0].get_stack_size()
            if stack_size <= 4: letter = 'a'
            elif stack_size <= 8: letter = 'b'
            else: letter = 'c'
        self.current_music = (letter, number)
        return 'music/%s%i.wav'%(letter,number)

    def update_music(self):
        return
        self.music_counter -= 1
        if self.music_counter == 0:
            self.music_counter = 50
            if check_music_status() == CLOSE_TO_END:
                next_music(self.choose_next_music())

    def new_game(self):
        play_music('music/a1.wav')
        if self.mode == 'one player game':
            self.status_box = StatusBox(self, array([500,100]), array([200,500]))
            self.status_box['player1_score'] = 0
            self.status_box['level'] = 1
            self.players.append(FrutrisBox(self, (250, 0)))
            self.delay = ONE_PLAYER_START_DELAY
            play_effect('menu_select_game_1')
        elif self.mode == 'two player game':
            self.status_box = StatusBox(self, array([300,100]), array([200,500]))
            self.status_box['player1_score'] = 0
            self.status_box['player2_score'] = 0
            self.players.append(FrutrisBox(self, (50, 0)))
            self.players.append(FrutrisBox(self, (500, 0)))
            self.delay = TWO_PLAYER_DELAY
            play_effect('menu_select_game_2')

    def terminate_game(self):
        stop_music()
        play_effect('menu_select_quit')
        time.sleep(1)
            
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

    def update(self):
        self.frutris_box.update()
        self.frutris_box.draw()
        self.status_box.draw()
        pygame.display.update()
        if self.frutris_box.game_over:
            self.exit()

    def _deadcode(self):
        """Check for game over."""
        if self.mode == 'one player game':
            if self.players[0].game_over:
                play_effect('game_over')
                self.show_game_over('GAME OVER!')
                play_effect('highscores_normal')
                self.show_highscores(self.status_box['player1_score'])
                self.terminate_game()
            else:
                self.level_counter -= 1
                if self.level_counter == 0:
                    self.status_box['level'] += 1
                    self.level_counter = LEVEL_COUNTER_INIT
                    if self.players[0].drop_delay > LEVEL_DROP_COUNTER_DECREASE:
                        self.players[0].drop_delay -= LEVEL_DROP_COUNTER_DECREASE
                    
        elif self.mode == 'two player game':
            if self.players[0].game_over:
                play_effect('winner_second')
                self.show_game_over('Player 2 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player2_score'])
                self.terminate_game()
            elif self.players[1].game_over:
                play_effect('winner_first')
                self.show_game_over('Player 1 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player1_score'])
                self.terminate_game()

        self.update_music()


    def get_listener(self):
        listener = EventListener(keymap = {
            K_LEFT: self.frutris_box.left,
            K_RIGHT: self.frutris_box.right,
            K_UP: self.frutris_box.up,
            K_DOWN: self.frutris_box.down,
            K_ESCAPE: self.exit
            })
        return listener

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(self.get_listener())
        self.events.add_callback(self)
        self.events.event_loop()



if __name__ == '__main__':
    game = Game('data/frutris.conf', FrutrisGame)
    game.run()

