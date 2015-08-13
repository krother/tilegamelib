#! /usr/bin/python

from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT
from tilegamelib.frame import Frame
from tilegamelib.game_factory import GameFactory
from tilegamelib.game import GameState, TitleScreenState, run_game
from tilegamelib.sprites import Sprite, SpriteList
from tilegamelib.basic_boxes import DictBox
#from snake_settings import SnakeSettings
import random
import time
import pygame

MOVE_DELAY = 15

LEVEL = """####################
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
####################"""

MOVE_OK = 1
MOVE_CRASH = 2
HEAD_SPEED = 4

TILE_SYNONYMS = [('#','b.wall'),('.','b.empty'),
                ('a','f.banana'),('b','f.orange'),
                ('c','f.melon'),('d','f.pineapple'),
                ('e','f.winogrona'),('f','f.cherry'),
                ('g','f.paprika'),
                ('x','f.diamond'),
                ]

HEAD_TILES = {
    UP: 'b.pac_up',
    DOWN: 'b.pac_down',
    LEFT: 'b.pac_left',
    RIGHT: 'b.pac_right'
    }


class SnakeLevel:

    def __init__(self, data):
        self.map = []
        self.set_level(data)

    def set_level(self, data):
        self.map = map(list, data.split("\n"))

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.map])

    def get(self, pos):
        return self.map[pos.y][pos.x]

    def place_fruit(self, pos, fruit):
        self.map[pos.y][pos.x] = fruit

    def remove_fruit(self, pos):
        tile = self.get(pos)
        if tile != '.':
            self.map[pos.y][pos.x] = '.'

    def place_random_fruit(self):
        x = random.randint(1, len(self.map[0]))
        y = random.randint(1, len(self.map))
        fruit = random.randint(0, 5)
        self.place_fruit(Vector(x, y), 'abcdef'[fruit])


class SnakeSprite:

    def __init__(self, frame, game_factory, pos):
        self.frame = frame
        self.gf = game_factory
        self.head = None
        self.tail = []
        self.tail_waiting = []
        self.move_queue = []
        self.tail_moves = []
        self.create_head(pos)

    @property
    def length(self):
        return len(self.tail) + len(self.tail_waiting) + 1
    
    @property
    def sprites(self):
        return [self.head] + self.tail
                
    def is_moving(self):
        if self.head.is_moving() or self.move_queue:
            return True
    
    def create_head(self, pos):
        tile = self.gf.tile_factory.get('b.pac_right')
        self.head = Sprite(self.frame, tile, pos, HEAD_SPEED)

    def add_tail_segment(self):
        tile = self.gf.tile_factory.get('b.tail')
        self.tail_waiting.append(Sprite(self.frame, tile, self.head.pos, HEAD_SPEED))

    def set_direction(self, direction):
        headtile = HEAD_TILES[direction]
        self.head.tile = self.gf.tile_factory.get(headtile)

    def add_move(self, direction, tail):
        self.move_queue.append([direction] + tail)

    def add_next_move(self):
        moves = self.move_queue.pop(0)
        self.set_direction(moves[0])
        for sprite, vec in zip(self.sprites, moves):
            sprite.add_move(vec)
        if self.tail_waiting:
            self.tail.append(self.tail_waiting.pop())

    def update(self):
        if not self.head.is_moving() and self.move_queue:
            self.add_next_move()
        for s in self.sprites:
            s.update()
            
    def draw(self):
        for s in self.sprites:
            s.draw()


        
class SnakeController:

    def __init__(self, pos, direction, level, sprite):
        self.sprite = sprite
        self.level = level
        self.pos = pos
        self.tail = []
        self.direction = direction
        self.crashed = False
        self.eaten = ''

    @property
    def positions(self):
        result = [self.pos]
        for pos in self.tail:
            result.append(result[-1] + pos)
        return result

    def grow(self):
        self.tail.append(Vector(0, 0))
        self.sprite.add_tail_segment()

    def get_tail_moves(self):
        result = []
        for t in self.tail:
            result.append(Vector(-t.x, -t.y))
        return result

    def move(self, vec):
        newpos = self.pos + vec
        tile = self.level.map[newpos.y][newpos.x]
        if newpos in self.positions or tile == '#':
            self.crashed = True
        else:
            self.pos = newpos
            self.direction = vec
            self.sprite.add_move(vec, self.get_tail_moves())
            if tile != '.':
                self.grow()
                self.eaten = tile
            if len(self.tail) > 0:
                self.tail = [Vector(-vec.x, -vec.y)] + self.tail[:-1]

    def left(self):
        self.move(LEFT)

    def right(self):
        self.move(RIGHT)

    def up(self):
        self.move(UP)

    def down(self):
        self.move(DOWN)



class SnakeGameState(GameState):

    def create(self):
        # screen
        frame = Frame(self.gf.screen, Rect(660, 20, 200, 200))
        self.status_box = DictBox(frame, {'score':0})

        # level
        self.create_level()
        self.gf.tile_factory.add_tile_synonyms(TILE_SYNONYMS)
        self.tmap = TiledMap(self.frame, self.gf.tile_factory)
        self.tmap.fill_map(str(self.level))
        self.tmap.cache_map()

        # snake
        start_pos = Vector(5, 5)
        frame = Frame(screen, Rect(10, 10, 640, 512))
        self.snake = SnakeSprite(frame, self.gf, start_pos)
        self.control = SnakeController(start_pos, RIGHT, self.level, self.snake)
        
        # events
        self.update_mode = self.update_ingame
        self.move_delay = MOVE_DELAY
        self.delay = MOVE_DELAY
        methods = (snake.left, snake.right, snake.up, snake.down)
        # KEY_REPEAT = GAME_KEY_REPEAT
        elis = EventListener(keymap=dict(zip(MOVES, methods)))
        self.events.add_listener(elis)

    def create_level(self):
        self.level = SnakeMap(LEVEL)
        self.place_random_fruit()
        self.map.fill_map(str(self.level))
        self.map.cache_map

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.snake.is_moving():
            self.draw()
            pygame.display.update()
            time.sleep(1)
            self.events.exit_signalled()

    def update_ingame(self):
        self.delay -= 1
        if self.delay <=0:
            self.move_sprites()
            self.delay = self.move_delay
        if self.controller.eaten and not self.snake.is_moving():
            self.level.place_random_fruit()
            self.level.remove_fruit(self.controller.pos)
            self.tmap.fill_map(str(self.level))
            #self.map.set_tile(pos, fruit)
            self.tmap.cache_map()
            self.status_box.data['score'] += 100
        if self.controller.crashed:
            self.update_mode = self.update_finish_move

    def update(self):
        self.update_mode()
        self.snake.update()
        self.draw()
        
    def draw(self):
        self.tmap.draw()
        self.snake.draw()
        self.status_box.draw()

    def get_next_state(self):
        return GameOverState(self.gf, self.score)


if __name__ == '__main__':
    snake_factory = GameFactory('data/settings.txt')
    snake_title = TitleScreenState(snake_factory)
    run_game(snake_title)
            
