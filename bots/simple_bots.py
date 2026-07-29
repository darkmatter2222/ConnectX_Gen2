# Simple Bot Examples

## Bot 1: Random Bot (baseline)
```python
import random
from kaggle_environments import make

def agent(obs, config):
    # Get valid moves (columns not full)
    valid_moves = [c for c in range(config["columns"]) if obs["board"][c] != 0]
    if not valid_moves:
        return 0  # fallback
    return random.choice(valid_moves)
```

## Bot 2: Smart Bot (greedy — always center)
```python
from kaggle_environments import make

def agent(obs, config):
    cols = config["columns"]
    # Try to play in the center, bias toward center
    for offset in range(cols):
        c = cols // 2 - offset
        if c < 0:
            c = cols - c
        if c < cols and obs["board"][c] != 0:
            return c
    # Fallback: first valid move
    for c in range(cols):
        if obs["board"][c] != 0:
            return c
    return 0
```

## Bot 3: Minimax with Alpha-Beta Pruning
```python
import sys
sys.setrecursionlimit(10000)

def agent(obs, config):
    cols = config["columns"]
    rows = config["rows"]
    inarow = config["inarow"]
    mark = obs["mark"]
    opp = 3 - mark  # if mark=1, opp=2; if mark=2, opp=1

    def make_board(obs):
        board = [[0] * cols for _ in range(rows)]
        for idx, val in enumerate(obs["board"]):
            if val != 0:
                r = idx // cols
                c = idx % cols
                board[r][c] = val
        return board

    def drop_piece(board, col, piece):
        for r in range(rows):
            if board[r][col] == 0:
                board[r][col] = piece
                return r
        return -1

    def winning_move(board, piece):
        # Check horizontal
        for r in range(rows):
            for c in range(cols - inarow + 1):
                if all(board[r][c+i] == piece for i in range(inarow)):
                    return True
        # Check vertical
        for c in range(cols):
            for r in range(rows - inarow + 1):
                if all(board[r+i][c] == piece for i in range(inarow)):
                    return True
        # Check diagonal (positive slope)
        for r in range(rows - inarow + 1):
            for c in range(cols - inarow + 1):
                if all(board[r+i][c+i] == piece for i in range(inarow)):
                    return True
        # Check diagonal (negative slope)
        for r in range(inarow - 1, rows):
            for c in range(cols - inarow + 1):
                if all(board[r-i][c+i] == piece for i in range(inarow)):
                    return True
        return False

    def get_valid_locs(board):
        valid = []
        for c in range(cols):
            if board[rows-1][c] == 0:
                valid.append(c)
        return valid

    def score_pos(board, piece):
        score = 0
        center_array = [board[r][cols//2] for r in range(rows)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for r in range(rows):
            row_array = [board[r][c] for c in range(cols)]
            for c in range(cols - inarow + 1):
                window = row_array[c:c+inarow]
                score += evaluate_window(window, piece)

        # Vertical
        for c in range(cols):
            col_array = [board[r][c] for r in range(rows)]
            for r in range(rows - inarow + 1):
                window = col_array[r:r+inarow]
                score += evaluate_window(window, piece)

        # Diagonal
        for r in range(rows - inarow + 1):
            for c in range(cols - inarow + 1):
                window = [board[r+i][c+i] for i in range(inarow)]
                score += evaluate_window(window, piece)
        for r in range(inarow - 1, rows):
            for c in range(cols - inarow + 1):
                window = [board[r-i][c+i] for i in range(inarow)]
                score += evaluate_window(window, piece)

        return score

    def evaluate_window(window, piece):
        score = 0
        opp_piece = 3 - piece if piece == 1 or piece == 2 else (1 if piece == 2 else 2)

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 3

        return score

    board = make_board(obs)
    valid_moves = get_valid_locs(board)

    if not valid_moves:
        return 0

    # Check for winning move
    for col in valid_moves:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, col, mark)
        if winning_move(temp_board, mark):
            return col

    # Check for blocking move
    for col in valid_moves:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, col, opp)
        if winning_move(temp_board, opp):
            return col

    # Score each possible move and pick best
    best_score = -float('inf')
    best_moves = []
    for col in valid_moves:
        temp_board = [row[:] for row in board]
        r = drop_piece(temp_board, col, mark)
        score = score_pos(temp_board, mark)
        if score > best_score:
            best_score = score
            best_moves = [col]
        elif score == best_score:
            best_moves.append(col)

    return best_moves[0]