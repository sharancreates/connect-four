import time

from connect4.core.board import Board
from connect4.agents.iterative_agent import IterativeAlphaBetaAgent


def test_returns_legal_move_within_time():
    board = Board()
    agent = IterativeAlphaBetaAgent(player=1, time_limit=0.3)

    start = time.perf_counter()
    move = agent.select_move(board)
    elapsed = time.perf_counter() - start

    assert move in board.get_legal_moves()
    assert elapsed < 0.3 + 0.5  # small margin for the last node


def test_depth_reached_is_recorded():
    agent = IterativeAlphaBetaAgent(player=1, time_limit=0.3)
    agent.select_move(Board())
    assert agent.depth_reached >= 1


def test_takes_immediate_win():
    board = Board()
    board.grid[5, 0:3] = 1
    board.grid[4, 0:2] = -1
    board.current_player = 1

    agent = IterativeAlphaBetaAgent(player=1, time_limit=0.3)
    assert agent.select_move(board) == 3


def test_board_is_unchanged_after_search():
    board = Board()
    board.make_move(3)
    before = board.grid.copy()

    agent = IterativeAlphaBetaAgent(player=-1, time_limit=0.2)
    agent.select_move(board)

    assert (board.grid == before).all()
