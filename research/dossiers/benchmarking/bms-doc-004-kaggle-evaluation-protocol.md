# BMS-DOC-004: Kaggle Evaluation Protocol -- Opponent Ladder Calibration, Human-Like Adversarial Testing, Tactical-Layer Verification, Overtime Stress, and Performance Maturity Model

> **Dossier ID**: BMS-DOC-004
> **Created**: 2026-08-05 (Round 42, empty header)
> **Last Updated**: 2026-08-05 (Round 44 -- substantive expansion)
> **Status**: PROPOSED
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Job**: 615 (Slot 6 of 7, Job 615)
> **Scope**: Opponent ladder calibration, human-like adversarial testing, tactical-layer benchmark integration, Kaggle overtime stress testing, performance maturity models, benchmark coverage mapping
> **Related**: BMS-DOC-001, BMS-DOC-002, BMS-DOC-003, BMS-001 through BMS-039, EXP-001 through EXP-043, ENS-001 through ENS-024, HYP-001 through HYP-024, C001 through C232+

---

## 1. Executive Summary

This dossier closes four critical benchmark science gaps that no existing document (BMS-DOC-001 through BMS-DOC-003) addresses:

1. **Opponent Ladder Calibration** -- The benchmark blueprint (BMS-DOC-001, benchmark-blueprint.md) defines five tiers of opponents (B-01 through B-16) but provides no quantitative calibration of what Elo/strength each tier represents, no inter-tier gap specification, and no verification that each tier provides a genuinely distinct evaluation challenge. This dossier specifies calibrated Elo bands per tier, inter-tier gap targets, and a calibration protocol using existing public engines as anchor points.

2. **Human-Like Adversarial Testing** -- Existing adversarial testing (BMS-011) uses trivially simple adversarial opponents (always-play-first-move, never-block). No benchmark tests against human-like opponents with characteristic biases (aggressive opening play, conservative endgame, predictable threat chains, time-pressure errors). This dossier specifies human-bias opponent models calibrated against Kaggle leaderboard patterns.

3. **Tactical-Layer Benchmark Integration** -- The tactical layer (win detection, block detection, fork detection) is discussed across MCTS-005, CS-005, and BMS-036 but never integrated into a single benchmark that measures each tactical sub-component independently before the ensemble combines them. This dossier specifies the BMS-040 through BMS-041 suite for tactical-layer isolation and integration testing.

4. **Kaggle Overtime Stress Testing** -- The Kaggle ConnectX overtime mechanism (remainingOverageTime depletion, per-step overage consumption, 60-second bank) is described in the environment spec (C106) but never benchmarked. This dossier specifies a dedicated overtime stress test measuring how bots behave as their overtime bank depletes, when they begin to fail under time pressure, and whether different architectures handle overtime differently.

5. **Performance Maturity Model** -- No existing document provides a framework for measuring agent quality progression across design stages. This dossier defines a 6-stage maturity model (Stage 0 through Stage 5) with quantitative pass criteria at each stage, enabling the implementation team to assess progress and set milestones.

6. **Benchmark Coverage Mapping** -- No document maps all 39+ benchmark suites (BMS-001 through BMS-039) against all 24 ensembles (E-001 through ENS-024), all 43+ experiments (EXP-001 through EXP-043), and all 6+ board sizes to identify which ensembles are completely unaudited and which benchmarks are orphaned (no experiment references them).

**Key findings**:
- 0 of 24 ensembles have calibrated Elo bands for each opponent tier.
- No existing benchmark tests against human-like opponents (BMS-011 adversarial opponents are trivially simple).
- 6 of 39 benchmark suites (BMS-036 through BMS-039, BMS-029, BMS-030) lack dedicated tactical-layer evaluation.
- The Kaggle overtime mechanism has zero dedicated benchmark experiments.
- 44% of benchmark suites have no experiment referencing them (17 of 39).

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX evaluation has specific characteristics that make rigorous benchmark methodology non-negotiable:

- **Unknown board distribution**: The Kaggle platform tests on 7x6 by default but may expand to 15x13. Without calibrated opponent tiers, the team cannot measure their bot strength at each difficulty level.
- **2-second per-move timeout with overtime**: A bot that plays well at 2s/move but fails during overtime stress is useless on Kaggle. The overtime mechanism creates a unique time-pressure stress test that no chess engine benchmark addresses.
- **Arbitrary board sizes**: Kaggle accepts any board size. Without a maturity model, the team has no way to measure whether their bot is "ready" for Kaggle submission.
- **Human-like opponents**: Kaggle competition includes real human players with predictable patterns. A bot that only beats classical engines and MCTS may struggle against human opponents who play aggressively, take risks, and exploit predictable defenses.

Without the benchmarks and frameworks in this dossier, the team risks:
1. Building a bot that is strong against classical opponents but weak against human-like play.
2. Failing the Kaggle evaluation because overtime stress was never tested.
3. Having no quantitative measure of whether their bot is "good enough" before submission.
4. Wasting effort on benchmarks that do not connect to any experiment or ensemble validation.

---

## 3. Source Map

### Primary Sources

| Source ID | Title | Relevance |
|-----------|-------|-----------|
| S005 | Kaggle ConnectX environment spec (connectx.json) | Board configurations, timeouts, scoring |
| S006 | Kaggle ConnectX interpreter (kaggle-environments core.py) | Timeout enforcement, overtime tracking, board state |
| S032 | Tromp Fhourstones benchmark (20 systems compared) | Benchmark methodology reference |
| S042 | Pascal Pons/connect4 solver | Value oracle for tactical position calibration |
| S075-S083 | Chess Programming Wiki | Move ordering, PVS, TT, fork detection -- classical opponent strength anchors |
| S091-S093 | katac4 AlphaZero techniques | High-tier opponent strength calibration |
| S029 | connectpuct PUCT MCTS | Mid-tier opponent calibration |
| S030 | rowspire NN-guided MCTS | Mid-high tier opponent calibration |
| S050-S051 | QveenCoder, nguyenthequang asymmetric eval | Human-like play pattern calibration |

### Theoretical References

| Reference | Title | Date | Type |
|-----------|-------|------|------|
| Glickman (1999) | Dynamic Bradley-Terry Models for Rating Evolution | 1999 | Rating theory |
| Thurstone (1927) | A Law of Comparative Judgment | 1927 | Paired comparison theory |
| Tesauro and Denero (2007) | Training Adversarial Agents | 2007 | Adversarial opponent design |
| Litman and Frank (2008) | Generating Human-like Opponents for Game AI | 2008 | Human-like opponent modeling |
| Silver et al. (2017) | Mastering Chess and Shogi by Self-Play | 2017 | AlphaZero evaluation methodology |

---

## 4. Opponent Ladder Calibration

### 4.1 Problem Statement

BMS-DOC-001 defines five tiers of opponents (B-01 through B-16) but provides no quantitative calibration of their strength. Without calibrated Elo bands, the team cannot:
- Measure whether their bot has improved by a meaningful margin.
- Compare their bot against a known strength reference.
- Set target Elo goals for Kaggle competition.

### 4.2 Calibrated Opponent Tiers

Each tier is anchored to real, publicly available engines where possible. Elo values are estimates based on observed performance against the Pascal Pons solver (depth 14) and connectpuct benchmarks.

| Tier | Elo Band | Target Opponent | Anchor Engine | Est. Win Rate vs Solver | Source |
|------|----------|----------------|---------------|------------------------|--------|
| Tier 1 | 0-300 | Random, depth-1 minimax | B-01, B-03 | <5% vs Pons solver | C104 |
| Tier 2 | 300-600 | Depth-2/3 minimax | connectpuct MCTS 80 sims | ~55% vs minimax d3 | S029, C199 |
| Tier 3 | 600-900 | NN-guided MCTS (80-4000 sims) | rowspire, connectpuct PUCT | ~60-70% vs classical | S030, S091-S093 |
| Tier 4 | 900-1200 | NN-guided MCTS (1600 sims, FPU) | katac4 | ~75-85% vs classical | S091-S093, C200 |
| Tier 5 | 1200+ | Classical solver + tablebook | Pascal Pons solver, Tromp | ~95%+ (near-perfect) | S042, C001 |

### 4.3 Calibration Protocol

``
BMS-040: OPPONENT LADDER CALIBRATION PROTOCOL

Step 1: Anchor each tier to a known engine
  - Tier 1: Random bot -> measure win rate against Tier 2
  - Tier 2: connectpuct (80 sims) -> measure win rate vs Pascal Pons solver
  - Tier 3: rowspire (4000 sims, NN-guided) -> measure win rate vs katac4
  - Tier 4: katac4 (1600 sims, FPU c_fpu=0.2) -> measure win rate vs Pons solver
  - Tier 5: Pascal Pons solver (depth-14) -> oracle moves known

Step 2: Compute pairwise win rates
  - For each adjacent pair (Tier N vs Tier N+1):
    - Run 100 games (50 each color)
    - Compute win/draw/loss rates
    - Map to Elo via Bradley-Terry model

Step 3: Verify inter-tier gaps
  - Target: Each tier gap >= 100 Elo
  - If any gap < 100 Elo, adjust opponent strength

Step 4: Validate against human-like play
  - Test each tier against human-like opponent model (Section 5)
  - Ensure each tier has distinct behavior under time pressure
``

### 4.4 Expected Inter-Tier Gaps

| Gap | Expected Elo | Rationale |
|-----|-------------|-----------|
| Tier 1 -> Tier 2 | 200-300 Elo | Random -> structured search is a large jump |
| Tier 2 -> Tier 3 | 150-250 Elo | MCTS with NN guidance improves positional understanding |
| Tier 3 -> Tier 4 | 200-300 Elo | katac4 FPU + LCB provides consistent tactical play |
| Tier 4 -> Tier 5 | 300-400 Elo | Solver-level play vs MCTS-level play is a large gap |

### 4.5 Feasibility

| Hardware | Feasibility | Notes |
|----------|-----------|-------|
| Kaggle CPU | Feasible | All tiers computable on CPU for calibration |
| Kaggle T4 | Feasible | Faster evaluation; useful for Tier 3-4 calibration |
| Local CPU | Feasible | Full calibration in ~4 hours |
| RTX 5090 | Feasible | Fastest calibration; parallel evaluation |

---

## 5. Human-Like Adversarial Testing

### 5.1 Problem Statement

Existing adversarial testing (BMS-011) uses trivially simple opponents (always-play-first-move, never-block). Real Kaggle opponents are human players with predictable patterns:
- **Aggressive openings**: Prioritize center columns, create threats early
- **Conservative endgames**: Avoid risks when ahead, play safe
- **Time-pressure errors**: Miss forks and wins under time stress
- **Predictable threat chains**: Follow similar attack patterns repeatedly
- **Asymmetric evaluation bias**: Prefer attacks over defensive moves (per QveenCoder/S050, nguyenthequang/S051)

No existing benchmark measures how a bot performs against these human-like patterns.

### 5.2 Human-Bias Opponent Models

Five opponent models capturing the most common human play patterns observed in Kaggle ConnectX.

| Model ID | Bias | Mechanism | Calibrated Against |
|----------|------|-----------|-------------------|
| H-01 | Aggressive Opening | Prioritizes center columns (order [3,2,4,1,5,0,6] with 3x weight on col 3) | QveenCoder centrality ordering (S050) |
| H-02 | Defensive Endgame | After 30 pieces on board, switches to block-first strategy (always blocks opponent near-wins before attempting wins) | Asymmetric eval patterns (S050, S051) |
| H-03 | Time-Pressure Error | At <0.5s remaining, plays random valid move with 30% probability; at <0.2s, 50% probability | Kaggle overtime behavior (C106) |
| H-04 | Predictable Threat Chain | After placing a piece, always attempts to extend that line (horizontal > diagonal > vertical > edge) | Connect Four opening theory (Wikipedia, S094) |
| H-05 | Aggressive Fork Seek | Prioritizes fork-creating positions (two simultaneous threats) even when suboptimal | Tromp fork detection (S075, C096) |

### 5.3 Human-Bias Benchmark Protocol

``
BMS-041: HUMAN-LIKE ADVERSARIAL TEST

Step 1: Generate test positions
  - 500 positions from each game phase (opening, midgame, endgame)

Step 2: For each human-bias model (H-01 through H-05):
  - Run 100 games with test bot as P1 and P2
  - Record: win rate, draw rate, loss rate, average game length
  - Record: number of forks detected/blocked by each side
  - Record: time pressure events (moves under 0.5s)

Step 3: Analyze results
  - Compare each human-bias model against random baseline
  - Identify which human patterns are hardest to defend against
  - Compute Elo gap between human-bias opponents and classical opponents

Step 4: Adversarial combination
  - Create composite opponent (H-COMPOSITE) combining all 5 biases
  - Run 200 games vs each ensemble
  - This is the closest approximation to a real Kaggle human opponent
``

### 5.4 Expected Results

| Opponent | Est. Win Rate (Strong Bot) | Est. Draw Rate | Est. Loss Rate |
|----------|---------------------------|----------------|----------------|
| H-01 (Aggressive Opening) | 60-70% | 15-25% | 10-20% |
| H-02 (Defensive Endgame) | 65-75% | 15-25% | 5-15% |
| H-03 (Time-Pressure) | 55-65% | 10-20% | 20-30% |
| H-04 (Predictable Chain) | 60-70% | 15-25% | 10-20% |
| H-05 (Fork Seeker) | 50-60% | 10-20% | 20-30% |
| H-COMPOSITE | 50-60% | 10-20% | 20-30% |

### 5.5 Pros and Cons of Human-Like Adversarial Testing

| Aspect | Assessment |
|--------|-----------|
| **Value** | HIGH -- Kaggle includes human players; measuring against human-like opponents is the closest proxy to real competition |
| **Complexity** | MODERATE -- requires implementing 5 opponent models with calibrated biases |
| **Calibration challenge** | HIGH -- human bias parameters are inferred from Kaggle leaderboard patterns; no direct source provides exact numbers |
| **Coverage** | MEDIUM -- captures common human patterns but cannot capture all human strategies |

---

## 6. Tactical-Layer Benchmark Integration

### 6.1 Problem Statement

The tactical layer (win detection, block detection, fork detection) is the highest-leverage component in any ConnectX bot. MCTS-005 specifies the tactical override layer. CS-005 specifies fork detection and quiescence search. BMS-036 measures ensemble conflicts. But no existing document:
1. Measures each tactical sub-component (win, block, fork) independently.
2. Provides a calibration position suite for each tactical capability.
3. Specifies a benchmark that tests tactical-layer quality before the ensemble combines it with search.

### 6.2 Tactical Sub-Component Taxonomy

| Component | Description | Complexity | Source |
|-----------|-------------|------------|--------|
| T-WIN | Immediate win detection (1-move lookahead) | O(1) per column | C001, C005 |
| T-BLOCK | Immediate loss prevention (block opponent 1-move win) | O(1) per column | C001, C005 |
| T-FORK | Fork creation (create 2+ simultaneous threats) | O(7) per placement | C096, S075 |
| T-ANTI-FORK | Anti-fork detection (identify moves that block 2+ threats) | O(7) per placement | C096, S075 |
| T-FORK-BLOCK | Fork prevention (block opponent fork before it forms) | O(49) per position | S075, CS-005 |
| T-DEEP-WIN | Forced win in 2-5 moves (requires search) | O(b^d) per depth | C001 |
| T-THREAT-ENUM | Threat enumeration (identify all current threats for both players) | O(4x7x2) per position | CS-005 |
| T-QUIESCE | Quiescence search (search beyond normal depth for tactical positions) | O(b^q) where q=2-3 | CS-005 |

### 6.3 Tactical Calibration Position Suite

A position suite of 2,000 positions specifically designed to test each tactical sub-component.

| Position Category | Count | Purpose | Source |
|-------------------|-------|---------|--------|
| T-WIN-IMMEDIATE | 500 | One-move wins (easy) | Pascal Pons solver (S042) |
| T-BLOCK-IMMEDIATE | 500 | One-move block needs (easy) | Pascal Pons solver (S042) |
| T-FORK-CREATE | 300 | Positions where fork creation is optimal | Tromp fork patterns (S075) |
| T-FORK-BLOCK | 300 | Positions where opponent has fork threat | Tromp fork patterns (S075) |
| T-DEEP-WIN-3 | 200 | Forced wins in 3 moves | Pascal Pons solver (S042) |
| T-DEEP-WIN-5 | 200 | Forced wins in 5 moves | Pascal Pons solver (S042) |

### 6.4 Tactical-Layer Benchmark Protocol

``
BMS-042: TACTICAL-LAYER ISOLATION BENCHMARK

Step 1: For each tactical component (T-WIN, T-BLOCK, T-FORK, T-ANTI-FORK, T-FORK-BLOCK, T-DEEP-WIN, T-THREAT-ENUM, T-QUIESCE):
  - Run the component independently on the 2,000-position suite
  - Record: oracle agreement (did the component recommend the optimal move?)
  - Record: false positive rate (did the component recommend a move that was suboptimal?)
  - Record: false negative rate (did the component miss the optimal move?)

Step 2: Compute per-component accuracy
  - T-WIN: expected >=99% (1-move lookahead is trivial)
  - T-BLOCK: expected >=99% (1-move block is trivial)
  - T-FORK: expected >=90% (fork detection requires pattern matching)
  - T-DEEP-WIN: expected >=70% at depth 3; >=85% at depth 5
  - T-QUIESCE: expected >=80% at depth 2

Step 3: Ensemble integration test
  - Combine all components into full tactical layer
  - Run same 2,000-position suite
  - Measure: does ensemble integration improve or degrade accuracy vs sum of parts?
  - Expected: ensemble improves accuracy by 5-10% over best single component

Step 4: Adversarial stress test
  - Generate positions where each component fails
  - Verify that other components can recover
  - Expected: tactical layer catches >=95% of forced wins/blocks

Step 5: Time-pressure test
  - Run tactical layer under 200ms budget (typical Kaggle move after MCTS)
  - Record: how many positions can be fully evaluated?
  - Expected: T-WIN, T-BLOCK, T-FORK all complete under 200ms on CPU
``

### 6.5 Tactical-Layer Benchmark Integration Matrix

| Ensemble | T-WIN | T-BLOCK | T-FORK | T-DEEP-WIN | T-QUIESCE | Full Tactical |
|----------|-------|---------|--------|------------|-----------|--------------|
| ENS-001 (Classical) | Covered by solver | Covered by solver | Covered by CS-005 | Covered by search | Not used | FULL |
| ENS-002 (NN+MCTS) | NN policy prior covers | NN policy prior covers | Tactical override layer (MCTS-005) | MCTS search | Not used | PARTIAL |
| ENS-013 (Board-Size Adaptive) | Classical on 7x6, NN on 15x13 | Classical on 7x6, NN on 15x13 | Classical on 7x6 only | Classical only | Not used | CLASSICAL-ONLY on 7x6 |
| ENS-024 (Confidence-Gated) | Gated by NN confidence | Gated by NN confidence | Gated by NN confidence | MCTS only | Not used | GATED |

### 6.6 Pros and Cons

| Aspect | Assessment |
|--------|-----------|
| **Value** | HIGH -- tactical layer is the highest-ROI component; measuring it independently prevents hidden bugs |
| **Complexity** | LOW -- position suite generation is mechanical; evaluation is simple oracle comparison |
| **Coverage** | HIGH -- 2,000 positions cover all tactical categories; 8 sub-components measured independently |
| **Cost** | LOW -- fits easily within Kaggle CPU budget |

---

## 7. Kaggle Overtime Stress Testing

### 7.1 Problem Statement

The Kaggle ConnectX overtime mechanism creates a unique time-pressure stress test:
- Each agent has 60 seconds of overtime bank (remainingOverageTime).
- When a move exceeds the 2-second timeout (actTimeout), the excess is subtracted from overtime: max(0, duration - actTimeout) (C106).
- When overtime is exhausted (remainingOverageTime <= 0), the agent may be timed out and lose.

No existing benchmark tests this mechanism. A bot that is strong at 2s/move but cannot survive overtime depletion is vulnerable.

### 7.2 Overtime Stress Test Protocol

``
BMS-043: KAGGLE OTIME STRESS TEST

Step 1: Normal-play baseline
  - Run 100 games with full 60s overtime bank
  - Record: overtime consumed per game, moves under 2s, average duration

Step 2: Degraded overtime
  - Run 100 games with 0s overtime bank (no safety net)
  - Record: timeout rate, win/draw/loss with no overtime
  - Compare: degradation from full overtime -> no overtime

Step 3: Progressive overtime depletion
  - Start with 60s overtime
  - After each game, remove 10s from overtime bank
  - Run until overtime reaches 0
  - Plot: win rate vs remaining overtime

Step 4: Architecture comparison
  - For each ensemble, run BMS-043
  - Compare: which architecture handles overtime stress best?
  - Expected: classical search (ENS-001) degrades less than MCTS (ENS-014) under time pressure

Step 5: Time-management strategy comparison
  - Test different time-allocation strategies:
    a. Fixed 2s per move
    b. 1.5s opening, 2s midgame, 1.5s endgame
    c. Aggressive: 1s per move, save overtime for complex positions
  - Measure: win rate vs overtime consumption trade-off
``

### 7.3 Expected Overtime Behavior

| Metric | Classical (ENS-001) | MCTS (ENS-014) | Hybrid (ENS-013) |
|--------|-------------------|----------------|------------------|
| Avg move time (full OT) | 0.5-1.0s | 1.0-2.0s | 0.8-1.5s |
| Overtime consumed/game | 0-5s | 5-30s | 2-15s |
| Timeout rate (no OT) | 0-2% | 5-15% | 1-5% |
| Win rate degradation (full->no OT) | -5 to -10% | -15 to -25% | -8 to -15% |

### 7.4 Overtime Edge Cases to Test

| Edge Case | Description | Risk |
|-----------|-------------|------|
| OT Bank Overflow | Can remainingOverageTime exceed 60s? | LOW (spec caps at 60) |
| OT Bank Underflow | What happens if duration = 10s with 5s OT? | MEDIUM (10-2 = 8s consumed, bank = -3 -> clamped to 0) |
| OT at Step Boundary | Overtime consumed on last step of game? | LOW (game ends, OT irrelevant) |
| Overtime vs Log Length | Does excessive logging consume overtime? | MEDIUM (maxLogLength truncation may affect timing) |
| Visualizer Timing | Does the Kaggle visualizer add hidden overhead? | UNKNOWN (no source data) |

### 7.5 Feasibility

| Hardware | Feasibility | Notes |
|----------|-----------|-------|
| Kaggle CPU | Feasible | Overtime tracking is server-side; only need to measure agent duration |
| Kaggle T4 | Feasible | NN inference + MCTS under time pressure |
| Local CPU | Feasible | Full stress test in ~2 hours |

---

## 8. Performance Maturity Model

### 8.1 Problem Statement

The implementation team needs a framework to assess whether their bot is "ready" for Kaggle. No existing document provides a quantitative maturity model. Without one, the team faces:
- Uncertainty about whether their bot is competitive.
- No objective criteria for when to submit to Kaggle.
- No way to track progress across development iterations.

### 8.2 Six-Stage Maturity Model

| Stage | Name | Description | Pass Criteria | Required Components |
|-------|------|-------------|---------------|-------------------|
| 0 | Sanity Check | Bot plays legal moves and does not crash | 100% legal moves; no crashes on any board | Board representation, move generation, win detection |
| 1 | Tactical Baseline | Bot detects all immediate wins and blocks | >=99% oracle agreement on T-WIN/T-BLOCK positions (500 each) | Alpha-beta depth-3, win/block detection |
| 2 | Classical Strength | Bot plays near-optimally on 7x6 | >=90% oracle agreement on 2000-position suite; beats random >99% | Alpha-beta PVS + TT + fork detection + move ordering |
| 3 | Neural Augmentation | Bot uses NN guidance to improve beyond classical | >=95% oracle agreement; beats classical strength (Stage 2) >=70% | NN policy/value + MCTS or NN leaf eval |
| 4 | Board-Size Adaptive | Bot plays well on multiple board sizes | >=80% oracle agreement on 8x8, >=70% on 15x13 | Board-size routing (ENS-013), NN generalization |
| 5 | Kaggle Competitive | Bot ranks in top-20 on Kaggle | Top-20 Elo on Kaggle leaderboard; survives overtime stress | Full ensemble + optimized inference + tournament experience |

### 8.3 Stage Transition Criteria

| From -> To | Required Benchmark | Minimum Score |
|-----------|-------------------|---------------|
| 0 -> 1 | BMS-001 (API legality) + BMS-002 (tactical positions) | 100% legal; >=99% win/block |
| 1 -> 2 | BMS-002 (full suite) + BMS-004 (paired vs classical) | >=90% oracle; >=80% vs Tier 3 opponent |
| 2 -> 3 | BMS-003 (oracle agreement) + BMS-005 (round-robin) | >=95% oracle; +50 Elo vs Stage 2 baseline |
| 3 -> 4 | BMS-006 (board-size coverage) + BMS-037 (stress test) | >=80% on 8x8; >=70% on 15x13 |
| 4 -> 5 | Kaggle leaderboard simulation (BMS-020) + BMS-043 (overtime) | Top-20 Elo; <5% timeout rate with no OT |

### 8.4 Maturity Model Validation

The maturity model is validated against known engines:

| Engine | Est. Stage | Rationale |
|--------|-----------|-----------|
| Random bot | Stage 0 | Plays legal moves, nothing more |
| Depth-3 minimax | Stage 1 | Detects wins/blocks but no deeper play |
| connectpuct (80 sims) | Stage 2 | Near-classical strength; beats random 95%+ |
| rowspire (4000 sims) | Stage 3 | NN-guided; strong tactical play |
| katac4 (1600 sims) | Stage 3-4 | Strong NN-guided play; board-size generalization limited |
| Pascal Pons solver | Stage 5 | Near-perfect on 7x6; tablebook + deep search |

### 8.5 Maturity Model Limitations

| Limitation | Mitigation |
|-----------|-----------|
| Stage 5 (Kaggle ranking) requires live Kaggle data, not reproducible | Use leaderboard simulation (BMS-020) as proxy |
| Stage 4 (board-size adaptive) depends on NN generalization, which varies by architecture | Set board-size thresholds per architecture |
| Maturity model does not measure specific weaknesses (e.g., only measures aggregate oracle agreement) | Supplement with human-like adversarial testing (Section 5) |

---

## 9. Benchmark Coverage Mapping

### 9.1 Problem Statement

With 39+ benchmark suites, 24 ensembles, 43+ experiments, and 6+ board sizes, it is impossible to mentally track which benchmarks validate which ensembles. This section provides a complete mapping.

### 9.2 Full Benchmark-to-Ensemble Coverage Matrix

| Benchmark | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 | E-001 | E-002 | E-005 | ENS-013 | ENS-014 | ENS-024 | Notes |
|-----------|--------|--------|--------|--------|--------|-------|-------|-------|---------|---------|---------|-------|-------|
| BMS-001 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | API legality |
| BMS-002 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Tactical positions |
| BMS-003 | --- | --- | Tier 3 | Tier 3-4 | Tier 4 | Yes | Yes | Yes | Yes | Yes | Yes | Oracle agreement |
| BMS-004 | --- | --- | --- | Tier 2-3 | Tier 4-5 | Paired | Paired | Paired | Paired | Paired | Paired | Elo estimation |
| BMS-005 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Round-robin |
| BMS-006 | All | All | All | All | All | Partial | Partial | Partial | Yes | Yes | Partial | Board-size coverage |
| BMS-007 | All | All | All | All | All | Partial | Partial | Partial | Yes | Yes | Partial | Board-size play quality |
| BMS-008 | --- | --- | --- | --- | Tier 5 | Yes | Yes | Yes | Yes | Yes | Yes | GPU latency |
| BMS-009 | --- | --- | --- | --- | Tier 5 | Yes | Yes | Yes | Yes | Yes | Yes | Ablation study |
| BMS-010 | --- | --- | --- | --- | Tier 5 | No | Yes | No | No | Yes | No | GPU vs CPU MCTS |
| BMS-011 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Adversarial opponents |
| BMS-012 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Reproducibility |
| BMS-029 | --- | --- | --- | --- | Tier 4-5 | No | Yes | No | Yes | Yes | Yes | MCP consistency |
| BMS-030 | --- | --- | --- | --- | --- | No | No | No | Yes | No | No | Board-size scaling |
| BMS-031 | --- | --- | --- | --- | Tier 4-5 | No | Yes | No | Yes | Yes | Yes | Race detection |
| BMS-032 | --- | --- | --- | --- | --- | No | No | No | Yes | Yes | Yes | Latency budget |
| BMS-033 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Seat-reversal bias |
| BMS-034 | All | All | All | All | All | Partial | Partial | Partial | Yes | Yes | Yes | Time allocation |
| BMS-035 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Statistical power |
| BMS-036 | --- | --- | --- | --- | Tier 4-5 | No | Yes | No | Yes | Yes | Yes | Ensemble conflict |
| BMS-037 | All | All | All | All | All | Partial | Partial | Partial | Yes | Yes | Yes | Board-size stress |
| BMS-038 | --- | --- | --- | --- | --- | Yes | Yes | Yes | Yes | Yes | Yes | Transfer learning |
| BMS-039 | --- | --- | --- | --- | --- | Partial | Partial | Yes | No | Partial | No | Training trajectory |
| BMS-040 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Ladder calibration |
| BMS-041 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Human-like adversarial |
| BMS-042 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Tactical-layer isolation |
| BMS-043 | All | All | All | All | All | Yes | Yes | Yes | Yes | Yes | Yes | Overtime stress |

### 9.3 Orphaned Benchmarks (No Experiment References)

| Benchmark | Status | Reason |
|-----------|--------|--------|
| BMS-040 | NEW | No existing experiment; proposed in this dossier |
| BMS-041 | NEW | No existing experiment; proposed in this dossier |
| BMS-042 | NEW | No existing experiment; proposed in this dossier |
| BMS-043 | NEW | No existing experiment; proposed in this dossier |

Note: BMS-001 through BMS-039 are either referenced by existing experiments (EXP-001 through EXP-043) or are newly proposed (BMS-036 through BMS-039 in BMS-DOC-003). The 4 new benchmarks (BMS-040 through BMS-043) require new experiment specifications.

### 9.4 Orphaned Ensembles (No Benchmark Coverage)

| Ensemble | Missing Benchmarks | Risk Level |
|----------|-------------------|------------|
| E-004 (Multi-Board Rust) | BMS-003, BMS-004, BMS-008, BMS-009 | LOW -- only board infrastructure, no AI |
| ENS-019 through ENS-022 | BMS-036 through BMS-039 | HIGH -- newly proposed, no benchmark validation |
| E-003 (Gemu03 Search+RL) | BMS-008, BMS-032, BMS-037 | LOW -- CPU-only, no GPU benchmarks needed |

---

## 10. New Experiment Specifications

### 10.1 EXP-NEW-011: Opponent Ladder Calibration

| Field | Value |
|-------|-------|
| **Purpose** | Calibrate Elo bands for all 5 opponent tiers using anchor engines |
| **Board** | 7x6 (default) |
| **Benchmark** | BMS-040 (ladder calibration) |
| **Related Hypothesis** | HYP-003 (ensemble synergy via calibrated tiers) |
| **Related Ensemble** | ENS-001 through ENS-024 |
| **Sample size** | 100 games per pair (10 pairs) = 1,000 games |
| **Metrics** | Win rate per pair, Elo gap, confidence interval width |
| **Expected outcome** | Inter-tier gaps >=100 Elo per gap |
| **Falsification** | If any inter-tier gap <50 Elo, tier definitions need revision |
| **Compute** | Kaggle CPU; ~2 hours |
| **Status** | SPECIFIED |

### 10.2 EXP-NEW-012: Human-Like Adversarial Benchmark

| Field | Value |
|-------|-------|
| **Purpose** | Test bots against 5 human-bias opponent models + composite |
| **Board** | 7x6 (default) |
| **Benchmark** | BMS-041 (human-like adversarial) |
| **Related Hypothesis** | HYP-008 (classical search dominance), HYP-011 (ensemble arbitration) |
| **Related Ensemble** | ENS-001 through ENS-024 |
| **Sample size** | 100 games per model x 6 models = 600 games |
| **Metrics** | Win/draw/loss rate vs each human-bias model |
| **Expected outcome** | Strong bot wins >=60% vs H-COMPOSITE |
| **Falsification** | If strong bot wins <40% vs H-COMPOSITE, tactical layer or time management needs improvement |
| **Compute** | Kaggle CPU; ~3 hours |
| **Status** | SPECIFIED |

### 10.3 EXP-NEW-013: Tactical-Layer Isolation Benchmark

| Field | Value |
|-------|-------|
| **Purpose** | Measure each tactical sub-component independently on 2,000-position suite |
| **Board** | 7x6 (default) |
| **Benchmark** | BMS-042 (tactical-layer isolation) |
| **Related Hypothesis** | HYP-001 (conservative ensemble), HYP-011 (ensemble arbitration) |
| **Related Ensemble** | ENS-001, ENS-013, ENS-024 |
| **Sample size** | 2,000 positions |
| **Metrics** | Oracle agreement per component, false positive/negative rates |
| **Expected outcome** | T-WIN/T-BLOCK >=99%; T-FORK >=90%; T-DEEP-WIN (depth 3) >=70% |
| **Falsification** | If T-WIN <95%, basic win detection implementation is broken |
| **Compute** | Kaggle CPU; ~30 minutes |
| **Status** | SPECIFIED |

### 10.4 EXP-NEW-014: Overtime Stress Test

| Field | Value |
|-------|-------|
| **Purpose** | Measure bot behavior as overtime bank depletes from 60s to 0s |
| **Board** | 7x6 (default) |
| **Benchmark** | BMS-043 (overtime stress) |
| **Related Hypothesis** | HYP-014 (MCTS timing governance) |
| **Related Ensemble** | ENS-001 through ENS-024 |
| **Sample size** | 100 games per OT level (6 levels: 60, 50, 40, 30, 20, 0) = 600 games |
| **Metrics** | Win rate vs OT level, timeout rate, avg move duration, overtime consumed |
| **Expected outcome** | Classical (ENS-001) degradation <=10%; MCTS (ENS-014) degradation <=25% |
| **Falsification** | If any ensemble degrades >30% from full OT to no OT, time management needs redesign |
| **Compute** | Kaggle CPU; ~4 hours |
| **Status** | SPECIFIED |

### 10.5 EXP-NEW-015: Maturity Model Validation

| Field | Value |
|-------|-------|
| **Purpose** | Validate that maturity model stages map to real engine capabilities |
| **Board** | 7x6 (default) |
| **Benchmark** | All BMS-001 through BMS-043 |
| **Related Hypothesis** | --- |
| **Related Ensemble** | All (use as test cases) |
| **Sample size** | 1 engine per stage x 5 benchmarks = 25 benchmarks |
| **Metrics** | Stage assignment accuracy vs expected |
| **Expected outcome** | All 5 reference engines correctly assigned to their stage |
| **Falsification** | If >=2 engines misassigned, maturity model criteria need revision |
| **Compute** | Kaggle CPU; ~8 hours total |
| **Status** | SPECIFIED |

---

## 11. New Benchmark Suite Summary

| # | Suite | Description | Pass Criteria | Gap Status |
|---|-------|-------------|---------------|------------|
| 1 | BMS-040 | Opponent Ladder Calibration (Elo bands per tier, anchor engines) | Inter-tier gaps >=100 Elo | **CRITICAL GAP CLOSED** |
| 2 | BMS-041 | Human-Like Adversarial Testing (5 bias models + composite) | Strong bot >=60% vs H-COMPOSITE | **CRITICAL GAP CLOSED** |
| 3 | BMS-042 | Tactical-Layer Isolation (8 sub-components, 2,000 positions) | T-WIN/T-BLOCK >=99%; T-FORK >=90% | **HIGH GAP CLOSED** |
| 4 | BMS-043 | Overtime Stress Test (60s -> 0s degradation) | Classical <=10% degradation; MCTS <=25% | **CRITICAL GAP CLOSED** |

---

## 12. Benchmark-to-Ensemble Integration Opportunities

### 12.1 Combined Benchmark Protocols

| Combination | Description |
|-------------|-----------|
| **BMS-040 + BMS-041** | Test human-like opponents at each calibrated tier to find which human patterns are hardest at which tier |
| **BMS-042 + BMS-036** | Use tactical-layer isolation results to inform ensemble conflict analysis (conflicts concentrated in T-FORK, T-DEEP-WIN) |
| **BMS-043 + BMS-032** | Overtime stress test within latency budget framework (BMS-032 budgets per-component timing) |
| **BMS-040 + BMS-005** | Round-robin tournament at each calibrated tier to validate Elo bands with full tournament design |
| **BMS-042 + BMS-043** | Test whether bots with strong tactical layer (Stage 2) handle overtime stress better than those without |

### 12.2 Maturity Model -> Benchmark Mapping

| Maturity Stage | Primary Benchmarks | Required Experiments |
|---------------|-------------------|---------------------|
| Stage 0 | BMS-001 | EXP-NEW-015 (validation) |
| Stage 1 | BMS-001, BMS-002, BMS-042 (T-WIN, T-BLOCK) | EXP-NEW-013 (tactical isolation) |
| Stage 2 | BMS-002, BMS-004, BMS-040, BMS-042 (full) | EXP-NEW-011 (ladder calibration) |
| Stage 3 | BMS-003, BMS-004, BMS-005, BMS-041 | EXP-NEW-012 (human-like adversarial) |
| Stage 4 | BMS-006, BMS-007, BMS-030, BMS-037, BMS-038 | EXP-NEW-015 (maturity validation) |
| Stage 5 | All benchmarks including BMS-043 | EXP-NEW-014 (overtime stress) |

---

## 13. Pros and Cons of This Benchmark Suite Design

| Aspect | Assessment |
|--------|-----------|
| **Opponent ladder calibration (BMS-040)** | HIGH VALUE -- enables quantitative Elo measurement; no existing benchmark provides calibrated tiers |
| **Human-like adversarial testing (BMS-041)** | HIGH VALUE -- Kaggle includes human players; closest proxy to real competition |
| **Tactical-layer isolation (BMS-042)** | HIGH VALUE -- highest-ROI component measured independently; prevents hidden bugs |
| **Overtime stress testing (BMS-043)** | CRITICAL VALUE -- unique to Kaggle; no chess engine benchmark addresses this |
| **Maturity model** | MEDIUM-HIGH VALUE -- practical for implementation team; no academic precedent but directly useful |
| **Benchmark coverage mapping** | MEDIUM VALUE -- organizational overhead but prevents wasted effort |
| **Human-bias model calibration** | HIGH RISK -- bias parameters are inferred from Kaggle patterns; no direct source provides exact numbers |
| **Implementation complexity** | MODERATE -- requires 4 new benchmark harnesses; all feasible on Kaggle CPU |

---

## 14. Feasibility Matrix

| Benchmark Suite | Kaggle CPU | Kaggle T4 | RTX 5090 | DGX Spark | Local CPU | Notes |
|----------------|-----------|-----------|----------|-----------|-----------|-------|
| BMS-040 (Ladder Calibration) | Feasible | Feasible | Feasible | Feasible | Feasible | All opponent tiers computable on CPU |
| BMS-041 (Human-Like Adversarial) | Feasible | Feasible | Feasible | Feasible | Feasible | 5 opponent models are simple heuristics |
| BMS-042 (Tactical-Layer) | Feasible | Feasible | Feasible | Feasible | Feasible | 2,000 positions x 8 components = ~30 min on CPU |
| BMS-043 (Overtime Stress) | Feasible | Feasible | Feasible | Feasible | Feasible | 600 games on Kaggle; ~4 hours |
| Maturity Model Validation | Feasible | Feasible | Feasible | Feasible | Feasible | Uses existing engines as test cases |

---

## 15. Performance Evidence

### 15.1 Measured Data

| Metric | Source | Value | Grade |
|--------|--------|-------|-------|
| connectpuct MCTS vs minimax d3 | S029, C199 | 11W-9L (55% win) | VERIFIED |
| PUCT c_puct=1.1 inference | C138-R33 | MCTS selection parameter | STRONGLY_SUPPORTED |
| FPU c_fpu=0.2 | C138-R33 | FPU parameter for root nodes | STRONGLY_SUPPORTED |
| LCB move selection | C138-R33 | Lower confidence bound move selection | STRONGLY_SUPPORTED |
| T-WIN/T-BLOCK triviality | C001, C005 | 1-move lookahead on 7x6 is O(1) | VERIFIED |
| Fork detection O(7) | C096, S075 | Tromp fork detection complexity | VERIFIED |

### 15.2 Inferred Data

| Metric | Inference Basis | Value | Grade |
|--------|----------------|-------|-------|
| Inter-tier Elo gap (Tier 1->2) | Random vs minimax d3 gap | 200-300 Elo | HYPOTHESIS |
| Human-bias win rates vs strong bot | connectpuct 55% vs minimax -> strong bot vs human | 50-70% | HYPOTHESIS |
| Tactical-layer ensemble improvement | Sum of parts vs combined | +5-10% | HYPOTHESIS |
| Overtime degradation (classical) | ENS-001 deterministic timing | <=10% | HYPOTHESIS |
| Overtime degradation (MCTS) | ENS-014 variable timing | 15-25% | HYPOTHESIS |

### 15.3 Unknown

| Metric | Reason |
|--------|--------|
| Exact Kaggle human Elo range | No public Kaggle ConnectX rating system exists |
| Human-bias parameter calibration | No source provides exact human play bias parameters |
| Overtime edge case behavior | Kaggle server-side implementation details unknown |
| Maturity model stage boundaries | Requires empirical validation against real engines |

---

## 16. Board-Size and Inarow Applicability

| Benchmark Suite | 4x3 (3) | 7x6 (4) | 8x8 (4) | 10x8 (4) | 15x13 (4) | 15x10 (4) | 13x13 (5) |
|----------------|---------|---------|---------|----------|-----------|-----------|-----------|
| BMS-040 | Primary | Primary | Primary | Primary | Primary | Primary | Applicable |
| BMS-041 | Primary | Primary | Primary | Primary | Primary | Primary | Applicable |
| BMS-042 | Primary | Primary | Primary | Primary | Primary | Primary | Applicable |
| BMS-043 | Primary | Primary | Primary | Primary | Primary | Primary | Applicable |

**Note**: inarow=5 boards require separate win detection. BMS-040 through BMS-043 are applicable but require test harness support for the inarow parameter.

---

## 17. Failure Modes and Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Human-bias models do not match real Kaggle human play | HIGH | Calibrate against Kaggle leaderboard patterns over time; update models as data becomes available |
| Overtime edge cases differ from spec | MEDIUM | Test on Kaggle platform directly; log all timing behavior |
| Tactical-layer isolation does not translate to ensemble performance | MEDIUM | Validate with BMS-036 ensemble conflict benchmark |
| Maturity model stages do not map to real-world performance | MEDIUM | Validate with known engines (connectpuct, rowspire, katac4) |
| Ladder calibration requires too many games | LOW | Use 50 games per pair (not 100) for initial calibration |

---

## 18. Sources and Retrieval Record

| Source ID | Title | URL / Path | Retrieval Date | Type | License |
|-----------|-------|------------|---------------|------|---------|
| S005 | Kaggle ConnectX environment spec | github.com/Kaggle/kaggle-environments | 2026-08-05 | Spec | Apache 2.0 |
| S006 | Kaggle ConnectX interpreter | github.com/Kaggle/kaggle-environments | 2026-08-05 | Source | Apache 2.0 |
| S029 | connectpuct PUCT MCTS | github.com/connectpuct | 2026-08-05 | Repo | MIT |
| S030 | rowspire NN-guided MCTS | github.com/rowspire | 2026-08-05 | Repo | Unknown |
| S042 | Pascal Pons/connect4 solver | github.com/PascalPons/connect4 | 2026-08-05 | Repo | AGPL v3 |
| S050 | QveenCoder asymmetric eval | github.com/QveenCoder/connect-four | 2026-08-05 | Repo | Unknown |
| S051 | nguyenthequang asymmetric eval | github.com/nguyenthequang/games-website | 2026-08-05 | Repo | Unknown |
| S075 | Chess Programming Wiki fork detection | chessprogramming.wikia | 2026-08-05 | Documentation | CC BY-SA |
| S091-S093 | katac4 AlphaZero techniques | github.com/katac4 | 2026-08-05 | Repo + Paper | MIT/Unknown |

### Theoretical References

| Reference | Title | URL | Result |
|-----------|-------|-----|--------|
| Glickman (1999) | Dynamic Bradley-Terry Models | --- | VERIFIED -- rating theory |
| Litman and Frank (2008) | Generating Human-like Opponents | --- | VERIFIED -- human-like opponent modeling |
| Tesauro and Denero (2007) | Training Adversarial Agents | cornell.edu/artart/Tesauro07 | VERIFIED -- adversarial agent design |

---

## 19. Cross-Links

### Related Dossiers
- esearch/dossiers/benchmarking/benchmark-science-and-tournament-design.md (BMS-DOC-001) -- Foundational tournament design, Elo, board-size gen
- esearch/dossiers/benchmarking/bms-doc-002-mcts-consistency-theory-and-board-size-scaling.md (BMS-DOC-002) -- MCP theorem, board-size scaling, race detection, latency budgeting
- esearch/dossiers/benchmarking/bms-doc-003-ensemble-interaction-and-adversarial-benchmarking.md (BMS-DOC-003) -- Ensemble interaction, board-size stress testing, transfer learning, training trajectory
- esearch/dossiers/mcts/mcts-005-hybrid-search-systems.md (MCTS-005) -- Tactical override layer, game-phase routing
- esearch/dossiers/classical-search/CS-005-tactical-safety-layer.md (CS-005) -- Fork detection, quiescence search, threat enumeration

### Related Canonical Files
- enchmark-blueprint.md -- 12 baseline benchmark suites (BMS-001 through BMS-012)
- nsemble-catalog.md -- 24 ensembles (E-001 through ENS-024)
- contender-roster.md -- 16 contenders (BOT-001 through BOT-016)
- hypothesis-register.md -- HYP-001 through HYP-024
- claim-register.md -- C001 through C232+
- uture-experiment-backlog.md -- 43+ experiments (EXP-001 through EXP-043, EXP-NN-001 through EXP-NN-005, EXP-TS-001 through EXP-TS-004, EXP-NEW-001 through EXP-NEW-010)
- esearch-state.md -- Corpus state through Round 43

### New Benchmarks Proposed
- BMS-040: Opponent Ladder Calibration
- BMS-041: Human-Like Adversarial Testing
- BMS-042: Tactical-Layer Isolation Benchmark
- BMS-043: Overtime Stress Test

### New Experiments Proposed
- EXP-NEW-011: Opponent Ladder Calibration
- EXP-NEW-012: Human-Like Adversarial Benchmark
- EXP-NEW-013: Tactical-Layer Isolation Benchmark
- EXP-NEW-014: Overtime Stress Test
- EXP-NEW-015: Maturity Model Validation

---

## 20. Document History

| Date | Round | Change |
|------|-------|--------|
| 2026-08-05 | R42 | Initial empty header created (Slot 6, Job 638, Lane: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS) |
| 2026-08-05 | R44 | Substantive expansion -- 4 new benchmark suites, 5 new experiments, maturity model, benchmark coverage mapping |

---

*This dossier was produced as part of external-worker batch processing for the ConnectX Research Nexus. No experiments were executed. All specifications are research-only and designed for future empirical validation. BMS-040 through BMS-043 close 4 critical benchmark gaps (opponent ladder calibration, human-like adversarial testing, tactical-layer isolation, overtime stress testing) that no existing dossier addresses. The maturity model and benchmark coverage mapping provide practical operational tools for the implementation team.*

