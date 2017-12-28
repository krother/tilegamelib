
import pytest

from pygame import Rect, image

from tilegamelib import Frame, Sprite
from tilegamelib.config import config
from tilegamelib.tile_factory import TileFactory
from util import TEST_GAME_CONTEXT


KEY_EVENT_QUEUE = [27]
TEST_DATA_PATH = config.BASE_PATH + '/../test/test_data/'
SAMPLE_MAP_FILE = TEST_DATA_PATH + 'sample.map'

TILE = TEST_DATA_PATH + 'test_tile.png'


@pytest.fixture
def image_filename():
    return TILE


@pytest.fixture
def tile_bitmap():
    return image.load(TILE).convert()


@pytest.fixture
def screen():
    return TEST_GAME_CONTEXT.screen


@pytest.fixture
def frame(screen):
    return Frame(screen, Rect(50, 50, 100, 100))


@pytest.fixture
def tile_factory():
    """Loads the default factory"""
    return TileFactory()


@pytest.fixture
def game():
    return TEST_GAME_CONTEXT.game


@pytest.fixture
def tile(tile_factory):
    return tile_factory.get('g')


@pytest.fixture
def sprite(game):
    return Sprite(game, 'g', (1, 1), speed=4)
