"""GUI Entrypoint for Connect Four.

Launches the interactive Pygame board for human-vs-AI or AI-vs-AI demonstration modes
with live playback speed adjustments, pause controls, last-move indicator, and
dynamic winning line overlay.
"""

from __future__ import annotations
import argparse
from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.gui import Connect4Pygame, PYGAME_AVAILABLE
from main import create_agent


def main() -> None:
    if not PYGAME_AVAILABLE:
        print("Error: Pygame is required to run the visual interface.")
        print("Please run: pip install pygame")
        return

    parser = argparse.ArgumentParser(
        description="Connect Four Pygame Graphical Interface (Adani University)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["human-vs-ai", "ai-vs-ai"],
        default="human-vs-ai",
        help="Gameplay mode: Human vs AI or AI vs AI demonstration",
    )
    parser.add_argument(
        "--agent",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="mcts",
        help="AI opponent type (Player 2) in human-vs-ai mode",
    )
    parser.add_argument(
        "--agent1",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="alphabeta",
        help="Player 1 AI type (in ai-vs-ai mode)",
    )
    parser.add_argument(
        "--agent2",
        choices=["random", "minimax", "alphabeta", "mcts"],
        default="mcts",
        help="Player 2 AI type (in ai-vs-ai mode)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=4,
        help="Search depth for Minimax/AlphaBeta",
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=400,
        help="MCTS simulation budget",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=None,
        help="MCTS thinking time limit in seconds",
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=5,
        choices=range(1, 10),
        help="Playback speed level (1: slow, 5: balanced, 9: fastest)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (for testing)",
    )

    args = parser.parse_args()

    agent1 = None
    agent2 = None

    if args.mode == "ai-vs-ai":
        agent1 = create_agent(
            args.agent1,
            f"Agent 1 ({args.agent1.capitalize()})",
            player=PLAYER_1,
            depth=args.depth,
            simulations=args.simulations,
            time_limit=args.time_limit,
        )
        agent2 = create_agent(
            args.agent2,
            f"Agent 2 ({args.agent2.capitalize()})",
            player=PLAYER_2,
            depth=args.depth,
            simulations=args.simulations,
            time_limit=args.time_limit,
        )
        print(f"\nLaunching Connect Four GUI Demo: {agent1.name} (Red) vs {agent2.name} (Yellow)")
    else:
        chosen_ai = args.agent
        agent2 = create_agent(
            chosen_ai,
            f"AI ({chosen_ai.capitalize()})",
            player=PLAYER_2,
            depth=args.depth,
            simulations=args.simulations,
            time_limit=args.time_limit,
        )
        print(f"\nLaunching Connect Four GUI: Human (Red) vs {agent2.name} (Yellow)")

    print("-" * 55)
    print("Controls:")
    print("  • Click Column : Drop disc (Human turn)")
    print("  • Spacebar     : Pause / Resume playback")
    print("  • Keys 1 to 9  : Adjust AI delay speed (1=slow, 9=fast)")
    print("  • 'R' Key      : Restart game")
    print("  • 'Q' Key      : Quit")
    print("-" * 55 + "\n")

    app = Connect4Pygame(
        agent1=agent1,
        agent2=agent2,
        opponent=agent2,
        mode=args.mode,
        speed=args.speed,
        headless=args.headless,
    )
    app.run()


if __name__ == "__main__":
    main()
