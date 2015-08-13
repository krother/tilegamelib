#! /usr/bin/python

from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from tilegamelib.frame import Frame
from tilegamelib.game import Game, GameApp
from tilegamelib.sprites import Sprite, SpriteList
from tilegamelib.tiled_map import MoveableTiledMap
from tilegamelib.basic_boxes import DictBox, LifeDisplay
from pac_settings import PacSettings
from pac_levels import LEVELS
from pac_sprites import Pac, Ghost
import random
import pygame

ONE_PLAYER_START_DELAY = 10


class PacLevel:
    
    def __init__(self, frame, factory, pac_player):
        self.map = MoveableTiledMap(frame, factory)
        frame = Frame(self, Rect(10, 425, 100,32))
        self.sprites = SpriteList()
        self.level = None
        self.collided = False
        self.player = pac_player
        self.mode = None

    @property
    def ghosts(self):
        return self.sprites[1:]

    def create_ghosts(self):
        for gp in self.level.ghost_positions:
            ghost = Ghost(self.context, gp, self.map)
            self.sprites.append(ghost)

    def check_collision(self):
        if self.player.collision(self.ghosts):
            self.mode = self.update_finish_move
            self.collided = True

    def update_die(self):
        """finish movements"""
        if not self.sprites.is_moving():
            self.draw()
            pygame.display.update()
            time.sleep(1)
            if self.pac.lives == 0:
                self.game_over = True
            else:
                self.master.reset_level()
                
    def update_level_complete(self):
        """finish movements"""
        if not self.sprites.is_moving():
            self.draw()
            pygame.display.update()
            time.sleep(1)
            self.master.level_complete()

    def update_ingame(self):
        self.check_collision()
        if not self.collided:
            for ghost in self.ghosts:
                ghost.keep_moving()
        self.check_collision()
        if self.pac.dots_eaten == self.dots_total:
            self.mode = self.update_level_complete
        
    def update(self):
        """Main game loop. Links to logic functions."""
        self.map.update()
        self.sprites.update()
        if self.mode:
            self.mode()
        
    def draw(self):
        """Draws the 2D map and sprites."""
        self.map.draw()
        self.sprites.draw()
            

class PacGame:

    def __init__(self):
        self.status_box = None

    def start_level(self, level):
        self.level = level
        self.map.fill_map(level)
        self.reset_level()

    def reset_level(self):
        self.sprites = SpriteList()
        self.lives.draw()
        self.create_pac()
        self.create_ghosts()
        self.mode = self.update_ingame

    @property
    def level(self):
        return self.status_box.data['level']

    def level_complete(self):
        self.status_box.data['level'] += 1
        if self.level > len(LEVELS):
            self.game_over_text = 'All levels complete!'
            self.terminate()
        else:
            self.players[0].start_level(LEVELS[self.level-1])
        
    def terminate(self):
        if self.players:
            self.highscore = self.players[0].score
        Game.terminate(self)

    def draw(self):
        Game.draw(self)
        self.status_box.draw()

    def create_players(self):
        frame = Frame(self, np.array([660,20]), np.array([200,200]))
        data = {
            'score': 0,
            'level':1,
            }
        self.status_box = DictBox(frame, data)
        frame = Frame(self, np.array([10, 10]), np.array([640,512]))
        self.players.append(PacBox(frame, self))
        self.players[0].start_level(LEVELS[self.level-1])

    def main(self):
        pass



if __name__ == '__main__':
    pac = PacGame()
    pac.main()

