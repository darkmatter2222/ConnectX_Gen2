"""
Bitboard Alpha-Beta Bot — 8×7/5 variant.

Adapted from bitboard_ab_improved (v2) for 8 columns × 7 rows × 5-in-a-row.
Board size: 56 cells → bitboards use 56 bits.

Unlike 7×6/4 (which is solved in ~20ms), 8×7/5 is not solved.
This bot is designed for the 8×7/5 target where deeper search
may not be sufficient, opening room for neural and MCTS enhancements.
"""

from __future__ import annotations

import time
import random
from dataclasses import dataclass
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS as DEFAULT_ROWS, COLS as DEFAULT_COLS, INAROW as DEFAULT_INAROW,
)

# ── Board configuration ──────────────────────────────────────────────────────────

ROWS: int = 7          # 7 rows (height)
COLS: int = 8          # 8 columns (width)
INAROW: int = 5        # 5 in a row to win
SIZE: int = ROWS * COLS  # 56

# ── Constants ────────────────────────────────────────────────────────────────────

_MAX_DEPTH: int = 10   # Max iterative-deepening depth for 8×7/5

_EMPTY_MASK: int = (1 << SIZE) - 1

# Cell bit positions: flat index i → bit position i (identity mapping)
_CELL_BIT: list[int] = list(range(SIZE))

# Precompute all win-line bitmasks (horizontal, vertical, two diagonals)
_LINE_MASKS: list[int] = []


def _init_lines() -> None:
    for r in range(ROWS):
        for c in range(COLS):
            # Horizontal
            if c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[r * COLS + c + k]
                _LINE_MASKS.append(mask)
            # Vertical
            if r + INAROW <= ROWS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c]
                _LINE_MASKS.append(mask)
            # Diagonal down-right
            if r + INAROW <= ROWS and c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c + k]
                _LINE_MASKS.append(mask)
            # Diagonal down-left
            if r + INAROW <= ROWS and c + 1 >= INAROW:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << _CELL_BIT[(r + k) * COLS + c - k]
                _LINE_MASKS.append(mask)


_init_lines()

# Number of win-lines for 8×7/5: horizontal + vertical + 2*diagonal
# horizontal: 7 rows × (8-5+1) = 7×4 = 28
# vertical:   8 cols × (7-5+1) = 8×3 = 24
# diag-downR: (7-5+1) × (8-5+1) = 3×4 = 12
# diag-downL: (7-5+1) × (8-1+1) − 3×4 = 3×4 = 12  (adjusted for boundaries)
# Total ≈ 76 lines (computed at module load time)


# ── Transposition table ──────────────────────────────────────────────────────────

@dataclass
class TTEntry:
    hash_key: int
    depth: int
    value: float
    flag: int  # 0=exact  1=lower  2=upper
    mark: int  # which player's perspective the value is stored under


class TranspositionTable:
    """Hash-table-backed transposition table."""

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


def _history_score(col: int, row: int) -> int:
    idx = row * COLS + col
    if 0 <= idx < len(_HISTORY_TABLE):
        return _HISTORY_TABLE[idx]
    return 0


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


# ── Bitboard helpers ───────────────────────────────────────────────────────────

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


# ── Evaluation ─────────────────────────────────────────────────────────────────

def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """Fork-aware positional evaluation for 8×7/5."""
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0
    center_col = cols // 2  # col 4 for 8 cols
    player_threats = opp_threats = 0
    player_block3 = opp_block3 = 0
    player_open2 = opp_open2 = 0
    player_threat_cells = [0] * SIZE
    opp_threat_cells = [0] * SIZE

    for line_mask in _LINE_MASKS:
        player_in = player_bb & line_mask
        opp_in = opp_bb & line_mask
        empty_in = empty_bb & line_mask
        if not player_in and not opp_in:
            continue

        p_count = bin(player_in).count('1')
        o_count = bin(opp_in).count('1')
        e_count = bin(empty_in).count('1')

        if p_count == INAROW:
            return 100000.0
        if o_count == INAROW:
            return -100000.0

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

        if p_count == 2 and e_count >= (INAROW - 2):
            player_open2 += 1
        if o_count == 2 and e_count >= (INAROW - 2):
            opp_open2 += 1

    score += player_threats * 800.0 - opp_threats * 800.0
    score += player_block3 * 200.0 - opp_block3 * 200.0

    max_p = max_o = 0
    for i in range(SIZE):
        if player_threat_cells[i] > max_p:
            max_p = player_threat_cells[i]
        if opp_threat_cells[i] > max_o:
            max_o = opp_threat_cells[i]
    if max_p >= 2:
        score += 200.0  # boosted for 5-in-a-row (harder to create forks)
    if max_o >= 2:
        score -= 200.0

    score += player_open2 * 30.0 - opp_open2 * 30.0

    for bit in _set_bits(player_bb):
        r, c = _row_col(bit, cols)
        if c == center_col:
            score += 1.0
        elif abs(c - center_col) <= 1:
            score += 0.5

    return score


# ── Threat check (used during move ordering) ───────────────────────────────────

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
        br, bc = r - dr, c - dc
        while (0 <= br < rows and 0 <= bc < cols and
               board[br * cols + bc] == mark):
            count += 1
            br -= dr
            bc -= dc
        if (count >= (INAROW - 1) and 0 <= br < rows and 0 <= bc < cols and
                board[br * cols + bc] == 0):
            return True
    return False


# ── Move ordering ──────────────────────────────────────────────────────────────

def _order_moves(
    board: list[int], legal: Sequence[int], mark: int,
    cols: int, tt: Optional[TranspositionTable],
    hash_key: int, depth: int,
) -> list[int]:
    """Order: killers -> wins -> blocks -> threats -> center -> history."""
    opp = 3 - mark

    # Recompute legal from current board (defensive)
    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killers = _KILLER_TABLE[depth]
    killer_moves = [k for k in killers if k >= 0 and k in legal]

    # History scores
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

        try:
            row = drop(board, col, mark, ROWS, cols)
            if _has_threat(board, col, mark, ROWS, cols):
                threats.append(col)
            un_drop(board, col, ROWS, cols, row=row)
        except ValueError:
            pass

    center = cols // 2
    others = sorted(
        [c for c in legal
         if c not in wins and c not in blocks and c not in threats],
        key=lambda c: abs(c - center),
    )

    seen = set()
    result = []
    for group in [killer_moves, wins, blocks, threats, others]:
        for col in group:
            if col not in seen:
                result.append(col)
                seen.add(col)
    for col in sorted(legal, key=lambda c: hist.get(c, 0), reverse=True):
        if col not in seen:
            result.append(col)
            seen.add(col)
    return result


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
    """
    Negamax with alpha-beta, TT, killer moves, history heuristic.

    is_root=True: skip TT lookup (used by iterative deepening at the root).
    """
    # Cap infinite bounds to prevent propagation issues.
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

    # Check immediate win — always first
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

    # Check if opponent already has a winning line on the board
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


# ── Iterative deepening ────────────────────────────────────────────────────────

def _iterative_deepening(
    board: list[int], mark: int, cols: int,
    time_limit: Optional[float],
    min_depth: int, max_depth: int,
) -> int:
    """
    Iterative deepening: search depth min_depth..max_depth.
    Returns the best_col from the deepest completed depth.
    """
    global _HISTORY_TABLE
    _clear_killer_history()
    _HISTORY_TABLE = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0  # center column
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


# ── Depth selector ─────────────────────────────────────────────────────────────

def _select_depth(time_limit: Optional[float]) -> tuple[int, int]:
    """Return (min_depth, max_depth) for iterative deepening.

    Adjusted for 8×7/5: the game is NOT solved at this board size,
    so the search tree grows rapidly. Max depth 8 is safe for the
    first move; deeper depths are used only when time permits and
    the board is more filled (lower branching factor).
    """
    if time_limit is not None:
        if time_limit > 2.0:
            return 4, 8
        elif time_limit > 1.0:
            return 3, 8
        elif time_limit > 0.5:
            return 3, 7
        elif time_limit > 0.2:
            return 2, 6
        elif time_limit > 0.1:
            return 2, 5
        else:
            return 1, 4
    return 3, 8


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_bot_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Bitboard alpha-beta for 8×7/5 — iterative deepening + killer + history."""
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


def bitboard_ab_bot_fast_8x7_5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast 8×7/5 — iterative deepening to depth 10."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = move_deadline
    col = _iterative_deepening(board_list, mark, cols, time_limit, 1, 10)
    if col in legal:
        return col
    return legal[0]