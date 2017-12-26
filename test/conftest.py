
from tilegamelib.config import config
from tilegamelib.tile_factory import TileFactory
from util import TEST_GAME_CONTEXT
import pytest


KEY_EVENT_QUEUE = [27]
TEST_DATA_PATH = config.BASE_PATH + '/../test/test_data/'
SAMPLE_MAP_FILE = TEST_DATA_PATH + 'sample.map'

TILE = TEST_DATA_PATH + 'test_tile.png'


@pytest.fixture
def screen():
    return TEST_GAME_CONTEXT.screen


@pytest.fixture
def tile_factory():
    """Loads the default factory"""
    return TileFactory()


@pytest.fixture
def game():
    return TEST_GAME_CONTEXT.game
