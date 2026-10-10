"""Unit tests for the benchmarking instrumentation wrapper."""

import time
from connect4.core.board import Board, PLAYER_1
from connect4.agents.random_agent import RandomAgent
from connect4.benchmark.instrumentation import (
    MetricsTracker,
    MoveMetrics,
    GameMetrics,
    format_metrics,
)


def test_metrics_tracker_context():
    """Verify MetricsTracker captures wall-clock time and memory."""
    tracker = MetricsTracker(track_memory=True)
    with tracker:
        # Perform memory and compute workload
        _ = [i ** 2 for i in range(10000)]
        time.sleep(0.01)

    assert tracker.duration_sec >= 0.009
    assert tracker.duration_sec < 1.0
    assert tracker.peak_memory_bytes >= 0


def test_profile_agent_move():
    """Verify profiling an agent's move produces valid MoveMetrics."""
    board = Board()
    agent = RandomAgent(name="TestRandom", player=PLAYER_1, seed=42)

    move, metric = MetricsTracker.profile_agent_move(agent, board, track_memory=True)
    assert 0 <= move < 7
    assert metric.move == move
    assert metric.player == PLAYER_1
    assert metric.duration_sec >= 0.0
    assert metric.nodes_expanded >= 1
    assert metric.peak_memory_bytes >= 0

    summary_str = format_metrics(metric)
    assert "Time:" in summary_str
    assert "Nodes:" in summary_str


def test_game_metrics_aggregation():
    """Verify aggregation across multiple moves in a game."""
    game_metrics = GameMetrics()
    m1 = MoveMetrics(move=3, player=1, duration_sec=0.01, nodes_expanded=50, peak_memory_bytes=1024)
    m2 = MoveMetrics(move=4, player=-1, duration_sec=0.02, nodes_expanded=100, peak_memory_bytes=2048)

    game_metrics.record_move(m1)
    game_metrics.record_move(m2)

    assert game_metrics.total_moves == 2
    assert abs(game_metrics.total_time_sec - 0.03) < 1e-6
    assert game_metrics.total_nodes_expanded == 150
    assert game_metrics.avg_nodes_per_move == 75.0
    assert game_metrics.avg_time_per_move_ms == 15.0
    assert game_metrics.peak_memory_bytes == 2048
    assert game_metrics.peak_memory_kb == 2.0
