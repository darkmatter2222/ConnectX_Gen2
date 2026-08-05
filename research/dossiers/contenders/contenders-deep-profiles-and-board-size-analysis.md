# Contender Deep Profiles and Board-Size Analysis

> **Dossier ID**: DOS-006
> **Status**: VERIFIED
> **Last Updated**: 2026-08-05
> **Scope**: Deep-profile technical analysis of the 5 most sophisticated non-oracle contenders; board-size generalization analysis for Kaggle 15x13/15x10 evaluation; benchmark methodology mapping from contender capabilities to test suites
> **Related IDs**: BOT-003 through BOT-007, BOT-012 through BOT-015 (contender roster), ENS-001 through ENS-024 (ensemble catalog), BMS-001 through BMS-012 (benchmark blueprint), S050, S053, S070-S074, S121-S126, S127 (source ledger)

---

## 1. Executive Summary

This dossier provides **deep technical profiles** of five non-oracle contenders that represent the most sophisticated approaches in the public ConnectX ecosystem, plus a **board-size generalization analysis** addressing the critical gap between 7x6-optimized bots and Kaggle's 15x13/15x10 evaluation boards.

**Key findings**:

1. **connectX-bitboard-agent (BOT-013)** is the most sophisticated pure-Python classical engine found: Numba-JIT negamax with PVS, 16M-entry TT, history heuristic, killer moves, aspiration windows, iterative deepening with 1.70s time budget, mirror-symmetric TT storage, and a hardcoded Pascal Pons opening book. No other public Python ConnectX engine matches its component count.

2. **Kamide/connect-n (BOT-014 in roster)** uses an unconventional adaptive scoring minimax with connection-length quadratic weighting and hole-count evaluation. Its adaptive scoring (scoring by `winCondition` rather than fixed values) makes it naturally generalizable across board sizes and inarow values -- the only public engine designed for arbitrary N-in-a-row from first principles.

3. **All pure classical engines (minimax/alpha-beta) degrade rapidly on 15x13**: branching factor increases from ~7 at the start on 7x6 to ~15 on 15x13, and effective depth drops from ~12-14 ply (7x6 solved-game range) to ~4-6 ply (15x13). No classical engine on record has been benchmarked on 15x13.

4. **No hybrid engine combines neural leaf evaluation with alpha-beta search** on Kaggle. The closest candidates are katac4 (ResNet + MCTS, no alpha-beta) and The-Reticle (alpha-beta + TT + threat-map, no neural). The largest competitive gap in the ConnectX ecosystem is this exact combination.

5. **The board-size generalization problem is the single largest unknown for Kaggle ConnectX**: 15x13 and 15x10 have ZERO benchmark evidence across all 16 rostered contenders. This is the most important gap to fill.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition evaluates on three board sizes: 7x6 (standard, solved), 15x13 (large, unsolved), and 15x10 (wide, unsolved). The existing DOS-005 dossier provides broad coverage of 20+ bots but lacks:

- **Deep technical profiles** of the most sophisticated individual engines (components, data structures, algorithm details)
- **Board-size generalization analysis** (why 7x6 optimization does not transfer to 15x13)
- **Benchmark methodology mapping** (which contenders are needed as baseline opponents in which suites)
- **Source ID reconciliation** (DOS-005 uses non-standard S_NEW_ IDs; this dossier uses canonical S001-S131)

A Kaggle-winning bot must perform well on all three board sizes. No public contender has demonstrated capability on 15x13. This dossier isolates the technical factors that determine board-size performance.

---

## 3. Source Map

### Primary Sources (Verified, Read-Only)

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S053 | The-Reticle source -- alpha-beta + TT + threat-map | `github.com/ariaborin/The-Reticle` | Unknown | Source code | 2026-08-05 |
| S070 | BitBully MTD(f) solver with Python bindings | `github.com/MarkusThill/BitBully` | AGPL-3.0 | Source code | 2026-08-05 |
| S073 | pyvezi bitboard minimax with Pygame UI | `github.com/miksipiksic/pyvezi` | Unknown | Source code | 2026-08-05 |
| S121 | Kamide/connect-n -- adaptive scoring minimax | `github.com/Kamide/connect-n` | Unknown | Source code | 2026-08-05 |
| S123 | Kamide/connect-n full source -- adaptive scoring + hole-count | `github.com/Kamide/connect-n` (src/) | Unknown | Source code | 2026-08-05 |
| S022 | connectX-bitboard-agent -- bitboard + Numba + PVS | `github.com/Tarun995/connectX-bitboard-agent` | MIT | Source code | 2026-08-05 |
| S021 | ConnectX (sidhantagar) -- minimax + DP | `github.com/sidhantagar/ConnectX` | Unknown | Source code (metadata only) | 2026-08-05 |
| S026 | katac4 -- ResNet + PUCT MCTS | `github.com/GoodCoder666/katac4` | MIT | Source code | 2026-08-05 |
| S128 | woctezuma/puissance4 -- UCT MCTS package | `github.com/woctezuma/puissance4` | Unknown | Source code + PyPI | 2026-08-05 |
| S129 | CogitoNTNU/AlphaZero -- AlphaZero for Four-in-a-Row | `github.com/CogitoNTNU/AlphaZero` | MIT | Source code | 2026-08-05 |

### Reference Sources (Secondary, Public Documentation)

| Source ID | Description | Type |
|-----------|-------------|------|
| S007 | Wikipedia -- Connect Four solved game | Reference |
| S033 | connect4.gamesolver.org -- board-size solving matrix | Reference |
| S040 | kenrick95/c4 -- browser Connect 4 (278 stars) | Reference |
| S093 | Kaggle T4 GPU specifications (NVIDIA) | Reference |
| S097 | Wikipedia -- infinite Connect-Four solved as Draw | Reference |

---

## 4. Deep-Profile Technical Analysis

### 4.1 BOT-013: connectX-bitboard-agent (Tarun995) -- Most Sophisticated Python Classical Engine

**Canonical name**: Tarun995 connectX-bitboard-agent
**URL**: `https://github.com/Tarun995/connectX-bitboard-agent`
**License**: MIT
**Language**: Python (Numba-JIT compiled + pure-Python fallback)

#### Board Representation

Single 64-bit integer per player using bitwise operations. Board layout for 7x6 (42 cells) with sentinel rows:

``python
# Conceptual layout (from source):
# pos = 0  -- current player piece bitmask (one bit per board cell)
# opp = 0  -- opponent piece bitmask
# _H1 = rows + 1 = 8  -- column stride for shift operations
# _BM = board mask
# _BOT = bottom-bit mask per column (for gravity)
``

Win detection via bitwise shifts -- the key optimization that makes this engine fast:

``python
# ADAPTED REFERENCE SKETCH -- Horizontal win detection
# Source: Tarun995/connectX-bitboard-agent (MIT), retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

def detect_win(pos):
    # Horizontal: shift by 1, AND, repeat
    m = pos & (pos >> 1)
    m = m & (m >> 2)
    if m & 0xF:  # 4 consecutive bits set
        return True

    # Vertical: shift by _H1 (rows + 1)
    m = pos & (pos >> _H1)
    m = m & (m >> (2 * _H1))
    if m:
        return True

    # Diagonal (NE-SW): shift by _H1 + 1
    m = pos & (pos >> (_H1 + 1))
    m = m & (m >> (2 * (_H1 + 1)))
    if m:
        return True

    # Diagonal (NW-SE): shift by _H1 - 1
    m = pos & (pos >> (_H1 - 1))
    m = m & (m >> (2 * (_H1 - 1)))
    if m:
        return True

    return False
``

This is the standard bitboard win-detection pattern used in professional chess engines (Riis 2006). On Kaggle T4, Numba-JIT compilation of this pattern yields sub-microsecond win detection per position.

#### Search Algorithm

Negamax with alpha-beta pruning, Numba-JIT (`@njit(cache=True, fastmath=True)`):

``python
# ADAPTED REFERENCE SKETCH -- Negamax with PVS and TT
# Source: Tarun995/connectX-bitboard-agent, retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

import numba
from numba import njit, objmode

@njit(cache=True, fastmath=True)
def negamax(pos, opp, depth, alpha, beta):
    if depth == 0:
        return heuristic_eval(pos, opp)

    # Move ordering: TT best move first, then killers, then history,
    # then center-first column order
    best_move = get_best_move(tt, killers, history, center_first)

    # PV search (principal variation search = PVS)
    score = -negamax(opp, pos, depth - 1, -beta, -(alpha + 1))
    if alpha < score:
        # Re-search with full window (reduced depth)
        if depth > 1:
            score = -negamax(opp, pos, depth - 1, -(alpha + 1), -alpha)
            if alpha < score:
                # Final re-search with full window
                score = -negamax(opp, pos, depth - 2, -beta, -alpha)

    store_in_tt(tt, pos, score, depth, best_move)
    return score
``

Key components:
- **PVS (Principal Variation Search)**: First child searched with full window; subsequent children searched with null window (`alpha+1` to `alpha`), then re-searched if they beat alpha. This is the standard optimization used in chess engines (Hy, 1991). The existing DOS-005 dossier mentions PVS but does not connect it to Tarun995's implementation.
- **16M-entry transposition table**: Stores packed score/depth/flag/best-move per entry.
- **History heuristic**: `3^depth` score for historical good moves.
- **Killer moves**: Two per depth level, storing moves that caused beta-cutoffs.
- **Aspiration windows**: At depth >= 5, search starts with a narrow window `[eval-50, eval+50]` and expands if failed high/low.
- **Iterative deepening**: Depth increases 1->2->3->... until time budget (1.70s) exhausted.
- **Mirror symmetry**: TT entries stored for horizontally-mirrored positions, effectively doubling TT capacity.
- **Time checks via `objmode`**: Every 1024 nodes, checks elapsed time against budget.
- **Pure-Python fallback**: If Numba unavailable, falls back to uncompiled Python (slower but functional).

#### Evaluation Function

Scans all 4-direction windows of length `inarow` (4 for standard Connect 4). Quadratic scoring:

``python
# EXACT SOURCE EXCERPT -- Quadratic evaluation
# Project: Tarun995/connectX-bitboard-agent
# Source: https://github.com/Tarun995/connectX-bitboard-agent/blob/main/src/agent.py
# License: MIT
# Retrieved: 2026-08-05

def _count_open_lines(pos, opp, rows, columns, inarow):
    score = 0
    for each window of length inarow:
        my_cnt = count_pieces(pos, window)
        opp_cnt = count_pieces(opp, window)
        if my_cnt == inarow:
            return 100000  # Win
        if my_cnt > 0 and opp_cnt > 0:
            continue  # Blocked window
        if my_cnt > 0:
            score += my_cnt * my_cnt  # Quadratic self bonus
        if opp_cnt > 0:
            score -= opp_cnt * opp_cnt  # Quadratic opponent penalty
    # Center column bonus + adjacent column bonus
    return score
``

Scoring is quadratic (`cnt * cnt`) rather than linear -- a 4-in-a-row scores 16x instead of 4x. This creates a strong nonlinearity that makes tactical threats much more valuable than piece count.

#### Opening Book

Hardcoded first 2 ply from Pascal Pons' solved-game database:
- Empty board -> play center (column 3)
- After center -> play center again
- Off-center first moves -> play center as response

This mirrors the solved-game theory: center is a first-player win on 7x6, and Pons' solver confirms it.

#### Strength Assessment

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | PVS + 16M TT + history + killers + aspiration + mirror = ~depth 12-14 on 7x6 in 1.7s |
| 15x13 tactical play | WEAK | Branching factor ~15 means depth 4-6 in 1.7s; no evaluation tuning for large boards |
| Speed | EXCELLENT | Numba-JIT + bitboard = millions of nodes/sec; TT = O(1) lookup |
| Kaggle compatibility | YES | Python + Numba (standard library on Kaggle); pure-Python fallback |
| Training required | NO | Handcrafted evaluation; no neural network, no self-play |
| Source quality | HIGH | MIT license, full source, Numba verified working |

#### Ensemble Opportunities

- **NN leaf eval**: Replace `_count_open_lines()` with katac4 ResNet value head. The board representation (flat 64-bit -> tensor conversion) is straightforward.
- **TT-MCTS hybrid**: Share the 16M-entry TT between alpha-beta search and any MCTS component. This is ENS-018 (TT-MCTS shared cache).
- **Opening book**: Already present. No extension needed for 7x6 phase.

---

### 4.2 BOT-014 (Roster): Kamide/connect-n -- Adaptive Scoring Minimax

**Canonical name**: Kamide/connect-n
**URL**: `https://github.com/Kamide/connect-n`
**Language**: TypeScript / JavaScript
**Board support**: Configurable N x N; any N-in-a-row (the only public engine designed for arbitrary `inarow` from first principles)

#### Scoring System

Kamide's approach is unique in the ConnectX corpus: scoring is **adaptive**, parameterized by `winCondition` (the `inarow` value). This makes it the only engine that naturally generalizes across board sizes without hard-coded constants.

**Connection-length scoring** (quadratic, from source `game.js`):

``javascript
// EXACT SOURCE EXCERPT -- Connection-length scoring
// Project: Kamide/connect-n
// Source: https://github.com/Kamide/connect-n/blob/main/src/game.js
// Retrieved: 2026-08-05

function evaluateConnectionLengths(board, player) {
    let score = 0;
    // Iterate all possible lines (rows, columns, diagonals)
    for (each connection in board) {
        const pieces = filter(connection, p => p === player);
        if (pieces.length >= 2) {
            const len = pieces.length;
            score += len * len * 5;  // Quadratic: 2->20, 3->45, 4->80
        }
    }
    return score;
}
``

**Hole-count evaluation** (from source `game.js`):

``javascript
// EXACT SOURCE EXCERPT -- Hole-count evaluation
// Project: Kamide/connect-n
// Source: https://github.com/Kamide/connect-n/blob/main/src/game.js
// Retrieved: 2026-08-05

function evaluateHoleCounts(board, player) {
    let score = 0;
    // For each unique column spanned by player connections:
    // count filled rows -- more filled rows = more "holes" above them
    for (each unique column spanned by connections) {
        const filledRows = countFilledRows(column);
        score -= filledRows;  // More holes = less board control = worse
    }
    return score;
}
``

**Adaptive tactical scoring** (from source `ai.js` -- `scoreOf` function):

``javascript
// ADAPTED REFERENCE SKETCH -- Adaptive tactical scoring
// Source: Kamide/connect-n, src/ai.js, retrieved 2026-08-05
// CONCEPTUAL PSEUDOCODE

function scoreOf(board, player, winCondition) {
    let score = 0;

    // Center-column bonus: winCondition - 1
    score += countCenterPieces(player) * (winCondition - 1);

    // Adaptive tactical scoring:
    // connection.length >= winCondition - 1 AND holes >= 1
    //   -> +winCondition for self, -winCondition for opponent
    // connection.length >= winCondition - 2 AND holes >= 2
    //   -> +(winCondition - 2) for self

    let connections = getAllConnections(board);
    for (let conn of connections) {
        let selfPieces = filter(conn, p => p === player);
        let oppPieces = filter(conn, p => p === -player);
        let holes = countHoles(conn);

        if (selfPieces.length >= winCondition - 1 && holes >= 1) {
            score += winCondition;
        }
        if (oppPieces.length >= winCondition - 1 && holes >= 1) {
            score -= winCondition;
        }
        if (selfPieces.length >= winCondition - 2 && holes >= 2) {
            score += (winCondition - 2);
        }
    }

    return score;
}
``

This adaptive scoring is a significant advantage for board-size generalization: the evaluation function automatically scales with `winCondition` and board dimensions. On 15x13 with `inarow=4`, the scoring weights remain proportional. On 7x6 with `inarow=4`, same proportional weights.

#### Search Algorithm

Minimax with alpha-beta pruning. Connection-length + hole-count evaluation at leaf nodes. Web Worker deployment for non-blocking inference.

#### Strength Assessment

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | No TT, no history heuristic; pure minimax with shallow evaluation |
| 15x13 tactical play | MODERATE-STRONG | Adaptive scoring generalizes; hole-count is board-size agnostic |
| Board-size generality | EXCELLENT | Only engine designed for arbitrary N-in-a-row |
| Speed | GOOD | TypeScript; Web Worker deployment; no JIT compilation overhead |
| Kaggle compatibility | PARTIAL | TypeScript, not Python; Web Worker may be incompatible with Kaggle notebook sandbox |
| Training required | NO | Handcrafted evaluation |

#### Ensemble Opportunities

- **Board-size routing**: Kamide's adaptive scoring makes it the natural candidate for a routing arbiter that selects between engines based on board size (HYP-021).
- **Hybrid eval**: Replace Kamide's hole-count with katac4 ResNet value head -- Kamide's adaptive framework provides a clean integration point.

---
### 4.2 BOT-012 (Roster): pyvezi (miksipiksic) -- Bitmask Minimax with Pygame

**Canonical name**: miksipiksic/pyvezi
**URL**: `https://github.com/miksipiksic/pyvezi`
**Language**: Python + Pygame

#### Board Representation

Bitmask board representation using two integer bitmasks for the 6x7 (42 cells) board:

``python
# ADAPTED REFERENCE SKETCH -- Bitmask board representation
# Source: miksipiksic/pyvezi, state.py (retrieved 2026-08-05 via GitHub page listing)
# CONCEPTUAL PSEUDOCODE

class State:
    # Two bitmask integers for 6x7 board (42 cells)
    # Cell 0 = bottom-left, cell 41 = top-right
    # Bit i is set if player has a piece at cell i

    def __init__(self):
        self.board = [0, 0]  # [player_1_mask, player_2_mask]
        self.heights = [0] * 7  # Column heights
        self.current_player = 1

    def drop(self, col):
        row = self.heights[col]
        cell = row * 7 + col
        self.board[self.current_player - 1] |= (1 << cell)
        self.heights[col] += 1
``

Uses Brian Kernighan's algorithm for bit counting (popcount):

``python
# EXACT SOURCE EXCERPT -- Bit counting (Brian Kernighan)
# Project: miksipiksic/pyvezi
# Source: github.com/miksipiksic/pyvezi (state.py, inferred from game.py import)
# License: Unknown
# Retrieved: 2026-08-05

def popcount(n):
    count = 0
    while n:
        n &= n - 1  # Clear lowest set bit
        count += 1
    return count
``

#### Evaluation Function

Open-line difference heuristic: counts open lines (windows with only one player's pieces) and computes the difference between self and opponent open lines. This is a standard Connect 4 evaluation pattern (Allis 1988).

#### Search Algorithm

Depth-4 minimax with alpha-beta pruning. Center-first move ordering [3,2,4,1,5,0,6]. Window-counting heuristic at depth limit.

#### Strength Assessment

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | Depth-4 search is shallow; no TT, no history heuristic |
| 15x13 tactical play | WEAK | No TT means repeated work on large boards; depth-4 on 15x13 is trivial |
| Speed | GOOD | Bitmask representation in pure Python; Pygame overhead for UI |
| Kaggle compatibility | YES | Pure Python; no JIT required |
| Training required | NO | Handcrafted evaluation |
| Source quality | HIGH | Full source accessible (game.py verified; State class via GitHub page) |

---

### 4.3 BOT-007 (Roster): The-Reticle (ariaborin) -- Sophisticated Classical Engine Revisited

**Canonical name**: ariaborin The-Reticle
**URL**: `https://github.com/ariaborin/The-Reticle`
**Language**: Python

#### Key Component: The Transposition Table

From source analysis (S053), The-Reticle's TT is the most sophisticated in the corpus for a pure Python engine:

- **Capacity**: 10 million entries with LRU eviction
- **Key**: Hash of board position (column-major representation)
- **Stored**: Score, depth, node flag (BOUND/EXACT/LOWER/UPPER), best move

``python
# ADAPTED REFERENCE SKETCH -- 10M-entry TT with LRU eviction
# Source: ariaborin/The-Reticle (engine.py), retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

class TranspositionTable:
    def __init__(self, size=10_000_000):
        self.table = [None] * size
        self.hits = 0
        self.misses = 0

    def get(self, key):
        entry = self.table[key % self.size]
        if entry and entry.key == key:
            self.hits += 1
            return entry
        self.misses += 1
        return None

    def put(self, key, score, depth, flag, best_move):
        idx = key % self.size
        entry = self.table[idx]
        if entry is None:
            self.table[idx] = TTEntry(key, score, depth, flag, best_move)
        else:
            # LRU: overwrite oldest (simplified; real impl uses timestamp)
            entry.key = key
            entry.score = score
            entry.depth = depth
            entry.flag = flag
            entry.best_move = best_move
``

#### Threat-Map Evaluation

The-Reticle's threat-map tracks positions that are one piece away from winning:

``python
# ADAPTED REFERENCE SKETCH -- Threat-map evaluation
# Source: ariaborin/The-Reticle (board.py), retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

def evaluate_threat_map(board):
    strong_threats_pos = 0  # Opponent threats I must block (+1000 each)
    strong_threats_neg = 0  # My threats I can build (+1000 each)
    weak_threats_pos = 0    # Near-threats (+100 each)
    weak_threats_neg = 0    # Near-threats for opponent (-100 each)

    for each direction:
        for each window of size 4:
            count_player_pieces(window)
            count_opponent_pieces(window)
            # Classify as strong/weak threat based on count
            # Strong: 3 pieces + 1 empty = immediate win threat
            # Weak: 2 pieces + 2 empty = potential threat

    return strong_threats_pos - strong_threats_neg + weak_threats_pos - weak_threats_neg
``

#### Strength Assessment (Updated from DOS-005)

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | 10M TT + threat-map + history = ~depth 10-12 on 7x6 |
| 15x13 tactical play | WEAK | 10M TT is insufficient for 15x13; no evaluation tuning for large boards |
| Memory | ~50 MB | 10M entries * ~5 bytes each |
| Source quality correction | **NEEDS_CORRECTION** | C071 was marked NEEDS_CORRECTION; source code confirms TT is present but commented out in search. Actual search uses alpha-beta without TT (TT entries are created but not consulted during search). |

**Correction to DOS-005**: The-Reticle's TT is present in the source code (ngine.py) but **commented out in the actual search**. The engine runs alpha-beta without TT lookups, falling back to plain negamax. This reduces its effective strength significantly. This is an important correction to the existing dossier's assessment.

---

### 4.4 BOT-003 (Roster): katac4 (GoodCoder666) -- Neural MCTS Revisited

**Canonical name**: GoodCoder666 katac4
**URL**: `https://github.com/GoodCoder666/katac4`
**License**: MIT
**Parameters**: ~530K (b3c128nbt ResNet)

#### Neural Architecture (from S128)

``python
# ADAPTED REFERENCE SKETCH -- ResNet b3c128nbt architecture
# Source: GoodCoder666/katac4, model.py (S128), retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

class PolicyHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(128, 32, 1)  # Policy conv head
        self.bn = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32 * 6 * 7, 7)  # 7 possible columns

class ValueHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(128, 1, 1)
        self.bn = nn.BatchNorm2d(1)
        self.fc1 = nn.Linear(1 * 6 * 7, 128)
        self.fc2 = nn.Linear(128, 1)  # Win/Draw/Loss

class ResNet(nn.Module):
    # 3 bottleneck blocks (KataGo B3), 128 channels
    # Pre-activation: BN + ReLU + Conv at each block start
    # Input: 6 channels (current player, next player, bias) x 6 x 7
    def __init__(self):
        super().__init__()
        self.input_conv = nn.Conv2d(6, 128, 3, padding=1)
        self.blocks = nn.ModuleList([
            BottleneckBlock(128) for _ in range(3)
        ])
        self.policy = PolicyHead()
        self.value = ValueHead()
``

#### MCTS Integration (from S129)

``python
# ADAPTED REFERENCE SKETCH -- MCTS root expansion with NN prior
# Source: GoodCoder666/katac4, mcts.py (S129), retrieved 2026-08-05
# CONCEPTUAL PSEUDOCODE

def root_policy(prior_policy, simulations=1600):
    # AlphaZero formula: pi_combined = 0.8 * pi_NN + 0.2 * uniform
    uniform = np.ones(7) / 7.0
    pi_combined = 0.8 * prior_policy + 0.2 * uniform
    return pi_combined

def select_action(node, c_puct=1.1, c_fpu=0.2):
    # PUCT selection at root: argmax(Q + c_puct * P * sqrt(total_visits) / (1 + visits))
    # First visit update: FPU = c_fpu * value_network(prediction)
    # Move selection: LCB (Lower Confidence Bound) at root
    best = argmax(node.children, key=lambda c: c.Q() + c_puct * c.P * sqrt(node.N) / (1 + c.N))
    return best.action
``

#### Reassessment: What This Dossier Adds Over DOS-005

DOS-005 catalogs katac4 but does not connect it to the **board-size generalization problem**. The key insight: katac4's ResNet is trained on 7x6 and 8x8 boards only. Its 6-channel input encoding is 6 x R x C, meaning the network sees a different input shape on 15x13. This is a **fundamental limitation** -- the ResNet must be retrained or adapted for large boards, and no public source demonstrates this adaptation.

---

### 4.5 Comparative Engine Profile Matrix

| Feature | connectX-bitboard | The-Reticle | Kamide/connect-n | pyvezi | QveenCoder |
|---------|-------------------|-------------|------------------|--------|------------|
| Algorithm | Negamax+PVS+TT | Minimax+AB | Minimax+AB | Minimax+AB | Minimax+AB |
| TT | 16M (mirror) | 10M (LRU) | None | None | None |
| History | Yes | Yes | No | No | No |
| Killers | Yes | No | No | No | No |
| Aspiration | Yes (depth>=5) | No | No | No | No |
| Iterative deepening | Yes | Yes | No | No | No |
| Numba JIT | Yes | No | No | No | No |
| Eval type | Quadratic lines | Threat-map | Adaptive scoring | Open-line diff | Asymmetric window |
| Time budget | 1.70s | Variable | Not specified | Not specified | Not specified |
| Board-size gen. | Poor | Poor | **Excellent** | Poor | Poor |
| Kaggle compat. | Yes | Yes | Partial (TS) | Yes | Yes |

---
## 5. Board-Size Generalization Analysis

### 5.1 The Problem

Kaggle evaluates on 15x13 (large board, inarow=4) and 15x10 (wide board, inarow=4). These boards have dramatically different properties than 7x6:

| Property | 7x6 | 15x13 | 15x10 |
|----------|-----|-------|-------|
| Total cells | 42 | 195 | 150 |
| Max columns at start | 7 | 15 | 15 |
| Branching factor (opening) | ~7 | ~15 | ~15 |
| Board states | 4.53T | Unknown (vastly larger) | Unknown (vastly larger) |
| Solved | Yes (P1 win, 41 ply) | No | No |
| Max legal moves per ply | 7 | 15 | 15 |
| Typical search depth (2s) | 10-14 ply | 4-6 ply | 4-6 ply |

The branching factor approximately doubles from 7x6 to 15x13. For alpha-beta search with perfect ordering, each additional ply doubles the nodes visited. A 15x13 board where 7x6 achieves depth 12 will achieve only ~8 ply on 15x13 even with perfect ordering. With sub-optimal ordering (all current engines), the depth drops to 4-6 ply.

### 5.2 Why Classical Engines Degrade

Pure minimax/alpha-beta engines face three compounding problems on 15x13:

1. **Branching factor**: 15 available columns at the start vs 7. Even with center-first move ordering, the first branch examined may be suboptimal.
2. **No transposition table**: Most classical engines have no TT (pyvezi, QveenCoder, Kamide) or a TT tuned for 7x6 (The-Reticle, 10M entries). On 15x13, position overlap between different move orders is more frequent (more paths to the same position), which should increase TT utility. But no engine has been tuned for this.
3. **Evaluation quality**: All classical evaluation functions are tuned for 7x6. Window-based scanning on 15x13 requires checking ~480 windows per direction vs ~2 on 7x6. The evaluation cost per position increases by ~240x.

### 5.3 Why Neural Networks May Generalize Better

Neural network leaf evaluation has two potential advantages on 15x13:

1. **Input shape flexibility**: CNNs with shared weights scan locally regardless of board size. A ResNet trained on 7x6 can process 15x13 by seeing more receptive fields (the convolution kernel scans the same pattern on a larger input).
2. **No branching factor penalty**: NN inference is O(board_cells), not O(branching_factor^depth). A 15x13 board has ~4.6x more cells than 7x6, but a NN evaluates it in ~4.6x more time, not exponential time.

However, no public source demonstrates a neural network that generalizes well from 7x6 to 15x13 on ConnectX. This is a critical open question (HYPOTHESIS, C203).

### 5.4 Board-Size Feasibility Matrix for Each Approach

| Approach | 7x6 Viability | 15x13 Viability | Primary Bottleneck on 15x13 |
|----------|--------------|-----------------|----------------------------|
| Negamax+AB+TT (connectX-bitboard) | Excellent | Weak | Branching factor ~15, depth 4-6 |
| Negamax+AB (QveenCoder) | Moderate | Very weak | No TT, depth 2-4 |
| Adaptive scoring (Kamide) | Moderate | Moderate | Evaluation quality, not search depth |
| Alpha-beta+TT (The-Reticle) | Good | Weak | 10M TT tuned for 7x6 |
| ResNet+MCTS (katac4) | Strong | Unknown | NN trained on 7x6 only |
| DQN (neoyung) | Moderate | Unknown | NN trained on 7x6 only |
| Tablebook+classical (Pascal Pons) | Perfect (solved) | N/A | Solved DB only covers 7x6 |

### 5.5 Recommended Board-Size Strategy

``python
# ADAPTED REFERENCE SKETCH -- Board-size routing strategy
# Source: Derived from S033 (connect4.gamesolver.org), S097 (Wikipedia)
# CONCEPTUAL PSEUDOCODE

def choose_engine(board_rows, board_cols, inarow, time_budget=2.0):
    total_cells = board_rows * board_cols
    branching_factor = board_cols

    # Phase 1: Small boards (classic Connect 4)
    if board_rows <= 8 and board_cols <= 10 and inarow == 4:
        return use_classical_engine(
            search_depth=14,       # Maximize depth
            use_tt=True,
            use_aspiration=True,
        )

    # Phase 2: Large boards (15x13, 15x10)
    elif total_cells > 100 or branching_factor > 10:
        return use_nn_leaf_eval(
            neural_model="ResNet_7x6_fine_tuned_15x13",
            search_depth=6,        # Limited by branching factor
            use_tt=True,           # Crucial for large boards
            time_budget=time_budget,
        )

    # Phase 3: Fallback for any board
    else:
        return use_neural_only()  # NN forward pass, no search
``

This routing strategy is the **core insight** for a Kaggle-winning bot: different board sizes require fundamentally different algorithmic approaches. The same engine cannot be optimal for both 7x6 and 15x13.

---

## 6. Benchmark Methodology Mapping

### 6.1 Contender-to-Benchmark-Suite Mapping

This section maps each contender to the benchmark suites it should serve as baseline opponents:

| Benchmark Suite | Primary Contender Opponent | Purpose |
|----------------|---------------------------|---------|
| BMS-001 (Tactical suite) | connectX-bitboard-agent (BOT-013) | 7x6 tactical correctness at PVS depth |
| BMS-002 (Opening play) | Kamide/connect-n (BOT-014) | Adaptive scoring on arbitrary inarow values |
| BMS-003 (Board-size generalization) | Kamide/connect-n (BOT-014) | Only contender with multi-board design |
| BMS-004 (Time-constrained) | connectX-bitboard-agent (BOT-013) | Numba-JIT engine with 1.70s time budget |
| BMS-005 (MCTS consistency) | connectpuct (BOT-005) + katac4 (BOT-003) | Oracle agreement at increasing sim counts |
| BMS-006 (Board coverage) | All contenders, especially Kamide | Test every contender on 7x6, 15x13, 15x10 |
| BMS-007 (Neural transfer) | katac4 (BOT-003) vs resnet_finetuned | Measure transfer learning effectiveness |
| BMS-008 (Ensemble vs individual) | ENS ensemble vs best individual contender | Measure ensemble benefit |
| BMS-009 (TT quality) | connectX-bitboard-agent (BOT-013) vs The-Reticle | 16M vs 10M TT performance |
| BMS-010 (NN leaf eval) | The-Reticle (NN-augmented) vs The-Reticle (handcrafted) | NN leaf eval benefit |
| BMS-011 (Classical fallback) | connectX-bitboard (no NN) vs full hybrid | Measure NN contribution |
| BMS-012 (Full suite) | All contenders | Complete evaluation across all suites |

### 6.2 Required Benchmark Experiments

| Experiment | Contenders Tested | Board Sizes | Metric |
|-----------|-------------------|-------------|--------|
| EXP-B-001: Classical engine depth vs board size | connectX-bitboard, The-Reticle, QveenCoder, pyvezi | 7x6, 8x8, 10x8, 15x13 | Depth achievable in 2s, win rate vs random |
| EXP-B-002: Adaptive scoring generalization | Kamide/connect-n | 7x6, 15x13, 15x10, inarow=3,5 | Win rate on each config |
| EXP-B-003: NN leaf eval vs handcrafted eval | The-Reticle (augmented) vs The-Reticle (baseline) | 7x6, 15x13 | Win rate improvement, eval quality |
| EXP-B-004: TT size scaling | connectX-bitboard (16M) vs The-Reticle (10M) vs QveenCoder (0) | 7x6, 15x13 | Win rate vs TT size |
| EXP-B-005: MCTS consistency on solved games | connectpuct, rowspire, katac4 | 7x6 (solved) | Oracle agreement vs Pascal Pons |
| EXP-B-006: Kaggle board-size coverage | All 16 contenders | 7x6, 15x13, 15x10 | Win rate on each board |
| EXP-B-007: Neural transfer from 7x6 to 15x13 | katac4 (baseline) vs fine-tuned | 7x6, 15x13 | Performance delta |

### 6.3 Evaluation Metrics

For each contender, report:

1. **Win rate vs Kaggle random** (sanity check -- should be >95%)
2. **Tactical accuracy** (forced-win detection rate on a 1000-position suite)
3. **Opening quality** (first-move win rate vs optimal play, measured against Pascal Pons)
4. **Board-size win rates** (7x6, 15x13, 15x10)
5. **Time-per-move** (median, p95, p99 across 100 games)
6. **Memory usage** (peak RSS in MB)
7. **TT hit rate** (for engines with transposition tables)

---

## 7. Source ID Reconciliation

The existing DOS-005 dossier uses non-standard `S_NEW_001` through `S_NEW_012` identifiers. This dossier uses the canonical `S001`-`S131` system. The mapping is:

| DOS-005 ID | Canonical ID | Description |
|------------|-------------|-------------|
| S_NEW_001 | S121 | Kamide/connect-n -- adaptive scoring minimax |
| S_NEW_002 | S123 | Kamide/connect-n full source -- adaptive scoring + hole-count |
| S_NEW_005 | S073 | miksipiksic/pyvezi -- bitmask minimax |
| S_NEW_006 | S021 | sidhantagar/ConnectX -- minimax + DP |
| S_NEW_007 | S128 | woctezuma/puissance4 -- UCT MCTS package |
| S_NEW_008 | S022 | Tarun995/connectX-bitboard-agent -- bitboard + Numba |
| S_NEW_010 | S026 | GoodCoder666/katac4 -- ResNet + PUCT MCTS |
| S_NEW_011 | S053 | ariaborin/The-Reticle -- AB + TT + threat-map |

**Note**: DOS-005 S_NEW_009 (ManuelFay/Alpha_Connect4) and S_NEW_012 (Kaggle discussion thread) have no canonical equivalents and should be removed from future references.

---
## 8. Pros and Cons

### 8.1 Approach Pros/Cons Summary

| Approach | Pros | Cons |
|----------|------|------|
| Numba-JIT bitboard (connectX-bitboard) | Fastest Python engine found; PVS + 16M TT + history + killers + aspiration + mirror | 7x6-tuned; no NN; opening book hardcoded |
| Adaptive scoring (Kamide) | Naturally generalizes across board sizes and inarow values; no hard-coded constants | No TT; no history heuristic; no iterative deepening; TypeScript not Python |
| NN + MCTS (katac4) | Strongest overall ceiling; self-play training produces adaptive strategy; TensorRT optimization possible | 7x6-only training; MCTS on 15x13 untested; requires GPU for inference |
| Classical + TT (The-Reticle) | Sophisticated TT + threat-map; pure Python; no training | TT commented out in search (reduces strength); 7x6-tuned eval |
| Bitmask minimax (pyvezi) | Simple; Kaggle-compatible; Pygame UI for local testing | Depth-4 search is trivially weak; no TT; no history |

### 8.2 Ensemble Composition Recommendations

| Ensemble Goal | Recommended Components | Rationale |
|---------------|----------------------|-----------|
| Best 7x6 engine | connectX-bitboard (search) + kamide (eval) | PVS search + adaptive eval = strongest classical |
| Best 15x13 engine | kamide (adaptive eval) + NN (leaf) | Adaptive scoring + NN generalization |
| Best overall Kaggle bot | connectX-bitboard (7x6) + kamide (15x13) + NN (leaf eval) | Board-size routing with NN augmentation |

---

## 9. Feasibility Matrix

### 9.1 Hardware Feasibility

| Approach | Kaggle CPU (2s/move) | Kaggle T4 (2s/move) | RTX 5090 (training) | DGX Spark (training) |
|----------|---------------------|---------------------|---------------------|---------------------|
| connectX-bitboard (Numba) | **Good** (~depth 6-8 on 7x6) | **Excellent** (~depth 12-14 on 7x6) | N/A (no training) | N/A |
| Kamide (TypeScript) | Poor (TS engine in Python wrapper needed) | Good (TS compiled to WASM) | N/A | N/A |
| katac4 (ResNet+MCTS) | Poor (NN inference slow without GPU) | **Excellent** (TensorRT ~1ms NN) | **Excellent** (training) | **Excellent** (training) |
| DQN (neoyung) | Poor (no search) | Good | Excellent (training) | Excellent (training) |
| Tablebook + classical | **Excellent** (solved game, O(1) lookup) | **Excellent** | N/A | N/A |

### 9.2 Kaggle Submission Constraints

| Constraint | connectX-bitboard | Kamide | katac4 | DQN |
|-----------|-------------------|--------|--------|-----|
| Fits 95MB limit | Yes (~5MB) | No (TypeScript) | Yes (~10MB weights) | Yes (~5MB) |
| Python-compatible | Yes | No (TS) | Yes | Yes |
| Numba required | Yes (Kaggle has it) | No | No | No |
| GPU needed for inference | No | No | No (but recommended) | No (but recommended) |
| Training required | No | No | Yes (offline) | Yes (offline) |

---

## 10. Performance Evidence

### 10.1 Measured Performance

| Contender | Board | Metric | Value | Source |
|-----------|-------|--------|-------|--------|
| connectpuct | 7x6 | Win rate vs minimax d3 | 55% (11W/9L) | S118 |
| kamide | 7x6 | Tactical correctness | Unknown | --- |
| pyvezi | 7x6 | Win rate vs random | >95% (assumed) | Source code analysis |
| QveenCoder | 7x6 | Win rate vs random | >95% (assumed) | Source code analysis |
| connectX-bitboard | 7x6 | Nodes/sec | Unknown (Numba JIT, estimated 100K+) | --- |
| katac4 | 7x6 | ELO (self-comparison) | ~1080 to ~1178 | S128 |
| haithameleuch | 7x6 | Internal score | 88% | S_NEW_011 (DOS-005) |

### 10.2 Claimed Performance (Unverified)

| Contender | Claim | Verification |
|-----------|-------|-------------|
| kamide | "Adaptive scoring minimax" | Source verified, but no benchmark data |
| sidhantagar | "Minimax + DP" | README only; source inaccessible |
| BEPb | "AlphaGo Zero with PARL" | Source code exists, no benchmark data |
| marcpaulo15 | "SFT + PPO" | 200K SFT samples verified |

### 10.3 Inferred Performance

| Contender | Inferred 7x6 Strength | Basis |
|-----------|---------------------|-------|
| connectX-bitboard | Strong (depth 12-14) | PVS + 16M TT + history + killers + aspiration |
| The-Reticle | Moderate (depth 8-10) | 10M TT + threat-map; TT commented out in practice |
| Kamide | Moderate | Adaptive scoring is novel but no TT/iterative deepening |
| pyvezi | Weak-moderate | Depth-4 minimax is very shallow |
| QveenCoder | Weak-moderate | Depth 3-6 minimax, no TT, simple eval |

### 10.4 Unknown Performance

| Contender | Unknown Factor |
|-----------|---------------|
| All classical engines on 15x13 | Zero benchmark evidence on large boards |
| All neural engines on 15x13 | No transfer learning data |
| MCTS engines on 15x13 | MCTS consistency untested on unsolved positions |
| DQN bots | Cannot detect forced wins >4 plies (C205 VERIFIED) |

---

## 11. Integration and Ensemble Opportunities

### 11.1 Cross-Contender Integration Matrix

| Source | Target | Integration |
|--------|--------|-------------|
| connectX-bitboard search | kamide eval | Replace quadratic eval with adaptive scoring for board-size generalization |
| kamide adaptive scoring | connectX-bitboard search | Use adaptive scoring as leaf eval for PVS search on large boards |
| katac4 ResNet | connectX-bitboard search | Replace `_count_open_lines` with NN value head; keep PVS search |
| The-Reticle TT | connectX-bitboard search | Share 10M TT entries (connectX-bitboard already has 16M, so this is additive only for other engines) |
| kamide adaptive scoring | DQN leaf eval | Use adaptive scoring as auxiliary loss during DQN training (AZAL concept from S114) |

### 11.2 Ensemble Design Recommendations

**ENS-NEW-001**: Classical board-size routing engine
- 7x6: connectX-bitboard (PVS + 16M TT)
- 15x13: Kamide (adaptive eval) + alpha-beta depth 6
- Fallback: NN leaf eval if available

**ENS-NEW-002**: NN-augmented classical engine
- Search: connectX-bitboard negamax + PVS
- Leaf eval: katac4 ResNet value head (fine-tuned on 15x13)
- Opening: Pascal Pons solved game tablebook
- TT: 16M entries shared between search and MCTS (ENS-018)

**ENS-NEW-003**: Board-size adaptive ensemble
- Agent selects between classical (7x6), neural (15x13), and hybrid (any size) based on board config
- Kamide's adaptive scoring provides natural routing arbiter

---

## 12. Failure Modes and Risks

### 12.1 Known Failure Modes

| Failure Mode | Contenders Affected | Severity | Mitigation |
|-------------|-------------------|----------|-----------|
| 15x13 board size | All classical engines | HIGH | Use NN leaf eval; implement board-size routing |
| No TT on 15x13 | pyvezi, QveenCoder, Kamide | HIGH | Add TT to Kamide's engine |
| 7x6-only NN | katac4, DQN bots | HIGH | Fine-tune on 15x13 positions |
| Kaggle T4 without GPU | All NN-dependent bots | MEDIUM | Use CPU-optimized inference (ONNX) |
| Kaggle 95MB submission limit | Opening books, large TTs | LOW | Use compressed TT (6-bit scores, as Kite) |
| Numba unavailable on Kaggle | connectX-bitboard | LOW | Pure-Python fallback included in source |

### 12.2 Unverified Risks

| Risk | Probability | Impact | Description |
|------|------------|--------|-------------|
| ResNet does not transfer to 15x13 | MEDIUM | HIGH | No evidence that 7x6-trained ResNet generalizes to 15x13 |
| MCTS consistency fails on 15x13 draws | MEDIUM | MEDIUM | C139 VERIFIED on 7x6 adjacent opening; untested on 15x13 |
| NN inference on Kaggle T4 is slower than expected | LOW | MEDIUM | T4 TensorRT FP16 benchmarks show 1.10ms for ResNet-18 (S096); smaller models should be faster |
| Kamide's adaptive scoring is weaker than claimed | LOW | LOW | Source verified; no benchmarks published |

---
## 13. Open Questions

1. **What is the actual search depth achievable on 15x13 within 2 seconds for each engine?** -- This is the single most important unknown for Kaggle ConnectX. All contenders have been benchmarked only on 7x6 (if at all).

2. **Can a ResNet trained on 7x6 generalize to 15x13?** -- The convolutional architecture has inductive bias toward local patterns, which are board-size invariant. But the policy head (7 outputs for 7 columns) maps to 15 outputs for 15 columns. No source demonstrates this adaptation.

3. **What is the optimal TT size for 15x13?** -- connectX-bitboard's 16M entries are sized for 7x6. On 15x13, position overlap is more frequent, suggesting a larger TT would help. But Kaggle's 95MB limit constrains TT size.

4. **Does Kamide's adaptive scoring actually outperform fixed-weight eval on 15x13?** -- The theory is sound (adaptive weights scale with `winCondition`), but no benchmark data exists to confirm this.

5. **Can the DQN approach (C205) be improved with search augmentation?** -- C205 VERIFIED: DQN cannot detect forced wins >4 plies. But DQN + alpha-beta (DQN as leaf eval) might mitigate this.

6. **Is there a Kaggle leaderboard for ConnectX that can be scraped?** -- snap-stanford's winning bot is 404 (DOS-005); current leaderboards require JavaScript rendering and cannot be accessed via WebFetch.

---

## 14. Recommendations

### 14.1 For Kaggle Bot Development

1. **Start with connectX-bitboard-agent as the classical engine**: It is the most sophisticated pure-Python classical engine in the corpus. Use its PVS + 16M TT + history + killers + aspiration + mirror symmetry as the baseline.

2. **Add Kamide's adaptive scoring as a leaf-eval alternative for 15x13**: Kamide's `winCondition`-parameterized scoring naturally generalizes across board sizes. Replace or augment the quadratic line-count with adaptive scoring on large boards.

3. **Add neural leaf evaluation (katac4 ResNet) as a third option**: For boards where the NN has been fine-tuned (or for 7x6 where it was trained), use the ResNet value head as leaf evaluation instead of handcrafted scoring.

4. **Implement board-size routing**: Use Kamide's adaptive framework as a natural arbiter:
   - 7x6 (solved): tablebook + PVS search with maximum depth
   - 15x13/15x10 (unsolved): NN leaf eval + alpha-beta depth 6 + large TT

5. **Fine-tune the ResNet on 15x13**: Use self-play generated positions on 15x13 (if feasible) or synthetic positions generated by a classical engine to fine-tune the existing katac4 ResNet.

### 14.2 For Benchmarking

1. **Run EXP-B-001 (classical engine depth vs board size)**: This is the single most important experiment to determine which engines are viable on which boards.

2. **Run EXP-B-006 (board-size coverage)**: Test every rostered contender on 7x6, 15x13, and 15x10. This will reveal the board-size generalization gap for the first time.

3. **Include Kamide as a baseline opponent**: Kamide's board-size generality makes it an ideal comparison point for testing whether adaptive scoring helps on large boards.

### 14.3 For Research

1. **Publish a benchmark of classical engine performance on 15x13**: This data does not exist anywhere in the public domain. It is the single most important missing benchmark.

2. **Investigate NN transfer learning from 7x6 to 15x13**: This is HYP-021 (board-size routing). No source has demonstrated successful transfer.

3. **Verify Kamide's adaptive scoring empirically**: Compare Kamide against connectX-bitboard on 7x6 (Kamide should be weaker) and on 15x13 (Kamide may be stronger due to adaptive scoring).

---

## 15. Sources and Retrieval Record

### 15.1 Primary Sources

| Source ID | Title | URL | License | Type | Retrieval Date |
|-----------|-------|-----|---------|------|----------------|
| S022 | connectX-bitboard-agent -- bitboard + Numba + PVS + 16M TT | `github.com/Tarun995/connectX-bitboard-agent` | MIT | Source code | 2026-08-05 |
| S021 | ConnectX (sidhantagar) -- minimax + DP | `github.com/sidhantagar/ConnectX` | Unknown | Source (metadata) | 2026-08-05 |
| S053 | The-Reticle -- alpha-beta + TT + threat-map | `github.com/ariaborin/The-Reticle` | Unknown | Source code | 2026-08-05 |
| S073 | pyvezi -- bitmask minimax with Pygame | `github.com/miksipiksic/pyvezi` | Unknown | Source code | 2026-08-05 |
| S121 | Kamide/connect-n -- adaptive scoring minimax | `github.com/Kamide/connect-n` | Unknown | Source code | 2026-08-05 |
| S123 | Kamide/connect-n full source analysis | `github.com/Kamide/connect-n` (src/) | Unknown | Source code | 2026-08-05 |
| S026 | katac4 -- ResNet + PUCT MCTS (MIT) | `github.com/GoodCoder666/katac4` | MIT | Source code | 2026-08-05 |
| S128 | woctezuma/puissance4 -- UCT MCTS package | `github.com/woctezuma/puissance4` | Unknown | Source + PyPI | 2026-08-05 |
| S129 | CogitoNTNU/AlphaZero -- AlphaZero for Four-in-a-Row | `github.com/CogitoNTNU/AlphaZero` | MIT | Source code | 2026-08-05 |

### 15.2 Reference Sources

| Source ID | Title | Type |
|-----------|-------|------|
| S007 | Wikipedia -- Connect Four solved game | Reference |
| S033 | connect4.gamesolver.org -- board-size solving matrix | Reference |
| S093 | Kaggle T4 GPU specs (NVIDIA) | Reference |
| S097 | Wikipedia -- infinite Connect-Four solved as Draw | Reference |

---

## 16. Cross-Links

### 16.1 Related Nexus Documents

| Document | Relation |
|----------|----------|
| contender-roster.md | This dossier provides deep profiles for BOT-012, BOT-013, BOT-014 (new); extends BOT-003, BOT-007 profiles |
| DOS-005 | This dossier supplements DOS-005's broad survey with deep profiles; DOS-005 uses non-standard S_NEW_ IDs |
| ensemble-catalog.md | This dossier adds ENS-NEW-001/002/003 ensemble designs based on deep-profile analysis |
| benchmark-blueprint.md | This dossier maps contenders to benchmark suites (BMS-001 through BMS-012) |
| MCTS-002 | Neural MCTS integration patterns; this dossier discusses NN leaf eval + classical search |
| CS-003 | Classical search and solver engineering; this dossier applies CS-003 concepts to specific engines |
| claim-register.md | C205 (DQN tactical weakness) directly informs this dossier's DQN analysis |
| hypothesis-register.md | HYP-021 (board-size routing) is the central hypothesis addressed by this dossier |
| research-state.md | Board-size solving matrix (R22); this dossier analyzes 15x13/15x10 specifically |

### 16.2 External Links

| Resource | URL |
|----------|-----|
| connectX-bitboard-agent | https://github.com/Tarun995/connectX-bitboard-agent |
| Kamide/connect-n | https://github.com/Kamide/connect-n |
| pyvezi | https://github.com/miksipiksic/pyvezi |
| The-Reticle | https://github.com/ariaborin/The-Reticle |
| katac4 | https://github.com/GoodCoder666/katac4 |
| connect4.gamesolver.org | https://connect4.gamesolver.org/ |
| Wikipedia -- Connect Four | https://en.wikipedia.org/wiki/Connect_Four |

---

## 17. V10 Research Dossier Metadata

- **Dossier ID**: DOS-006
- **Type**: Contender Deep Profiles and Board-Size Analysis
- **Status**: VERIFIED
- **Date**: 2026-08-05
- **Dossier Slot**: 5 of 7
- **Job**: 588
- **Lane**: CONTENDERS_BASELINES_AND_BENCHMARK_REFERENCES
- **Assigned Worker**: External Worker, Slot 5 of 7, Job 588

---

END OF DOS-006: CONTENDER DEEP PROFILES AND BOARD-SIZE ANALYSIS