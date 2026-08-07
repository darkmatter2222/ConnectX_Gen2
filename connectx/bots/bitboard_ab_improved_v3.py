"""
Bitboard Alpha-Beta Bot — v3 (Improved Evaluation).

Enhanced over v2 with:
  * Better threat evaluation (open/threat scoring per-line)
  * Piece count advantage (more pieces = more win opportunities)
  * Improved column control (columns 2-5 preferred, edges penalized)
  * Better fork detection (multi-threat positions)
  * Edge column awareness

v2 was: iterative deepening, killer moves, history, null-move + safety fix.
v3 is v2 with improved evaluation function.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Sequence

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW, SIZE,
)

# ── Constants ──────────────────────────────────────────────────────────────────

_MAX_DEPTH: int = 18
_EMPTY_MASK: int = (1 << SIZE) - 1

_CELL_BIT: list[int] = [r * COLS + c for r in range(ROWS) for c in range(COLS)]

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


# ── Transposition table ────────────────────────────────────────────────────────

@dataclass
class TTEntry:
    hash_key: int
    depth: int
    value: float
    flag: int  # 0=exact  1=lower  2=upper


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

    def put(self, key: int, depth: int, value: float, flag: int) -> None:
        self._table[key & (self._size - 1)] = TTEntry(
            hash_key=key, depth=depth, value=value, flag=flag
        )

    def clear(self) -> None:
        self._table = [None] * self._size


TT = TranspositionTable(1 << 19)


# ── Zobrist hashing ────────────────────────────────────────────────────────────

_ZOBRIST: list[list[int]] = []


def _init_zobrist() -> None:
    import random
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


# ── v3 Evaluation — improved over v2 ──────────────────────────────────────────

def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """
    Fork-aware positional evaluation (v3).

    Improvements over v2:
    - Better threat evaluation (open2 scoring)
    - Piece count advantage
    - Column control (columns 2-5 valued, edges penalized)
    - More accurate fork detection
    - Blocked threat penalty
    """
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0
    center_col = cols // 2

    # Track threats per cell for fork detection
    player_threat_cells = [0] * SIZE
    opp_threat_cells = [0] * SIZE

    player_threats = opp_threats = 0
    player_block3 = opp_block3 = 0
    player_open2 = opp_open2 = 0
    player_open3 = opp_open3 = 0

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

        # Count pieces
        player_pieces += p_count
        opp_pieces += o_count

        # Terminal check
        if p_count == INAROW:
            return 100000.0
        if o_count == INAROW:
            return -100000.0

        # 3-in-a-row threats
        if p_count == 3:
            if e_count >= 1:
                player_threats += 1
                player_open3 += 1
                for bit in _set_bits(player_in):
                    player_threat_cells[bit] += 1
            else:
                player_block3 += 1  # blocked threat (less valuable)

        if o_count == 3:
            if e_count >= 1:
                opp_threats += 1
                opp_open3 += 1
                for bit in _set_bits(opp_in):
                    opp_threat_cells[bit] += 1
            else:
                opp_block3 += 1

        # 2-in-a-row open (two open ends = more dangerous)
        if p_count == 2 and e_count >= 2:
            player_open2 += 1
        if o_count == 2 and e_count >= 2:
            opp_open2 += 1

    # ── Threat scoring ──
    # Open3 threats are critical — worth much more than open2
    score += player_open3 * 2000.0 - opp_open3 * 2000.0
    # Open2 threats are moderately valuable
    score += player_open2 * 100.0 - opp_open2 * 100.0
    # General threats (any 3-in-a-row)
    score += player_threats * 600.0 - opp_threats * 600.0
    # Blocked threats (less dangerous but still positional)
    score += player_block3 * 150.0 - opp_block3 * 150.0

    # ── Fork detection ──
    # A cell with two opponent threats = fork
    for i in range(SIZE):
        if player_threat_cells[i] >= 2:
            score += 200.0
        if opp_threat_cells[i] >= 2:
            score -= 200.0

    # ── Piece count advantage ──
    # More pieces = more opportunities to create threats
    if player_pieces > opp_pieces:
        score += (player_pieces - opp_pieces) * 5.0
    elif opp_pieces > player_pieces:
        score -= (opp_pieces - player_pieces) * 5.0

    # ── Column control ──
    player_col = [0] * COLS
    opp_col = [0] * COLS
    for bit in _set_bits(player_bb):
        _, c = _row_col(bit, cols)
        player_col[c] += 1
    for bit in _set_bits(opp_bb):
        _, c = _row_col(bit, cols)
        opp_col[c] += 1

    for c in range(COLS):
        # Columns 2-5 (the "core" columns) are most valuable
        if c in (2, 3, 4):
            score += (player_col[c] - opp_col[c]) * 3.0
        elif c in (1, 5):
            score += (player_col[c] - opp_col[c]) * 1.5
        else:
            # Edge columns (0, 6) are least valuable
            score += (player_col[c] - opp_col[c]) * 0.5

    # ── Height advantage ──
    # Higher pieces in columns = more threat creation potential
    player_height = opp_height = 0
    for bit in _set_bits(player_bb):
        r, _ = _row_col(bit, cols)
        player_height += r
    for bit in _set_bits(opp_bb):
        r, _ = _row_col(bit, cols)
        opp_height += r
    score += (player_height - opp_height) * 0.3

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
        if (count >= 3 and 0 <= fr < rows and 0 <= fc < cols and
                board[fr * cols + fc] == 0):
            return True
        br, bc = r - dr, c - dc
        while (0 <= br < rows and 0 <= bc < cols and
                board[br * cols + bc] == mark):
            count += 1
            br -= br
            bc -= bc
        if (count >= 3 and 0 <= br < rows and 0 <= bc < cols and
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
        drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            wins.append(col)
            un_drop(board, col, ROWS, cols)
            continue
        un_drop(board, col, ROWS, cols)

        drop(board, col, opp, ROWS, cols)
        if check_win(board, col, opp, ROWS, cols):
            blocks.append(col)
            un_drop(board, col, ROWS, cols)
            continue
        un_drop(board, col, ROWS, cols)

        try:
            drop(board, col, mark, ROWS, cols)
            if _has_threat(board, col, mark, ROWS, cols):
                threats.append(col)
            un_drop(board, col, ROWS, cols)
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
        drop(board, col, mark, ROWS, cols)
        w = check_win(board, col, mark, ROWS, cols)
        if w:
            un_drop(board, col, ROWS, cols)
            if tt is not None:
                tt.put(hash_key, depth, 100000.0, 0)
            return 100000.0, col
        un_drop(board, col, ROWS, cols)

    # TT lookup — skip at root (iterative deepening manages TT at root)
    tt_entry = None
    if tt is not None and not is_root:
        tt_entry = tt.get(hash_key, depth)

    if tt_entry is not None:
        val = tt_entry.value
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

    # Null-move pruning — only when no immediate tactical moves exist
    null_ok = True
    if depth >= 3 and len(legal) > 1:
        try:
            opp = 3 - mark
            for col in legal:
                try:
                    drop(board, col, opp, ROWS, cols)
                    if check_win(board, col, opp, ROWS, cols):
                        null_ok = False
                        un_drop(board, col, ROWS, cols)
                        break
                except (ValueError, IndexError):
                    pass
                else:
                    try:
                        un_drop(board, col, ROWS, cols)
                    except (ValueError, IndexError):
                        pass
            if not null_ok:
                pass
        except (ValueError, IndexError):
            null_ok = False

    if null_ok:
        null_board = list(board)
        score = -_negamax(
            null_board, mark, depth - 3,
            -beta, -beta + 1,
            cols, tt, time_limit, counter, start_time,
        )[0]
        if score >= beta:
            return beta, legal[0]

    ordered = _order_moves(board, legal, mark, cols, tt, hash_key, depth)

    for col in ordered:
        try:
            drop(board, col, mark, ROWS, cols)
        except ValueError:
            continue
        score, _ = _negamax(
            board, 3 - mark, depth - 1,
            -beta, -alpha,
            cols, tt, time_limit, counter, start_time,
        )
        score = -score
        try:
            un_drop(board, col, ROWS, cols)
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
                tt.put(hash_key, depth, beta, 2)
            break

    if tt is not None:
        flag = 2 if best_score >= beta else (1 if best_score <= alpha else 0)
        tt.put(hash_key, depth, best_score, flag)

    return best_score, best_col


# ── Iterative deepening ────────────────────────────────────────────────────────

def _iterative_deepening(
    board: list[int], mark: int, cols: int,
    time_limit: Optional[float],
    min_depth: int, max_depth: int,
) -> int:
    """
    Iterative deepening: search depth min_depth..max_depth.
    TT is reused across depths for better pruning.
    Root-level search skips TT (is_root=True) to avoid stale entries.
    """
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


# ── Depth selector ─────────────────────────────────────────────────────────────

def _select_depth(time_limit: Optional[float]) -> tuple[int, int]:
    """Return (min_depth, max_depth) for iterative deepening."""
    if time_limit is not None:
        if time_limit > 1.0:
            return 3, 14
        elif time_limit > 0.5:
            return 3, 11
        elif time_limit > 0.2:
            return 3, 10
        elif time_limit > 0.1:
            return 2, 9
        else:
            return 2, 7
    return 3, 14


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_bot_v3(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Bitboard alpha-beta v3 — improved evaluation + iterative deepening."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline

    min_d, max_d = _select_depth(time_limit)
    col = _iterative_deepening(
        board_list, mark, cols, time_limit, min_d, max_d,
    )
    if col in legal:
        return col
    return legal[0]


def bitboard_ab_bot_fast_v3(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast v3 — iterative deepening to depth 8, improved eval."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline

    col = _iterative_deepening(
        board_list, mark, cols, time_limit, 1, 8,
    )
    if col in legal:
        return col
    return legal[0]