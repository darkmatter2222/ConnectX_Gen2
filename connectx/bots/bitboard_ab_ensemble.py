"""
Alpha-beta with ensemble evaluation: v2 heuristic + neural network.

Uses a weighted combination of v2's handcrafted evaluation and the trained
neural network. This provides:
1. Robustness: v2's heuristic handles edge cases correctly
2. Learning: NN captures positional patterns not in the heuristic
3. Safety: if NN fails, v2 fallback prevents crashes

Architecture: score = w_heuristic × v2_eval + w_nn × nn_eval
Default weights: w_heuristic=0.7, w_nn=0.3
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
_nn_device = 'cuda'


def _get_nn_model():
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


# ── v2 Heuristic evaluation ──────────────────────────────────────────────────

_BITMASK = [1 << (r * COLS + c) for r in range(ROWS) for c in range(COLS)]
_LINE_MASKS = []


def _init_lines():
    for r in range(ROWS):
        for c in range(COLS):
            if c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << (r * COLS + c + k)
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << ((r + k) * COLS + c)
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS and c + INAROW <= COLS:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << ((r + k) * COLS + c + k)
                _LINE_MASKS.append(mask)
            if r + INAROW <= ROWS and c + 1 >= INAROW:
                mask = 0
                for k in range(INAROW):
                    mask |= 1 << ((r + k) * COLS + c - k)
                _LINE_MASKS.append(mask)


_init_lines()


def _to_bb(board, mark):
    bb = 0
    for i, v in enumerate(board):
        if v == mark:
            bb |= _BITMASK[i]
    return bb


def _heuristic_eval(board, mark, cols=COLS):
    """v2's fork-aware evaluation."""
    opp = 3 - mark
    player_bb = _to_bb(board, mark)
    opp_bb = _to_bb(board, opp)
    empty_bb = ~(player_bb | opp_bb) & ((1 << SIZE) - 1)

    score = 0.0
    threat_cells = [0] * SIZE

    player_threats = opp_threats = 0
    player_block3 = opp_block3 = 0
    player_open2 = opp_open2 = 0

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

        if p_count == 3 and e_count >= 1:
            player_threats += 1
            for bit in range(SIZE):
                if player_in & (1 << bit):
                    threat_cells[bit] += 1
        elif p_count == 3:
            player_block3 += 1

        if o_count == 3 and e_count >= 1:
            opp_threats += 1
            for bit in range(SIZE):
                if opp_in & (1 << bit):
                    threat_cells[bit] -= 1
        elif o_count == 3:
            opp_block3 += 1

        if p_count == 2 and e_count >= 2:
            player_open2 += 1
        if o_count == 2 and e_count >= 2:
            opp_open2 += 1

    score += player_open2 * 100.0 - opp_open2 * 100.0
    score += player_threats * 600.0 - opp_threats * 600.0
    score += player_block3 * 150.0 - opp_block3 * 150.0

    for tc in threat_cells:
        if tc >= 2:
            score += 200.0
        elif tc <= -2:
            score -= 200.0

    return score


# ── NN evaluation ──────────────────────────────────────────────────────────────

def _encode_board(board, mark):
    opp = 3 - mark
    n = ROWS * COLS
    enc = np.zeros(2 * n, dtype=np.float32)
    for i in range(n):
        if board[i] == mark:
            enc[i] = 1.0
        elif board[i] == opp:
            enc[i + n] = 1.0
    return enc


def _nn_evaluate(board, mark, cols=COLS):
    """Evaluate using trained neural network."""
    model = _get_nn_model()
    if model is None:
        return 0.0
    try:
        import torch
        feat = _encode_board(board, mark)
        with torch.no_grad():
            x = torch.from_numpy(feat).to(_nn_device).unsqueeze(0).float()
            return model(x).item()
    except Exception:
        return 0.0


# ── Ensemble evaluation ────────────────────────────────────────────────────────

def _ensemble_eval(board, mark, cols=COLS, w_nn=0.3):
    """Weighted ensemble of v2 heuristic and NN evaluation."""
    h = _heuristic_eval(board, mark, cols)
    n = _nn_evaluate(board, mark, cols)
    return (1 - w_nn) * h + w_nn * n * 5000.0  # Scale NN output to match heuristic range


# ── Transposition table ────────────────────────────────────────────────────────

@dataclass
class TTEntry:
    hash_key: int
    depth: int
    value: float
    flag: int


class TranspositionTable:
    def __init__(self, size=1 << 19):
        self._size = size
        self._table = [None] * size

    def get(self, key, depth):
        entry = self._table[key & (self._size - 1)]
        if entry and entry.hash_key == key and entry.depth >= depth:
            return entry
        return None

    def put(self, key, depth, value, flag):
        self._table[key & (self._size - 1)] = TTEntry(key, depth, value, flag)

    def clear(self):
        self._table = [None] * self._size


TT = TranspositionTable()

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


def _order_moves(board, legal, mark, cols, tt, hash_key, depth, tt_move, killer_list):
    opp = 3 - mark
    current = valid_moves(board, cols)
    current_set = set(current)
    legal = [c for c in legal if c in current_set] or current

    killer_moves = [k for k in killer_list if k >= 0 and k in legal]

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
            rc = (idx // cols, idx % cols)
            is_threat = False
            for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
                cnt = 1
                fr, fc = rc[0]+dr, rc[1]+dc
                while 0 <= fr < ROWS and 0 <= fc < COLS and board[fr*cols+fc] == mark:
                    cnt += 1; fr += dr; fc += dc
                if cnt >= 3 and 0 <= fr < ROWS and 0 <= fc < COLS and board[fr*cols+fc] == 0:
                    is_threat = True; break
                br, bc = rc[0]-dr, rc[1]-dc
                while 0 <= br < ROWS and 0 <= bc < COLS and board[br*cols+bc] == mark:
                    cnt += 1; br -= dr; bc -= dc
                if cnt >= 3 and 0 <= br < ROWS and 0 <= bc < COLS and board[br*cols+bc] == 0:
                    is_threat = True; break
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

def _pvs(board, mark, depth, alpha, beta, cols=COLS,
         tt=None, time_limit=None, counter=None, start_time=None,
         is_root=False, w_nn=0.3):
    legal = valid_moves(board, cols)
    if not legal:
        return 0.0, 0

    if time_limit and start_time and (time.time() - start_time >= time_limit):
        return _heuristic_eval(board, mark, cols), legal[0]

    if counter:
        counter[0] += 1

    hash_key = _zobrist_hash(board)

    for col in legal:
        drop(board, col, mark, ROWS, cols)
        if check_win(board, col, mark, ROWS, cols):
            un_drop(board, col, ROWS, cols)
            if tt:
                tt.put(hash_key, depth, 100000.0, 0)
            return 100000.0, col
        un_drop(board, col, ROWS, cols)

    tt_entry = None
    if tt and not is_root:
        tt_entry = tt.get(hash_key, depth)

    if tt_entry:
        val = tt_entry.value
        if tt_entry.flag == 0: return val, legal[0]
        if tt_entry.flag == 1 and val >= beta: return val, legal[0]
        if tt_entry.flag == 2 and val <= alpha: return val, legal[0]

    if depth <= 0:
        return _ensemble_eval(board, mark, cols, w_nn), legal[0]

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
        score = -_pvs(null_board, mark, depth - 3, -beta, -beta + 1,
                      cols, tt, time_limit, counter, start_time)[0]
        if score >= beta:
            return beta, legal[0]

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
            score, _ = _pvs(board, 3-mark, depth-1, -beta, -alpha,
                           cols, tt, time_limit, counter, start_time)
            score = -score
            first = False
        else:
            score, _ = _pvs(board, 3-mark, depth-1, -alpha-1, -alpha,
                           cols, tt, time_limit, counter, start_time)
            score = -score
            if score > alpha and score < beta:
                score, _ = _pvs(board, 3-mark, depth-1, -beta, -alpha,
                               cols, tt, time_limit, counter, start_time)
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
            if tt:
                tt.put(hash_key, depth, beta, 2)
            break

    if tt:
        flag = 2 if best_score >= beta else (1 if best_score <= alpha else 0)
        tt.put(hash_key, depth, best_score, flag)

    return best_score, best_col


# ── Public API ─────────────────────────────────────────────────────────────────

def bitboard_ab_ensemble_bot(
    board, mark, legal, cols=COLS,
    move_deadline=None, remaining_overage=0.0, seed=None,
) -> int:
    """Alpha-beta with ensemble evaluation (v2 heuristic + NN)."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    time_limit = None
    if move_deadline is not None:
        time_limit = move_deadline

    w_nn = 0.3  # weight for NN evaluation
    if move_deadline and move_deadline < 0.2:
        w_nn = 0.0  # fall back to pure heuristic at very low time

    _clear_killer_history()
    _HISTORY_TABLE[:] = [0] * len(_HISTORY_TABLE)
    TT.clear()

    start_time = time.time()
    best_col = 0
    counter = [0]

    for depth in range(1, 18):
        if time_limit and start_time and (time.time() - start_time >= time_limit):
            break

        legal = valid_moves(board_list, cols)
        if not legal:
            return 0

        _, col = _pvs(list(board_list), mark, depth,
                      float("-inf"), float("inf"),
                      cols, TT, time_limit, counter, start_time,
                      is_root=True, w_nn=w_nn)

        if col not in legal:
            col = legal[0]
        best_col = col

        for r in range(ROWS - 1, -1, -1):
            if board_list[r * cols + best_col] == mark:
                _update_history(best_col, r, depth * 100)
                break

        if time_limit and start_time and (time.time() - start_time >= time_limit):
            break

    return best_col if best_col in legal else legal[0]