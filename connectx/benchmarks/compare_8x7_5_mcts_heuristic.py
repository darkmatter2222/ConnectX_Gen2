"""Compare regular MCTS vs heuristic MCTS vs AB at 8x7/5."""

import time, sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS_REG
from connectx.bots.mcts_8x7_5 import mcts_bot_heuristic_8x7_5 as MCTS_HEUR


def play_game(bot1_func, bot1_seat, bot2_func, bot2_seat):
    """Play one game between bot1 and bot2."""
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if mark == bot1_seat:
            m = bot1_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        else:
            m = bot2_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        elapsed = time.time() - t0
        total_time += elapsed

        if m not in legal:
            return 'INVALID', len(moves), total_time

        connectx.drop(board, m, mark, 7, 8)
        moves.append((turn + 1, mark, m, elapsed))

        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            return f"P{mark}_WINS", len(moves), total_time

    return f"DRAW_{len(moves)}", len(moves), total_time


if __name__ == '__main__':
    print("=== 8x7/5: Regular MCTS vs Heuristic MCTS vs AB ===")
    print()

    n_games = 10

    # Regular MCTS vs AB
    print("--- Regular MCTS (500 sims) vs AB ---")
    reg_vs_ab = {'reg': 0, 'ab': 0, 'draw': 0}
    for i in range(n_games):
        bot1 = MCTS_REG if i % 2 == 0 else AB
        seat1 = 2 if i % 2 == 0 else 1
        bot2 = AB if i % 2 == 0 else MCTS_REG
        seat2 = 1 if i % 2 == 0 else 2
        result, n, t = play_game(bot1, seat1, bot2, seat2)
        if 'P1_WINS' in result:
            if seat1 == 1:
                reg_vs_ab['reg'] += 1
            else:
                reg_vs_ab['ab'] += 1
        elif 'P2_WINS' in result:
            if seat2 == 2:
                reg_vs_ab['reg'] += 1
            else:
                reg_vs_ab['ab'] += 1
        else:
            reg_vs_ab['draw'] += 1
        print(f"  Game {i+1}: {result}")

    print(f"  Regular MCTS wins: {reg_vs_ab['reg']}, AB wins: {reg_vs_ab['ab']}, Draws: {reg_vs_ab['draw']}")
    print()

    # Heuristic MCTS vs AB
    print("--- Heuristic MCTS (500 sims) vs AB ---")
    heur_vs_ab = {'heur': 0, 'ab': 0, 'draw': 0}
    for i in range(n_games):
        bot1 = MCTS_HEUR if i % 2 == 0 else AB
        seat1 = 2 if i % 2 == 0 else 1
        bot2 = AB if i % 2 == 0 else MCTS_HEUR
        seat2 = 1 if i % 2 == 0 else 2
        result, n, t = play_game(bot1, seat1, bot2, seat2)
        if 'P1_WINS' in result:
            if seat1 == 1:
                heur_vs_ab['heur'] += 1
            else:
                heur_vs_ab['ab'] += 1
        elif 'P2_WINS' in result:
            if seat2 == 2:
                heur_vs_ab['heur'] += 1
            else:
                heur_vs_ab['ab'] += 1
        else:
            heur_vs_ab['draw'] += 1
        print(f"  Game {i+1}: {result}")

    print(f"  Heuristic MCTS wins: {heur_vs_ab['heur']}, AB wins: {heur_vs_ab['ab']}, Draws: {heur_vs_ab['draw']}")
    print()

    # Head-to-head: Regular vs Heuristic
    print("--- Regular MCTS vs Heuristic MCTS ---")
    reg_vs_heur = {'reg': 0, 'heur': 0, 'draw': 0}
    for i in range(n_games):
        bot1 = MCTS_REG if i % 2 == 0 else MCTS_HEUR
        seat1 = 2 if i % 2 == 0 else 1
        bot2 = MCTS_HEUR if i % 2 == 0 else MCTS_REG
        seat2 = 1 if i % 2 == 0 else 2
        result, n, t = play_game(bot1, seat1, bot2, seat2)
        if 'P1_WINS' in result:
            if seat1 == 1:
                reg_vs_heur['reg'] += 1
            else:
                reg_vs_heur['heur'] += 1
        elif 'P2_WINS' in result:
            if seat2 == 2:
                reg_vs_heur['reg'] += 1
            else:
                reg_vs_heur['heur'] += 1
        else:
            reg_vs_heur['draw'] += 1
        print(f"  Game {i+1}: {result}")

    print(f"  Regular MCTS wins: {reg_vs_heur['reg']}, Heuristic MCTS wins: {reg_vs_heur['heur']}, Draws: {reg_vs_heur['draw']}")