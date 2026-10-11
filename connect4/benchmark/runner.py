"""Multi-Game Automated Benchmark Runner.

Executes head-to-head series between two agents across N games,
alternating first-player privileges to balance first-mover advantage,
and collects aggregate win rates, latencies, node expansions, and memory usage.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import time
from connect4.core.board import Board, PLAYER_1, PLAYER_2
from connect4.agents.base import Agent
from connect4.benchmark.instrumentation import MetricsTracker, MoveMetrics


@dataclass
class SingleGameRecord:
    """Record of an individual game outcome and telemetry."""

    game_number: int
    player1_name: str
    player2_name: str
    winner_name: Optional[str]  # None if draw
    total_moves: int
    duration_sec: float
    p1_moves: int
    p2_moves: int
    p1_time_ms: float
    p2_time_ms: float
    p1_nodes: int
    p2_nodes: int


@dataclass
class MatchStats:
    """Aggregated statistics across a multi-game benchmark series."""

    agent1_name: str
    agent2_name: str
    total_games: int = 0
    agent1_wins: int = 0
    agent2_wins: int = 0
    draws: int = 0

    # Aggregate telemetry for Agent 1
    agent1_total_moves: int = 0
    agent1_total_time_ms: float = 0.0
    agent1_total_nodes: int = 0
    agent1_peak_memory_kb: float = 0.0

    # Aggregate telemetry for Agent 2
    agent2_total_moves: int = 0
    agent2_total_time_ms: float = 0.0
    agent2_total_nodes: int = 0
    agent2_peak_memory_kb: float = 0.0

    games: List[SingleGameRecord] = field(default_factory=list)

    @property
    def agent1_win_rate(self) -> float:
        return (self.agent1_wins / self.total_games * 100.0) if self.total_games else 0.0

    @property
    def agent2_win_rate(self) -> float:
        return (self.agent2_wins / self.total_games * 100.0) if self.total_games else 0.0

    @property
    def draw_rate(self) -> float:
        return (self.draws / self.total_games * 100.0) if self.total_games else 0.0

    @property
    def agent1_avg_time_ms(self) -> float:
        return (self.agent1_total_time_ms / self.agent1_total_moves) if self.agent1_total_moves else 0.0

    @property
    def agent2_avg_time_ms(self) -> float:
        return (self.agent2_total_time_ms / self.agent2_total_moves) if self.agent2_total_moves else 0.0

    @property
    def agent1_avg_nodes(self) -> float:
        return (self.agent1_total_nodes / self.agent1_total_moves) if self.agent1_total_moves else 0.0

    @property
    def agent2_avg_nodes(self) -> float:
        return (self.agent2_total_nodes / self.agent2_total_moves) if self.agent2_total_moves else 0.0


class BenchmarkRunner:
    """Orchestrator for automated competitive evaluations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def run_series(
        self,
        agent_a: Agent,
        agent_b: Agent,
        num_games: int = 10,
        track_memory: bool = True,
    ) -> MatchStats:
        """Run an N-game series alternating starting player."""
        stats = MatchStats(agent1_name=agent_a.name, agent2_name=agent_b.name)

        for game_idx in range(1, num_games + 1):
            # Alternate who plays as Player 1 (Red / first mover)
            if game_idx % 2 == 1:
                p1_agent, p2_agent = agent_a, agent_b
                p1_is_a = True
            else:
                p1_agent, p2_agent = agent_b, agent_a
                p1_is_a = False

            # Set tokens for this game
            p1_agent.player = PLAYER_1
            p2_agent.player = PLAYER_2

            board = Board()
            game_start = time.perf_counter()

            p1_time, p2_time = 0.0, 0.0
            p1_nodes, p2_nodes = 0, 0
            p1_moves, p2_moves = 0, 0
            p1_mem, p2_mem = 0.0, 0.0

            while not board.is_terminal():
                curr_player = board.current_player
                active_agent = p1_agent if curr_player == PLAYER_1 else p2_agent

                move, metric = MetricsTracker.profile_agent_move(
                    active_agent,
                    board,
                    track_memory=track_memory,
                )
                board.make_move(move)

                if curr_player == PLAYER_1:
                    p1_moves += 1
                    p1_time += metric.duration_ms
                    p1_nodes += metric.nodes_expanded
                    p1_mem = max(p1_mem, metric.peak_memory_kb)
                else:
                    p2_moves += 1
                    p2_time += metric.duration_ms
                    p2_nodes += metric.nodes_expanded
                    p2_mem = max(p2_mem, metric.peak_memory_kb)

            game_duration = time.perf_counter() - game_start
            winner_token = board.get_winner()

            if winner_token == PLAYER_1:
                winner_agent = p1_agent.name
                if p1_is_a:
                    stats.agent1_wins += 1
                else:
                    stats.agent2_wins += 1
            elif winner_token == PLAYER_2:
                winner_agent = p2_agent.name
                if p1_is_a:
                    stats.agent2_wins += 1
                else:
                    stats.agent1_wins += 1
            else:
                winner_agent = None
                stats.draws += 1

            stats.total_games += 1

            # Update Agent A and Agent B aggregates
            if p1_is_a:
                stats.agent1_total_moves += p1_moves
                stats.agent1_total_time_ms += p1_time
                stats.agent1_total_nodes += p1_nodes
                stats.agent1_peak_memory_kb = max(stats.agent1_peak_memory_kb, p1_mem)

                stats.agent2_total_moves += p2_moves
                stats.agent2_total_time_ms += p2_time
                stats.agent2_total_nodes += p2_nodes
                stats.agent2_peak_memory_kb = max(stats.agent2_peak_memory_kb, p2_mem)
            else:
                stats.agent1_total_moves += p2_moves
                stats.agent1_total_time_ms += p2_time
                stats.agent1_total_nodes += p2_nodes
                stats.agent1_peak_memory_kb = max(stats.agent1_peak_memory_kb, p2_mem)

                stats.agent2_total_moves += p1_moves
                stats.agent2_total_time_ms += p1_time
                stats.agent2_total_nodes += p1_nodes
                stats.agent2_peak_memory_kb = max(stats.agent2_peak_memory_kb, p1_mem)

            record = SingleGameRecord(
                game_number=game_idx,
                player1_name=p1_agent.name,
                player2_name=p2_agent.name,
                winner_name=winner_agent,
                total_moves=p1_moves + p2_moves,
                duration_sec=game_duration,
                p1_moves=p1_moves,
                p2_moves=p2_moves,
                p1_time_ms=p1_time,
                p2_time_ms=p2_time,
                p1_nodes=p1_nodes,
                p2_nodes=p2_nodes,
            )
            stats.games.append(record)

            if self.verbose:
                win_str = winner_agent if winner_agent else "Draw"
                print(f"Game {game_idx:02d}/{num_games:02d}: Winner={win_str} ({p1_moves+p2_moves} moves in {game_duration*1000:.1f}ms)")

        return stats

    @staticmethod
    def format_report(stats: MatchStats) -> str:
        """Render a formatted comparison table for the benchmark series."""
        lines = []
        lines.append("\n" + "=" * 65)
        lines.append("            BENCHMARK MATCH EVALUATION REPORT")
        lines.append("=" * 65)
        lines.append(f" Total Games Played: {stats.total_games}")
        lines.append("-" * 65)
        lines.append(f"{'Metric':<25} | {stats.agent1_name:<16} | {stats.agent2_name:<16}")
        lines.append("-" * 65)
        lines.append(f"{'Wins (Win Rate)':<25} | {stats.agent1_wins} ({stats.agent1_win_rate:.1f}%)" + f"{'':<6} | {stats.agent2_wins} ({stats.agent2_win_rate:.1f}%)")
        lines.append(f"{'Draws (Draw Rate)':<25} | {stats.draws} ({stats.draw_rate:.1f}%)")
        lines.append(f"{'Total Moves Played':<25} | {stats.agent1_total_moves:<16} | {stats.agent2_total_moves:<16}")
        lines.append(f"{'Avg Decision Time':<25} | {stats.agent1_avg_time_ms:.2f} ms{'':<8} | {stats.agent2_avg_time_ms:.2f} ms")
        lines.append(f"{'Avg Expansions / Move':<25} | {stats.agent1_avg_nodes:,.1f}{'':<10} | {stats.agent2_avg_nodes:,.1f}")
        lines.append(f"{'Peak Memory':<25} | {stats.agent1_peak_memory_kb:.1f} KB{'':<9} | {stats.agent2_peak_memory_kb:.1f} KB")
        lines.append("=" * 65 + "\n")
        return "\n".join(lines)
