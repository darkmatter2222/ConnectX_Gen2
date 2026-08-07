"""Compare MCTS PUCT vs v2."""
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
from connectx.bots.mcts_puct import mcts_puct_bot
import random

def play_game(p1_fn, p2_fn, seed):
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

N = 10
mcts_wins = 0
mcts_losses = 0

for i in range(N):
    # MCTS PUCT as P1 vs v2 as P2
    r = play_game(mcts_puct_bot, bitboard_ab_bot_v2, seed=42 + i)
    if r == 1: mcts_wins += 1
    elif r == 2: mcts_losses += 1

for i in range(N):
    # v2 as P1 vs MCTS PUCT as P2
    r = play_game(bitboard_ab_bot_v2, mcts_puct_bot, seed=200 + i)
    if r == 1: mcts_losses += 1
    elif r == 2: mcts_wins += 1

total = N * 2
draws = total - mcts_wins - mcts_losses
print(f"MCTS PUCT vs v2 ({total} games):")
print(f"  MCTS PUCT: {mcts_wins}W {mcts_losses}L {draws}D ({mcts_wins/total*100:.0f}%)")
print(f"  v2: {mcts_losses}W {mcts_wins}L {draws}D ({mcts_losses/total*100:.0f}%)")

# Also compare timing
import time
board = connectx.make_board(7, 6)
for fn_name, fn in [("v2", bitboard_ab_bot_v2), ("mcts_puct", mcts_puct_bot)]:
    times = []
    for i in range(20):
        legal = connectx.valid_moves(board, 7)
        start = time.time()
        fn(board, 1, legal, 7, 0.5, 0.0, seed=i)
        times.append(time.time() - start)
    print(f"  {fn_name}: avg={sum(times)/len(times)*1000:.1f}ms, min={min(times)*1000:.1f}ms, max={max(times)*1000:.1f}ms")