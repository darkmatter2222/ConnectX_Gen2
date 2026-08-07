"""Debug v2 vs v2 with board state after each move."""
import sys
sys.path.insert(0, ".")

from connectx.engine import check_win, drop, valid_moves, ROWS, COLS, EMPTY
from connectx.bots import bitboard_ab_bot_fast_v2

board = [EMPTY] * 42
turn = 1

while True:
    legal = valid_moves(board, COLS)
    print(f"\nTurn {turn}: legal={legal}, empty_cells={board.count(EMPTY)}")
    print(f"  Top row (0-6): {board[0:7]}")
    print(f"  Bottom row (35-41): {board[35:42]}")

    if not legal:
        print("No moves left")
        break

    mark = 1 if turn % 2 == 1 else 2
    col = bitboard_ab_bot_fast_v2(board, mark, legal)
    print(f"  Bot({mark}) chose col {col}")

    # Verify it was in legal
    assert col in legal, f"Bot chose {col} but legal was {legal}"

    row = drop(board, col, mark, ROWS, COLS)
    print(f"  Dropped at row {row}, cell index {row * COLS + col}")
    print(f"  Top row after: {board[0:7]}")
    print(f"  Bottom row after: {board[35:42]}")

    if check_win(board, col, mark, ROWS, COLS):
        print(f"P{mark} WINS at row {row}!")
        break

    turn += 1
    if all(c != EMPTY for c in board):
        print("Board full")
        break

    if turn > 50:
        print("Too many moves, stopping")
        break