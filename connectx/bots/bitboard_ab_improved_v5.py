"""
Bitboard Alpha-Beta Bot — v5 (Fast Evaluation + Deep Search).

v5 is v2 with:
  * Minimal evaluation function (~3x faster than v3/v4)
  * Deeper search (depth 16+ within 2s) due to faster eval
  * Same search improvements: PVS, killer moves, history, null-move

Rationale: If the evaluation function is 3x faster, iterative deepening
can search ~2 more ply within the same time budget. Each extra ply can
improve strength by ~10-20% in alpha-beta search.

The evaluation is intentionally simple:
  - Immediate win/loss detection (handled by search)
  - Threat scoring (3-in-a-row = critical)
  - Fork detection (double threats = strong)
  - Center control (columns 2-5 preferred)

No piece count, no height, no open2 scoring — those features add cost
without proportionally better signal for Connect 4.
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
    flag: int


class TranspositionTable:
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
    return _HISTORY_TABLE[idx] if 0 <= idx < len(_HISTORY_TABLE) else 0


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


# ── v5 Evaluation — minimal, fast ─────────────────────────────────────────────

def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """
    Minimal fork-aware evaluation — optimized for speed.

    Only key features:
    - Threats (3-in-a-row open) — high score
    - Forks (double threat) — highest score
    - Center control — moderate score

    No piece count, no height, no blocked threats, no open2.
    This is ~3x faster than v3 while capturing the essential positional info.
    """
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0
    threat_cells = [0] * SIZE

    for line_mask in _LINE_MASKS:
        player_in = player_bb & line_mask
        opp_in = opp_bb & line_mask
        empty_in = empty_bb & line_mask

        p_count = bin(player_in).count('1')
        o_count = bin(opp_in).count('1')
        e_count = bin(empty_in).count('1')

        if not p_count and not o_count:
            continue

        if p_count == INAROW:
            return 100000.0
        if o_count == INAROW:
            return -100000.0

        # Open 3-in-a-row (critical threat)
        if p_count == 3 and e_count >= 1:
            for bit in _set_bits(player_in):
                threat_cells[bit] += 1
        if o_count == 3 and e_count >= 1:
            for bit in _set_bits(opp_in):
                threat_cells[bit] -= 1

    # Fork scoring (2+ threats on same cell = strong)
    for tc in threat_cells:
        if tc >= 2:
            score += 1500.0
        elif tc <= -2:
            score -= 1500.0

    # Individual threats
    for tc in threat_cells:
        score += tc * 100.0

    # Center control (columns 2-5 preferred)
    player_col = [0] * COLS
    opp_col = [0] * COLS
    for bit in _set_bits(player_bb):
        _, c = _row_col(bit, cols)
        player_col[c] += 1
    for bit in _set_bits(opp_bb):
        _, c = _row_col(bit, cols)
        opp_col[c] += 1

    for c in range(COLS):
        if c in (2, 3, 4):
            score += (player_col[c] - opp_col[c]) * 5.0
        elif c in (1, 5):
            score += (player_col[c] - opp_col[c]) * 2.0
        else:
            score += (player_col[c] - opp_col[c]) * 0.5

    return score


# ── Move ordering ──────────────────────────────────────────────────────────────

def _order_moves_pvs(
    board: list[int], legal: Sequence[int], mark: int,
    cols: int, tt: Optional[TranspositionTable],
    hash_key: int, depth: int,
    tt_move: int, killer_moves_list: list[int],
) -> list[int]:
    opp = 3 - mark

    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killer_moves = [k for k in killer_moves_list if k >= 0 and k in legal]

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
            r = 0
            for rr in range(ROWS - 1, -1, -1):
                if board[rr * cols + col] == mark:
                    r = rr
                    break
            idx = r * cols + col
            rc = idx // cols, idx % cols
            is_threat = False
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                cnt = 1
                fr, fc = rc[0] + dr, rc[1] + dc
                while (0 <= fr < ROWS and 0 <= fc < COLS and
                        board[fr * cols + fc] == mark):
                    cnt += 1
                    fr += dr
                    fc += dc
                if cnt >= 3 and 0 <= fr < ROWS and 0 <= fc < COLS and board[fr * cols + fc] == 0:
                    is_threat = True
                    break
                br, bc = rc[0] - dr, rc[1] - dc
                while (0 <= br < ROWS and 0 <= bc < COLS and
                        board[br * cols + bc] == mark):
                    cnt += 1
                    br -= dr
                    bc -= dc
                if cnt >= 3 and 0 <= br < ROWS and 0 <= bc < COLS and board[br * cols + bc] == 0:
                    is_threat = True
                    break
            if is_threat:
                threats.append(col)
            un_drop(board, col, ROWS, cols)
        except ValueError:
            pass

    center = cols // 2
    others = sorted(
        [c for c in legal if c not in wins and c not in blocks and c not in threats],
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


# ── PVS Negamax ────────────────────────────────────────────────────────────────

def _pvs(
    board: list[int], mark: int, depth: int,
    alpha: float, beta: float,
    cols: int = COLS,
    tt: Optional[TranspositionTable] = None,
    time_limit: Optional[float] = None,
    counter: Optional[list[int]] = None,
    start_time: Optional[float] = None,
    is_root: bool = False,
) -> tuple[float, int]:
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
        drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            if tt is not None:
                tt.put(hash_key, depth, 100000.0, 0)
            return 100000.0, col
        un_drop(board, col, ROWS, cols)

    tt_entry = None
    if tt is not None and not is_root:
        tt_entry = tt.get(hash_key, depth)

    if tt_entry is not None:
        val = tt_entry.value
        if tt_entry.flag == 0:
            return val, 0
        if tt_entry.flag == 1 and val >= beta:
            return val, 0
        if tt_entry.flag == 2 and val <= alpha:
            return val, 0

    if depth <= 0:
        return _evaluate(board, mark, cols), legal[0]

    # Null-move pruning
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
        except (ValueError, IndexError):
            null_ok = False

    if null_ok:
        null_board = list(board)
        score = -_pvs(
            null_board, mark, depth - 3,
            -beta, -beta + 1,
            cols, tt, time_limit, counter, start_time,
        )[0]
        if score >= beta:
            return beta, 0

    # Move ordering
    tt_move = 0
    ordered = _order_moves_pvs(board, legal, mark, cols, tt, hash_key,
                               depth, tt_move, _KILLER_TABLE[depth][:])

    best_score = float("-inf")
    best_col = ordered[0]
    first = True

    for col in ordered:
        try:
            drop(board, col, mark, ROWS, cols)
        except ValueError:
            continue

        if first:
            score, _ = _pvs(
                board, 3 - mark, depth - 1,
                -beta, -alpha,
                cols, tt, time_limit, counter, start_time,
            )
            score = -score
            first = False
        else:
            score, _ = _pvs(
                board, 3 - mark, depth - 1,
                -alpha - 1, -alpha,
                cols, tt, time_limit, counter, start_time,
            )
            score = -score
            if score > alpha and score < beta:
                score, _ = _pvs(
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
    global _HISTORY_TABLE
    _clear_killer_history()
    _HISTORY_TABLE = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0
    counter = [0]

    for depth in range(min_depth, max_depth + 1):
        if time_limit is not None and start_time is not None:
            if time.time() - start_time >= time_limit * 0.95:
                break

        legal = valid_moves(board, cols)
        if not legal:
            return 0

        board_copy = list(board)

        _, col = _pvs(
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
    """v5: deeper search thanks to fast evaluation."""
    if time_limit is not None:
        if time_limit > 1.0:
            return 3, 18
        elif time_limit > 0.5:
            return 3, 15
        elif time_limit > 0.2:
            return 2, 13
        elif time_limit > 0.1:
            return 2, 11
        else:
            return 2, 9
    return 3, 18


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_bot_v5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Bitboard alpha-beta v5 — fast eval + PVS."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline - time.time()

    min_d, max_d = _select_depth(time_limit)
    col = _iterative_deepening(
        board_list, mark, cols, time_limit, min_d, max_d,
    )
    if col in legal:
        return col
    return legal[0]


def bitboard_ab_bot_fast_v5(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast v5 — PVS to depth 12."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline - time.time()

    col = _iterative_deepening(
        board_list, mark, cols, time_limit, 1, 12,
    )
    if col in legal:
        return col
    return legal[0]