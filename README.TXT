
# tilegamelib

A Python/pygame library for games based on quadratic tiles.

(c) 2015 Kristian Rother (krother@academis.eu)

Distributed under the conditions of the Python license.
(some artwork covered by a separate license. See ART_LICENSE.TXT for details)

## Description

tilegamelib makes it easier to create pygame-based games that have graphics consisting of small square-shaped tiles (think Sokoban, Pacman, Tetris, Atomix and their countless siblings).


## Installation for development

### 1. Setting up virtualenv

    cd tilegamelib/
    mkvirtualenv tilegamelib
    setvirtualenvproject ~/.virtualenvs/tilegamelib/ .
 
### 2. Installing pygame

    hg clone https://bitbucket.org/pygame/pygame
    cd pygame
    python3 setup.py install --prefix="$HOME/.virtualenvs/tilegamelib"

### 3. Installing tilegamelib

    pip install --editable .


## Testing

    cd test
    python test_all.py



## How to use it

To get started:

1. Run the examples in `examples/`
2. Read the code
3. Try things


## Classes

Here is an overview of the most important classes

### screen.Screen

manages the main screen window.


### frame.Frame

a part of a screen


### tiles.Tile

a quadratic piece of graphic.


### tile_factory.TileFactory

a class that produces tiles.


### sprites.Sprite

A moveable tile.


### tiled_map.TiledMap

a 2D array of tiles.
    	

### events.EventGenerator

Observer pattern for EventListeners. Contains an event loop, detects and distributes events

