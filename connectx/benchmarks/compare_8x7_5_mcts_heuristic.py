"""Compare heuristic MCTS vs regular MCTS at 8x7/5."""

import time
import sys
sys.path.insert(0, '.')

import connectx
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS
from connectx.bots.mcts_8x7_5 import mcts_bot_heuristic_8x7_5 as MCTS_H

def play_game(mcts_type='regular'):
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if mark == 1:
            if mcts_type == 'heuristic':
                m = MCTS_H(board, mark, legal, 8, move_deadline=2.0, num_simulations=500, seed=turn)
            else:
                m = MCTS(board, mark, legal, 8, move_deadline=2.0, num_simulations=500, seed=turn)
        else:
            if mcts_type == 'heuristic':
                m = MCTS_H(board, mark, legal, 8, move_deadline=2.0, num_simulations=500, seed=turn)
            else:
                m = MCTS(board, mark, legal, 8, move_deadline=2.0, num_simulations=500, seed=turn)
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
    print("=== Heuristic MCTS vs Regular MCTS (8x7/5, 500 sims) ===")
    print(f"Regular: piece-count playout termination")
    print(f"Heuristic: positional heuristic (center+height+adjacency)")
    print()

    reg_wins = 0
    heur_wins = 0
    draws = 0
    n_games = 5

    for i in range(n_games):
        mcts_type = 'heuristic' if i % 2 == 0 else 'regular'
        result, n_moves, gt, moves = play_game(mcts_type)

        if result == 'INVALID':
            print(f"Game {i+1}: INVALID")
        elif 'P1_WINS' in result:
            if mcts_type == 'heuristic':
                heur_wins += 1
                print(f"Game {i+1}: Heuristic(P1) wins | {n_moves} moves | {gt:.1f}s")
            else:
                reg_wins += 1
                print(f"Game {i+1}: Regular(P1) wins | {n_moves} moves | {gt:.1f}s")
        elif 'P2_WINS' in result:
            if mcts_type == 'heuristic':
                heur_wins += 1
                print(f"Game {i+1}: Heuristic(P2) wins | {n_moves} moves | {gt:.1f}s")
            else:
                reg_wins += 1
                print(f"Game {i+1}: Regular(P2) wins | {n_moves} moves | {gt:.1f}s")
        else:
            draws += 1
            print(f"Game {i+1}: DRAW ({n_moves} moves) | {gt:.1f}s")

    print()
    print(f"=== Summary ({n_games} games) ===")
    print(f"Regular MCTS wins: {reg_wins}")
    print(f"Heuristic MCTS wins: {heur_wins}")
    print(f"Draws: {draws}")