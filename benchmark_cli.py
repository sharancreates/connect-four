"""Automated Benchmark Suite CLI.

Enables auto-running N seeded matches between any two agents
and generating comparative win-rate, node-expansion, and latency tables,
as well as running full round-robin tournaments.
"""

import argparse
import csv
import os
from itertools import combinations
from typing import Any, Dict, List, Optional, Tuple

from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.benchmark.runner import BenchmarkRunner
from main import create_agent
from connect4.agents.random_agent import RandomAgent
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.alphabeta_agent import AlphaBetaAgent
from connect4.agents.mcts_agent import MCTSAgent


def run_round_robin(
    output_csv: str = "docs/results/tournament.csv",
    games_per_pair: int = 20,
    seed: Optional[int] = 42,
    verbose: bool = False,
) -> Tuple[List[List[float]], List[Dict[str, Any]]]:
    """Run full round-robin tournament between benchmark agents.

    Executes games_per_pair games for every unique pair among:
    Random, Minimax (d=3), AlphaBeta (d=4), AlphaBeta (d=6), MCTS (N=500),
    with alternating first mover.
    """
    agent_configs = [
        ("Random", lambda s: RandomAgent(name="Random", seed=s)),
        ("Minimax (d=3)", lambda s: MinimaxAgent(name="Minimax (d=3)", depth=3)),
        ("AlphaBeta (d=4)", lambda s: AlphaBetaAgent(name="AlphaBeta (d=4)", depth=4)),
        ("AlphaBeta (d=6)", lambda s: AlphaBetaAgent(name="AlphaBeta (d=6)", depth=6)),
        ("MCTS (N=500)", lambda s: MCTSAgent(name="MCTS (N=500)", simulations=500, seed=s)),
    ]
    agent_names = [name for name, _ in agent_configs]
    factory_dict = dict(agent_configs)

    runner = BenchmarkRunner(verbose=verbose)
    rows: List[Dict[str, Any]] = []
    pairings = list(combinations(agent_names, 2))

    for pair_idx, (name_a, name_b) in enumerate(pairings):
        print(f"[{pair_idx + 1:02d}/{len(pairings):02d}] Running series: {name_a} vs {name_b} ({games_per_pair} games, alternating starts)...")
        agent_a = factory_dict[name_a](seed + pair_idx * 100 if seed is not None else None)
        agent_b = factory_dict[name_b](seed + pair_idx * 100 + 50 if seed is not None else None)

        stats = runner.run_series(agent_a, agent_b, num_games=games_per_pair, track_memory=False)

        for rec in stats.games:
            winner = rec.winner_name if rec.winner_name is not None else "Draw"
            rows.append({
                "agents": f"{name_a} vs {name_b}",
                "first_mover": rec.player1_name,
                "winner": winner,
                "plies": rec.total_moves,
            })

    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["agents", "first_mover", "winner", "plies"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} raw game results to {output_csv}")

    # Compute win-rate matrix
    matrix: List[List[float]] = []
    for i, name_i in enumerate(agent_names):
        row: List[float] = []
        for j, name_j in enumerate(agent_names):
            if i == j:
                row.append(50.0)
            else:
                matchup_games = [r for r in rows if r["agents"] in (f"{name_i} vs {name_j}", f"{name_j} vs {name_i}")]
                i_wins = sum(1 for r in matchup_games if r["winner"] == name_i)
                win_pct = round((i_wins / len(matchup_games)) * 100.0, 1)
                row.append(win_pct)
        matrix.append(row)

    print("\nComputed Win-Rate Matrix (%):")
    for name, r in zip(agent_names, matrix):
        print(f"  {name:<16}: {r}")

    return matrix, rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated Connect Four Multi-Game Benchmark Runner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--round-robin",
        action="store_true",
        help="Run full round-robin tournament between benchmark agents",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="docs/results/tournament.csv",
        help="Path to save raw tournament game records in round-robin mode",
    )
    parser.add_argument(
        "--agent1",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="alphabeta",
        help="Agent 1 identifier",
    )
    parser.add_argument(
        "--agent2",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="mcts",
        help="Agent 2 identifier",
    )
    parser.add_argument(
        "--games",
        type=int,
        default=10,
        help="Number of games to execute (alternating turns)",
    )
    parser.add_argument(
        "--depth1",
        type=int,
        default=4,
        help="Search depth for Agent 1 (if Minimax or AlphaBeta)",
    )
    parser.add_argument(
        "--depth2",
        type=int,
        default=4,
        help="Search depth for Agent 2 (if Minimax or AlphaBeta)",
    )
    parser.add_argument(
        "--simulations1",
        type=int,
        default=300,
        help="MCTS simulations for Agent 1",
    )
    parser.add_argument(
        "--simulations2",
        type=int,
        default=300,
        help="MCTS simulations for Agent 2",
    )
    parser.add_argument(
        "--time-limit1",
        type=float,
        default=None,
        help="MCTS time limit in seconds for Agent 1",
    )
    parser.add_argument(
        "--time-limit2",
        type=float,
        default=None,
        help="MCTS time limit in seconds for Agent 2",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Initial seed for reproducible matches",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print outcome of each individual game",
    )

    args = parser.parse_args()

    if args.round_robin:
        run_round_robin(
            output_csv=args.output_csv,
            games_per_pair=args.games if args.games != 10 else 20,
            seed=args.seed,
            verbose=args.verbose,
        )
        return

    a1 = create_agent(
        args.agent1,
        f"{args.agent1.capitalize()}",
        player=PLAYER_1,
        depth=args.depth1,
        simulations=args.simulations1,
        time_limit=args.time_limit1,
        seed=args.seed,
    )
    a2 = create_agent(
        args.agent2,
        f"{args.agent2.capitalize()}",
        player=PLAYER_2,
        depth=args.depth2,
        simulations=args.simulations2,
        time_limit=args.time_limit2,
        seed=args.seed + 100 if args.seed is not None else None,
    )

    print(f"\nStarting benchmark: {a1.name} vs {a2.name} ({args.games} games, alternating starts)...")
    runner = BenchmarkRunner(verbose=args.verbose)
    stats = runner.run_series(a1, a2, num_games=args.games)

    report = runner.format_report(stats)
    print(report)


if __name__ == "__main__":
    main()
