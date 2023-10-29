import pytest
from world import World
import numpy as np


@pytest.fixture
def world_init():
    world = World()
    world.board_size = 5
    world.chess_board = np.zeros((world.board_size, world.board_size, 4), dtype=bool)
    world.chess_board[0, :, 0] = True
    world.chess_board[:, 0, 3] = True
    world.chess_board[-1, :, 2] = True
    world.chess_board[:, -1, 1] = True
    world.max_step = (world.board_size + 1) // 2
    return world


@pytest.fixture
def world_1(world_init):
    # Gameboard_9
    world_init.p0_pos = np.asarray([2, 3])
    world_init.p1_pos = np.asarray([2, 1])
    world_init.turn = 0
    barriers = (
        (0, 0, 1),
        (0, 1, 1),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 1),
        (1, 3, 3),
        (2, 1, 2),
        (2, 2, 2),
        (2, 3, 1),
        (2, 4, 3),
        (3, 0, 1),
        (3, 1, 0),
        (3, 1, 2),
        (3, 1, 3),
        (3, 2, 0),
        (4, 0, 1),
        (4, 1, 0),
        (4, 1, 3),
    )
    for bar in barriers:
        world_init.chess_board[bar] = True
    return world_init


@pytest.fixture
def world_2(world_init):
    # Gameboard_9
    world_init.p0_pos = np.asarray([0, 2])
    world_init.p1_pos = np.asarray([2, 2])
    world_init.turn = 0
    barriers = (
        (0, 0, 1),
        (0, 1, 1),
        (0, 1, 3),
        (0, 2, 2),
        (0, 2, 3),
        (1, 2, 0),
        (1, 2, 1),
        (1, 3, 3),
        (2, 1, 2),
        (2, 2, 1),
        (2, 2, 2),
        (2, 3, 1),
        (2, 3, 3),
        (2, 4, 3),
        (3, 0, 1),
        (3, 1, 0),
        (3, 1, 2),
        (3, 1, 3),
        (3, 2, 0),
        (4, 0, 1),
        (4, 1, 0),
        (4, 1, 3),
    )
    for bar in barriers:
        world_init.chess_board[bar] = True
    return world_init
