"""Pygame GUI Interface for Connect Four.

Provides a graphical 6x7 interactive board with smooth rendering,
mouse hover tracking, click-to-drop column selection, winning 4-in-a-row
ray overlays, last-move indicator rings, playback pause/speed controls,
and support for Human-vs-AI and AI-vs-AI demonstration modes.
"""

from __future__ import annotations
import os
import sys
from typing import Optional, Tuple, List
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
COLOR_PLAYER1 = (239, 68, 68)     # Vibrant Red
COLOR_PLAYER2 = (250, 204, 21)    # Vibrant Yellow
COLOR_TEXT = (248, 250, 252)
COLOR_LAST_MOVE = (255, 255, 255) # Crisp White Ring for Last Move
COLOR_WIN_LINE = (52, 211, 153)   # Neon Emerald Glow for Winning Ray
COLOR_PAUSED = (251, 146, 60)     # Amber for Paused Indicator

SPEED_DELAY_MAP = {
    1: 1200,
    2: 900,
    3: 650,
    4: 450,
    5: 300,
    6: 200,
    7: 120,
    8: 70,
    9: 25,
}


class Connect4Pygame:
    """Manages the Pygame display window, user inputs, and rendering loop."""

    def __init__(
        self,
        opponent: Optional[Agent] = None,
        agent1: Optional[Agent] = None,
        agent2: Optional[Agent] = None,
        mode: str = "human-vs-ai",
        speed: int = 5,
        headless: bool = False,
    ):
        """Initialize GUI application.

        Args:
            opponent: Autonomous Agent playing as Player 2 ('O' / Yellow). Backwards compatible.
            agent1: Autonomous Agent playing as Player 1 ('X' / Red) in AI-vs-AI mode.
            agent2: Autonomous Agent playing as Player 2 ('O' / Yellow).
            mode: Game mode ("human-vs-ai" or "ai-vs-ai").
            speed: Playback speed level from 1 (slow) to 9 (ultra-fast).
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
        self.font = pygame.font.SysFont("Helvetica", 32, bold=True)
        self.small_font = pygame.font.SysFont("Helvetica", 20)
        self.status_font = pygame.font.SysFont("Helvetica", 16)

        self.mode = mode
        self.agent1 = agent1
        self.agent2 = agent2 or opponent
        self.opponent = self.agent2  # Preserved for backwards compatibility

        self.speed = max(1, min(9, speed))
        self.delay_ms = SPEED_DELAY_MAP.get(self.speed, 300)
        self.paused = False

        self.board = Board()
        self.game_over = False
        self.winner: Optional[int] = None
        self.winning_coords: Optional[List[Tuple[int, int]]] = None
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
        self.winning_coords = None

    def set_speed(self, speed: int) -> None:
        """Adjust playback speed level (1 to 9)."""
        self.speed = max(1, min(9, speed))
        self.delay_ms = SPEED_DELAY_MAP.get(self.speed, 300)

    def toggle_pause(self) -> None:
        """Toggle pause state."""
        self.paused = not self.paused

    def draw_board(self, hover_x: Optional[int] = None) -> None:
        """Render board, slots, hover disc, last move ring, winning line, and status HUD."""
        # Top banner background
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, (0, 0, WIDTH, SQUARESIZE))

        # Render hover piece if Human's turn, not paused, and not game over
        if (
            not self.game_over
            and not self.paused
            and hover_x is not None
            and self.mode == "human-vs-ai"
            and self.board.current_player == PLAYER_1
        ):
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

                center = (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int((r + 1) * SQUARESIZE + SQUARESIZE / 2),
                )
                pygame.draw.circle(self.screen, color, center, RADIUS)

        # Highlight last placed move with clean accented ring
        if self.board.last_move is not None:
            r_last, c_last = self.board.last_move
            last_center = (
                int(c_last * SQUARESIZE + SQUARESIZE / 2),
                int((r_last + 1) * SQUARESIZE + SQUARESIZE / 2),
            )
            pygame.draw.circle(self.screen, COLOR_LAST_MOVE, last_center, RADIUS - 4, width=4)
            pygame.draw.circle(self.screen, COLOR_LAST_MOVE, last_center, 5)

        # Draw dynamic winning 4-in-a-row ray overlay if game is terminal with winner
        if self.game_over and self.winning_coords and len(self.winning_coords) >= 4:
            c_start = (
                int(self.winning_coords[0][1] * SQUARESIZE + SQUARESIZE / 2),
                int((self.winning_coords[0][0] + 1) * SQUARESIZE + SQUARESIZE / 2),
            )
            c_end = (
                int(self.winning_coords[-1][1] * SQUARESIZE + SQUARESIZE / 2),
                int((self.winning_coords[-1][0] + 1) * SQUARESIZE + SQUARESIZE / 2),
            )
            # Draw prominent glowing ray line
            pygame.draw.line(self.screen, COLOR_WIN_LINE, c_start, c_end, width=8)

            # Draw highlighted accent rings around all 4 winning discs
            for r_win, col_win in self.winning_coords:
                pt = (
                    int(col_win * SQUARESIZE + SQUARESIZE / 2),
                    int((r_win + 1) * SQUARESIZE + SQUARESIZE / 2),
                )
                pygame.draw.circle(self.screen, COLOR_WIN_LINE, pt, RADIUS - 2, width=5)

        # Render Header Info & Status HUD
        if self.game_over:
            if self.winner == PLAYER_1:
                p1_name = self.agent1.name if self.agent1 else "Player 1 (Red)"
                msg = f"{p1_name} Wins! [R] to Restart"
                color = COLOR_PLAYER1
            elif self.winner == PLAYER_2:
                p2_name = self.agent2.name if self.agent2 else "Player 2 (Yellow)"
                msg = f"{p2_name} Wins! [R] to Restart"
                color = COLOR_PLAYER2
            else:
                msg = "Draw! Board Full. [R] to Restart"
                color = COLOR_TEXT

            text_surf = self.font.render(msg, True, color)
            self.screen.blit(text_surf, (20, 20))
        elif self.paused:
            msg = "[PAUSED] Press SPACE to Resume"
            text_surf = self.font.render(msg, True, COLOR_PAUSED)
            self.screen.blit(text_surf, (20, 20))
        else:
            if self.mode == "human-vs-ai":
                if self.board.current_player == PLAYER_1:
                    msg = "Your Turn (Red)"
                    color = COLOR_PLAYER1
                else:
                    opp_name = self.agent2.name if self.agent2 else "AI"
                    msg = f"{opp_name} Thinking..."
                    color = COLOR_PLAYER2
            else:
                curr_agent = self.agent1 if self.board.current_player == PLAYER_1 else self.agent2
                name = curr_agent.name if curr_agent else "Agent"
                msg = f"{name}'s Turn"
                color = COLOR_PLAYER1 if self.board.current_player == PLAYER_1 else COLOR_PLAYER2

            text_surf = self.font.render(msg, True, color)
            self.screen.blit(text_surf, (20, 20))

        # Bottom/Right info text: speed & controls
        hud_text = f"Speed: {self.speed} (Keys 1-9) | [Space] Pause"
        hud_surf = self.status_font.render(hud_text, True, (148, 163, 184))
        self.screen.blit(hud_surf, (WIDTH - hud_surf.get_width() - 15, 65))

        pygame.display.update()

    def step_human_move(self, col: int) -> bool:
        """Process a human disc drop into column. Returns True if move was executed."""
        if self.game_over or self.paused or not self.board.is_valid_move(col):
            return False

        self.board.make_move(col)
        if self.board.is_terminal():
            self.game_over = True
            self.winner = self.board.get_winner()
            self.winning_coords = self.board.get_winning_coordinates()
        return True

    def step_ai_move(self, agent: Optional[Agent] = None) -> None:
        """Trigger autonomous move computation for the active player."""
        if self.game_over or self.paused:
            return

        active_agent = agent or (self.agent1 if self.board.current_player == PLAYER_1 else self.agent2)
        if active_agent is None:
            return

        # Render thinking status
        self.screen.fill(COLOR_BACKGROUND, (0, 0, WIDTH, SQUARESIZE))
        color = COLOR_PLAYER1 if self.board.current_player == PLAYER_1 else COLOR_PLAYER2
        lbl = self.font.render(f"{active_agent.name} thinking...", True, color)
        self.screen.blit(lbl, (20, 20))
        hud_text = f"Speed: {self.speed} (Keys 1-9) | [Space] Pause"
        hud_surf = self.status_font.render(hud_text, True, (148, 163, 184))
        self.screen.blit(hud_surf, (WIDTH - hud_surf.get_width() - 15, 65))
        pygame.display.update()

        ai_move = active_agent.select_move(self.board)
        self.board.make_move(ai_move)

        if self.board.is_terminal():
            self.game_over = True
            self.winner = self.board.get_winner()
            self.winning_coords = self.board.get_winning_coordinates()

    def run(self) -> None:
        """Main graphical event loop with interactive controls."""
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
                    elif event.key == pygame.K_SPACE:
                        self.toggle_pause()
                        self.draw_board(hover_x)
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        new_speed = event.key - pygame.K_0
                        self.set_speed(new_speed)
                        self.draw_board(hover_x)
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        self.set_speed(self.speed + 1)
                        self.draw_board(hover_x)
                    elif event.key == pygame.K_MINUS:
                        self.set_speed(self.speed - 1)
                        self.draw_board(hover_x)

                elif event.type == pygame.MOUSEMOTION:
                    hover_x = event.pos[0]
                    if not self.game_over and not self.paused:
                        self.draw_board(hover_x)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (
                        self.mode == "human-vs-ai"
                        and not self.game_over
                        and not self.paused
                        and self.board.current_player == PLAYER_1
                    ):
                        col = self.get_column_from_x(event.pos[0])
                        if self.step_human_move(col):
                            self.draw_board(hover_x)

                            # AI response turn
                            if not self.game_over and not self.paused and self.agent2 is not None:
                                pygame.time.wait(self.delay_ms)
                                self.step_ai_move(self.agent2)
                                self.draw_board(hover_x)

            # AI-vs-AI autonomous turn stepping
            if self.mode == "ai-vs-ai" and not self.game_over and not self.paused:
                pygame.time.wait(self.delay_ms)
                if self.board.current_player == PLAYER_1 and self.agent1 is not None:
                    self.step_ai_move(self.agent1)
                elif self.board.current_player == PLAYER_2 and self.agent2 is not None:
                    self.step_ai_move(self.agent2)
                self.draw_board(hover_x)

            # Human-vs-AI if AI turn is pending (e.g. unpaused)
            elif (
                self.mode == "human-vs-ai"
                and not self.game_over
                and not self.paused
                and self.board.current_player == PLAYER_2
                and self.agent2 is not None
            ):
                pygame.time.wait(self.delay_ms)
                self.step_ai_move(self.agent2)
                self.draw_board(hover_x)

        pygame.quit()
