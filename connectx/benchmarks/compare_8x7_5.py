"""Compare the two 8x7/5 bot variants."""

import time
import sys
sys.path.insert(0, '.')

import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as V1
from connectx.bots.bitboard_ab_8x7_5_deep import bitboard_ab_bot_8x7_5_deep as V2


def play_game(v1_as_p1=True):
    """Play one game between the two variants."""
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if (mark == 1 and v1_as_p1) or (mark == 2 and not v1_as_p1):
            m = V1(board, mark, legal, 8, move_deadline=2.0)
        else:
            m = V2(board, mark, legal, 8, move_deadline=2.0)
        elapsed = time.time() - t0
        total_time += elapsed

        if m not in legal:
            return 'INVALID', len(moves), total_time, moves

        connectx.drop(board, m, mark, 7, 8)
        moves.append((turn + 1, mark, m, elapsed))

        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            return f"P{mark}_WINS", len(moves), total_time, moves

    return f"DRAW_{len(moves)}_moves", len(moves), total_time, moves


if __name__ == '__main__':
    print("=== 8x7/5 Variant Comparison ===")
    print(f"V1: full eval, depth 8 (faster)")
    print(f"V2: simple eval, depth 10 (deeper)")
    print()

    v1_as_p1 = True
    v1_wins_p1 = 0
    v1_wins_p2 = 0
    v2_wins_p1 = 0
    v2_wins_p2 = 0
    draws = 0
    total_moves = 0
    total_time = 0.0
    n_games = 5

    for i in range(n_games):
        result, n_moves, gt, moves = play_game(v1_as_p1=True)
        v1_as_p1 = not v1_as_p1  # alternate

        total_moves += n_moves
        total_time += gt

        if 'P1_WINS' in result:
            v1_wins_p1 += 1
            print(f"Game {i+1}: V1(P1) wins | {n_moves} moves | {total_time:.1f}s")
        elif 'P2_WINS' in result:
            v1_wins_p2 += 1
            print(f"Game {i+1}: V2(P2) wins | {n_moves} moves | {total_time:.1f}s")
        else:
            draws += 1
            print(f"Game {i+1}: DRAW ({n_moves} moves) | {total_time:.1f}s")

        # Show first 3 moves
        if len(moves) >= 3:
            print(f"  Opening: {' '.join(f'{t}:P{m}c{c}' for t, m, c, _ in moves[:3])}")
        print()

    print(f"=== Summary ({n_games} games) ===")
    print(f"V1 as P1: {v1_wins_p1}W")
    print(f"V2 as P2: {v1_wins_p2}W")
    print(f"Draws: {draws}")
    print(f"Average moves per game: {total_moves/n_games:.0f}")
    print(f"Average total time: {total_time/n_games:.1f}s")