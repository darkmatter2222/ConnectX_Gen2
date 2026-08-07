"""Bitboard AB 8x7/5 v2 - improved evaluation.

Adapted from bitboard_ab_improved_v3 (v3) for 8x7/5.
Key improvements over the original 8x7/5 eval:

- Open3 detection (3 pieces with 2+ empty = potential threat)
- Better fork scoring (+1000)
- Piece count advantage
- Column control (center columns valued more)
- Height advantage scoring
- Open2 with 2+ empty ends (more dangerous)

Board: 8 cols x 7 rows x 5-in-a-row = 56 cells.
"""

from __future__ import annotations

import time
import random
from typing import Optional, Sequence
from dataclasses import dataclass

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS as DEFAULT_ROWS, COLS as DEFAULT_COLS, INAROW as DEFAULT_INAROW,
)

# Board configuration
ROWS = 7
COLS = 8
INAROW = 5
SIZE = ROWS * COLS  # 56

# Constants
_MAX_DEPTH = 10

# Cell bit positions
_EMPTY_MASK = (1 << SIZE) - 1
_CELL_BIT = list(range(SIZE))

# Precompute all win-line bitmasks
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


# Bitboard helpers
def _to_bitboard(board: Sequence[int], mark: int) -> int:
    bb = 0
    for i, cell in enumerate(board):
        if cell == mark:
            bb |= 1 << _CELL_BIT[i]
    return bb


def _set_bits(x: int) -> list[int]:
    bits, i = [], 0
    while x:
        if x & 1:
            bits.append(i)
        x >>= 1
        i += 1
    return bits


def _row_col(bit: int, cols: int) -> tuple[int, int]:
    return bit // cols, bit % cols


# Killer moves / history table
_KILLER_TABLE: list[list[int]] = [[-1, -1] for _ in range(20)]
_HISTORY_TABLE: list[int] = [0] * (SIZE * SIZE)


def _clear_killer_history() -> None:
    for i in range(len(_KILLER_TABLE)):
        _KILLER_TABLE[i] = [-1, -1]


def _record_killer(depth: int, move: int) -> None:
    if _KILLER_TABLE[depth][0] != move:
        if _KILLER_TABLE[depth][1] != move:
            _KILLER_TABLE[depth][1] = _KILLER_TABLE[depth][0]
        _KILLER_TABLE[depth][0] = move


# Zobrist hashing
import hashlib


def _zobrist_hash(board: list[int]) -> int:
    h = 0
    for i, cell in enumerate(board):
        if cell != 0:
            key = hashlib.sha256(f"{i}_{cell}".encode()).digest()
            h ^= int.from_bytes(key[:8], 'big')
    return h


# Transposition table
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

    def get(self, hash_key: int, depth: int) -> Optional[TTEntry]:
        entry = self._table[hash_key % self._size]
        if entry is not None and entry.hash_key == hash_key:
            if entry.depth >= depth:
                return entry
        return None

    def put(self, hash_key: int, depth: int, value: float, flag: int, mark: int) -> None:
        idx = hash_key % self._size
        existing = self._table[idx]
        if existing is None or existing.depth <= depth:
            self._table[idx] = TTEntry(hash_key, depth, value, flag, mark)

    def clear(self) -> None:
        self._table = [None] * self._size


TT = TranspositionTable()


# ── Improved evaluation (v2) ────────────────────────────────────────────────────

def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """Enhanced fork-aware positional evaluation for 8x7/5."""
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0

    player_threats = opp_threats = 0
    player_block3 = opp_block3 = 0
    player_open3 = opp_open3 = 0
    player_open2 = opp_open2 = 0
    opp_open2 = 0

    player_threat_cells = [0] * SIZE
    opp_threat_cells = [0] * SIZE

    player_pieces = opp_pieces = 0

    for line_mask in _LINE_MASKS:
        player_in = player_bb & line_mask
        opp_in = opp_bb & line_mask
        empty_in = empty_bb & line_mask

        p_count = bin(player_in).count('1')
        o_count = bin(opp_in).count('1')
        e_count = bin(empty_in).count('1')

        if not p_count and not o_count:
            continue

        player_pieces += p_count
        opp_pieces += o_count

        if p_count == INAROW:
            return 100000.0
        if o_count == INAROW:
            return -100000.0

        # 4-in-a-row threats (immediate threat)
        if p_count == (INAROW - 1) and e_count >= 1:
            player_threats += 1
            for bit in _set_bits(player_in):
                player_threat_cells[bit] += 1
        elif p_count == (INAROW - 1):
            player_block3 += 1

        if o_count == (INAROW - 1) and e_count >= 1:
            opp_threats += 1
            for bit in _set_bits(opp_in):
                opp_threat_cells[bit] += 1
        elif o_count == (INAROW - 1):
            opp_block3 += 1

        # 3-in-a-row with 2+ empty = potential threat
        if p_count == 3 and e_count >= 2:
            player_open3 += 1
        if o_count == 3 and e_count >= 2:
            opp_open3 += 1

        # 2-in-a-row open (both ends open)
        if p_count == 2 and e_count >= 2:
            player_open2 += 1
        if o_count == 2 and e_count >= 2:
            opp_open2 += 1

    # Threat scoring
    score += player_threats * 5000.0 - opp_threats * 5000.0
    score += player_block3 * 300.0 - opp_block3 * 300.0
    score += player_open3 * 800.0 - opp_open3 * 800.0
    score += player_open2 * 200.0 - opp_open2 * 200.0

    # Fork detection
    for i in range(SIZE):
        if player_threat_cells[i] >= 2:
            score += 1000.0
        if opp_threat_cells[i] >= 2:
            score -= 1000.0

    # Piece count advantage
    if player_pieces > opp_pieces:
        score += (player_pieces - opp_pieces) * 10.0
    elif opp_pieces > player_pieces:
        score -= (opp_pieces - player_pieces) * 10.0

    # Column control
    player_col = [0] * COLS
    opp_col = [0] * COLS
    for bit in _set_bits(player_bb):
        _, c = _row_col(bit, cols)
        player_col[c] += 1
    for bit in _set_bits(opp_bb):
        _, c = _row_col(bit, cols)
        opp_col[c] += 1

    center_col = cols // 2
    for c in range(COLS):
        d = abs(c - center_col)
        if d == 0:
            score += (player_col[c] - opp_col[c]) * 5.0
        elif d == 1:
            score += (player_col[c] - opp_col[c]) * 2.0
        elif d == 2:
            score += (player_col[c] - opp_col[c]) * 0.5

    # Height advantage
    player_height = opp_height = 0
    for bit in _set_bits(player_bb):
        r, _ = _row_col(bit, cols)
        player_height += r
    for bit in _set_bits(opp_bb):
        r, _ = _row_col(bit, cols)
        opp_height += r
    score += (player_height - opp_height) * 0.5

    return score


# ── Threat helpers ──────────────────────────────────────────────────────────────

def _has_threat(board: list[int], last_col: int, mark: int,
                rows: int, cols: int) -> bool:
    last_row = 0
    for r in range(rows - 1, -1, -1):
        if board[r * cols + last_col] == mark:
            last_row = r
            break
    return _is_threat_at(board, last_row * cols + last_col, mark, rows, cols)


def _is_threat_at(board: list[int], idx: int, mark: int,
                  rows: int, cols: int) -> bool:
    r, c = idx // cols, idx % cols
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1
        fr, fc = r + dr, c + dc
        while (0 <= fr < rows and 0 <= fc < cols and
               board[fr * cols + fc] == mark):
            count += 1
            fr += dr
            fc += dc
        if (count >= (INAROW - 1) and 0 <= fr < rows and 0 <= fc < cols and
                board[fr * cols + fc] == 0):
            return True
    return False


# ── History score ───────────────────────────────────────────────────────────────

def _history_score(col: int, row: int) -> int:
    return row + 1


# ── Move ordering ───────────────────────────────────────────────────────────────

def _order_moves(
    board: list[int], legal: Sequence[int], mark: int,
    cols: int, tt: Optional[TranspositionTable],
    hash_key: int, depth: int,
) -> list[int]:
    """Order: killers -> wins -> blocks -> threats -> center -> history."""
    global _HISTORY_TABLE
    opp = 3 - mark

    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killers = _KILLER_TABLE[depth]
    killer_moves_list = [k for k in killers if k >= 0 and k in legal]

    hist: dict[int, int] = {}
    for col in legal:
        for r in range(ROWS - 1, -1, -1):
            if board[r * cols + col] == 0:
                hist[col] = _history_score(col, r)
                break
        else:
            hist[col] = 0

    wins, blocks, threats = [], [], []
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

        if _has_threat(board, col, mark, ROWS, cols):
            threats.append(col)

    remaining = [c for c in legal if c not in wins and c not in blocks and c not in threats]
    scored: list[tuple[int, int]] = []

    for col in wins:
        scored.append((10000, col))
    for col in blocks:
        scored.append((5000, col))
    for col in threats:
        scored.append((2000, col))
    for col in killer_moves_list:
        if col not in wins and col not in blocks and col not in threats:
            scored.append((3000, col))
    for col in remaining:
        h = hist.get(col, 0)
        center = cols // 2
        center_score = max(0, 10 - abs(col - center))
        scored.append((h + center_score, col))

    scored.sort(key=lambda x: -x[0])
    return [col for _, col in scored]


# ── Negamax ─────────────────────────────────────────────────────────────────────

def _negamax(
    board: list[int], mark: int, depth: int,
    alpha: float, beta: float,
    cols: int = COLS,
    tt: Optional[TranspositionTable] = None,
    time_limit: Optional[float] = None,
    counter: Optional[list[int]] = None,
    start_time: Optional[float] = None,
    is_root: bool = False,
) -> tuple[float, int]:
    """Negamax with alpha-beta, TT, killer moves, history heuristic."""
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

    # Immediate win check
    for col in legal:
        row = drop(board, col, mark, ROWS, cols)
        w = check_win(board, col, mark, ROWS, cols)
        if w:
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

    best_score = float("-inf")
    best_col = legal[0]

    # Check if opponent already has a winning line
    opp = 3 - mark
    opp_bb = _to_bitboard(board, opp)
    if opp_bb:
        for line_mask in _LINE_MASKS:
            if bin(opp_bb & line_mask).count('1') == INAROW:
                return -100000.0, legal[0]

    # Null-move pruning
    null_ok = True
    if depth >= 3 and len(legal) > 1:
        try:
            opp = 3 - mark
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
            if not null_ok:
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


# ── Iterative deepening ─────────────────────────────────────────────────────────

def _iterative_deepening(
    board: list[int], mark: int, cols: int,
    time_limit: Optional[float],
    min_depth: int, max_depth: int,
) -> int:
    """Iterative deepening: search depth min_depth..max_depth."""
    global _HISTORY_TABLE
    _clear_killer_history()
    _HISTORY_TABLE = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0
    counter = [0]

    for depth in range(min_depth, max_depth + 1):
        if time_limit is not None:
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

        if time.time() - start_time >= time_limit:
            break

        best_col = col

    return best_col


# ── Public API ──────────────────────────────────────────────────────────────────

def bitboard_ab_bot_8x7_5_v2(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Full-depth 8x7/5 AB with improved evaluation (v2)."""
    board_list = list(board)
    legal_list = list(legal) if legal else []
    if not legal_list:
        legal_list = list(
            i for i in range(cols) if board_list[i * ROWS + ROWS - 1] == 0
        )
    if not legal_list:
        return 0

    time_limit = move_deadline if move_deadline is not None else 2.0

    pieces = sum(1 for x in board_list if x != 0)
    if pieces == 0:
        return cols // 2

    return _iterative_deepening(
        board_list, mark, cols, time_limit, min_depth=4, max_depth=10,
    )


def bitboard_ab_bot_fast_8x7_5_v2(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast 8x7/5 AB with improved evaluation (v2)."""
    board_list = list(board)
    legal_list = list(legal) if legal else []
    if not legal_list:
        legal_list = list(
            i for i in range(cols) if board_list[i * ROWS + ROWS - 1] == 0
        )
    if not legal_list:
        return 0

    time_limit = move_deadline if move_deadline is not None else 2.0

    pieces = sum(1 for x in board_list if x != 0)
    if pieces == 0:
        return cols // 2

    return _iterative_deepening(
        board_list, mark, cols, time_limit, min_depth=4, max_depth=8,
    )