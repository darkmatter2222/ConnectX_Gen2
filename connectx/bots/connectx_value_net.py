"""
ConnectX Value Network — Perspective-aware win-probability predictor.

Architecture:
  84 inputs (two 7x6 channels) -> 128 (tanh) -> 128 (tanh) -> 64 (tanh) -> 1 (tanh)

The value is **perspective-aware**: it represents the win probability
from the perspective of the player who last moved (i.e. the player
whose mark fills channel 0 of the board encoding).

Output range: [-1, +1]
  +1  = current player wins
  -1  = current player loses
   0  = draw

This module provides:
  - PyTorch GPUValueNet (GPU/CPU training & inference)
  - SimpleValueNet (CPU-only fallback, no PyTorch dependency)
  - Lazy singleton accessor for bot integration
"""

from __future__ import annotations

import math
import struct
from typing import List, Optional, Sequence

ROWS = 6
COLS = 7
INPUT_DIM = ROWS * COLS * 2  # 84


# ── CPU-only fallback evaluator (no PyTorch needed) ────────────────────────────


class SimpleValueNet:
    """Lightweight feedforward value network for CPU evaluation."""

    def __init__(self) -> None:
        rng = __import__('random').Random(42)

        def _init(m: int, n: int) -> List[List[float]]:
            scale = math.sqrt(2.0 / m)
            return [[rng.gauss(0, scale) for _ in range(n)] for _ in range(m)]

        self.w1: List[List[float]] = _init(INPUT_DIM, 128)
        self.b1: List[float] = [0.0] * 128
        self.w2: List[List[float]] = _init(128, 128)
        self.b2: List[float] = [0.0] * 128
        self.w3: List[List[float]] = _init(128, 64)
        self.b3: List[float] = [0.0] * 64
        self.w4: List[float] = _init(64, 1)
        self.b4: float = 0.0

    @staticmethod
    def _tanh(x: float) -> float:
        if x > 10.0:
            return 1.0
        if x < -10.0:
            return -1.0
        return math.tanh(x)

    def forward(self, x: List[float]) -> float:
        """Forward pass: 84 -> 128 -> 128 -> 64 -> 1 (all tanh)."""
        # Layer 1: 84 -> 128
        h1 = [0.0] * 128
        for j in range(128):
            s = self.b1[j]
            for i in range(INPUT_DIM):
                if x[i] != 0.0:
                    s += x[i] * self.w1[i][j]
            h1[j] = self._tanh(s)

        # Layer 2: 128 -> 128
        h2 = [0.0] * 128
        for j in range(128):
            s = self.b2[j]
            for i in range(128):
                s += h1[i] * self.w2[i][j]
            h2[j] = self._tanh(s)

        # Layer 3: 128 -> 64
        h3 = [0.0] * 64
        for j in range(64):
            s = self.b3[j]
            for i in range(128):
                s += h2[i] * self.w3[i][j]
            h3[j] = self._tanh(s)

        # Layer 4: 64 -> 1
        s = self.b4
        for i in range(64):
            s += h3[i] * self.w4[i][0]
        return self._tanh(s)

    def evaluate(self, board: Sequence[int], mark: int, cols: int = COLS) -> float:
        """Encode board and evaluate value."""
        opp = 3 - mark
        enc = [0.0] * INPUT_DIM
        n = ROWS * COLS
        for i in range(n):
            if board[i] == mark:
                enc[i] = 1.0
            elif board[i] == opp:
                enc[i + n] = 1.0
        return self.forward(enc)

    def save(self, path: str) -> None:
        """Save weights to binary file."""
        with open(path, 'wb') as f:
            f.write(b'SVNT')
            for row in self.w1:
                for v in row:
                    f.write(struct.pack('d', v))
            for v in self.b1:
                f.write(struct.pack('d', v))
            for row in self.w2:
                for v in row:
                    f.write(struct.pack('d', v))
            for v in self.b2:
                f.write(struct.pack('d', v))
            for row in self.w3:
                for v in row:
                    f.write(struct.pack('d', v))
            for v in self.b3:
                f.write(struct.pack('d', v))
            for row in self.w4:
                for v in row:
                    f.write(struct.pack('d', v))
            f.write(struct.pack('d', self.b4))

    def load(self, path: str) -> None:
        """Load weights from binary file."""
        with open(path, 'rb') as f:
            if f.read(4) != b'SVNT':
                raise ValueError("Invalid value network file")
            total_w = INPUT_DIM * 128 + 128 * 128 + 128 * 64 + 64 * 1
            total_b = 128 + 128 + 64 + 1
            vals: List[float] = []
            for _ in range(total_w + total_b):
                vals.append(struct.unpack('d', f.read(8))[0])
            idx = 0

            def _read_list(n: int) -> List[float]:
                nonlocal idx
                r = vals[idx:idx + n]
                idx += n
                return r

            self.w1 = [vals[idx + i * 128:(i + 1) * 128]
                       for i in range(INPUT_DIM)]
            idx += INPUT_DIM * 128
            self.b1 = _read_list(128)
            self.w2 = [vals[idx + i * 128:(i + 1) * 128]
                       for i in range(128)]
            idx += 128 * 128
            self.b2 = _read_list(128)
            self.w3 = [vals[idx + i * 64:(i + 1) * 64]
                       for i in range(128)]
            idx += 128 * 64
            self.b3 = _read_list(64)
            self.w4 = [vals[idx + i * 1:(i + 1) * 1]]
            idx += 64 * 1
            self.b4 = _read_list(1)[0]


# ── PyTorch value network ──────────────────────────────────────────────────────

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False


if _HAS_TORCH:
    class ConnectXValueNet(nn.Module):
        """ConnectX value network: 84 -> 128 -> 128 -> 64 -> 1 (tanh)."""

        def __init__(self) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(INPUT_DIM, 128),
                nn.Tanh(),
                nn.Linear(128, 128),
                nn.Tanh(),
                nn.Linear(128, 64),
                nn.Tanh(),
                nn.Linear(64, 1),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.net(x)


    class GPUValueNet:
        """GPU-accelerated neural network value predictor."""

        def __init__(self, device: Optional[str] = None) -> None:
            if device is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
            self.device = device
            self.model = ConnectXValueNet().to(device)
            self.model.eval()

        def evaluate(self, board: Sequence[int], mark: int, cols: int = COLS) -> float:
            """Evaluate a single board position."""
            opp = 3 - mark
            n = ROWS * COLS
            feat = [0.0] * (2 * n)
            for i in range(n):
                if board[i] == mark:
                    feat[i] = 1.0
                elif board[i] == opp:
                    feat[i + n] = 1.0
            with torch.no_grad():
                x = torch.tensor([feat], dtype=torch.float32).to(self.device)
                return self.model(x).item()

        def save(self, path: str) -> None:
            """Save model weights."""
            torch.save(self.model.state_dict(), path)

        def load(self, path: str) -> None:
            """Load model weights."""
            self.model.load_state_dict(
                torch.load(path, map_location=self.device, weights_only=True)
            )
            self.model.eval()


# ── Singleton access ───────────────────────────────────────────────────────────

_value_net: Optional[GPUValueNet] = None


def get_value_net() -> Optional[GPUValueNet]:
    """Get or create the GPU value network (lazy init)."""
    global _value_net
    if _value_net is None and _HAS_TORCH:
        _value_net = GPUValueNet()
    return _value_net


def value_predict(board: Sequence[int], mark: int, cols: int = COLS) -> float:
    """
    Predict the value of a board position from mark's perspective.

    Returns a float in [-1, +1]:
      +1 = mark wins
      -1 = mark loses
       0 = draw
    """
    if _HAS_TORCH and _value_net is not None:
        return _value_net.evaluate(board, mark, cols)
    return SimpleValueNet().evaluate(board, mark, cols)