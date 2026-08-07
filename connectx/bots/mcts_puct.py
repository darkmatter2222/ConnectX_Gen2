"""
Strong MCTS Bot with tuned PUCT and improved playouts.

Improvements over base mcts.py:
- Lower C parameter for more exploitation (1.2 vs 1.4)
- Better center column ordering
- More iterations at later game stages
- Faster board operations
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW,
)


# ── MCTS Node ─────────────────────────────────────────────────────────────────

@dataclass
class MCTSNode:
    """A node in the MCTS search tree."""
    col: int
    mark: int
    board_snapshot: list[int]
    wins: float = 0.0
    visits: int = 0
    children: dict[int, 'MCTSNode'] = field(default_factory=dict)
    is_terminal: bool = False

    @property
    def best_child(self) -> Optional['MCTSNode']:
        if not self.children:
            return None
        return max(self.children.values(), key=lambda c: c.visits)

    def puct_score(self, c: float, parent_visits: int) -> float:
        if self.visits == 0:
            return float('inf')
        if parent_visits <= 1:
            return self.wins / self.visits
        q = self.wins / self.visits
        c_term = c * math.sqrt(math.log(parent_visits) / self.visits)
        return q + c_term


# ── Board hash ─────────────────────────────────────────────────────────────────

_ZOBRIST: list[list[int]] = []

def _init_zobrist() -> None:
    import random as _rng
    rng = _rng.Random(42)
    SIZE = ROWS * COLS
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])

_init_zobrist()


def _hash_board(board: Sequence[int]) -> int:
    h = 0
    for i, cell in enumerate(board):
        if cell != 0:
            h ^= _ZOBRIST[cell - 1][i]
    return h


# ── Tactical rollout ───────────────────────────────────────────────────────────

def _simulate(board: list[int], mark: int, cols: int, max_steps: int = 42) -> float:
    """
    Tactical rollout — improved ordering.

    Each player prefers:
      1. Immediate wins
      2. Blocking opponent wins
      3. Fork creation (creating two threats)
      4. Blocking opponent forks
      5. Center column preference
      6. Otherwise random
    """
    opp = 3 - mark
    board = list(board)
    steps = 0

    while steps < max_steps:
        legal = valid_moves(board, cols)
        if not legal:
            return 0.0

        # Priority 1: find a winning move
        for col in list(legal):
            try:
                row = drop(board, col, mark, ROWS, cols)
            except ValueError:
                continue
            if check_win(board, col, mark, ROWS, cols):
                return 1.0

        # Priority 2: block opponent's win
        for col in list(legal):
            try:
                row = drop(board, col, opp, ROWS, cols)
            except ValueError:
                continue
            if check_win(board, col, opp, ROWS, cols):
                un_drop(board, col, ROWS, cols, row=row)
                mark, opp = opp, mark
                steps += 1
                break
            un_drop(board, col, ROWS, cols, row=row)
        else:
            # Priority 3: fork creation — check if any move creates a fork
            fork_move = None
            for col in list(legal):
                try:
                    row = drop(board, col, mark, ROWS, cols)
                except ValueError:
                    continue
                # Count threats for mark after this move
                threats = 0
                for r in range(ROWS):
                    for c2 in range(COLS):
                        if c2 + INAROW <= COLS:
                            line = [board[r * COLS + c2 + k] for k in range(INAROW)]
                            if line.count(mark) == INAROW - 1 and line.count(0) == 1 and c2 != col:
                                threats += 1
                        if r + INAROW <= ROWS:
                            line = [board[(r + k) * COLS + c2] for k in range(INAROW)]
                            if line.count(mark) == INAROW - 1 and line.count(0) == 1 and r != row // ROWS:
                                threats += 1
                        if r + INAROW <= ROWS and c2 + INAROW <= COLS:
                            line = [board[(r + k) * COLS + c2 + k] for k in range(INAROW)]
                            if line.count(mark) == INAROW - 1 and line.count(0) == 1:
                                threats += 1
                        if r + INAROW <= ROWS and c2 >= INAROW:
                            line = [board[(r + k) * COLS + c2 - k] for k in range(INAROW)]
                            if line.count(mark) == INAROW - 1 and line.count(0) == 1:
                                threats += 1
                un_drop(board, col, ROWS, cols, row=row)
                if threats >= 2:
                    fork_move = col
                    break

            if fork_move is not None:
                mark, opp = opp, mark
                steps += 1
                continue

            # Priority 4: center column preference
            center = cols // 2
            ordered = []
            for offset in range(cols):
                left = center - offset
                if left >= 0 and left in legal:
                    ordered.append(left)
                right = center + 1 + offset
                if right < cols and right in legal:
                    ordered.append(right)

            if ordered:
                if random.random() < 0.85:
                    col = ordered[0]
                else:
                    col = random.choice(ordered)
            elif legal:
                col = random.choice(legal)
            else:
                return 0.0

            available = valid_moves(board, cols)
            while col not in available:
                if not available:
                    return 0.0
                col = random.choice(available)
                available = valid_moves(board, cols)

            try:
                drop(board, col, mark, ROWS, cols)
            except ValueError:
                mark, opp = opp, mark
                continue

            steps += 1
            mark, opp = opp, mark

    return 0.0


# ── MCTS Search ────────────────────────────────────────────────────────────────

def _mcts_search(
    root_board: list[int],
    mark: int,
    time_limit: float,
    cols: int = COLS,
    c: float = 1.2,
    max_iterations: int = 8000,
) -> tuple[int, MCTSNode]:
    """
    Run MCTS with tuned parameters.

    - Lower C (1.2) for more exploitation
    - More iterations (8000) for better tree search
    """
    root_board = list(root_board)
    legal = valid_moves(root_board, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(root_board))

    # Build root node
    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(root_board)
        drop(board_copy, col, mark, ROWS, cols)
        if check_win(board_copy, col, mark, ROWS, cols):
            node = MCTSNode(col=col, mark=mark, board_snapshot=list(board_copy))
            node.visits = 1
            node.wins = 1.0
            root_children[col] = node
            continue
        root_children[col] = MCTSNode(col=col, mark=mark, board_snapshot=list(board_copy))

    root = MCTSNode(col=-1, mark=mark, board_snapshot=list(root_board), children=root_children)

    start_time = time.time()
    iterations = 0

    while iterations < max_iterations:
        if time.time() - start_time > time_limit:
            break

        iterations += 1

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
                    child = MCTSNode(col=col, mark=current.mark, board_snapshot=list(board_copy))
                    current.children[col] = child
                    path.append(child)
                    current = child

        # --- SIMULATION ---
        sim_board = list(current.board_snapshot)
        sim_mark = 3 - current.mark
        reward = _simulate(sim_board, sim_mark, cols, max_steps=42)
        our_value = 1.0 - reward

        # --- BACK-PROPAGATION ---
        for node in reversed(path):
            if node.mark == mark:
                node.wins += our_value
            else:
                node.wins += 1.0 - our_value
            node.visits += 1

    if not root.children:
        return 0, root
    best = max(root.children.values(), key=lambda c: c.visits)
    return best.col, root


# ── Public bot API ─────────────────────────────────────────────────────────────

def mcts_puct_bot(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Strong MCTS bot with tuned PUCT parameters."""
    board_list = list(board)
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

    time_limit = 0.15
    if move_deadline is not None:
        time_limit = max(0.05, move_deadline - 0.05)

    if seed is not None:
        random.seed(seed)

    best_col, _ = _mcts_search(board_list, mark, time_limit, cols, c=1.2, max_iterations=8000)
    return best_col