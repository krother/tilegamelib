
from tilegamelib import RIGHT
from tilegamelib.games.sliding_puzzle import SlidingPuzzle


SOLVED = '''
######
#aaaa#
#bbbb#
#cccc#
#ddd.#
######
'''

ONE_AWAY = '''
######
#aaaa#
#bbbb#
#ccc.#
#dddc#
######
'''

TWO_DELETE = '''
######
#aaaa#
#bbbb#
#cc..#
#dddc#
######
'''

TWO_AWAY = '''
######
#aaaa#
#bbbb#
#cc.c#
#dddc#
######
'''


def test_repr():
    s = SlidingPuzzle(SOLVED)
    assert str(s) == SOLVED.strip()


def test_solved():
    s = SlidingPuzzle(SOLVED)
    assert s.solved


def test_not_solved():
    s = SlidingPuzzle(ONE_AWAY)
    assert not s.solved


def test_move():
    s = SlidingPuzzle(ONE_AWAY)
    mv = s.move(RIGHT)
    assert str(s) == TWO_DELETE.strip()
    mv.finish()
    assert str(s) == TWO_AWAY.strip()
