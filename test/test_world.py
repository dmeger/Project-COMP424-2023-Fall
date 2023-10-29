import pytest


@pytest.mark.parametrize("end_pos", [(0, 4), (0, 0), (2, 3), (3, 0), (4, 4)])
def test_check_boundary_pass(world_1, end_pos):
    assert world_1.check_boundary(end_pos)


@pytest.mark.parametrize("end_pos", [(-1, 4), (0, 5), (4, 6), (-1, -1), (6, 0)])
def test_check_boundary_fail(world_1, end_pos):
    assert not world_1.check_boundary(end_pos)


@pytest.mark.parametrize(
    "end_pos, dir", [((1, 1), 0), ((0, 2), 2), ((0, 4), 3), ((3, 1), 1), ((4, 2), 0)]
)
def test_check_valid_step_pass(world_1, end_pos, dir):
    start_pos = world_1.p0_pos if not world_1.turn else world_1.p1_pos
    assert world_1.check_valid_step(start_pos, end_pos, dir)


@pytest.mark.parametrize(
    "end_pos, dir",
    [((2, 0), 0), ((2, 1), 0), ((3, 1), 2), ((0, 3), 0), ((4, 1), 1), ((0, 1), 2)],
)
def test_check_valid_step_fail(world_1, end_pos, dir):
    start_pos = world_1.p0_pos if not world_1.turn else world_1.p1_pos
    assert not world_1.check_valid_step(start_pos, end_pos, dir)


def test_check_endgame_world_1(world_1):
    is_end, p0_score, p1_score = world_1.check_endgame()
    assert not is_end
    assert p0_score == 25
    assert p1_score == 25


def test_check_endgame_world_2(world_2):
    is_end, p0_score, p1_score = world_2.check_endgame()
    assert is_end
    assert p0_score == 15
    assert p1_score == 10
