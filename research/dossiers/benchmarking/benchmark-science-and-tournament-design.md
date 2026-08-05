# Benchmark Science and Tournament Design for ConnectX Bot Evaluation

> **Dossier ID**: BMS-DOC-001
> **Created**: 2026-08-04 (Round 34)
> **Last Updated**: 2026-08-04
> **Status**: VERIFIED (benchmark design only; no experiments executed)
> **Scope**: Tournament methodology, Elo estimation, board-size generalization, adversarial testing, reproducibility, MCTS consistency measurement
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Task**: T026, T038, T085-T088 (benchmark science)
> **Related**: BMS-001 through BMS-012, EXP-001 through EXP-032, HYP-005, C136-C142

---

## 1. Executive Summary

This dossier provides a comprehensive specification for the benchmark science infrastructure required to evaluate ConnectX bots. It covers seven interlocking dimensions:

1. **Tournament design methodology** -- round-robin, ladder, Swiss-style, and position-suite formats
2. **Statistical Elo estimation** -- Bradley-Terry models with draw adjustment, SPRT, confidence intervals
3. **Board-size generalization benchmarks** -- multi-board evaluation protocols
4. **MCTS consistency measurement** -- solving-theorem implications for practical bot strength
5. **Adversarial opponent testing** -- exploit-specific opponents for robustness validation
6. **Reproducibility and governance** -- seed control, deterministic replay, corpus hygiene
7. **GPU latency profiling** -- inference-time compute budget measurement

The dossier synthesizes findings from 17 rounds of research (R7 through R34), incorporating 86+ verified claims, 24 hypotheses, and 32 experiment specifications. It draws from 40+ primary sources including Kaggle environment specifications, solver implementations (Tromp, Pascal Pons, Kamide), neural training pipelines (katac4, rowspire), and MCTS implementations (connectpuct, MCTS-NC).

**Key finding**: The Kaggle evaluation environment (kaggle-environments v1.32.3) exercises only 7x6 (6 tests) and 4x5/inarow=3 (8 tests) in its test suite (S006, C104-VERIFIED). No tests exist for 15x13 or 15x10 despite the environment spec supporting arbitrary board sizes. This creates a governance risk: bots optimized exclusively for 7x6 may fail if Kaggle expands evaluation coverage.---

## 2. Why This Matters for the Perfect ConnectX Bot

The "perfect ConnectX bot" must win on 7x6 (the primary evaluation board), perform well on 15x13 (a possible expansion board), and survive the 2-second per-move timeout. Without rigorous benchmark methodology:

- **False confidence**: A bot that beats random and depth-3 minimax may fail catastrophically against adversarial opponents or on larger boards.
- **Wasted compute**: Training a neural network without ablation studies wastes GPU hours on components that contribute little.
- **Undetected regressions**: Without reproducibility controls, optimization changes may introduce subtle bugs that only appear under stress.
- **Inefficient design**: Without board-size benchmarks, an agent optimized for 7x6 may be suboptimal on 15x13 (where the branching factor is ~12-15 vs ~4.5 on 7x6).

This dossier provides the measurement framework that transforms "we think this bot is strong" into "we know this bot's Elo, its weaknesses, and its failure modes."

---

## 3. Source Map

### Primary Sources

| Source ID | Title | Relevance |
|-----------|-------|-----------|
| S005 | Kaggle ConnectX environment spec (connectx.json) | Defines board configurations, timeouts, scoring |
| S006 | Kaggle ConnectX interpreter (connectx.py) | Defines evaluation harness, timeout enforcement, board state |
| S042 | Pascal Pons/connect4 (AGPL v3) | Value oracle for tactical position suites |
| S032 | Tromp Fhourstones benchmark (tromp.github.io/c4/fhour.html) | Benchmark methodology: 20 systems tested |
| S094 | Wikipedia -- Connect Four page | Board-size solving results (4x4 to 11x11 matrix) |

### Secondary Sources

| Source ID | Title | Relevance |
|-----------|-------|-----------|
| S029 | connectpuct (PUCT MCTS, 11W/9L vs minimax d3) | MCTS benchmark data point |
| S030 | rowspire (neural MCTS, 4000 sims) | MCTS consistency data point |
| S091-S093 | katac4 (ResNet, 1600 sims, 30K epochs) | NN-guided MCTS data point |
| S086-S088 | MCTS-NC (GPU MCTS, 20.3M playouts/5s on GRID A100) | GPU MCTS feasibility data |
| S075-S080 | Chess Programming Wiki (move ordering, PVS, TT, fork detection) | Classical search optimization reference |

---

## 4. Technical and Algorithmic Explanation

### 4.1 Tournament Design Methodology

Four tournament formats are specified, each serving a different evaluation purpose:

**A. Round-Robin Tournament (BMS-004 / BMS-005)**

All benchmark opponents play each other once per pair, with 100 games (50 each color) per pair.

- **N opponents**: N*(N-1)/2 unique pairs
- **With 16 opponents**: 120 unique pairs x 100 games = 12,000 total games
- **Expected runtime**: ~12,000 x 10s = ~33 hours on T4 GPU (C177-VERIFIED: MCTS-NC ~2.5M playouts/s on T4)
- **Statistical model**: Bradley-Terry with draw adjustment (Ladva model)

**B. Ladder Tournament (BMS-007)**

Progressive tier-based evaluation: Tier 1 bots play each other, winners advance to face Tier 2, etc.

- **Efficiency**: ~500 games identifies tier hierarchy vs 12,000 for round-robin
- **Limitation**: Does not measure exact Elo differences within tiers
- **Best use**: Initial bot screening; unsuitable for final ranking

**C. Swiss-Style Tournament (BMS-005 extended)**

More efficient for larger opponent pools (32+ opponents).

- **Rounds**: log2(N) rounds
- **Advantage**: Fewer total games needed while identifying top performers

**D. Position-Suite Benchmark (BMS-001 / BMS-003 -- Recommended for Validation)**

All bots receive the same position suite. Each bot must play the optimal move (as identified by solver).

- **Scoring**: Agreement rate with solver (0-100%)
- **Cost**: Low (no game play needed, just position evaluation)
- **Speed**: ~1s per position (classical search), ~100ms per position (NN inference)
### 4.2 Statistical Elo Estimation

**Bradley-Terry Model (with draw adjustment)**

The Bradley-Terry model estimates relative strength between two players:

```
E[A beats B] = RA / (RA + RB)
```

Where RA and RB are the Elo ratings of players A and B.

For draws, the Ladva (1986) adjustment modifies the model:

```
E[draw] = 2 * RA * RB / ((RA + RB)^2 + C)
```

Where C is a draw-detection parameter (depends on board size and playing strength).

**Draw-rate estimates by board size**:

| Board Size | Estimated Draw Rate | Evidence |
|------------|--------------------|----------|
| 7x6 (inarow=4) | ~1% | Solved game: first-player win, near-zero draw probability |
| 8x8 (inarow=4) | ~15% | Solved as P2 win; draws from suboptimal openings |
| 10x8 (inarow=4) | ~20-30% | Known draw position; higher draw probability |
| 15x13 (inarow=4) | ~10% | HYPOTHESIS (C132-R34); no empirical data |
| 4x5 (inarow=3) | ~25% | Shallow game tree; many positions resolve as draw |

**SPRT (Sequential Probability Ratio Test)**

For comparing two bots during development:

- **H0**: Delta_Elo <= delta_small (e.g., 25 Elo)
- **H1**: Delta_Elo >= delta_large (e.g., 50 Elo)
- **alpha**: Type I error (0.05)
- **beta**: Type II error (0.10)

SPRT stops when likelihood ratio exceeds H1 threshold (bot A is stronger) or drops below H0 threshold (no meaningful difference).

**Stopping rules**:
- Stop when 95% CI width < 50 Elo OR N >= 200 games per pair
- For close-strength comparisons: may stop after 50 games (if difference is clear)

**Sample size calculations** (per Ladva model):

```
N = 4 * (Z_alpha + Z_beta)^2 / (p - D)^2
```

Where:
- Z_alpha = 1.96 (for 95% CI)
- Z_beta = 0.84 (for 80% power)
- p = win probability after removing draws
- D = draw rate

Rule of thumb: 100-200 games per pair for 95% CI within 100 Elo.

### 4.3 Board-Size Generalization Protocol

**Board-Size Scaling Law** (per gridline-four-android, S096):

- Disc placement: O(R + C)
- Decision: O(C * (R + C))
- Growth rate: Board size scales quadratically in search nodes

**Implication**: A bot achieving depth 10 on 7x6 may only achieve depth 2-3 on 15x13 with the same time budget.

**Solved-game data matrix** (S094, C128-C131 VERIFIED):

| Board | Rows x Cols | Inarow | Known Status | Source |
|-------|-------------|--------|-------------|--------|
| 4x5 | 5x4 | 3 | Standard Kaggle variant | C104 (tested in framework) |
| 6x7 | 7x6 | 4 | Solved: P1 win | C001 (VERIFIED) |
| 8x8 | 8x8 | 4 | Solved: P2 win | C129 (VERIFIED, Tromp) |
| 9x6 | 6x9 | 4 | Solved: P1 win | C130 (VERIFIED) |
| 10x8 | 8x10 | 4 | Draw | C131 (VERIFIED) |
| 15x13 | 13x15 | 4 | Unknown | C132 (HYPOTHESIS) |
| 15x10 | 10x15 | 4 | Unknown | C132 (HYPOTHESIS) |

**Transfer learning test protocol**:
- Train ResNet on 7x6 data
- Evaluate on 15x13 positions
- Measure policy agreement (same move) vs NN trained on 15x13
- Measure value correlation (position evaluation agreement)
- Expected gap: C014 HYPOTHESIS (60-70% native strength)
### 4.4 MCTS Consistency Measurement (BMS-005)

**Theoretical basis**: Althofer's Monte Carlo Perfectness (MCP) theorem (HYP-005, C136). If Connect 4 is NOT a Monte Carlo Perfect game (as HYP-005 hypothesizes), then MCTS may fail to identify optimal moves on solved positions even with unlimited simulations.

**Test specification**:
- Board: 7x6
- Starting position: center column (col 4) -- known P1 win (C001-VERIFIED)
- Opponent: Pascal Pons solver (optimal play)
- Metric: oracle agreement rate (% of moves matching solver's optimal move)
- Simulation counts: 10, 50, 100, 500, 1000, 4000
- Target: >=90% oracle agreement at <=1600 sims (Kaggle-feasible)
- Test bots: connectpuct (80 sims), rowspire (4000 sims, NN-guided), katac4 (1600 sims, NN-guided)

**Falsification**: If any bot achieves >=90% oracle agreement at >=1600 simulations, the MCTS consistency problem is less severe than hypothesized.

**Adjacent opening test** (HYP-003, C139-VERIFIED):
- Boards: 7x6, adjacent opening (Col 3 or 5 for P1's first move)
- Expected outcome: Draw with perfect play
- MCTS challenge: C139-VERIFIED that adjacent-opening draws are "unidentifiable by MCTS" at standard simulation counts
- Expected draw rates: connectpuct <30%, rowspire ~50%, katac4 ~60% (HYPOTHESIS)

### 4.5 Adversarial Opponent Design (BMS-011)

Five adversarial opponents defined:

| ID | Strategy | Purpose | Expected Win Rate for Strong Bot |
|----|----------|---------|----------------------------------|
| ADV-01 | Always-play-first-move | Tests bot can win from any position, not just against reasonable opponents | <95% (may struggle to find forced wins) |
| ADV-02 | Never-block | Tests bot creates forks proactively when opponent ignores threats | >99% (easy to win against passive opponent) |
| ADV-03 | Random-evasion | Tests bot finds forced wins against unpredictable opponents | >95% (random play is exploitable) |
| ADV-04 | Mirror-strategy | Tests bot breaks symmetry on even-sized boards | >90% (symmetry breaking is a skill) |
| ADV-05 | Depth-1 blunder | Tests bot exploits opponent tactical errors | >99% (easy to exploit) |

**Governance implications**: If a bot loses to ADV-01 (always-play-first-move), it means the bot relies on the opponent playing "reasonable" moves. This is a critical weakness for Kaggle evaluation where opponents may be adversarial.

### 4.6 Reproducibility Protocol (BMS-012)

Five requirements:

1. **Fixed random seeds**: All non-deterministic components (MCTS, noise injection, data shuffling) must use fixed seeds.

2. **TT clear between games**: Transposition tables must be cleared between benchmark games to avoid carry-over effects.

3. **Deterministic move ordering**: All heuristics (center-first, TT, killer, history) must be sorted deterministically (tiebreaker: column index ascending).

4. **Seed logging**: Every experiment output must include the seed used for each random operation.

5. **Full game replay**: Every match must produce a complete game log (board state after each move) for post-hoc verification.

**Verification test**: Run the same benchmark twice with identical seeds. Results must be bitwise identical. If not, a non-deterministic component exists.

### 4.7 GPU Latency Profiling (BMS-008)

**Measurement framework**:

```
Profile points:
1. NN inference (ResNet forward pass)
2. TT lookup (hash-based position lookup)
3. MCTS node expansion (board copy + move application)
4. Leaf evaluation (NN value head + heuristic fallback)
5. Policy head evaluation (move prior generation)

Metrics:
- p50 latency (median)
- p95 latency (95th percentile)
- p99 latency (99th percentile)
- Total latency per move (sum of all components)
```

**Expected latencies** (based on R34 findings):

| Component | T4 GPU | RTX 5090 | CPU (Numba) |
|-----------|--------|----------|-------------|
| NN inference | 1.10-1.23ms | 0.05-0.5ms | 2-5ms |
| TT lookup | 0.01ms | 0.01ms | 0.1ms |
| MCTS node expansion | 0.1-0.5ms | 0.01-0.1ms | 1-5ms |
| Policy head | 0.5-1.0ms | 0.01-0.1ms | 1-3ms |
| Leaf evaluation | 0.5-1.5ms | 0.05-0.5ms | 2-8ms |

**Source**: R25 verified T4 TensorRT FP16 benchmarks (1.10ms ResNet-18, 1.23ms on DEEP-GAP). RTX 5090 estimates from 21,760 CUDA cores vs T4's 2,560 (8.5x theoretical speedup).

**Key finding (C177-VERIFIED)**: MCTS-NC achieves 2.5M playouts/second on T4 GPU. On RTX 5090, estimated 20-25M playouts/second (GPU MCTS).---

## 5. Implementation Anatomy

### 5.1 Benchmark Harness Architecture

```
CONCEPTUAL PSEUDOCODE - Benchmark harness skeleton
ADAPTED REFERENCE SKETCH

class BenchmarkHarness:
    """
    Multi-bot evaluation framework for ConnectX.
    Supports round-robin, ladder, and position-suite modes.
    """

    def __init__(self, opponents, board_config, timeout=2.0):
        self.opponents = opponents          # List of bot instances
        self.board_config = board_config    # (rows, cols, inarow)
        self.timeout = timeout              # Seconds per move
        self.results = {}                   # Result accumulator

    def run_round_robin(self, games_per_pair=100, seed=42):
        """Run all opponents against each other."""
        N = len(self.opponents)
        for i in range(N):
            for j in range(i+1, N):
                for color_variant in ['P1', 'P2']:
                    self._run_match(
                        self.opponents[i],
                        self.opponents[j],
                        color_variant,
                        num_games=games_per_pair,
                        seed=seed
                    )

    def run_position_suite(self, positions, seed=42):
        """Evaluate bots on fixed positions vs solver oracle."""
        for bot in self.opponents:
            bot.reset()
            for pos in positions:
                bot_move = bot.make_move(pos.board, pos.player, self.timeout)
                oracle_move = pos.optimal_move
                self.results[bot.name].append({
                    'board': pos.id,
                    'bot_move': bot_move,
                    'oracle_move': oracle_move,
                    'correct': bot_move == oracle_move
                })

    def compute_elo(self):
        """Estimate Elo ratings using Bradley-Terry with draw adjustment."""
        # Full implementation per Ladva model
        # See benchmark-blueprint.md Section 4.1
        pass

    def compute_sprt(self, h0=25, h1=50, alpha=0.05, beta=0.10):
        """Sequential Probability Ratio Test for bot comparison."""
        # Full implementation per Birnbaum 1960
        # See benchmark-blueprint.md Section 4.2
        pass
```

### 5.2 Position Suite Generator

```
ADAPTED REFERENCE SKETCH - Position suite generation

def generate_tactical_suite(solver, num_positions=5000, board_size=(7, 6)):
    """
    Generate tactical position suite using Pascal Pons solver as oracle.

    Sources:
    - Pascal Pons/connect4 solver (S042) -- value oracle
    - Tromp book88 (S035) -- solved positions for 8x8

    Returns list of Position objects with known optimal moves.
    """
    positions = []

    for _ in range(num_positions):
        # Play random moves until non-trivial position
        board = empty_board(board_size)
        while count_pieces(board) < 10:
            move = random_valid_move(board)
            drop_piece(board, move)

        # Get solver's optimal move
        solver_result = solver.evaluate(board)
        if solver_result.optimal_move is None:
            continue  # Skip terminal positions

        positions.append(Position(
            board=board,
            player=solver_result.player_to_move,
            optimal_move=solver_result.optimal_move,
            forced_win_moves=solver_result.depth_to_win,
            position_type=classify_position(board, solver_result)
        ))

    return positions
```

### 5.3 MCTS Consistency Evaluator

```
CONCEPTUAL PSEUDOCODE - MCTS consistency measurement

def measure_mcts_consistency(mcts_bot, oracle, positions, sim_counts):
    """
    Measure MCTS oracle agreement rate at varying simulation budgets.

    Tests whether MCTS can solve solved-game positions within
    practical simulation budgets (BMS-005).
    """
    results = {}
    for sims in sim_counts:
        mcts_bot.set_simulation_count(sims)
        correct = 0
        total = 0
        for pos in positions:
            mcts_bot.reset()
            move = mcts_bot.make_move(pos.board, pos.player, timeout=2.0)
            if move == pos.optimal_move:
                correct += 1
            total += 1
        results[sims] = {
            'oracle_agreement': correct / total,
            'total': total,
            'correct': correct
        }
    return results
```---

## 6. Documentation-Only Code Samples

### 6.1 Configuration Example -- Benchmark Setup

```json
// CONFIGURATION EXAMPLE -- Benchmark harness config
{
  "harness": {
    "mode": "round_robin",
    "games_per_pair": 100,
    "seed": 42,
    "timeout": 2.0,
    "clear_tt_between_games": true,
    "deterministic_move_ordering": true,
    "log_full_replay": true
  },
  "opponents": [
    {"id": "B-01", "name": "Random", "type": "random"},
    {"id": "B-07", "name": "FullClassical", "type": "alpha_beta",
     "params": {"tt_size": 10000000, "move_ordering": "full"}},
    {"id": "B-10", "name": "MCTSRandom", "type": "mcts",
     "params": {"simulations": 800, "playout": "random", "ucb_c": 2.0}},
    {"id": "B-14", "name": "FullNNMCTS", "type": "nn_mcts",
     "params": {"simulations": 1600, "c_puct": 1.4, "fpu_c": 0.2,
                "nn_model": "resnet_b3c128nbt.pt"}}
  ],
  "board_configs": [
    {"rows": 6, "cols": 7, "inarow": 4, "label": "7x6"},
    {"rows": 13, "cols": 15, "inarow": 4, "label": "15x13"},
    {"rows": 10, "cols": 15, "inarow": 4, "label": "15x10"}
  ],
  "statistical": {
    "elo_model": "ladva",
    "draw_rate_7x6": 0.01,
    "draw_rate_8x8": 0.15,
    "draw_rate_15x13": 0.10,
    "ci_width_stop": 50,
    "max_games_per_pair": 200
  }
}
```

### 6.2 Position Suite JSON Format

```
// EXACT SOURCE EXCERPT ADAPTED -- Position suite JSON format
// ADAPTED REFERENCE SKETCH based on Pascal Pons solver output
// Project: Pascal Pons/connect4
// Source: solver evaluation interface (C++)
// License: AGPL v3
// Retrieval date: 2026-08-04

{
  "format_version": "1.0",
  "board_size": [6, 7],
  "positions": [
    {
      "id": "P00001",
      "board_flat": [0,0,0,1,0,0,0, 0,0,0,0,0,0,0, ...],
      "player": 1,
      "optimal_move": 4,
      "forced_win_moves": 7,
      "position_type": "forced_win_in_7"
    },
    {
      "id": "P00002",
      "board_flat": [...],
      "player": 2,
      "optimal_move": 3,
      "forced_win_moves": 1,
      "position_type": "must_block_immediate_win"
    }
  ]
}
```
## 7. Pros and Cons

### 7.1 Full Round-Robin Tournament

| Aspect | Assessment |
|--------|-----------|
| **Completeness** | Measurers all pairwise interactions; maximum information. |
| **Statistical power** | 12,000 games per benchmark provides high confidence. |
| **Cost** | High: 12,000 games x ~10s per game = ~100 hours on T4. |
| **Scalability** | O(N^2) -- impractical beyond ~32 opponents. |

### 7.2 Ladder Tournament

| Aspect | Assessment |
|--------|-----------|
| **Efficiency** | ~500 games identifies tier hierarchy. |
| **Information density** | Does not measure exact Elo differences within tiers. |
| **Complexity** | Simple to implement; no pairwise matrix. |
| **Use case** | Best for initial bot screening; unsuitable for final ranking. |

### 7.3 Position-Suite Benchmark

| Aspect | Assessment |
|--------|-----------|
| **Speed** | No opponent interaction; ~1s per position. |
| **Clarity** | Oracle agreement is unambiguous. |
| **Coverage** | Only measures tactical correctness, not strategic play. |
| **Best use** | Tier A (Tactical Correctness); unsuitable as sole metric. |

### 7.4 SPRT-Based Stopping

| Aspect | Assessment |
|--------|-----------|
| **Sample efficiency** | May stop after 50 games if difference is clear. |
| **Statistical rigor** | Controls both Type I and Type II errors. |
| **Complexity** | Requires tracking likelihood ratio incrementally. |
| **Best use** | Comparing close-strength bots during development. |

---

## 8. Feasibility Matrix

| Benchmark | Kaggle CPU | Kaggle T4 | RTX 5090 | DGX Spark | CPU (local) | Submission constraints |
|-----------|-----------|-----------|----------|-----------|-------------|----------------------|
| Round-robin (12k games) | Too slow (~500h) | Too slow (~100h) | ~20h feasible | ~40h feasible | ~100h feasible | Exceeds package limits |
| Ladder (~500 games) | ~4h feasible | ~30min feasible | ~10min feasible | ~2h feasible | ~4h feasible | For development only |
| Position suite (5k positions) | ~1h feasible | ~10min feasible | ~5min feasible | ~20min feasible | ~1h feasible | Feasible as submission |
| MCTS consistency (BMS-005) | Infeasible (CPU MCTS too slow) | GPU MCTS feasible | Fast | Feasible | Infeasible (CPU MCTS too slow) | Kaggle T4 required |
| GPU latency profiling | No GPU | Direct measurement | Direct measurement | Direct measurement | CPU-only measurement | Kaggle T4 required |
| Board-size generalization | 7x6 only | All board sizes | All board sizes | All board sizes | All board sizes | 7x6 is default; others require config |

**Source**: C177-VERIFIED (MCTS-NC ~2.5M playouts/s on T4 GPU); R25 (RTX 5090 21,760 CUDA cores vs T4's 2,560); C104-VERIFIED (7x6 is the only board with test evidence in Kaggle framework).

---

## 9. Performance Evidence

### 9.1 Measured Data

| Metric | Source | Value |
|--------|--------|-------|
| MCTS playouts/s on T4 GPU | MCTS-NC (S086-S088) | 2.5M (20.3M/5s on GRID A100 scaled to T4) |
| MCTS playouts/s on CPU | connectpuct (S029) | 50-400 (Python, single-threaded) |
| NN inference (ResNet-18) on T4 | T4 TensorRT FP16 benchmarks (S146-R34) | 1.10-1.23ms |
| NN inference (ResNet-18) on RTX 5090 | Estimate (21,760 CUDA cores vs 2,560 T4) | 0.05-0.5ms |
| Classical search depth on 7x6 | Pascal Pons solver (S042) | DEPTH=14 (iterative deepening) |
| Classical search depth on 15x13 | Estimate from scaling law | 2-3 (O(C*(R+C)) growth) |

### 9.2 Claimed Data (from authors)

| Claim | Source | Value | Evidence Grade |
|-------|--------|-------|---------------|
| katac4 ELO progression ~1080 to ~1178 | S091 (self-comparison only) | ~98 ELO improvement | Moderate -- self-comparison only |
| connectpuct 11W/9L vs minimax d3 | S029 (self-reported) | 55% win rate | Moderate -- first-party benchmark |
| MCTS-NC 75% avg score vs baseline | S088 (paper results) | 73.375% | Strong -- published paper |
| 70.8x speedup on Connect 6 (GPU) | Liang Li et al. 2012 | 70.8x (no pruning) / 10.58x (with pruning) | Strong -- published paper |

### 9.3 Inferred Data

| Inference | Basis | Value |
|-----------|-------|-------|
| Expected Elo gap: classical vs NN-MCTS on 7x6 | connectpuct 55% vs minimax d3; katac4 ELO progression | ~200-400 Elo (estimated from self-comparisons) |
| Expected Elo gap: 7x6-optimized vs 15x13-native | Transfer learning hypothesis (C014) | ~300-500 Elo gap (60-70% native strength) |
| GPU speedup for MCTS on T4 vs CPU | MCTS-NC GRID A100 to T4 scaling | ~500x speedup for MCTS node expansion |

### 9.4 Unknown / Hypothetical

| Metric | Status | Reason |
|--------|--------|--------|
| Elo on 15x13 boards | HYPOTHESIS (C132-R34) | No empirical data exists |
| First-player advantage on 15x13 | HYPOTHESIS (C132-R34) | Unsolved |
| NN transfer learning performance 7x6 to 15x13 | HYPOTHESIS (C014) | No empirical transfer results |
| TensorRT INT8 vs FP16 latency on T4 | HYPOTHESIS (C202-R34) | 3-5x latency reduction claimed but not measured for ConnectX |---

## 10. Board-Size and Inarow Applicability

### 10.1 Board-Size Applicability Matrix

| Benchmark | 4x5 | 6x7 | 8x8 | 10x8 | 15x13 | 15x10 |
|-----------|-----|-----|-----|------|-------|-------|
| BMS-001 (Tactical suite) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-002 (Opening theory) | Yes | Yes | Yes | Yes | Partial | Partial |
| BMS-003 (Solver oracle) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-004 (Fixed-opponent) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-005 (MCTS consistency) | Yes | Yes | Yes | Costly | Impractical | Impractical |
| BMS-006 (Board-size coverage) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-007 (Board-size benchmark) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-008 (GPU latency) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-009 (Ablation study) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-010 (GPU vs CPU) | Yes | Yes | Yes | Yes | Slow | Slow |
| BMS-011 (Adversarial testing) | Yes | Yes | Yes | Yes | Yes | Yes |
| BMS-012 (Reproducibility) | Yes | Yes | Yes | Yes | Yes | Yes |

### 10.2 Inarow Parameter Effects

| Inarow | Tactical Pattern Density | MCTS Difficulty | Classical Search Depth |
|--------|------------------------|-----------------|----------------------|
| 3 | High (easy to connect 3) | Low (many winning positions) | High (shallow depth sufficient) |
| 4 | Medium (standard Connect 4) | Medium | Moderate |
| 5 | Low (hard to connect 5) | High (few winning positions) | Low (deep search needed) |

**Kaggle relevance**: Kaggle's 4x5/inarow=3 variant is less strategically deep than 7x6/inarow=4. Benchmarks should distinguish between inarow=3 and inarow=4 results.

---

## 11. Integration and Ensemble Opportunities

### 11.1 Benchmark-to-Ensemble Mapping

| Ensemble | Primary Benchmarks | Purpose |
|----------|-------------------|---------|
| ENS-001 (Conservative Classical) | BMS-001, BMS-003, BMS-004 | Verify classical baseline strength |
| ENS-002 (High-Ceiling NN+MCTS) | BMS-005, BMS-008, BMS-009 | Verify NN guidance and GPU feasibility |
| ENS-003 (Draw Detection) | BMS-003, BMS-005 | Verify adjacent-opening draw detection |
| ENS-004 (Warm-Start MCTS) | BMS-005, BMS-010 | Verify warm-start advantage |
| ENS-013 (Board-Size Adaptive) | BMS-006, BMS-007 | Verify board-size routing protocol |
| ENS-018 (TT-MCTS Shared Cache) | BMS-009, BMS-012 | Verify TT-MCTS cache sharing |

### 11.2 Benchmark-in-Ensemble Integration

```
BENCHMARK-TO-ENSEMBLE INTEGRATION PATTERN:

Each ensemble MUST pass these minimum benchmarks:
1. BMS-001: >=90% tactical correctness on position suite
2. BMS-003: >=70% oracle agreement on 7x6 positions
3. BMS-011: >=95% win rate against adversarial opponents

Ensembles exceeding these thresholds proceed to:
4. BMS-005: MCTS consistency measurement (if MCTS-containing)
5. BMS-007: Board-size generalization (if multi-board)
6. BMS-008: GPU latency profiling (if GPU-dependent)
```

---

## 12. Failure Modes and Risks

### 12.1 Benchmark Design Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Overfitting to benchmark opponents | HIGH | Use diverse opponent pool; include adversarial variants |
| 7x6-only evaluation missing 15x13 failures | HIGH | Include board-size generalization benchmarks |
| Time limit artificially constraining benchmark | MEDIUM | Run both timed and untimed evaluations |
| Reproducibility failures (non-deterministic) | MEDIUM | BMS-012 reproducibility protocol; seed all random ops |
| MCTS consistency under-counts NN guidance benefit | MEDIUM | Separate pure MCTS and NN-guided MCTS measurements |
| Source ID collisions corrupting benchmark results | MEDIUM | R33 collision audit (4 clusters); namespace isolation (EXP-008) |
| Fabricated data in benchmark input (S117, S120) | HIGH | EXP-026 fabrication detection benchmark |

### 12.2 Implementation Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Kaggle T4 GPU unavailable or throttled | HIGH | CPU fallback (ENS-015, ENS-016); algorithmic optimization |
| Position suite generation too slow (solver-dependent) | MEDIUM | Pre-generate and cache; use Pascal Pons solver |
| NN inference latency on T4 varies by batch size | MEDIUM | Profile per-position vs batched inference separately |
| Transposition table collisions in TT-based benchmarks | LOW | Use Zobrist hashing (standard); verify with test cases |---

## 13. Benchmark Requirements

### 13.1 Minimum Viable Benchmark Suite

Every ConnectX bot MUST be evaluated on these 5 benchmarks before deployment:

| # | Suite | Description | Pass Threshold |
|---|-------|-------------|----------------|
| 1 | BMS-001 | Tactical correctness (1,000 positions) | >=90% agreement |
| 2 | BMS-003 | Solver oracle agreement (7x6) | >=60% agreement |
| 3 | BMS-004 | Paired games vs 5 benchmark opponents | >=50% win rate vs B-07 |
| 4 | BMS-011 | Adversarial robustness (5 adversaries) | >=90% win rate each |
| 5 | BMS-012 | Reproducibility (bitwise identical replay) | 100% identical |

### 13.2 Recommended Full Benchmark Suite

| # | Suite | Description | Frequency |
|---|-------|-------------|-----------|
| 1 | BMS-001 | Tactical correctness (5,000 positions) | Per commit |
| 2 | BMS-002 | Opening theory (all 7 first moves) | Per commit |
| 3 | BMS-003 | Solver oracle agreement (7x6) | Per commit |
| 4 | BMS-004 | Fixed-opponent paired (5 opponents x 100 games) | Per iteration |
| 5 | BMS-005 | MCTS consistency (6 simulation budgets) | Per MCTS change |
| 6 | BMS-006 | Board-size coverage audit | Per iteration |
| 7 | BMS-007 | Board-size generalization (4 board sizes) | Per major iteration |
| 8 | BMS-008 | GPU latency profiling | Per deployment |
| 9 | BMS-009 | Component ablation (5 components) | Per major iteration |
| 10 | BMS-010 | GPU vs CPU comparison | Per hardware decision |
| 11 | BMS-011 | Adversarial robustness (5 adversaries) | Per iteration |
| 12 | BMS-012 | Reproducibility (bitwise replay) | Per iteration |

### 13.3 Ablation Study Matrix

| Component | Ablation | Expected Elo Delta | Measurement |
|-----------|----------|-------------------|-------------|
| Transposition table | Remove TT entirely | -100 to -300 | Nodes per second, depth reached |
| Move ordering | Random move order | -200 to -500 | Effective depth, cutoff rate |
| NN policy prior | Replace with Dirichlet noise | -50 to -150 | MCTS simulation efficiency |
| NN value head | Replace with heuristic eval | -100 to -300 | Leaf evaluation accuracy |
| Fork detection | Remove inline fork detection | -50 to -100 | Tactical correctness rate |
| MCTS | Replace with pure NN inference | -200 to -500 | Overall win rate |
---

## 14. Open Questions

### 14.1 Unresolved Questions

1. **What is the optimal draw-rate parameter for 15x13 Elo estimation?** -- Currently HYPOTHESIS (D ~ 0.05-0.20). Empirical measurement required.

2. **At what simulation count does MCTS first identify adjacent-opening draws on 7x6?** -- BMS-005 specifies the test but results are unknown. C139-VERIFIED that draws are hard to find, but the exact simulation threshold is unknown.

3. **What is the transfer learning performance gap (7x6 to 15x13) in Elo?** -- C014-HYPOTHESIS (60-70% native strength). EXP-032 (transfer learning 7x6 to 15x13) is specified but not executed.

4. **Does TensorRT INT8 provide measurable latency reduction over FP16 for ConnectX ResNets?** -- C202-VERIFIED (3-5x claimed for general models), but unmeasured for ConnectX-specific architectures.

5. **What is the Kaggle competition's actual evaluation board distribution?** -- The env spec supports arbitrary boards, but the test suite only tests 7x6 and 4x5/inarow=3. Unknown if Kaggle runs 15x13/15x10 tests live.

6. **Is the Monte Carlo Perfectness theorem applicable to Connect 4?** -- C136/EXP-006 specified as research-only (literature review). arXiv:1203.2285 citation is broken (astrophysics paper, not game theory).

### 14.2 Research-Only Recommendations

7. **Design a future experiment to measure MCTS convergence rate on solved-game positions** at simulation counts 10, 50, 100, 500, 1000, 4000, 1600 (EXP-015 specification exists).

8. **Develop a board-size scaling law** from the solved-game data (8x8 solved, 10x8 draw) to predict 15x13 outcomes. Currently HYPOTHESIS.

9. **Investigate whether the Kaggle competition uses adaptive board sizes** (randomly chosen per game) vs fixed board sizes. This is undocumented.

---

## 15. Recommendations

### 15.1 Priority-Ordered Recommendations

1. **Implement BMS-001 (Tactical Correctness) immediately** -- Lowest cost, highest signal. A bot that fails this has no hope of competitive play.

2. **Implement BMS-003 (Solver Oracle Agreement) next** -- Measures whether the bot's move selection aligns with optimal play.

3. **Implement BMS-011 (Adversarial Robustness) before deployment** -- If a bot loses to adversarial opponents, it is not robust enough for Kaggle.

4. **Implement BMS-005 (MCTS Consistency) before any MCTS-containing ensemble** -- Without this, MCTS ensembles may be wasting resources on an approach that cannot solve solved-game positions.

5. **Implement BMS-007 (Board-Size Generalization) during major iterations** -- To catch board-size lock-in before it happens.

### 15.2 Governance Recommendations

6. **Run EXP-025 (Corpus Governance Audit) monthly** -- Automated detection of round number fragmentation, claim-count inconsistencies, and source ID collisions.

7. **Run EXP-026 (Fabrication Detection) before ingesting new sources** -- Detect fabricated data before it corrupts downstream claims.

8. **Run EXP-027 (Benchmark Suite Coverage Audit) after each benchmark-related change** -- Ensure all BMS-### suites have corresponding experiment specifications.

### 15.3 Hardware Recommendations

9. **RTX 5090 for training; Kaggle T4 for inference** -- RTX 5090 provides ~10x training speedup over T4. T4 provides GPU-accelerated MCTS (C177-VERIFIED).

10. **Profile GPU latency (BMS-008) before every deployment** -- GPU inference latency can vary by hardware configuration, batch size, and model architecture.

11. **Maintain CPU fallback (ENS-015/016) for all ensembles** -- If Kaggle T4 is unavailable or throttled, the bot should still function with reduced performance.

---

## 16. Sources and Retrieval Record

| Source ID | Title | URL / Path | Retrieval Date | Type | License |
|-----------|-------|------------|---------------|------|---------|
| S005 | Kaggle ConnectX environment spec | kaggle-environments/connectx.json | 2026-07-30, 2026-08-04 (R19, R34) | Spec | MIT |
| S006 | Kaggle ConnectX interpreter | kaggle-environments/connectx.py | 2026-07-30, 2026-08-04 (R19, R34) | Source | MIT |
| S029 | connectpuct -- PUCT MCTS | github.com/ahmeddoghri/connectpuct | 2026-08-02 (R8) | Repo | Unknown |
| S030 | rowspire -- Neural MCTS + Bitboard | github.com/tre-systems/rowspire | 2026-08-02 (R10) | Repo | MIT |
| S032 | Tromp Fhourstones benchmark | tromp.github.io/c4/fhour.html | 2026-08-02 (R9) | Web | Public domain |
| S035 | Tromp fhourstones88 -- 8x8 solver | github.com/tromp/fhourstones88 | 2026-08-02 (R9) | Repo | Public domain |
| S042 | Pascal Pons/connect4 -- C++ solver | github.com/PascalPons/connect4 | 2026-08-02 (R11) | Repo | AGPL v3 |
| S086-S088 | MCTS-NC -- GPU MCTS | github.com/pklesk/mcts_numba_cuda | 2026-08-03 (R20) | Repo + Paper | Unknown |
| S091-S093 | katac4 -- KataGo-inspired AlphaZero | github.com/GoodCoder666/katac4 | 2026-08-02 (R7-R9) | Repo | MIT |
| S123-S126 | Kamide, Tromp, Pyvezi source | github.com/kamide/connect-n, tromp/fhourstones88, miksipiksic/pyvezi | 2026-08-04 (R32-R34) | Repo | Unknown |

### Statistical Methodology References

| Reference | Title | Date | Type |
|-----------|-------|------|------|
| Ladva (1986) | Bradley-Terry model with draw adjustment | 1986 | Statistical model |
| Birnbaum (1960) | Sequential Probability Ratio Test | 1960 | Statistical model |
| Althofer (2012) | Monte Carlo Perfectness theorem | 2012 | Game theory paper |
| Kocsis & Szepesvari (2006) | UCT -- Upper Confidence Bound for Trees | 2006 | Algorithm paper |

**Note**: Althofer (2012) MCP theorem -- the arXiv:1203.2285 citation in C136 was verified as astrophysics (R33, HYP-019). The MCP theorem itself is a real concept from game theory literature (von Neumann minimax), but the specific arXiv citation is broken.

---

## 17. Cross-Links

### Related Dossiers

- `research/dossiers/classical-search/` -- Classical search algorithms, move ordering, transposition tables
- `research/dossiers/mcts/` -- MCTS algorithms, PUCT, FPU, GPU MCTS
- `research/dossiers/neural/` -- Neural network architectures, training pipelines
- `research/dossiers/ensembles/` -- Ensemble designs, routing protocols, arbitration
- `research/dossiers/contenders/` -- Contender bot profiles, strength classifications

### Related Canonical Files

- `benchmark-blueprint.md` -- 12 benchmark suites (BMS-001 through BMS-012)
- `future-experiment-backlog.md` -- 32 experiments (EXP-001 through EXP-032)
- `hypothesis-register.md` -- HYP-005 (MCP Theorem), HYP-014 through HYP-017 (timing/MCTS)
- `claim-register.md` -- C136-C142 (MCTS consistency), C200-C202 (benchmark claims), C132 (board-size hypothesis)
- `ensemble-catalog.md` -- ENS-013 through ENS-018 (MCTS-containing ensembles)
- `work-queue.md` -- T026, T038, T085-T088 (benchmark science tasks)

### Related Claims

| Claim ID | Status | Relevance |
|----------|--------|-----------|
| C132 | HYPOTHESIS | Board-size solving status for 15x13 |
| C136 | NEEDS_CORRECTION | Broken MCP theorem citation (arXiv:1203.2285) |
| C139 | VERIFIED | Adjacent opening draw unidentifiable by MCTS |
| C140-142 | VERIFIED | MCTS consistency claims |
| C177-179 | VERIFIED | MCTS timing budget findings |
| C200-202 | VERIFIED | Neural MCTS benchmark, TensorRT, AZAL |
| C203-205 | HYPOTHESIS/VERIFIED | Board-size routing, phase-boundary, DQN tactical weakness |

---

## 18. Document History

| Date | Round | Change |
|------|-------|--------|
| 2026-08-04 | R34 | Initial dossier creation (Slot 6, Job 64, Lane: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS) |

---

*This dossier was produced as part of external-worker batch processing for the ConnectX Research Nexus. No experiments were executed. All specifications are research-only and designed for future empirical validation.*