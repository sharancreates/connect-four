"""Command-Line Game Loop for Connect Four.

Supports Human-vs-Agent, Agent-vs-Agent, and Human-vs-Human matches
with real-time performance instrumentation, move logging, and board rendering.
"""

from __future__ import annotations
import time
from typing import Optional, Dict
from connect4.core.board import Board, PLAYER_1, PLAYER_2, COLS
from connect4.agents.base import Agent
from connect4.benchmark.instrumentation import (
    MetricsTracker,
    GameMetrics,
    format_metrics,
)


class HumanPlayer(Agent):
    """Wrapper allowing a human player to interact through terminal stdin."""

    def __init__(self, name: str = "Human", player: int = PLAYER_1):
        super().__init__(name=name, player=player)

    def select_move(self, board: Board) -> int:
        """Prompt human for a column input until valid."""
        legal_moves = board.get_legal_moves()
        while True:
            try:
                raw = input(f"\n[{self.name} (Player {'X' if self.player == 1 else 'O'})] Enter column (0-6) or 'q' to quit: ").strip()
                if raw.lower() in ("q", "quit", "exit"):
                    print("Game terminated by user.")
                    raise KeyboardInterrupt("Exited by player")
                col = int(raw)
                if col in legal_moves:
                    return col
                else:
                    print(f"Invalid column. Legal columns: {legal_moves}")
            except ValueError:
                print("Please enter a valid integer column index (0-6).")


class CLIGameLoop:
    """Manages the lifecycle of a Connect Four game in the terminal."""

    def __init__(
        self,
        player1: Agent,
        player2: Agent,
        delay_between_moves: float = 0.0,
        show_metrics: bool = True,
        use_color: bool = True,
    ):
        """Initialize the game loop.

        Args:
            player1: Agent or Human representing Player 1 ('X').
            player2: Agent or Human representing Player 2 ('O').
            delay_between_moves: Optional sleep delay in seconds (for watchable agent-vs-agent).
            show_metrics: Whether to display time, memory, and node counts per move.
            use_color: Whether to use ANSI terminal colors.
        """
        self.player1: Agent = player1
        self.player2: Agent = player2
        self.delay_between_moves: float = delay_between_moves
        self.show_metrics: bool = show_metrics
        self.use_color: bool = use_color

        self.board: Board = Board()
        self.metrics: Dict[int, GameMetrics] = {
            PLAYER_1: GameMetrics(),
            PLAYER_2: GameMetrics(),
        }

    def _get_agent(self, player_token: int) -> Agent:
        return self.player1 if player_token == PLAYER_1 else self.player2

    def run(self) -> Optional[int]:
        """Execute the game to completion.

        Returns:
            The winning player (PLAYER_1 = 1, PLAYER_2 = -1), or 0 for draw, or None if aborted.
        """
        print("\n" + "=" * 50)
        print("         CONNECT FOUR -- AI GAME ENGINE")
        print("=" * 50)
        print(f" Player 1 (X): {self.player1.name}")
        print(f" Player 2 (O): {self.player2.name}")
        print("=" * 50 + "\n")

        print(self.board.render(use_color=self.use_color))

        turn_count = 0
        try:
            while not self.board.is_terminal():
                turn_count += 1
                current_token = self.board.current_player
                active_agent = self._get_agent(current_token)
                token_symbol = "X" if current_token == PLAYER_1 else "O"

                print(f"\n--- Turn {turn_count}: {active_agent.name} ({token_symbol}) ---")

                if isinstance(active_agent, HumanPlayer):
                    move = active_agent.select_move(self.board)
                    row = self.board.make_move(move)
                    print(f"Move: Column {move} (landed at row {row})")
                else:
                    # Autonomous agent: profile decision
                    move, move_metric = MetricsTracker.profile_agent_move(
                        agent=active_agent,
                        board=self.board,
                        track_memory=self.show_metrics,
                    )
                    row = self.board.make_move(move)
                    self.metrics[current_token].record_move(move_metric)

                    print(f"Move: Column {move} (landed at row {row})")
                    if self.show_metrics:
                        print(f"Metrics: {format_metrics(move_metric)}")

                print("\n" + self.board.render(use_color=self.use_color))

                if self.delay_between_moves > 0 and not isinstance(active_agent, HumanPlayer):
                    time.sleep(self.delay_between_moves)

        except KeyboardInterrupt:
            print("\nGame aborted by user.")
            return None

        # Game finished
        winner = self.board.get_winner()
        self._display_summary(winner, turn_count)
        return winner

    def _display_summary(self, winner: Optional[int], turn_count: int) -> None:
        """Print post-game summary and performance telemetry."""
        print("\n" + "=" * 50)
        print("                 GAME OVER")
        print("=" * 50)

        if winner == PLAYER_1:
            print(f" [WINNER] {self.player1.name} (Player X)!")
        elif winner == PLAYER_2:
            print(f" [WINNER] {self.player2.name} (Player O)!")
        else:
            print(" [DRAW] Game ended in a DRAW (Board full)!")

        print(f" Total turns played: {turn_count}")
        print("-" * 50)
        print(" AGENT TELEMETRY:")

        for token, label in [(PLAYER_1, "Player 1 (X)"), (PLAYER_2, "Player 2 (O)")]:
            agent = self._get_agent(token)
            g_metric = self.metrics[token]
            if g_metric.total_moves > 0:
                print(f" [{label}] {agent.name}:")
                print(f"   * Total Moves:     {g_metric.total_moves}")
                print(f"   * Total Time:      {g_metric.total_time_sec * 1000:.2f} ms")
                print(f"   * Avg Time / Move: {g_metric.avg_time_per_move_ms:.2f} ms")
                print(f"   * Total Nodes:     {g_metric.total_nodes_expanded:,}")
                print(f"   * Avg Nodes / Move:{g_metric.avg_nodes_per_move:,.1f}")
                print(f"   * Peak Memory:     {g_metric.peak_memory_kb:.2f} KB")
        print("=" * 50 + "\n")
