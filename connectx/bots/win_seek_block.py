"""
Win-Seek-Block Bot — priority-order tactical bot.

Priority order:
  1. If a move wins immediately, take it.
  2. If an opponent move would win, block it.
  3. Otherwise, prefer center columns (bias toward the center).

This is a strong baseline against random play and a useful
diagnostic: if a deeper bot loses to this one, it lacks
basic tactics.
"""

from __future__ import annotations
from typing import Sequence

from connectx.engine import check_win, valid_moves


def _try_move(board: list[int], col: int, mark: int, cols: int) -> int:
    """
    Simulate dropping ``mark`` in ``col``.

    Returns the row where the piece landed, or -1 if column is full.
    Temporarily mutates and restores the board.
    """
    for r in range(len(board) // cols):
        idx = r * cols + col
        if board[idx] == 0:
            board[idx] = mark
            return r
    return -1


def _untry_move(board: list[int], col: int, cols: int) -> None:
    """Undo a temporary drop (remove top piece from column)."""
    for r in range(len(board) // cols - 1, -1, -1):
        idx = r * cols + col
        if board[idx] != 0:
            board[idx] = 0
            return


def win_seek_block_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int,
) -> int:
    """
    Priority-order tactical bot: win > block > center bias.

    Args:
        board: flat board array (read-only)
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns

    Returns:
        column index (0-based)
    """
    board_list = list(board)
    opp = 3 - mark  # opponent mark

    # Priority 1: win if possible
    for col in legal:
        _try_move(board_list, col, mark, cols)
        if check_win(board_list, col, mark):
            _untry_move(board_list, col, cols)
            return col
        _untry_move(board_list, col, cols)

    # Priority 2: block opponent's win
    for col in legal:
        _try_move(board_list, col, opp, cols)
        if check_win(board_list, col, opp):
            _untry_move(board_list, col, cols)
            return col
        _untry_move(board_list, col, cols)

    # Priority 3: prefer center columns (left-to-right center-out)
    center = cols // 2
    ordered: list[int] = []
    for offset in range(cols):
        left = center - offset
        if left >= 0:
            ordered.append(left)
        right = center + 1 + offset
        if right < cols:
            ordered.append(right)

    for col in ordered:
        if col in legal:
            return col

    # Fallback (shouldn't happen if legal is correct)
    return legal[0]