"""
Generate behavioral cloning (BC) data for ConnectX neural network.

Generates positions from v2 vs MCTS games where v2's moves serve as
the training targets. This provides:
1. Diverse positions (MCTS plays differently than v2)
2. v2's optimal responses as labels
3. More varied board states than random games

Usage:
  python generate_bc_data.py --n-games 5000 --output training_bc_data.npz
"""

from __future__ import annotations

import os
import sys
import argparse
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from connectx.engine import (
    valid_moves, check_win, drop, ROWS, COLS,
)

try:
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
    HAS_V2 = True
except ImportError:
    HAS_V2 = False

try:
    from connectx.bots.mcts import mcts_bot
    HAS_MCTS = True
except ImportError:
    HAS_MCTS = False


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


def generate_bc_data(
    n_games: int = 5000,
    seed: int = 42,
    output_file: str = 'training_bc_data.npz',
) -> None:
    """Generate BC data from v2 vs MCTS games."""
    if not HAS_V2 or not HAS_MCTS:
        print("ERROR: Need both v2 and MCTS bots available")
        sys.exit(1)

    import random
    random.seed(seed)
    np.random.seed(seed)

    all_boards = []
    all_moves = []

    for i in range(n_games):
        board = np.zeros(ROWS * COLS, dtype=np.int8)
        current = 1
        is_v2_turn = True  # v2 always plays first

        for step in range(42):
            legal = list(valid_moves(board, COLS))
            if not legal:
                break

            if is_v2_turn:
                # v2 plays — record as training data
                mark = 1 if is_v2_turn else 2
                move = bitboard_ab_bot_v2(
                    board, current, legal, COLS, move_deadline=1.0
                )
                if move not in legal:
                    move = random.choice(legal)

                enc = encode_flat(board, current)
                all_boards.append(enc)
                all_moves.append(move)

                drop(board, move, current, ROWS, COLS)
                if check_win(board, move, current, ROWS, COLS):
                    break
                current = 3 - current
                is_v2_turn = False
            else:
                # MCTS plays — don't record (not v2's move)
                move = mcts_bot(
                    board, current, legal, COLS, move_deadline=0.5
                )
                drop(board, move, current, ROWS, COLS)
                if check_win(board, move, current, ROWS, COLS):
                    break
                current = 3 - current
                is_v2_turn = True

    # Save
    result = {
        'boards': np.array(all_boards, dtype=np.float32),
        'moves': np.array(all_moves, dtype=np.int32),
    }
    np.savez_compressed(output_file, **result)

    print(f"Generated {len(all_boards)} positions from {n_games} games")
    print(f"Move distribution: {np.bincount(all_moves, minlength=7).tolist()}")
    print(f"Saved to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-games', type=int, default=5000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=str, default='training_bc_data.npz')
    args = parser.parse_args()

    generate_bc_data(
        n_games=args.n_games,
        seed=args.seed,
        output_file=args.output,
    )