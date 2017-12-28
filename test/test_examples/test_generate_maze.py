
from examples.generate_maze import (create_grid_string, create_maze, get_all_dot_positions,
                                    get_neighbors)


def test_create_grid():
    dots = set(((1, 1), (1, 2), (1, 3), (2, 2), (3, 1), (3, 2), (3, 3)))
    grid = create_grid_string(dots, 5, 5)
    assert grid == """#####
#*#*#
#***#
#*#*#
#####"""


def test_create_empty_grid():
    positions = get_all_dot_positions(5, 5)
    grid = create_grid_string(positions, 5, 5)
    assert grid == """#####
#***#
#***#
#***#
#####"""


def test_neighbors():
    neighbors = get_neighbors(3, 2)
    grid = create_grid_string(neighbors, 5, 5)
    assert grid == """#####
##***
##*#*
##***
#####"""


def test_create_maze():
    maze = create_maze(12, 7)
    assert len(maze) == 13 * 7 - 1
    for row in maze.strip().split('\n'):
        assert len(row) == 12
