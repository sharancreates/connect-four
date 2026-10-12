"""GUI Entrypoint for Connect Four.

Launches the interactive Pygame board for human-vs-AI gameplay.
"""

import argparse
from connect4.core.board import PLAYER_2
from connect4.gui import Connect4Pygame, PYGAME_AVAILABLE
from main import create_agent


def main() -> None:
    if not PYGAME_AVAILABLE:
        print("Error: Pygame is required to run the visual interface.")
        print("Please run: pip install pygame")
        return

    parser = argparse.ArgumentParser(
        description="Connect Four Pygame Graphical Interface",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--agent",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="mcts",
        help="AI opponent type",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=4,
        help="Search depth for Minimax/AlphaBeta opponent",
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=400,
        help="MCTS simulation budget for opponent",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=None,
        help="MCTS time limit in seconds for opponent",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (for testing)",
    )

    args = parser.parse_args()

    opponent = create_agent(
        args.agent,
        f"AI ({args.agent.capitalize()})",
        player=PLAYER_2,
        depth=args.depth,
        simulations=args.simulations,
        time_limit=args.time_limit,
    )

    app = Connect4Pygame(opponent=opponent, headless=args.headless)
    print(f"\nLaunching Connect Four GUI: Human (Red) vs {opponent.name} (Yellow)...")
    print("Press 'Q' to quit, 'R' to restart game.\n")
    app.run()


if __name__ == "__main__":
    main()
