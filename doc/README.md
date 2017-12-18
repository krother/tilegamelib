
# Writing a Mini-Game with tilegamelib

The Python library **tilegamelib** is a wrapper around the popular library **pygame**. It is meant to facilitate creating simple games. Let's see whether we can build a simple maze game with a few lines of Python code.

## 1. Create a Game Object

The base for developing games is the class `tilegamelib.Game`. We first need to import it:

    from tilegamelib import Game

Now we can create a `Game` object and runs its *event loop*:

    game = Game()
    game.event_loop()

When you run the program, you should see a black window that closes when you press the *escape* key. (With some GUIs like Anaconda Spyder on Windows, the window may appear in the background, so press Alt-Tab to focus it).

## 2. A class for the game

Let's write a class for our own game that will contain all game data. We move the `Game` object into that class. Note that we make it an **attribute** of the class by the `self` prefix:

    class MazeGame:

        def __init__(self):
            self.game = Game()
            self.game.event_loop()


Of course, we need to instantiate the `MazeGame` class as well. A good practice is to use a `__main__` block at the end of the file:

if __name__ == '__main__':
    maze_game = MazeGame()


## 3. Drawing a Tile Map

The class `tilegamelib.TiledMap` is responsible for drawing 2D-maps composed of square tiles. Let's import it:

    from tilegamelib import TiledMap

In `__init__` we create a new map and fill it with wall tiles:

    self.map = TiledMap(self.game.frame, self.game.tile_factory)
    self.map.fill_map('#', (10, 10))

At this point, we won't see anything yet. First, we need to write a method in `MazeGame` that draws the map:

    def draw(self):
        self.map.draw()

We also need to modify the call of `event_loop()`, so that it calls our `draw()` method in regular intervals. Note that **`event_loop()` must be called in the last line of the `__init__()` method.**

    self.game.event_loop(draw_func=self.draw)

Now you should see a blue kind of chessboard.

## 4. Map Contents

To let a bit more happen on the screen, we can set the contents of the map to a string containing 10 x 10 characters:

    MAZE = """##########
    #........#
    #.#.####.#
    #.#......#
    #.#....#.#
    #.#....#.#
    #......#.#
    #.####.#.#
    #........#
    ##########"""

And set the `TiledMap` to use this data:

    self.map.set_map(MAZE)

There are several characters encoding for predefined graphic tiles:

| characters | graphics |
|------------|----------|
| `#`        | wall     |
| `.`        | empty    |
| `*`        | dot      |
| `x`        | dark crate  |
| `X`        | light crate  |
| `a`-`h`    | fruit     |
| `d`        | diamond   |
| `+`        | star      |
| `@`        | blue dot  |

## 5. Sprites

Another possibility to draw tiles are **sprites**, moveable objects:

    from tilegamelib.sprites import Sprite

Of course, sprites need to be created in `__init__` as well (again, **before** calling `event_loop`). We will give our sprite a well-known *"face"*:

    self.sprite = Sprite(self.game.frame, self.game.get_tile('b.pac_right'),
                         (1, 1), speed=2)

And we need to draw the sprite in `draw()`:

    self.sprite.draw()

## 6. Action!

Now we will move our sprite. The `Game` class is taking care of reading from the keyboard. All we need to do is to redirect the arrow keys to our own method. As this is a very common thing, this is rather straightforward:

    def move(self, direction):
        print(direction)

And modify the call to `event_loop()` to:

    self.game.event_loop(figure_moves=self.move, draw_func=self.draw)

Now you should see that `direction` contains a different vector for each arrow key. We can pass on that vector to `sprite`, so that it moves:

    self.sprite.add_move(direction)
    self.game.wait_for_move(self.sprite, self.draw, 0.01)

The number at the end is for adjusting movement speed.

Now the figure should move through the maze!

## 7. Questions you might have at this point

### 7.1 How can I check the tile at the sprite position?

    print(self.map.at(self.sprite.pos))

### 7.2 How can I check the position where the sprite is moving?

    print(self.sprite.pos + direction)

### 7.3 How can I place something on the map?

    self.map.set_tile((4,4), 'a')

### 7.4 What other tiles are there?

See the file [`tiles.conf`](https://github.com/krother/tilegamelib/blob/master/examples/data/tiles.conf).

### 7.5 Can I draw text?

    self.game.frame.print_text("Hello World", (50, 400))

### 7.6 I want a ghost that moves randomly. How?

You can find all movement vectors by importing

    from tilegamelib.vector import UP, DOWN, LEFT, RIGHT

Place the code moving the ghost sprite at the beginning of `draw()`.

## 8. Go create!

The documentation of `tilegamelib` is still very immature, in particular the details of how to plug in your own graphics, keys and sound effects. Please report any questions and issues on [GitHub](https://github.com/krother/tilegamelib) or by e-mail to `krother@academis.eu`.
