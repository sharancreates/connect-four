"""Connect Four Board Representation and Game Logic.

Provides a 6x7 grid state representation, move execution, undoing,
win detection (horizontal, vertical, diagonal), and terminal state evaluation.
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import numpy as np

ROWS: int = 6
COLS: int = 7

EMPTY: int = 0
PLAYER_1: int = 1   # Typically 'X' / Red
PLAYER_2: int = -1  # Typically 'O' / Yellow


class Board:
    """Represents a standard 6x7 Connect Four game state.

    The grid is indexed such that row 0 is the top row and row 5 is the bottom row.
    Discs fall by gravity into the lowest empty row of the chosen column.
    """

    def __init__(self, grid: Optional[np.ndarray] = None, current_player: int = PLAYER_1):
        """Initialize the Connect Four board.

        Args:
            grid: Optional 6x7 numpy array representing the initial state.
            current_player: Active player turn (PLAYER_1 = 1 or PLAYER_2 = -1).
        """
        if grid is not None:
            self.grid = np.array(grid, dtype=np.int8)
        else:
            self.grid = np.zeros((ROWS, COLS), dtype=np.int8)

        self.current_player: int = current_player
        self.last_move: Optional[Tuple[int, int]] = None  # (row, col) of last move
        self._winner: Optional[int] = None
        self._is_terminal: Optional[bool] = None

    def copy(self) -> Board:
        """Create an independent deep copy of the board state."""
        new_board = Board(self.grid, self.current_player)
        new_board.last_move = self.last_move
        new_board._winner = self._winner
        new_board._is_terminal = self._is_terminal
        return new_board

    def is_valid_move(self, col: int) -> bool:
        """Check if dropping a disc in the specified column is legal.

        Args:
            col: Target column index (0 to 6).

        Returns:
            True if col is within bounds and top row of col is empty; False otherwise.
        """
        return 0 <= col < COLS and self.grid[0, col] == EMPTY

    def get_legal_moves(self) -> List[int]:
        """Return a list of column indices where a disc can be legally dropped."""
        if self._winner is not None:
            return []
        return [c for c in range(COLS) if self.grid[0, c] == EMPTY]

    def make_move(self, col: int) -> int:
        """Drop a disc for the current player into the specified column.

        Args:
            col: Target column index.

        Returns:
            The row index where the disc landed.

        Raises:
            ValueError: If the column is full or invalid.
        """
        if not self.is_valid_move(col):
            raise ValueError(f"Illegal move: column {col} is full or out of bounds.")

        # Find the lowest available row in column col (from row 5 upwards)
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r, col] == EMPTY:
                self.grid[r, col] = self.current_player
                self.last_move = (r, col)

                # Check if this move wins the game
                if self._check_win_at(r, col, self.current_player):
                    self._winner = self.current_player
                    self._is_terminal = True
                elif not (self.grid[0] == EMPTY).any():
                    self._winner = None  # Draw
                    self._is_terminal = True
                else:
                    self._winner = None
                    self._is_terminal = False

                # Toggle turn to opponent
                self.current_player = -self.current_player
                return r

        raise ValueError(f"Column {col} has no available space.")

    def undo_move(self, col: int) -> None:
        """Undo the top-most disc in the specified column.

        Used for efficient backtracking in search algorithms without full copying.

        Args:
            col: Column index to pop the piece from.

        Raises:
            ValueError: If the column is completely empty.
        """
        # Find the highest occupied row in column col (from row 0 downwards)
        for r in range(ROWS):
            if self.grid[r, col] != EMPTY:
                self.grid[r, col] = EMPTY
                # Turn toggles back to player who made the undone move
                self.current_player = -self.current_player
                self.last_move = None
                self._winner = None
                self._is_terminal = None
                return

        raise ValueError(f"Cannot undo move: column {col} is empty.")

    def _check_win_at(self, row: int, col: int, player: int) -> bool:
        """Check if the piece at (row, col) forms a 4-in-a-row for player."""
        # 1. Horizontal
        consecutive = 0
        for c in range(max(0, col - 3), min(COLS, col + 4)):
            if self.grid[row, c] == player:
                consecutive += 1
                if consecutive >= 4:
                    return True
            else:
                consecutive = 0

        # 2. Vertical
        consecutive = 0
        for r in range(max(0, row - 3), min(ROWS, row + 4)):
            if self.grid[r, col] == player:
                consecutive += 1
                if consecutive >= 4:
                    return True
            else:
                consecutive = 0

        # 3. Positive diagonal (bottom-left to top-right: row decreases as col increases)
        consecutive = 0
        for offset in range(-3, 4):
            r, c = row - offset, col + offset
            if 0 <= r < ROWS and 0 <= c < COLS:
                if self.grid[r, c] == player:
                    consecutive += 1
                    if consecutive >= 4:
                        return True
                else:
                    consecutive = 0

        # 4. Negative diagonal (top-left to bottom-right: row increases as col increases)
        consecutive = 0
        for offset in range(-3, 4):
            r, c = row + offset, col + offset
            if 0 <= r < ROWS and 0 <= c < COLS:
                if self.grid[r, c] == player:
                    consecutive += 1
                    if consecutive >= 4:
                        return True
                else:
                    consecutive = 0

        return False

    def check_win(self, player: int) -> bool:
        """Scan the entire board to determine if player has 4 in a row."""
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if (self.grid[r, c:c + 4] == player).all():
                    return True

        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if (self.grid[r:r + 4, c] == player).all():
                    return True

        # Positive Diagonal (bottom-left to top-right)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r - i, c + i] == player for i in range(4)):
                    return True

        # Negative Diagonal (top-left to bottom-right)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r + i, c + i] == player for i in range(4)):
                    return True

        return False

    def is_full(self) -> bool:
        """Check if all positions on the board are occupied."""
        return not (self.grid[0] == EMPTY).any()

    def is_terminal(self) -> bool:
        """Check if the game has ended (win for either player or draw)."""
        if self._is_terminal is not None:
            return self._is_terminal
        if self.check_win(PLAYER_1):
            self._winner = PLAYER_1
            self._is_terminal = True
            return True
        if self.check_win(PLAYER_2):
            self._winner = PLAYER_2
            self._is_terminal = True
            return True
        if self.is_full():
            self._winner = None
            self._is_terminal = True
            return True
        self._is_terminal = False
        return False

    def get_winner(self) -> Optional[int]:
        """Return the winner of the game (PLAYER_1, PLAYER_2, or None)."""
        if not self.is_terminal():
            return None
        return self._winner

    def render(self, use_color: bool = True) -> str:
        """Return a formatted string representing the board for CLI display."""
        symbols = {
            EMPTY: " . ",
            PLAYER_1: "\033[91m X \033[0m" if use_color else " X ",
            PLAYER_2: "\033[93m O \033[0m" if use_color else " O ",
        }
        lines = []
        lines.append("  " + "   ".join(str(c) for c in range(COLS)))
        lines.append("+" + "---+" * COLS)
        for r in range(ROWS):
            row_str = "|"
            for c in range(COLS):
                row_str += symbols[self.grid[r, c]] + "|"
            lines.append(row_str)
            lines.append("+" + "---+" * COLS)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.render(use_color=False)
