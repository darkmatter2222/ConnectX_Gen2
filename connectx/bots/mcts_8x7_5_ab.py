"""AB-guided MCTS for 8×7/5 Connect Four.

Enhances MCTS with alpha-beta evaluation at terminal positions during playouts.
Instead of binary win/loss (±1.0), uses AB heuristic evaluation for nuanced
position quality feedback.
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


# ── Win-line masks ────────────────────────────────────────────────────────────

_LINE_MASKS: list[int] = []


def _precompute_line_masks() -> list[int]:
    masks = []
    for r in range(ROWS):
        for c in range(COLS - INAROW + 1):
            mask = 0
            for k in range(INAROW):
                mask |= 1 << (r * COLS + c + k)
            masks.append(mask)
    for c in range(COLS):
        for r in range(ROWS - INAROW + 1):
            mask = 0
            for k in range(INAROW):
                mask |= 1 << ((r + k) * COLS + c)
            masks.append(mask)
    for r in range(ROWS - INAROW + 1):
        for c in range(COLS - INAROW + 1):
            mask = 0
            for k in range(INAROW):
                mask |= 1 << ((r + k) * COLS + c + k)
            masks.append(mask)
    for r in range(ROWS - INAROW + 1):
        for c in range(INAROW - 1, COLS):
            mask = 0
            for k in range(INAROW):
                mask |= 1 << ((r + k) * COLS + c - k)
            masks.append(mask)
    return masks


_LINE_MASKS = _precompute_line_masks()


def _popcount(x: int) -> int:
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count


def _to_bitboard(board: list[int], mark: int) -> int:
    bb = 0
    for i in range(len(board)):
        if board[i] == mark:
            bb |= 1 << i
    return bb


# ── AB evaluation for playout terminal ───────────────────────────────────────

def _ab_eval(board: list[int], mark: int) -> float:
    """Lightweight AB eval: threats + column control."""
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    score = 0.0
    player_threats = opp_threats = 0

    for line_mask in _LINE_MASKS:
        p_count = _popcount(player_bb & line_mask)
        o_count = _popcount(opp_bb & line_mask)
        e_count = _popcount((~player_bb & ~opp_bb) & line_mask)

        if p_count == (INAROW - 1) and e_count >= 1:
            player_threats += 1
        if o_count == (INAROW - 1) and e_count >= 1:
            opp_threats += 1

    score += player_threats * 5000.0 - opp_threats * 5000.0

    center = COLS // 2
    mark_col = opp_col = [0] * COLS
    for c in range(COLS):
        for r in range(ROWS):
            v = board[r * COLS + c]
            if v == mark:
                mark_col[c] = 1
            elif v == opp:
                opp_col[c] = 1

    for c in range(COLS):
        d = abs(c - center)
        w = 2.0 if d == 0 else (1.0 if d == 1 else 0.5)
        score += (mark_col[c] - opp_col[c]) * w

    return score


# ── Tactical helpers ──────────────────────────────────────────────────────────

def _is_win(board: list[int], mark: int) -> Optional[int]:
    for col in valid_moves(board, COLS):
        row = drop(board, col, mark, ROWS, COLS)
        if check_win(board, col, mark, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            return col
        un_drop(board, col, ROWS, COLS, row=row)
    return None


def _is_block(board: list[int], mark: int) -> Optional[int]:
    opp = 3 - mark
    for col in valid_moves(board, COLS):
        row = drop(board, col, opp, ROWS, COLS)
        if check_win(board, col, opp, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            return col
        un_drop(board, col, ROWS, COLS, row=row)
    return None


def _is_threat(board: list[int], mark: int) -> list[int]:
    threats = []
    for col in valid_moves(board, COLS):
        row = drop(board, col, mark, ROWS, COLS)
        if check_win(board, col, mark, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            continue
        player_bb = _to_bitboard(board, mark)
        for line_mask in _LINE_MASKS:
            if _popcount(player_bb & line_mask) >= INAROW - 1:
                threats.append(col)
                break
        un_drop(board, col, ROWS, COLS, row=row)
    return threats


# ── AB-guided playout ────────────────────────────────────────────────────────

def _ab_playout(
    board: list[int], start_mark: int,
    cols: int, max_steps: int = 200,
) -> float:
    """AB-guided playout with tactical moves + AB eval termination."""
    opp = 3 - start_mark
    b = list(board)
    current = start_mark
    steps = 0

    while steps < max_steps:
        legal = valid_moves(b, cols)
        if not legal:
            break

        win_col = _is_win(b, current)
        if win_col is not None:
            return 1.0 if current == start_mark else -1.0

        block_col = _is_block(b, current)
        if block_col is not None:
            row = drop(b, block_col, current, ROWS, COLS)
            steps += 1
            current, opp = opp, 3 - opp
            continue

        threats = _is_threat(b, current)
        if threats:
            row = drop(b, threats[0], current, ROWS, COLS)
            steps += 1
            current, opp = opp, 3 - opp
            continue

        opp_threats = _is_threat(b, opp)
        if opp_threats:
            row = drop(b, opp_threats[0], current, ROWS, COLS)
            steps += 1
            current, opp = opp, 3 - opp
            continue

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
            col = ordered[0] if random.random() < 0.85 else random.choice(ordered)
        elif legal:
            col = random.choice(legal)
        else:
            break

        available = valid_moves(b, cols)
        while col not in available:
            if not available:
                break
            col = random.choice(available)
            available = valid_moves(b, cols)

        try:
            drop(b, col, current, ROWS, COLS)
        except ValueError:
            current, opp = opp, 3 - opp
            continue

        steps += 1
        current, opp = opp, 3 - opp

    our_eval = _ab_eval(b, start_mark)
    return max(-1.0, min(1.0, our_eval / 30.0))


# ── MCTS search ───────────────────────────────────────────────────────────────

@dataclass
class MCTSNode:
    col: int
    mark: int
    board_snapshot: list[int]
    wins: float = 0.0
    visits: int = 0
    children: dict[int, MCTSNode] = field(default_factory=dict)
    is_terminal: bool = False

    def puct_score(self, c: float, parent_visits: int) -> float:
        if self.visits == 0:
            return float('inf')
        if parent_visits <= 1:
            return self.wins / self.visits
        q = self.wins / self.visits
        c_term = c * math.sqrt(math.log(parent_visits) / self.visits)
        return q + c_term


def _mcts_search(
    root_board: list[int], mark: int, time_limit: float,
    cols: int = COLS, c: float = 1.2, max_iterations: int = 5000,
) -> tuple[int, MCTSNode]:
    root_board = list(root_board)
    legal = valid_moves(root_board, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(root_board))

    for col in legal:
        board_copy = list(root_board)
        row = drop(board_copy, col, mark, ROWS, COLS)
        if check_win(board_copy, col, mark, ROWS, COLS):
            return col, None
        un_drop(board_copy, col, ROWS, COLS, row=row)

    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(root_board)
        row = drop(board_copy, col, mark, ROWS, COLS)
        root_children[col] = MCTSNode(col=col, mark=mark, board_snapshot=list(board_copy))

    root = MCTSNode(col=-1, mark=mark, board_snapshot=list(root_board), children=root_children)
    start_time = time.time()
    iterations = 0

    while iterations < max_iterations:
        if time.time() - start_time > time_limit:
            break
        iterations += 1

        current = root
        path = [root]
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

        if not current.is_terminal:
            legal = valid_moves(current.board_snapshot, cols)
            if legal:
                explored = set(current.children.keys())
                unexplored = [col for col in legal if col not in explored]
                if unexplored:
                    col = unexplored[0]
                    board_copy = list(current.board_snapshot)
                    row = drop(board_copy, col, current.mark, ROWS, COLS)
                    child = MCTSNode(col=col, mark=current.mark, board_snapshot=list(board_copy))
                    current.children[col] = child
                    path.append(child)
                    current = child

        sim_board = list(current.board_snapshot)
        sim_mark = 3 - current.mark
        reward = _ab_playout(sim_board, sim_mark, cols, max_steps=200)
        our_value = -reward

        for node in reversed(path):
            if node.mark == mark:
                node.wins += our_value
            else:
                node.wins += -our_value
            node.visits += 1

    if not root.children:
        return 0, root
    best = max(root.children.values(), key=lambda n: n.visits)
    return best.col, root


# ── Public bot API ────────────────────────────────────────────────────────────

def mcts_ab_bot_8x7_5(
    board: Sequence[int], mark: int,
    legal: Optional[Sequence[int]] = None, cols: int = COLS,
    move_deadline: Optional[float] = None, remaining_overage: float = 0.0,
    seed: Optional[int] = None, num_simulations: int = 5000,
    exploration: float = 1.2,
) -> int:
    """AB-guided MCTS for 8x7/5 with AB terminal eval + tactical playouts."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0
    time_limit = max(0.05, (move_deadline if move_deadline else 2.0) - 0.05)
    if seed is not None:
        random.seed(seed)
    best_col, _ = _mcts_search(board_list, mark, time_limit, cols, c=exploration, max_iterations=num_simulations)
    return best_col


def mcts_ab_bot_fast_8x7_5(
    board: Sequence[int], mark: int,
    legal: Optional[Sequence[int]] = None, cols: int = COLS,
    move_deadline: Optional[float] = None, remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast AB-guided MCTS — 2500 simulations."""
    return mcts_ab_bot_8x7_5(
        board, mark, legal, cols, move_deadline, remaining_overage, seed,
        num_simulations=2500, exploration=1.2,
    )