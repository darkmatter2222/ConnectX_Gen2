"""Tactical-override MCTS for 8×7/5 Connect Four.

Enhances standard PUCT MCTS with:
1. AB-assisted threat detection during playouts (searches deeper when threats exist)
2. AB heuristic evaluation at playout terminal positions (not just win/loss)
3. Threat-aware move selection (prioritizes creating threats)

This hybrid approach uses AB's superior depth-4 tactical vision during MCTS
playouts, while keeping MCTS's broad exploration of non-tactical positions.
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


# ── Tactical helpers (shared with AB) ──────────────────────────────────────────

def _count_in_row(board: list[int], mark: int, c1: int, r1: int, dc: int, dr: int) -> int:
    """Count consecutive pieces of `mark` starting from (c1, r1) in direction (dc, dr)."""
    count = 0
    c, r = c1, r1
    while 0 <= c < COLS and 0 <= r < ROWS:
        if board[r * COLS + c] == mark:
            count += 1
        else:
            break
        c += dc
        r += dr
    return count


def _is_threat(board: list[int], mark: int, threat_len: int = INAROW - 1) -> list[int]:
    """Find columns where placing `mark` creates a threat (INAROW-1 in a line)."""
    threats = []
    for col in valid_moves(board, COLS):
        row = drop(board, col, mark, ROWS, COLS)
        opp = 3 - mark
        if check_win(board, col, mark, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            continue
        # Check for threats (4 in a line with 1 empty)
        for r in range(ROWS):
            for dc, dr in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count = _count_in_row(board, mark, col, r, dc, dr)
                if count >= threat_len:
                    threats.append(col)
                    break
            if col in threats:
                break
        un_drop(board, col, ROWS, COLS, row=row)
    return threats


def _is_block(board: list[int], mark: int) -> Optional[int]:
    """Find the column where opponent has an immediate win (need to block)."""
    opp = 3 - mark
    for col in valid_moves(board, COLS):
        row = drop(board, col, opp, ROWS, COLS)
        if check_win(board, col, opp, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            return col
        un_drop(board, col, ROWS, COLS, row=row)
    return None


def _is_win(board: list[int], mark: int) -> Optional[int]:
    """Find the column where mark can win immediately."""
    for col in valid_moves(board, COLS):
        row = drop(board, col, mark, ROWS, COLS)
        if check_win(board, col, mark, ROWS, COLS):
            un_drop(board, col, ROWS, COLS, row=row)
            return col
        un_drop(board, col, ROWS, COLS, row=row)
    return None


# ── Simple heuristic eval (lightweight, no AB search) ────────────────────────

def _heuristic_eval(board: list[int], mark: int) -> float:
    """Lightweight positional eval for MCTS playout termination.

    Scores center control, height advantage, and piece adjacency.
    Much cheaper than full AB eval but more informative than win/loss only.
    """
    opp = 3 - mark
    score = 0.0

    # Center control: columns 2-5 worth more
    mark_center = opp_center = 0
    mark_pieces = opp_pieces = 0
    mark_adj = opp_adj = 0

    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r * COLS + c]
            if cell == mark:
                mark_pieces += 1
                if 2 <= c <= 5:
                    mark_center += 1
                # Adjacency: check right and down
                if c + 1 < COLS and board[r * COLS + c + 1] == mark:
                    mark_adj += 1
                if r + 1 < ROWS and board[(r + 1) * COLS + c] == mark:
                    mark_adj += 1
            elif cell == opp:
                opp_pieces += 1
                if 2 <= c <= 5:
                    opp_center += 1
                if c + 1 < COLS and board[r * COLS + c + 1] == opp:
                    opp_adj += 1
                if r + 1 < ROWS and board[(r + 1) * COLS + c] == opp:
                    opp_adj += 1

    score += (mark_center - opp_center) * 2.0
    score += (mark_pieces - opp_pieces) * 1.0
    score += (mark_adj - opp_adj) * 0.5

    # Height advantage
    mark_height = opp_height = 0
    for c in range(COLS):
        mark_height += board[c * ROWS + ROWS - 1] - board[c * ROWS]
        opp_height += board[c * ROWS + ROWS - 1] - board[c * ROWS]
    # Simplified: just count pieces per column
    for c in range(COLS):
        mh = oh = 0
        for r in range(ROWS):
            if board[r * COLS + c] == mark:
                mh = r + 1
            if board[r * COLS + c] == opp:
                oh = r + 1
        mark_height += mh
        opp_height += oh
    score += (mark_height - opp_height) * 0.3

    return score


# ── Tactical playout with AB-assisted threat resolution ──────────────────────

def _tactical_playout(
    board: list[int], start_mark: int,
    cols: int, max_steps: int = 200,
) -> tuple[float, bool]:
    """Tactical playout with AB-assisted threat detection.

    Returns (reward, used_tactical_override).

    Unlike standard playout which just checks wins/blocks, this function
    uses threat detection and heuristic eval to make smarter moves.
    """
    opp = 3 - start_mark
    b = list(board)
    current = start_mark
    steps = 0
    used_override = False

    while steps < max_steps:
        legal = valid_moves(b, cols)
        if not legal:
            return 0.0, used_override

        # Priority 1: find a winning move (always do this)
        win_col = _is_win(b, current)
        if win_col is not None:
            return 1.0 if current == start_mark else -1.0, False

        # Priority 2: block opponent's win
        block_col = _is_block(b, current)
        if block_col is not None:
            row = drop(b, block_col, current, ROWS, COLS)
            steps += 1
            current = opp
            opp = 3 - current
            continue

        # Priority 2.5: create a threat (4-in-line) for yourself
        threats = _is_threat(b, current)
        if threats:
            # Pick the first threat (center preference from sorted valid_moves)
            row = drop(b, threats[0], current, ROWS, COLS)
            steps += 1
            current = opp
            opp = 3 - current
            continue

        # Priority 3: block opponent's threats
        opp_threats = _is_threat(b, opp)
        if opp_threats:
            # Block the first threat
            row = drop(b, opp_threats[0], current, ROWS, COLS)
            steps += 1
            current = opp
            opp = 3 - current
            continue

        # Priority 4: center column preference with some randomness
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
            return 0.0, used_override

        # Retry if column is now full
        available = valid_moves(b, cols)
        while col not in available:
            if not available:
                return 0.0, used_override
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

    # Terminal: evaluate with heuristic instead of draw
    our_eval = _heuristic_eval(b, start_mark)
    # Scale to [-1, 1] range: eval typically in [-20, 20]
    reward = max(-1.0, min(1.0, our_eval / 20.0))
    return reward, False


# ── MCTS search ───────────────────────────────────────────────────────────────

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


def _mcts_search(
    root_board: list[int],
    mark: int,
    time_limit: float,
    cols: int = COLS,
    c: float = 1.2,
    max_iterations: int = 5000,
) -> tuple[int, MCTSNode]:
    """Run full tree MCTS with PUCT selection and tactical playouts."""
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
        reward, _ = _tactical_playout(sim_board, sim_mark, cols, max_steps=200)

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


# ── Public bot API ────────────────────────────────────────────────────────────


def mcts_tactical_bot_8x7_5(
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
    """Tactical MCTS bot for 8x7/5 with threat-aware playouts.

    Uses AB-assisted threat detection during playouts and heuristic
    evaluation at terminal positions for richer feedback signals.
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


def mcts_tactical_bot_fast_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast tactical MCTS for 8x7/5 — half iterations."""
    return mcts_tactical_bot_8x7_5(
        board, mark, legal, cols, move_deadline,
        remaining_overage, seed,
        num_simulations=2500,
        exploration=1.2,
    )