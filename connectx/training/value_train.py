"""
Value Network Training Script — Cycle 13.

Trains the perspective-aware value network (84 -> 128 -> 128 -> 64 -> 1, tanh)
on ConnectX position-outcome pairs.  Targets:

  boards[i]  : (N, 84) float — board encoding for the player who moved
  outcomes[i]: (N,) float     — game outcome from that player's perspective

Training uses MSE loss with cosine-annealing LR schedule and gradient clipping.
Data is split 90/10 into train/val.

Usage:
  python value_train.py --data training_data.npz --output-dir models/value_net --epochs 30
"""

from __future__ import annotations

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, TensorDataset

_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in os.sys.path:
    os.sys.path.insert(0, _project_root)

from connectx.bots.connectx_value_net import ConnectXValueNet


class ValueDataset(Dataset):
    """Dataset for value network training."""

    def __init__(self, boards: np.ndarray, outcomes: np.ndarray):
        self.boards = torch.tensor(boards, dtype=torch.float32)
        self.outcomes = torch.tensor(outcomes, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.boards)

    def __getitem__(self, idx: int):
        return self.boards[idx], self.outcomes[idx]


def train_value_net(
    data_file: str = 'value_data.npz',
    output_dir: str = 'models/value_net',
    epochs: int = 30,
    batch_size: int = 256,
    lr: float = 1e-3,
    device: Optional[str] = None,
) -> None:
    """Train the ConnectX value network."""
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    print(f"Device: {device}")
    print(f"Training {data_file} with {epochs} epochs, batch_size={batch_size}, lr={lr}")

    # Load dataset
    data = np.load(data_file)
    boards = data['boards']  # (N, 84)
    outcomes = data['outcomes']  # (N,)

    print(f"Dataset size: {len(boards)} positions")
    print(f"Target distribution: mean={outcomes.mean():.3f}, std={outcomes.std():.3f}")
    print(f"Target range: [{outcomes.min():.3f}, {outcomes.max():.3f}]")

    # Count outcome classes
    n_close_to_1 = int((outcomes > 0.5).sum())
    n_close_to_neg1 = int((outcomes < -0.5).sum())
    n_close_to_0 = int((abs(outcomes) <= 0.5).sum())
    print(f"Outcome classes: win={n_close_to_1}, loss={n_close_to_neg1}, draw={n_close_to_0}")

    # Split into train/val (90/10)
    n = len(boards)
    indices = np.random.permutation(n)
    split = int(0.9 * n)
    train_idx, val_idx = indices[:split], indices[split:]

    train_set = ValueDataset(boards[train_idx], outcomes[train_idx])
    val_set = ValueDataset(boards[val_idx], outcomes[val_idx])

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)

    # Initialize model
    model = ConnectXValueNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.MSELoss()

    os.makedirs(output_dir, exist_ok=True)

    best_loss = float('inf')
    best_epoch = 0

    for epoch in range(1, epochs + 1):
        # --- Train ---
        model.train()
        train_loss = 0.0
        n_batches = 0

        for boards_b, targets_b in train_loader:
            boards_b = boards_b.to(device)
            targets_b = targets_b.to(device)

            optimizer.zero_grad()
            preds = model(boards_b)
            loss = criterion(preds.squeeze(-1), targets_b)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            train_loss += loss.item()
            n_batches += 1

        train_loss /= n_batches

        # --- Validate ---
        model.eval()
        val_loss = 0.0
        val_mae = 0.0
        n_batches = 0

        with torch.no_grad():
            for boards_b, targets_b in val_loader:
                boards_b = boards_b.to(device)
                targets_b = targets_b.to(device)

                preds = model(boards_b)
                val_loss += criterion(preds.squeeze(-1), targets_b).item()
                val_mae += F.l1_loss(preds.squeeze(-1), targets_b).item()
                n_batches += 1

        val_loss /= n_batches
        val_mae /= n_batches
        scheduler.step()

        if val_loss < best_loss:
            best_loss = val_loss
            best_epoch = epoch
            torch.save(model.state_dict(), os.path.join(output_dir, 'best.pth'))

        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d}/{epochs}: train_loss={train_loss:.4f} "
                  f"val_loss={val_loss:.4f} val_mae={val_mae:.4f} "
                  f"lr={scheduler.get_last_lr()[0]:.2e} "
                  f"(best_val={best_loss:.4f} @ epoch {best_epoch})")

    # Save final model
    torch.save(model.state_dict(), os.path.join(output_dir, 'final.pth'))
    print(f"\nTraining complete. Best val_loss={best_loss:.4f} at epoch {best_epoch}")
    print(f"Saved to {output_dir}/")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train ConnectX value network')
    parser.add_argument('--data', type=str, default='value_data.npz')
    parser.add_argument('--output-dir', type=str, default='models/value_net')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--batch-size', type=int, default=256)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--device', type=str, default=None)
    args = parser.parse_args()

    train_value_net(
        data_file=args.data,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
    )