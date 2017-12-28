
import time

from tilegamelib.move import Move
from tilegamelib.vector import RIGHT


def test_move(game, frame, tile_factory):
    pac = tile_factory.get('b.pac_right')
    move = Move(frame, pac, (50, 50), RIGHT * 2, 200)
    game.wait_for_move(move)
    time.sleep(1)
