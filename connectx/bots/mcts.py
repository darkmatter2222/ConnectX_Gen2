"""
Monte Carlo Tree Search (MCTS) Bot — pure simulation-based player.

Builds a search tree from the current position through repeated
iterations of: selection → expansion → simulation → back-propagation.

Uses PUCT (Predictor-Utility Curvature Upper Confidence Bound) for
exploration:

    score(q, n, N) = q / n + C * sqrt(ln(N) / n)

The rollout phase uses a **tactical playout**: each player prefers
winning moves, then blocking, then center columns, then random.
This produces far more informative simulations than pure random
play.

Strength: strong tactical awareness through deep simulation search.
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
    col: int  # move that led to this node
    mark: int  # which mark placed this move
    board_snapshot: list[int]  # board state AFTER this move
    wins: float = 0.0  # total wins from current player's perspective
    visits: int = 0
    children: dict[int, 'MCTSNode'] = field(default_factory=dict)
    is_terminal: bool = False

    @property
    def best_child(self) -> Optional['MCTSNode']:
        """Return the child with the highest visit count."""
        if not self.children:
            return None
        return max(self.children.values(), key=lambda c: c.visits)

    def puct_score(self, c: float, parent_visits: int) -> float:
        """
        PUCT (Predictor-Utility Curvature Upper Confidence Bound) score.

        Higher = more promising for exploration.
        """
        if self.visits == 0:
            return float('inf')  # unvisited nodes get infinite UCB
        if parent_visits <= 1:
            return self.wins / self.visits  # no exploration bonus needed
        q = self.wins / self.visits  # win rate from our perspective
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

def _simulate(
    board: list[int], mark: int, cols: int,
    max_steps: int = 42,
) -> float:
    """
    Tactical rollout from current position to terminal.

    Each player prefers:
      1. Immediate wins
      2. Blocking opponent's wins
      3. Center column preference (with 80/20 noise)
      4. Otherwise random

    Returns:
        1.0 if mark wins, 0.0 if draw/opponent wins
    """
    opp = 3 - mark
    steps = 0

    while steps < max_steps:
        legal = valid_moves(board, cols)
        if not legal:
            return 0.0  # no moves left — draw or opponent wins

        # Priority 1: find a winning move
        win_move: Optional[int] = None
        for col in list(legal):
            try:
                row = drop(board, col, mark, ROWS, cols)
            except ValueError:
                continue
            if check_win(board, col, mark, ROWS, cols):
                un_drop(board, col, ROWS, cols, row=row)
                win_move = col
                break
            un_drop(board, col, ROWS, cols, row=row)

        if win_move is not None:
            try:
                drop(board, win_move, mark, ROWS, cols)
            except ValueError:
                # Column became full — skip
                mark, opp = opp, mark
                continue
            return 1.0  # mark wins

        # Priority 2: block opponent's win
        block_move: Optional[int] = None
        for col in list(legal):
            try:
                row = drop(board, col, opp, ROWS, cols)
            except ValueError:
                continue
            if check_win(board, col, opp, ROWS, cols):
                un_drop(board, col, ROWS, cols, row=row)
                block_move = col
                break
            un_drop(board, col, ROWS, cols, row=row)

        if block_move is not None:
            try:
                drop(board, block_move, mark, ROWS, cols)
                steps += 1
                mark, opp = opp, mark
                continue
            except ValueError:
                mark, opp = opp, mark
                continue

        # Priority 3: prefer center columns (left-to-right from center)
        center = cols // 2
        ordered: list[int] = []
        for offset in range(cols):
            left = center - offset
            if left >= 0 and left in legal:
                ordered.append(left)
            right = center + 1 + offset
            if right < cols and right in legal:
                ordered.append(right)

        if ordered:
            if random.random() < 0.8:
                col = ordered[0]
            else:
                col = random.choice(ordered)
        elif legal:
            col = random.choice(legal)
        else:
            return 0.0

        # Filter out full columns (gravity may have filled them)
        available = valid_moves(board, cols)
        while col not in available:
            if not available:
                return 0.0  # no moves left — draw or opponent wins
            col = random.choice(available)
            available = valid_moves(board, cols)

        try:
            drop(board, col, mark, ROWS, cols)
        except ValueError:
            continue  # shouldn't happen after filtering

        steps += 1
        mark, opp = opp, mark

    return 0.0  # no win found — draw or opponent wins


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
    Run MCTS iterations until time is up or max iterations reached.

    Returns (best_col, root_node).
    """
    root_board = list(root_board)
    legal = valid_moves(root_board, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(root_board))

    # Build root node from all legal moves
    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(root_board)
        drop(board_copy, col, mark, ROWS, cols)
        if check_win(board_copy, col, mark, ROWS, cols):
            node = MCTSNode(
                col=col, mark=mark, board_snapshot=list(board_copy),
            )
            node.visits = 1
            node.wins = 1.0
            root_children[col] = node
            continue

        node = MCTSNode(
            col=col, mark=mark, board_snapshot=list(board_copy),
        )
        root_children[col] = node

    root = MCTSNode(
        col=-1, mark=mark, board_snapshot=list(root_board),
        children=root_children,
    )

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

                    if check_win(board_copy, col, current.mark, ROWS, cols):
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                        )
                    else:
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                        )

                    current.children[col] = child
                    path.append(child)
                    current = child
                elif current.visits == 0:
                    col = min(legal)
                    board_copy = list(current.board_snapshot)
                    drop(board_copy, col, current.mark, ROWS, cols)
                    child = MCTSNode(
                        col=col, mark=current.mark,
                        board_snapshot=list(board_copy),
                    )
                    current.children[col] = child
                    path.append(child)
                    current = child

        # --- SIMULATION ---
        sim_board = list(current.board_snapshot)
        sim_mark = 3 - current.mark
        reward = _simulate(sim_board, sim_mark, cols, max_steps=42)

        # Convert: 1.0 = sim_mark won → our_value = 0 (we lost)
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


def mcts_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    MCTS bot — Monte Carlo tree search with tactical playouts.

    Args:
        board: flat board array (read-only)
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns
        move_deadline: optional epoch time when this move must be returned
        remaining_overage: seconds of overage budget (unused)
        seed: optional random seed for reproducibility

    Returns:
        column index (0-based)
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

    board_list = list(board)

    # Compute time budget (leave 50ms margin)
    time_limit = 0.15
    if move_deadline is not None:
        time_limit = max(0.05, move_deadline - time.time() - 0.05)

    if seed is not None:
        random.seed(seed)

    best_col, _ = _mcts_search(board_list, mark, time_limit, cols, c=1.4)
    return best_col


def mcts_bot_fast(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    Fast MCTS bot — fixed 500 iterations, no time management.

    For matches where the full MCTS might exceed the action deadline.
    """
    board_list = list(board)

    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    for col in legal:
        board_list[col] = mark
        if check_win(board_list, col, mark, ROWS, cols):
            board_list[col] = 0
            return col
        board_list[col] = 0

    opp = 3 - mark
    for col in legal:
        board_list[col] = opp
        if check_win(board_list, col, opp, ROWS, cols):
            board_list[col] = 0
            board_list = list(board)
            return col
        board_list[col] = 0

    board_list = list(board)
    best_col, _ = _mcts_search(
        board_list, mark, 0.1, cols, c=1.4, max_iterations=500,
    )
    return best_col


# ── Value-guided MCTS ──────────────────────────────────────────────────────────


def _value_evaluation(
    board: list[int], root_mark: int, cols: int = COLS,
) -> float:
    """
    Evaluate board using the trained value network.

    Returns value in [0, 1] representing win probability from
    root_mark's perspective.  Uses SimpleValueNet CPU fallback.
    """
    try:
        from connectx.bots.connectx_value_net import get_value_net
        net = get_value_net()
        v = net.evaluate(board, root_mark, cols)
        # v is in [-1, +1] → map to [0, 1]
        return (v + 1.0) / 2.0
    except Exception:
        return 0.5  # fallback: neutral


def mcts_bot_value(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    MCTS bot — Monte Carlo tree search with value-network leaf evaluation.

    Uses the trained value network to evaluate terminal / leaf positions
    instead of (or in addition to) tactical playouts.  MCTS tolerates
    coarse value predictions better than alpha-beta because it averages
    over many simulations.

    Hybrid approach:
      - Value network provides the primary leaf estimate.
      - Tactical playout validates the value when the network is uncertain
        (near 0.5 draw zone) or when the value is an obvious terminal result.

    Args:
        board: flat board array (read-only)
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns
        move_deadline: optional epoch time when this move must be returned
        remaining_overage: seconds of overage budget (unused)
        seed: optional random seed for reproducibility

    Returns:
        column index (0-based)
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

    board_list = list(board)

    # Compute time budget (leave 50ms margin)
    time_limit = 0.15
    if move_deadline is not None:
        time_limit = max(0.05, move_deadline - time.time() - 0.05)

    if seed is not None:
        random.seed(seed)

    best_col, _ = _mcts_search_value(
        board_list, mark, time_limit, cols, c=1.4
    )
    return best_col


def _mcts_search_value(
    root_board: list[int],
    mark: int,
    time_limit: float,
    cols: int = COLS,
    c: float = 1.4,
    max_iterations: int = 5000,
) -> tuple[int, MCTSNode]:
    """
    MCTS search with value-network leaf evaluation.

    Same structure as _mcts_search but replaces the SIMULATION phase
    with value-network prediction for leaf evaluation.
    """
    root_board = list(root_board)
    legal = valid_moves(root_board, cols)
    if not legal:
        return 0, MCTSNode(col=0, mark=mark, board_snapshot=list(root_board))

    # Build root node from all legal moves
    root_children: dict[int, MCTSNode] = {}
    for col in legal:
        board_copy = list(root_board)
        drop(board_copy, col, mark, ROWS, cols)
        if check_win(board_copy, col, mark, ROWS, cols):
            node = MCTSNode(
                col=col, mark=mark, board_snapshot=list(board_copy),
            )
            node.visits = 1
            node.wins = 1.0
            root_children[col] = node
            continue

        node = MCTSNode(
            col=col, mark=mark, board_snapshot=list(board_copy),
        )
        root_children[col] = node

    root = MCTSNode(
        col=-1, mark=mark, board_snapshot=list(root_board),
        children=root_children,
    )

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
                elif p == best_puct and child.visits > (
                    best_child.visits if best_child else 0
                ):
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
                unexplored = [
                    col for col in legal if col not in explored
                ]
                if unexplored:
                    col = min(unexplored)
                    board_copy = list(current.board_snapshot)
                    drop(board_copy, col, current.mark, ROWS, cols)

                    if check_win(board_copy, col, current.mark, ROWS, cols):
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                        )
                    else:
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                        )

                    current.children[col] = child
                    path.append(child)
                    current = child
                elif current.visits == 0:
                    col = min(legal)
                    board_copy = list(current.board_snapshot)
                    drop(board_copy, col, current.mark, ROWS, cols)
                    child = MCTSNode(
                        col=col, mark=current.mark,
                        board_snapshot=list(board_copy),
                    )
                    current.children[col] = child
                    path.append(child)
                    current = child

        # --- VALUE EVALUATION ---
        # Use the value network for leaf evaluation from the ROOT
        # player's perspective.  The value is in [0, 1].
        value = _value_evaluation(current.board_snapshot, mark, cols)

        # Blend with tactical playout when value is near-neutral
        # (the network is uncertain in draw-like positions).
        if 0.35 < value < 0.65:
            sim_board = list(current.board_snapshot)
            sim_mark = 3 - current.mark
            reward = _simulate(
                sim_board, sim_mark, cols, max_steps=42
            )
            # Weighted average: 70% value, 30% playout
            value = 0.7 * value + 0.3 * (1.0 - reward)

        # --- BACK-PROPAGATION ---
        for node in reversed(path):
            if node.mark == mark:
                node.wins += value
            else:
                node.wins += 1.0 - value
            node.visits += 1

    # Return the most-visited child (most reliable estimate)
    if not root.children:
        return 0, root
    best = max(root.children.values(), key=lambda c: c.visits)
    return best.col, root