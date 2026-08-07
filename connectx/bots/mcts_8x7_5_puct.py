"""
MCTS PUCT Bot for 8x7/5 Connect Four.

Full tree-search MCTS with PUCT (Policy-Upper Confidence Bound) selection.
Uses tactical playouts (win/block/center ordering) instead of random.
Compared against the UCB1 root-only MCTS in mcts_8x7_5.py.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional, Sequence

from connectx.engine import drop, un_drop, valid_moves, check_win

ROWS = 7
COLS = 8
INAROW = 5


@dataclass
class MCTSNode:
    """Node in the MCTS search tree."""
    col: int
    mark: int
    board_snapshot: list[int]
    wins: float = 0.0
    visits: int = 0
    children: dict[int, MCTSNode] = field(default_factory=dict)
    is_terminal: bool = False

    def puct_score(self, c: float, parent_visits: int) -> float:
        """PUCT: q/n + C * sqrt(log(N) / n)."""
        if self.visits == 0:
            return float('inf')
        if parent_visits <= 1:
            return self.wins / self.visits
        q = self.wins / self.visits
        c_term = c * math.sqrt(math.log(parent_visits) / self.visits)
        return q + c_term


def _tactical_playout(
    board: list[int], start_mark: int,
    cols: int, max_steps: int = 200,
) -> float:
    """Tactical playout with smart move ordering.

    Instead of random moves, each player prefers:
      1. Immediate wins
      2. Blocking opponent wins
      3. Center column preference
      4. Otherwise random
    """
    opp = 3 - start_mark
    b = list(board)
    current = start_mark
    steps = 0

    while steps < max_steps:
        legal = valid_moves(b, cols)
        if not legal:
            return 0.0

        # Priority 1: find a winning move
        for col in list(legal):
            try:
                row = drop(b, col, current, ROWS, COLS)
            except ValueError:
                continue
            if check_win(b, col, current, ROWS, COLS):
                return 1.0 if current == start_mark else -1.0
            un_drop(b, col, ROWS, COLS, row=row)

        # Priority 2: block opponent's win
        blocked = False
        for col in list(legal):
            try:
                row = drop(b, col, opp, ROWS, COLS)
            except ValueError:
                continue
            if check_win(b, col, opp, ROWS, COLS):
                un_drop(b, col, ROWS, COLS, row=row)
                current = opp
                steps += 1
                blocked = True
                break
            un_drop(b, col, ROWS, COLS, row=row)
        if blocked:
            opp = 3 - current
            continue

        # Priority 3: center column preference
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

        # Retry if column is now full
        available = valid_moves(b, cols)
        while col not in available:
            if not available:
                return 0.0
            col = random.choice(available)
            available = valid_moves(b, cols)

        try:
            drop(b, col, current, ROWS, COLS)
        except ValueError:
            current = opp
            opp = 3 - current
            continue

        steps += 1
        current = 3 - current
        opp = 3 - current

    # Time limit — draw
    return 0.0


def _mcts_search(
    root_board: list[int],
    mark: int,
    time_limit: float,
    cols: int = COLS,
    c: float = 1.2,
    max_iterations: int = 5000,
) -> tuple[int, MCTSNode]:
    """Run full tree MCTS with PUCT selection."""
    root_board = list(root_board)
    legal = valid_moves(root_board, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(root_board))

    # Check for immediate win
    for col in legal:
        board_copy = list(root_board)
        row = drop(board_copy, col, mark, ROWS, COLS)
        if check_win(board_copy, col, mark, ROWS, COLS):
            return col, None
        un_drop(board_copy, col, ROWS, COLS, row=row)

    # Build root node
    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(root_board)
        row = drop(board_copy, col, mark, ROWS, COLS)
        node = MCTSNode(
            col=col, mark=mark, board_snapshot=list(board_copy)
        )
        root_children[col] = node

    root = MCTSNode(
        col=-1, mark=mark, board_snapshot=list(root_board),
        children=root_children
    )

    start_time = time.time()
    iterations = 0

    while iterations < max_iterations:
        if time.time() - start_time > time_limit:
            break

        iterations += 1

        # === SELECTION ===
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

        # === EXPANSION ===
        if not current.is_terminal:
            legal = valid_moves(current.board_snapshot, cols)
            if legal:
                explored = set(current.children.keys())
                unexplored = [col for col in legal if col not in explored]
                if unexplored:
                    col = unexplored[0]
                    board_copy = list(current.board_snapshot)
                    row = drop(board_copy, col, current.mark, ROWS, COLS)
                    child = MCTSNode(
                        col=col, mark=current.mark,
                        board_snapshot=list(board_copy)
                    )
                    current.children[col] = child
                    path.append(child)
                    current = child

        # === SIMULATION ===
        sim_board = list(current.board_snapshot)
        sim_mark = 3 - current.mark
        reward = _tactical_playout(sim_board, sim_mark, cols, max_steps=200)

        # Convert from sim_mark's perspective to current.mark's perspective
        our_value = -reward

        # === BACK-PROPAGATION ===
        for node in reversed(path):
            if node.mark == mark:
                node.wins += our_value
            else:
                node.wins += -our_value
            node.visits += 1

    if not root.children:
        return 0, root
    best = max(root.children.values(), key=lambda c: c.visits)
    return best.col, root


# ── Public bot API ─────────────────────────────────────────────────────────────


def mcts_puct_bot_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
    num_simulations: int = 5000,
    exploration: float = 1.2,
) -> int:
    """PUCT MCTS bot for 8x7/5 with tactical playouts.

    Args:
        num_simulations: Target iteration count.
        exploration: PUCT exploration constant (C parameter).
    """
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = move_deadline if move_deadline is not None else 2.0
    time_limit = max(0.05, time_limit - 0.05)

    if seed is not None:
        random.seed(seed)

    best_col, _ = _mcts_search(
        board_list, mark, time_limit, cols,
        c=exploration, max_iterations=num_simulations
    )
    return best_col


def mcts_puct_bot_fast_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast PUCT MCTS for 8x7/5 — half time, fewer iterations."""
    return mcts_puct_bot_8x7_5(
        board, mark, legal, cols, move_deadline,
        remaining_overage, seed,
        num_simulations=2500,
        exploration=1.2,
    )