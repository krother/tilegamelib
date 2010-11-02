
tilegamelib
===========

A Pygame library for games based on quadratic elements.

(c) 2010 Kristian Rother (krother@rubor.de)

Distributed under the conditions of the GNU General public license.
See LICENSE_GPL.TXT for details.

Version 0.8


Description
-----------
tilegamelib makes it easier to create pygame-based games that have graphics consisting of small square-shaped parts 
(all of Sokoban, Pacman, Tetris, Atomix and their countless clones).

The library emerged from cleaning up the code of Frutris (see www.rubor.de), and applying Unit Tests and some design patterns.


Installation
------------
1) Install pygame
2) python setup.py install


Testing
-------
cd test
python test_all.py


How to use it
-------------
To get started, I recommend the following approach:

1) Run all tests.
2) Look for something interesting on the screen.
3) See in the according test how it is done.


Classes:
--------
Here is an overview of modules and Classes

interfaces.py
	Drawable - provides draw() 
	Updateable - provides update()
	Modal - provides acitvate()
	Commandable - provides handle_command()
	GameContext - provides access to a game environment.
	
settings.py
	'''all kinds of constants in class variables, that can be inherited.'''
	BasicSettings
	DialogSettings(BasicSettings)

screen.py
	Screen - manages the main screen window.
	Frame - a part of a screen
	GameElement - anything in the game that needs a screen, settings, sounds, tiles.

tiles.py
	Tile - quadratic piece of graphic.
	TileFactory - a class that produces tiles.

sprites.py
	Sprite(Drawable) - A moveable tile.
	AnimationSequence(Drawable, Updateable) - displays a sequence of tiles.
	SpriteList(Drawable, Updateable) - container for sprites

tiled_map.py
        Move - an instruction for moving something.   
    	TiledMap(Drawable) - a 2D arrays of tiles.
    	MoveableTiledMap(TiledMap, Updateable) - a TiledMap where tiles can smoothly be moved simulatneously.

basic_boxes.py	
	TextBox(Drawable) - a box displaying text
	ImageBox(Drawable) - a box displaying a static image
	DictBox(Drawable) - a box displaying a dictionary

events.py
	# Observer pattern for EventListeners
	EventGenerator - contains an event loop, detects and distributes events
	EventListener - does something with an event.

game_over.py
	GameOverBox(Drawable, Modal) - shows a game over message.

game_paused.py
	AnyKeyListener(EventListener) - waits for a key to be pressed.
	PausedBox(Drawable, Updateable) - shows a 'game paused' message.

menu.py
	MenuBox(Drawable) - manages a menu
	TileMenuBox(MenuBox) - a menu composed of tiles
	TextMenuBox(MenuBox) - a menu composed of text

highscores.py
	''''''
	TextEnteringListener(EventListener) - collects text until enter.
	HighscoreList - saveable high score list.
	HighscoreBox(Drawable, Updateable, Commandable, Modal) - displays a high score list.

player.py
	PlayerBox(Drawable, Updateable) - manages a player instance

game.py
	Game - manages several players

game_engine.py
	GameFactory - creates instances of everything.
	GameEngine - guides the flow from main menu to game and vice versa.

sounds.py
	MusicPlayer(Updateable)
	EffectPlayer(Updateable)

