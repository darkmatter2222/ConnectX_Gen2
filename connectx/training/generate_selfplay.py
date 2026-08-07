"""Generate ConnectX self-play data for value network training.

Generates games where two alpha-beta bots play against each other with
noise injected into move selection. The key is to produce positions where
the outcome is not trivially determined.

Strategy:
- Play v2 (strong) against v1 (weaker) at 20% noise
- This produces imbalanced games with clear outcomes
- Record all positions with the game result as label
"""
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab import bitboard_ab_bot
from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
import random
import numpy as np
import csv
import os
import time
from pathlib import Path


def encode_board(board, mark):
    """Encode board as 21 features: mark channels + col heights."""
    board = list(board)
    features = []
    # 2 binary channels: mark 1 presence, mark 2 presence
    for i in range(42):
        features.append(1.0 if board[i] == mark else 0.0)
        features.append(1.0 if board[i] == (3 - mark) else 0.0)
    # 1 channel: column height (normalized 0-1)
    for c in range(7):
        h = 0
        for r in range(6):
            if board[r * 7 + c] != 0:
                h = r + 1
                break
        features.append(h / 6.0)
    return features


def generate_selfplay(mark1, mark2, noise, num_games, seed_offset=0):
    """Generate self-play data.

    Args:
        mark1: bot1's mark (always 1 for simplicity)
        mark2: bot2's mark (always 2)
        noise: noise level (0-1) - probability of random move
        num_games: number of games to play
        seed_offset: random seed offset for reproducibility

    Returns:
        List of (features_array, label) tuples
    """
    all_positions = []

    for game_idx in range(num_games):
        rng = random.Random(seed_offset + game_idx)
        board = connectx.make_board(7, 6)
        turn = 0
        last_move_col = -1
        last_move_mark = -1

        while not connectx.is_terminal(board, 6, 7):
            legal = connectx.valid_moves(board, 7)
            if not legal:
                break

            if turn % 2 == 0:
                current_mark = 1
                bot_fn = mark1
            else:
                current_mark = 2
                bot_fn = mark2

            board_list = list(board)
            legal = connectx.valid_moves(board_list, 7)

            # Encode and record position
            features = encode_board(board, current_mark)
            all_positions.append((features, current_mark, turn))

            # Get move from bot
            try:
                move = bot_fn(board_list, current_mark, legal, 7, 1.5, 55.0)
            except Exception:
                move = rng.choice(legal)

            # Apply noise: random move with probability `noise`
            if rng.random() < noise:
                move = rng.choice(legal)

            if move not in legal:
                move = legal[0] if legal else 3

            connectx.drop(board, move, current_mark)
            last_move_col = move
            last_move_mark = current_mark
            turn += 1

            if turn >= 42:
                break

        # Determine outcome
        winner = None
        if last_move_col >= 0:
            if connectx.check_win(board, last_move_col, last_move_mark, 6, 7):
                winner = last_move_mark
            elif connectx.is_terminal(board, 6, 7):
                winner = 0  # draw

        # Label positions
        for features, player_mark, move_turn in all_positions:
            if winner == player_mark:
                label = 1.0
            elif winner == 0:
                label = 0.5
            else:
                label = 0.0
            yield np.array(features), label


if __name__ == "__main__":
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)

    print("Generating self-play: v2 vs v1 at 20% noise, 500 games...")
    start = time.time()

    positions = []
    game_count = 0

    for features, label in generate_selfplay(
        bitboard_ab_bot_v2, bitboard_ab_bot,
        noise=0.2, num_games=500
    ):
        positions.append((features, label))
        game_count += 1

        if len(positions) % 5000 == 0:
            elapsed = time.time() - start
            print(f"  {len(positions)} positions, {elapsed:.1f}s")

    elapsed = time.time() - start
    print(f"Generated {len(positions)} positions in {elapsed:.1f}s")

    # Save as NPZ
    boards = np.array([p[0] for p in positions])
    outcomes = np.array([p[1] for p in positions])
    np.savez(DATA_DIR / "selfplay_v2_v1_20noise_500games.npz",
             boards=boards, outcomes=outcomes)

    # Print summary
    wins_p1 = np.sum(outcomes == 1.0)
    wins_p2 = np.sum(outcomes == 0.0)
    draws = np.sum(outcomes == 0.5)
    print(f"\nLabel distribution:")
    print(f"  P1 wins: {int(wins_p1)} ({wins_p1/len(outcomes)*100:.1f}%)")
    print(f"  P2 wins: {int(wins_p2)} ({wins_p2/len(outcomes)*100:.1f}%)")
    print(f"  Draws:   {int(draws)} ({draws/len(outcomes)*100:.1f}%)")
    print(f"  Non-draw: {int(wins_p1+wins_p2)/len(outcomes)*100:.1f}%")