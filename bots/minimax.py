"""
ConnectX Bot with Minimax + Alpha-Beta Pruning

This bot implements a minimax search with alpha-beta pruning and
positional evaluation for the Connect X (Connect Four) game.

Key techniques:
1. Center column preference
2. Evaluation of 4-in-a-row windows
3. Alpha-beta pruning for efficient search
4. Win/block detection as first priority
5. Depth-limited search for performance
"""
import sys
sys.setrecursionlimit(100000)


class ConnectXBot:
    def __init__(self):
        self.search_depth = 8  # Default search depth

    def step(self, obs, config):
        cols = config["columns"]
        rows = config["rows"]
        inarow = config["inarow"]
        mark = obs["mark"]
        opp = 3 - mark  # opponent's mark

        def board_2d(obs):
            """Convert flat board to 2D array. board[r][c]"""
            b = [[0] * cols for _ in range(rows)]
            for idx, v in enumerate(obs["board"]):
                if v != 0:
                    b[idx // cols][idx % cols] = v
            return b

        def drop(b, col, piece):
            """Drop piece in column, returns row index or -1 if full"""
            for r in range(rows):
                if b[r][col] == 0:
                    b[r][col] = piece
                    return r
            return -1

        def remove_piece(b, col):
            """Remove top piece from column"""
            for r in range(rows - 1, -1, -1):
                if b[r][col] != 0:
                    b[r][col] = 0
                    return True
            return False

        def is_valid(b, col):
            """Check if column is valid (not full)"""
            return col < cols and b[rows - 1][col] == 0

        def winning(b, piece):
            """Check if piece wins on board"""
            # Horizontal
            for r in range(rows):
                for c in range(cols - inarow + 1):
                    if all(b[r][c + i] == piece for i in range(inarow)):
                        return True
            # Vertical
            for c in range(cols):
                for r in range(rows - inarow + 1):
                    if all(b[r + i][c] == piece for i in range(inarow)):
                        return True
            # Diagonal /
            for r in range(rows - inarow + 1):
                for c in range(cols - inarow + 1):
                    if all(b[r + i][c + i] == piece for i in range(inarow)):
                        return True
            # Diagonal \
            for r in range(inarow - 1, rows):
                for c in range(cols - inarow + 1):
                    if all(b[r - i][c + i] == piece for i in range(inarow)):
                        return True
            return False

        def get_valid_cols(b):
            """Get all valid column indices"""
            return [c for c in range(cols) if is_valid(b, c)]

        def evaluate(b, piece):
            """Evaluate board position for the given piece"""
            score = 0

            # Center column preference
            center = cols // 2
            center_col = [b[r][center] for r in range(rows)]
            center_count = center_col.count(piece)
            score += center_count * 3

            # Score all possible windows of length inarow
            # Horizontal
            for r in range(rows):
                for c in range(cols - inarow + 1):
                    window = [b[r][c + i] for i in range(inarow)]
                    score += self._score_window(window, piece, opp)

            # Vertical
            for c in range(cols):
                for r in range(rows - inarow + 1):
                    window = [b[r + i][c] for i in range(inarow)]
                    score += self._score_window(window, piece, opp)

            # Diagonal /
            for r in range(rows - inarow + 1):
                for c in range(cols - inarow + 1):
                    window = [b[r + i][c + i] for i in range(inarow)]
                    score += self._score_window(window, piece, opp)

            # Diagonal \
            for r in range(inarow - 1, rows):
                for c in range(cols - inarow + 1):
                    window = [b[r - i][c + i] for i in range(inarow)]
                    score += self._score_window(window, piece, opp)

            return score

        def _score_window(window, piece, opp):
            """Score a window of length inarow"""
            count_piece = window.count(piece)
            count_empty = window.count(0)
            count_opp = window.count(opp)

            if count_piece == 4:
                return 100
            elif count_piece == 3 and count_empty == 1:
                return 5
            elif count_piece == 2 and count_empty == 2:
                return 2

            if count_opp == 3 and count_empty == 1:
                return -3

            return 0

        def minimax(b, depth, alpha, beta, maximizing, piece, opp):
            """Minimax with alpha-beta pruning"""
            valid = get_valid_cols(b)

            if depth == 0 or not valid:
                if winning(b, piece):
                    return 1000000 if maximizing else -1000000
                if winning(b, opp):
                    return -1000000 if maximizing else 1000000
                return evaluate(b, piece)

            if maximizing:
                max_eval = -float('inf')
                # Check for winning move first
                for col in valid:
                    r = drop(b, col, piece)
                    if r != -1:
                        if winning(b, piece):
                            remove_piece(b, col)
                            return 1000000
                        eval = minimax(b, depth - 1, alpha, beta, False, piece, opp)
                        remove_piece(b, col)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if alpha >= beta:
                            break
                return max_eval
            else:
                min_eval = float('inf')
                # Check for winning move first
                for col in valid:
                    r = drop(b, col, opp)
                    if r != -1:
                        if winning(b, opp):
                            remove_piece(b, col)
                            return -1000000
                        eval = minimax(b, depth - 1, alpha, beta, True, piece, opp)
                        remove_piece(b, col)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if alpha >= beta:
                            break
                return min_eval

        board = board_2d(obs)
        valid = get_valid_cols(board)

        if not valid:
            return 0

        # Check if we can win now
        for col in valid:
            temp = [row[:] for row in board]
            drop(temp, col, mark)
            if winning(temp, mark):
                return col

        # Check if opponent can win and we need to block
        for col in valid:
            temp = [row[:] for row in board]
            drop(temp, col, opp)
            if winning(temp, opp):
                return col

        # Minimax search
        best_score = -float('inf')
        best_move = valid[0]

        # Order moves: try center columns first for better pruning
        sorted_valid = sorted(valid, key=lambda c: abs(c - cols // 2))

        for col in sorted_valid:
            temp = [row[:] for row in board]
            drop(temp, col, mark)
            score = minimax(temp, self.search_depth, -float('inf'), float('inf'), False, mark, opp)
            remove_piece(temp, col)

            if score > best_score:
                best_score = score
                best_move = col

        return best_move


# Kaggle agent function
def agent(obs, config):
    bot = ConnectXBot()
    return bot.step(obs, config)