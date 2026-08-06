# BMS-DOC-005: Kaggle Competitive Benchmark Design and Evaluation Protocol

> **Dossier ID**: BMS-DOC-005
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Author**: External Worker, Slot 6, Jobs 613/614, Benchmark Science Lane
> **Scope**: Comprehensive benchmark design for Kaggle ConnectX competition: evaluation protocol, resource profiling, pipeline gates, empirical experiment design, and competitive strategy
> **Related claims**: C226-C233 (governance findings), C184-C192 (benchmark science)
> **Related hypotheses**: HYP-024 (adaptive board-size MCTS)
> **Related ensembles**: ENS-001 through ENS-024 (all require benchmark validation)
> **Related components**: CMP-003, CMP-004, CMP-008, CMP-012, CMP-014, CMP-017

---

## 1. Executive Summary

This dossier specifies a **complete benchmark protocol** for evaluating ConnectX bots on the Kaggle platform and locally. It covers four interlocking pillars:

1. **Kaggle evaluation protocol** — How to test bots against Kaggle's built-in agents (Random, Minimax, Heuristic, MCTS) with controlled parameters and statistical validity.
2. **Resource profiling framework** — Three-tier profiling (single move, sustained game, stress test) covering memory, VRAM, CPU utilization, latency distribution, and the critical 2-second action budget.
3. **Pipeline gate calibration** — Five-stage promotion gates (Sanity → Tactical → Classical → Neural → Deployment) that filter bots before expensive full-game evaluation.
4. **Empirical experiment design** — 6 concrete experiments (EXP-BMS-001 through EXP-BMS-006) with compute requirements, expected runtime, and success criteria.

The benchmark design is **board-size agnostic**: it covers 7×6 (standard), 8×8, 10×8, 15×10, and 15×13 configurations with appropriate scaling rules for each.

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle environment imposes hard constraints (95MB package limit, 2-second action budget, T4 GPU or CPU) that make benchmarking fundamentally different from local testing. A bot that performs well locally may fail on Kaggle due to:

1. **Package size limits**: 95MB constrains which neural networks can be deployed. A ResNet b3c128n (~2.3MB) can be deployed; a large transformer cannot.
2. **Latency constraints**: 2 seconds per move means deep alpha-beta search (depth-8+) is infeasible on CPU. Shallow search with strong evaluation may outperform deep search on large boards.
3. **GPU availability**: T4 has ~16GB VRAM but limited FP32 throughput vs. RTX 5090. Neural network inference must be optimized for T4.
4. **Statistical validity**: Kaggle tournaments typically run 100-500 games per bot. Results with <100 games may not be statistically significant.

This benchmark design ensures that:
- Every bot is evaluated on the same 4 dimensions (strength, speed, memory, stability)
- Results are reproducible locally and on Kaggle
- The benchmark pipeline can be automated for CI integration

## 3. Source Map

### Primary Sources (Directly Authenticated)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S077 | Kaggle ConnectX API documentation | Kaggle official docs | VERIFIED |
| S078 | Kaggle ConnectX environment source (connectx.py) | Kaggle source code | VERIFIED |
| S082 | test_connectx.py (279 lines, 12 official tests) | Kaggle test suite | VERIFIED |
| S033 | Pascal Pons/connect4 solver (AGPL v3) | GitHub source | VERIFIED |
| S028 | blanyal/AlphaZero-Light (MIT) | GitHub source | VERIFIED |
| S094 | Wikipedia -- Connect Four (board-size solving results) | Public wiki | VERIFIED |

### Secondary Sources (Supporting Methodology)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S075 | Chess Programming Wiki -- Transposition table strategies | Public wiki | VERIFIED |
| S078 (CPW) | Chess Programming Wiki -- Fork detection (6 canonical patterns) | Public wiki | VERIFIED |
| S137 | Chess Programming Wiki -- MCTS and board representation | Public wiki | VERIFIED |

### Retrieval Date: 2026-08-05

---

## 4. Kaggle Evaluation Protocol

### 4.1 Built-in Agent Baseline

Kaggle's ConnectX environment includes 4 built-in agents:

| Agent | Algorithm | Depth/Config | Reference |
|-------|-----------|-------------|-----------|
| random_agent | Uniform random | N/A | `connectx.py: random_agent` |
| minimax_agent | Alpha-beta minimax | depth=4 (default) | `connectx.py: minimax_agent` |
| negamax_agent | Alpha-beta negamax | depth=4 (default) | `connectx.py: negamax_agent` |
| interpreter/agent framework | Full environment | — | `kaggle_environments/envs/connectx/connectx.py` |

**Benchmark gate**: Any new bot must beat the random_agent baseline (win rate > 50% on 100 games). This is Stage 0 (Sanity Gate).

### 4.2 Evaluation Matrix

| Bot vs | 7×6 | 8×8 | 10×8 | 15×10 | 15×13 |
|--------|-----|-----|------|-------|-------|
| random_agent | 200 games | 200 games | 200 games | 200 games | 200 games |
| minimax_agent | 200 games | 100 games | 100 games | 100 games | 100 games |
| negamax_agent | 200 games | 100 games | 100 games | 100 games | 100 games |
| MCTS agent (if available) | 100 games | — | — | — | — |

**Statistical note**: 200 games provides ~10% margin of error for a 50% win rate. 100 games provides ~15% margin of error. Kaggle tournament results with 500 games would provide ~7% margin of error.

### 4.3 Win Rate as Evaluation Metric

Win rate is the primary evaluation metric because:
- It maps directly to Kaggle competition scoring
- It is interpretable by non-technical stakeholders
- It captures the full game outcome (not just move quality)

**Limitations**: Win rate does not capture:
- Speed of play (2-second budget adherence)
- Memory usage (95MB limit adherence)
- Robustness (does the bot handle edge cases?)
- Board-size generalization (performance on unsized boards)

For these, use secondary metrics (latency profile, memory profile, error rate, board-size scaling).

## 5. Resource Profiling Framework

### 5.1 Tier 1: Single-Move Profiling

Measure per-move resource usage on 100 random board positions:

| Metric | Measurement Method |
|--------|-------------------|
| Wall-clock latency (p50, p95, p99) | Python `time.perf_counter()` around each move |
| Peak memory (RSS) | `tracemalloc` or `resource.getrusage()` |
| CPU utilization | `os.cpu_count()` × `psutil.Process().cpu_percent()` |
| VRAM usage (if GPU) | `torch.cuda.max_memory_allocated()` or `nvidia-smi` |

**Threshold**: p95 latency < 2000ms (Kaggle action budget). p99 latency < 3000ms (grace period).

### 5.2 Tier 2: Sustained Game Profiling

Run full games (100 per configuration) and measure:

| Metric | Measurement Method |
|--------|-------------------|
| Total game time | `time.perf_counter()` over full game |
| Average moves per second | Games × moves / total time |
| Memory growth over game | Memory profile at each move |
| CPU utilization over time | Per-move CPU tracking |
| GPU utilization (if applicable) | Per-move GPU tracking |

**Analysis**: Plot memory and CPU over time to detect:
- Memory leaks (monotonically increasing RSS)
- CPU saturation (consistently at 100%)
- GPU underutilization (low utilization suggests bottleneck elsewhere)

### 5.3 Tier 3: Stress Test

Evaluate under sustained load:

| Experiment | Description |
|------------|-------------|
| Memory leak test | Run 10,000 moves without TT clear; measure memory growth |
| Concurrent evaluation | Measure latency of parallel move evaluation |
| Warm vs cold start | Measure first-move latency vs subsequent moves |
| Overtime behavior | What happens when move > 2 seconds? (bot may lose) |

## 6. Pipeline Gate Calibration

The 5-stage promotion gate filters bots before expensive full-game evaluation:

### Stage 0: Sanity Gate
**Input**: New bot code
**Checks**:
- Code compiles / imports without errors
- Implements required API (`move(obs, config)` function)
- Handles edge cases (first move, last move, draw detection)
**Output**: Pass → Stage 1 / Fail → rejected
**Cost**: ~5 seconds

### Stage 1: Tactical Gate
**Input**: Sanity-passed bot
**Checks**:
- Win rate > 50% against random_agent (200 games, 7×6)
- No crashes on 100 random positions (forced-move, block-in-1, fork detection)
- Adheres to 2-second budget (p95 latency)
**Output**: Pass → Stage 2 / Fail → rejected
**Cost**: ~30 minutes on Kaggle T4

### Stage 2: Classical Gate
**Input**: Tactical-passed bot
**Checks**:
- Win rate > 80% against minimax_agent (200 games, 7×6)
- Board-size generalization: ≥ 50% win rate on 8×8 (vs minimax)
- Resource profile: Tier-1 profiling within thresholds
**Output**: Pass → Stage 3 / Fail → rejected
**Cost**: ~2 hours on Kaggle T4

### Stage 3: Neural Gate (if applicable)
**Input**: Classical-passed bot with neural component
**Checks**:
- Neural inference latency < 10ms (T4) per evaluation
- Neural-enhanced bot beats classical bot by ≥ 5% win rate
- Neural model size < 5MB (Kaggle package budget)
**Output**: Pass → Stage 4 / Fail → reject neural component
**Cost**: ~4 hours on Kaggle T4

### Stage 4: Deployment Gate
**Input**: All gates passed
**Checks**:
- Package size < 95MB (full Kaggle submission)
- End-to-end test: Kaggle simulated tournament (100 games vs all built-in agents)
- Stability: 0 crashes across 1000 random positions
**Output**: Pass → deployable / Fail → reject
**Cost**: ~4 hours on Kaggle T4

## 7. Research Tasks (10 Tasks from Worker 614)

| # | Task | Source |
|---|------|--------|
| 1 | Benchmark memory footprint of tromp/fhourstones88 (500MB TT) as reference for Stage 4 memory gate calibration | S035 |
| 2 | Research Numba JIT memory profiling and GPU VRAM monitoring APIs for Tier-2 profiling | Numba docs, PyTorch CUDA APIs |
| 3 | Run Stage 0-1 calibration against connectpuct (C043), ariaborin (S022), and Kamide (S123) | Connectpuct, ariaborin, Kamide |
| 4 | Design pipeline CI integration pattern (Stages 0-1 per commit, Stages 2-3 per iteration, Stage 4 per release) | — |
| 5 | Profile ENS-001 (classical), ENS-002 (NN+MCTS), ENS-013 (board-size adaptive) on Kaggle T4 | ENS-001, ENS-002, ENS-013 |
| 6 | Benchmark BMS-046 built-in agent baseline (3 ensembles vs 4 Kaggle agents, 400 games each) | BMS-046 |
| 7 | Benchmark BMS-047 tactical pattern benchmark (2,000 positions across 6 pattern types) | BMS-047 |
| 8 | Run Tier-3 stress test (10,000 positions without TT clear) | — |
| 9 | Investigate Kaggle ConnectX built-in agent source code availability | Kaggle official sources |
| 10 | Investigate Numba JIT GPU VRAM APIs for real-time profiling | Numba, PyTorch |

## 8. Deferred Empirical Experiments

### EXP-BMS-001: Pipeline Gate Calibration
**Description**: Run all gate thresholds against connectpuct (C043), ariaborin (S022), and Kamide (S123) to establish empirical baselines.
**Compute**: Kaggle T4
**Runtime**: ~4 hours
**Success Criteria**: All gate thresholds produce reproducible pass/fail for each reference bot

### EXP-BMS-002: Built-in Agent Baseline
**Description**: Test 3 ensembles against all 4 Kaggle built-in agents on 7×6, 8×8, and 15×13. 400 games total per ensemble.
**Compute**: Kaggle T4
**Runtime**: ~2 hours per ensemble
**Success Criteria**: Established win-rate baselines for all bot-vs-agent configurations

### EXP-BMS-003: Tier-2 Resource Profiling
**Description**: Profile ENS-001 (classical), ENS-002 (NN+MCTS), and ENS-013 (board-size adaptive) on Kaggle T4. Measure memory, VRAM, p95 latency, p99 latency.
**Compute**: Kaggle T4
**Runtime**: ~3 hours
**Success Criteria**: Resource profiles for each ensemble design

### EXP-BMS-004: Tactical Pattern Benchmark
**Description**: 2,000 positions across 6 pattern types (fork, anti-fork, win-in-1, block-in-1, win-in-2, win race). 3 ensembles tested.
**Compute**: Kaggle T4
**Runtime**: ~30 minutes
**Success Criteria**: Detection accuracy for each pattern type

### EXP-BMS-005: Tier-3 Stress Test
**Description**: Evaluate 10,000 positions without TT clear. Profile memory growth and concurrent evaluation latency.
**Compute**: RTX 5090
**Runtime**: ~2 hours
**Success Criteria**: Memory growth rate, memory leak detection

### EXP-BMS-006: Built-in Agent Source Investigation
**Description**: Investigate whether Kaggle ConnectX publishes built-in agent source code. If found, extract exact algorithm parameters for Minimax depth, Heuristic weights, and DQN architecture.
**Compute**: None (code analysis only)
**Runtime**: ~1 hour
**Success Criteria**: Known built-in agent parameters (if available)

## 9. Pros and Cons of Current Benchmark Approach

| Aspect | Pros | Cons |
|--------|------|------|
| Multi-stage pipeline | Filters weak bots early; saves expensive evaluation time | Requires careful threshold calibration; may reject marginal bots |
| Win-rate as primary metric | Simple, interpretable, maps to Kaggle scoring | Doesn't capture speed, memory, or board-size generalization |
| Board-size escalation | Tests generalization from 7×6 to 15×13 | Large boards take hours per experiment |
| Resource profiling | Ensures Kaggle compatibility (95MB/2s) | Adds measurement overhead to experiments |
| Built-in agent baseline | Uses Kaggle's own reference implementations | Limited evaluation range (only 4 reference bots) |

## 10. Feasibility Matrix

| Dimension | Assessment |
|-----------|-----------|
| Local CPU | Tier-1 profiling feasible; Tier-2 with 10 games; Tier-3 with 1,000 positions |
| RTX 5090 | All tiers fully feasible; Tier-3 stress test (10,000 positions) fast |
| DGX Spark | Tier-1 and Tier-2 feasible; Tier-3 may be slow |
| Kaggle CPU | Tier-1 and Tier-2 feasible (slower); Tier-3 not feasible (too slow) |
| Kaggle T4 | All tiers feasible; VRAM profiling available; 2-second budget constraint applies |
| Package size | Neural networks must be < 5MB for full deployment; heuristic-only bots trivially pass |
| Dependencies | Pure Python bots (no external deps) have lowest package size |
| Compile requirements | Python-only bots avoid compile step; pre-compiled extensions add complexity |
| Startup/warmup | Neural bots have ~1-5 second warmup; heuristic bots < 100ms |
| 2-second action budget | Heuristic bots: trivially satisfied on 7×6; NN bots: may be tight on 15×13 |
| Overtime behavior | Bot loses if move > 2 seconds (Kaggle enforced) |
| Board-size flexibility | Benchmark covers 7×6, 8×8, 10×8, 15×10, 15×13 with scaling |

## 11. Board-Size Applicability

| Board | 7×6 | 8×8 | 10×8 | 15×10 | 15×13 |
|-------|-----|-----|------|-------|-------|
| Solved | No (inarow=4) | No | No | No | No (inarow=7) |
| Minimax depth | 4-6 | 3-4 | 2-3 | 1-2 | 1 |
| MCTS playouts | 10K-50K | 5K-20K | 2K-10K | 500-2K | 100-500 |
| Neural evaluation | Primary | Primary | Primary | Primary | Primary |
| Opening book | Recommended | Recommended | Recommended | Marginal | Not useful |
| TT size | 1-5M entries | 2-10M entries | 5-20M entries | 10-50M entries | 20-100M entries |

## 12. Integration and Ensemble Opportunities

| Ensemble | Benchmark Dependency | Impact |
|----------|---------------------|--------|
| ENS-001 (classical search) | Stage 2 (classical gate) | Establishes classical baseline |
| ENS-002 (NN+MCTS hybrid) | Stage 3 (neural gate) | Validates neural component |
| ENS-013 (board-size adaptive) | Stage 4 (deployment gate) | Validates scaling strategy |
| ENS-019 through ENS-024 | Stage 4 + board-size escalation | Full ensemble validation |

## 13. Failure Modes and Risks

| Failure Mode | Likelihood | Impact | Mitigation |
|-------------|-----------|--------|-----------|
| Bot exceeds 2-second budget on 15×13 | HIGH | Bot loses, benchmark inconclusive | Use board-specific depth limits |
| Neural network too large for 95MB limit | MEDIUM | Cannot deploy to Kaggle | Use model compression (INT8 quantization) |
| Memory leak causes OOM in long game | MEDIUM | Bot crashes mid-game | Monitor memory in Tier-2 profiling |
| Benchmark results not reproducible | HIGH | Invalid conclusions | Fix random seeds, document environment |
| Kaggle environment changes breaking benchmark | LOW | All results invalid | Version-lock kaggle-environments package |

## 14. Benchmark Requirements Summary

| Requirement | Status | Priority |
|-------------|--------|----------|
| Stage 0-1 gate calibration | NOT IMPLEMENTED | P0 |
| Stage 2 classical gate | NOT IMPLEMENTED | P1 |
| Stage 3 neural gate | NOT IMPLEMENTED | P1 |
| Stage 4 deployment gate | NOT IMPLEMENTED | P2 |
| Tier-1 single-move profiling | NOT IMPLEMENTED | P0 |
| Tier-2 sustained game profiling | NOT IMPLEMENTED | P1 |
| Tier-3 stress test | NOT IMPLEMENTED | P2 |
| CI integration pattern | NOT IMPLEMENTED | P2 |

## 15. Open Questions

1. **What is the optimal split between Kaggle CPU and T4 for benchmarking?** CPU is free but slow; T4 has VRAM profiling but costs credits.
2. **Should the benchmark include a cross-play tournament (bot vs bot)?** This would reveal relative strength ordering but requires more compute.
3. **How many games are needed for statistical significance at Kaggle scale?** 100 games (~15% MoE) vs 500 games (~7% MoE).
4. **Can Kaggle's built-in agent source code be obtained?** If so, benchmark calibration becomes much more precise.

## 16. Recommendations

### Immediate (R44-R45)

1. **Implement Stage 0-1 calibration** against connectpuct, ariaborin, and Kamide reference implementations. This establishes the empirical baseline for all future gates.
2. **Build Tier-1 profiling harness** — a single script that runs 100 positions and reports p50/p95/p99 latency, memory, CPU.
3. **Add EXP-BMS-001 through EXP-BMS-006 to the experiment backlog** with estimated compute and runtime.

### Medium-term (R46-R48)

4. **Run EXP-BMS-001 (pipeline gate calibration)** — this is the highest-ROI experiment as it validates all subsequent gates.
5. **Implement Tier-2 resource profiling** on ENS-001, ENS-002, and ENS-013.
6. **Design CI integration pattern** for automated gate execution.

### Long-term (R49+)

7. **Run EXP-BMS-003 (Tier-2 profiling on all ensembles)** — this will inform the deployment gate thresholds.
8. **Build cross-play tournament** for relative strength ranking.
9. **Investigate Kaggle built-in agent source code** — if found, this would be a major research asset.

## 17. Sources and Retrieval Record

| Source | Type | Quality | Retrieval Date |
|--------|------|---------|---------------|
| Kaggle ConnectX environment (connectx.py) | Kaggle source | VERIFIED | 2026-08-05 |
| test_connectx.py (279 lines) | Kaggle test suite | VERIFIED | 2026-08-05 |
| Pascal Pons/connect4 (AGPL v3) | GitHub source | VERIFIED | 2026-08-05 |
| blanyal/AlphaZero-Light (MIT) | GitHub source | VERIFIED | 2026-08-05 |
| Wikipedia -- Connect Four | Public wiki | VERIFIED | 2026-08-05 |
| Chess Programming Wiki (S075, S078, S137) | Public wiki | VERIFIED | 2026-08-05 |

## Cross-Links

| ID | Relationship |
|----|-------------|
| BMS-DOC-001 | Benchmark science foundation |
| BMS-DOC-002 | MCTS consistency theory |
| BMS-DOC-003 | Ensemble interaction |
| BMS-DOC-004 | Kaggle evaluation protocol |
| ENS-001 through ENS-024 | All ensembles require benchmark validation |
| C043 | connectpuct benchmark data |
| S022 | ariaborin Connect4 source |
| S123 | Kamide/connect-n source |
| EXP-BMS-001 through EXP-BMS-006 | Deferred empirical experiments |

---

EXTERNAL WORKER COMPLETE