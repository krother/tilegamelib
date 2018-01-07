
# tilegamelib

A Python library for games based on square tiles.

[![Build Status](https://travis-ci.org/krother/tilegamelib.svg?branch=master)](https://travis-ci.org/krother/tilegamelib)

(c) 2015 Kristian Rother (krother@academis.eu)

Distributed under the conditions of the MIT license.
(some artwork covered by a separate license. See ART_LICENSE.TXT for details)

## Description

tilegamelib helps create pygame-based games that have graphics consisting of small square-shaped tiles (think Sokoban, Pacman, Tetris, Atomix and their countless siblings).


## Installation

It is assumed that you have **Python 3.5** or higher. The instructions here work for Linux and Windows.
I have no idea how pygame works on MacOS.

The installation should handle itself:

    pip install tilegamelib

However, *if this fails*, feel encouraged to download the source code and try the following steps:

### Step 1: Install pygame

Just try:

    pip install pygame

### Step 2: Tell Python where to find tilegamelib

Set the `PYTHONPATH` environment variable to the directory in which this `README` file is (In Spyder, check the *"Tools"* menu).

Alternatively, you can try a local installation using `pip`:

    pip install --editable .


### Setting up pygame with virtualenv

    hg clone https://bitbucket.org/pygame/pygame
    cd pygame
    python3 setup.py install --prefix="$HOME/.virtualenvs/tilegamelib"


## Play example Games

Run the programs in the `examples/` directory:

* `examples/sliding_puzzle.py`
* `examples/collect_fruit.py`
* `examples/boxes.py`
* `examples/snake.py`
* `examples/pac.py`
* `examples/starscape/starscape.py`
* `examples/frutris/frutris.py`


## Write your own mini-game

See the [Beginners Guide](doc/README.md)

## Running automated Tests

    cd test
    python test_all.py


## Classes

Here is an overview of the most important classes

| class | description |
|-------|-------------|
| tilegamelib.Game | Facade for frequently used functions |
| tilegamelib.TiledMap | 2D map composed of tiles |
| tilegamelib.Sprite   | moving object |
| tilegamelib.Screen   | manages screen window |
| tilegamelib.EventGenerator | main event loop |
| tilegamelib.Frame | rectangular area on screen |
| tilegamelib.TileFactory | loads tile graphics |
