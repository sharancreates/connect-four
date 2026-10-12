from connect4.core.board import Board
from connect4.agents.heuristic import evaluate_board, WINDOWS


def test_window_count():
    # 24 horizontal + 21 vertical + 24 diagonal
    assert len(WINDOWS) == 69


def test_empty_board_scores_zero():
    assert evaluate_board(Board(), 1) == 0


def test_center_disc_better_than_edge():
    center = Board()
    center.grid[5, 3] = 1
    edge = Board()
    edge.grid[5, 0] = 1
    assert evaluate_board(center, 1) > evaluate_board(edge, 1)


def test_perspective_flips_sign():
    b = Board()
    b.grid[5, 3] = 1
    assert evaluate_board(b, 1) == -evaluate_board(b, -1)


def test_open_three_beats_open_two():
    two = Board()
    two.grid[5, 1:3] = 1
    three = Board()
    three.grid[5, 0:3] = 1
    assert evaluate_board(three, 1) > evaluate_board(two, 1)


def test_opponent_three_is_negative():
    b = Board()
    b.grid[5, 0:3] = -1
    assert evaluate_board(b, 1) < 0


def test_blocked_three_worth_less_than_open_three():
    open_three = Board()
    open_three.grid[5, 0:3] = 1
    blocked = Board()
    blocked.grid[5, 0:3] = 1
    blocked.grid[5, 3] = -1
    assert evaluate_board(open_three, 1) > evaluate_board(blocked, 1)


def test_vertical_three_counts():
    b = Board()
    b.grid[3:6, 0] = 1
    assert evaluate_board(b, 1) > 0


def test_diagonal_three_counts():
    b = Board()
    b.grid[5, 0] = 1
    b.grid[4, 1] = 1
    b.grid[3, 2] = 1
    assert evaluate_board(b, 1) > 0
