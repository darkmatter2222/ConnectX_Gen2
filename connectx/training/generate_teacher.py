"""
Generate labeled training data using v2 alpha-beta evaluation as teacher.

For each random-player position, compute v2's evaluation (alpha-beta) and
use it as a training target. This distills v2's evaluation function into
a neural network.

The key advantage over outcome-based training:
- Each position gets a unique evaluation score (not just +1/-1/0)
- The network learns fine-grained positional patterns
- Works even with heavily biased datasets (P1 always wins)
"""

from __future__ import annotations

import os
import sys
import random
import argparse
from pathlib import Path
from typing import List, Tuple

import numpy as np

_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in os.sys.path:
    os.sys.path.insert(0, _project_root)

from connectx.engine import make_board, valid_moves, check_win, drop, ROWS, COLS

try:
    from connectx.bots.bitboard_ab_improved import _evaluate as v2_evaluate
    HAS_V2_EVAL = True
except ImportError:
    HAS_V2_EVAL = False


def encode_flat(board, mark):
    """Encode board into flat 84-element float vector."""
    opp = 3 - mark
    n = ROWS * COLS
    enc = np.zeros(2 * n, dtype=np.float32)
    for i in range(n):
        if board[i] == mark:
            enc[i] = 1.0
        elif board[i] == opp:
            enc[i + n] = 1.0
    return enc


def generate_teacher_data(
    n_games: int = 5000,
    noise: float = 0.5,
    seed: int = 42,
    output_file: str = 'training_data_teacher.npz',
) -> dict:
    """
    Generate training data where labels come from v2's evaluation.
    """
    if not HAS_V2_EVAL:
        print("v2 evaluation not available")
        return {}

    random.seed(seed)
    np.random.seed(seed)

    all_boards = []
    all_moves = []
    all_targets = []

    eval_count = 0
    for i in range(n_games):
        game_seed = seed + i
        random.seed(game_seed)

        board = np.zeros(ROWS * COLS, dtype=np.int8)
        current = 1
        winner = 0

        for _ in range(1, 43):
            legal = list(valid_moves(board, COLS))
            if not legal:
                break

            if random.random() < noise:
                col = random.choice(legal)
            else:
                scores = np.array(
                    [1.0 / (1 + abs(c - COLS // 2)) + np.random.uniform(-noise, noise)
                     for c in legal], dtype=np.float32)
                col = legal[int(np.argmax(scores))]

            drop(board, col, current, ROWS, COLS)

            enc = encode_flat(board, current)

            # v2 evaluation from current player's perspective
            v2_eval = v2_evaluate(board, current, COLS)

            # Normalize to [-1, 1] using tanh
            # v2 scores range: ~[-5000, 5000] for tactical positions
            # Scale to make most non-terminal positions fall in [-1, 1]
            target = float(np.tanh(v2_eval / 200.0))

            all_boards.append(enc)
            all_moves.append(col)
            all_targets.append(target)
            eval_count += 1

            if check_win(board, col, current, ROWS, COLS):
                winner = current
                break
            current = 3 - current

    result = {
        'boards': np.array(all_boards, dtype=np.float32),
        'moves': np.array(all_moves, dtype=np.int32),
        'targets': np.array(all_targets, dtype=np.float32),
    }
    np.savez_compressed(output_file, **result)

    targets_arr = result['targets']
    print(f"Generated {len(result['boards'])} labeled positions")
    print(f"Targets: mean={np.mean(targets_arr):.3f}, std={np.std(targets_arr):.3f}")
    print(f"Target range: [{targets_arr.min():.3f}, {targets_arr.max():.3f}]")
    print(f"+ve: {sum(1 for t in targets_arr if t > 0.1)}/{len(targets_arr)}, "
          f"-ve: {sum(1 for t in targets_arr if t < -0.1)}/{len(targets_arr)}, "
          f"neutral: {sum(1 for t in targets_arr if abs(t) <= 0.1)}/{len(targets_arr)}")
    print(f"Saved to {output_file}")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-games', type=int, default=5000)
    parser.add_argument('--noise', type=float, default=0.5)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=str, default='training_data_teacher.npz')
    args = parser.parse_args()

    generate_teacher_data(
        n_games=args.n_games,
        noise=args.noise,
        seed=args.seed,
        output_file=args.output,
    )