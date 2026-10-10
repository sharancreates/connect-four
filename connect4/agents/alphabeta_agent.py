"""Alpha-Beta Agent for Connect Four (same as plain Minimax, but with pruning)."""
from connect4.core.board import COLS
from connect4.agents.base import Agent

WIN = 100000
LOSS = -100000
DRAW = 0


class AlphaBetaAgent(Agent):

    def __init__(self, name="AlphaBeta", player=1, depth=4):
        super().__init__(name=name, player=player)
        self.depth = depth

    def order_moves(self, moves):
        # center columns first, pruning works better when good moves come first
        center = COLS // 2
        return sorted(moves, key=lambda c: abs(c - center))

    def select_move(self, board):
        moves = self.order_moves(board.get_legal_moves())
        if not moves:
            raise ValueError("No legal moves available.")

        # only one choice, no need to search
        if len(moves) == 1:
            self.nodes_expanded += 1
            return moves[0]

        best_score = float("-inf")
        best_move = moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for col in moves:
            board.make_move(col)
            score = self.min_value(board, self.depth - 1, alpha, beta)
            board.undo_move(col)

            if score > best_score:
                best_score = score
                best_move = col

            alpha = max(alpha, best_score)

        return best_move

    def max_value(self, board, depth, alpha, beta):
        self.nodes_expanded += 1

        # terminal check (same scoring as plain minimax)
        if board._winner == self.player:
            return WIN + depth
        elif board._winner == -self.player:
            return LOSS - depth
        elif board._is_terminal:
            return DRAW

        if depth <= 0:
            return self.evaluate(board)

        moves = self.order_moves(board.get_legal_moves())
        if not moves:
            return DRAW

        value = float("-inf")
        for col in moves:
            board.make_move(col)
            value = max(value, self.min_value(board, depth - 1, alpha, beta))
            board.undo_move(col)

            # opponent will never allow this branch, stop looking
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, board, depth, alpha, beta):
        self.nodes_expanded += 1

        if board._winner == self.player:
            return WIN + depth
        elif board._winner == -self.player:
            return LOSS - depth
        elif board._is_terminal:
            return DRAW

        if depth <= 0:
            return self.evaluate(board)

        moves = self.order_moves(board.get_legal_moves())
        if not moves:
            return DRAW

        value = float("inf")
        for col in moves:
            board.make_move(col)
            value = min(value, self.max_value(board, depth - 1, alpha, beta))
            board.undo_move(col)

            # we already have a better option elsewhere, stop looking
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def evaluate(self, board):
        # same simple heuristic as plain minimax for now (center control)
        # the proper heuristic comes in the next step
        center_col = board.grid[:, COLS // 2]
        mine = int((center_col == self.player).sum())
        theirs = int((center_col == -self.player).sum())
        return (mine - theirs) * 3.0
