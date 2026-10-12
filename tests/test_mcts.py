"""Unit and behavioral tests for Monte Carlo Tree Search (MCTS) Agent."""

import time
import pytest
from connect4.core.board import Board, PLAYER_1, PLAYER_2
from connect4.agents.mcts_agent import MCTSAgent


def test_mcts_legal_move():
    """Verify MCTS always returns a legal, available column."""
    board = Board()
    agent = MCTSAgent("MCTS_Test", player=PLAYER_1, simulations=50, seed=42)
    move = agent.select_move(board)
    assert move in board.get_legal_moves()


def test_mcts_immediate_win():
    """Verify MCTS seizes an immediate winning opportunity."""
    board = Board()
    # P1 has 3 horizontally aligned pieces at (5, 0), (5, 1), (5, 2)
    board.grid[5, 0] = PLAYER_1
    board.grid[5, 1] = PLAYER_1
    board.grid[5, 2] = PLAYER_1
    board.current_player = PLAYER_1

    agent = MCTSAgent("MCTS_Win", player=PLAYER_1, simulations=100, seed=42)
    move = agent.select_move(board)

    # Move must complete the 4-in-a-row at column 3
    assert move == 3


def test_mcts_blocks_immediate_win():
    """Verify MCTS defends against opponent's immediate winning threat."""
    board = Board()
    # Opponent (P1) has 3 pieces stacked vertically in column 4
    board.grid[5, 4] = PLAYER_1
    board.grid[4, 4] = PLAYER_1
    board.grid[3, 4] = PLAYER_1

    # It is P2's turn
    board.current_player = PLAYER_2
    agent = MCTSAgent("MCTS_Block", player=PLAYER_2, simulations=100, seed=42)
    move = agent.select_move(board)

    # Must block in column 4
    assert move == 4


def test_mcts_fixed_simulation_budget():
    """Verify MCTS obeys fixed simulation count."""
    board = Board()
    sim_count = 75
    agent = MCTSAgent("MCTS_FixedSim", player=PLAYER_1, simulations=sim_count, seed=42)
    _ = agent.select_move(board)

    # Each simulation rollout increments nodes_expanded
    assert agent.nodes_expanded >= sim_count


def test_mcts_time_limit_budget():
    """Verify MCTS terminates within the designated wall-clock time limit."""
    board = Board()
    time_limit = 0.05  # 50 ms
    agent = MCTSAgent("MCTS_Timed", player=PLAYER_1, time_limit=time_limit, seed=42)

    start = time.perf_counter()
    _ = agent.select_move(board)
    elapsed = time.perf_counter() - start

    # Should finish around 50ms (giving modest buffer for final rollout completion)
    assert elapsed < 0.25
    assert agent.nodes_expanded > 0


def test_mcts_seed_determinism():
    """Verify identical seeds produce identical decisions given fixed simulations."""
    board = Board()
    agent1 = MCTSAgent("MCTS_1", player=PLAYER_1, simulations=100, seed=999)
    agent2 = MCTSAgent("MCTS_2", player=PLAYER_1, simulations=100, seed=999)

    move1 = agent1.select_move(board.copy())
    move2 = agent2.select_move(board.copy())

    assert move1 == move2
