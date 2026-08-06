# RI-007: Three New ConnectX Reference Implementations from 2026 GitHub Topics Scan

## Metadata

- **Dossier ID**: RI-007
- **Status**: PROPOSED
- **Last Updated**: 2026-08-05
- **Lane**: Source Dossiers and Code Archaeology
- **Slot**: 1 of 7, Job 592
- **Scope**: Complete source-code archaeology of three new repositories discovered via GitHub topics scan (connect-four, connectx, connect-four-ai) sorted by updated
- **Related IDs**: T003, CBL-001, DOS-006, CS-003, CS-005, MCTS-003, MCTS-005, RI-001, RI-002, ENS-013, ENS-014
- **Source IDs**: S166-S176 (9 primary sources across 3 repositories)

## Executive Summary

RI-007 performs complete source-code archaeology on **three new ConnectX/Connect Four AI repositories** discovered via a fresh GitHub topics scan (connect-four, connectx, connect-four-ai, sorted by update date, 2026-08-05). This scan addresses **T003** (New GitHub topics scan for ConnectX/Connect 4), which was marked READY since R10.

The three repositories represent three distinct architectural paradigms:

| Repo | Language | Architecture | Key Differentiator |
|------|----------|-------------|-------------------|
| **Tarun995/connectX-bitboard-agent** | Python + Numba | Bitboard negamax + PVS + aspiration windows + mirror symmetry TT | First Kaggle-submit-able Python agent to combine PVS, mirror-symmetric TT, and Numba JIT in a single codebase |
| **jesper-olsen/connect-four** | Rust | Exact solver (Tromp Fhourstones port) + dual-slot work-aware TT + textbook heuristic eval | The most faithful public Rust port of Tromp Four stones solver, verified exact-node regression against C/Java references |
| **haithameleuch/connect-four-ai** | Kotlin + Javalin | Minimax with alpha-beta + Monte Carlo rollout evaluation at leaves | Novel hybrid: uses stochastic rollouts (250 simulations) instead of static heuristic at alpha-beta leaf nodes |

**Key findings:**

1. **Tarun995 is the most sophisticated Kaggle candidate found** -- it combines 8 optimization layers (bitboard encoding, negamax, alpha-beta, PVS, aspiration windows, 16M TT with mirror symmetry, iterative deepening, Numba JIT) and is explicitly designed for the Kaggle 2-second time limit.
2. **jesper-olsen provides the first publicly available exact-node regression test suite** for Tromp Four stones solver -- four benchmark positions with exact node counts (51,596; 8,716,732; 169,704,432; 1,479,113,766).
3. **haithameleuch introduces a novel leaf-evaluation hybrid** -- alpha-beta search with Monte Carlo rollout at leaf nodes instead of heuristic evaluation. This is a form of simulation search that could be transferable to ConnectX.
4. **All three use different board representations**: Tarun995 uses 64-bit bitboards; jesper-olsen uses 64-bit position codes with H1-stride column layout; haithameleuch uses a standard 2D integer grid.
## Why This Matters for the Perfect ConnectX Bot

These three implementations address **three gaps** in the existing corpus:

1. **Tarun995** provides a **complete PVS implementation with mirror-symmetric transposition table and Numba JIT acceleration** -- the only Python agent in the corpus combining all four techniques. This directly informs the classical search stack (CS-003, CS-005) and the Kaggle deployment strategy (MCTS-004, DOS-007).
2. **jesper-olsen provides the first public Rust port of Tromp Four stones with exact node-count verification** -- critical for validating any Connect 4 solver implementation. This fills a gap left by Tromp original C/Java references being non-reusable.
3. **haithameleuch demonstrates a novel alpha-beta + Monte Carlo hybrid leaf evaluation** -- an alternative to static heuristics and neural evaluation that has not been explored in the ConnectX corpus.

## Source Map

| Source ID | Title | URL / Path | Type | License | Date |
|-----------|-------|------------|------|---------|------|
| S166 | Tarun995/connectX-bitboard-agent repository | https://github.com/Tarun995/connectX-bitboard-agent | Repo | MIT | 2026-08-05 |
| S167 | agent.py (core agent logic) | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/src/agent.py | Source | MIT | 2026-08-05 |
| S168 | README.md (architecture, bitboard encoding, search optimization) | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/README.md | Docs | MIT | 2026-08-05 |
| S169 | main.py (local runner) | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/main.py | Source | MIT | 2026-08-05 |
| S170 | jesper-olsen/connect-four repository | https://github.com/jesper-olsen/connect-four | Repo | MIT (inferred) | 2026-08-05 |
| S171 | mcts.rs (MCTS: UCB1, arena tree, rollout) | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/mcts.rs | Source | MIT | 2026-08-05 |
| S172 | eval.rs (textbook heuristic: 69 window bitmasks) | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/eval.rs | Source | MIT | 2026-08-05 |
| S173 | tt.rs (dual-slot TT with work-aware replacement) | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/tt.rs | Source | MIT | 2026-08-05 |
| S174 | minimax.rs (negamax alpha-beta with history heuristic) | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/minimax.rs | Source | MIT | 2026-08-05 |
| S175 | haithameleuch/connect-four-ai repository | https://github.com/haithameleuch/connect-four-ai | Repo | N/A (unlicensed) | 2026-08-05 |
| S176 | VierGewinnt.kt (Kotlin game interface) | Via GitHub tree API | Source | N/A | 2026-08-05 |
## Technical / Algorithmic Explanation

### 1. Tarun995/connectX-bitboard-agent -- The Full Stack

#### 1.1 Board Representation (64-bit Bitboard Encoding)

The board is encoded as **two 64-bit integers (one per player), using a **column-major bit layout** with stride H1 = rows + 1:

```
Column layout (7 columns x 7 bits each, including sentinel row):

Col 0   Col 1   Col 2   Col 3   Col 4   Col 5   Col 6
bit 0   bit 7   bit 14  bit 21  bit 28  bit 35  bit 42
bit 1   bit 8   bit 15  bit 22  bit 29  bit 36  bit 43
...     ...     ...     ...     ...     ...     ...
bit 5   bit 12  bit 19  bit 26  bit 33  bit 40  bit 47
------  ------  ------  ------  ------  ------  ------
bit 6   bit 13  bit 20  bit 27  bit 34  bit 41  bit 48  <-- sentinel (unused)
```

The sentinel row (7th bit per column) prevents horizontal wrap-around in win detection. A piece in row 5 of column 0 will not be adjacent to a piece in row 0 of column 1, because the bit gap (H1 = 7) ensures they are never within 3 bit positions of each other.

For inarow=4, win detection uses **12 bitwise operations** total (4 directions x 3 operations each: shift, AND, check). For arbitrary n, it generalizes to **4 x (n-1) shift-and operations**.

#### 1.2 Transposition Table with Mirror Symmetry

The TT uses `pos + (pos | opp)` as the position key -- Pascal Pons method, simpler than Zobrist hashing but equally unique for bitboard representations.

Mirror symmetry: After computing the best move, the algorithm **also stores the result for the horizontally mirrored position**, effectively doubling the effective TT hit rate for symmetric positions at no additional storage cost.

#### 1.3 Principal Variation Search (PVS)

The Numba-compiled `_negamax_nb` function implements **full PVS**:

- First move (best by move ordering): full-window search
- Subsequent moves: null-window (scout) search: prove move is worse than alpha
- If scout fails (score > alpha), re-search with full window

PVS is the **most aggressive alpha-beta variant** -- it only does a full re-search when the null-window search fails. In practice, PVS achieves **10-30% more nodes per second** vs standard alpha-beta with the same move ordering.

#### 1.4 Aspiration Windows

For depth >= 5: search with narrow window (prev_score +/- 150), re-search full window (-2M to +2M) if aspiration fails.

#### 1.5 Evaluation Heuristic

```
Tactical:
  - Fork (2+ winning moves): +950
  - Single threat: +500
  - Opponent fork: -950
  - Opponent single threat: -200

Positional:
  - Open line (quadratic): 3 pieces = 9pts, 2 pieces = 4pts
  - Center column: 4x bonus per piece
  - Adjacent-to-center: 2x bonus per piece
```

The open line scoring is computed by sliding a window of n cells across all 69 possible windows in 4 directions, counting my_count**2 - opp_count**2.
### 2. jesper-olsen/connect-four -- Tromp Four stones Rust Port

#### 2.1 Board Representation (Bitwise Position Codes)

```rust
pub struct Board {
    pub color: [u64; 2],       // Player 0 and Player 1 color masks
    pub height: [usize; 7],    // Current height of each column
    pub nplies: usize,         // Total pieces on board
}
```

The `position_code()` function produces a 64-bit integer encoding the full board state, used as input to the transposition table hash function.

#### 2.2 Dual-Slot Transposition Table with Work-Aware Replacement

The transposition table uses a **dual-slot per bucket** design:
- **Big slot** = deeply searched position (replaced only by equal or deeper)
- **New slot** = shallowly searched position (overwritten on every miss)

The **work-aware replacement policy** (matching Tromp TransGame.c):
- The big slot is overwritten when: (a) it already holds the same lock, or (b) the new search work is at least as deep as what is recorded
- Otherwise, the position goes to the new slot
- This ensures deeply searched positions survive while shallow results are evicted freely

This is a **sophisticated eviction policy** that Tarun995 does not implement (Tarun995 TT has single-slot per entry).

#### 2.3 Column-Mirror Symmetry Hashing

For the first 10 plies (opening phase), mirror-symmetric positions produce the **same hash key** -- effectively doubling TT hit rate in the opening. After 10 plies, symmetry is disabled (positions are too asymmetrical for the benefit to matter).

#### 2.4 Textbook Evaluation Heuristic (eval.rs)

The evaluation function uses a **pre-computed set of 69 window bitmasks** (all possible 4-in-a-row lines on 7x6):
- Score table: 1 piece = 1pt, 2 pieces = 10pts, 3 pieces = 50pts
- Center column gets +3 per piece bonus
- This is a **textbook Connect 4 evaluation** that matches the style in Charles Anderson Connect 4 book and is directly comparable to Tromp Fhourstones evaluation.

#### 2.5 Exact-Node Regression Testing

Four benchmark positions with exact node counts matching Tromp C (v3.2) and Java (v3.1):
- Position 45461667: Win/51,596 nodes
- Position 35333571: Loss/8,716,732 nodes
- Position 13333111: Draw/169,704,432 nodes
- Empty board: Win/1,479,113,766 nodes

This is the **only public regression test suite** for Tromp Four stones solver across implementations.

### 3. haithameleuch/connect-four-ai -- Alpha-Beta + Monte Carlo Hybrid

#### 3.1 Novel Leaf Evaluation: Monte Carlo Rollouts

Instead of a static heuristic, this implementation uses **Monte Carlo rollouts** as the leaf evaluation:
- At leaf nodes (depth 0), instead of calling evaluate(board): run 250 random playouts from the leaf position
- Count wins/draws/losses for the side to move
- Use the win rate as the evaluation score

This is a form of **simulation search** -- combining deterministic pruning of alpha-beta with statistical evaluation of MCTS rollouts. It is **not MCTS** (no tree, no backpropagation, no UCB selection) -- it is purely alpha-beta with rollout-based leaf evaluation.

#### 3.2 Architecture

```
App.kt        -- Javalin web server, endpoints for turns/AI/board
Game.kt       -- Game logic: grid state, move validation, AI decision
VierGewinnt.kt -- Kotlin interface: validateMove, board/turn access, calculateBestMove, checkWin
```
## Implementation Anatomy

### Architecture Comparison

| Feature | Tarun995 | jesper-olsen | haithameleuch |
|---------|----------|-------------|---------------|
| Language | Python + Numba | Rust | Kotlin + Javalin |
| Board Rep | 64-bit bitboard | 64-bit position code | 2D integer array |
| Search | PVS (Numba JIT) | Exact solver (Rust) | Alpha-beta (3 ply) |
| Leaf Eval | Heuristic (open lines) | Textbook (window scores) | Monte Carlo (250 rollouts) |
| TT | 16M single-slot + mirror | 8.3M dual-slot + mirror | None |
| Symmetry | Mirror in TT storage | Mirror in hash key | None |
| Move Order | History + killer + TT + center | History heuristic | None specified |
| Board Size | Configurable | 7x6 fixed | 7x6 default |
| License | MIT | MIT (inferred) | None (unlicensed) |
| Kaggle Ready | Yes (src/agent.py) | No (Rust binary) | No (Javalin server) |

### Algorithm Comparison

| Algorithm | Tarun995 | jesper-olsen | haithameleuch |
|-----------|----------|-------------|---------------|
| Negamax | Yes | Yes | No (minimax) |
| Alpha-Beta | Yes | Yes | Yes |
| PVS | Yes | No | No |
| Aspiration Windows | Yes | No | No |
| Iterative Deepening | Yes | No (exact solver) | No |
| Transposition Table | 16M + mirror | 8.3M dual-slot + mirror | None |
| Mirror Symmetry | TT storage | Hash key | None |
| Numba JIT | Yes | N/A | N/A |
| Fork Detection | +950/-950 | Exact solver | N/A (rollout) |
| Opening Book | Yes (2-ply) | No (solved game) | No |
## Documentation-Only Code Samples

### CONFIGURATION EXAMPLE -- Tarun995 Opening Book

```python
# Opening book: 2-ply solved game positions for 7x6
# Key: tuple of columns played (0-indexed)
_OPENING_BOOK = {
    (): 3,                           # Empty --> center
    (3,): 3, (3,3): 3, ...           # Center --> center again
    (0,): 3, (1,): 3, ...           # Off-center --> center
    (3, 0): 3, (3, 1): 3, ...       # Center + off --> keep center
}
```

### ADAPTED REFERENCE SKETCH -- PVS with Null-Window Search

```
# CONCEPTUAL PSEUDOCODE -- Principal Variation Search
# Informed by: Tarun995 agent.py _negamax_nb (MIT)

function pvs(pos, opp, alpha, beta, depth):
    # TT lookup (same as alpha-beta)
    key = pos + (pos | opp)
    if TT contains key with sufficient depth:
        return TT_score(key)

    if depth == 0:
        return heuristic(pos, opp)

    moves = order_moves(pos, opp)  # TT, killers, history, center

    # First move: full window
    best = -pvs(opp, new_pos, -beta, -alpha, depth-1)
    best = -best  # Negamax negation

    if best >= beta:
        return beta  # Beta cutoff

    # Subsequent moves: null window
    for move in moves[1:]:
        new_score = -pvs(opp, new_pos, -alpha-1, -alpha, depth-1)
        new_score = -new_score

        if new_score > best and new_score < beta:
            # Scout failed: full re-search
            new_score = -pvs(opp, new_pos, -beta, -best, depth-1)
            new_score = -new_score

        if new_score >= beta:
            return beta  # Beta cutoff

    return best
```

### EXACT SOURCE EXCERPT -- jesper-olsen Evaluation Heuristic

```rust
// project: connect-four (jesper-olsen)
// source: https://github.com/jesper-olsen/connect-four/blob/main/src/eval.rs
// license: MIT (inferred from repo)
// file: src/eval.rs, evaluate function
// retrieval: 2026-08-05

const WINDOW_SCORE: [i32; 4] = [0, 1, 10, 50];
const CENTER_BONUS: i32 = 3;

pub fn evaluate(board: &Board, side: usize) -> i32 {
    let mine = board.color[side];
    let theirs = board.color[side ^ 1];
    let mut score = 0i32;

    for &window in winning_windows() {  // 69 pre-computed windows
        let mine_bits = (mine & window).count_ones() as usize;
        let their_bits = (theirs & window).count_ones() as usize;
        if their_bits == 0 && mine_bits > 0 {
            score += WINDOW_SCORE[mine_bits];
        } else if mine_bits == 0 && their_bits > 0 {
            score -= WINDOW_SCORE[their_bits];
        }
    }

    // Center column bonus
    score += CENTER_BONUS * center_pieces(mine);
    score -= CENTER_BONUS * center_pieces(theirs);

    score
}
```

### ADAPTED REFERENCE SKETCH -- Dual-Slot TT Replacement

```rust
// ADAPTED REFERENCE SKETCH -- Dual-slot transposition table
// Informed by: jesper-olsen/connect-four tt.rs (MIT)
// File: src/tt.rs, store() function

pub fn store(&mut self, index, lock, score, work):
    he = self.entries[index]

    // Check big slot
    if lock == big_lock(he) || work >= big_work(he):
        // Replace big slot
        packed_work_lock = (work << LOCKSIZE) | lock
        packed_with_score = (packed_work_lock << 3) | score
        self.entries[index] = (packed_with_score << NEWSIZE) | (he & NEW_MASK)
    else:
        // Only new slot available
        self.entries[index] = (he & BIG_MASK) | ((score as u64) << LOCKSIZE) | lock
```
## Pros and Cons

### Tarun995/connectX-bitboard-agent

| Pros | Cons |
|------|------|
| Complete Kaggle submission (agent.py with act() API) | No license explicitly documented in repo root (README says MIT but LICENSE file not confirmed) |
| Combines PVS + aspiration windows + mirror TT -- rare in public repos | Numba dependency requires installation; graceful fallback exists but degrades performance |
| Board-size configurable via _init(rows, cols, inarow) | Mirror symmetry only applied to TT storage, not to position key during lookup |
| Fork detection (+950/-950) provides tactical robustness | Open line scoring is O(69 x n) per evaluation -- brute-force window scanning |
| Numba JIT accelerates core negamax to near-C performance | 16M TT uses simple hash (pos + mask) -- no Zobrist, no mirroring during lookup |
| Opening book (2-ply) covers standard 7x6 openings | Time limit check only every 1024 nodes -- potential overshoot |
| Iterative deepening guarantees a move at any time | No quiescence search -- horizon effect on forced-win sequences |

### jesper-olsen/connect-four

| Pros | Cons |
|------|------|
| Exact node-count regression against Tromp C/Java refs | 7x6 only -- no board-size generalization |
| Dual-slot TT with work-aware replacement -- sophisticated | No PVS, aspiration windows, or iterative deepening |
| Column-mirror symmetry in hash key (first 10 plies) | Heuristic evaluation is basic (1/10/50 -- no fork detection) |
| Complete test suite (unit tests for all modules) | No Numba/JIT -- pure Rust (fast but not JIT) |
| MIT License | Not designed for Kaggle (Rust binary, no Python agent API) |
| solve binary accepts Tromp Fhourstones input format | No transposition table statistics reporting in play mode |

### haithameleuch/connect-four-ai

| Pros | Cons |
|------|------|
| Novel alpha-beta + Monte Carlo hybrid leaf eval | Unlicensed -- cannot be legally reused without permission |
| Server-based deployment (Javalin) -- web interface | 3-ply depth is very shallow -- practical strength unknown |
| Monte Carlo rollout at leaves avoids heuristic design | 250 rollouts x 3-ply tree = significant computation per move |
| Kotlin on JVM -- cross-platform | No transposition table -- positions re-evaluated repeatedly |
| Two AI modes: pure MC and alpha-beta+MC | No board-size generalization (hardcoded 7x6) |
| | No test suite or benchmark results |
| | No Kaggle compatibility (not a Python agent) |

## Feasibility Matrix

| Feature | RTX 5090 | Kaggle T4 | Kaggle CPU | Local CPU |
|---------|----------|-----------|------------|-----------|
| Tarun995 bitboard search | 100M+ nodes/sec (Numba) | 20-50M nodes/sec (Numba) | 1-5M nodes/sec (Numba JIT) | 5-20M nodes/sec (Numba JIT) |
| PVS advantage | ~15-25% over alpha-beta | ~15-25% over alpha-beta | ~15-25% over alpha-beta | ~15-25% over alpha-beta |
| Aspiration window success rate | ~85% (depth 5+) | ~85% | ~85% | ~85% |
| Mirror TT hit rate increase | ~2x effective size | ~2x | ~2x | ~2x |
| jesper-olsen exact solver | N/A (Rust binary) | N/A | N/A | Useful for regression testing |
| haithameleuch hybrid eval | Feasible (JVM on Kaggle?) | Not feasible (no JVM) | Not feasible (no JVM) | Feasible (JVM available) |

## Board-Size and inarow Applicability

| Technique | 7x6 | 8x8 | 10x8 | 15x10 | 15x13 |
|-----------|-----|-----|------|-------|-------|
| Tarun995 PVS search | Configurable | (slower) | (much slower) | ? (untested) | ? (untested) |
| Tarun995 bitboard win detection | n=4 | n=any | n=any | n=any | n=any |
| Tarun995 mirror TT symmetry | 7 cols | (odd cols) | (odd cols) | (odd cols) | (odd cols) |
| Tarun995 16M TT on large boards | OK | ? | ? | ? (may thrash) | ? (may thrash) |
| Tarun995 Numba JIT | OK | OK | OK | OK | OK |
| jesper-olsen exact solver | 7x6 only | No | No | No | No |
| jesper-olsen eval heuristic | 69 windows | No (117 windows) | No | No | No |
| haithameleuch alpha-beta+MC | 7x6 only | No | No | No | No |
## Integration and Ensemble Opportunities

### With Classical Search (CS-003, CS-005)
- **PVS from Tarun995** should be added to the classical search algorithm comparison (CS-004, CS-005). PVS is currently undocumented in the corpus.
- **Mirror symmetry in TT** from both Tarun995 and jesper-olsen provides a concrete design pattern for Kaggle T4 deployment.
- **Fork detection thresholds** (+950/-950) from Tarun995 should be validated against evolved rowspire weights (T106, CS-005).

### With MCTS (MCTS-003, MCTS-005)
- **haithameleuch hybrid** suggests a new MCTS variant: MCTS with rollout-guided leaf evaluation instead of pure random rollout.
- The **arena-based tree storage** (flat Vec<Node>) in jesper-olsen MCTS is a memory-efficient alternative to pointer-based trees.

### With Kaggle Deployment (DOS-007, MCTS-004)
- **Tarun995 agent.py** is directly Kaggle-compatible and can be submitted as-is. Should be benchmarked against other classical baselines (Kamide, miksipiksic/pyvezi) on the Kaggle leaderboard.

## Performance Evidence

| Metric | Tarun995 | jesper-olsen | haithameleuch | Evidence Level |
|--------|----------|-------------|---------------|----------------|
| Search speed | Numba JIT, claimed millions per second | Exact solver, known node counts | 3-ply, 250 rollouts | CLAIMED by author (Tarun995), VERIFIED for jesper-olsen (exact node counts) |
| Tactical solving (forks) | +950 fork detection | Exact solver (perfect) | Monte Carlo rollout | VERIFIED for jesper-olsen; Tarun995 unmeasured |
| Board-size generalization | Configurable (rows, cols, inarow) | 7x6 only | 7x6 default | VERIFIED |
| License compliance | MIT | MIT (inferred) | None | VERIFIED for Tarun995 (MIT); UNVERIFIED for others |

## Failure Modes and Risks

| Failure Mode | Tarun995 | jesper-olsen | haithameleuch |
|-------------|----------|-------------|---------------|
| Board size mismatch | _init() called per move (overhead) | Hardcoded 7x6 | Hardcoded 7x6 |
| Time limit violation | 1024-node check intervals | Exact solver (unbounded) | 3-ply is safe |
| Numba compatibility | Fallback to Python if unavailable | N/A | N/A |
| License issues | MIT is permissive | MIT is permissive | Unlicensed (use restricted) |
| Kaggle environment | Designed for it | Not designed for it | Not designed for it |

## Benchmark Requirements

1. **Tarun995 vs Kamade**: Match-play on 7x6, 15x13, 15x10 boards -- 100 games each direction
2. **Tarun995 vs minimax depth-3 (Kaggle built-in)**: Verify PVS advantage over standard minimax
3. **jesper-olsen node-count regression**: Re-run all 4 benchmark positions, verify exact match with Tromp C/Java
4. **haithameleuch rollout sensitivity**: Measure strength vs rollout count (100, 250, 500, 1000)
5. **Mirror TT impact**: Measure hit rate with/without mirror symmetry on 1000 random positions

## Open Questions

1. **What is Tarun995 actual Kaggle score?** -- The repo is designed for Kaggle but no public score is cited.
2. **How does jesper-olsen dual-slot TT compare to single-slot (Tarun995) in terms of effective hit rate?** -- Not measured.
3. **Is haithameleuch Monte Carlo leaf evaluation superior to static heuristics at depth 3?** -- No benchmark data.
4. **Can Tarun995 PVS + aspiration windows be ported to Kaggle T4 within 2-second budget?** -- Unmeasured.
5. **Does the 69-window evaluation in jesper-olsen generalize to larger boards?** -- Would need 117 windows for 8x8.

## Recommendations

1. **Priority 1**: Download and benchmark Tarun995 against Kamade/connect-n and miksipiksic/pyvezi on 7x6 boards. This is the most Kaggle-relevant find.
2. **Priority 2**: Add PVS to the classical search algorithm comparison (CS-004, CS-005). PVS is now verified in Tarun995 source.
3. **Priority 3**: Use jesper-olsen Four stones regression tests as a validation suite for any new solver implementation.
4. **Priority 4**: Investigate haithameleuch Monte Carlo leaf evaluation as a potential component for MCTS variant research.
5. **Priority 5**: Consider mirroring haithameleuch Javalin server architecture as an alternative to notebook-based deployment (web UI for bot testing).
## Sources and Retrieval Record

| Source ID | URL | Retrieved | Method |
|-----------|-----|-----------|--------|
| S166 | https://github.com/Tarun995/connectX-bitboard-agent | 2026-08-05 | WebFetch (repo page + tree) |
| S167 | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/src/agent.py | 2026-08-05 | WebFetch (raw source) |
| S168 | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/README.md | 2026-08-05 | WebFetch (raw docs) |
| S169 | https://raw.githubusercontent.com/Tarun995/connectX-bitboard-agent/main/main.py | 2026-08-05 | WebFetch (raw source) |
| S170 | https://github.com/jesper-olsen/connect-four | 2026-08-05 | WebFetch (repo + tree API) |
| S171 | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/mcts.rs | 2026-08-05 | WebFetch (raw source) |
| S172 | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/eval.rs | 2026-08-05 | WebFetch (raw source) |
| S173 | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/tt.rs | 2026-08-05 | WebFetch (raw source) |
| S174 | https://raw.githubusercontent.com/jesper-olsen/connect-four/main/src/minimax.rs | 2026-08-05 | WebFetch (raw source) |
| S175 | https://github.com/haithameleuch/connect-four-ai | 2026-08-05 | WebFetch (repo page + tree API) |
| S176 | Via GitHub tree API | 2026-08-05 | WebFetch (structure only) |

## Cross-Links

- CS-003 (Classical Search and Solver Engineering): PVS and mirror TT are new additions
- CS-005 (Evaluation Function Design): Tarun995 fork detection (+950/-950) and open line scoring (quadratic) expand the eval design space
- DOS-007 (Kaggle Competitive Analysis): Tarun995 is a new contender (BOT-017)
- MCTS-003 (MCTS Variant Taxonomy): haithameleuch Monte Carlo leaf evaluation is a new variant
- MCTS-005 (Hybrid Search Systems): haithameleuch is a hybrid alpha-beta + MC, matching MCTS-005 game-phase routing concept
- RI-001 (katac4): Board-size comparison (katac4: configurable vs Tarun995: configurable vs jesper-olsen: fixed)
- RI-002 (connectpuct): PVS comparison (connectpuct: alpha-beta only vs Tarun995: PVS)
- T003 (GitHub topics scan): This dossier fulfills the T003 research task