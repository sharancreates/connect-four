"""Member 1 experiments for Week 3 (complexity and failure-mode analysis).

Run from the repo root, for example:
    python experiments_cli.py --experiment depth --plot
"""

import argparse
import csv
import os
import time

from connect4.core.board import Board
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.alphabeta_agent import AlphaBetaAgent
from connect4.agents.iterative_agent import IterativeAlphaBetaAgent
from connect4.agents.mcts_agent import MCTSAgent


# fixed positions so every run is repeatable
POSITIONS = {
    "empty": [],
    "mid-game": [3, 3, 2, 4, 4, 2, 5, 3],
}


def make_position(moves):
    board = Board()
    for col in moves:
        board.make_move(col)
    return board


def save_csv(out_dir, name, header, rows):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print("saved", path)


# Experiment 1: how time and nodes grow with depth

def run_depth(results_dir, time_cap):
    kinds = [
        ("minimax", 5, lambda p, d: MinimaxAgent(player=p, depth=d)),
        ("alphabeta", 7, lambda p, d: AlphaBetaAgent(player=p, depth=d)),
        ("alphabeta+heuristic", 7, lambda p, d: AlphaBetaAgent(player=p, depth=d, use_heuristic=True)),
    ]
    rows = []

    for pos_name, moves in POSITIONS.items():
        print("\nPosition:", pos_name)
        for kind, max_depth, make in kinds:
            for depth in range(1, max_depth + 1):
                board = make_position(moves)
                agent = make(board.current_player, depth)

                start = time.perf_counter()
                agent.select_move(board)
                ms = (time.perf_counter() - start) * 1000

                rows.append([pos_name, kind, depth, agent.nodes_expanded, round(ms, 2)])
                print(f"  {kind:20s} depth {depth}: {agent.nodes_expanded:>10,} nodes, {ms:>10.1f} ms")

                # stop going deeper once one move is too slow
                if ms / 1000 > time_cap:
                    print(f"  {kind}: stopped, one move took more than {time_cap} s")
                    break

    save_csv(results_dir, "depth_scaling.csv",
             ["position", "agent", "depth", "nodes", "time_ms"], rows)

    # pruning efficiency = how many fewer nodes alphabeta needs than minimax
    nodes = {}
    for pos, kind, depth, n, ms in rows:
        nodes[(pos, kind, depth)] = n

    print("\nPruning efficiency (same evaluation, alphabeta vs minimax)")
    for (pos, kind, depth), n in sorted(nodes.items()):
        if kind == "minimax":
            ab = nodes.get((pos, "alphabeta", depth))
            if ab:
                print(f"  {pos:9s} depth {depth}: minimax {n:>9,}, alphabeta {ab:>8,}, {100 * (1 - ab / n):.1f}% fewer nodes")

    return rows


# Experiment 2: what depth does iterative deepening reach in a time budget

def run_iterative(results_dir):
    rows = []
    print("\nIterative deepening: depth reached per time budget")

    for pos_name, moves in POSITIONS.items():
        for limit in [0.05, 0.2, 0.5, 1.0]:
            board = make_position(moves)
            agent = IterativeAlphaBetaAgent(player=board.current_player, max_depth=12, time_limit=limit)

            start = time.perf_counter()
            agent.select_move(board)
            elapsed = time.perf_counter() - start

            rows.append([pos_name, limit, agent.depth_reached, agent.nodes_expanded, round(elapsed, 3)])
            print(f"  {pos_name:9s} limit {limit:>4} s: depth {agent.depth_reached}, {agent.nodes_expanded:>8,} nodes, took {elapsed:.3f} s")

    save_csv(results_dir, "iterative_depth.csv",
             ["position", "time_limit_s", "depth_reached", "nodes", "elapsed_s"], rows)
    return rows


# Experiment 3: does MCTS block an immediate win when it has few simulations

def block_position():
    # X has 3 in the bottom row (cols 0-2), O to move and must play column 3
    board = Board()
    board.grid[5, 0:3] = 1
    board.grid[4, 0:2] = -1
    board.current_player = -1
    return board


def run_block(results_dir):
    rows = []
    print("\nBlock test: must play column 3 (20 seeds per budget)")

    for sims in [5, 20, 100, 500]:
        hits = 0
        for seed in range(20):
            agent = MCTSAgent(player=-1, simulations=sims, seed=seed)
            if agent.select_move(block_position()) == 3:
                hits += 1
        rows.append([sims, 20, hits])
        print(f"  MCTS {sims:>4} simulations: blocked {hits}/20")

    ab = AlphaBetaAgent(player=-1, depth=2)
    ab_move = ab.select_move(block_position())
    print(f"  AlphaBeta depth 2: played column {ab_move}")

    save_csv(results_dir, "block_test.csv", ["simulations", "trials", "blocked"], rows)
    return rows


# Experiment 4: MCTS (different budgets) against Alpha-Beta depth 4 with heuristic

def play_game(make_x, make_o):
    board = Board()
    x = make_x(1)
    o = make_o(-1)
    plies = 0
    while not board.is_terminal():
        agent = x if board.current_player == 1 else o
        board.make_move(agent.select_move(board))
        plies += 1
    return board.get_winner(), plies


def run_mcts(results_dir, games, budgets):
    rows = []
    print("\nMCTS vs AlphaBeta (depth 4, heuristic), sides alternate each game")

    for sims in budgets:
        wins = draws = losses = 0
        lost_plies = []

        for g in range(games):
            mcts_first = (g % 2 == 0)

            def make_mcts(p):
                return MCTSAgent(player=p, simulations=sims, seed=g)

            def make_ab(p):
                return AlphaBetaAgent(player=p, depth=4, use_heuristic=True)

            if mcts_first:
                winner, plies = play_game(make_mcts, make_ab)
                mcts_side = 1
            else:
                winner, plies = play_game(make_ab, make_mcts)
                mcts_side = -1

            if winner is None:
                draws += 1
            elif winner == mcts_side:
                wins += 1
            else:
                losses += 1
                lost_plies.append(plies)

        avg_lost = round(sum(lost_plies) / len(lost_plies), 1) if lost_plies else 0
        rows.append([sims, games, wins, draws, losses, avg_lost])
        print(f"  {sims:>5} simulations: {wins} wins, {draws} draws, {losses} losses (avg length of lost games: {avg_lost} plies)")

    save_csv(results_dir, "mcts_vs_alphabeta.csv",
             ["simulations", "games", "mcts_wins", "draws", "mcts_losses", "avg_plies_when_lost"], rows)
    return rows


# Plots

def plot_depth(rows, fig_dir):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 4.5))
    for kind in ["minimax", "alphabeta", "alphabeta+heuristic"]:
        pts = [(d, ms) for pos, k, d, n, ms in rows if pos == "mid-game" and k == kind]
        if pts:
            plt.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=kind)

    plt.yscale("log")
    plt.xlabel("Search depth")
    plt.ylabel("Time per move (ms, log scale)")
    plt.title("Time per move vs search depth (mid-game position)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    os.makedirs(fig_dir, exist_ok=True)
    path = os.path.join(fig_dir, "fig5_depth_scaling.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print("saved", path)


def plot_mcts(rows, fig_dir):
    import matplotlib.pyplot as plt

    labels = [str(r[0]) for r in rows]
    wins = [r[2] for r in rows]
    draws = [r[3] for r in rows]
    losses = [r[4] for r in rows]

    plt.figure(figsize=(7, 4.5))
    plt.bar(labels, wins, label="MCTS wins")
    plt.bar(labels, draws, bottom=wins, label="Draws")
    plt.bar(labels, losses, bottom=[w + d for w, d in zip(wins, draws)], label="MCTS losses")

    plt.xlabel("MCTS simulations per move")
    plt.ylabel("Games")
    plt.title("MCTS vs Alpha-Beta (depth 4, heuristic)")
    plt.legend()

    os.makedirs(fig_dir, exist_ok=True)
    path = os.path.join(fig_dir, "fig6_mcts_strength.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print("saved", path)


def main():
    parser = argparse.ArgumentParser(description="Member 1 experiments (Week 3)")
    parser.add_argument("--experiment", choices=["all", "depth", "iterative", "block", "mcts"], default="all")
    parser.add_argument("--games", type=int, default=6, help="games per MCTS budget")
    parser.add_argument("--budgets", type=int, nargs="+", default=[50, 200, 500, 1000], help="MCTS simulation budgets")
    parser.add_argument("--time-cap", type=float, default=20.0, help="stop going deeper after one move takes this many seconds")
    parser.add_argument("--results-dir", default="docs/results")
    parser.add_argument("--fig-dir", default="docs/figures")
    parser.add_argument("--plot", action="store_true", help="also save figures")
    args = parser.parse_args()

    if args.experiment in ("all", "depth"):
        rows = run_depth(args.results_dir, args.time_cap)
        if args.plot:
            plot_depth(rows, args.fig_dir)

    if args.experiment in ("all", "iterative"):
        run_iterative(args.results_dir)

    if args.experiment in ("all", "block"):
        run_block(args.results_dir)

    if args.experiment in ("all", "mcts"):
        rows = run_mcts(args.results_dir, args.games, args.budgets)
        if args.plot:
            plot_mcts(rows, args.fig_dir)


if __name__ == "__main__":
    main()
