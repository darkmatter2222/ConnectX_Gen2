"""Compare MCTS vs Alpha-Beta at 8x7/5."""

import time
import sys
sys.path.insert(0, '.')

import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS


def play_game(mcts_as_p1=False):
    """Play one game: AB vs MCTS."""
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if (mark == 1 and not mcts_as_p1) or (mark == 2 and mcts_as_p1):
            m = AB(board, mark, legal, 8, move_deadline=2.0)
        else:
            m = MCTS(board, mark, legal, 8, move_deadline=2.0, num_simulations=300)
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
    print("=== 8x7/5: MCTS vs Alpha-Beta (full eval, depth 8) ===")
    print(f"AB: full eval, depth 8")
    print(f"MCTS: 300 simulations per move, UCB1")
    print()

    ab_wins_p1 = 0
    ab_wins_p2 = 0
    mcts_wins_p1 = 0
    mcts_wins_p2 = 0
    draws = 0
    total_moves = 0
    total_time = 0.0
    n_games = 5

    for i in range(n_games):
        mcts_as_p1 = (i % 2 == 1)
        result, n_moves, gt, moves = play_game(mcts_as_p1=mcts_as_p1)
        total_moves += n_moves
        total_time += gt

        if result == 'INVALID':
            print(f"Game {i+1}: INVALID MOVE")
        elif 'P1_WINS' in result:
            if not mcts_as_p1:
                ab_wins_p1 += 1
                print(f"Game {i+1}: AB(P1) wins | {n_moves} moves | {gt:.1f}s")
            else:
                mcts_wins_p1 += 1
                print(f"Game {i+1}: MCTS(P1) wins | {n_moves} moves | {gt:.1f}s")
        elif 'P2_WINS' in result:
            if mcts_as_p1:
                mcts_wins_p2 += 1
                print(f"Game {i+1}: MCTS(P2) wins | {n_moves} moves | {gt:.1f}s")
            else:
                ab_wins_p2 += 1
                print(f"Game {i+1}: AB(P2) wins | {n_moves} moves | {gt:.1f}s")
        else:
            draws += 1
            print(f"Game {i+1}: DRAW ({n_moves} moves) | {gt:.1f}s")

        if len(moves) >= 3:
            print(f"  Opening: {' '.join(f'{t}:P{m}c{c}' for t, m, c, _ in moves[:3])}")
        print()

    print(f"=== Summary ({n_games} games) ===")
    print(f"AB as P1: {ab_wins_p1}W")
    print(f"AB as P2: {ab_wins_p2}W")
    print(f"MCTS as P1: {mcts_wins_p1}W")
    print(f"MCTS as P2: {mcts_wins_p2}W")
    print(f"Draws: {draws}")
    print(f"Average moves per game: {total_moves/n_games:.0f}")
    print(f"Average total time: {total_time/n_games:.1f}s")