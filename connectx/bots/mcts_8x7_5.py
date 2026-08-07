"""
MCTS (Monte Carlo Tree Search) Bot for 8×7/5 Connect Four.

Unlike 7×6/4 where MCTS was weak (solved game, perfect alpha-beta dominates),
8×7/5 is not solved — the larger branching factor and deeper win condition
give MCTS meaningful exploration value.

Uses UCB1 selection + random playouts + terminal win-detection pruning.
"""

from __future__ import annotations

import math
import time
import random
from collections import defaultdict
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
)

ROWS: int = 7
COLS: int = 8
INAROW: int = 5


def _positional_heuristic(board: list[int], mark: int, cols: int) -> float:
    """Lightweight positional evaluation for playout termination.

    Scores from mark's perspective. Returns value in [-1, +1].
    Considers center control, height advantage, and adjacency.
    """
    score = 0.0
    opp = 3 - mark

    center_col = cols // 2
    my_center = 0
    opp_center = 0
    my_height = 0
    opp_height = 0
    my_adjacent = 0
    opp_adjacent = 0

    for i in range(len(board)):
        cell = board[i]
        if cell == 0:
            continue
        r = i // cols
        c = i % cols
        height = r / (ROWS - 1)  # Normalized height 0-1

        if cell == mark:
            if c == center_col:
                my_center += 1
            elif abs(c - center_col) <= 1:
                my_center += 0.5
            my_height += height

            # Adjacency: check neighbors
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                nr, nc = r + dr, c + dc
                ni = nr * cols + nc
                if 0 <= nr < ROWS and 0 <= nc < cols and board[ni] == mark:
                    my_adjacent += 1
        else:
            if c == center_col:
                opp_center += 1
            elif abs(c - center_col) <= 1:
                opp_center += 0.5
            opp_height += height
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                nr, nc = r + dr, c + dc
                ni = nr * cols + nc
                if 0 <= nr < ROWS and 0 <= nc < cols and board[ni] == opp:
                    opp_adjacent += 1

    # Center advantage: weighted 40%
    score += 0.4 * (my_center - opp_center) / max(1, cols)
    # Height advantage: weighted 30%
    score += 0.3 * (my_height - opp_height) / ROWS
    # Adjacency: weighted 30%
    score += 0.3 * (my_adjacent - opp_adjacent) / max(1, len(board))

    return max(-1.0, min(1.0, score))


def _random_playout(
    board: list[int], start_mark: int, cols: int,
    rng: random.Random, max_depth: int = 200,
    use_heuristic: bool = False,
) -> float:
    """Random playout from current position.

    Returns +1 if start_mark wins, -1 if opponent wins, 0 for draw.
    If use_heuristic, scores terminal positions positionally instead of
    by piece count.
    """
    b = list(board)
    current_mark = start_mark
    depth = 0

    while depth < max_depth:
        legal = valid_moves(b, cols)
        if not legal:
            break

        # Check for terminal win
        for col in legal:
            row = drop(b, col, current_mark, ROWS, COLS)
            if check_win(b, col, current_mark, ROWS, COLS):
                # current_mark wins
                return 1.0 if current_mark == start_mark else -1.0
            un_drop(b, col, ROWS, COLS, row=row)

        # Board full?
        if len(legal) == 0:
            return 0.0  # Draw

        # Random move
        col = rng.choice(legal)
        drop(b, col, current_mark, ROWS, COLS)
        current_mark = 3 - current_mark
        depth += 1

    # Time limit reached mid-playout
    if use_heuristic:
        # Positional heuristic: better than piece count
        return _positional_heuristic(b, start_mark, cols)
    else:
        # Piece count fallback
        my_count = sum(1 for c in b if c == 1)
        opp_count = sum(1 for c in b if c == 2)
        diff = my_count - opp_count
        if start_mark == 1:
            return 1.0 if diff > 0 else (-1.0 if diff < 0 else 0.0)
        else:
            return 1.0 if diff < 0 else (-1.0 if diff > 0 else 0.0)


def mcts_bot_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
    num_simulations: int = 500,
    exploration: float = 1.414,
    use_heuristic: bool = False,
) -> int:
    """MCTS bot for 8×7/5 Connect Four.

    Uses a root-only MCTS: select from root children, simulate, backpropagate
    to root statistics. No deep tree — just root-level move selection.

    This is simpler and more robust than building a full tree, because:
    - 8 columns × 7 rows = 56 cells, deep trees exhaust memory fast
    - Root-only with repeated visits per move is sufficient

    Args:
        num_simulations: Number of iterations (each = select+sim+backprop).
        exploration: UCB1 exploration constant.
        use_heuristic: Use positional heuristic for playout termination
                       instead of simple piece count. More informative but
                       slightly slower per iteration.
    """
    board_list = list(board)
    legal = valid_moves(board_list, COLS)
    if not legal:
        return 0

    rng = random.Random(seed if seed is not None else int(time.time() * 1000) % (2**32))
    start_time = time.time()
    time_limit = move_deadline if move_deadline is not None else 2.0

    # Root-level statistics: per-move win count and visit count
    # Always from mark's perspective
    move_wins: dict[int, int] = defaultdict(int)
    move_visits: dict[int, int] = defaultdict(int)
    total_visits = 0

    best_col = legal[0]

    for sim in range(num_simulations):
        # Check time
        if time.time() - start_time >= time_limit * 0.95:
            break

        # --- Selection: pick a move using UCB1 ---
        # We select from root-level candidates: all legal moves
        # Each "selection" simulates playing that move, then doing a playout
        # The playout outcome tells us if that move leads to a win

        # But we also want to refine: re-select a move we've already tried,
        # play a new board position, and get a fresh playout.
        # This is a "root replay" strategy.

        # For simplicity: just pick the move with highest UCB1 at root level
        # and always start a fresh playout from the board position after that move.
        # Then backpropagate.

        # Pick move with best UCB1
        candidate_moves = []
        for c in legal:
            v = move_visits.get(c, 0)
            if v == 0:
                candidate_moves.append((c, float('inf')))
            else:
                win_rate = move_wins[c] / v
                ucb = win_rate + exploration * math.sqrt(
                    math.log(total_visits) / v
                )
                candidate_moves.append((c, ucb))

        if not candidate_moves:
            chosen = rng.choice(legal)
        else:
            chosen = max(candidate_moves, key=lambda x: x[1])[0]

        # --- Simulation: play chosen move, then random playout ---
        b_after = list(board_list)
        try:
            row = drop(b_after, chosen, mark, ROWS, COLS)
        except (ValueError, IndexError):
            continue

        # Check if chosen move is an immediate win
        if check_win(b_after, chosen, mark, ROWS, COLS):
            # Immediate win — definitely best
            move_wins[chosen] += 1
            move_visits[chosen] += 1
            total_visits += 1
            best_col = chosen  # Always pick immediate wins
            continue

        # Random playout from this position
        result = _random_playout(b_after, 3 - mark, COLS, rng, use_heuristic=use_heuristic)
        # result is from (3-mark)'s perspective; convert to mark's perspective
        result_from_mark = -result

        # Backpropagate: this move led to result_from_mark
        move_visits[chosen] += 1
        if result_from_mark > 0:
            move_wins[chosen] += 1
        total_visits += 1

    # Select best move: most visited (robust choice)
    if move_visits:
        best_col = max(legal, key=lambda c: move_visits.get(c, 0))

    if best_col not in legal:
        best_col = legal[0]
    return best_col


def mcts_bot_fast_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast MCTS for 8×7/5 — fewer simulations, good for time pressure."""
    return mcts_bot_8x7_5(
        board, mark, legal, cols, move_deadline,
        remaining_overage, seed,
        num_simulations=200,
    )


def mcts_bot_heuristic_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
    num_simulations: int = 500,
    exploration: float = 1.414,
) -> int:
    """MCTS for 8×7/5 with heuristic leaf evaluation.

    Uses positional heuristic (center control, height, adjacency) to score
    playout terminal positions instead of simple piece count. This provides
    more informative feedback to MCTS, especially in mid-game positions
    where piece count is less decisive.
    """
    return mcts_bot_8x7_5(
        board, mark, legal, cols, move_deadline,
        remaining_overage, seed,
        num_simulations=num_simulations,
        exploration=exploration,
        use_heuristic=True,
    )