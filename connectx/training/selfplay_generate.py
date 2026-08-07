"""Self-play data generator for value network refinement.

Generates balanced games by running v2 against v2 (seat-reversed).
This produces balanced outcomes (~50% W / 50% L) since both players
are equal strength — unlike v2-vs-MCTS which has first-player bias.

Usage:
    python connectx/training/selfplay_generate.py \
        --games 100 \
        --output data/selfplay_positions.csv \
        --seed 42
"""

from __future__ import annotations

import csv
import sys
import argparse
import random
import time
from pathlib import Path

sys.path.insert(0, ".")

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW, EMPTY,
)
from connectx.bots import bitboard_ab_bot_fast_v2


def play_game(
    seed: int = None,
    noise: float = 0.05,
    verbose: bool = False,
) -> tuple[list[tuple[str, int]], str]:
    """
    Play a single self-play game between two v2 bots (seat-reversed).

    Returns:
        (positions, outcome)
        - positions: list of (board_str, mark) tuples
          where mark = player to move at that position
        - outcome: 'W' if P1 won, 'L' if P2 won, 'D' if draw
    """
    if seed is not None:
        random.seed(seed)

    board = [EMPTY] * (ROWS * COLS)
    moves = []
    turn = 1  # P1's turn

    while True:
        legal = valid_moves(board, COLS)
        if not legal:
            break

        if turn % 2 == 1:
            mark = 1
        else:
            mark = 2

        # Record position before move (board state, whose turn)
        bstr = ''.join(str(c) for c in board)
        moves.append((bstr, mark))

        # Use v2 bot with optional noise (occasionally pick 2nd-best move)
        if noise > 0 and random.random() < noise:
            # Play a random legal move (noise)
            col = random.choice(legal)
        else:
            col = bitboard_ab_bot_fast_v2(
                board, mark, legal,
                move_deadline=None,
            )

        if col < 0 or col >= COLS or board[col] != EMPTY:
            col = random.choice(legal)

        row = drop(board, col, mark, ROWS, COLS)

        if check_win(board, col, mark, ROWS, COLS):
            if verbose:
                print(f"  P{mark} wins in {len(moves)} moves")
            return moves, 'W' if mark == 1 else 'L'

        turn += 1
        if all(cell != EMPTY for cell in board):
            if verbose:
                print(f"  Draw in {len(moves)} moves")
            return moves, 'D'


def generate_positions(
    moves: list[tuple[str, int]],
    outcome: str,
) -> list[dict]:
    """
    Convert game moves into training positions.

    For each position, record the board state, player to move, and
    the game outcome from that player's perspective.

    Args:
        moves: list of (board_str, mark) tuples
        outcome: 'W', 'L', or 'D' from P1's perspective

    Returns:
        List of position dicts for training.
    """
    positions = []

    for i, (bstr, mark) in enumerate(moves):
        if outcome == 'D':
            label = 'D'
        elif outcome == 'W':
            label = 'W' if mark == 1 else 'L'
        else:  # outcome == 'L'
            label = 'L' if mark == 1 else 'W'

        positions.append({
            'board': bstr,
            'mark': mark,
            'label': label,
            'move_num': i + 1,
        })

    return positions


def run(
    num_games: int = 100,
    output: str = 'data/selfplay_positions.csv',
    seed: int = 42,
    noise: float = 0.05,
    verbose: bool = False,
):
    """
    Generate self-play positions and save to CSV.

    Args:
        num_games: number of self-play games to generate
        output: output CSV file path
        seed: random seed
        noise: probability of random move (0.0 = no noise)
        verbose: print progress
    """
    all_positions = []
    wins_p1 = 0
    wins_p2 = 0
    draws = 0

    t0 = time.time()
    for i in range(num_games):
        pos, outcome = play_game(seed=seed + i, noise=noise, verbose=False)
        positions = generate_positions(pos, outcome)
        all_positions.extend(positions)

        if outcome == 'W':
            wins_p1 += 1
        elif outcome == 'L':
            wins_p2 += 1
        else:
            draws += 1

    elapsed = time.time() - t0
    print(f"Generated {len(all_positions)} positions from {num_games} games "
          f"in {elapsed:.0f}s")
    print(f"  P1 wins: {wins_p1}, P2 wins: {wins_p2}, Draws: {draws} "
          f"({wins_p1 + wins_p2 + draws}/{num_games})")

    # Write CSV
    outpath = Path(output)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    with open(outpath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['board', 'mark', 'label', 'move_num'])
        for p in all_positions:
            writer.writerow([p['board'], p['mark'], p['label'], p['move_num']])

    print(f"Saved {len(all_positions)} positions to {outpath}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Self-play data generator')
    parser.add_argument('--games', type=int, default=100,
                        help='Number of games to play')
    parser.add_argument('--output', type=str, default='data/selfplay_positions.csv',
                        help='Output CSV file')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    parser.add_argument('--noise', type=float, default=0.05,
                        help='Noise probability (random moves)')
    args = parser.parse_args()

    run(args.games, args.output, args.seed, args.noise, verbose=True)