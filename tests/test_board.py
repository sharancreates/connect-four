"""Unit tests for Connect Four Board representation and rule enforcement."""

import pytest
import numpy as np
from connect4.core.board import Board, ROWS, COLS, EMPTY, PLAYER_1, PLAYER_2


def test_initial_board_state():
    """Verify fresh board properties."""
    board = Board()
    assert board.grid.shape == (ROWS, COLS)
    assert (board.grid == EMPTY).all()
    assert board.current_player == PLAYER_1
    assert board.get_legal_moves() == list(range(COLS))
    assert not board.is_terminal()
    assert board.get_winner() is None


def test_make_move_gravity():
    """Verify discs fall to bottom and stack upwards."""
    board = Board()
    row0 = board.make_move(3)
    assert row0 == 5  # Bottom row
    assert board.grid[5, 3] == PLAYER_1
    assert board.current_player == PLAYER_2

    row1 = board.make_move(3)
    assert row1 == 4  # Stacks on top
    assert board.grid[4, 3] == PLAYER_2
    assert board.current_player == PLAYER_1


def test_illegal_move_full_column():
    """Verify that playing into a full column raises ValueError."""
    board = Board()
    for _ in range(ROWS):
        board.make_move(0)
    assert not board.is_valid_move(0)
    assert 0 not in board.get_legal_moves()
    with pytest.raises(ValueError):
        board.make_move(0)


def test_undo_move():
    """Verify move undo restores previous state and turn."""
    board = Board()
    board.make_move(2)
    assert board.grid[5, 2] == PLAYER_1
    assert board.current_player == PLAYER_2

    board.undo_move(2)
    assert board.grid[5, 2] == EMPTY
    assert board.current_player == PLAYER_1
    assert not board.is_terminal()


def test_horizontal_win():
    """Verify detection of 4-in-a-row horizontally."""
    board = Board()
    # P1 plays 0, 1, 2, 3; P2 plays in column 6
    moves_p1 = [0, 1, 2, 3]
    moves_p2 = [6, 6, 6]

    for p1_col, p2_col in zip(moves_p1[:3], moves_p2):
        board.make_move(p1_col)
        board.make_move(p2_col)

    # Final winning move for P1
    board.make_move(moves_p1[3])

    assert board.is_terminal()
    assert board.get_winner() == PLAYER_1


def test_vertical_win():
    """Verify detection of 4-in-a-row vertically."""
    board = Board()
    # P1 plays col 2; P2 plays col 3
    for _ in range(3):
        board.make_move(2)
        board.make_move(3)

    # P1 plays 4th in col 2
    board.make_move(2)

    assert board.is_terminal()
    assert board.get_winner() == PLAYER_1


def test_positive_diagonal_win():
    """Verify detection of positive diagonal (bottom-left to top-right)."""
    board = Board()
    # Build staircase in columns 0, 1, 2, 3 so P1 connects (5,0), (4,1), (3,2), (2,3)
    # Col 0: P1 at row 5
    # Col 1: P2 at row 5, P1 at row 4
    # Col 2: P2 at row 5, P2 at row 4, P1 at row 3
    # Col 3: P2 at row 5, P2 at row 4, P2 at row 3, P1 at row 2
    sequence = [
        0, 1,  # P1 at (5,0), P2 at (5,1)
        1, 2,  # P1 at (4,1), P2 at (5,2)
        2, 3,  # P1 at (4,2), P2 at (5,3)
        3, 2,  # P1 at (4,3), P2 at (3,2) [P1 now needs (3,2)? Wait, let's setup explicit grid]
    ]
    # Let's verify via explicit setup:
    grid = np.zeros((ROWS, COLS), dtype=np.int8)
    grid[5, 0] = PLAYER_1
    grid[4, 1] = PLAYER_1
    grid[3, 2] = PLAYER_1
    grid[2, 3] = PLAYER_1

    test_board = Board(grid)
    assert test_board.check_win(PLAYER_1)
    assert test_board.is_terminal()
    assert test_board.get_winner() == PLAYER_1


def test_negative_diagonal_win():
    """Verify detection of negative diagonal (top-left to bottom-right)."""
    grid = np.zeros((ROWS, COLS), dtype=np.int8)
    grid[2, 0] = PLAYER_2
    grid[3, 1] = PLAYER_2
    grid[4, 2] = PLAYER_2
    grid[5, 3] = PLAYER_2

    test_board = Board(grid)
    assert test_board.check_win(PLAYER_2)
    assert test_board.is_terminal()
    assert test_board.get_winner() == PLAYER_2


def test_draw_condition():
    """Verify game identifies full board without 4-in-a-row as draw."""
    # Pattern with no 4-in-a-row:
    # Alternate columns with pairs:
    # 1 1 -1 -1 1 1 -1
    pattern = np.array([
        [ 1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1],
        [ 1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1],
        [ 1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1],
    ], dtype=np.int8)

    draw_board = Board(pattern)
    assert not draw_board.check_win(PLAYER_1)
    assert not draw_board.check_win(PLAYER_2)
    assert draw_board.is_full()
    assert draw_board.is_terminal()
    assert draw_board.get_winner() is None


def test_get_winning_coordinates():
    """Verify get_winning_coordinates correctly locates horizontal, vertical, and diagonal lines."""
    empty_board = Board()
    assert empty_board.get_winning_coordinates() is None

    # 1. Horizontal win in row 5
    h_board = Board()
    for col in range(3):
        h_board.make_move(col)      # P1
        h_board.make_move(col + 4)  # P2
    h_board.make_move(3)            # P1 wins: row 5, cols 0..3
    assert h_board.get_winning_coordinates() == [(5, 0), (5, 1), (5, 2), (5, 3)]

    # 2. Vertical win in col 2
    v_board = Board()
    for _ in range(3):
        v_board.make_move(2)  # P1
        v_board.make_move(4)  # P2
    v_board.make_move(2)      # P1 wins: rows 5, 4, 3, 2 in col 2
    assert v_board.get_winning_coordinates() == [(2, 2), (3, 2), (4, 2), (5, 2)]

    # 3. Positive diagonal win
    pos_grid = np.zeros((ROWS, COLS), dtype=np.int8)
    pos_grid[5, 0] = PLAYER_1
    pos_grid[4, 1] = PLAYER_1
    pos_grid[3, 2] = PLAYER_1
    pos_grid[2, 3] = PLAYER_1
    pos_board = Board(pos_grid)
    assert pos_board.get_winning_coordinates() == [(5, 0), (4, 1), (3, 2), (2, 3)]

    # 4. Negative diagonal win
    neg_grid = np.zeros((ROWS, COLS), dtype=np.int8)
    neg_grid[2, 0] = PLAYER_2
    neg_grid[3, 1] = PLAYER_2
    neg_grid[4, 2] = PLAYER_2
    neg_grid[5, 3] = PLAYER_2
    neg_board = Board(neg_grid)
    assert neg_board.get_winning_coordinates() == [(2, 0), (3, 1), (4, 2), (5, 3)]
