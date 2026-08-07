"""
MCTS Bot with BC (Behavioral Cloning) Policy Prior.

Uses a trained policy network (learned from v2's move choices) as a prior
for MCTS PUCT exploration. This combines v2's strategic knowledge with
MCTS's tactical search depth.

PUCT with prior:
    score(q, n, N, prior) = q/n + C * prior * sqrt(N/(1+n))
"""

from __future__ import annotations

import math
import random
import time
import torch
import torch.nn as nn
from dataclasses import dataclass, field
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW,
)


class BCNet(nn.Module):
    """Policy network: 84 inputs -> 256 -> 128 -> 7 (softmax)."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(84, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 7),  # 7 columns, logits
        )

    def forward(self, x):
        return self.net(x)


# Global cached model
_model: Optional[BCNet] = None
_model_device = 'cpu'


def _get_model():
    global _model, _model_device
    if _model is not None:
        return _model

    _model = BCNet()
    model_path = 'models/connectx_nn_bc/best.pth'
    try:
        _model.load_state_dict(
            torch.load(model_path, map_location='cpu', weights_only=True)
        )
        _model_device = 'cpu'
    except FileNotFoundError:
        print("Warning: BC model not found, falling back to uniform prior")
        _model_device = 'cpu'

    _model.eval()
    return _model


def encode_board(board, mark):
    """Encode board as 84-element feature vector."""
    opp = 3 - mark
    enc = torch.zeros(84, dtype=torch.float32)
    for i in range(42):
        if board[i] == mark:
            enc[i] = 1.0
        elif board[i] == opp:
            enc[i + 42] = 1.0
    return enc


def get_bc_prior(board, mark, legal_cols):
    """Get BC policy prior over legal moves."""
    model = _get_model()
    enc = encode_board(board, mark)
    with torch.no_grad():
        logits = model(enc.unsqueeze(0))
    probs = torch.softmax(logits, dim=1).squeeze(0)

    prior = {}
    for col in legal_cols:
        prior[col] = probs[col].item()

    # Normalize to sum to 1
    total = sum(prior.values())
    if total > 0:
        for col in prior:
            prior[col] /= total
    return prior


# ── MCTS Node ─────────────────────────────────────────────────────────────────

@dataclass
class MCTSNode:
    col: int
    mark: int
    board_snapshot: list[int]
    wins: float = 0.0
    visits: int = 0
    children: dict[int, 'MCTSNode'] = field(default_factory=dict)
    prior: float = 1.0 / 7.0
    is_terminal: bool = False

    @property
    def visit_count(self) -> int:
        return self.visits

    @property
    def win_rate(self) -> float:
        if self.visits == 0:
            return 0.0
        return self.wins / self.visits

    def puct_score(self, c: float, parent_visits: int) -> float:
        if self.visits == 0:
            # UCB exploration term
            if parent_visits == 0:
                return float('inf')
            return c * math.sqrt(parent_visits) * self.prior
        # Exploitation + exploration
        exploitation = self.wins / self.visits
        exploration = c * math.sqrt(parent_visits) * self.prior / (1 + self.visits)
        return exploitation + exploration


def _simulate(board, mark, cols, max_steps=42):
    """Tactical simulation for MCTS playouts."""
    opp = 3 - mark
    board_list = list(board)

    for _ in range(max_steps):
        legal = valid_moves(board_list, cols)
        if not legal:
            break

        # Win
        for col in legal:
            if check_win(board_list, col, mark, ROWS, cols):
                return 1.0

        # Block
        for col in legal:
            board_list[col] = mark
            is_full = all(board_list[r * cols] != 0 for r in range(ROWS))
            if not is_full:
                un_drop(board_list, col, ROWS, cols)
            else:
                board_list[col] = 0
            if check_win(board_list, col, opp, ROWS, cols):
                un_drop(board_list, col, ROWS, cols)
                break
            board_list[col] = 0

        # Center column preference
        if 3 in legal:
            col = 3
        elif 2 in legal or 4 in legal:
            col = 2 if 2 in legal else 4
        else:
            col = random.choice(legal)

        try:
            drop(board_list, col, mark, ROWS, cols)
        except ValueError:
            break

        mark, opp = opp, mark

    return 0.0


# ── MCTS Search ────────────────────────────────────────────────────────────────


def _mcts_search(
    root_board: list[int],
    mark: int,
    time_limit: float,
    cols: int = COLS,
    c: float = 1.4,
    max_iterations: int = 5000,
) -> tuple[int, MCTSNode]:
    """
    Run MCTS iterations with BC policy prior until time is up or
    max iterations reached.
    """
    board_list = list(root_board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(board_list))

    # Get BC policy prior for root moves
    root_priors = get_bc_prior(board_list, mark, legal)

    # Build root node from all legal moves
    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(board_list)
        drop(board_copy, col, mark, ROWS, cols)
        prior = root_priors.get(col, 1.0 / len(legal))

        if check_win(board_copy, col, mark, ROWS, cols):
            node = MCTSNode(
                col=col, mark=mark, board_snapshot=list(board_copy),
                prior=prior,
            )
            node.visits = 1
            node.wins = 1.0
            root_children[col] = node
            continue

        node = MCTSNode(
            col=col, mark=mark, board_snapshot=list(board_copy),
            prior=prior,
        )
        root_children[col] = node

    root = MCTSNode(
        col=0, mark=mark, board_snapshot=list(board_list),
        children=root_children,
    )

    start_time = time.time()

    for _ in range(max_iterations):
        if time.time() - start_time >= time_limit:
            break

        # --- SELECTION ---
        current = root
        path: list[MCTSNode] = [root]

        while current.children:
            best_puct = float('-inf')
            best_child = None
            for child in current.children.values():
                p = child.puct_score(c, current.visits)
                if p > best_puct:
                    best_puct = p
                    best_child = child
                elif p == best_puct and child.visits > (best_child.visits if best_child else 0):
                    best_child = child

            if best_child is None:
                break

            current = best_child
            path.append(current)

        # --- EXPANSION ---
        if not current.is_terminal:
            legal = valid_moves(current.board_snapshot, cols)
            if legal:
                explored = set(current.children.keys())
                unexplored = [col for col in legal if col not in explored]
                if unexplored:
                    col = min(unexplored)
                    board_copy = list(current.board_snapshot)
                    drop(board_copy, col, current.mark, ROWS, cols)

                    # Get prior for expanded child from BC model
                    child_prior = root_priors.get(col, 1.0 / len(legal))

                    if check_win(board_copy, col, current.mark, ROWS, cols):
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                            prior=child_prior,
                        )
                    else:
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                            prior=child_prior,
                        )

                    current.children[col] = child
                    path.append(child)
                    current = child

        # --- SIMULATION ---
        sim_board = list(current.board_snapshot)
        sim_mark = 3 - current.mark
        reward = _simulate(sim_board, sim_mark, cols, max_steps=42)

        # Convert: 1.0 = sim_mark won → our_value = 0
        #           0.0 = no win → our_value = 0 (draw)
        our_value = 1.0 - reward

        # --- BACK-PROPAGATION ---
        for node in reversed(path):
            if node.mark == mark:
                node.wins += our_value
            else:
                node.wins += 1.0 - our_value
            node.visits += 1

    # Return the most-visited child (most reliable estimate)
    if not root.children:
        return 0, root
    best = max(root.children.values(), key=lambda c: c.visits)
    return best.col, root


# ── Public bot API ─────────────────────────────────────────────────────────────


def mcts_bc_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    MCTS bot with BC policy prior.

    Combines MCTS tactical search with BC strategic knowledge for
    move selection. Uses the BC model's policy as a prior in the
    PUCT exploration formula.
    """
    board_list = list(board)

    # Recompute legal moves
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    # Check for immediate win
    for col in legal:
        board_list[col] = mark
        if check_win(board_list, col, mark, ROWS, cols):
            board_list[col] = 0
            return col
        board_list[col] = 0

    # Check for immediate block
    opp = 3 - mark
    for col in legal:
        board_list[col] = opp
        if check_win(board_list, col, opp, ROWS, cols):
            board_list[col] = 0
            board_list = list(board)
            return col
        board_list[col] = 0

    # Set time budget
    time_limit = 0.15
    if move_deadline is not None:
        time_limit = max(0.05, move_deadline - 0.05)

    if seed is not None:
        random.seed(seed)

    best_col, _ = _mcts_search(board_list, mark, time_limit, cols, c=1.4)
    return best_col