"""Monte Carlo Tree Search (MCTS) Agent for Connect Four.

Implements selection via UCT (Upper Confidence bound applied to Trees),
random rollout simulation policy, and backpropagation with dual-mode budgeting
(fixed simulation count and wall-clock time limit).
"""

from __future__ import annotations
import math
import random
import time
from typing import Dict, List, Optional
from connect4.core.board import Board, PLAYER_1, PLAYER_2, COLS
from connect4.agents.base import Agent


class MCTSNode:
    """A node in the Monte Carlo Search Tree representing a board configuration."""

    def __init__(
        self,
        state: Board,
        move: Optional[int] = None,
        parent: Optional[MCTSNode] = None,
        player_who_moved: Optional[int] = None,
    ):
        """Initialize tree node.

        Args:
            state: Board state at this node.
            move: Column action taken to reach this node from parent.
            parent: Parent MCTSNode.
            player_who_moved: The player token who made the move to reach this state.
        """
        self.state: Board = state
        self.move: Optional[int] = move
        self.parent: Optional[MCTSNode] = parent
        self.player_who_moved: int = player_who_moved if player_who_moved is not None else -state.current_player
        self.children: Dict[int, MCTSNode] = {}
        self.untried_moves: List[int] = state.get_legal_moves() if not state.is_terminal() else []
        self.visits: int = 0
        self.total_value: float = 0.0

    def is_fully_expanded(self) -> bool:
        """Check if all legal actions from this state have child nodes."""
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        """Check if node corresponds to a game-over terminal state."""
        return self.state.is_terminal()

    def best_child(self, c_param: float = 1.414, rng: Optional[random.Random] = None) -> MCTSNode:
        """Select child node with maximum UCT score.

        UCT = (w_i / n_i) + c_param * sqrt(2 * ln(N) / n_i)
        """
        best_score = float("-inf")
        best_children: List[MCTSNode] = []

        for child in self.children.values():
            if child.visits == 0:
                return child

            # Exploitation: win-rate from perspective of the player choosing this child
            exploitation = child.total_value / child.visits
            # Exploration
            exploration = c_param * math.sqrt((2.0 * math.log(self.visits)) / child.visits)
            uct_score = exploitation + exploration

            if uct_score > best_score:
                best_score = uct_score
                best_children = [child]
            elif math.isclose(uct_score, best_score, rel_tol=1e-7):
                best_children.append(child)

        choice_fn = rng.choice if rng is not None else random.choice
        return choice_fn(best_children)


class MCTSAgent(Agent):
    """Autonomous agent powered by Monte Carlo Tree Search with UCT."""

    def __init__(
        self,
        name: str = "MCTSAgent",
        player: int = PLAYER_1,
        simulations: int = 500,
        time_limit: Optional[float] = None,
        exploration_constant: float = 1.414,
        seed: Optional[int] = None,
    ):
        """Initialize MCTS Agent.

        Args:
            name: Identifier name.
            player: Assigned player token (PLAYER_1 = 1, PLAYER_2 = -1).
            simulations: Number of MCTS rollout iterations per move.
            time_limit: Optional wall-clock time limit in seconds per move.
            exploration_constant: Exploration factor Cp (default sqrt(2) approx 1.414).
            seed: Optional random seed for reproducible rollouts.
        """
        super().__init__(name=name, player=player)
        self.simulations: int = simulations
        self.time_limit: Optional[float] = time_limit
        self.exploration_constant: float = exploration_constant
        self.rng = random.Random(seed)

    def select_move(self, board: Board) -> int:
        """Select optimal move using MCTS tree search.

        Args:
            board: Current game board.

        Returns:
            Column index of chosen action.
        """
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves available.")

        # Single legal move: play directly
        if len(legal_moves) == 1:
            self.nodes_expanded += 1
            return legal_moves[0]

        # Tactical sanity check: if an immediate winning move exists, take it!
        for col in legal_moves:
            b_copy = board.copy()
            b_copy.make_move(col)
            if b_copy.get_winner() == self.player:
                self.nodes_expanded += 1
                return col

        # Tactical defense: if opponent would win on immediate next ply, block it!
        opponent = -self.player
        for col in legal_moves:
            b_copy = board.copy()
            b_copy.current_player = opponent
            b_copy.make_move(col)
            if b_copy.get_winner() == opponent:
                self.nodes_expanded += 1
                return col

        root = MCTSNode(
            state=board.copy(),
            player_who_moved=-board.current_player,
        )

        iteration = 0
        start_time = time.perf_counter()

        def budget_available() -> bool:
            if self.time_limit is not None:
                return (time.perf_counter() - start_time) < self.time_limit
            return iteration < self.simulations

        while budget_available():
            iteration += 1

            # 1. Selection
            node = root
            while node.is_fully_expanded() and not node.is_terminal():
                node = node.best_child(self.exploration_constant, rng=self.rng)

            # 2. Expansion
            if not node.is_terminal() and node.untried_moves:
                move = node.untried_moves.pop(self.rng.randrange(len(node.untried_moves)))
                next_state = node.state.copy()
                next_state.make_move(move)
                child_node = MCTSNode(
                    state=next_state,
                    move=move,
                    parent=node,
                    player_who_moved=node.state.current_player,
                )
                node.children[move] = child_node
                node = child_node

            # 3. Simulation (Rollout)
            rollout_state = node.state.copy()
            winner = self._simulate_rollout(rollout_state)
            self.nodes_expanded += 1

            # 4. Backpropagation
            curr: Optional[MCTSNode] = node
            while curr is not None:
                curr.visits += 1
                if winner == curr.player_who_moved:
                    curr.total_value += 1.0
                elif winner == -curr.player_who_moved:
                    curr.total_value -= 1.0
                curr = curr.parent

        if not root.children:
            return self.rng.choice(legal_moves)

        # Most-visited child is the robust decision
        best_child_node = max(root.children.values(), key=lambda c: c.visits)
        assert best_child_node.move is not None
        return best_child_node.move

    def _simulate_rollout(self, state: Board) -> Optional[int]:
        """Perform a random simulation rollout until terminal state."""
        max_depth = 42
        depth = 0
        while not state.is_terminal() and depth < max_depth:
            depth += 1
            legal = state.get_legal_moves()
            if not legal:
                break
            move = self.rng.choice(legal)
            state.make_move(move)
        return state.get_winner()
