"""Unit tests for Random and Plain Minimax baseline agents."""

import pytest
from connect4.core.board import Board, PLAYER_1, PLAYER_2
from connect4.agents.random_agent import RandomAgent
from connect4.agents.minimax_agent import MinimaxAgent


def test_random_agent_legal_moves():
    """Verify RandomAgent always selects legal columns."""
    board = Board()
    agent = RandomAgent("RandomTest", player=PLAYER_1, seed=123)

    for _ in range(20):
        move = agent.select_move(board)
        assert move in board.get_legal_moves()


def test_minimax_agent_wins_immediately():
    """Verify Minimax agent seizes an immediate horizontal win."""
    board = Board()
    # P1 has 3 pieces at (5, 0), (5, 1), (5, 2)
    board.grid[5, 0] = PLAYER_1
    board.grid[5, 1] = PLAYER_1
    board.grid[5, 2] = PLAYER_1
    board.current_player = PLAYER_1

    agent = MinimaxAgent(name="MinimaxP1", player=PLAYER_1, depth=3)
    best_move = agent.select_move(board)

    # Move must complete the four-in-a-row at column 3
    assert best_move == 3
    assert agent.nodes_expanded > 0


def test_minimax_agent_blocks_opponent_win():
    """Verify Minimax agent blocks an opponent's vertical win threat."""
    board = Board()
    # Opponent (P1) has 3 pieces stacked vertically in column 2
    board.grid[5, 2] = PLAYER_1
    board.grid[4, 2] = PLAYER_1
    board.grid[3, 2] = PLAYER_1

    # Now it is P2's turn
    board.current_player = PLAYER_2
    agent = MinimaxAgent(name="MinimaxP2", player=PLAYER_2, depth=3)
    best_move = agent.select_move(board)

    # Must block in column 2
    assert best_move == 2


def test_minimax_node_count_tracking():
    """Verify that plain Minimax tracks raw nodes expanded across depths."""
    board = Board()
    agent_d2 = MinimaxAgent("D2", player=PLAYER_1, depth=2)
    agent_d2.select_move(board)
    nodes_d2 = agent_d2.nodes_expanded

    agent_d3 = MinimaxAgent("D3", player=PLAYER_1, depth=3)
    agent_d3.select_move(board)
    nodes_d3 = agent_d3.nodes_expanded

    # Deeper search must expand significantly more nodes in plain Minimax
    assert nodes_d3 > nodes_d2
    assert nodes_d2 > 0
