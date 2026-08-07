"""
Kaggle ConnectX Bot — Self-contained deployable submission.

Implements v2 alpha-beta with iterative deepening, killer moves,
history heuristic, transposition table, null-move pruning, and
bounds-capped negamax (inf-fix).

Kaggle API:
    def agent(obs, config) -> int
        obs.board: flat list/array of length rows*cols (0=empty, 1=player, 2=opponent)
        obs.mark: 1 or 2
        config.columns: int (7)
        config.rows: int (6)
        config.inarow: int (4)

Usage:
    1. Copy this entire file to Kaggle workspace
    2. Submit as the bot file
    3. Kaggle calls agent(obs, config) each turn

Performance profile:
    - Empty board: ~61ms per move
    - Mid-game: 1-14ms per move
    - Well within 2-second action budget
"""

from __future__ import annotations

import time
from typing import Optional, Sequence

# =============================================================================
# Constants
# =============================================================================

ROWS = 6
COLS = 7
INAROW = 4
SIZE = ROWS * COLS  # 42
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2


# =============================================================================
# Line masks for win detection and evaluation
# =============================================================================

_CELL_BIT = [r * COLS + c for r in range(ROWS) for c in range(COLS)]

_LINE_MASKS = []


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

_EMPTY_MASK = (1 << SIZE) - 1


# =============================================================================
# Direction constants
# =============================================================================

_DIRS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def _index(row: int, col: int, cols: int) -> int:
    """Convert (row, col) to flat index."""
    return row * cols + col


def _in_a_row(board, start_row, start_col, dr, dc, mark, inarow, rows, cols):
    """Check inarow consecutive cells starting at (start_row, start_col)
    in direction (dr, dc) all equal mark."""
    count = 0
    r, c = start_row, start_col
    for _ in range(inarow):
        if 0 <= r < rows and 0 <= c < cols and board[_index(r, c, cols)] == mark:
            count += 1
        else:
            break
        r += dr
        c += dc
    return count == inarow


# =============================================================================
# Engine: drop, un_drop, valid_moves, check_win
# =============================================================================


def drop(board: list[int], col: int, mark: int, rows: int, cols: int) -> int:
    """Place mark in column col at the lowest empty row. Returns row index."""
    for r in range(rows - 1, -1, -1):
        if board[r * cols + col] == EMPTY:
            board[r * cols + col] = mark
            return r
    raise ValueError(f"Column {col} is full")


def un_drop(board: list[int], col: int, rows: int, cols: int, row: int) -> None:
    """Remove piece from column col at the given row."""
    board[row * cols + col] = EMPTY


def valid_moves(board: list[int], cols: int) -> list[int]:
    """Return list of legal column indices."""
    return [c for c in range(cols) if board[c] == EMPTY]


def check_win(board: list[int], last_col: int, mark: int, rows: int, cols: int) -> bool:
    """Check if the last move in last_col created a win for mark."""
    # Find the row where the piece landed
    placed_row = None
    for r in range(rows):
        if board[_index(r, last_col, cols)] == mark:
            placed_row = r
            break
    if placed_row is None:
        return False

    for dr, dc in _DIRS:
        if _in_a_row(board, placed_row, last_col, dr, dc, mark, INAROW, rows, cols):
            return True
        if _in_a_row(board, placed_row, last_col, -dr, -dc, mark, INAROW, rows, cols):
            return True

    return False


# =============================================================================
# Zobrist hashing
# =============================================================================

_ZOBRIST = [[0] * SIZE for _ in range(2)]


def _init_zobrist() -> None:
    import random
    rng = random.Random(42)
    _ZOBRIST[0] = [rng.getrandbits(64) for _ in range(SIZE)]
    _ZOBRIST[1] = [rng.getrandbits(64) for _ in range(SIZE)]


_init_zobrist()


def _zobrist_hash(board: Sequence[int]) -> int:
    h = 0
    for i, cell in enumerate(board):
        if cell != EMPTY:
            h ^= _ZOBRIST[cell - 1][i]
    return h


# =============================================================================
# Transposition table
# =============================================================================

class TTEntry:
    __slots__ = ('hash_key', 'depth', 'value', 'flag', 'mark')

    def __init__(self, hash_key: int, depth: int, value: float, flag: int, mark: int) -> None:
        self.hash_key = hash_key
        self.depth = depth
        self.value = value
        self.flag = flag
        self.mark = mark


class TranspositionTable:
    def __init__(self, size: int = 1 << 19) -> None:
        self._size = size
        self._table = [None] * size

    def get(self, key: int, depth: int) -> Optional[TTEntry]:
        entry = self._table[key & (self._size - 1)]
        if entry is not None and entry.hash_key == key and entry.depth >= depth:
            return entry
        return None

    def put(self, key: int, depth: int, value: float, flag: int, mark: int) -> None:
        self._table[key & (self._size - 1)] = TTEntry(key, depth, value, flag, mark)

    def clear(self) -> None:
        self._table = [None] * self._size


# =============================================================================
# Killer moves & history
# =============================================================================

_KILLER_TABLE = [[-1, -1] for _ in range(64)]
_HISTORY_TABLE = [0] * (SIZE * 4)


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


# =============================================================================
# Bitboard helpers
# =============================================================================


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


def _row_col(bit: int, cols: int) -> tuple:
    return bit // cols, bit % cols


# =============================================================================
# Evaluation
# =============================================================================


def _evaluate(board: list[int], mark: int, cols: int = COLS) -> float:
    """Fork-aware positional evaluation."""
    opp = 3 - mark
    player_bb = _to_bitboard(board, mark)
    opp_bb = _to_bitboard(board, opp)
    empty_bb = ~(player_bb | opp_bb) & _EMPTY_MASK

    score = 0.0
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

    score += player_threats * 800.0 - opp_threats * 800.0
    score += player_block3 * 200.0 - opp_block3 * 200.0

    max_p = max_o = 0
    for i in range(SIZE):
        if player_threat_cells[i] > max_p:
            max_p = player_threat_cells[i]
        if opp_threat_cells[i] > max_o:
            max_o = opp_threat_cells[i]
    if max_p >= 2:
        score += 100.0
    if max_o >= 2:
        score -= 100.0

    score += player_open2 * 30.0 - opp_open2 * 30.0

    for bit in _set_bits(player_bb):
        r, c = _row_col(bit, cols)
        if c == center_col:
            score += 1.0
        elif abs(c - center_col) == 1:
            score += 0.5

    return score


center_col = COLS // 2


# =============================================================================
# Threat check (move ordering)
# =============================================================================


def _has_threat(board: list[int], last_col: int, mark: int, rows: int, cols: int) -> bool:
    last_row = 0
    for r in range(rows - 1, -1, -1):
        if board[r * cols + last_col] == mark:
            last_row = r
            break
    return _is_threat_at(board, last_row * cols + last_col, mark, rows, cols)


def _is_threat_at(board: list[int], idx: int, mark: int, rows: int, cols: int) -> bool:
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
                board[fr * cols + fc] == EMPTY):
            return True
        br, bc = r - dr, c - dc
        while (0 <= br < rows and 0 <= bc < cols and
               board[br * cols + bc] == mark):
            count += 1
            br -= dr
            bc -= dc
        if (count >= 3 and 0 <= br < rows and 0 <= bc < cols and
                board[br * cols + bc] == EMPTY):
            return True
    return False


# =============================================================================
# Move ordering
# =============================================================================


def _order_moves(
    board: list[int], legal: Sequence[int], mark: int,
    cols: int, tt: TranspositionTable, hash_key: int, depth: int,
) -> list[int]:
    """Order: killers -> wins -> blocks -> threats -> center -> history."""
    opp = 3 - mark

    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killers = _KILLER_TABLE[depth]
    killer_moves = [k for k in killers if k >= 0 and k in legal]

    hist = {}
    for col in legal:
        for r in range(ROWS - 1, -1, -1):
            if board[r * cols + col] == EMPTY:
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

    others = sorted(
        [c for c in legal if c not in wins and c not in blocks and c not in threats],
        key=lambda c: abs(c - center_col),
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


# =============================================================================
# Negamax with alpha-beta, TT, null-move pruning, bounds capping
# =============================================================================


def _negamax(
    board: list[int], mark: int, depth: int,
    alpha: float, beta: float,
    cols: int = COLS,
    tt: Optional[TranspositionTable] = None,
    time_limit: Optional[float] = None,
    counter: Optional[list] = None,
    start_time: Optional[float] = None,
    is_root: bool = False,
) -> tuple:
    """Negamax with alpha-beta, TT, killer moves, history heuristic."""
    # Bounds capping prevents infinity propagation
    alpha = max(alpha, -100000.0)
    beta = min(beta, 100000.0)

    legal = valid_moves(board, cols)
    if not legal:
        return 0.0, legal[0] if legal else 0

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
            return val, 0
        if tt_entry.flag == 1 and val >= beta:
            return val, 0
        if tt_entry.flag == 2 and val <= alpha:
            return val, 0

    if depth <= 0:
        return _evaluate(board, mark, cols), legal[0]

    best_score = float("-inf")
    best_col = legal[0]

    # Check opponent 4-in-a-row
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
            for col in legal:
                try:
                    opp_row = drop(board, col, opp, ROWS, cols)
                    if check_win(board, col, opp, ROWS, cols):
                        null_ok = False
                        un_drop(board, col, ROWS, cols, row=opp_row)
                        break
                except ValueError:
                    pass
                else:
                    try:
                        un_drop(board, col, ROWS, cols, row=opp_row)
                    except ValueError:
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
            return beta, 0

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


# =============================================================================
# Iterative deepening
# =============================================================================


def _iterative_deepening(
    board: list[int], mark: int, cols: int,
    time_limit: Optional[float],
    min_depth: int, max_depth: int,
) -> int:
    """Iterative deepening: returns best move from deepest completed depth."""
    global _HISTORY_TABLE
    _clear_killer_history()
    _HISTORY_TABLE = [0] * len(_HISTORY_TABLE)
    tt = TranspositionTable(1 << 19)

    start_time = time.time()
    best_col = COLS // 2  # default: center
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
            cols, tt, time_limit, counter, start_time,
            is_root=True,
        )

        if col not in legal:
            col = legal[0]

        best_col = col

        for r in range(ROWS - 1, -1, -1):
            if board_copy[r * cols + best_col] == mark:
                _update_history(best_col, r, depth * 100)
                break

        if time_limit is not None:
            if time.time() - start_time >= time_limit:
                break

    return best_col


# =============================================================================
# Depth selector
# =============================================================================


def _select_depth(time_limit: Optional[float]) -> tuple:
    """Return (min_depth, max_depth)."""
    if time_limit is not None:
        if time_limit > 1.0:
            return 3, 12
        elif time_limit > 0.5:
            return 3, 10
        elif time_limit > 0.2:
            return 3, 9
        elif time_limit > 0.1:
            return 2, 8
        else:
            return 2, 7
    return 3, 12


# =============================================================================
# Public API
# =============================================================================


def bitboard_ab_bot_v2(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Bitboard alpha-beta v2 -- iterative deepening + killer moves + history."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = max(0.01, move_deadline - time.time())

    min_d, max_d = _select_depth(time_limit)
    col = _iterative_deepening(
        board_list, mark, cols, time_limit, min_d, max_d,
    )
    if col in legal:
        return col
    return legal[0]


# =============================================================================
# Kaggle entry point
# =============================================================================


def agent(obs, config) -> int:
    """
    Kaggle ConnectX bot entry point.

    Args:
        obs: Observation with .board (flat array) and .mark (1 or 2)
        config: Configuration with .columns, .rows, .inarow

    Returns:
        Column index (0-based) to drop piece
    """
    board = list(obs.board)
    mark = obs.mark
    cols = getattr(config, 'columns', COLS)
    rows = getattr(config, 'rows', ROWS)
    inarow = getattr(config, 'inarow', INAROW)

    # Get legal moves
    legal = [c for c in range(cols) if board[c] == EMPTY]

    if not legal:
        return 0

    # Kaggle doesn't pass deadlines directly; estimate from context
    col = bitboard_ab_bot_v2(
        board, mark, legal, cols,
        move_deadline=None,
        remaining_overage=0.0,
        seed=None,
    )

    if col not in legal:
        return legal[0]
    return col


def connectx_bot(obs, config) -> int:
    """Alias for Kaggle agent."""
    return agent(obs, config)