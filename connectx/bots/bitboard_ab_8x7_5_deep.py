"""
Bitboard Alpha-Beta Bot — 8×7/5 Deep variant.

A deeper-search variant of bitboard_ab_8x7_5 with simpler evaluation
to maximize search depth within time limits.

Strategy: shallower eval, deeper search. Compensates for less positional
understanding by searching further ahead.
"""

from __future__ import annotations

import time
import random
from dataclasses import dataclass
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
)

# ── Board configuration ─────────────────────────────────────────────────────────

ROWS: int = 7
COLS: int = 8
INAROW: int = 5
SIZE: int = ROWS * COLS  # 56

# ── Constants ────────────────────────────────────────────────────────────────────

_EMPTY_MASK: int = (1 << SIZE) - 1
_CELL_BIT: list[int] = list(range(SIZE))
_LINE_MASKS: list[int] = []


def _init_lines() -> None:
    for r in range(ROWS):
        for c in range(COLS):
            if c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[r * COLS + c + k]
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c]
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS and c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c + k]
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS and c + 1 >= INAROW:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c - k]
                _LINE_MASKS.append(mask)


_init_lines()


# ── Transposition table ──────────────────────────────────────────────────────────

@dataclass
class TTEntry:
    hash_key: int
    depth: int
    value: float
    flag: int
    mark: int


class TranspositionTable:
    def __init__(self, size: int = 1 << 19) -> None:
        self._size = size
        self._table: list[Optional[TTEntry]] = [None] * size

    def get(self, key: int, depth: int) -> Optional[TTEntry]:
        entry = self._table[key & (self._size - 1)]
        if entry is not None and entry.hash_key == key and entry.depth >= depth:
            return entry
        return None

    def put(self, key: int, depth: int, value: float, flag: int, mark: int) -> None:
        self._table[key & (self._size - 1)] = TTEntry(
            hash_key=key, depth=depth, value=value, flag=flag, mark=mark
        )

    def clear(self) -> None:
        self._table = [None] * self._size


TT = TranspositionTable(1 << 19)


# ── Zobrist hashing ────────────────────────────────────────────────────────────

_ZOBRIST: list[list[int]] = []


def _init_zobrist() -> None:
    rng = random.Random(42)
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])


_init_zobrist()


def _zobrist_hash(board: Sequence[int]) -> int:
    h = 0
    for i, cell in enumerate(board):
        if cell != 0:
            h ^= _ZOBRIST[cell - 1][i]
    return h


# ── Killer moves & history ────────────────────────────────────────────────────

_KILLER_TABLE: list[list[int]] = [[-1, -1] for _ in range(64)]
_HISTORY_TABLE: list[int] = [0] * (SIZE * 4)


def _update_history(col: int, row: int, bonus: int) -> None:
    idx = row * COLS + col
    if 0 <= idx < len(_HISTORY_TABLE):
        _HISTORY_TABLE[idx] += bonus


def _record_killer(depth: int, move: int) -> None:
    if _KILLER_TABLE[depth][0] != move:
        _KILLER_TABLE[depth][1] = _KILLER_TABLE[depth][0]
        _KILLER_TABLE[depth][0] = move


def _clear_killer_history() -> None:
    for i in range(len(_KILLER_TABLE)):
        _KILLER_TABLE[i] = [-1, -1]


# ── Evaluation — SIMPLIFIED ───────────────────────────────────────────────────

def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """Minimal evaluation: center control + piece count.

    Much cheaper than the full v2 evaluation, allowing deeper search.
    """
    opp = 3 - mark
    center_col = cols // 2
    score = 0.0
    piece_count = 0

    for i in range(SIZE):
        cell = board[i]
        if cell == 0:
            continue
        piece_count += 1
        r, c = i // cols, i % cols

        if cell == mark:
            # Center bonus
            if c == center_col:
                score += 0.5
            elif abs(c - center_col) <= 1:
                score += 0.25
            # Height bonus (more advanced = better)
            score += r * 0.1
        else:
            if c == center_col:
                score -= 0.5
            elif abs(c - center_col) <= 1:
                score -= 0.25
            score -= r * 0.1

    # Slight advantage for moving first (if board is nearly full, less advantage)
    if piece_count < 10:
        score += 0.5

    return score


# ── Threat check (quick version) ───────────────────────────────────────────────

def _has_threat(board: list[int], col: int, mark: int,
                rows: int, cols: int) -> bool:
    """Quick threat check: does this move create a 3-in-a-row with an open end?"""
    last_row = 0
    for r in range(rows - 1, -1, -1):
        if board[r * cols + col] == mark:
            last_row = r
            break

    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1
        fr, fc = last_row + dr, col + dc
        while (0 <= fr < rows and 0 <= fc < cols and
               board[fr * cols + fc] == mark):
            count += 1
            fr += dr
            fc += dc
        if count >= 3 and 0 <= fr < rows and 0 <= fc < cols and board[fr * cols + fc] == 0:
            return True
        br, bc = last_row - dr, col - dc
        while (0 <= br < rows and 0 <= bc < cols and
               board[br * cols + bc] == mark):
            count += 1
            br -= dr
            bc -= dc
        if count >= 3 and 0 <= br < rows and 0 <= bc < cols and board[br * cols + bc] == 0:
            return True
    return False


# ── Move ordering (simplified) ─────────────────────────────────────────────────

def _order_moves(
    board: list[int], legal: Sequence[int], mark: int,
    cols: int, tt, hash_key: int, depth: int,
) -> list[int]:
    """Simplified ordering: killers -> wins -> blocks -> center -> others."""
    opp = 3 - mark

    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killers = _KILLER_TABLE[depth]
    killer_moves = [k for k in killers if k >= 0 and k in legal]

    wins, blocks = [], []
    for col in legal:
        row = drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            wins.append(col)
            un_drop(board, col, ROWS, cols, row=row)
            continue
        un_drop(board, col, ROWS, cols, row=row)

        row = drop(board, col, opp, ROWS, cols)
        if check_win(board, col, opp, ROWS, cols):
            blocks.append(col)
            un_drop(board, col, ROWS, cols, row=row)
            continue
        un_drop(board, col, ROWS, cols, row=row)

    center = cols // 2
    others = sorted(
        [c for c in legal if c not in wins and c not in blocks],
        key=lambda c: abs(c - center),
    )

    seen = set()
    result = []
    for group in [killer_moves, wins, blocks, others]:
        for col in group:
            if col not in seen:
                result.append(col)
                seen.add(col)
    return result


# ── Negamax ─────────────────────────────────────────────────────────────────────

def _negamax(
    board: list[int], mark: int, depth: int,
    alpha: float, beta: float,
    cols: int = COLS,
    tt = None,
    time_limit: Optional[float] = None,
    counter: Optional[list[int]] = None,
    start_time: Optional[float] = None,
    is_root: bool = False,
) -> tuple[float, int]:
    """Simplified negamax — faster evaluation for deeper search."""
    alpha = max(alpha, -100000.0)
    beta = min(beta, 100000.0)

    legal = valid_moves(board, cols)
    if not legal:
        return 0.0, 0

    if time_limit is not None and start_time is not None:
        if time.time() - start_time >= time_limit:
            return _evaluate(board, mark, cols), legal[0]

    if counter is not None:
        counter[0] += 1

    hash_key = _zobrist_hash(board)

    # Check immediate win
    for col in legal:
        row = drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols, row=row)
            if tt is not None:
                tt.put(hash_key, depth, 100000.0, 0, mark)
            return 100000.0, col
        un_drop(board, col, ROWS, cols, row=row)

    # TT lookup
    tt_entry = None
    if tt is not None and not is_root:
        tt_entry = tt.get(hash_key, depth)

    if tt_entry is not None:
        val = -tt_entry.value if tt_entry.mark != mark else tt_entry.value
        if tt_entry.flag == 0:
            return val, legal[0]
        if tt_entry.flag == 1 and val >= beta:
            return val, legal[0]
        if tt_entry.flag == 2 and val <= alpha:
            return val, legal[0]

    if depth <= 0:
        return _evaluate(board, mark, cols), legal[0]

    # Check opponent win
    opp = 3 - mark
    opp_bb = 0
    for i, cell in enumerate(board):
        if cell == opp:
            opp_bb |= 1 << i

    if opp_bb:
        for line_mask in _LINE_MASKS:
            if bin(opp_bb & line_mask).count('1') == INAROW:
                return -100000.0, legal[0]

    # Null-move pruning
    null_ok = True
    if depth >= 3 and len(legal) > 1:
        try:
            for col in legal:
                try:
                    opp_row = drop(board, col, opp, ROWS, cols)
                    if check_win(board, col, opp, ROWS, cols):
                        null_ok = False
                        un_drop(board, col, ROWS, cols, row=opp_row)
                        break
                except (ValueError, IndexError):
                    pass
                else:
                    try:
                        un_drop(board, col, ROWS, cols, row=opp_row)
                    except (ValueError, IndexError):
                        pass
        except (ValueError, IndexError):
            null_ok = False

    if null_ok:
        null_board = list(board)
        score = -_negamax(
            null_board, 3 - mark, depth - 3,
            -beta, -beta + 1,
            cols, tt, time_limit, counter, start_time,
            is_root=True,
        )[0]
        if score >= beta:
            return beta, legal[0]

    ordered = _order_moves(board, legal, mark, cols, tt, hash_key, depth)

    best_score = float("-inf")
    best_col = legal[0]

    for col in ordered:
        try:
            drop_row = drop(board, col, mark, ROWS, cols)
        except ValueError:
            continue

        score, _ = _negamax(
            board, 3 - mark, depth - 1,
            -beta, -alpha,
            cols, tt, time_limit, counter, start_time,
        )
        score = -score

        try:
            un_drop(board, col, ROWS, cols, row=drop_row)
        except ValueError:
            pass

        if score > best_score:
            best_score = score
            best_col = col

        if score > alpha:
            alpha = score

        if alpha >= beta:
            _record_killer(depth, col)
            if tt is not None:
                tt.put(hash_key, depth, beta, 2, mark)
            break

    if tt is not None:
        flag = 2 if best_score >= beta else (1 if best_score <= alpha else 0)
        tt.put(hash_key, depth, best_score, flag, mark)

    return best_score, best_col


# ── Iterative deepening ────────────────────────────────────────────────────────

def _iterative_deepening(
    board: list[int], mark: int, cols: int,
    time_limit: Optional[float],
    min_depth: int, max_depth: int,
) -> int:
    global _HISTORY_TABLE
    _clear_killer_history()
    _HISTORY_TABLE = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0
    counter = [0]

    for depth in range(min_depth, max_depth + 1):
        if time_limit is not None and start_time is not None:
            elapsed = time.time() - start_time
            if elapsed >= time_limit * 0.95:
                break

        legal = valid_moves(board, cols)
        if not legal:
            return 0

        board_copy = list(board)
        _, col = _negamax(
            board_copy, mark, depth,
            float("-inf"), float("inf"),
            cols, TT, time_limit, counter, start_time,
            is_root=True,
        )

        if col not in legal:
            col = legal[0]
        best_col = col

        for r in range(ROWS - 1, -1, -1):
            if board_copy[r * cols + best_col] == mark:
                _update_history(best_col, r, depth * 100)
                break

        if time_limit is not None and start_time is not None:
            if time.time() - start_time >= time_limit:
                break

    return best_col


# ── Depth selector — DEEPER variant ────────────────────────────────────────────

def _select_depth(time_limit: Optional[float]) -> tuple[int, int]:
    """Deeper search — simpler eval means we can search further."""
    if time_limit is not None:
        if time_limit > 2.0:
            return 4, 10
        elif time_limit > 1.0:
            return 3, 10
        elif time_limit > 0.5:
            return 3, 8
        elif time_limit > 0.2:
            return 2, 7
        elif time_limit > 0.1:
            return 2, 6
        else:
            return 1, 5
    return 4, 10


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_bot_8x7_5_deep(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Deep variant — simpler evaluation, deeper search."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = move_deadline
    min_d, max_d = _select_depth(time_limit)
    col = _iterative_deepening(
        board_list, mark, cols, time_limit, min_d, max_d,
    )
    if col in legal:
        return col
    return legal[0]


def bitboard_ab_bot_8x7_5_fast_deep(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast deep — depth 8 max."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    col = _iterative_deepening(board_list, mark, cols, None, 1, 8)
    if col in legal:
        return col
    return legal[0]