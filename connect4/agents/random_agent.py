"""Random Baseline Agent for Connect Four.

Selects moves uniformly at random from the set of currently legal columns.
Provides a lower-bound performance baseline.
"""

from __future__ import annotations
import random
from typing import Optional
from connect4.core.board import Board
from connect4.agents.base import Agent


class RandomAgent(Agent):
    """Agent that chooses uniformly from available legal columns."""

    def __init__(self, name: str = "RandomAgent", player: int = 1, seed: Optional[int] = None):
        """Initialize random agent.

        Args:
            name: Identifier for the agent.
            player: Assigned player piece (1 or -1).
            seed: Optional integer seed for deterministic random selection.
        """
        super().__init__(name=name, player=player)
        self.rng = random.Random(seed)

    def select_move(self, board: Board) -> int:
        """Pick a uniform random legal column.

        Args:
            board: Current game Board.

        Returns:
            Column index chosen.

        Raises:
            ValueError: If no legal moves are available.
        """
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves available on the board.")

        self.nodes_expanded += 1
        return self.rng.choice(legal_moves)
