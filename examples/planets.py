
from math import sqrt
import time

import pygame

from tilegamelib.screen import Screen
from tilegamelib.tile_factory import TileFactory
from tilegamelib.vector import Vector

VERZOEGERUNG = 0.01


class Planet:

    def __init__(self, name, x, y, vx, vy, masse):
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.masse = masse

    def entfernung(self, planet):
        '''Entfernung ausrechnen'''
        dx = (self.x - planet.x)**2
        dy = (self.y - planet.y)**2
        return sqrt(dx**2 + dy**2)

    def anziehungskraft(self, planet):
        '''Geschwindigkeit veraendern'''
        entfernung = self.entfernung(planet)
        if entfernung > 0:
            beschl_x = -planet.masse / (entfernung**3) * self.x
            beschl_y = -planet.masse / (entfernung**3) * self.y
            self.vx += beschl_x
            self.vy += beschl_y

    def bewegen(self):
        '''Position veraendern'''
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def zeichnen(self, screen, tiles):
        '''Auf dem Bildschirm anzeigen'''
        tile = tiles.get(self.name.lower())
        tile.draw(screen, Vector(self.x + 300, self.y + 200))


def simulieren(planeten, screen, tf):
    screen.clear()
    sonne = planeten[0]
    planeten = planeten[1:]
    for p in planeten:
        p.bewegen()
        p.zeichnen(screen, tf)
        p.anziehungskraft(sonne)
    sonne.zeichnen(screen, tf)
    pygame.display.update()
    time.sleep(VERZOEGERUNG)


sc = Screen(Vector(600, 400), 'data/background.png')
tf = TileFactory('data/tiles.conf')

planeten = [
    Planet("Sonne", 0, 0, 0, 0, 300000000),
    Planet("Erde", 0, 100, 2.17601657851805, 0, 1),
    Planet("Venus", 0, 60, -5.91572020809202436808504899092, 0, 1)
]

while True:
    simulieren(planeten, sc, tf)
