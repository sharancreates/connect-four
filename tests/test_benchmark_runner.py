"""Integration tests for the automated multi-game benchmark runner."""

import pytest
from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.agents.random_agent import RandomAgent
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.benchmark.runner import BenchmarkRunner, MatchStats


def test_benchmark_runner_series_execution():
    """Verify running an automated multi-game series."""
    agent1 = RandomAgent("Random_1", player=PLAYER_1, seed=10)
    agent2 = MinimaxAgent("Minimax_2", player=PLAYER_2, depth=2)

    runner = BenchmarkRunner(verbose=False)
    num_games = 4
    stats: MatchStats = runner.run_series(agent1, agent2, num_games=num_games)

    assert stats.total_games == num_games
    assert len(stats.games) == num_games
    assert stats.agent1_wins + stats.agent2_wins + stats.draws == num_games

    # Both agents must have recorded moves, decision times, and node expansions
    assert stats.agent1_total_moves > 0
    assert stats.agent2_total_moves > 0
    assert stats.agent2_total_nodes > 0
    assert stats.agent1_avg_time_ms >= 0.0
    assert stats.agent2_avg_time_ms > 0.0

    report = runner.format_report(stats)
    assert "BENCHMARK MATCH EVALUATION REPORT" in report
    assert "Total Games Played: 4" in report
    assert stats.agent1_name in report
    assert stats.agent2_name in report


def test_benchmark_runner_alternates_first_mover():
    """Verify first-player status alternates across consecutive games."""
    agent1 = RandomAgent("AgentA", player=PLAYER_1, seed=1)
    agent2 = RandomAgent("AgentB", player=PLAYER_2, seed=2)

    runner = BenchmarkRunner(verbose=False)
    stats = runner.run_series(agent1, agent2, num_games=4)

    assert stats.games[0].player1_name == "AgentA"
    assert stats.games[1].player1_name == "AgentB"
    assert stats.games[2].player1_name == "AgentA"
    assert stats.games[3].player1_name == "AgentB"
