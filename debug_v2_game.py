"""Debug: play a single v2 vs v2 game."""
import sys
sys.path.insert(0, ".")

from connectx.engine import check_win, drop, valid_moves, ROWS, COLS, EMPTY
from connectx.bots import bitboard_ab_bot_fast_v2

board = [EMPTY] * 42
turn = 1
moves = []

while True:
    legal = valid_moves(board, COLS)
    if not legal:
        print("No moves left — draw")
        break

    mark = 1 if turn % 2 == 1 else 2
    col = bitboard_ab_bot_fast_v2(board, mark, legal)
    board[col] = mark

    if check_win(board, col, mark, ROWS, COLS):
        print(f"P{mark} wins in {len(moves)+1} moves")
        break

    print(f"Move {len(moves)+1}: P{mark} -> col {col}")
    moves.append((mark, col))
    turn += 1

    if all(c != EMPTY for c in board):
        print("Board full — draw")
        break