"""
Value Network Data Generator — Cycle 13.

Generates training data from v2 vs MCTS games.

Each position is stored as:
  boards[i]   : (N, 84) float — board encoding for the player who moved
  outcomes[i] : (N,) float    — game outcome from that player's perspective
                  (+1 = win, -1 = loss, 0 = draw)

This produces perspective-aware value labels from diverse positions
(MCTS creates imperfect play, so second-player outcomes are non-trivial).

Usage:
  python value_generate.py --n-games 2000 --output O:/path/value_data.npz
"""

from __future__ import annotations

import os
import sys
import argparse
import random
from pathlib import Path
from typing import List, Tuple

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


def encode(board, mark):
    """Encode board into flat 84-element feature vector."""
    opp = 3 - mark
    n = ROWS * COLS
    enc = np.zeros(2 * n, dtype=np.float32)
    for i in range(n):
        if board[i] == mark:
            enc[i] = 1.0
        elif board[i] == opp:
            enc[i + n] = 1.0
    return enc


def play_one_game(v2_mark: int, mcts_mark: int, seed: int):
    """
    Play one v2 vs MCTS game.

    Returns (winner, positions) where positions is a list of
    (encoded_board, mark) tuples.
    """
    if seed is not None:
        random.seed(seed)

    board = np.zeros(ROWS * COLS, dtype=np.int8)
    positions = []  # list of (enc, mark)
    winner = 0
    current = v2_mark

    for step in range(42):
        legal = list(valid_moves(board, COLS))
        if not legal:
            break

        if current == v2_mark:
            move = bitboard_ab_bot_v2(
                board, current, legal, COLS, move_deadline=1.0
            )
        else:
            move = mcts_bot(
                board, current, legal, COLS, move_deadline=0.5,
                seed=None,  # MCTS uses global random, don't override
            )

        if move not in legal:
            move = legal[0]

        drop(board, move, current, ROWS, COLS)
        enc = encode(board, current)
        positions.append((enc.copy(), current))

        if check_win(board, move, current, ROWS, COLS):
            winner = current
            break

        current = 3 - current

    return winner, positions


def generate_dataset(
    n_games: int = 2000,
    seed: int = 42,
    output_file: str = 'value_data.npz',
) -> dict:
    """Generate value training data from v2 vs MCTS games."""
    if not HAS_V2 or not HAS_MCTS:
        print("ERROR: Need both v2 and MCTS bots available")
        sys.exit(1)

    all_boards = []
    all_outcomes = []
    n_v2_wins = 0
    n_mcts_wins = 0
    n_draws = 0

    for i in range(n_games):
        game_seed = seed + i * 7  # offset to avoid correlation

        # Alternate: v2 plays mark 1 in one game, mark 2 in next
        v2_marks = [1, 2] * (n_games // 2 + 1)
        mcts_mark = 3 - v2_marks[i]

        winner, positions = play_one_game(v2_marks[i], mcts_mark, game_seed)

        if winner == 1:
            n_v2_wins += 1
        elif winner == 2:
            n_mcts_wins += 1
        else:
            n_draws += 1

        for enc, mark in positions:
            if winner == 0:
                outcome = 0.0
            elif winner == mark:
                outcome = 1.0
            else:
                outcome = -1.0
            all_boards.append(enc)
            all_outcomes.append(outcome)

    # Save
    result = {
        'boards': np.array(all_boards, dtype=np.float32),
        'outcomes': np.array(all_outcomes, dtype=np.float32),
    }
    np.savez_compressed(output_file, **result)

    print(f"Generated {len(all_boards)} positions from {n_games} games")
    print(f"Game outcomes: v2_wins={n_v2_wins}, mcts_wins={n_mcts_wins}, draws={n_draws}")
    outcomes = np.array(all_outcomes)
    print(f"Outcome stats: mean={outcomes.mean():.3f}, std={outcomes.std():.3f}")
    print(f"Saved to {output_file}")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate value network training data')
    parser.add_argument('--n-games', type=int, default=2000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=str, default='value_data.npz')
    args = parser.parse_args()

    generate_dataset(
        n_games=args.n_games,
        seed=args.seed,
        output_file=args.output,
    )