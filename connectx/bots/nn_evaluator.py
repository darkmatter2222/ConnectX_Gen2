"""
Compact Neural Network Evaluator for ConnectX.

Designed for both CPU and GPU evaluation.
Provides both a simple CPU-only evaluator (no PyTorch needed) and
a GPU-accelerated batch evaluator when PyTorch is available.

Architecture: 84 -> 128 -> 1 (ReLU hidden, tanh output)
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence

ROWS = 6
COLS = 7
INPUT_DIM = ROWS * COLS * 2  # 84: two channels (mark 1, mark 2)
HIDDEN_DIM = 128

_EMPTY = 0
_MARK_1 = 1
_MARK_2 = 2


# ── CPU-only fallback evaluator (no PyTorch needed) ──────────────────────────

class SimpleNN:
    """Lightweight feedforward network for CPU evaluation."""

    def __init__(self) -> None:
        import random
        rng = random.Random(42)
        scale1 = math.sqrt(2.0 / INPUT_DIM)
        scale2 = math.sqrt(2.0 / HIDDEN_DIM)

        self.w1: list[list[float]] = [
            [rng.gauss(0, scale1) for _ in range(HIDDEN_DIM)]
            for _ in range(INPUT_DIM)
        ]
        self.b1: list[float] = [0.0] * HIDDEN_DIM
        self.w2: list[float] = [rng.gauss(0, scale2) for _ in range(HIDDEN_DIM)]
        self.b2: float = 0.0

    def forward(self, x: List[float]) -> float:
        """Forward pass: 84 -> 128 (ReLU) -> 1 (tanh)."""
        # Layer 1: ReLU
        h = [0.0] * HIDDEN_DIM
        for j in range(HIDDEN_DIM):
            s = self.b1[j]
            for i in range(INPUT_DIM):
                if x[i]:
                    s += x[i] * self.w1[i][j]
            h[j] = s if s > 0 else 0.0  # ReLU

        # Layer 2: tanh (with linear approx for small values)
        s = self.b2
        for j in range(HIDDEN_DIM):
            s += h[j] * self.w2[j]
        if -0.7 < s < 0.7:
            return s
        return math.tanh(s)

    def evaluate(self, board: Sequence[int], mark: int, cols: int = COLS) -> float:
        """Encode board and evaluate."""
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
        """Save weights."""
        with open(path, 'wb') as f:
            f.write(b'SNNE')
            import struct
            for i in range(INPUT_DIM):
                for j in range(HIDDEN_DIM):
                    f.write(struct.pack('d', self.w1[i][j]))
            for j in range(HIDDEN_DIM):
                f.write(struct.pack('d', self.b1[j]))
            for j in range(HIDDEN_DIM):
                f.write(struct.pack('d', self.w2[j]))
            f.write(struct.pack('d', self.b2))

    def load(self, path: str) -> None:
        """Load weights."""
        with open(path, 'rb') as f:
            if f.read(4) != b'SNNE':
                raise ValueError("Invalid network file")
            f.read(4)
            import struct
            for i in range(INPUT_DIM):
                for j in range(HIDDEN_DIM):
                    self.w1[i][j] = struct.unpack('d', f.read(8))[0]
            for j in range(HIDDEN_DIM):
                self.b1[j] = struct.unpack('d', f.read(8))[0]
            for j in range(HIDDEN_DIM):
                self.w2[j] = struct.unpack('d', f.read(8))[0]
            self.b2 = struct.unpack('d', f.read(8))[0]


# ── GPU/PyTorch evaluator ────────────────────────────────────────────────────

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False


if _HAS_TORCH:
    class ConnectXNet(nn.Module):
        """ConnectX evaluation network: 84 -> 128 -> 1."""

        def __init__(self) -> None:
            super().__init__()
            self.fc1 = nn.Linear(INPUT_DIM, HIDDEN_DIM)
            self.fc2 = nn.Linear(HIDDEN_DIM, 1)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            h = F.relu(self.fc1(x))
            return torch.tanh(self.fc2(h))


    def _board_to_tensor(
        board: Sequence[int], mark: int, cols: int = COLS
    ) -> torch.Tensor:
        """Encode board into tensor of shape (1, 84)."""
        opp = 3 - mark
        n = ROWS * COLS
        feat = [0.0] * INPUT_DIM
        for i in range(n):
            if board[i] == mark:
                feat[i] = 1.0
            elif board[i] == opp:
                feat[i + n] = 1.0
        return torch.tensor([feat], dtype=torch.float32)


    class GPU_NNEvaluator:
        """GPU-accelerated neural network evaluator."""

        def __init__(self, device: Optional[str] = None) -> None:
            if device is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
            self.device = device
            self.model = ConnectXNet().to(device)
            self.model.eval()

        def evaluate(self, board: Sequence[int], mark: int, cols: int = COLS) -> float:
            """Evaluate a single board position."""
            with torch.no_grad():
                x = _board_to_tensor(board, mark, cols).to(self.device)
                return self.model(x).item()

        def evaluate_batch(
            self,
            boards: List[Sequence[int]],
            marks: List[int],
            cols: int = COLS,
        ) -> List[float]:
            """Evaluate a batch of positions in parallel."""
            n = len(boards)
            opp = [3 - m for m in marks]
            data = torch.zeros(n, INPUT_DIM, dtype=torch.float32)

            for i in range(n):
                for j in range(ROWS * COLS):
                    if boards[i][j] == marks[i]:
                        data[i, j] = 1.0
                    elif boards[i][j] == opp[i]:
                        data[i, j + ROWS * COLS] = 1.0

            with torch.no_grad():
                x = data.to(self.device)
                logits = self.model(x)
                return logits.cpu().squeeze(-1).tolist()

        def save(self, path: str) -> None:
            """Save model weights."""
            torch.save(self.model.state_dict(), path)

        def load(self, path: str) -> None:
            """Load model weights."""
            self.model.load_state_dict(
                torch.load(path, map_location=self.device, weights_only=True)
            )


# ── Singleton access ──────────────────────────────────────────────────────────

_evaluator: Optional[GPU_NNEvaluator] = None
_simple_evaluator: Optional[SimpleNN] = None


def get_evaluator() -> Optional[GPU_NNEvaluator]:
    """Get or create the GPU evaluator (lazy init)."""
    global _evaluator
    if _evaluator is None and _HAS_TORCH:
        _evaluator = GPU_NNEvaluator()
    return _evaluator


def get_simple_evaluator() -> SimpleNN:
    """Get or create the simple (CPU-only) evaluator."""
    global _simple_evaluator
    if _simple_evaluator is None:
        _simple_evaluator = SimpleNN()
    return _simple_evaluator


def evaluate(board: Sequence[int], mark: int, cols: int = COLS) -> float:
    """
    Evaluate a board position.
    Uses GPU if available, falls back to simple CPU.
    """
    if _HAS_TORCH and _evaluator is not None:
        return _evaluator.evaluate(board, mark, cols)
    return get_simple_evaluator().evaluate(board, mark, cols)