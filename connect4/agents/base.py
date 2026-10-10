"""Base Agent Interface for Connect Four Players."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from connect4.core.board import Board


class Agent(ABC):
    """Abstract base class for all Connect Four autonomous agents and human interfaces."""

    def __init__(self, name: str, player: int = 1):
        """Initialize base agent.

        Args:
            name: Human-readable identifier for the agent.
            player: Player token (PLAYER_1 = 1 or PLAYER_2 = -1).
        """
        self.name: str = name
        self.player: int = player
        self.nodes_expanded: int = 0

    @abstractmethod
    def select_move(self, board: Board) -> int:
        """Choose a legal column index (0 to 6) to play on the given board.

        Args:
            board: Current game Board state.

        Returns:
            Column index to place a disc in.
        """
        pass

    def reset_stats(self) -> None:
        """Reset internal metrics (such as nodes_expanded) before a new search/game."""
        self.nodes_expanded = 0

    def get_stats(self) -> Dict[str, Any]:
        """Return runtime statistics accumulated by the agent."""
        return {
            "name": self.name,
            "player": self.player,
            "nodes_expanded": self.nodes_expanded,
        }

    def __str__(self) -> str:
        return f"{self.name} (Player {self.player})"
