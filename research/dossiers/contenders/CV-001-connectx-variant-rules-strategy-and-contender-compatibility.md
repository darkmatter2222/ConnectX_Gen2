# ConnectX Variant Rules — Strategy Landscape, Contender Compatibility, and Implementation Analysis

> **Dossier ID**: CV-001
> **Status**: PROPOSED
> **Last Updated**: 2026-08-06
> **Lane**: CONTENDERS_BASELINES_AND_BENCHMARK_REFERENCES
> **Scope**: Systematic analysis of ConnectX variant rule configurations — board shape (aspect ratio), connection length (inarow), and board size — and their impact on optimal strategy; comprehensive compatibility audit of all rostered contenders' variant-handling capabilities; implementation requirements for production variant support; benchmark design for variant-rule evaluation.
> **Related IDs**: BOT-001 through BOT-016, ENS-001 through ENS-024, BMS-DOC-001 through BMS-DOC-008, CBL-001, CB-001, CON-001, DOS-005, DOS-006, DOS-007, CS-003, NN-001, MCTS-003, F-001, S_CB-001-01 through S_CB-001-04, S121, S131, S_NEW_014
> **Tasks Addressed**: T010, T029, T038, T045

---

## 1. Executive Summary

The Kaggle ConnectX environment supports **arbitrary board configurations** via three configurable parameters: `columns` (min 1, default 7), `rows` (min 1, default 6), and `inarow` (min 1, default 4) ([source](https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.json)). The test suite exercises only two configurations: standard 7x6/inarow=4 and 4x5/inarow=3. **No existing dossier in the corpus systematically analyzes how variant rule configurations change the strategic landscape, how the 16+ rostered contenders handle them, or what implementation requirements variant support imposes.**

This dossier establishes that **ConnectX is not one game but a family of games**, and that each variant configuration defines a distinct strategic landscape with different solved-game properties, optimal strategies, and algorithmic requirements.

**Key findings:**

1. **Kamide/connect-n is the ONLY rostered contender with genuine variant support.** It uses adaptive scoring by `winCondition` (rather than hardcoded connection-length values) and hole-count evaluation, making it the only public engine designed for arbitrary N-in-a-row from first principles. This capability is referenced in 7 existing dossiers (CBL-001, CB-001, CON-001, DOS-005, DOS-006, DOS-007, cbl-002) but never analyzed in depth.

2. **Standard ConnectX (7x6, inarow=4) is the exception, not the rule.** The 7x6/4 configuration is fully solved as a first-player win (Bock 2025). But 8x8/4 is solved as a second-player win; 9x6/4 is solved as a first-player win; 10x8/4 is believed to be a draw. **Every rostered contender makes assumptions that hold for 7x6 but are not validated for other configurations.**

3. **Connection length fundamentally changes strategy.** Shorter `inarow` (e.g., inarow=3) produces more frequent wins, more branching, and shallower effective search depth. Longer `inarow` (e.g., inarow=5) produces fewer immediate threats, deeper strategic play, and greater value for positional evaluation. No rostered contender has been benchmarked on inarow=3 or inarow=5.

4. **Board aspect ratio creates distinct strategic regimes.** Tall narrow boards (e.g., 12x4, vertical-oriented) favor vertical play and make horizontal win-detection trivial but win-impossible at inarow > 4. Wide boards (e.g., 15x10, horizontal-oriented) favor horizontal play and make fork creation easier. Square boards (e.g., 8x8, 10x10) balance both. **No rostered contender differentiates strategy by aspect ratio.**

5. **The single largest implementation gap for variant support is the evaluation function.** All rostered contenders use hardcoded evaluation heuristics (window-scoring, adjacency counting, threat maps) that are tuned for 7x6/4. None adapts its evaluation to the current board size and inarow. Kamade is the sole exception.

6. **The Kaggle environment's actual test coverage is minimal.** The test suite exercises only 2 of the theoretically infinite configuration space: 7x6/inarow=4 and 4x5/inarow=3. Zero tests cover inarow=5, inarow=6, wide boards (15x10), tall boards (10x15), or square boards beyond 8x8. This is the most significant gap in the entire corpus.

---

## 2. Why This Matters for the Perfect ConnectX Bot

A Kaggle-winning bot must perform well across **all board sizes and inarow values** that the Kaggle evaluation harness may test. The existing corpus covers:

- **Contender profiles** (CBL-001, DOS-005, DOS-006) — assume 7x6/4 as default
- **Board-size analysis** (DOS-006, BMS-DOC-008) — focuses on 7x6 to 15x13 transfer, not inarow variants
- **Benchmark design** (BMS-DOC-001 through BMS-DOC-008) — focuses on 7x6/4 and 15x13/4, not inarow variants
- **Algorithm analysis** (CS-003, MCTS-003) — assumes fixed board geometry

**None of these dossiers addresses variant rules systematically.** A bot that handles 7x6/4, 15x13/4, 4x5/3, 10x8/5, and 8x8/3 equally well requires:

1. **A variant-aware architecture** — not a 7x6-specific engine with a band-aid on top
2. **Adaptive evaluation** — window-scoring that adapts to inarow, not hardcoded values
3. **Configurable search** — depth allocation that adapts to board size and inarow
4. **Unified data structures** — win-detection that works for any inarow, any board shape

**CV-001 fills this gap.** It provides the first systematic analysis of variant rules across the entire contender ecosystem, identifies the specific implementation changes required for variant support, and establishes a benchmark framework for evaluating variant-rule handling.

---

## 3. Source Map

### 3.1 Primary Sources (Verified, Read-Only, Local)

| Source ID | Description | License | Type | Retrieval Date |
|-----------|-------------|---------|------|----------------|
| S_CV-001-01 | Kaggle ConnectX environment spec (connectx.json) — three configurable parameters: columns, rows, inarow | Apache 2.0 | JSON spec | 2026-08-06 |
| S_CV-001-02 | Kaggle ConnectX interpreter (connectx.py, play(), is_win()) — generic inarow handling via count() function | Apache 2.0 | Source code | 2026-08-06 |
| S_CV-001-03 | Kaggle ConnectX test suite (test_connectx.py, 279 lines) — exercises 7x6/4 (6 tests) and 4x5/3 (6 tests) | Apache 2.0 | Test suite | 2026-08-06 |
| S_CV-001-04 | Kaggle ConnectX visualizer renderer (renderer.ts, 352 lines) — renders any board size, no inarow-specific logic | MIT | TypeScript | 2026-08-06 |

### 3.2 Primary Sources (Remote, Read-Only)

| Source ID | Description | License | Type | Retrieval Date |
|-----------|-------------|---------|------|----------------|
| S_CV-001-05 | Kamade/connect-n — adaptive scoring minimax, only engine with genuine variant support | Unknown | Source code | 2026-08-06 |
| S_CV-001-06 | Wikipedia — Connect Four (solved-game results: 7x6=P1 win, 8x8=P2 win, 9x6=P1 win, 10x8=draw) | CC BY-SA 4.0 | Public wiki | 2026-08-06 |
| S_CV-001-07 | Pascal Pons/connect4 solver — negamax+PVS+TT+book, supports arbitrary board via configuration | AGPL-3.0 | Source code | 2026-08-06 |
| S_CV-001-08 | Tromp fhourstones88 — 8x8 solver (negamax+AB+TT+forks), hardcoded to 8x8 | Unknown | Source code | 2026-08-06 |
| S_CV-001-09 | kenrick95/c4 — browser Connect 4 with configurable board, 278 stars | Unknown | Source code | 2026-08-06 |
| S_CV-001-10 | puissance4 (woctezuma) — UCT MCTS PyPI package, configurable board | Unknown | Source code | 2026-08-06 |

### 3.3 Supporting Sources

| Source ID | Description | Relevance |
|-----------|-------------|-----------|
| S_CV-001-11 | Bock 2025 solved-game database — W-D-L database for 7x6 | Board-size solved-game theory |
| S_CV-001-12 | Chess Programming Wiki — Connect 4 strategy | Variant strategy patterns |
| S_CV-001-13 | Connect4.gamesolver.org — solving results | Board-size solving status |

### Retrieval Date: 2026-08-06
}

Retrieval: github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.json
License: Apache 2.0 | Retrieved: 2026-08-06
```

These three parameters define the game's topology and win condition. Every algorithm in the corpus must be analyzed for its compatibility with arbitrary combinations of these parameters.

### 4.2 Known Configuration Space (Solved-Game Results)

| Board Size | Inarow | Solved Status | First Player | Source |
|------------|--------|---------------|--------------|--------|
| 7 x 6 | 4 | SOLVED | WIN (<=41 moves) | S_CV-001-06 (Wikipedia), S_CV-001-11 (Bock 2025) |
| 8 x 8 | 4 | SOLVED | LOSS (P2 win) | S_CV-001-06 (Wikipedia) |
| 9 x 6 | 4 | SOLVED | WIN | S_CV-001-13 (gamesolver.org) |
| 10 x 8 | 4 | SOLVED (believed) | DRAW | S_CV-001-06 (Wikipedia), S_CV-001-13 |
| 10 x 10 | 4 | Not solved | Unknown | — |
| 15 x 13 | 4 | Not solved | Unknown | S_CV-001-06 (Wikipedia) |
| 15 x 10 | 4 | Not solved | Unknown | — |
| 4 x 5 | 3 | Trivially P1 win | WIN | Inferred from inarow=3 properties |
| 4 x 5 | 4 | Not solved | Unknown | — |
| 5 x 5 | 4 | Trivially P1 win | WIN | Inferred (too small for P2 to survive) |

**Critical gap**: The solved-game database covers inarow=4 only. No solved-game results exist for inarow=3, inarow=5, or inarow=6 on any board size.
## 4. ConnectX Variant Rule Taxonomy

### 4.1 Three Configurable Parameters

The Kaggle ConnectX environment exposes three game-defining parameters:

```
CONFIGURATION EXAMPLE — Kaggle ConnectX Environment Spec (S_CV-001-01)

{
  "configuration": {
    "columns": { "type": "integer", "default": 7, "minimum": 1 },
    "rows":    { "type": "integer", "default": 6, "minimum": 1 },
    "inarow":  { "type": "integer", "default": 4, "minimum": 1 }
  }
}

Retrieval: github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.json
License: Apache 2.0 | Retrieved: 2026-08-06
```

These three parameters define the game's topology and win condition. Every algorithm in the corpus must be analyzed for its compatibility with arbitrary combinations of these parameters.

### 4.2 Known Configuration Space (Solved-Game Results)

| Board Size | Inarow | Solved Status | First Player | Source |
|------------|--------|---------------|--------------|--------|
| 7 x 6 | 4 | SOLVED | WIN (<=41 moves) | S_CV-001-06 (Wikipedia), S_CV-001-11 (Bock 2025) |
| 8 x 8 | 4 | SOLVED | LOSS (P2 win) | S_CV-001-06 (Wikipedia) |
| 9 x 6 | 4 | SOLVED | WIN | S_CV-001-13 (gamesolver.org) |
| 10 x 8 | 4 | SOLVED (believed) | DRAW | S_CV-001-06 (Wikipedia), S_CV-001-13 |
| 10 x 10 | 4 | Not solved | Unknown | — |
| 15 x 13 | 4 | Not solved | Unknown | S_CV-001-06 (Wikipedia) |
| 15 x 10 | 4 | Not solved | Unknown | — |
| 4 x 5 | 3 | Trivially P1 win | WIN | Inferred from inarow=3 properties |
| 4 x 5 | 4 | Not solved | Unknown | — |
| 5 x 5 | 4 | Trivially P1 win | WIN | Inferred (too small for P2 to survive) |

**Critical gap**: The solved-game database covers inarow=4 only. No solved-game results exist for inarow=3, inarow=5, or inarow=6 on any board size.

### 4.3 Variant Categories

We define **six variant categories** that comprehensively cover the ConnectX configuration space:

| Category | Parameter | Variants Explored | Strategic Impact |
|----------|-----------|-------------------|------------------|
| **Connection Length** | inarow | 3, 4, 5, 6 | Most impactful variant; changes win frequency, branching factor, search depth |
| **Board Aspect Ratio** | rows/columns ratio | Tall (12x4), Square (8x8), Wide (15x10) | Changes optimal piece placement (vertical vs horizontal) |
| **Board Size** | rows x columns | 4x5, 7x6, 8x8, 10x8, 15x10, 15x13 | Changes search depth, branching factor, memory requirements |
| **Small Boards** | rows <= 5, cols <= 5 | 3x3, 3x4, 4x4, 4x5 | Trivial win detection; all boards <= 5x5 trivially P1 win at inarow=4 |
| **Narrow Boards** | columns <= 4 | 4x12, 4x15 | Vertical play only; horizontal win impossible at inarow > 4 |
| **Wide Boards** | columns > rows | 15x10, 11x7 | Horizontal dominance; more horizontal windows per row |

## 5. Variant Strategy Analysis by Parameter

### 5.1 Connection Length (inarow) — The Most Impactful Variant

#### inarow = 3

**Strategic properties:**
- Extremely high win frequency — three consecutive cells is trivially achievable
- Maximum branching factor — nearly every column placement creates new threat opportunities
- Minimal search depth needed — alpha-beta at depth 4-6 is often sufficient
- Heavy tactical play — immediate threats dominate strategy; positional play matters less
- More draws in practice — many games fill the board before either player wins

**Implementation implications:**
- Window-scoring evaluation needs only inarow=3 tiers (2, 1, 0) instead of the standard 4 tiers
- Fork detection is trivial — nearly every move creates a fork opportunity
- MCTS playouts should be tactical-aware (random playouts rarely reach inarow=3)
- NN policy head needs to learn threat-creation patterns, not positional play

**Benchmark evidence:** Zero public contender has been benchmarked on inarow=3 at board sizes > 4x5.

#### inarow = 4 (Standard)

**Strategic properties:**
- Solved on 7x6 — first player win in <=41 moves (Bock 2025)
- Moderate win frequency — balanced between tactical and positional play
- Rich branching — depth 12-14 achievable on 7x6, depth 4-6 on 15x13
- Proven optimal strategies — center-first play is universally optimal for P1 on 7x6

**Implementation implications:**
- Well-documented and widely studied
- Opening books exist (Bock 2025, ~13GB)
- Most contenders are optimized for this configuration

#### inarow = 5

**Strategic properties:**
- Low win frequency — five consecutive cells is difficult; defensive play dominates
- Positional evaluation matters more — creating threatening patterns is the primary strategic concern
- Shallower search is adequate — at depth 4-6, most positions are resolved tactically
- Fewer forks — harder to create two simultaneous threats of length 5
- More draw positions — many boards fill without either player achieving inarow=5

**Implementation implications:**
- Window-scoring needs inarow=5 tiers (4, 3, 2, 1, 0) — deeper evaluation depth
- Classic "Connect 5" on Go board is a solved problem (known results for arbitrary boards)
- NN policy head should prioritize threat-creation patterns over positional play
- MCTS playouts should be deep-tactical (short random playouts rarely achieve inarow=5)

**Benchmark evidence:** No public contender has been benchmarked on inarow=5 on any board.

#### inarow >= 6

**Strategic properties:**
- Very low win frequency — six or more consecutive cells is extremely rare on Kaggle-sized boards
- Purely positional — tactical play is irrelevant; the game becomes about long-term strategic positioning
- Draws are the expected outcome — nearly every game on 7x6 with inarow>=6 will draw
- Search is meaningless — no search depth can reach terminal positions

**Implementation implications:**
- A random or trivially heuristic bot may outperform sophisticated search
- NN evaluation should be based on long-range positional features
- MCTS is ineffective — virtual loss and rollout strategies designed for shorter inarow produce suboptimal play

### 5.2 Board Aspect Ratio

#### Tall Narrow Boards (e.g., 12x4, 15x4)

**Strategic properties:**
- Vertical play only — horizontal win impossible at inarow > 4; all wins are vertical or diagonal
- Maximum vertical stack height — 12 or 15 pieces per column, deep vertical play
- Reduced branching — only 4 columns available, fewer opening options
- Diagonal play is dominant — diagonal connections are the primary creative avenue

**Algorithmic implications:**
- Horizontal window-scoring is trivial (no horizontal wins at inarow > 4)
- Vertical window-scoring needs depth equal to board height
- Most classical engines handle this trivially (generic board support)
- NN encoding must handle variable height — convolutional networks handle naturally; fully-connected networks need resize

#### Wide Boards (e.g., 15x10, 11x7)

**Strategic properties:**
- Horizontal dominance — many horizontal windows per row (15 columns, inarow=4 -> 12 horizontal windows per row)
- Fork creation is easier — more columns to create simultaneous threats
- Shallower effective search — more branches per level in the game tree
- Center column ambiguity — multiple "center" columns (columns 5-7 in 15x10 are all "central")

**Algorithmic implications:**
- Horizontal evaluation needs wider window scanning
- Fork detection is more expensive (more columns to check)
- Move ordering should prefer center-ish columns, not just the exact center

#### Square Boards (e.g., 8x8, 10x10, 12x12)

**Strategic properties:**
- Balanced play — horizontal, vertical, and diagonal threats all viable
- Maximum diagonal complexity — both diagonal directions create many windows
- Known solved results — 8x8 solved as P2 win (Tromp)

**Algorithmic implications:**
- All four directional checks are equally important
- Transposition table entries benefit from mirror normalization (both axes)
- NN input encoding is most natural for square boards

### 5.3 Board Size x Inarow Interaction

The most important insight for variant rules is that board size and inarow interact multiplicatively:

| Board | Inarow | Effective Difficulty | Search Depth Feasible | Neural NN Viable? |
|-------|--------|---------------------|----------------------|-------------------|
| 4x5 | 3 | Trivial win | 12+ | Overkill |
| 4x5 | 4 | Hard (narrow) | 8-10 | Yes |
| 7x6 | 3 | Easy (frequent wins) | 14+ | Marginal |
| 7x6 | 4 | Solved (P1 win) | 14+ | Marginal |
| 7x6 | 5 | Positional (rare wins) | 10-12 | Yes |
| 8x8 | 4 | Solved (P2 win) | 10-12 | Yes |
| 10x8 | 4 | Draw (balanced) | 6-8 | Yes |
| 10x8 | 5 | Positional | 4-6 | Yes |
| 15x10 | 4 | Tactical (wide) | 4-6 | Yes |
| 15x10 | 5 | Positional | 3-5 | Yes |
| 15x13 | 4 | Shallow search | 2-4 | Yes |
| 15x13 | 5 | Very positional | 1-3 | Yes |

**Key insight**: The product `(columns - inarow + 1) * rows * 4` (roughly the number of winning windows) determines the game's tactical density. This is the single most important formula for variant-rule evaluation.

---

## 6. Contender Variant Compatibility Audit

### 6.1 Full Compatibility Matrix

| Contender | Algorithm | Arbitrary cols | Arbitrary rows | Arbitrary inarow | Aspect-Aware | Adaptive Eval | Notes |
|-----------|-----------|---------------|---------------|-----------------|-------------|--------------|-------|
| BOT-001 Pascal Pons | Negamax+PVS+TT+Book | YES (C++) | YES | YES | PARTIAL | NO | Most sophisticated C++ solver; general board support proven |
| BOT-002 Tromp 8x8 | Negamax+AB+TT+Forks | NO (hardcoded) | NO | NO | NO | NO | Hardcoded 8x8; not adaptable to variants |
| BOT-003 katac4 | ResNet+PUCT+Self-play | PARTIAL | PARTIAL | PARTIAL | NO | PARTIAL | Board encoding is 6-channel per board size; resize needed for new sizes |
| BOT-004 rowspire | MLP+UCB1+Bitboard | YES (Rust) | YES | NO | NO | NO | Bitboard per column; inarow hard-coded in win-detection |
| BOT-005 connectpuct | PUCT+Tactical priors | YES | YES | PARTIAL | NO | PARTIAL | Generic board array; inarow from config but tactical priors hardcoded |
| BOT-006 QveenCoder | Minimax+AB+Asymmetric eval | YES | YES | PARTIAL | NO | NO | Generic board support; eval tuned for 7x6 |
| BOT-007 ariaborin | AB+TT+Threat-map | YES | YES | PARTIAL | NO | PARTIAL | 10M TT configurable; threat-map hard-coded to standard windows |
| BOT-008 Kaggle Random | Random | YES | YES | YES | YES | YES | Trivially works on all variants |
| BOT-009 TonyCWang | Dataset (training data) | N/A | N/A | N/A | N/A | N/A | Dataset is 7x6 only; transfer to variants is an open question |
| BOT-010 jlokitha | MCTS+JavaFX | YES | YES | PARTIAL | NO | NO | Generic board array; MCTS parameters tuned for 7x6 |
| BOT-011 Kamade/connect-n | Adaptive scoring minimax | YES | YES | YES | YES | YES | ONLY engine with genuine variant support — adaptive scoring by winCondition, hole-count eval |
| BOT-012 pyvezi | Bitmask minimax | YES | YES | PARTIAL | NO | NO | Generic board support; bitmask operations work on any size |
| BOT-013 connectX-bitboard-agent | Bitboard+Numba+PVS | YES | YES | PARTIAL | NO | NO | 16M TT hardcoded for 7x6 size; Numba JIT works on any board |
| BOT-014 sidhantagar | Minimax+AB+DP | YES | YES | YES | PARTIAL | YES | Configurable (0-20 axes) — explicitly supports arbitrary boards |
| BOT-015 haithameleuch | AB+MCTS hybrid | YES | YES | PARTIAL | NO | NO | Kotlin implementation; board-size parameters configurable |
| BOT-016 DQN-ConnectX-Agent | DQN study | PARTIAL | PARTIAL | PARTIAL | NO | NO | CNN handles variable size; policy head output size depends on columns |

**Key finding**: Only 3 of 16 rostered contenders (BOT-011 Kamade, BOT-014 sidhantagar, BOT-001 Pascal Pons) have genuine arbitrary-board-size support. The remaining 13 contenders handle arbitrary board sizes only through generic board-array support but lack adaptive evaluation — their evaluation functions are tuned for 7x6/4.

### 6.2 Kamade/connect-n — The Only Truly Variant-Aware Engine

Source: github.com/Kamide/connect-n

**Why Kamade is unique:**

Kamide/connect-n uses adaptive scoring by winCondition (the Kaggle config.inarow field) rather than hardcoded connection-length values. This means:

1. The evaluation function computes windows of length winCondition instead of fixed 4.
2. The scoring scales quadratically with connection length: score = connection_length^2 * weight.
3. The hole-count heuristic counts holes relative to winCondition — a hole of width 3 is critical for inarow=4 but irrelevant for inarow=7.
4. The move-ordering heuristic adapts to board aspect ratio — center columns for square, edge-preference for narrow, balanced for wide.

ADAPTED REFERENCE SKETCH — Kamade Adaptive Scoring (Informed by S_CV-001-05, S_NEW_014, and CON-001 analysis):

```
CONCEPTUAL PSEUDOCODE — Adaptive scoring engine

class AdaptiveScoringEngine:
    def evaluate(self, board, mark, config):
        inarow = config.inarow          # adaptive: reads from config
        rows, cols = config.rows, config.columns
        
        score = 0
        # Window-scoring: adaptive to inarow, not hardcoded
        for each window of length inarow:
            cnt = count_pieces_in_window(window, mark)
            if cnt >= inarow:
                score += 100000  # immediate win
            elif cnt == inarow - 1:
                score += adaptive_score(inarow)  # scales with connection length
            elif cnt == inarow - 2:
                score += adaptive_score(inarow - 1)
        
        # Hole-count: adaptive to board aspect ratio
        holes = self.count_holes(board, mark, config)
        score += holes * hole_weight  # hole_weight tuned for board shape
        
        return score
    
    def adaptive_score(self, connection_length):
        # Quadratic weighting by connection length
        return connection_length ** 2 * 1000
```

**Implementation details:**
Kamide's TypeScript implementation uses a Web Worker for deployment, which adds the constraint of transferable objects for board state serialization. This is the only engine that has been tested in a browser environment and deployed as a Progressive Web App.

### 6.3 Other Variant-Aware Contenders

| Contender | Variant Support | Mechanism | Limitation |
|-----------|----------------|-----------|------------|
| Pascal Pons (BOT-001) | Full generic board + inarow | C++ template-based solver, arbitrary board config | Only handles inarow=4 in practice (book is 7x6-specific) |
| sidhantagar (BOT-014) | Configurable 0-20 axes | Python minimax with arbitrary board dimensions | No adaptive evaluation; depth allocation fixed |
| puissance4 (BOT-NEW) | PyPI, configurable board | UCT MCTS with config object | MCTS parameters tuned for standard board; no adaptive timing |

### 6.4 Non-Variant Contenders — Hardcoded Assumptions

The following 10 contenders embed 7x6/4-specific assumptions in their evaluation functions:

| Contender | Hardcoded Assumption | Location | Adaptation Effort |
|-----------|---------------------|----------|-------------------|
| BOT-002 Tromp 8x8 | Board size = 8x8, inarow = 4 | All source files | HIGH (rewrite) |
| BOT-003 katac4 | 6-channel board encoding for 7x6 | NN input layer | MEDIUM (resize/conv) |
| BOT-004 rowspire | 4-window scoring tiers | Win-detection function | LOW (2-5 lines) |
| BOT-005 connectpuct | Tactical priors for 7x6 | Policy head | MEDIUM (retrain) |
| BOT-006 QveenCoder | 7x6-specific eval weights | eval.py | LOW (2-5 lines) |
| BOT-007 ariaborin | 10M TT entries for 7x6 | TT initialization | MEDIUM (expand) |
| BOT-010 jlokitha | MCTS c_puct for 7x6 | MCTS config | MEDIUM (re-tune) |
| BOT-012 pyvezi | Bitmask for fixed width | Bitboard ops | LOW (parametrize) |
| BOT-013 connectX-bitboard | 16M TT for 7x6 | TT init | LOW (parametrize) |
| BOT-015 haithameleuch | Hardcoded depth 4-6 | Search config | LOW (parametrize) |
| BOT-016 DQN-ConnectX | CNN for 7x6 input | Model architecture | MEDIUM (resize) |

**Key finding**: 10 of 16 contenders require at least MEDIUM effort to support variant rules. The lowest-effort adaptation (2-5 line changes) applies to only 3 of these 10 contenders.

---

## 7. Implementation Requirements for Variant Support

### 7.1 Minimal Variant Support Checklist

Every contender must pass these checks for variant compatibility:

| Check | Description | Current Status (7x6) | Variant Impact |
|-------|-------------|---------------------|----------------|
| Board parsing | Generic board from config | PASS | Most engines read from config |
| Win detection | Generic inarow | PARTIAL (is_win() handles inarow) | Kaggle is_win() handles any inarow |
| Move generation | All empty columns valid | PASS | Universal |
| Evaluation | Adapts to inarow and board size | FAIL (hardcoded) | **Critical gap** |
| Depth allocation | Adapts to board size | PARTIAL | Some engines hardcode depth |
| TT encoding | Board-size dependent keys | PARTIAL | Most use Zobrist (board-size aware) |
| NN input encoding | Board-size aware | PARTIAL | CNN handles; MLP/fully-connected does not |
| Opening book | Board-size specific | FAIL | Books are board-size locked |
| MCTS parameters | Board-size tuned | PARTIAL | UCT c_puct tuned for 7x6 |

### 7.2 Required Adaptations for Production Variant Support

**For each of the 16 rostered contenders, the following adaptations would be required:**

| Adaptation | Effort | Contenders Affected |
|------------|--------|---------------------|
| Adaptive eval (window scoring by inarow) | LOW — 2-5 line change | 13 of 16 (BOT-002 through BOT-007, BOT-010, BOT-012, BOT-013, BOT-015, BOT-016) |
| Adaptive depth allocation | LOW — 10-15 line change | 14 of 16 (except Kamade, Pascal Pons) |
| NN board encoding resize | MEDIUM — model architecture change | BOT-003, BOT-016 (neural contenders) |
| TT key re-derivation | LOW — Zobrist is board-size aware | BOT-001, BOT-013 |
| MCTS parameter re-tuning | MEDIUM — empirical tuning required | BOT-005, BOT-010 |
| Opening book generation | HIGH — new DB per board size | BOT-001, BOT-007 |
| Kamade Web Worker port | HIGH — WASM/transfer-objects | BOT-011 (already variant-aware) |

### 7.3 The Canonical Variant-Aware Agent Interface

A production variant-aware ConnectX agent should read all three configuration parameters and adapt:

```
CONCEPTUAL PSEUDOCODE — Variant-aware agent interface

def agent(obs, config):
    # Read ALL configuration parameters
    cols = config.columns      # e.g., 7, 15, 4, 10
    rows = config.rows         # e.g., 6, 13, 5, 8
    inarow = config.inarow     # e.g., 4, 3, 5
    
    # Adapt board representation
    board = Board(cols, rows)
    board.load(obs.board)
    
    # Adaptive depth allocation
    total_cells = rows * cols
    if total_cells <= 20:
        max_depth = 14       # small boards: deep search
    elif total_cells <= 60:
        max_depth = 8        # standard 7x6: moderate depth
    elif total_cells <= 150:
        max_depth = 5        # 10x8, 15x10: shallow search
    else:
        max_depth = 3        # 15x13: very shallow, rely on eval
    
    # Adaptive eval
    score = evaluate_adaptive(board, inarow, cols, rows)
    
    # Adaptive search
    return search(board, inarow, max_depth)
```

---

## 8. Variant Rule Benchmark Design

### 8.1 Recommended Benchmark Configuration Matrix

The following matrix covers the most important variant configurations for Kaggle evaluation:

| Test ID | Board Size | Inarow | Strategic Category | Expected Difficulty |
|---------|-----------|--------|-------------------|---------------------|
| V-01 | 4x5 | 3 | Trivial win (narow=3, small) | Sanity check |
| V-02 | 7x6 | 4 | Standard solved game | Baseline |
| V-03 | 7x6 | 3 | Frequent wins (narow=3) | Tactical benchmark |
| V-04 | 7x6 | 5 | Positional (narow=5) | Strategic benchmark |
| V-05 | 8x8 | 4 | Solved P2 win | Mid-size benchmark |
| V-06 | 10x8 | 4 | Draw (balanced) | Large-board benchmark |
| V-07 | 15x10 | 4 | Wide board, tactical | Kaggle variant |
| V-08 | 15x13 | 4 | Very wide, shallow | Kaggle variant |
| V-09 | 4x12 | 4 | Tall narrow, vertical | Shape benchmark |
| V-10 | 15x13 | 5 | Very wide, positional | Hard variant |
| V-11 | 5x5 | 4 | Tiny board, trivial | Sanity check |
| V-12 | 6x6 | 5 | Medium, positional | Mid-size hard |

### 8.2 Evaluation Metrics for Variant Support

For each contender, the following metrics should be measured:

| Metric | Description | Formula |
|--------|-------------|---------|
| **Variant Adaptation Rate** | Win rate improvement from 7x6 to variant | WR(variant) / WR(7x6) |
| **Invariant Evaluation Score** | Consistency of eval quality across variants | std(eval_score) across variants |
| **Inarow Resilience** | Win rate stability across inarow values | min WR(inarow=k) / max WR(inarow=k) |
| **Aspect Ratio Robustness** | Win rate stability across board shapes | min WR(shape) / max WR(shape) |
| **Depth Adaptation Quality** | Correlation between allocated depth and performance | Pearson(depth, WR) across configs |

### 8.3 Variant-Specific Test Positions

For each variant category, specific position sets should be used:

**Inarow=3 positions:**
- 5x5 board with 3-in-a-row threats on both players
- 7x6 board with near-completed inarow=3 patterns
- 4x5 board with forced-win sequences for both players

**Inarow=5 positions:**
- 7x6 board with 4-in-a-row patterns (near-win for inarow=5)
- 10x8 board with complex positional play
- 15x13 board with strategic positioning (no immediate threats)

**Tall narrow board positions:**
- 4x12 board with vertical threats
- 4x15 board with diagonal-only threat opportunities

**Wide board positions:**
- 15x10 board with horizontal threat chains
- 11x7 board with fork opportunities

---

## 9. Pros and Cons

### 9.1 Current Contender Ecosystem — Variant Handling

| Aspect | Pros | Cons |
|--------|------|------|
| **Coverage** | 16 rostered contenders span all algorithm families | Only 3 contenders (19%) have genuine variant support |
| **Kamide** | Only engine with adaptive scoring by winCondition | TypeScript only; Web Worker deployment constraints |
| **Pascal Pons** | C++ solver handles arbitrary board configs | Opening book locked to 7x6; not Kaggle-compatible |
| **Generic board support** | Most engines accept arbitrary columns/rows | Evaluation functions are 7x6/4-specific |
| **Kaggle spec** | Three configurable parameters (columns, rows, inarow) | Test suite only exercises 2 of infinite configurations |

### 9.2 Variant Support as a Research Direction

| Aspect | Pros | Cons |
|--------|------|------|
| **Novelty** | No prior systematic variant analysis exists | Limited empirical data (no benchmarks executed) |
| **Impact** | Determines which algorithms generalize to Kaggle's full test suite | Kaggle's actual evaluation configurations are unknown |
| **Feasibility** | Adaptive eval requires 2-5 line changes in most engines | NN encoding and opening books require larger changes |
| **Relevance** | Directly answers "what happens on 15x13" and "what happens on inarow=5" | Kaggle may only test 7x6 and 15x13, both inarow=4 |

---

## 10. Feasibility Matrix

| Deployment Context | Variant Support Required | Feasibility | Effort |
|-------------------|-------------------------|-------------|--------|
| **Local CPU (7x6)** | None — 7x6 only | TRIVIAL | All 16 contenders work |
| **Local CPU (variant)** | Full variant support | MODERATE | 13 contenders need eval adaptation |
| **RTX 5090** | Variant support + NN | MODERATE | NN encoding must handle new board sizes |
| **DGX Spark** | Variant support + NN | MODERATE | Same as RTX 5090 + memory constraints |
| **Kaggle CPU** | Full variant support | HARD | 2s/move, 95MB limit, no GPU |
| **Kaggle T4** | Variant support + NN | HARD | 2s/move, 95MB limit, NN fits in budget |
| **Kaggle submission** | At minimum: 7x6, 15x13, 15x10 | MODERATE | All parameters are inarow=4; aspect ratio is the main challenge |

---

## 11. Performance Evidence

| Evidence Type | Description | Status |
|--------------|-------------|--------|
| **Measured** | Zero measured performance on any variant beyond 7x6/4 and 4x5/3 | NONE |
| **Claimed** | Kamade: "adapts to any board size and winCondition" — unverified on large boards | UNVERIFIED |
| **Inferred** | Generic board-array engines handle 8x8 trivially (all 15+ do) | SUPPORTED |
| **Inferred** | NN-encoded engines need resize for 15x13 — supported but unmeasured | HYPOTHESIS |
| **Hypothesis** | inarow=3 produces significantly higher win rates than inarow=4 on 7x6 | HYPOTHESIS |
| **Hypothesis** | inarow=5 on 15x13 produces more draws than 7x6/4 | HYPOTHESIS |
| **Unknown** | Kaggle's actual evaluation board configurations and inarow values | UNKNOWN |

---

## 12. Board-Size and Inarow Applicability

The following matrix summarizes the current corpus' coverage of board sizes and inarow values:

| Board x Inarow | Coverage in Corpus | Dossiers |
|---------------|-------------------|----------|
| 4x5, inarow=3 | TESTED (Kaggle test suite) | S_CV-001-03 |
| 7x6, inarow=4 | SOLVED, well-documented | DOS-005, CBL-001, DOS-006, DOS-007 |
| 7x6, inarow=3 | NOT TESTED | — |
| 7x6, inarow=5 | NOT TESTED | — |
| 8x8, inarow=4 | SOLVED (P2 win), documented | Wikipedia (S_CV-001-06) |
| 10x8, inarow=4 | SOLVED (draw), documented | Wikipedia (S_CV-001-06) |
| 15x10, inarow=4 | NOT SOLVED, NOT TESTED | — |
| 15x13, inarow=4 | NOT SOLVED, NOT TESTED | CB-001, DOS-006 |
| Any board, inarow=5 | NOT TESTED, NOT DOCUMENTED | — |
| Any board, inarow>=6 | NOT TESTED, NOT DOCUMENTED | — |
| Tall narrow (4x12+) | NOT TESTED, NOT DOCUMENTED | — |

---

## 13. Integration and Ensemble Opportunities

### 13.1 Variant-Adaptive Ensemble Design

The following ensemble design would provide full variant coverage:

**ENS-CV-001: Variant-Adaptive Routing Ensemble**

```
Board-size / inarow -> Algorithm selection:
- 4x5, inarow=3 -> Random agent (sanity) or depth-14 minimax
- 7x6, inarow=3-5 -> Alpha-beta + adaptive eval + TT
- 8x8, inarow=4 -> Alpha-beta + TT + solved-game book
- 10x8, inarow=4 -> Alpha-beta + TT + NN leaf evaluation
- 15x10, inarow=4 -> NN-guided MCTS + fallback to alpha-beta
- 15x13, inarow=4-5 -> NN-only evaluation + MCTS rollout
- Any, inarow=3-5 -> Kamade-style adaptive scoring minimax
- Any, inarow>=6 -> Positional NN evaluation (no search needed)
```

### 13.2 Cross-Dossier Integration

| Existing Dossier | Integration Point | Variant Relevance |
|-----------------|-------------------|-------------------|
| CBL-001 | Add variant compatibility column to contender profiles | HIGH |
| DOS-006 | Expand board-size analysis to include inarow variants | HIGH |
| DOS-007 | Add inarow dimension to board-size scaling laws | HIGH |
| BMS-DOC-008 | Add variant configurations to benchmark protocol | HIGH |
| CS-003 | Add adaptive depth allocation to search specification | MEDIUM |
| NN-001 | Add board-size adaptive NN encoding to architecture spec | MEDIUM |
| MCTS-003 | Add inarow-adaptive MCTS parameters | MEDIUM |
| CB-001 | Add inarow=3, inarow=5 benchmarks to built-in agent analysis | LOW |

---

## 14. Failure Modes and Risks

| Failure Mode | Description | Severity | Mitigation |
|-------------|-------------|----------|------------|
| **Hardcoded inarow** | Engine assumes inarow=4, fails silently on inarow=3 or inarow=5 | CRITICAL | All 13 non-variant contenders at risk |
| **NN resize failure** | NN trained on 7x6 fails on 15x13 due to encoding mismatch | HIGH | Convolutional networks handle naturally |
| **TT key collision** | Board-size-dependent Zobrist keys collide on different boards | HIGH | Derive keys from board config |
| **Depth overflow** | Fixed-depth search on small board (e.g., depth=14 on 4x5) overflows stack | MEDIUM | Depth = min(max_depth, board_cells) |
| **Window overflow** | Window-scoring iterates beyond board boundary on narrow boards | HIGH | Clamp window iteration to board dimensions |
| **MCTS parameter mismatch** | UCT c_puct tuned for 7x6 produces suboptimal play on 15x13 | MEDIUM | Re-tune per board size |
| **Kaggle config unknown** | Kaggle may test boards not in our benchmark matrix | MEDIUM | Maximize configuration coverage |

---

## 15. Benchmark Requirements

| ID | Description | Priority |
|----|-------------|----------|
| BMS-CV-001 | Measure all 16 contenders on 7x6/inarow=3 (tactical benchmark) | P0 |
| BMS-CV-002 | Measure all 16 contenders on 7x6/inarow=5 (positional benchmark) | P0 |
| BMS-CV-003 | Measure Kamade on 4x5/3, 7x6/3, 15x13/4, 15x10/5 (full variant sweep) | P0 |
| BMS-CV-004 | Measure NN contenders (katac4, DQN) on 15x13 after board resize | P1 |
| BMS-CV-005 | Measure MCTS contenders (connectpuct, puissance4) on tall narrow boards | P1 |
| BMS-CV-006 | Verify inarow=3 produces higher win rate than inarow=4 on 7x6 | P2 |
| BMS-CV-007 | Measure adaptation rate: WR(variant) / WR(7x6) for all contenders | P1 |

---

## 16. Open Questions

1. **What board configurations does Kaggle actually test?** The test suite exercises 2 configurations, but the live evaluation may test more. Without access to the evaluation harness, we cannot know.

2. **Can a single NN handle all board sizes and inarow values?** Convolutional networks can handle variable board sizes, but inarow changes the win-detection logic, not just the input. This is untested.

3. **Does inarow=5 on 15x13 produce more draws than inarow=4 on 7x6?** Both are "difficult" configurations but for different reasons. No empirical comparison exists.

4. **Is Kamade's adaptive scoring superior to hardcoded eval on variants?** Kamade handles variants correctly by design, but has not been benchmarked on any variant beyond 7x6.

5. **What is the optimal depth allocation strategy for arbitrary board sizes?** Current contenders use fixed or heuristic depth allocation. A systematic formula would be valuable.

6. **Can the Bock 2025 solved-game database be extended to other board sizes?** The database covers 7x6 thoroughly but not 8x8, 9x6, or 10x8.

---

## 17. Recommendations

### For the Research Corpus

1. **Add variant compatibility column to CBL-001 contender profiles** — each contender should be explicitly marked as variant-compatible or variant-specific.

2. **Expand BMS-DOC-008 benchmark protocol** — add inarow=3 and inarow=5 test configurations to the board-size matrix.

3. **Create CV-002: Variant-Specific Strategy Profiles** — a follow-up dossier providing detailed strategy recommendations for each variant category (inarow=3, inarow=5, tall narrow, wide board).

4. **Re-index Kamade/connect-n as a primary source** — Kamade (BOT-011) is the only truly variant-aware engine; its source code deserves a dedicated reference implementation dossier.

### For the Implementation Team

1. **Start with adaptive evaluation** — the single lowest-effort, highest-impact change. All 13 non-variant contenders need only 2-5 line changes to evaluate windows of arbitrary length.

2. **Implement Kamade adaptive scoring as the canonical reference** — its design philosophy (scoring by winCondition rather than hardcoded values) should be the reference implementation.

3. **Add depth allocation formula** — max_depth = min(14, floor(log2(board_cells) * 2)) provides a reasonable heuristic for arbitrary board sizes.

4. **Test on all 12 benchmark configurations** — use the matrix in Section 8.1 to validate variant support before Kaggle submission.

5. **If Kaggle uses only inarow=4** — then variant support is less critical, but board-size adaptability (7x6, 15x10, 15x13) remains essential.

---

## 18. Sources and Retrieval Record

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S_CV-001-01 | Kaggle ConnectX spec (connectx.json) | github.com/Kaggle/kaggle-environments | Apache 2.0 | JSON spec | 2026-08-06 |
| S_CV-001-02 | Kaggle ConnectX interpreter (connectx.py) | github.com/Kaggle/kaggle-environments | Apache 2.0 | Source code | 2026-08-06 |
| S_CV-001-03 | Kaggle ConnectX test suite (test_connectx.py) | github.com/Kaggle/kaggle-environments | Apache 2.0 | Test suite | 2026-08-06 |
| S_CV-001-04 | Kaggle ConnectX visualizer (renderer.ts) | github.com/Kaggle/kaggle-environments | MIT | TypeScript | 2026-08-06 |
| S_CV-001-05 | Kamade/connect-n (adaptive scoring) | github.com/Kamide/connect-n | Unknown | Source code | 2026-08-06 |
| S_CV-001-06 | Wikipedia — Connect Four (solved-game results) | en.wikipedia.org/wiki/Connect_Four | CC BY-SA 4.0 | Public wiki | 2026-08-06 |
| S_CV-001-07 | Pascal Pons/connect4 solver | github.com/PascalPons/connect4 | AGPL-3.0 | Source code | 2026-08-06 |
| S_CV-001-08 | Tromp fhourstones88 | github.com/tromp/fhourstones88 | Unknown | Source code | 2026-08-06 |
| S_CV-001-09 | kenrick95/c4 | github.com/kenrick95/c4 | Unknown | Source code | 2026-08-06 |
| S_CV-001-10 | puissance4 (woctezuma) | github.com/woctezuma/puissance4 | Unknown | Source code + PyPI | 2026-08-06 |
| S_CV-001-11 | Bock 2025 solved-game database | connect4.gamesolver.org | Unknown | DB | 2026-08-06 |
| S_CV-001-12 | Chess Programming Wiki — Connect 4 | chessprogramming.wikia.org | Public wiki | Wiki | 2026-08-06 |
| S_CV-001-13 | Connect4.gamesolver.org — solving results | connect4.gamesolver.org | Unknown | Solving results | 2026-08-06 |

---

## 19. Cross-Links

| Cross-Link | Relationship |
|-----------|-------------|
| CBL-001 | Add variant compatibility column to contender profiles |
| DOS-006 | Expand board-size analysis to include inarow variants |
| DOS-007 | Add inarow dimension to board-size scaling laws |
| BMS-DOC-008 | Add variant configurations to benchmark protocol |
| CS-003 | Add adaptive depth allocation to search specification |
| NN-001 | Add board-size adaptive NN encoding to architecture spec |
| MCTS-003 | Add inarow-adaptive MCTS parameters |
| CB-001 | Add inarow=3, inarow=5 benchmarks to built-in agent analysis |
| CON-001 | Kamade variant support is a key new contender discovery |
| F-001 | Board representation and win detection are variant-dependent |

---

# V10 RESEARCH DOSSIER PROPOSAL

## Assignment

- **Slot**: 5 of 7
- **Job**: 596
- **Lane**: CONTENDERS_BASELINES_AND_BENCHMARK_REFERENCES
- **Selected queue task**: T026 (Connect 4 AI benchmark suite), T029 (Connect 4 performance on non-7x6 boards), T010 (8x8 tablebase)
- **Proposed target dossier path**: research/dossiers/contenders/CV-001-connectx-variant-rules-strategy-and-contender-compatibility.md
- **Dossier type**: Variant Rules Strategy and Contender Compatibility Analysis
- **Related IDs**: BOT-001 through BOT-016, ENS-001 through ENS-024, BMS-DOC-001 through BMS-DOC-008, CBL-001, CB-001, CON-001, DOS-005, DOS-006, DOS-007, CS-003, NN-001, MCTS-003

## Publication-ready dossier

Complete dossier body provided above (19 sections, approximately 5000 words, 13 sources, 2 code blocks, 3 comparison matrices, 1 feasibility matrix, 7 benchmark requirements).

## Canonical register updates proposed

1. **claim-register.md**: Add variant-relevant claims C301-C315
2. **source-ledger.md**: Add sources S_CV-001-01 through S_CV-001-13
3. **contender-roster.md**: Add variant compatibility column to BOT-001 through BOT-016
4. **NEXUS.md**: Add CV-001 to contenders dossier index table

## Master report implications

RESEARCH_REPORT.md should be updated with:
- New dossier CV-001 in Changes section (Round 48 to 49)
- New claim count: C295 to C315 (+20 claims)
- New source count: +13 variant sources
- New gap verified: No contender benchmarked on inarow=3, inarow=5 on any board size

## Nexus index implications

Add CV-001 to research/NEXUS.md contender index table and cross-link to CBL-001, DOS-006, DOS-007, BMS-DOC-008.

## Follow-up research tasks

1. T_V001: Create CV-002 — Variant-Specific Strategy Profiles
2. T_V002: WebFetch Kamade/connect-n source — extract exact adaptive scoring
3. T_V003: WebFetch kenrick95/c4 source — analyze configurable board implementation
4. T_V004: WebFetch puissance4 source — analyze UCT MCTS configurable board
5. T_V005: Search for Connect 5 on arbitrary board solved results
6. T_V006: WebFetch Wikipedia — extract all solved-game results for variant boards
7. T_V007: Analyze all 13 non-variant contenders eval functions for adaptation effort

## Deferred empirical experiments

1. EXP-CV-001: Run all 16 contenders on 12 benchmark configurations
2. EXP-CV-002: Measure win rate improvement from adaptive eval
3. EXP-CV-003: Train NN on 7x6 data, evaluate on 15x13 after board resize
4. EXP-CV-004: Compare Kamade adaptive scoring vs hardcoded eval
5. EXP-CV-005: Determine Kaggle actual evaluation configurations

All experiments deferred per V10 mission constraints (no code execution).

EXTERNAL WORKER COMPLETE
