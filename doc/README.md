
# Writing a Mini-Game with tilegamelib

The Python library **tilegamelib** is a wrapper around the `arcade` library. It is meant to facilitate creating simple games. Let's see whether we can build a simple maze game with a few lines of Python code.

## 1. Import arcade

Let's import the library first:

    import arcade

## 2. A class for the game

The base for developing games is the class `arcade.Window`.
We can create our own subclass and run it in the arcade *event loop*:

    class MyGame(arcade.Window):

        def __init__(self):
            super().__init__(600, 400, "my game")

Of course, we need to instantiate our class as well. A good practice is to use a `__main__` block at the end of the file:

    if __name__ == '__main__':
        window = MyGame()
        arcade.run()


When you run the program, you should see a black window that forever. In some environments the window may appear in the background, so press Alt-Tab to focus it.


## 3. Adding state

We can keep game data inside the class. To do so, add attributes inside the `__init__` function. E.g. to store the score, we could define an integer:

    self.score = 0


## 4. Load a tileset

For the graphics, we need to load a set of tiles. You find images and a specification CSV file in the `examples` folder:

    from tilegamelib import load_tiles

    tiles = load_tiles('fruit.csv')

## 5. Create a Tile Map

The class `tilegamelib.TiledMap` draws 2D-maps composed of the tiles we just loaded. Let's import it:

    from tilegamelib import TiledMap

Create a new map in `__init__` and fill it with a sample level (given as a string):

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

    self.map = TiledMap(tiles, MAZE)

## 6. Draw the map

At this point, you won't see anything yet. First, you need to add a method to your class that draws the map:

    def draw(self):
        self.map.draw()

Fortunately, `arcade` calls this method in short intervals automatically. You won't have to call it yourself.

## 7. More tiles

Experiment with the symbols in the map. For some of them, you may have to edit the CSV file.

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

## 8. Sprites

Another possibility to draw tiles explicitly. The loaded tiles bring their own method for it. Let's draw some fruit in the `draw()` method:

    tiles['a'].draw(100, 100, 32, 32)

Make sure this line occurs **after** drawing the tiled map, otherwise the map might occlude the fruit of your work (**pun :-)**).

The parameters are the x and y position and the size. Note that `arcade` allows you to zoom and shrink textures.

**Note:** `arcade` has its own sprite class, but I haven't explored it yet.

## 9. Action!

To move the object, we need keyboard controls. If you want the
keys to our own method, use:

    from tilegamelib import PLAYER_MOVES

    ...
        def on_key_press(self, symbol, mod):
            vec = PLAYER_MOVES.get(symbol)
            if vec:
                self.move(vec)
            elif symbol == ESCAPE:
                arcade.window_commands.close_window()


The `arcade.key` module contains constants to access all kinds of keys.

## 10. Vectors

The `tilegamelib.vector` class allows you to conveniently define positions that you can add together:

    from tilegamelib import Vector
    from tilegamelib.vector import UP, DOWN, LEFT, RIGHT

    position = Vector(3, 4)
    position += LEFT

## 11. Questions you might have at this point

### 11.1 How can I check the tile at a given position?

    print(self.map.at(self.sprite.pos))

### 11.2 How can I check the position where I am moving?

    print(self.sprite.pos + direction)

### 11.3 How can I place something on the map?

    self.map.set_tile((4,4), 'a')

### 11.4 What other tiles are there?

See the `examples/images` folder.

### 11.5 Can I draw text?

Yes, but I have to look it up.

### 11.6 I want a ghost that moves randomly. How?

You can find all movement vectors by importing

    from tilegamelib.vector import UP, DOWN, LEFT, RIGHT

To manage the movement, define an `update()` method that is also calle automatically.

## 12. Go create!

The documentation of `tilegamelib` is still very immature, in particular the details of how to plug in your own graphics, keys and sound effects. Please report any questions and issues on [GitHub](https://github.com/krother/tilegamelib) or by e-mail to `krother@academis.eu`.
