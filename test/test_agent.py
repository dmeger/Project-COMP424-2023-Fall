import pytest
import os
import random
import numpy as np
from world import World
from agents import *
from copy import deepcopy


@pytest.mark.parametrize("board_size", [5, 6, 7])
@pytest.mark.parametrize("agent", ["random_agent", "student_agent"])
def test_step(board_size, agent):
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    world = World(
        player_1=agent,
        player_2="random_agent",
        board_size=board_size,
        display_ui=False,
    )
    assert world.turn == 0
    cur_player, cur_pos, adv_pos = world.get_current_player()
    next_pos, dir = cur_player.step(
        deepcopy(world.chess_board),
        tuple(cur_pos),
        tuple(adv_pos),
        world.max_step,
    )
    assert type(next_pos) == tuple
    assert len(next_pos) == 2
    assert type(dir) == int
    assert dir in [0, 1, 2, 3]
    next_pos = np.asarray(next_pos, dtype=cur_pos.dtype)
    assert world.check_boundary(next_pos)
