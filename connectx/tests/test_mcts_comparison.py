"""Compare MCTS vs v2: 20 seat-reversed games."""
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
from connectx.bots.mcts import mcts_bot
import random

def play_game(p1_fn, p2_fn, seed):
    """Play game. P1 is mark 1, P2 is mark 2. Returns winner mark (1, 2, or 0 for draw)."""
    random.seed(seed)
    board = connectx.make_board(7, 6)
    for turn in range(42):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 7)
        if not legal:
            return 0
        fn = p1_fn if turn % 2 == 0 else p2_fn
        action = fn(board, mark, legal, 7, 0.5, 0.0, seed + turn)
        if action not in legal:
            action = random.choice(legal)
        connectx.drop(board, action, mark)
        if connectx.check_win(board, action, mark, 6, 7, 4):
            return mark
    return 0

# MCTS vs v2: 10 games each direction
results_mcts_p1 = []
results_mcts_p2 = []

for i in range(10):
    # MCTS as P1 (mark 1)
    winner = play_game(mcts_bot, bitboard_ab_bot_v2, seed=42 + i)
    results_mcts_p1.append(winner)

    # MCTS as P2 (mark 2)
    winner = play_game(bitboard_ab_bot_v2, mcts_bot, seed=200 + i)
    results_mcts_p2.append(winner)

# Compute stats
mcts_wins = sum(1 for w in results_mcts_p1 if w == 1) + sum(1 for w in results_mcts_p2 if w == 2)
mcts_losses = sum(1 for w in results_mcts_p1 if w == 2) + sum(1 for w in results_mcts_p2 if w == 1)
draws = 20 - mcts_wins - mcts_losses

print(f"MCTS vs v2 (20 games, 10 each direction):")
print(f"  MCTS: {mcts_wins}W {mcts_losses}L {draws}D ({mcts_wins/20*100:.0f}%)")
print(f"  v2: {mcts_losses}W {mcts_wins}L {draws}D ({mcts_losses/20*100:.0f}%)")
print(f"  MCTS as P1: {sum(1 for w in results_mcts_p1 if w == 1)}/10")
print(f"  MCTS as P2: {sum(1 for w in results_mcts_p2 if w == 2)}/10")