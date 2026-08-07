"""AlphaZero-style self-play refinement pipeline.

Complete pipeline:
1. Generate self-play data (v2 vs v2, seat-reversed)
2. Convert CSV to NPZ format for training
3. Train value network on balanced data
4. Evaluate new value network

Usage:
    python connectx/training/selfplay_pipeline.py --games 50 --epochs 20
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def encode_board(board_str: str, mark: int, cols: int = 7) -> list[float]:
    """
    Encode a 42-char board string + mark into an 84-element feature vector.

    First 42 elements: board state (1 for mark's pieces, 2 for opponent's)
    Next 42 elements: board state from opponent's perspective

    This is the "perspective-aware" encoding used by the value network.
    """
    # Parse board string
    cells = [int(c) for c in board_str]

    # Identify mark's pieces and opponent's pieces
    pieces = []
    opponent = []
    for cell in cells:
        if cell == mark:
            pieces.append(1.0)
            opponent.append(0.0)
        elif cell == 3 - mark:
            pieces.append(0.0)
            opponent.append(1.0)
        else:
            pieces.append(0.0)
            opponent.append(0.0)

    return pieces + opponent


def csv_to_npz(csv_path: str, npz_path: str) -> None:
    """
    Convert self-play CSV to NPZ format for training.

    CSV columns: board, mark, label, move_num
    Label: 'W' (current player wins), 'L' (current player loses), 'D' (draw)
    Target: +1.0 for W, -1.0 for L, 0.0 for D
    """
    boards = []
    outcomes = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            board_str = row['board']
            mark = int(row['mark'])
            label = row['label']

            # Convert label to outcome
            if label == 'W':
                outcome = 1.0
            elif label == 'L':
                outcome = -1.0
            else:  # 'D'
                outcome = 0.0

            board_vec = encode_board(board_str, mark)
            boards.append(board_vec)
            outcomes.append(outcome)

    boards_np = np.array(boards, dtype=np.float32)
    outcomes_np = np.array(outcomes, dtype=np.float32)

    np.savez(npz_path, boards=boards_np, outcomes=outcomes_np)
    print(f"Converted {len(boards)} positions to {npz_path}")
    print(f"  Features: {boards_np.shape}")
    print(f"  Targets: mean={outcomes_np.mean():.3f}, std={outcomes_np.std():.3f}")
    print(f"  Distribution: W={int((outcomes_np > 0.5).sum())}, "
          f"L={int((outcomes_np < -0.5).sum())}, D={int((abs(outcomes_np) <= 0.5).sum())}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Self-play refinement pipeline')
    parser.add_argument('--games', type=int, default=50,
                        help='Number of self-play games')
    parser.add_argument('--csv', type=str, default='data/selfplay_positions.csv',
                        help='Self-play CSV output')
    parser.add_argument('--npz', type=str, default='data/selfplay_data.npz',
                        help='Training data NPZ output')
    parser.add_argument('--epochs', type=int, default=30,
                        help='Training epochs')
    parser.add_argument('--batch-size', type=int, default=256,
                        help='Batch size')
    parser.add_argument('--lr', type=float, default=1e-3,
                        help='Learning rate')
    parser.add_argument('--output-dir', type=str, default='models/value_net',
                        help='Output model directory')
    args = parser.parse_args()

    # Step 1: Generate self-play data
    print("=" * 60)
    print("Step 1: Generating self-play data")
    print("=" * 60)
    from connectx.training.selfplay_generate import run as run_selfplay
    run_selfplay(
        num_games=args.games,
        output=args.csv,
        seed=42,
        noise=0.0,
        verbose=True,
    )

    # Step 2: Convert CSV to NPZ
    print("\n" + "=" * 60)
    print("Step 2: Converting CSV to NPZ format")
    print("=" * 60)
    csv_to_npz(args.csv, args.npz)

    # Step 3: Train value network
    print("\n" + "=" * 60)
    print("Step 3: Training value network")
    print("=" * 60)
    os.chdir(str(Path(__file__).parent.parent.parent))
    from connectx.training.value_train import train_value_net
    train_value_net(
        data_file=args.npz,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
    )

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    print(f"  Self-play data: {args.csv}")
    print(f"  Training data:  {args.npz}")
    print(f"  Model weights:  {args.output_dir}/best.pth")
    print(f"\nNext step: evaluate the new model vs the old model")
    print(f"  python evaluate_value.py --model-dir {args.output_dir}")