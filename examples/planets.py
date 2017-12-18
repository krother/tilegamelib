
from math import sqrt
import time

import numpy as np

import pygame

from tilegamelib.screen import Screen
from tilegamelib.tile_factory import TileFactory

VERZOEGERUNG = 0.01


class Planet:

    def __init__(self, name, x, y, vx, vy, masse):
        self.name = name
        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])
        self.masse = masse

    def entfernung(self, planet):
        '''Entfernung ausrechnen'''
        delta = (self.position - planet.position)**2
        return sqrt(delta[0]**2 + delta[1]**2)

    def anziehungskraft(self, planet):
        '''Geschwindigkeit veraendern'''
        entfernung = self.entfernung(planet)
        if entfernung > 0:
            beschleunigung = -planet.masse / (entfernung**3) * self.position
            self.velocity += beschleunigung

    def bewegen(self):
        '''Position veraendern'''
        self.position += self.velocity

    def zeichnen(self, screen, tiles):
        '''Auf dem Bildschirm anzeigen'''
        tile = tiles.get(self.name.lower())
        tile.draw(screen, (self.position[0] + 300, self.position[1] + 200))


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


sc = Screen()
tf = TileFactory()

planeten = [
    Planet("Sonne", 0.0, 0.0, 0.0, 0.0, 300000000.0),
    Planet("Erde", 0.0, 100.0, 2.17601657851805, 0.0, 1.0),
    Planet("Venus", 0.0, 60.0, -5.91572020809202436808504899092, 0.0, 1.0)
]

while True:
    simulieren(planeten, sc, tf)
