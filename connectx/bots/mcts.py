"""
Monte Carlo Tree Search (MCTS) Bot — pure simulation-based player.

Builds a search tree from the current position through repeated
iterations of: selection → expansion → simulation → back-propagation.

Uses PUCT (Predictor-Utility Curvature Upper Confidence Bound) for
exploration:

    score(q, n, N) = q / n + C * sqrt(ln(N) / n)

where q = accumulated reward, n = node visits, N = parent visits,
C = exploration constant.

Strength: strong tactical awareness through deep random playouts.
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
    wins: float = 0.0  # total wins from this node's perspective
    visits: int = 0
    children: dict[int, 'MCTSNode'] = field(default_factory=dict)
    is_terminal: bool = False
    terminal_value: float = 0.0  # 1.0 = current player won, -1.0 = lost, 0.0 = draw

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
        q = self.wins / self.visits  # win rate from our perspective
        c_term = c * math.sqrt(math.log(parent_visits) / self.visits)
        return q + c_term


# ── Board hash for fast lookup ─────────────────────────────────────────────────

_ZOBRIST: list[list[int]] = []


def _init_zobrist() -> None:
    import random
    rng = random.Random(42)
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


# ── MCTS Search ────────────────────────────────────────────────────────────────


def _simulate(
    board: list[int], mark: int, cols: int,
    max_steps: int = 42,
) -> float:
    """
    Random rollout from current position to terminal.

    Returns:
        1.0 if mark wins, 0.0 if draw/opponent wins
    """
    opp = 3 - mark
    legal = valid_moves(board, cols)
    steps = 0

    while legal and steps < max_steps:
        # Simple: pick a random legal move
        col = random.choice(legal)
        drop(board, col, mark, ROWS, cols)

        if check_win(board, col, mark, ROWS, cols):
            return 1.0  # mark wins

        # Switch player
        mark, opp = opp, mark
        legal = valid_moves(board, cols)
        steps += 1

    return 0.0  # no win found → draw or opponent wins


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
        # Check if this move wins immediately
        if check_win(board_copy, col, mark, ROWS, cols):
            node = MCTSNode(
                col=col, mark=mark, board_snapshot=list(board_copy),
                is_terminal=True, terminal_value=1.0,
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
            # Find best child by PUCT score
            best_puct = float('-inf')
            best_child = None
            for child in current.children.values():
                p = child.puct_score(c, current.visits)
                if p > best_puct:
                    best_puct = p
                    best_child = child
                elif p == best_puct and child.visits > (best_child.visits if best_child else 0):
                    # Tie-break: prefer more visited (more stable estimate)
                    best_child = child

            if best_child is None:
                break

            current = best_child
            path.append(current)

        # --- EXPANSION ---
        if not current.is_terminal and current.children:
            legal = valid_moves(current.board_snapshot, cols)
            if legal:
                # Find a legal move not yet explored
                explored = set(current.children.keys())
                unexplored = [col for col in legal if col not in explored]
                if unexplored:
                    # Pick the first unexplored legal move (deterministic)
                    col = min(unexplored)
                    board_copy = list(current.board_snapshot)
                    row = drop(board_copy, col, current.mark, ROWS, cols)

                    if check_win(board_copy, col, current.mark, ROWS, cols):
                        child = MCTSNode(
                            col=col, mark=current.mark,
                            board_snapshot=list(board_copy),
                            is_terminal=True, terminal_value=1.0,
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
                    # All moves explored but node is unvisited — just pick one
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
        sim_mark = 3 - current.mark  # opponent's turn to move next
        reward = _simulate(sim_board, sim_mark, cols, max_steps=42)

        # The reward is from the SIMULATION player's perspective.
        # We need to convert: if opponent (sim_mark) wins → reward=1 → our value = -1 → draw = 0.5
        # If sim_mark doesn't win → reward=0 → our value = 1 (for draw) or 0 (for loss)
        # Convert: our_value = 1.0 - reward (from our perspective, win=1, draw=0.5, loss=0)
        our_value = 1.0 - reward  # if opponent won, we lost (0); if no win, we get partial credit

        # --- BACK-PROPAGATION ---
        for node in reversed(path):
            # For nodes where it's the SEARCH player's turn
            # (these are the nodes we're evaluating FROM the search player's perspective)
            node.wins += our_value if node.mark == mark else (1.0 - our_value)
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
    MCTS bot — uses Monte Carlo tree search for move selection.

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

    # Compute time budget (leave 0.05s margin)
    time_limit = 0.15  # default: 150ms
    if move_deadline is not None:
        time_limit = max(0.05, move_deadline - time.time() - 0.05)

    # Use seed for reproducibility if provided
    if seed is not None:
        import random
        random.seed(seed)

    best_col, _ = _mcts_search(
        board_list, mark, time_limit,
        cols, c=1.4,
    )

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

    best_col, _ = _mcts_search(
        board_list, mark, 0.1, cols, c=1.4, max_iterations=500,
    )

    return best_col