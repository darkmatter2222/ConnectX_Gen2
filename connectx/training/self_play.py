"""
Self-play dataset generator for ConnectX neural network training.

Two modes:
  1. Random self-play: both players make random moves (high exploration)
  2. Strategic self-play: both players use v2 alpha-beta (competitive)

Architecture: 84 inputs (two 7x6 channels) -> 128 hidden -> 1 output (tanh)
"""

from __future__ import annotations

import os
import sys
import random
import argparse
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in os.sys.path:
    os.sys.path.insert(0, _project_root)

from connectx.engine import make_board, valid_moves, check_win, drop, ROWS, COLS

try:
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
    HAS_V2 = True
except ImportError:
    HAS_V2 = False


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


def play_game_random(
    mark_1: int = 1, mark_2: int = 2,
    noise: float = 0.3, seed: Optional[int] = None,
) -> Tuple[List[Tuple], int]:
    """
    Play one random game.

    Returns: (list of (enc, move_col), winner) where winner is 1, 2, or 0.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    board = np.zeros(ROWS * COLS, dtype=np.int8)
    moves = []
    current = mark_1
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
        moves.append((enc.copy(), col))

        if check_win(board, col, current, ROWS, COLS):
            winner = current
            break

        current = 3 - current

    return moves, winner


def play_game_strategic(
    mark_1: int = 1, mark_2: int = 2,
    seed: Optional[int] = None,
) -> Tuple[List[Tuple], int]:
    """Play one game with v2 alpha-beta vs v2 alpha-beta."""
    if not HAS_V2:
        raise RuntimeError("v2 bot not available")

    if seed is not None:
        random.seed(seed)

    board = np.zeros(ROWS * COLS, dtype=np.int8)
    moves = []
    current = mark_1
    winner = 0

    for _ in range(1, 43):
        legal = list(valid_moves(board, COLS))
        if not legal:
            break

        col = bitboard_ab_bot_v2(
            board, current, legal, COLS, move_deadline=0.5
        )
        if col not in legal:
            col = legal[0]

        drop(board, col, current, ROWS, COLS)

        enc = encode_flat(board, current)
        moves.append((enc.copy(), col))

        if check_win(board, col, current, ROWS, COLS):
            winner = current
            break

        current = 3 - current

    return moves, winner


def generate_dataset(
    n_games: int = 1000,
    noise: float = 0.3,
    seed: int = 42,
    output_file: str = 'training_data.npz',
    strategic: bool = False,
) -> dict:
    """
    Generate ConnectX training data.

    Each position is stored as:
      boards[i]   : (N, 84) float — board encoding for player who moved
      moves[i]    : (N,) int — column index of move taken
      outcomes[i] : (N,) float — z-score: +1 win, -1 loss, 0 draw
    """
    random.seed(seed)
    np.random.seed(seed)

    play_fn = play_game_strategic if strategic else play_game_random

    all_boards = []
    all_moves = []
    all_outcomes = []

    for i in range(n_games):
        game_seed = seed + i
        moves, winner = play_fn(seed=game_seed)

        for j, (enc, col) in enumerate(moves):
            # Determine perspective
            player_turn = 1 if (j % 2 == 0) else -1

            if winner == 1:
                z = 1.0 if player_turn == 1 else -1.0
            elif winner == 2:
                z = -1.0 if player_turn == 1 else 1.0
            else:
                z = 0.0

            all_boards.append(enc)
            all_moves.append(col)
            all_outcomes.append(z)

    # Save
    result = {
        'boards': np.array(all_boards, dtype=np.float32),
        'moves': np.array(all_moves, dtype=np.int32),
        'outcomes': np.array(all_outcomes, dtype=np.float32),
    }
    np.savez_compressed(output_file, **result)

    n_wins = sum(1 for o in all_outcomes if abs(o) == 1.0)
    n_draws = sum(1 for o in all_outcomes if o == 0.0)
    print(f"Generated {len(result['boards'])} positions from {n_games} games")
    print(f"Win rate: {n_wins}/{len(all_outcomes)} = {n_wins/len(all_outcomes)*100:.0f}%")
    print(f"Draw rate: {n_draws}/{len(all_outcomes)} = {n_draws/len(all_outcomes)*100:.0f}%")
    if len(all_outcomes) > 0:
        print(f"Outcome std: {np.std(all_outcomes):.3f}, mean: {np.mean(all_outcomes):.3f}")
    print(f"Saved to {output_file}")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-games', type=int, default=1000)
    parser.add_argument('--noise', type=float, default=0.3)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=str, default='training_data.npz')
    parser.add_argument('--strategic', action='store_true')
    args = parser.parse_args()

    generate_dataset(
        n_games=args.n_games,
        noise=args.noise,
        seed=args.seed,
        output_file=args.output,
        strategic=args.strategic,
    )