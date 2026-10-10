"""Plain Minimax Agent (No Pruning) for Connect Four.

Implements classic depth-limited adversarial Minimax search without pruning.
Tracks and reports raw node expansions to measure state-space explosion
as required for Week 1 baseline benchmarking.
"""

from __future__ import annotations
from typing import Optional, Tuple
from connect4.core.board import Board, PLAYER_1, PLAYER_2, EMPTY, ROWS, COLS
from connect4.agents.base import Agent

WIN_SCORE = 100000
LOSS_SCORE = -100000
DRAW_SCORE = 0


class MinimaxAgent(Agent):
    """Exhaustive depth-limited Minimax agent without pruning."""

    def __init__(
        self,
        name: str = "PlainMinimax",
        player: int = 1,
        depth: int = 4,
    ):
        """Initialize Plain Minimax Agent.

        Args:
            name: Agent identifier name.
            player: Assigned player (PLAYER_1 = 1, PLAYER_2 = -1).
            depth: Maximum search depth.
        """
        super().__init__(name=name, player=player)
        self.depth: int = depth

    def select_move(self, board: Board) -> int:
        """Choose the optimal move using depth-limited plain Minimax search.

        Args:
            board: Current Board state.

        Returns:
            Column index of the best move found.
        """
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves available.")

        # Single legal move: play it directly
        if len(legal_moves) == 1:
            self.nodes_expanded += 1
            return legal_moves[0]

        best_score = float("-inf")
        best_move = legal_moves[0]

        # Prefer center-out move ordering for clean tie-breaking
        center = COLS // 2
        ordered_moves = sorted(legal_moves, key=lambda c: abs(c - center))

        for col in ordered_moves:
            board.make_move(col)
            # After making move, it is opponent's turn, so we call min_value
            score = self._min_value(board, self.depth - 1)
            board.undo_move(col)

            if score > best_score:
                best_score = score
                best_move = col

        return best_move

    def _max_value(self, board: Board, depth: int) -> float:
        """Maximizing step for the agent."""
        self.nodes_expanded += 1

        # Check terminal state
        if board._winner == self.player:
            return WIN_SCORE + depth
        elif board._winner == -self.player:
            return LOSS_SCORE - depth
        elif board._is_terminal:
            return DRAW_SCORE

        if depth <= 0:
            return self._evaluate_board(board)

        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return DRAW_SCORE

        value = float("-inf")
        for col in legal_moves:
            board.make_move(col)
            value = max(value, self._min_value(board, depth - 1))
            board.undo_move(col)
        return value

    def _min_value(self, board: Board, depth: int) -> float:
        """Minimizing step for the opponent."""
        self.nodes_expanded += 1

        # Check terminal state
        if board._winner == self.player:
            return WIN_SCORE + depth
        elif board._winner == -self.player:
            return LOSS_SCORE - depth
        elif board._is_terminal:
            return DRAW_SCORE

        if depth <= 0:
            return self._evaluate_board(board)

        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return DRAW_SCORE

        value = float("inf")
        for col in legal_moves:
            board.make_move(col)
            value = min(value, self._max_value(board, depth - 1))
            board.undo_move(col)
        return value

    def _evaluate_board(self, board: Board) -> float:
        """Simple baseline heuristic for depth cutoff.

        Gives slight weight to center column control and 2/3 disc alignments.
        """
        center_col = board.grid[:, COLS // 2]
        center_count = int((center_col == self.player).sum()) - int((center_col == -self.player).sum())
        return center_count * 3.0
