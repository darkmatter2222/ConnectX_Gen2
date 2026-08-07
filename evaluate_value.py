"""
Cycle 13 Evaluation: vValue bot vs baselines.

Runs seat-reversed paired evaluations:
  - vValue vs v2 (40 games)
  - vValue vs mcts (40 games)
  - v2 vs mcts (40 games, control)
  - nn_evaluator vs mcts (40 games, comparison)

Uses the trained value network from models/value_net/best.pth.
"""

from __future__ import annotations

import os
import sys
import random
import time
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from connectx.engine import play_game, play_game_seated, ROWS, COLS
from connectx.bots.bitboard_ab_improved import (
    bitboard_ab_bot_v2, bitboard_ab_bot_fast_v2,
)
from connectx.bots.bitboard_ab_value import (
    bitboard_ab_bot_vvalue, bitboard_ab_bot_vvalue_fast,
)
from connectx.bots.mcts import mcts_bot, mcts_bot_fast
from connectx.bots.nn_evaluator import evaluate as nn_evaluate, get_evaluator
from connectx.bots.connectx_value_net import get_value_net
from connectx.engine import play_game_seated, valid_moves as _valid_moves
from typing import Callable
import os
import random
COLS = 7

# ── NN-evaluated bot wrapper ──────────────────────────────────────────────────

def nn_bot(board, mark, legal, cols=COLS, move_deadline=None,
           remaining_overage=0.0, seed=None):
    """Bot that uses the trained NN evaluator (from Cycle 11/12)."""
    board_list = list(board)
    legal = list(__import__('connectx.engine', fromlist=['valid_moves']).valid_moves(board_list, cols))
    if not legal:
        return 0

    try:
        val = nn_evaluate(board_list, mark, cols)
        # Prefer center moves with highest NN value
        best_col = legal[0]
        best_val = float('-inf')
        for col in legal:
            board_list[col] = mark
            v = nn_evaluate(board_list, mark, cols)
            board_list[col] = 0
            if v > best_val:
                best_val = v
                best_col = col
        return best_col
    except Exception:
        return legal[0]


# ── Evaluation runner ────────────────────────────────────────────────────────

def run_paired_eval(
    bot1_name: str, bot1_fn: Callable,
    bot2_name: str, bot2_fn: Callable,
    n_games: int = 40,
    seed: int = 42,
) -> dict:
    """Run n_games paired evaluation (alternating seats)."""
    random.seed(seed)

    wins1, wins2, draws = 0, 0, 0
    crashes1, crashes2 = 0, 0
    total_time = 0.0

    for i in range(n_games):
        seat = 1 if i % 2 == 0 else 2
        try:
            g1, g2 = play_game_seated(bot1_fn, bot2_fn)
        except Exception as e:
            print(f"  Crash: {e}")
            crashes1 += 1
            continue

        for g in [g1, g2]:
            if g.winner == 1:
                if seat == 1:
                    wins1 += 1
                else:
                    wins2 += 1
            elif g.winner == 2:
                if seat == 2:
                    wins1 += 1
                else:
                    wins2 += 1
            else:
                draws += 1

    total = wins1 + wins2 + draws
    print(f"\n  {bot1_name} vs {bot2_name} ({n_games} games × 2 seats)")
    print(f"  {bot1_name}: {wins1} wins ({wins1/total*100:.1f}%)")
    print(f"  {bot2_name}: {wins2} wins ({wins2/total*100:.1f}%)")
    print(f"  Draws: {draws} ({draws/total*100:.1f}%)")
    print(f"  Crashes ({bot1_name}): {crashes1}")
    print(f"  Crashes ({bot2_name}): {crashes2}")

    return {'bot1_wins': wins1, 'bot2_wins': wins2, 'draws': draws,
            'total': total, 'crashes1': crashes1, 'crashes2': crashes2}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Cycle 13 Evaluation: vValue vs Baselines")
    print("=" * 60)

    # Load the value network so vValue can use it
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'value_net', 'best.pth')
    print(f"\nLoading value network from: {model_path}")
    vn = get_value_net()
    if vn is not None:
        vn.load(model_path)
        print("Value network loaded successfully")
        print(f"  Empty board value: {vn.evaluate([0]*42, 1):.4f}")
    else:
        print("WARNING: No value network available — vValue will fall back to v2")

    # ── Define bot closures ─────────────────────────────────────────────────

    def v2_bot(board, mark, legal, cols=COLS, move_deadline=None,
               remaining_overage=0.0, seed=None):
        return bitboard_ab_bot_v2(board, mark, legal, cols, move_deadline,
                                   remaining_overage, seed)

    def v2_fast_bot(board, mark, legal, cols=COLS, move_deadline=None,
                    remaining_overage=0.0, seed=None):
        return bitboard_ab_bot_fast_v2(board, mark, legal, cols, move_deadline,
                                        remaining_overage, seed)

    def vvalue_bot(board, mark, legal, cols=COLS, move_deadline=None,
                   remaining_overage=0.0, seed=None):
        return bitboard_ab_bot_vvalue(board, mark, legal, cols, move_deadline,
                                       remaining_overage, seed)

    def vvalue_fast_bot(board, mark, legal, cols=COLS, move_deadline=None,
                        remaining_overage=0.0, seed=None):
        return bitboard_ab_bot_vvalue_fast(board, mark, legal, cols, move_deadline,
                                            remaining_overage, seed)

    def mcts_fast_bot(board, mark, legal, cols=COLS, move_deadline=None,
                      remaining_overage=0.0, seed=None):
        return mcts_bot_fast(board, mark, legal, cols, move_deadline,
                              remaining_overage, seed)

    def nn_bot_wrapper(board, mark, legal, cols=COLS, move_deadline=None,
                       remaining_overage=0.0, seed=None):
        return nn_bot(board, mark, legal, cols, move_deadline,
                       remaining_overage, seed)

    # ── Run evaluations ───────────────────────────────────────────────────

    results = {}

    # vValue vs v2 (control — should be ~50/50 if NN contributes little)
    results['vvalue_vs_v2'] = run_paired_eval(
        'vValue', vvalue_bot, 'v2', v2_bot, n_games=40, seed=100)

    # vValue vs MCTS
    results['vvalue_vs_mcts'] = run_paired_eval(
        'vValue', vvalue_bot, 'MCTS', mcts_fast_bot, n_games=40, seed=200)

    # v2 vs MCTS (control)
    results['v2_vs_mcts'] = run_paired_eval(
        'v2', v2_bot, 'MCTS', mcts_fast_bot, n_games=40, seed=300)

    # NN evaluator vs MCTS (comparison)
    results['nn_vs_mcts'] = run_paired_eval(
        'NN_eval', nn_bot_wrapper, 'MCTS', mcts_fast_bot, n_games=40, seed=400)

    # ── Summary ──────────────────────────────────────────────────────────

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, r in results.items():
        total = r['total']
        bot1_pct = r['bot1_wins'] / total * 100
        bot2_pct = r['bot2_wins'] / total * 100
        draw_pct = r['draws'] / total * 100
        print(f"  {name}: {bot1_pct:.0f}% / {bot2_pct:.0f}% / {draw_pct:.0f}%D")

    print("\nDone.")


if __name__ == '__main__':
    main()