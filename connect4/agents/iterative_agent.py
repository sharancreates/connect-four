"""Iterative Deepening Alpha-Beta Agent with a per-move time budget."""

import time

from connect4.agents.alphabeta_agent import AlphaBetaAgent, WIN


class TimeUp(Exception):
    pass


class IterativeAlphaBetaAgent(AlphaBetaAgent):

    def __init__(self, name="IterativeAlphaBeta", player=1, max_depth=10, time_limit=1.0):
        super().__init__(name=name, player=player, depth=max_depth, use_heuristic=True)
        self.max_depth = max_depth
        self.time_limit = time_limit      # seconds per move
        self.deadline = 0.0
        self.depth_reached = 0            # last depth that finished in time

    def check_time(self):
        if time.perf_counter() > self.deadline:
            raise TimeUp()

    # check the clock at every node, then do the normal alpha-beta step
    def max_value(self, board, depth, alpha, beta):
        self.check_time()
        return super().max_value(board, depth, alpha, beta)

    def min_value(self, board, depth, alpha, beta):
        self.check_time()
        return super().min_value(board, depth, alpha, beta)

    def search_root(self, board, moves, depth):
        best_score = float("-inf")
        best_move = moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for col in moves:
            board.make_move(col)
            score = self.min_value(board, depth - 1, alpha, beta)
            board.undo_move(col)

            if score > best_score:
                best_score = score
                best_move = col

            alpha = max(alpha, best_score)

        return best_move, best_score

    def select_move(self, board):
        moves = self.order_moves(board.get_legal_moves())
        if not moves:
            raise ValueError("No legal moves available.")

        if len(moves) == 1:
            self.nodes_expanded += 1
            return moves[0]

        self.deadline = time.perf_counter() + self.time_limit
        self.depth_reached = 0
        best_move = moves[0]

        for depth in range(1, self.max_depth + 1):
            try:
                # search a copy, so a timeout in the middle cannot leave the real board changed
                move, score = self.search_root(board.copy(), moves, depth)
            except TimeUp:
                break

            best_move = move
            self.depth_reached = depth

            # forced win found, no need to go deeper
            if score >= WIN:
                break

            # try the best move of this depth first at the next depth
            moves.remove(best_move)
            moves.insert(0, best_move)

        return best_move
