"""Comparative Visualization and Plotting Module for Connect Four AI Benchmark.

Generates publication-quality figures comparing Minimax, Alpha-Beta pruning,
and Monte Carlo Tree Search across execution time, nodes expanded (log-scale),
tournament win-rate matrix, and MCTS simulation budget scaling.
All figures are constructed strictly from empirical benchmark CSV results.
"""

from __future__ import annotations
import csv
import os
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

# Force headless Agg backend before importing pyplot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Palette definition
COLOR_MINIMAX = "#ef4444"              # Crimson Red
COLOR_ALPHABETA = "#3b82f6"            # Royal Blue
COLOR_ALPHABETA_HEURISTIC = "#f97316"  # Orange
COLOR_MCTS = "#10b981"                 # Emerald Green
COLOR_ITERATIVE = "#8b5cf6"            # Purple
COLOR_RANDOM = "#64748b"               # Slate Gray


def _setup_style() -> None:
    """Configure modern academic plot typography and layout."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 1.2,
        "grid.color": "#e2e8f0",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
    })


def plot_execution_time_vs_depth(
    csv_path: str = "docs/results/depth_scaling.csv",
    output_path: str = "docs/figures/fig1_execution_time_vs_depth.png",
) -> str:
    """Plot search latency comparison as depth increases from depth_scaling.csv.

    Figure 1: Mean Move Latency vs. Search Depth.
    Two panels: 'Empty Board' and 'Mid-Game Position'.
    Lines for minimax, alphabeta, alphabeta+heuristic.
    Minimax stops at depth 5; does not extrapolate.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing required CSV file: {csv_path}")

    _setup_style()

    data: Dict[str, Dict[str, List[Tuple[int, float]]]] = {
        "empty": {"minimax": [], "alphabeta": [], "alphabeta+heuristic": []},
        "mid-game": {"minimax": [], "alphabeta": [], "alphabeta+heuristic": []},
    }

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pos = row["position"].strip()
            agent = row["agent"].strip()
            depth = int(row["depth"])
            time_ms = float(row["time_ms"])
            if pos in data and agent in data[pos]:
                if agent == "minimax" and depth > 5:
                    continue  # Minimax stops at depth 5; do not extrapolate
                data[pos][agent].append((depth, time_ms))

    for pos in data:
        for agent in data[pos]:
            data[pos][agent].sort(key=lambda x: x[0])

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig, (ax_empty, ax_mid) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    agent_configs = [
        ("minimax", "Vanilla Minimax", COLOR_MINIMAX, "o", 2.2),
        ("alphabeta", "Alpha-Beta", COLOR_ALPHABETA, "s", 2.2),
        ("alphabeta+heuristic", "Alpha-Beta + Heuristic", COLOR_ALPHABETA_HEURISTIC, "^", 2.2),
    ]

    for ax, pos_key, panel_title in [
        (ax_empty, "empty", "Position: Empty Board"),
        (ax_mid, "mid-game", "Position: Mid-Game"),
    ]:
        for agent_key, label, color, marker, lw in agent_configs:
            pts = data[pos_key].get(agent_key, [])
            if pts:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                ax.plot(xs, ys, label=label, color=color, marker=marker, linewidth=lw, markersize=6)

        ax.set_title(panel_title, fontsize=12, fontweight="bold", pad=10, color="#0f172a")
        ax.set_xlabel("Search Depth (plies)", fontsize=11, fontweight="semibold", color="#1e293b")
        ax.set_ylabel("Execution Time (ms)", fontsize=11, fontweight="semibold", color="#1e293b")
        ax.grid(True)
        ax.legend(frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1", fontsize=9.5)

    fig.suptitle(
        "Figure 1: Mean Move Latency vs. Search Depth",
        fontsize=14,
        fontweight="bold",
        y=0.98,
        color="#0f172a",
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_nodes_expanded_log_scale(
    csv_path: str = "docs/results/depth_scaling.csv",
    output_path: str = "docs/figures/fig2_nodes_expanded_log_scale.png",
) -> str:
    """Plot search space expansion on logarithmic scale from depth_scaling.csv.

    Figure 2: Search Tree Node Expansions (Logarithmic Scale) vs. Depth.
    Two panels: 'Empty Board' and 'Mid-Game Position'.
    Lines for minimax, alphabeta, alphabeta+heuristic.
    Minimax stops at depth 5; does not extrapolate.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing required CSV file: {csv_path}")

    _setup_style()

    data: Dict[str, Dict[str, List[Tuple[int, int]]]] = {
        "empty": {"minimax": [], "alphabeta": [], "alphabeta+heuristic": []},
        "mid-game": {"minimax": [], "alphabeta": [], "alphabeta+heuristic": []},
    }

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pos = row["position"].strip()
            agent = row["agent"].strip()
            depth = int(row["depth"])
            nodes = int(row["nodes"])
            if pos in data and agent in data[pos]:
                if agent == "minimax" and depth > 5:
                    continue  # Minimax stops at depth 5; do not extrapolate
                data[pos][agent].append((depth, nodes))

    for pos in data:
        for agent in data[pos]:
            data[pos][agent].sort(key=lambda x: x[0])

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig, (ax_empty, ax_mid) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    agent_configs = [
        ("minimax", "Vanilla Minimax", COLOR_MINIMAX, "o", 2.2),
        ("alphabeta", "Alpha-Beta", COLOR_ALPHABETA, "s", 2.2),
        ("alphabeta+heuristic", "Alpha-Beta + Heuristic", COLOR_ALPHABETA_HEURISTIC, "^", 2.2),
    ]

    for ax, pos_key, panel_title in [
        (ax_empty, "empty", "Position: Empty Board"),
        (ax_mid, "mid-game", "Position: Mid-Game"),
    ]:
        for agent_key, label, color, marker, lw in agent_configs:
            pts = data[pos_key].get(agent_key, [])
            if pts:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                ax.semilogy(xs, ys, label=label, color=color, marker=marker, linewidth=lw, markersize=6)

        ax.set_title(panel_title, fontsize=12, fontweight="bold", pad=10, color="#0f172a")
        ax.set_xlabel("Search Depth (plies)", fontsize=11, fontweight="semibold", color="#1e293b")
        ax.set_ylabel(r"Nodes Expanded ($\log_{10}$ Scale)", fontsize=11, fontweight="semibold", color="#1e293b")
        ax.grid(True, which="both", axis="y")
        ax.grid(True, which="major", axis="x")
        ax.legend(frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1", fontsize=9.5)

    fig.suptitle(
        "Figure 2: Search Tree Node Expansions vs. Depth (Logarithmic Scale)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
        color="#0f172a",
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_winrate_matrix_heatmap(
    csv_path: str = "docs/results/tournament.csv",
    output_path: str = "docs/figures/fig3_tournament_winrate_heatmap.png",
) -> str:
    """Plot head-to-head tournament win-rate matrix heatmap from tournament.csv.

    Figure 3: Round-robin results (20 games per pair).
    Computes score = (wins + 0.5*draws)/games for row agent.
    Prints W-D-L in each cell.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing required CSV file: {csv_path}")

    _setup_style()

    with open(csv_path, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Canonical agent ordering
    canonical_agents = [
        "Random",
        "Minimax (d=3)",
        "AlphaBeta (d=4)",
        "AlphaBeta (d=6)",
        "MCTS (N=500)",
    ]

    # Discover agents from tournament CSV
    present_agents: List[str] = []
    for r in rows:
        pair = r["agents"].split(" vs ")
        for p in pair:
            p_clean = p.strip()
            if p_clean not in present_agents:
                present_agents.append(p_clean)

    agents = [a for a in canonical_agents if a in present_agents]
    for a in present_agents:
        if a not in agents:
            agents.append(a)

    n_agents = len(agents)
    matrix = np.full((n_agents, n_agents), np.nan)
    cell_texts = [["" for _ in range(n_agents)] for _ in range(n_agents)]

    for i, a_row in enumerate(agents):
        for j, b_col in enumerate(agents):
            if i == j:
                matrix[i, j] = 50.0  # Neutral baseline on diagonal
                cell_texts[i][j] = "—"
                continue

            pair_games = [
                r for r in rows
                if r["agents"] in (f"{a_row} vs {b_col}", f"{b_col} vs {a_row}")
            ]
            if not pair_games:
                continue

            wins = sum(1 for r in pair_games if r["winner"].strip() == a_row)
            draws = sum(1 for r in pair_games if r["winner"].strip() == "Draw")
            losses = sum(1 for r in pair_games if r["winner"].strip() == b_col)
            tot = len(pair_games)

            score_pct = ((wins + 0.5 * draws) / tot) * 100.0 if tot > 0 else 0.0
            matrix[i, j] = score_pct
            cell_texts[i][j] = f"{wins}-{draws}-{losses}\n({score_pct:.1f}%)"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.8, 6.6), dpi=300)

    cax = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=100)
    cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Row Agent Score (%) [Wins + 0.5 × Draws]", fontsize=10, fontweight="semibold")

    ax.set_xticks(range(n_agents))
    ax.set_yticks(range(n_agents))
    ax.set_xticklabels(agents, rotation=30, ha="right", fontsize=9.5, fontweight="medium")
    ax.set_yticklabels(agents, fontsize=9.5, fontweight="medium")

    for i in range(n_agents):
        for j in range(n_agents):
            val = matrix[i, j]
            text = cell_texts[i][j]
            text_color = "white" if (not np.isnan(val) and val >= 60) else "#0f172a"
            ax.text(
                j,
                i,
                text,
                ha="center",
                va="center",
                color=text_color,
                fontsize=9.0,
                fontweight="bold",
            )

    ax.set_title(
        "Figure 3: Round-robin results (20 games per pair)",
        fontsize=13,
        fontweight="bold",
        pad=16,
        color="#0f172a",
    )
    ax.set_xlabel("Opponent Agent (Column)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_ylabel("Subject Agent (Row)", fontsize=11, fontweight="semibold", labelpad=8)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_mcts_vs_alphabeta(
    csv_path: str = "docs/results/mcts_vs_alphabeta.csv",
    output_path: str = "docs/figures/fig6_mcts_strength.png",
) -> str:
    """Plot MCTS performance vs Alpha-Beta by simulation budget from mcts_vs_alphabeta.csv.

    Figure 5/6: MCTS vs Alpha-Beta (depth 4, heuristic) across simulation budgets.
    Stacked bars for outcomes (Wins, Draws, Losses) and line for average game length when lost.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing required CSV file: {csv_path}")

    _setup_style()

    budgets = []
    games = []
    mcts_wins = []
    draws = []
    mcts_losses = []
    avg_plies_lost = []

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            budgets.append(str(row["simulations"]))
            games.append(int(row["games"]))
            mcts_wins.append(int(row["mcts_wins"]))
            draws.append(int(row["draws"]))
            mcts_losses.append(int(row["mcts_losses"]))
            avg_plies_lost.append(float(row["avg_plies_when_lost"]))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig, (ax_bar, ax_len) = plt.subplots(1, 2, figsize=(12, 5.0), dpi=300)

    # Left panel: Stacked outcomes
    x_indices = np.arange(len(budgets))
    bar_width = 0.55

    bottom_draws = mcts_wins
    bottom_losses = [w + d for w, d in zip(mcts_wins, draws)]

    ax_bar.bar(x_indices, mcts_wins, bar_width, label="MCTS Wins", color=COLOR_MCTS)
    ax_bar.bar(x_indices, draws, bar_width, bottom=bottom_draws, label="Draws", color="#94a3b8")
    ax_bar.bar(x_indices, mcts_losses, bar_width, bottom=bottom_losses, label="MCTS Losses", color=COLOR_MINIMAX)

    for i in range(len(budgets)):
        w = mcts_wins[i]
        d = draws[i]
        l = mcts_losses[i]
        if w > 0:
            ax_bar.text(i, w / 2, f"{w}", ha="center", va="center", color="white", fontweight="bold", fontsize=9.5)
        if d > 0:
            ax_bar.text(i, w + d / 2, f"{d}", ha="center", va="center", color="white", fontweight="bold", fontsize=9.5)
        if l > 0:
            ax_bar.text(i, w + d + l / 2, f"{l}", ha="center", va="center", color="white", fontweight="bold", fontsize=9.5)

    ax_bar.set_xticks(x_indices)
    ax_bar.set_xticklabels(budgets, fontweight="medium")
    ax_bar.set_xlabel("MCTS Simulations per Move", fontsize=11, fontweight="semibold", color="#1e293b")
    ax_bar.set_ylabel("Number of Games", fontsize=11, fontweight="semibold", color="#1e293b")
    ax_bar.set_title("Match Outcomes vs. Alpha-Beta (d=4)", fontsize=12, fontweight="bold", pad=10)
    ax_bar.set_ylim(0, max(games) * 1.15)
    ax_bar.legend(loc="upper left", frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1", fontsize=9.5)
    ax_bar.grid(True, axis="y")

    # Right panel: Average plies when lost
    ax_len.plot(x_indices, avg_plies_lost, marker="o", color=COLOR_ALPHABETA, linewidth=2.2, markersize=7)
    for i, txt in enumerate(avg_plies_lost):
        ax_len.annotate(
            f"{txt:.1f} plies",
            (x_indices[i], avg_plies_lost[i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontweight="bold",
            fontsize=9.5,
        )

    ax_len.set_xticks(x_indices)
    ax_len.set_xticklabels(budgets, fontweight="medium")
    ax_len.set_xlabel("MCTS Simulations per Move", fontsize=11, fontweight="semibold", color="#1e293b")
    ax_len.set_ylabel("Average Plies in Lost Games", fontsize=11, fontweight="semibold", color="#1e293b")
    ax_len.set_title("Resistance: Game Length When Lost", fontsize=12, fontweight="bold", pad=10)
    ax_len.set_ylim(0, max(avg_plies_lost) * 1.25)
    ax_len.grid(True)

    fig.suptitle(
        "Figure 5/6: MCTS Scaling vs. Alpha-Beta (d=4, Heuristic)",
        fontsize=13,
        fontweight="bold",
        y=0.98,
        color="#0f172a",
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


# Aliases for convenience
plot_mcts_strength = plot_mcts_vs_alphabeta
plot_mcts_budget_scaling = plot_mcts_vs_alphabeta


def generate_all_figures(
    output_dir: str = "docs/figures",
    results_dir: str = "docs/results",
) -> List[str]:
    """Generate all publication benchmark figures from CSV results files."""
    os.makedirs(output_dir, exist_ok=True)
    depth_csv = os.path.join(results_dir, "depth_scaling.csv")
    tournament_csv = os.path.join(results_dir, "tournament.csv")
    mcts_csv = os.path.join(results_dir, "mcts_vs_alphabeta.csv")

    f1 = plot_execution_time_vs_depth(
        csv_path=depth_csv,
        output_path=os.path.join(output_dir, "fig1_execution_time_vs_depth.png"),
    )
    f2 = plot_nodes_expanded_log_scale(
        csv_path=depth_csv,
        output_path=os.path.join(output_dir, "fig2_nodes_expanded_log_scale.png"),
    )
    f3 = plot_winrate_matrix_heatmap(
        csv_path=tournament_csv,
        output_path=os.path.join(output_dir, "fig3_tournament_winrate_heatmap.png"),
    )
    f6 = plot_mcts_vs_alphabeta(
        csv_path=mcts_csv,
        output_path=os.path.join(output_dir, "fig6_mcts_strength.png"),
    )
    return [f1, f2, f3, f6]
