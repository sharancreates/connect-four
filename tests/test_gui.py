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


@pytest.mark.skipif(not PYGAME_AVAILABLE, reason="Pygame is not installed")
def test_gui_pause_and_speed_controls():
    """Verify pause toggle and speed adjustment logic."""
    app = Connect4Pygame(headless=True, speed=5)
    assert app.speed == 5
    assert not app.paused

    # Toggle pause
    app.toggle_pause()
    assert app.paused is True
    # While paused, human moves should be rejected
    assert app.step_human_move(0) is False

    app.toggle_pause()
    assert app.paused is False

    # Adjust speed
    app.set_speed(1)
    assert app.speed == 1
    assert app.delay_ms == 1200

    app.set_speed(9)
    assert app.speed == 9
    assert app.delay_ms == 25

    # Out of range clamps
    app.set_speed(99)
    assert app.speed == 9
    app.set_speed(-5)
    assert app.speed == 1


@pytest.mark.skipif(not PYGAME_AVAILABLE, reason="Pygame is not installed")
def test_gui_winning_overlay_rendering():
    """Verify that winning coordinates trigger winning line rendering in draw_board."""
    agent = RandomAgent("RandomGUI", player=PLAYER_2, seed=1)
    app = Connect4Pygame(opponent=agent, headless=True)

    # Force a winning sequence for Player 1: columns 0, 1, 2, 3
    for col in range(3):
        app.step_human_move(col)          # P1
        app.board.make_move(col + 4)      # P2
    app.step_human_move(3)                # P1 wins

    assert app.game_over is True
    assert app.winner == PLAYER_1
    assert app.winning_coords == [(5, 0), (5, 1), (5, 2), (5, 3)]

    # draw_board should execute without exception, drawing winning line and last move
    app.draw_board()


@pytest.mark.skipif(not PYGAME_AVAILABLE, reason="Pygame is not installed")
def test_gui_ai_vs_ai_mode():
    """Verify AI-vs-AI mode initialization and autonomous step execution."""
    agent1 = RandomAgent("P1_Random", player=PLAYER_1, seed=10)
    agent2 = RandomAgent("P2_Random", player=PLAYER_2, seed=20)
    app = Connect4Pygame(
        agent1=agent1,
        agent2=agent2,
        mode="ai-vs-ai",
        speed=9,
        headless=True,
    )

    assert app.mode == "ai-vs-ai"
    assert app.board.current_player == PLAYER_1

    # Step AI 1
    app.step_ai_move(agent1)
    assert app.board.current_player == PLAYER_2
    assert app.board.last_move is not None

    # Step AI 2
    app.step_ai_move(agent2)
    assert app.board.current_player == PLAYER_1
