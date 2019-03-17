
import arcade
from arcade.key import ESCAPE
from collections import Counter
from tilegamelib import TiledMap, load_tiles
from tilegamelib import MapMove
from tilegamelib import PLAYER_MOVES
from tilegamelib import Vector


PUZZLEMAP = """######
#abce#
#ecba#
#abce#
#acb.#
######"""

SIZEX, SIZEY = (350, 350)


class SlidingPuzzle(arcade.Window):

    def __init__(self):
        """initialize everything"""
        super().__init__(SIZEX, SIZEY, "Sliding Puzzle")
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles = load_tiles('fruit.csv')
        self.map = TiledMap(self.tiles, PUZZLEMAP, offset=Vector(100, 100))
        self.gap = Vector(4, 4)
        self.moving = None

    def count_same(self, row):
        """counts most frequent char in a string"""
        counter = Counter(row)
        return counter.most_common(1)[0][1]

    def check_complete(self):
        """exit if all fruit sorted into rows"""
        same = [self.count_same(row) for row in self.map.map[1:5]]
        if sum(same) == 15:
            arcade.window_commands.close_window()

    def on_draw(self):
        """automatically called to draw everything"""
        arcade.start_render()
        self.map.draw()
        if self.moving:
            self.moving.draw()

    def move(self, vec):
        """starts a move"""
        source = self.gap - vec
        if self.map.at(source) == '#' or self.moving:
            return
        self.moving = MapMove(self.map, source, vec)
        self.gap = source

    def update(self, delta_time):
        """automatically called every frame"""
        if self.moving:
            self.moving.update()
            if self.moving.finished:
                self.moving = None
                self.check_complete()

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        vec = PLAYER_MOVES.get(symbol)
        if vec:
            self.move(vec)
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()


if __name__ == '__main__':
    window = SlidingPuzzle()
    arcade.run()
