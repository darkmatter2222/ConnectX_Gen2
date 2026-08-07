"""
Alpha-beta with neural network evaluation.

Uses a trained neural network (via knowledge distillation from v2)
as the leaf evaluation function.

Model path: O:\\master_model_collection\\ConnectX_Gen2_Phase2\\models\\connectx_nn_teacher\\best.pth
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np

from connectx.engine import (
    check_win, drop, un_drop, valid_moves,
    ROWS, COLS, INAROW, SIZE,
)
from connectx.bots.nn_evaluator import ConnectXNet

# ── Model path ─────────────────────────────────────────────────────────────────

_MODEL_PATH = os.environ.get(
    'CONNECTX_NN_MODEL',
    r'O:\master_model_collection\ConnectX_Gen2_Phase2\models\connectx_nn_teacher\best.pth',
)

_nn_model = None
_nn_device = 'cuda'  # try GPU, fall back to CPU


def _get_nn_model():
    """Lazy-load the trained neural network model."""
    global _nn_model
    if _nn_model is not None:
        return _nn_model

    try:
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        _nn_model = ConnectXNet().to(device)
        _nn_model.load_state_dict(
            torch.load(_MODEL_PATH, map_location=device, weights_only=True)
        )
        _nn_model.eval()
        return _nn_model
    except Exception:
        return None


def _nn_evaluate(board, mark, cols=COLS):
    """Evaluate board using trained neural network."""
    model = _get_nn_model()
    if model is None:
        return 0.0  # Fallback

    try:
        import torch
        opp = 3 - mark
        n = ROWS * COLS
        feat = np.zeros(2 * n, dtype=np.float32)

        for i in range(n):
            if board[i] == mark:
                feat[i] = 1.0
            elif board[i] == opp:
                feat[i + n] = 1.0

        with torch.no_grad():
            x = torch.tensor([feat], dtype=torch.float32).to(_nn_device)
            return model(x).item()
    except Exception:
        return 0.0


def _heuristic_eval(board, mark, cols=COLS):
    """Simple heuristic fallback if NN fails."""
    opp = 3 - mark
    score = 0.0

    player_col = [0] * COLS
    opp_col = [0] * COLS

    for i in range(ROWS * COLS):
        if board[i] == mark:
            score += 1.0
            _, c = divmod(i, COLS)
            player_col[c] += 1
        elif board[i] == opp:
            score -= 1.0
            _, c = divmod(i, COLS)
            opp_col[c] += 1

    center = cols // 2
    for c in range(COLS):
        score += (player_col[c] - opp_col[c]) * max(0, 3 - abs(c - center)) * 0.1

    return score


# ── Bitboard helpers ───────────────────────────────────────────────────────────

_CELL_BIT = [r * COLS + c for r in range(ROWS) for c in range(COLS)]
_LINE_MASKS = []
_EMPTY_MASK = (1 << SIZE) - 1


def _init_lines():
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
    def __init__(self, size: int = 1 << 19) -> None:
        self._size = size
        self._table: list = [None] * size

    def get(self, key, depth):
        entry = self._table[key & (self._size - 1)]
        if entry is not None and entry.hash_key == key and entry.depth >= depth:
            return entry
        return None

    def put(self, key, depth, value, flag):
        self._table[key & (self._size - 1)] = TTEntry(key, depth, value, flag)

    def clear(self):
        self._table = [None] * self._size


TT = TranspositionTable(1 << 19)


# ── Zobrist hashing ────────────────────────────────────────────────────────────

_ZOBRIST = []


def _init_zobrist():
    import random
    rng = random.Random(42)
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])
    _ZOBRIST.append([rng.getrandbits(64) for _ in range(SIZE)])


_init_zobrist()


def _zobrist_hash(board):
    h = 0
    for i, cell in enumerate(board):
        if cell != 0:
            h ^= _ZOBRIST[cell - 1][i]
    return h


# ── Killer moves & history ────────────────────────────────────────────────────

_KILLER_TABLE = [[-1, -1] for _ in range(64)]
_HISTORY_TABLE = [0] * (SIZE * 4)


def _history_score(col, row):
    idx = row * COLS + col
    return _HISTORY_TABLE[idx] if 0 <= idx < len(_HISTORY_TABLE) else 0


def _update_history(col, row, bonus):
    idx = row * COLS + col
    if 0 <= idx < len(_HISTORY_TABLE):
        _HISTORY_TABLE[idx] += bonus


def _record_killer(depth, move):
    if _KILLER_TABLE[depth][0] != move:
        _KILLER_TABLE[depth][1] = _KILLER_TABLE[depth][0]
        _KILLER_TABLE[depth][0] = move


def _clear_killer_history():
    for i in range(len(_KILLER_TABLE)):
        _KILLER_TABLE[i] = [-1, -1]


# ── Move ordering ──────────────────────────────────────────────────────────────

def _order_moves(board, legal, mark, cols, tt, hash_key, depth, tt_move, killer_moves_list):
    opp = 3 - mark
    current_legal = valid_moves(board, cols)
    current_set = set(current_legal)
    legal = [c for c in legal if c in current_set] or current_legal

    killer_moves = [k for k in killer_moves_list if k >= 0 and k in legal]

    hist = {}
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
                while (0 <= fr < ROWS and 0 <= fc < COLS and board[fr * cols + fc] == mark):
                    cnt += 1; fr += dr; fc += dc
                if cnt >= 3 and 0 <= fr < ROWS and 0 <= fc < COLS and board[fr * cols + fc] == 0:
                    is_threat = True
                    break
                br, bc = rc[0] - dr, rc[1] - dc
                while (0 <= br < ROWS and 0 <= bc < COLS and board[br * cols + bc] == mark):
                    cnt += 1; br -= dr; bc -= dc
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


# ── PVS Negamax with NN evaluation ─────────────────────────────────────────────

def _pvs(
    board, mark, depth, alpha, beta,
    cols=COLS, tt=None, time_limit=None,
    counter=None, start_time=None, is_root=False,
):
    legal = valid_moves(board, cols)
    if not legal:
        return 0.0, 0

    if time_limit is not None and start_time is not None:
        if time.time() - start_time >= time_limit:
            val = _nn_evaluate(board, mark, cols)
            return val, legal[0]

    if counter is not None:
        counter[0] += 1

    hash_key = _zobrist_hash(board)

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
        return _nn_evaluate(board, mark, cols), legal[0]

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
            -beta, -beta + 1, cols, tt, time_limit, counter, start_time,
        )[0]
        if score >= beta:
            return beta, 0

    ordered = _order_moves(board, legal, mark, cols, tt, hash_key,
                           depth, 0, _KILLER_TABLE[depth][:])

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
                -beta, -alpha, cols, tt, time_limit, counter, start_time,
            )
            score = -score
            first = False
        else:
            score, _ = _pvs(
                board, 3 - mark, depth - 1,
                -alpha - 1, -alpha, cols, tt, time_limit, counter, start_time,
            )
            score = -score
            if score > alpha and score < beta:
                score, _ = _pvs(
                    board, 3 - mark, depth - 1,
                    -beta, -alpha, cols, tt, time_limit, counter, start_time,
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


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_nn_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Alpha-beta with neural network evaluation."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline - time.time()

    _clear_killer_history()
    _HISTORY_TABLE[:] = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0
    counter = [0]

    for depth in range(1, 18):
        if time_limit is not None and start_time is not None:
            if time.time() - start_time >= time_limit:
                break

        legal = valid_moves(board_list, cols)
        if not legal:
            return 0

        _, col = _pvs(
            list(board_list), mark, depth,
            float("-inf"), float("inf"),
            cols, TT, time_limit, counter, start_time,
            is_root=True,
        )

        if col not in legal:
            col = legal[0]
        best_col = col

        for r in range(ROWS - 1, -1, -1):
            if board_list[r * cols + best_col] == mark:
                _update_history(best_col, r, depth * 100)
                break

        if time_limit is not None and start_time is not None:
            if time.time() - start_time >= time_limit:
                break

    return best_col if best_col in legal else legal[0]