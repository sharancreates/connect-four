"""Heuristic evaluation for Connect Four (used when the search reaches its depth limit)."""

from connect4.core.board import ROWS, COLS, EMPTY

# weights, easy to tune later
CENTER_WEIGHT = 3
THREE_WEIGHT = 5
TWO_WEIGHT = 2
OPP_THREE_WEIGHT = -6
OPP_TWO_WEIGHT = -2


def make_windows():
    # every group of 4 cells in a line, stored as (row, col) positions
    windows = []

    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            windows.append([(r, c + i) for i in range(4)])

    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            windows.append([(r + i, c) for i in range(4)])

    # both diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            windows.append([(r + i, c + i) for i in range(4)])
            windows.append([(r + 3 - i, c + i) for i in range(4)])

    return windows


WINDOWS = make_windows()  # 69 windows in total


def score_window(values, player):
    mine = values.count(player)
    theirs = values.count(-player)
    empty = values.count(EMPTY)

    # a window with both players' discs can never become 4 in a row, so it scores 0
    if mine == 3 and empty == 1:
        return THREE_WEIGHT
    if mine == 2 and empty == 2:
        return TWO_WEIGHT
    if theirs == 3 and empty == 1:
        return OPP_THREE_WEIGHT
    if theirs == 2 and empty == 2:
        return OPP_TWO_WEIGHT
    return 0


def evaluate_board(board, player):
    # positive = good for player, negative = good for opponent
    rows = board.grid.tolist()
    score = 0

    # center column control
    center = COLS // 2
    for r in range(ROWS):
        if rows[r][center] == player:
            score += CENTER_WEIGHT
        elif rows[r][center] == -player:
            score -= CENTER_WEIGHT

    # open twos and threes (threat counting)
    for window in WINDOWS:
        values = [rows[r][c] for r, c in window]
        score += score_window(values, player)

    return float(score)
