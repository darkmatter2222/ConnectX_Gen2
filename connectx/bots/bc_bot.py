"""
Behavioral cloning bot: policy network predicts v2's moves.

Uses a trained BC policy network (84->256->7) as the primary move
selector. Falls back to v2 alpha-beta when the network is uncertain
(low confidence or OOD position).

Model path: O:\master_model_collection\ConnectX_Gen2_Phase2\models\connectx_nn_bc\best.pth
"""

from __future__ import annotations

import os
import time
from typing import Optional, Sequence

import numpy as np

from connectx.engine import (
    valid_moves, ROWS, COLS,
)

_MODEL_PATH = os.environ.get(
    'CONNECTX_BC_MODEL',
    r'O:\master_model_collection\ConnectX_Gen2_Phase2\models\connectx_nn_bc\best.pth',
)

_bc_model = None
_bc_device = 'cuda'


def _get_bc_model():
    global _bc_model
    if _bc_model is not None:
        return _bc_model
    try:
        import torch
        import torch.nn as nn
        from connectx.training.train_bc import ConnectXPolicyNet

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        _bc_model = ConnectXPolicyNet().to(device)
        _bc_model.load_state_dict(
            torch.load(_MODEL_PATH, map_location=device, weights_only=True)
        )
        _bc_model.eval()
        return _bc_model
    except Exception:
        return None


def _encode_board(board, mark):
    """Encode board for policy network."""
    opp = 3 - mark
    n = ROWS * COLS
    enc = np.zeros(2 * n, dtype=np.float32)
    for i in range(n):
        if board[i] == mark:
            enc[i] = 1.0
        elif board[i] == opp:
            enc[i + n] = 1.0
    return enc


def bc_bot(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Policy network bot with v2 fallback."""
    board_list = list(board)
    legal = list(valid_moves(board_list, cols))
    if not legal:
        return 0

    model = _get_bc_model()
    if model is None:
        # Fall back to v2 if BC model not available
        from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2 as _v2_bot
        return _v2_bot(board_list, mark, legal, cols, move_deadline, remaining_overage, seed)

    try:
        import torch
        with torch.no_grad():
            feat = torch.from_numpy(_encode_board(board, mark)).to(_bc_device).unsqueeze(0).float()
            logits = model(feat)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

            # Pick the move with highest probability among legal moves
            legal_probs = [(c, probs[c]) for c in legal]
            legal_probs.sort(key=lambda x: x[1], reverse=True)

            if legal_probs[0][1] > 0.9:  # High confidence
                return legal_probs[0][0]
            elif len(legal_probs) > 1 and legal_probs[1][1] < 0.1:
                # Clear preference
                return legal_probs[0][0]
            else:
                # Low confidence — fall back to v2
                pass
    except Exception:
        pass

    # Fall back to v2
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2 as _v2_bot
    return _v2_bot(board_list, mark, legal, cols, move_deadline, remaining_overage, seed)