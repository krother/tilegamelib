"""
Generiert Sternenhimmel
"""

import os
from random import randint
import sys

from PIL import Image
from PIL import ImageDraw

XSIZE, YSIZE = 800, 600
STAR_PATH = os.path.split(__file__)[0]

def create_starmap(radius, color, nstars, outfile):
    w = Image.new('RGBA', (XSIZE, YSIZE))
    d = ImageDraw.Draw(w)

    for i in range(nstars):
        x = randint(0, XSIZE)
        y = randint(0, YSIZE)
        d.ellipse(((x, y), (x+radius, y+radius)), '#'+color)

    w.save(outfile)


if __name__ == '__main__':
    if len(sys.argv) == 5:
        RADIUS = int(sys.argv[1])
        COLOR = sys.argv[2]
        NSTARS = int(sys.argv[3])
        OUTFILE = sys.argv[4]
        create_starmap(RADIUS, COLOR, NSTARS, OUTFILE)
    elif len(sys.argv) == 1:
        create_starmap(3, 'ffffff', 50, os.path.join(STAR_PATH, 'stars1.png'))
        create_starmap(2, 'cccccc', 100, os.path.join(STAR_PATH, 'stars2.png'))
        create_starmap(1, 'aaaaaa', 200, os.path.join(STAR_PATH, 'stars3.png'))
    elif sys.argv[1] == 'big':
        XSIZE, YSIZE = 1600, 1200
        create_starmap(2, 'cccccc', 50, os.path.join(STAR_PATH, 'stars1b.png'))
        create_starmap(1, 'bbbbbb', 100, os.path.join(STAR_PATH, 'stars2b.png'))
        create_starmap(1, '999999', 200, os.path.join(STAR_PATH, 'stars3b.png'))

    else:
        print("generate stars: python create_stars.py <radius> <hex-color> <n_stars> <png_filename>")
