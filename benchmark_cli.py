"""Automated Benchmark Suite CLI.

Enables auto-running N seeded matches between any two agents
and generating comparative win-rate, node-expansion, and latency tables.
"""

import argparse
from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.benchmark.runner import BenchmarkRunner
from main import create_agent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated Connect Four Multi-Game Benchmark Runner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
