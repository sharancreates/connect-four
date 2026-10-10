"""Instrumentation and Profiling Wrapper for Connect Four Benchmarks.

Provides real-time tracking of:
- Wall-clock decision time (using time.perf_counter)
- Memory usage and peak memory consumption (using tracemalloc)
- State / node expansions explored during search
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time
import tracemalloc


@dataclass
class MoveMetrics:
    """Metrics recorded for an individual move decision."""

    move: int
    player: int
    duration_sec: float
    nodes_expanded: int = 0
    peak_memory_bytes: int = 0
    current_memory_bytes: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        """Move computation time in milliseconds."""
        return self.duration_sec * 1000.0

    @property
    def peak_memory_kb(self) -> float:
        """Peak memory used during this move in kilobytes."""
        return self.peak_memory_bytes / 1024.0

    @property
    def peak_memory_mb(self) -> float:
        """Peak memory used during this move in megabytes."""
        return self.peak_memory_bytes / (1024.0 * 1024.0)


@dataclass
class GameMetrics:
    """Aggregated metrics collected across an entire game."""

    total_moves: int = 0
    total_time_sec: float = 0.0
    total_nodes_expanded: int = 0
    peak_memory_bytes: int = 0
    moves_history: List[MoveMetrics] = field(default_factory=list)

    def record_move(self, move_metric: MoveMetrics) -> None:
        """Append a move metric to history and update running aggregates."""
        self.moves_history.append(move_metric)
        self.total_moves += 1
        self.total_time_sec += move_metric.duration_sec
        self.total_nodes_expanded += move_metric.nodes_expanded
        if move_metric.peak_memory_bytes > self.peak_memory_bytes:
            self.peak_memory_bytes = move_metric.peak_memory_bytes

    @property
    def avg_time_per_move_ms(self) -> float:
        """Average decision time per move in milliseconds."""
        if self.total_moves == 0:
            return 0.0
        return (self.total_time_sec / self.total_moves) * 1000.0

    @property
    def avg_nodes_per_move(self) -> float:
        """Average nodes expanded per move."""
        if self.total_moves == 0:
            return 0.0
        return self.total_nodes_expanded / self.total_moves

    @property
    def peak_memory_kb(self) -> float:
        """Maximum peak memory observed in KB."""
        return self.peak_memory_bytes / 1024.0


class MetricsTracker:
    """Context manager and instrumentation wrapper for profiling agent decisions."""

    def __init__(self, track_memory: bool = True):
        """Initialize tracker.

        Args:
            track_memory: Whether to enable tracemalloc for memory measurements.
        """
        self.track_memory: bool = track_memory
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration_sec: float = 0.0
        self.peak_memory_bytes: int = 0
        self.current_memory_bytes: int = 0

    def __enter__(self) -> MetricsTracker:
        """Start performance profiling."""
        if self.track_memory:
            if not tracemalloc.is_tracing():
                tracemalloc.start()
            tracemalloc.reset_peak()
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop profiling and record metrics."""
        self.end_time = time.perf_counter()
        self.duration_sec = self.end_time - self.start_time
        if self.track_memory:
            current, peak = tracemalloc.get_traced_memory()
            self.current_memory_bytes = current
            self.peak_memory_bytes = peak

    @staticmethod
    def profile_agent_move(
        agent: Any,
        board: Any,
        track_memory: bool = True,
    ) -> tuple[int, MoveMetrics]:
        """Profile an agent's select_move invocation.

        Args:
            agent: The game-playing agent instance.
            board: Current Board state.
            track_memory: Whether to measure memory usage via tracemalloc.

        Returns:
            Tuple of (chosen_column, MoveMetrics).
        """
        # Reset agent node counter if it supports it
        initial_nodes = getattr(agent, "nodes_expanded", 0)

        tracker = MetricsTracker(track_memory=track_memory)
        with tracker:
            move = agent.select_move(board)

        final_nodes = getattr(agent, "nodes_expanded", 0)
        nodes_expanded = max(0, final_nodes - initial_nodes)

        metric = MoveMetrics(
            move=move,
            player=board.current_player,
            duration_sec=tracker.duration_sec,
            nodes_expanded=nodes_expanded,
            peak_memory_bytes=tracker.peak_memory_bytes,
            current_memory_bytes=tracker.current_memory_bytes,
        )
        return move, metric


def format_metrics(metric: MoveMetrics) -> str:
    """Format a MoveMetrics record into a concise summary string."""
    parts = [
        f"Time: {metric.duration_ms:.2f} ms",
        f"Nodes: {metric.nodes_expanded:,}",
    ]
    if metric.peak_memory_bytes > 0:
        parts.append(f"Peak Mem: {metric.peak_memory_kb:.2f} KB")
    return " | ".join(parts)
