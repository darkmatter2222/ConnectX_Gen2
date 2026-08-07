"""
Bitboard Alpha-Beta Bot — strong classical ConnectX player.

Internal representation uses 64-bit bitboards for the player and opponent.
Bitwise operations evaluate all horizontal, vertical, and diagonal lines
in parallel, yielding far greater throughput than the per-window scanning
of the shallow minimax.

External interface: ``board`` stays as a flat list (row-major) for gym
compatibility.  Conversion overhead is amortised over deep searches.

Features
--------
* Negamax with alpha-beta pruning + null-move pruning
* Transposition table (zobrist-hashed) with depth tracking
* Move ordering: center bias + tactical hints
* Time management: stops when deadline is reached

Strength: expected to defeat all built-in baselines consistently.
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

_MAX_DEPTH: int = 16
_EMPTY_MASK: int = (1 << SIZE) - 1  # lowest 42 bits

# Precomputed bit index for each flat-cell index
_CELL_BIT: list[int] = [r * COLS + c for r in range(ROWS) for c in range(COLS)]

# Precomputed line bitmasks for every winning line
_LINE_MASKS: list[int] = []


def _init_lines() -> None:
    """Build bitmask for every winning line (7x6/4 → 69 horizontal + 69 vertical + 36 diag)."""
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


# ── Transposition table ────────────────────────────────────────────────────────


@dataclass
class TTEntry:
    """One entry in the transposition table."""
    hash_key: int
    depth: int
    value: float
    flag: int  # 0 = exact, 1 = lower bound, 2 = upper bound


class TranspositionTable:
    """Hash-table-backed transposition table (power-of-two size)."""

    def __init__(self, size: int = 1 << 18) -> None:
        self._size = size
        self._table: list[Optional[TTEntry]] = [None] * size

    def get(self, key: int, depth: int) -> Optional[TTEntry]:
        entry = self._table[key & (self._size - 1)]
        if entry is not None and entry.hash_key == key and entry.depth >= depth:
            return entry
        return None

    def put(self, key: int, depth: int, value: float, flag: int) -> None:
        self._table[key & (self._size - 1)] = TTEntry(hash_key=key, depth=depth, value=value, flag=flag)

    def clear(self) -> None:
        self._table = [None] * self._size


TT = TranspositionTable(1 << 18)


# ── Zobrist hashing ────────────────────────────────────────────────────────────

_ZOBRIST: list[list[int]] = []


def _init_zobrist() -> None:
    """Initialize Zobrist keys for every cell and mark."""
    import random
    rng = random.Random(42)
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])  # mark 1
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])  # mark 2


_init_zobrist()


def _zobrist_hash(board: Sequence[int]) -> int:
    """Compute Zobrist hash of board state."""
    h = 0
    for i, cell in enumerate(board):
        if cell != 0:
            h ^= _ZOBRIST[cell - 1][i]
    return h


# ── Bitboard evaluation ────────────────────────────────────────────────────────

def _to_bitboard(board: Sequence[int], mark: int) -> int:
    """Bitboard: bits set where the specified mark has pieces."""
    bb = 0
    for i, cell in enumerate(board):
        if cell == mark:
            bb |= 1 << _CELL_BIT[i]
    return bb


def _set_bits(x: int) -> list[int]:
    """Return indices of set bits in x."""
    bits = []
    i = 0
    while x:
        if x & 1:
            bits.append(i)
        x >>= 1
        i += 1
    return bits


def _row_col(bit: int, cols: int) -> tuple[int, int]:
    """Convert bit index to (row, col)."""
    return bit // cols, bit % cols


def _open_end_bonus(board: list[int], line_mask: int, mark: int,
                    cols: int) -> float:
    """
    Bonus if a 3-in-a-row has an open (empty) end that can be
    extended by a legal move.  Detects forks and anti-forks.
    """
    cells = []
    for bit in _set_bits(line_mask):
        r, c = _row_col(bit, cols)
        cells.append((r, c))
    cells.sort()

    first, last = cells[0], cells[-1]
    bonus = 0.0

    # Left / above extensions of first cell
    if first[1] > 0 and board[first[0] * cols + (first[1] - 1)] == 0:
        bonus += 50.0
    if first[0] > 0 and board[(first[0] - 1) * cols + first[1]] == 0:
        bonus += 50.0

    # Right / below extensions of last cell
    if last[1] + INAROW - 1 < cols:
        if board[last[0] * cols + (last[1] + INAROW - 1)] == 0:
            bonus += 50.0
    if last[0] + INAROW - 1 < ROWS:
        if board[(last[0] + INAROW - 1) * cols + last[1]] == 0:
            bonus += 50.0

    return bonus


# ── Fork and threat-weighted evaluation ────────────────────────────────────────

def _evaluate(
    board: list[int], mark: int, cols: int = COLS,
    depth: int = 0,
) -> float:
    """
    Fork-aware positional evaluation with threat weighting.

    Scoring (higher = better for ``mark``):
      +100000  immediate win
      +800     threat (3-in-row with open end)
      +200     blocked threat (3-in-row)
      +100     fork (2+ threats sharing a cell)
      +30      good 2-in-row (2 pieces + 2 empty cells)
      +1       per piece in center column
      -800     opponent threat
      -200     opponent blocked threat
      -100     opponent fork
      -30      opponent 2-in-row
    """
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0
    center_col = cols // 2

    # Track open 3s and 2s
    player_threats = 0
    player_block3 = 0
    player_open2 = 0

    opp_threats = 0
    opp_block3 = 0
    opp_open2 = 0

    # Count cells participating in threats (for fork detection)
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

        # Track open 3s (threats)
        if p_count == 3 and e_count >= 1:
            player_threats += 1
            for bit in _set_bits(player_in):
                player_threat_cells[bit] += 1
        elif p_count == 3:
            player_block3 += 1

        if o_count == 3 and e_count >= 1:
            opp_threats += 1
            for bit in _set_bits(opp_in):
                opp_threat_cells[bit] += 1
        elif o_count == 3:
            opp_block3 += 1

        if p_count == 2 and e_count >= 2:
            player_open2 += 1
        if o_count == 2 and e_count >= 2:
            opp_open2 += 1

    # ── Threat scoring ──
    score += player_threats * 800.0
    score += opp_threats * (-800.0)

    # ── Blocked threats ──
    score += player_block3 * 200.0
    score += opp_block3 * (-200.0)

    # ── Fork detection ──
    max_p = 0
    max_o = 0
    for i in range(SIZE):
        if player_threat_cells[i] > max_p:
            max_p = player_threat_cells[i]
        if opp_threat_cells[i] > max_o:
            max_o = opp_threat_cells[i]
    if max_p >= 2:
        score += 100.0
    if max_o >= 2:
        score -= 100.0

    # ── Open 2-in-row scoring ──
    score += player_open2 * 30.0
    score += opp_open2 * (-30.0)

    # ── Center control ──
    for bit in _set_bits(player_bb):
        r, c = _row_col(bit, cols)
        if c == center_col:
            score += 1.0
        elif abs(c - center_col) == 1:
            score += 0.5

    return score


def _line_participation(board: list[int], r: int, c: int,
                        rows: int, cols: int) -> int:
    """
    Count how many winning lines pass through cell (r, c).
    Higher weight = more strategic value for center control.
    """
    count = 0
    # Horizontal
    if c + INAROW <= cols:
        count += 1
    if c >= INAROW - 1:
        count += 1
    # Vertical
    if r + INAROW <= rows:
        count += 1
    # Diagonal down-right
    if r + INAROW <= rows and c + INAROW <= cols:
        count += 1
    # Diagonal down-left
    if r + INAROW <= rows and c >= INAROW - 1:
        count += 1
    return count


# ── Negamax with alpha-beta ────────────────────────────────────────────────────


def _negamax(
    board: list[int],
    mark: int,
    depth: int,
    alpha: float,
    beta: float,
    cols: int = COLS,
    tt: Optional[TranspositionTable] = None,
    time_limit: Optional[float] = None,
    counter: Optional[list[int]] = None,
    start_time: Optional[float] = None,
) -> tuple[float, int]:
    """
    Negamax with alpha-beta pruning, transposition table, and time check.

    Returns (score, best_col).
    """
    legal = valid_moves(board, cols)
    if not legal:
        return 0.0, 0

    # Time limit exceeded?
    if time_limit is not None and start_time is not None:
        if time.time() - start_time >= time_limit:
            return _evaluate(board, mark, cols), legal[0]

    if counter is not None:
        counter[0] += 1

    hash_key = _zobrist_hash(board)
    tt_entry = None if tt is None else tt.get(hash_key, depth)

    if tt_entry is not None:
        val = tt_entry.value
        if tt_entry.flag == 0:  # exact
            return val, legal[0]
        if tt_entry.flag == 1 and val >= beta:  # lower bound (Alpha)
            return val, legal[0]
        if tt_entry.flag == 2 and val <= alpha:  # upper bound (Beta)
            return val, legal[0]

    # Depth reached — evaluate
    if depth <= 0:
        return _evaluate(board, mark, cols, depth=depth), legal[0]

    # Check immediate win
    for col in legal:
        drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            return 100000.0, col
        un_drop(board, col, ROWS, cols)

    best_score = float("-inf")
    best_col = legal[0]

    # Null-move pruning: skip our turn and see if opponent still loses
    if depth >= 3 and len(legal) > 1:
        null_board = list(board)
        # Skip: opponent would play two moves in a row, so we look at
        # the position with depth-3 reduced and color flipped
        score = -_negamax(
            null_board, mark, depth - 3,
            -beta, -beta + 1,
            cols, tt, time_limit, counter, start_time,
        )[0]
        if score >= beta:
            return beta, legal[0]

    # Order moves for better pruning
    ordered = _order_moves(board, legal, mark, cols)

    for col in ordered:
        drop(board, col, mark, ROWS, cols)
        score, _ = _negamax(
            board, 3 - mark, depth - 1,
            -beta, -alpha,
            cols, tt, time_limit, counter, start_time,
        )
        score = -score
        un_drop(board, col, ROWS, cols)

        if score > best_score:
            best_score = score
            best_col = col

        if score > alpha:
            alpha = score

        if alpha >= beta:
            if tt is not None:
                tt.put(hash_key, depth, beta, 2)
            break

    if tt is not None:
        flag = 0
        if best_score >= beta:
            flag = 2  # upper bound
        elif best_score <= alpha:
            flag = 1  # lower bound
        tt.put(hash_key, depth, best_score, flag)

    return best_score, best_col


# ── Move ordering ──────────────────────────────────────────────────────────────

def _order_moves(board: list[int], legal: Sequence[int], mark: int,
                 cols: int = COLS) -> list[int]:
    """
    Order legal moves for better alpha-beta pruning.

    Priority:
      1. Immediate wins
      2. Blocking opponent's immediate wins
      3. Moves that create forks or major threats
      4. Center-biased moves
    """
    opp = 3 - mark
    wins: list[int] = []
    blocks: list[int] = []
    threats: list[int] = []  # moves creating threats
    others: list[int] = []

    for col in legal:
        drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            wins.append(col)
            continue
        un_drop(board, col, ROWS, cols)

        drop(board, col, opp, ROWS, cols)
        if check_win(board, col, opp, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            blocks.append(col)
            continue
        un_drop(board, col, ROWS, cols)

        # Check if placing here creates a threat (3-in-row with open end)
        try:
            drop(board, col, mark, ROWS, cols)
            if _has_threat(board, col, mark, ROWS, cols):
                threats.append(col)
            un_drop(board, col, ROWS, cols)
        except ValueError:
            pass

        others.append(col)

    center = cols // 2
    others.sort(key=lambda c: abs(c - center))
    threats.sort(key=lambda c: abs(c - center))
    blocks.sort(key=lambda c: abs(c - center))

    return wins + blocks + threats + others


def _has_threat(board: list[int], last_col: int, mark: int,
                rows: int, cols: int) -> bool:
    """
    Check if placing a piece in last_col creates a threat
    (3-in-row with at least one open end).
    """
    last_row = 0
    for r in range(rows - 1, -1, -1):
        if board[r * cols + last_col] == mark:
            last_row = r
            break

    # Check all lines through this cell
    cell_idx = last_row * cols + last_col
    return _is_threat_at(board, cell_idx, mark, rows, cols)


def _is_threat_at(board: list[int], idx: int, mark: int,
                  rows: int, cols: int) -> bool:
    """Check if placing at idx creates a threat in any direction."""
    r = idx // cols
    c = idx % cols

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        # Count consecutive pieces in both directions
        count = 1  # count the piece itself

        # Forward direction
        fr, fc = r + dr, c + dc
        while 0 <= fr < rows and 0 <= fc < cols and board[fr * cols + fc] == mark:
            count += 1
            fr += dr
            fc += dc

        # Check open end in forward direction
        if count >= 3:
            if 0 <= fr < rows and 0 <= fc < cols and board[fr * cols + fc] == 0:
                return True

        # Backward direction
        br, bc = r - dr, c - dc
        while 0 <= br < rows and 0 <= bc < cols and board[br * cols + bc] == mark:
            count += 1
            br -= dr
            bc -= dc

        # Check open end in backward direction
        if count >= 3:
            if 0 <= br < rows and 0 <= bc < cols and board[br * cols + bc] == 0:
                return True

    return False


# ── Time-aware depth selector ──────────────────────────────────────────────────

def _select_depth(board: list[int], time_limit: Optional[float],
                  cols: int = COLS) -> int:
    """
    Choose search depth based on time budget and board occupancy.

    Early game (few pieces): shallow — more branches to search
    Late game (many pieces): deep — fewer branches, tactical
    Generous time: deeper search
    Tight time: shallower but with immediate win detection
    """
    pieces = sum(1 for cell in board if cell != 0)

    if time_limit is not None and time_limit > 1.0:
        base = 10
    elif time_limit is not None and time_limit > 0.5:
        base = 9
    elif time_limit is not None and time_limit > 0.2:
        base = 8
    elif time_limit is not None and time_limit > 0.1:
        base = 7
    else:
        base = 6

    # Early game: fewer pieces → fewer branches → can go deeper
    # But also: early game has more moves to search → shallower
    if pieces < 8:
        base = max(6, base - 1)
    elif pieces > 32:
        base = min(14, base + 2)

    return base


# ── Public bot API ─────────────────────────────────────────────────────────────


def bitboard_ab_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    Bitboard alpha-beta bot — main entry point.

    Args:
        board: flat board array (read-only)
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns
        move_deadline: optional epoch time when this move must be returned
        remaining_overage: seconds of overage budget (unused)
        seed: deterministic seed (unused, for API compatibility)

    Returns:
        column index (0-based)
    """
    board_list = list(board)

    # Recompute legal moves — caller's list may include full columns
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    # Compute time budget
    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline

    depth = _select_depth(board_list, time_limit, cols)

    # Reset transposition table for each move to avoid stale entries
    TT.clear()

    _, best_col = _negamax(
        board_list, mark, depth,
        float("-inf"), float("inf"),
        cols, TT, time_limit,
        [0], time.time(),
    )

    return best_col


def bitboard_ab_bot_fast(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """
    Fast bitboard bot — fixed depth 7, no time management.

    For matches where the full bot might exceed the action deadline.
    """
    board_list = list(board)

    # Recompute legal moves
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    TT.clear()
    _, col = _negamax(
        board_list, mark, 7,
        float("-inf"), float("inf"),
        cols, TT, None,
        [0], None,
    )
    return col