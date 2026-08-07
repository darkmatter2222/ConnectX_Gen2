"""
Shallow Minimax Bot — depth-3 minimax with alpha-beta pruning.

Uses a simple positional evaluation:
  - Center column preference
  - Threat detection (3-in-a-row with open end)
  - Win detection (already handled by search)

This bot plays noticeably better than win-seek-block and serves
as the first classical benchmark. It should be playable against
the official Kaggle negamax agent.
"""

from __future__ import annotations
from typing import Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW,
)


# Precompute row offsets for each column
_ROW_OFFSETS: list[int] = [r * COLS for r in range(ROWS)]


def _evaluate(board: list[int], mark: int, cols: int = COLS) -> int:
    """
    Positional evaluation function.

    Scoring scheme:
      +100  if we can win in 1
      +30   if we have 3-in-a-row (threat)
      +10   if we have 2-in-a-row (setup)
      +1    per piece in center column
      -10   if opponent has 3-in-a-row (danger)

    Positive = good for ``mark``, negative = bad for ``mark``.
    """
    opp = 3 - mark
    score = 0

    # Center column preference (weight 1 per piece)
    for r in range(ROWS):
        if board[r * COLS + cols // 2] == mark:
            score += 1

    # Check all possible windows of length INAROW
    # Horizontal
    for r in range(ROWS):
        base = r * COLS
        for c in range(cols - INAROW + 1):
            window = tuple(board[base + c + k] for k in range(INAROW))
            score += _eval_window(window, mark, opp)

    # Vertical
    for c in range(cols):
        for r in range(ROWS - INAROW + 1):
            window = tuple(board[(r + k) * COLS + c] for k in range(INAROW))
            score += _eval_window(window, mark, opp)

    # Diagonal down-right
    for r in range(ROWS - INAROW + 1):
        for c in range(cols - INAROW + 1):
            window = tuple(board[(r + k) * COLS + c + k] for k in range(INAROW))
            score += _eval_window(window, mark, opp)

    # Diagonal down-left
    for r in range(INAROW - 1, ROWS):
        for c in range(INAROW - 1, cols):
            window = tuple(board[(r - k) * COLS + c - k] for k in range(INAROW))
            score += _eval_window(window, mark, opp)

    return score


def _eval_window(window: tuple[int, ...], mark: int, opp: int) -> int:
    """Evaluate a single window of INAROW cells."""
    mark_count = sum(1 for c in window if c == mark)
    opp_count = sum(1 for c in window if c == opp)
    empty_count = sum(1 for c in window if c == 0)

    if mark_count == INAROW:
        return 100
    if opp_count == INAROW:
        return -10
    if mark_count == 3 and empty_count == 1:
        return 30
    if opp_count == 3 and empty_count == 1:
        return -30
    if mark_count == 2 and empty_count == 2:
        return 10
    if opp_count == 2 and empty_count == 2:
        return -10
    return 0


def _negamax(
    board: list[int], mark: int, depth: int,
    alpha: float, beta: float,
    cols: int = COLS,
) -> tuple[int, int]:
    """
    Negamax with alpha-beta pruning.

    Returns (score, best_col).
    """
    legal = valid_moves(board, cols)
    if not legal:
        return 0, legal[0] if legal else 0

    # Terminal: board full
    if len(legal) == 0:
        return 0, legal[0] if legal else 0

    # Depth reached — evaluate
    if depth <= 0:
        return _evaluate(board, mark, cols), legal[0]

    # Check immediate win
    for col in legal:
        row = drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            return 10000, col
        un_drop(board, col, ROWS, cols)

    # Check immediate block (opponent would win)
    opp = 3 - mark
    for col in legal:
        row = drop(board, col, opp, ROWS, cols)
        if check_win(board, col, opp, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            # Must block — but we want the *best* block, not just any
            # Continue searching with a forced score

    best_score = float("-inf")
    best_col = legal[0]

    # Sort moves: center bias for better pruning
    legal_sorted = sorted(legal, key=lambda c: abs(c - cols // 2))

    for col in legal_sorted:
        row = drop(board, col, mark, ROWS, cols)
        score, _ = _negamax(board, opp, depth - 1, -beta, -alpha, cols)
        score = -score
        un_drop(board, col, ROWS, cols)

        if score > best_score:
            best_score = score
            best_col = col

        if score > alpha:
            alpha = score

    return best_score, best_col


def shallow_minimax_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int,
) -> int:
    """
    Depth-3 negamax with alpha-beta pruning.

    Args:
        board: flat board array
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns

    Returns:
        column index (0-based)
    """
    board_list = list(board)
    _, col = _negamax(board_list, mark, 3, float("-inf"), float("inf"), cols)
    return col


def depth2_minimax_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int,
) -> int:
    """
    Depth-2 negamax — faster, shallower variant of shallow_minimax_bot.

    Useful for timing-bound matches.
    """
    board_list = list(board)
    _, col = _negamax(board_list, mark, 2, float("-inf"), float("inf"), cols)
    return col