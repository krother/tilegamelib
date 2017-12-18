
# tilegamelib

A Python/pygame library for games based on square tiles.

(c) 2015 Kristian Rother (krother@academis.eu)

Distributed under the conditions of the MIT license.
(some artwork covered by a separate license. See ART_LICENSE.TXT for details)

## Description

tilegamelib makes it easier to create pygame-based games that have graphics consisting of small square-shaped tiles (think Sokoban, Pacman, Tetris, Atomix and their countless siblings).


## Installation for development

### 1. Setting up virtualenv

    cd tilegamelib/
    mkvirtualenv tilegamelib
    setvirtualenvproject ~/.virtualenvs/tilegamelib/ .
 
### 2. Installing pygame

Just try:

    pip install pygame

With older versions of `pip`, you need to install `pygame` manually:

    hg clone https://bitbucket.org/pygame/pygame
    cd pygame
    python3 setup.py install --prefix="$HOME/.virtualenvs/tilegamelib"

### 3. Installing tilegamelib

    pip install --editable .


## 4. Play example Games

Run the programs in the `examples/` directory:

    cd examples/
    python __main__.py


## Running automated Tests

    cd test
    python test_all.py


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

