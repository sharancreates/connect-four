"""Unit tests for Alpha-Beta Pruning Agent."""

import pytest
from connect4.core.board import Board, PLAYER_1, PLAYER_2
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.alphabeta_agent import AlphaBetaAgent


def test_alphabeta_vs_minimax_same_moves():
    """AlphaBetaAgent and MinimaxAgent choose the same move on at least 3 different positions at depth 3."""
    # Position 1: Empty board
    pos1 = Board()

    # Position 2: Early game opening moves
    pos2 = Board()
    for col in [3, 3, 2, 4]:
        pos2.make_move(col)

    # Position 3: Midgame tactical position
    pos3 = Board()
    for col in [3, 2, 4, 3, 2, 1, 0]:
        pos3.make_move(col)

    positions = [pos1, pos2, pos3]

    for i, base_board in enumerate(positions, start=1):
        b_mm = base_board.copy()
        b_ab = base_board.copy()

        agent_mm = MinimaxAgent(name="Minimax", player=base_board.current_player, depth=3)
        agent_ab = AlphaBetaAgent(name="AlphaBeta", player=base_board.current_player, depth=3)

        move_mm = agent_mm.select_move(b_mm)
        move_ab = agent_ab.select_move(b_ab)

        assert move_ab == move_mm, f"Move mismatch on position {i}: Minimax={move_mm}, AlphaBeta={move_ab}"


def test_alphabeta_expands_fewer_nodes_than_minimax():
    """AlphaBetaAgent expands fewer nodes than MinimaxAgent at depth 4 from the empty board."""
    board_mm = Board()
    board_ab = Board()

    agent_mm = MinimaxAgent(name="Minimax", player=PLAYER_1, depth=4)
    agent_ab = AlphaBetaAgent(name="AlphaBeta", player=PLAYER_1, depth=4)

    agent_mm.select_move(board_mm)
    agent_ab.select_move(board_ab)

    assert agent_ab.nodes_expanded < agent_mm.nodes_expanded, (
        f"AlphaBeta expanded {agent_ab.nodes_expanded} nodes, "
        f"expected fewer than Minimax's {agent_mm.nodes_expanded}"
    )


def test_alphabeta_takes_immediate_win():
    """AlphaBetaAgent takes an immediate winning move when one exists."""
    board = Board()
    # P1 has 3 pieces horizontally at row 5, cols 0, 1, 2
    board.grid[5, 0] = PLAYER_1
    board.grid[5, 1] = PLAYER_1
    board.grid[5, 2] = PLAYER_1
    board.current_player = PLAYER_1

    agent = AlphaBetaAgent(name="AlphaBetaP1", player=PLAYER_1, depth=3)
    best_move = agent.select_move(board)

    # Move must complete the horizontal win at column 3
    assert best_move == 3
    assert agent.nodes_expanded > 0


def test_alphabeta_blocks_opponent_immediate_win():
    """AlphaBetaAgent blocks the opponent's immediate win when it has no win of its own."""
    board = Board()
    # Opponent (P1) has 3 pieces stacked vertically in column 2
    board.grid[5, 2] = PLAYER_1
    board.grid[4, 2] = PLAYER_1
    board.grid[3, 2] = PLAYER_1

    # Current player is P2
    board.current_player = PLAYER_2

    agent = AlphaBetaAgent(name="AlphaBetaP2", player=PLAYER_2, depth=3)
    best_move = agent.select_move(board)

    # Must block in column 2
    assert best_move == 2
