"""Unit and headless integration tests for Pygame GUI."""

import pytest
from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.agents.random_agent import RandomAgent
from connect4.gui.pygame_app import Connect4Pygame, PYGAME_AVAILABLE


@pytest.mark.skipif(not PYGAME_AVAILABLE, reason="Pygame is not installed")
def test_gui_column_coordinate_mapping():
    """Verify x-coordinate to column mapping logic."""
    assert Connect4Pygame.get_column_from_x(50) == 0
    assert Connect4Pygame.get_column_from_x(150) == 1
    assert Connect4Pygame.get_column_from_x(350) == 3
    assert Connect4Pygame.get_column_from_x(650) == 6
    # Out of bounds clamping
    assert Connect4Pygame.get_column_from_x(-50) == 0
    assert Connect4Pygame.get_column_from_x(999) == 6


@pytest.mark.skipif(not PYGAME_AVAILABLE, reason="Pygame is not installed")
def test_gui_headless_gameplay_flow():
    """Verify board interactions inside headless Pygame app."""
    agent = RandomAgent("RandomGUI", player=PLAYER_2, seed=42)
    app = Connect4Pygame(opponent=agent, headless=True)

    # Initial state
    assert not app.game_over
    assert app.board.current_player == PLAYER_1

    # Human makes a move in column 3
    success = app.step_human_move(3)
    assert success is True
    assert app.board.current_player == PLAYER_2

    # AI responds
    app.step_ai_move()
    assert app.board.current_player == PLAYER_1

    # Reset
    app.reset()
    assert not app.game_over
    assert app.board.get_legal_moves() == list(range(7))
