"""Primary CLI Entrypoint for Connect Four AI.

Allows launching Human-vs-Agent, Agent-vs-Agent, and Human-vs-Human matches
with configurable search depth, random seeds, and real-time instrumentation.
"""

import argparse
import sys
from connect4.core.board import PLAYER_1, PLAYER_2
from connect4.agents.base import Agent
from connect4.agents.random_agent import RandomAgent
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.cli.game_loop import CLIGameLoop, HumanPlayer


def create_agent(agent_type: str, name: str, player: int, depth: int, seed: int | None = None) -> Agent:
    """Factory creating an Agent instance based on type argument."""
    agent_type = agent_type.lower()
    if agent_type == "human":
        return HumanPlayer(name=name, player=player)
    elif agent_type == "random":
        return RandomAgent(name=name, player=player, seed=seed)
    elif agent_type == "minimax":
        return MinimaxAgent(name=name, player=player, depth=depth)
    else:
        raise ValueError(f"Unknown agent type: '{agent_type}'. Supported: human, random, minimax.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Connect Four AI — Minimax vs. MCTS Project (Foundation of AI)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["human-vs-agent", "agent-vs-agent", "human-vs-human"],
        default="human-vs-agent",
        help="Gameplay mode",
    )
    parser.add_argument(
        "--agent1",
        choices=["human", "random", "minimax"],
        default="human",
        help="Player 1 type (X)",
    )
    parser.add_argument(
        "--agent2",
        choices=["human", "random", "minimax"],
        default="minimax",
        help="Player 2 type (O)",
    )
    parser.add_argument(
        "--depth1",
        type=int,
        default=4,
        help="Search depth for Player 1 (if Minimax)",
    )
    parser.add_argument(
        "--depth2",
        type=int,
        default=4,
        help="Search depth for Player 2 (if Minimax)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Delay in seconds between moves in agent-vs-agent mode",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--no-metrics",
        action="store_true",
        help="Disable instrumentation telemetry per move",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colored terminal output",
    )

    args = parser.parse_args()

    # Configure agents based on selected mode
    if args.mode == "human-vs-agent":
        p1 = HumanPlayer("Human Player", player=PLAYER_1)
        p2 = create_agent(args.agent2 if args.agent2 != "human" else "minimax", "AI Opponent", player=PLAYER_2, depth=args.depth2, seed=args.seed)
    elif args.mode == "agent-vs-agent":
        a1_type = args.agent1 if args.agent1 != "human" else "random"
        a2_type = args.agent2 if args.agent2 != "human" else "minimax"
        p1 = create_agent(a1_type, f"Agent 1 ({a1_type.capitalize()})", player=PLAYER_1, depth=args.depth1, seed=args.seed)
        p2 = create_agent(a2_type, f"Agent 2 ({a2_type.capitalize()})", player=PLAYER_2, depth=args.depth2, seed=None if args.seed is None else args.seed + 1)
    else:  # human-vs-human
        p1 = HumanPlayer("Player 1", player=PLAYER_1)
        p2 = HumanPlayer("Player 2", player=PLAYER_2)

    game = CLIGameLoop(
        player1=p1,
        player2=p2,
        delay_between_moves=args.delay if args.mode == "agent-vs-agent" else 0.0,
        show_metrics=not args.no_metrics,
        use_color=not args.no_color,
    )
    game.run()


if __name__ == "__main__":
    main()
