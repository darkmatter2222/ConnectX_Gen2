"""
Behavioral Cloning (BC) training for ConnectX neural network.

Instead of training the NN to predict v2's evaluation, train it to
predict v2's MOVE choices. This captures v2's decision-making directly.

Architecture: 84 inputs -> 256 hidden -> 7 outputs (softmax over columns)

Usage:
  python train_bc.py --data training_bc_data.npz --output-dir models/connectx_nn_bc
"""

from __future__ import annotations

import os
import sys
import math
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, TensorDataset

import numpy as np
from pathlib import Path


class ConnectXPolicyNet(nn.Module):
    """Policy network: predicts column probabilities."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(84, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 7),  # 7 columns
        )

    def forward(self, x):
        return self.net(x)


class ConnectXDataset(Dataset):
    """Dataset for ConnectX policy network training."""

    def __init__(self, boards: np.ndarray, moves: np.ndarray):
        self.boards = torch.tensor(boards, dtype=torch.float32)
        self.moves = torch.tensor(moves, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.boards)

    def __getitem__(self, idx: int):
        return self.boards[idx], self.moves[idx]


def train_bc(
    data_file: str = 'training_bc_data.npz',
    output_dir: str = 'models/connectx_nn_bc',
    epochs: int = 50,
    batch_size: int = 256,
    lr: float = 1e-3,
    device: Optional[str] = None,
) -> None:
    """Train policy network via behavioral cloning."""
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    print(f"Device: {device}")
    print(f"Training {data_file} with {epochs} epochs, batch_size={batch_size}, lr={lr}")

    data = np.load(data_file)
    boards = data['boards']
    moves = data['moves']

    print(f"Dataset size: {len(boards)} positions")
    print(f"Move distribution: {np.bincount(moves, minlength=7).tolist()}")

    # Split into train/val (90/10)
    n = len(boards)
    indices = np.random.permutation(n)
    split = int(0.9 * n)
    train_idx, val_idx = indices[:split], indices[split:]

    train_set = ConnectXDataset(boards[train_idx], moves[train_idx])
    val_set = ConnectXDataset(boards[val_idx], moves[val_idx])

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)

    model = ConnectXPolicyNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    os.makedirs(output_dir, exist_ok=True)

    best_acc = 0.0
    best_epoch = 0

    for epoch in range(1, epochs + 1):
        # Train
        model.train()
        train_loss = 0.0
        n_batches = 0

        for boards_b, targets_b in train_loader:
            boards_b = boards_b.to(device)
            targets_b = targets_b.to(device)

            optimizer.zero_grad()
            logits = model(boards_b)
            loss = criterion(logits, targets_b)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            train_loss += loss.item()
            n_batches += 1

        train_loss /= n_batches

        # Validate
        model.eval()
        val_loss = 0.0
        val_acc = 0.0
        n_batches = 0

        with torch.no_grad():
            for boards_b, targets_b in val_loader:
                boards_b = boards_b.to(device)
                targets_b = targets_b.to(device)

                logits = model(boards_b)
                loss = criterion(logits, targets_b)
                val_loss += loss.item()
                val_acc += (logits.argmax(dim=1) == targets_b).sum().item()
                n_batches += 1

        val_loss /= n_batches
        val_acc /= len(val_set)

        scheduler.step()

        if val_acc > best_acc:
            best_acc = val_acc
            best_epoch = epoch
            torch.save(model.state_dict(), os.path.join(output_dir, 'best.pth'))

        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d}/{epochs}: train_loss={train_loss:.4f} "
                  f"val_loss={val_loss:.4f} val_acc={val_acc:.4f} "
                  f"lr={scheduler.get_last_lr()[0]:.2e} "
                  f"(best_val_acc={best_acc:.4f} @ epoch {best_epoch})")

    torch.save(model.state_dict(), os.path.join(output_dir, 'final.pth'))
    print(f"\nTraining complete. Best val_acc={best_acc:.4f} at epoch {best_epoch}")
    print(f"Saved to {output_dir}/")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='training_bc_data.npz')
    parser.add_argument('--output-dir', type=str, default='models/connectx_nn_bc')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=256)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--device', type=str, default=None)
    args = parser.parse_args()

    train_bc(
        data_file=args.data,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
    )