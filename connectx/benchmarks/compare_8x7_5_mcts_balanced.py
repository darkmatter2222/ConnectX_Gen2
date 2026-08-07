"""Balanced 20-game MCTS vs AB comparison."""

import time, sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS

ab_p1 = 0
ab_p2 = 0
mcts_p1 = 0
mcts_p2 = 0
draws = 0
total_time = 0.0
total_moves = 0
n_games = 20

for i in range(n_games):
    # Alternate: even = AB as P1, odd = MCTS as P1
    mcts_as_p1 = (i % 2 == 1)

    board = connectx.make_board(7, 8)
    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        if (mark == 1 and not mcts_as_p1) or (mark == 2 and mcts_as_p1):
            m = AB(board, mark, legal, 8, move_deadline=2.0)
        else:
            m = MCTS(board, mark, legal, 8, move_deadline=2.0, num_simulations=500)
        if m not in legal:
            break
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            if not mcts_as_p1:
                if mark == 1:
                    ab_p1 += 1
                else:
                    mcts_p2 += 1
            else:
                if mark == 1:
                    mcts_p1 += 1
                else:
                    ab_p2 += 1
            break
    else:
        draws += 1
    total_moves += turn + 1

print(f"AB as P1: {ab_p1}")
print(f"AB as P2: {ab_p2}")
print(f"MCTS as P1: {mcts_p1}")
print(f"MCTS as P2: {mcts_p2}")
print(f"Draws: {draws}")
print(f"Avg moves/game: {total_moves/n_games:.0f}")
print()

# Overall AB win rate (excluding draws)
ab_decisive = ab_p1 + ab_p2
mcts_decisive = mcts_p1 + mcts_p2
draw_games = draws
print(f"AB decisive wins: {ab_decisive}/{ab_decisive + mcts_p1}")
print(f"MCTS decisive wins: {mcts_p1}/{mcts_p1 + ab_p2}")
if ab_decisive > 0:
    print(f"AB as P1 win rate: {ab_p1 / max(1, ab_p1 + mcts_p2):.0%}")
if mcts_decisive > 0:
    print(f"MCTS as P1 win rate: {mcts_p1 / max(1, mcts_p1 + ab_p2):.0%}")