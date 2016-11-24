"""
Generiert Sternenhimmel
"""

from PIL import Image
from PIL import ImageDraw
from random import randint
import sys


XSIZE, YSIZE = 800, 600

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
        create_starmap(3, 'ffffff', 50, 'stars1.png')
        create_starmap(2, 'cccccc', 100, 'stars2.png')
        create_starmap(1, 'aaaaaa', 200, 'stars3.png')

    else:
        print("generate stars: python sterne.py <radius> <hex-farbe> <anzahl> <png_datei>")
