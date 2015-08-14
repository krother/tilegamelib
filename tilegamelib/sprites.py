
from tilegamelib.screen import Screen
from tilegamelib.frame import Frame
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT
from tilegamelib.move import Move, wait_for_move
from vector import Vector
from pygame import Rect
import pygame
import time


class Sprite:
    """
    Object that moves along a tile grid.
    Sprites have a queue of moves.
    """
    def __init__(self, frame, tile, pos=None, speed=1):
        self.frame = frame
        self.tile = tile
        self.size = self.tile.size
        self.pos = pos # position in tiles not pixels
        if pos == None:
            self.pos = Vector(0,0)
        
        self.path = [] # Queue of moves
        self._move = None
        self.direction = None
        self.speed = speed

    def add_move(self, direction, priority=False):
        """Adds a move to the movement queue."""
        if priority:
            self.path = [direction] + self.path
        else:
            self.path.append(direction)

    def get_next_move(self):
        """Pull next move from the queue"""
        if self.path:
            self.direction = self.path.pop(0)
            start_vector = self.pos * self.size.x
            self._move = Move(self.frame, self.tile, start_vector, self.direction*self.speed, steps=self.size.x//self.speed)

    @property
    def finished(self):
        if self._move and not self._move.finished or self.path:
            return False
        return True

    def move(self):
        """apply path to object vector and perform movement."""
        if not self._move:
            self.get_next_move()
        if self._move:
            self._move.move()
            if self._move.finished:
                self.pos += self.direction
                self._move = None
                self.direction = None
    
    def draw(self):
        """Draw the sprite on the screen."""
        if not self._move:
            pos = self.pos * self.size.x
            destrect = Rect(pos.x,pos.y,self.size.x,self.size.y)
            self.tile.draw(self.frame, destrect)
    

if __name__ == '__main__':
    screen = Screen(Vector(800,550), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 400, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')

    sprite = Sprite(frame, tile_factory.get('#'), Vector(3, 3))
    sprite.draw()
    pygame.display.update()
    time.sleep(1.0)

    sprite.add_move(DOWN)
    sprite.add_move(DOWN)
    sprite.add_move(RIGHT)
    sprite.add_move(UP)
    wait_for_move(sprite, screen, sprite.draw, 0.01)
    
    sprite.draw()
    pygame.display.update()
    time.sleep(1.0)
