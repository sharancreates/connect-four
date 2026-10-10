"""Integration tests for the CLI game loop."""

from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.agents.random_agent import RandomAgent
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.cli.game_loop import CLIGameLoop


def test_agent_vs_agent_game_simulation():
    """Verify an automated game runs to terminal state and collects metrics."""
    agent1 = RandomAgent(name="RandomP1", player=PLAYER_1, seed=42)
    agent2 = MinimaxAgent(name="MinimaxP2", player=PLAYER_2, depth=2)

    game = CLIGameLoop(
        player1=agent1,
        player2=agent2,
        delay_between_moves=0.0,
        show_metrics=False,
        use_color=False,
    )
    result = game.run()

    # Result should be either 1, -1, or None (draw)
    assert result in (PLAYER_1, PLAYER_2, None)
    assert game.board.is_terminal()
    assert game.metrics[PLAYER_1].total_moves > 0
    assert game.metrics[PLAYER_2].total_moves > 0
    assert game.metrics[PLAYER_2].total_nodes_expanded > 0
