"""Decision log for the report and the demo.

Shows, move by move, how Alpha-Beta scores every column from a fixed mid-game
position, which column it picks and how many nodes it needed.

Run from the repo root:
    python decision_log_cli.py --depth 4 --plies 6
"""

import argparse
import os

from connect4.core.board import Board
from connect4.agents.alphabeta_agent import AlphaBetaAgent
from connect4.agents.heuristic import evaluate_board

# same mid-game position as in experiments_cli.py
MID_GAME = [3, 3, 2, 4, 4, 2, 5, 3]


def root_scores(agent, board, depth):
    # score every legal column with a full window, so each value is exact
    scores = []
    for col in agent.order_moves(board.get_legal_moves()):
        before = agent.nodes_expanded
        board.make_move(col)
        score = agent.min_value(board, depth - 1, float("-inf"), float("inf"))
        board.undo_move(col)
        scores.append((col, score, agent.nodes_expanded - before))
    return scores


def run(depth, plies, out_path):
    lines = []
    board = Board()
    for col in MID_GAME:
        board.make_move(col)

    lines.append(f"Decision log: Alpha-Beta, depth {depth}, heuristic on")
    lines.append(f"Start position after moves {MID_GAME}")
    lines.append("Scores are from the point of view of the player to move (higher is better).")
    lines.append("")

    for ply in range(1, plies + 1):
        if board.is_terminal():
            lines.append("Game over.")
            break

        player = board.current_player
        name = "X" if player == 1 else "O"

        # one agent for the analysis, a fresh one for the real search
        analysis = AlphaBetaAgent(player=player, depth=depth, use_heuristic=True)
        scores = root_scores(analysis, board, depth)

        agent = AlphaBetaAgent(player=player, depth=depth, use_heuristic=True)
        move = agent.select_move(board)

        lines.append(f"--- Ply {ply}: player {name} to move ---")
        lines.append(str(board))
        lines.append(f"Heuristic value of this position for {name}: {evaluate_board(board, player)}")
        lines.append("Column | score | nodes (full window)")
        for col, score, nodes in scores:
            lines.append(f"  {col}    | {score:>9.1f} | {nodes}")
        lines.append(f"Chosen column: {move} (search used {agent.nodes_expanded} nodes with pruning)")
        lines.append("")

        board.make_move(move)

    lines.append("Final board:")
    lines.append(str(board))

    text = "\n".join(lines)
    print(text)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(text + "\n")
    print("\nsaved", out_path)


def main():
    parser = argparse.ArgumentParser(description="Alpha-Beta decision log")
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--plies", type=int, default=6)
    parser.add_argument("--out", default="docs/results/decision_log.txt")
    args = parser.parse_args()
    run(args.depth, args.plies, args.out)


if __name__ == "__main__":
    main()
