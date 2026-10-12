"""Pygame GUI Interface for Connect Four.

Provides a graphical 6x7 interactive board with smooth rendering,
mouse hover tracking, click-to-drop column selection, and support
for Human-vs-AI and AI-vs-AI demonstration modes.
"""

from __future__ import annotations
import os
import sys
from typing import Optional, Tuple
from connect4.core.board import Board, ROWS, COLS, EMPTY, PLAYER_1, PLAYER_2
from connect4.agents.base import Agent

# Try importing pygame; allow headless operation
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


# Constants for UI Layout
SQUARESIZE: int = 100
RADIUS: int = int(SQUARESIZE / 2 - 5)
WIDTH: int = COLS * SQUARESIZE
HEIGHT: int = (ROWS + 1) * SQUARESIZE

# Palette definition
COLOR_BOARD = (20, 85, 200)
COLOR_BACKGROUND = (15, 23, 42)
COLOR_EMPTY = (30, 41, 59)
COLOR_PLAYER1 = (239, 68, 68)   # Vibrant Red
COLOR_PLAYER2 = (250, 204, 21)  # Vibrant Yellow
COLOR_TEXT = (248, 250, 252)


class Connect4Pygame:
    """Manages the Pygame display window, user inputs, and rendering loop."""

    def __init__(
        self,
        opponent: Optional[Agent] = None,
        headless: bool = False,
    ):
        """Initialize GUI application.

        Args:
            opponent: Autonomous Agent playing as Player 2 ('O' / Yellow).
            headless: If True, uses dummy SDL video driver for headless testing.
        """
        if not PYGAME_AVAILABLE:
            raise ImportError(
                "Pygame is not installed. Run 'pip install pygame' to use the GUI."
            )

        self.headless = headless
        if self.headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect Four — Intelligent Game Agent (Adani University)")
        self.font = pygame.font.SysFont("Helvetica", 36, bold=True)
        self.small_font = pygame.font.SysFont("Helvetica", 22)

        self.opponent = opponent
        self.board = Board()
        self.game_over = False
        self.winner: Optional[int] = None
        self.clock = pygame.time.Clock()

    @staticmethod
    def get_column_from_x(x: int) -> int:
        """Map screen x coordinate to column index (0 to 6)."""
        col = int(x // SQUARESIZE)
        return max(0, min(COLS - 1, col))

    def reset(self) -> None:
        """Reset board and state for a new game."""
        self.board = Board()
        self.game_over = False
        self.winner = None

    def draw_board(self, hover_x: Optional[int] = None) -> None:
        """Render board, slots, and hover disc."""
        # Top banner background
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, (0, 0, WIDTH, SQUARESIZE))

        # Render hover piece if Human's turn and not game over
        if not self.game_over and hover_x is not None and self.board.current_player == PLAYER_1:
            pygame.draw.circle(
                self.screen,
                COLOR_PLAYER1,
                (hover_x, int(SQUARESIZE / 2)),
                RADIUS,
            )

        # Draw grid frame and piece slots
        for c in range(COLS):
            for r in range(ROWS):
                # Blue background rectangle
                pygame.draw.rect(
                    self.screen,
                    COLOR_BOARD,
                    (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE),
                )

                # Determine slot color based on board piece
                val = self.board.grid[r, c]
                if val == PLAYER_1:
                    color = COLOR_PLAYER1
                elif val == PLAYER_2:
                    color = COLOR_PLAYER2
                else:
                    color = COLOR_EMPTY

                pygame.draw.circle(
                    self.screen,
                    color,
                    (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS,
                )

        # Draw game-over banner if applicable
        if self.game_over:
            if self.winner == PLAYER_1:
                msg = "Player 1 (Red) Wins! Press 'R' to Restart"
                color = COLOR_PLAYER1
            elif self.winner == PLAYER_2:
                msg = f"{self.opponent.name if self.opponent else 'Player 2'} Wins! Press 'R' to Restart"
                color = COLOR_PLAYER2
            else:
                msg = "Draw! Board Full. Press 'R' to Restart"
                color = COLOR_TEXT

            text_surf = self.font.render(msg, True, color)
            self.screen.blit(text_surf, (20, 25))

        pygame.display.update()

    def step_human_move(self, col: int) -> bool:
        """Process a human disc drop into column. Returns True if move was executed."""
        if self.game_over or not self.board.is_valid_move(col):
            return False

        self.board.make_move(col)
        if self.board.is_terminal():
            self.game_over = True
            self.winner = self.board.get_winner()
        return True

    def step_ai_move(self) -> None:
        """Trigger AI move computation and update board."""
        if self.game_over or self.opponent is None or self.board.current_player != PLAYER_2:
            return

        # Render current state with thinking label
        self.screen.fill(COLOR_BACKGROUND, (0, 0, WIDTH, SQUARESIZE))
        lbl = self.font.render(f"{self.opponent.name} is thinking...", True, COLOR_PLAYER2)
        self.screen.blit(lbl, (20, 25))
        pygame.display.update()

        ai_move = self.opponent.select_move(self.board)
        self.board.make_move(ai_move)

        if self.board.is_terminal():
            self.game_over = True
            self.winner = self.board.get_winner()

    def run(self) -> None:
        """Main graphical event loop."""
        running = True
        hover_x = WIDTH // 2

        self.draw_board(hover_x)

        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        break
                    elif event.key == pygame.K_r:
                        self.reset()
                        self.draw_board(hover_x)

                elif event.type == pygame.MOUSEMOTION:
                    hover_x = event.pos[0]
                    self.draw_board(hover_x)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.game_over and self.board.current_player == PLAYER_1:
                        col = self.get_column_from_x(event.pos[0])
                        if self.step_human_move(col):
                            self.draw_board(hover_x)

                            # If game didn't end and AI is playing as Player 2:
                            if not self.game_over and self.opponent is not None:
                                pygame.time.wait(200)
                                self.step_ai_move()
                                self.draw_board(hover_x)

            if not self.game_over and self.board.current_player == PLAYER_2 and self.opponent is not None:
                self.step_ai_move()
                self.draw_board(hover_x)

        pygame.quit()
