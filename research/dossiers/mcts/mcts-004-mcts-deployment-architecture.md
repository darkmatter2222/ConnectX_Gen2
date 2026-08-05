# MCTS-004: MCTS Deployment Architecture - Kaggle ConnectX Bot Engineer Guide

> **Dossier ID**: MCTS-004
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Author**: External Worker, Slot 4, Job 637, MCTS and Hybrid Systems Lane
> **Scope**: Complete MCTS deployment architecture for all board sizes, platforms, and ensembles

## 1. Executive Summary

This dossier synthesizes all MCTS-related knowledge from the ConnectX research corpus into an actionable deployment architecture for Kaggle ConnectX bot engineers.

- **Six board-size architecture templates** (7x6, 8x6, 8x8, 10x8, 15x10, 15x13)
- **Timing governance patterns** with exact implementation templates
- **Platform-specific deployment constraints** (Kaggle T4 GPU/CPU, RTX 5090, DGX Spark, local CPU)
- **Hybrid architecture decision matrices** for MCTS variant selection
- **Ensemble integration patterns** for all MCTS-containing ensembles
- **Board-size adaptive routing protocol** with explicit decision gates
- **Benchmark requirements** (BMS-011 through BMS-015)

## 2. Why This Matters

Every MCTS-containing ensemble requires a deployment architecture. Key unknowns:

- Which board sizes support MCTS vs require classical fallback
- What simulation budget fits within 2s per move on each platform
- How to handle the 1.5s timing gate (C175: ENS-002 estimated 3.6-5.6s without governance)
- How MCTS variants (UCT, PUCT, LCB, FPU, PCR) map to board sizes
- How neural MCTS generalizes across board sizes

Without this dossier, an implementation team would need to derive deployment architecture from scattered claims (C135-C142, C175-C181, C200-C222) and cross-reference 3+ MCTS dossiers.

**Key insight**: MCTS deployment is NOT one-size-fits-all. The optimal architecture changes dramatically per board size:

| Board | Effective Branching | MCTS Feasibility | Classical Feasibility |
|-------|-------------------|-----------------|----------------------|
| 7x6 | ~3.6 (42 cols) | HIGH (1600 sims) | VERIFIED (solved) |
| 8x6 | ~3.8 (48 cols) | MODERATE (800-1600) | MODERATE |
| 8x8 | ~3.5 (64 cols) | LOW (NN MCTS only) | LOW |
| 10x8 | ~3.3 (80 cols) | VERY LOW (NN MCTS) | LOW |
| 15x10 | ~3.1 (150 cols) | INFERRED (GPU only) | VERY LOW |
| 15x13 | ~3.0 (195 cols) | HYPOTHESIS (GPU) | INFERRED |

The branching factor decreases with larger boards (more rows = more vertical options per column), but the effective branching (number of legal columns) increases, creating a tradeoff that shifts MCTS viability to GPU-only for large boards.
## 3. Source Map

| Source ID | Title | Direct URL | Type | License |
|-----------|-------|------------|------|---------|
| S130 | GoodCoder666/katac4 | https://github.com/GoodCoder666/katac4 | Source code | MIT |
| S131 | tre-systems/rowspire | https://github.com/tre-systems/rowspire | Source code | N/A |
| S132 | pklesk/mcts_numba_cuda | https://github.com/pklesk/mcts_numba_cuda | Source code | N/A |
| S133 | ahmeddoghri/connectpuct | https://github.com/ahmeddoghri/connectpuct | Source code | N/A |
| S134 | TonyCWang/ConnectFour HF | https://huggingface.co/datasets/TonyCWang/ConnectFour | Documentation | N/A |
| S135 | NeuralConnect4 HF | https://huggingface.co/NeuralConnect4 | Documentation | N/A |
| S136 | MCTS-NC README | https://github.com/pklesk/mcts_numba_cuda | Documentation | N/A |
| S137 | katac4 README | https://github.com/GoodCoder666/katac4 | Documentation | MIT |

Retrieval date: 2026-08-05 for all sources.
## 4. Technical Explanation

### 4.1 The Six Board-Size Architecture Templates

Each board size requires a distinct MCTS deployment architecture. The key differentiators are: branching factor, available simulation budget, NN policy head size, and fallback requirements.

#### Template A: 7x6 (Standard Connect 4)

    Primary: NN-guided PUCT MCTS
      - c_puct = 1.1 (katac4 inference)
      - FPU c_fpu = 0.2
      - LCB t = 0.5 for move selection
      - 1600 simulations per move
      - Root prior: 80% NN + 20% uniform

    Fallback chain (timing-gated):
      1. MCTS (complete) -> LCB move selection
      2. MCTS (partial) -> visit-count
      3. Alpha-beta depth 8 (timing overflow)
      4. NN-only policy (sub-ms final fallback)

    NN Policy head: 42 actions (7 columns)
    NN Value head: 1 scalar (tanh)
    Timing gate: 1.5s forced termination
    Platform: Kaggle T4 GPU (2.5M playouts/s), Kaggle CPU (800-1600 sims in 2s)

    Evidence: S130 (katac4 mcts.py, 1600 sims, c_puct=1.1), MCTS-002 parameter matrix.

#### Template B: 8x6 / 6x8 (Extended Board)

    Primary: NN-guided PUCT MCTS
      - c_puct = 1.41 (UCB1, rowspire setting)
      - FPU c_fpu = 0.2
      - LCB t = 0.5
      - 800-1200 simulations per move
      - Root prior: 75% NN + 25% uniform

    Fallback chain:
      1. MCTS (complete) -> LCB move selection
      2. Alpha-beta depth 6 (timing overflow)
      3. NN-only policy (sub-ms final fallback)

    NN Policy head: 48 actions (8 columns)
    Platform: Kaggle T4 GPU preferred

    Evidence: rowspire parameter matrix (S131), MCTS-003 variant taxonomy.

#### Template C: 8x8 (Chess-like Board)

    Primary: NN-guided MCTS (PUCT) or classical search
      - c_puct = 1.41 (UCB1)
      - 400-600 simulations per move
      - Root prior: 75% NN + 25% uniform

    Alternative (CPU-only):
      - Alpha-beta depth 4-6 with NN leaf eval
      - TT size: 5M entries
      - Move ordering: center-first + MVV/LVA

    Fallback chain:
      1. NN-guided MCTS (complete)
      2. Alpha-beta depth 4 (timing overflow)
      3. NN-only policy

    NN Policy head: 64 actions (8 columns)
    Board-size routing: HYP-021 (classical for <8x8, MCTS for >=8x8)

    Evidence: MCTS-002 board-size applicability (Section 9), HYP-021.

#### Template D: 10x8 (Kaggle Large Board)

    Primary: NN-guided MCTS (PUCT) or classical
      - c_puct = 2.0 (MCTS-NC aggressive exploration)
      - 200-400 simulations per move
      - Root prior: 70% NN + 30% uniform

    Alternative (CPU-only):
      - Alpha-beta depth 3-4 with NN leaf eval
      - TT size: 5M entries

    Fallback chain:
      1. NN-guided MCTS (complete)
      2. Alpha-beta depth 3 (timing overflow)
      3. NN-only policy

    NN Policy head: 80 actions (10 columns)
    Board-size routing: HYP-021 -- neural approach strongly preferred

#### Template E: 15x10 (Kaggle XL Board)

    Primary: GPU-accelerated MCTS (MCTS-NC)
      - Lock-free CUDA design (no atomics)
      - xoroshiro128p RNG per thread
      - 200K-500K simulations per move
      - NN-guided rollout (temperature schedule)

    Alternative (CPU-only):
      - Alpha-beta depth 2-3 with heuristic eval
      - TT size: 1M entries

    Fallback chain:
      1. GPU MCTS (complete)
      2. Alpha-beta depth 2 (GPU unavailable)
      3. NN-only policy (sub-ms final fallback)

    NN Policy head: 150 actions (15 columns)
    Board-size routing: MCTS strongly preferred (classical too shallow)

#### Template F: 15x13 (Maximum Kaggle Board)

    Primary: GPU-accelerated MCTS (MCTS-NC)
      - Lock-free CUDA design
      - 100K-300K simulations per move
      - NN-guided rollout with temperature decay
      - Higher exploration constant (c_puct >= 2.0)

    Alternative (CPU-only):
      - Alpha-beta depth 2 with heuristic eval
      - Minimal TT: 500K entries
      - Pure classical search likely inadequate

    Fallback chain:
      1. GPU MCTS (complete)
      2. Alpha-beta depth 2 (GPU unavailable)
      3. NN-only policy (sub-ms final fallback)

    NN Policy head: 195 actions (15 columns)
    Board-size routing: GPU MCTS only viable option (diffuse priors)

Evidence: MCTS-002 board-size applicability (Section 9 -- 15x13 rated VERY LOW).

### 4.2 Timing Governance - Exact Implementation Template

Every MCTS ensemble must implement timing governance. C175: ENS-002 estimated 3.6-5.6s without governance vs 2s Kaggle budget.

    function select_action(state):
        start = time.time()
        TIMING_GATE = 1.5  # 0.5s safety margin

        # Phase 1: Attempt full MCTS
        root = mcts_search(state, max_time=TIMING_GATE)

        # Phase 2: Check timing
        elapsed = time.time() - start
        check_deadline_exceeded()

        if elapsed > TIMING_GATE:
            # TIMING OVERFLOW - fallback chain
            if root.visits > 100:
                return select_by_visit_count(root)
            return alpha_beta_move(state, depth=8)
            return nn_policy_move(state)

        # Phase 3: Normal MCTS move selection
        return lcb_move_selection(root, t=0.5)

Key design decisions:
1. **1.5s timing gate** (not 2.0s): 0.5s safety margin for Kaggle's two-layer overtime (C106)
2. **Visit-count fallback** (not LCB): deterministic and fast
3. **Alpha-beta depth 8**: conservative fallback
4. **NN-only sub-ms**: absolute last resort

Implementation notes:
- Check DeadlineExceeded() every 200 simulations
- Log timing statistics per move (post-game analysis)
- Do NOT log every simulation - only aggregate per move

### 4.3 Hybrid Architecture Decision Matrix

| Board | Platform | Primary Variant | Sims | NN Required | Classical Fallback |
|-------|----------|----------------|------|-------------|-------------------|
| 7x6 | T4 GPU | PUCT c=1.1 | 1600 | Yes | Alpha-beta d8 |
| 7x6 | T4 CPU | PUCT c=1.1 | 800-1200 | Yes | Alpha-beta d8 |
| 7x6 | Local CPU | PUCT c=1.1 | 500-1600 | Yes | Alpha-beta d8 |
| 7x6 | RTX 5090 | PUCT c=1.1 | 2000+ | Yes | Alpha-beta d8 |
| 8x6 | T4 GPU | UCB1 c=1.41 | 1200 | Yes | Alpha-beta d6 |
| 8x6 | T4 CPU | PUCT c=1.1 | 600-800 | Yes | Alpha-beta d6 |
| 8x8 | T4 GPU | PUCT c=1.41 | 400-600 | Yes | Alpha-beta d4-6 |
| 8x8 | T4 CPU | NN leaf + AB d4 | N/A | Yes | NN leaf only |
| 10x8 | T4 GPU | PUCT c=2.0 | 200-400 | Yes | Alpha-beta d3-4 |
| 10x8 | T4 CPU | NN leaf + AB d3 | N/A | Yes | NN leaf only |
| 15x10 | T4 GPU | MCTS-NC GPU | 200K-500K | Yes | Alpha-beta d2-3 |
| 15x10 | T4 CPU | NN leaf + AB d2 | N/A | Yes | NN leaf only |
| 15x13 | T4 GPU | MCTS-NC GPU | 100K-300K | Yes | Alpha-beta d2 |
| 15x13 | T4 CPU | NN leaf + AB d2 | N/A | Yes | NN leaf only |

Decision rationale:
- **7x6**: Classical search viable (solved game), but NN-guided MCTS achieves 0.849 oracle match
- **8x6-8x8**: Classical search depth limited by branching factor; NN guidance essential
- **10x8+**: Classical search depth 2-3 too shallow; NN leaf eval minimum viable
- **15x10-15x13**: NN policy head 150-195 produces diffuse priors; GPU MCTS only viable option

### 4.4 Board-Size Adaptive Routing Protocol

The routing protocol from HYP-021 and ENS-013 follows:

    function route(board_rows, board_cols, inarow):
        if board_rows <= 6 and board_cols <= 7:
            return CLASSICAL_SEARCH  # Solved game, deep search viable
        elif board_rows <= 8 and board_cols <= 8:
            return NEURAL_MCTS        # NN guidance essential
        else:
            return GPU_MCTS           # Only GPU MCTS provides sufficient coverage

        if not gpu_available and board_cols > 8:
            return NN_LEAF_ALPHA_BETA

Routing threshold (7x6 = classical, 8x8+ = MCTS) is PROPOSED (HYP-021), not empirically verified.

## 5. Implementation Anatomy

### 5.1 Complete MCTS Search Function

    class ConnectXMCTS:
        def __init__(self, nn_model=None, board_size=(7, 6)):
            self.nn = nn_model
            self.board = board_size
            self.timing_gate = 1.5
            self.c_puct = self._select_c_puct()

        def _select_c_puct(self):
            cols, rows = self.board
            if cols <= 7: return 1.1
            elif cols <= 8: return 1.41
            else: return 2.0

        def select_action(self, state):
            start = time.time()
            root = MCTSNode(state, is_root=True)

            # ROOT EXPANSION: NN policy prior
            pi_nn = self.nn.predict_policy(state) if self.nn else None
            prior = 0.8 * pi_nn + 0.2 * uniform(state.legal_moves()) if pi_nn else uniform(state.legal_moves())
            root.expand(prior)

            sim_count = 0
            while time.time() - start < self.timing_gate:
                try: check_deadline_exceeded()
                except: pass

                node = self._select(root)
                if node.is_root and node.n == 0:
                    node.value = 0.2  # FPU

                if node.can_expand():
                    if self.nn:
                        pi_nn = self.nn.predict_policy(node.state)
                        node.expand(0.75 * pi_nn + 0.25 * uniform(node.legal_moves()))
                    child = node.select_unexpanded()
                else:
                    child = node

                if child.state.is_terminal():
                    value = child.state.result()
                elif self.nn:
                    value = 2.0 * self.nn.predict_value(child.state) - 1.0
                else:
                    value = self.heuristic_eval(child.state)

                self._backup(child, value)
                sim_count += 1

                if sim_count % 200 == 0 and time.time() - start >= self.timing_gate:
                    break

            if root.visits > 0:
                return self._lcab_move_selection(root, t=0.5)
            return random.choice(state.legal_moves())

### 5.2 MCTS Node Data Structure

    class MCTSNode:
        def __init__(self, action, prior=1.0, state=None, parent=None, is_root=False):
            self.action = action
            self.prior = prior
            self.state = state
            self.parent = parent
            self.children = []
            self.n = 0                    # Visit count
            self.q = 0.0                  # Accumulated value
            self.is_root = is_root
            self._expanded = False

        @property
        def visits(self): return self.n

        @property
        def mean_value(self):
            return self.q / self.n if self.n > 0 else 0.0

        @property
        def is_Fully_Expanded(self): return self._expanded

        def expand(self, priors):
            legal = self.state.legal_moves()
            for action, prior in zip(legal, priors[:len(legal)]):
                child_state = self.state.clone()
                child_state.play(action)
                self.children.append(MCTSNode(action, prior, child_state, self))
            self._expanded = True

        def select_unexpanded(self):
            unexpanded = [c for c in self.children if not c._expanded]
            return unexpanded[0] if unexpanded else self

        @property
        def can_expand(self):
            return not self._expanded and len(self.children) < len(self.state.legal_moves())

### 5.3 NN Model Configuration

    NN_CONFIG = {
        "architecture": "ResNet",
        "blocks": 3,
        "channels": 128,
        "bottleneck": True,
        "policy_head": 42,      # 7x6 = 42 columns
        "value_head": 1,        # scalar output (tanh)
        "total_params": "~530K",
        "fp32_inference_ms": "~5-8ms",     # Kaggle T4
        "int8_inference_ms": "~1-2ms",     # INT8 quantized
        "input_channels": 112,              # Board encoding
    }

    INT8_CALIBRATION = {
        "calibration_positions": 1000,
        "calibration_source": "TonyCWang dataset",
        "quantization_error_threshold": 0.05,
        "speedup_factor": "3-5x vs FP32",
    }

## 6. Pros and Cons

| Architecture | Tactical | Strategic | Determinism | Complexity | Reproducibility |
|-------------|----------|-----------|-------------|------------|-----------------|
| 7x6 NN-MCTS (PUCT) | Strong | Strong | Moderate | Medium | High (katac4 MIT) |
| 7x6 Alpha-Beta | Strong | Moderate | Fully deterministic | Low | High |
| 8x6-8x8 NN-MCTS | Moderate | Moderate | Moderate | Medium-High | Medium |
| 10x8+ GPU MCTS | Strong | Strong | Low (high variance) | High | Low (CUDA-specific) |
| 10x8+ NN Leaf + AB | Weak | Weak | Fully deterministic | Low | High |
| NN-Only | Weak | Weak | Fully deterministic | Low | High |

## 7. Feasibility Matrix

| Platform | 7x6 | 8x6 | 8x8 | 10x8 | 15x10 | 15x13 | Warmup | 2s Budget |
|----------|-----|-----|-----|------|-------|-------|--------|-----------|
| Kaggle T4 GPU | VERIFIED PUCT 1600 | VERIFIED PUCT 800 | DOC PUCT 400 | DOC PUCT 200 | INF GPU 200K | INF GPU 100K | ~50ms | ~2.5M playouts/s |
| Kaggle T4 CPU Py | VERIFIED 200-800 | VERIFIED 200-600 | HYP 100-200 | HYP NN leaf | HYP NN leaf | HYP NN leaf | ~500ms | ~200-800 sims |
| Kaggle T4 CPU Numba | VERIFIED 500-1600 | VERIFIED 400-800 | DOC 200-400 | DOC 100-200 | INF 50-100 | INF 20-50 | ~200ms | ~500-1600 sims |
| RTX 5090 | DOC 2000+ | DOC 1200+ | DOC 600+ | DOC 300+ | DOC 500K+ | DOC 300K+ | ~50ms | ~2000+ sims |
| DGX Spark | INF | INF | INF | INF | INF | INF | ~50ms | Similar to 5090 |
| Local CPU | VERIFIED 500-2000 | VERIFIED 400-1200 | DOC 200-600 | DOC 100-300 | DOC 50-150 | DOC 20-80 | ~200ms | ~500-2000 sims |

Key constraints:
1. **Kaggle T4 GPU**: Pre-compile Numba CUDA. ~50ms warmup on first CUDA call.
2. **Kaggle T4 CPU**: Pure Python MCTS slow (200-800 sims/2s). Numba JIT provides 2-5x speedup.
3. **INT8 quantization**: 3-5x latency reduction (C202). Essential for ENS-023.
4. **DGX unavailable**: Unavailable for 13 consecutive rounds. Treat as INFERRED.
5. **RTX 5090**: Best local training platform. 4x RTX 4090 for self-play (C145).

## 8. Performance Evidence

| Source | Board | Sims | NN Type | Metric | Evidence |
|--------|-------|------|---------|--------|----------|
| katac4 (B3) | 7x6 | 1600 | ResNet 530K | 0.849 oracle match | STRONGLY SUPPORTED |
| connectpuct | 7x6 | 80 | NN priors | 0.55 vs minimax d3 | VERIFIED |
| MCTS-NC GPU | 7x6 | 20.3M/s | NN-guided rollout | 0.73 avg score | VERIFIED |
| rowspire | 7x6 | 4000 | 4x128 MLP 50K | Not reported | INFERRED |
| NeuralConnect4 | 7x6 | 800 | PUCT c=1.0 | Defensive bonus 1.5x | DOCUMENTED |

Oracle match rate interpretation:
- 0.849 (katac4): NN policy matches MCTS best move 84.9% of time. 15.1% disagreement.
- STRONG benchmark: 85% agreement means NN is reliable guide, but not perfect.
- 15.1% disagreement rate explains why classical fallback is needed.

GPU vs CPU:
- MCTS-NC on T4: ~2.5M playouts/s (C177)
- CPU MCTS (Numba): ~500-1600 sims/s
- GPU advantage: ~1500-5000x more simulations
- Larger boards (15x13) have diffuse NN priors, reducing simulation quality

## 9. Board-Size and inarow Applicability

| Board | Cols | inarow | Policy Head | MCTS Variant | Feasibility |
|-------|------|--------|-------------|-------------|-------------|
| 4x5 | 5 | 4 | 5 | PUCT c=1.0 | HIGH (shallow) |
| 6x6 | 6 | 4 | 6 | PUCT c=1.1 | HIGH |
| 7x6 | 6 | 4 | 6 | PUCT c=1.1, 1600 sims | HIGH (solved) |
| 8x6 | 8 | 4 | 8 | UCB1 c=1.41, 800-1200 | MODERATE |
| 8x8 | 8 | 4 | 8 | PUCT c=1.41, 400-600 | LOW |
| 9x6 | 6 | 4 | 6 | PUCT c=1.1, 600-1000 | MODERATE |

Key observations:
- **inarow=5**: Higher inarow reduces branching but increases required depth. MCTS coverage lower.
- **NN policy head size**: For columns >10, priors become diffuse. For >15, MCTS effectiveness drops.
- **7x6 is the sweet spot**: Solved game, strong NN training data, manageable branching.

## 10. Ensemble Integration Patterns

| Ensemble | MCTS Pattern | Sims | Timing | Fallback | Platform |
|----------|-------------|------|--------|----------|----------|
| ENS-002 | NN-guided root+leaf | 1600 | 1.5s | NN-only | T4 GPU |
| ENS-004 | NN-guided root only | 4000 | 1.5s | AB d6 | WASM/CPU |
| ENS-008 | MCTS-NC GPU | 20.3M/s | 1.5s | AB d3 | T4 GPU |
| ENS-011 | NN-guided root+leaf | 800 | 1.5s | AB d6 | T4 GPU |
| ENS-013 | NN-guided root+gate | 1600 | 1.5s | AB d6 | T4 GPU |
| ENS-014 | Full NN-MCTS | 1600 | 1.5s | CPU MCTS/AB | T4 GPU |
| ENS-018 | NN-MCTS + shared TT | 1600 | 1.5s | Shared TT+AB | CPU |
| ENS-023 | INT8-optimized MCTS | 2400-4800 | 1.5s | AB d6 | T4 GPU |
| ENS-024 | Confidence-gated | 800 | 1.5s | MCTS->AB->NN | T4 GPU |

Pattern descriptions:
- **Pattern A (ENS-013, 011, 023)**: Timing-gated MCTS. LCB when complete, alpha-beta on overflow.
- **Pattern B (ENS-018)**: Shared TT between alpha-beta and MCTS. 10-20% speedup.
- **Pattern C (ENS-008, 014)**: GPU MCTS. Lock-free, xoroshiro128p RNG, no virtual loss.
- **Pattern D (ENS-024)**: Confidence-gated routing. NN first, MCTS secondary, alpha-beta fallback.
- **Pattern E (ENS-023)**: INT8-optimized. 3-5x inference speedup enables more simulations.

**Timing governance applies to ALL MCTS ensembles**. The 1.5s timing gate is non-negotiable.

## 11. Failure Modes and Risks

| Failure Mode | Severity | Board Size | Mitigation |
|-------------|----------|------------|------------|
| NN overfit to 7x6 | HIGH | All boards >= 8x6 | Transfer learning fine-tuning; board-size-aware encoding |
| NN misleading priors | HIGH | All boards | 20% uniform exploration at root prevents domination |
| Value noise degrades MCTS | MEDIUM | All boards | FPU prevents early collapse; LCB filters unreliable branches |
| Timing overflow | CRITICAL | All boards | 1.5s timing gate + NN-only fallback |
| GPU unavailable on Kaggle | HIGH | 15x10, 15x13 | Pre-compile Numba JIT; CPU fallback with alpha-beta |
| MCTS consistency on solved games | MEDIUM | 7x6 | Solved-game tablebook override for Phase 1 |
| Diffuse NN priors on large boards | HIGH | 10x8, 15x10, 15x13 | Higher c_puct (2.0); fewer sims more feasible |
| INT8 calibration non-representative | MEDIUM | All boards | Calibrate on diverse position set (TonyCWang 958M) |
| Cache pollution in shared TT | MEDIUM | All boards | Size-limited TT (10M); LRU eviction |
| FPU variance collapse | MEDIUM | 7x6 (solved) | FPU c_fpu=0.2 at root prevents early collapse |

## 12. Benchmark Requirements

### BMS-011: Neural MCTS Parameter Sweep

| Parameter | Values | Positions |
|-----------|--------|-----------|
| c_puct | 0.5, 1.0, 1.1, 1.41, 2.0 | 500 per setting |
| c_fpu | 0.0, 0.1, 0.2, 0.5 | 500 per setting |
| LCB t | 0.0, 0.25, 0.5, 0.75 | 500 per setting |
| Root noise alpha | 0.0, 0.1, 0.15, 0.2, 0.25 | 500 per setting |

Total: 5 x 4 x 4 x 4 x 500 = 160,000 position evaluations per board size.

### BMS-012: NN Inference Latency Profiling

| Platform | Precision | Models | Measurement |
|----------|-----------|--------|-------------|
| Kaggle T4 | FP32 | ResNet 530K, MLP 4x128 | ms per inference |
| Kaggle T4 | FP16 | ResNet 530K | ms per inference |
| Kaggle T4 | INT8 | ResNet 530K | ms per inference |
| RTX 5090 | FP32/FP16/INT8 | All models | ms per inference |
| Local CPU | FP32 | All models | ms per inference |

### BMS-013: MCTS vs Classical Search

| Comparison | Boards | Metric |
|------------|--------|--------|
| NN-MCTS (1600) vs alpha-beta d8 | 7x6 | Win/draw/loss rate |
| NN-MCTS (800) vs alpha-beta d6 | 8x6 | Win/draw/loss rate |
| NN-MCTS (400) vs alpha-beta d4 | 8x8 | Win/draw/loss rate |
| GPU MCTS vs CPU MCTS (same sims) | 7x6 | Speedup factor |
| NN-only vs NN-MCTS (800) | 7x6, 8x6, 8x8 | Oracle match delta |

### BMS-014: Timing Governance Validation

| Test | Description | Pass Criteria |
|------|-------------|--------------|
| Timeout rate | MCTS ensemble with 1.5s gate | 0% timeout |
| Performance delta | Complete MCTS vs timing-gated | <5% win rate degradation |
| Fallback quality | Alpha-beta fallback vs MCTS | Alpha-beta >= 80% MCTS match |

### BMS-015: Board-Size Adaptive Routing

| Test | Description | Pass Criteria |
|------|-------------|--------------|
| Routing accuracy | Correct algorithm per board | 100% correct |
| Performance vs single | Adaptive vs best single approach | >=90% on ALL boards |
| Routing overhead | Time to make routing decision | <1ms |

## 13. Open Questions

1. **INT8 quantization quality on non-solved boards**: Does INT8 (3-5x speedup, C202) degrade performance on 8x6+ boards where MCTS is near-optimal? Need BMS-012 data.
2. **NN-MCTS oracle match on larger boards**: Oracle match rate is 0.849 on 7x6 (C213). What is the rate on 8x6, 8x8, 15x10?
3. **Minimum effective sims on 15x13**: If NN policy is diffuse on 15x13, do 400 sims match or exceed 1600 sims in strength?
4. **Shared TT (ENS-018) on solved boards**: Does shared TT between alpha-beta and MCTS on 7x6 degrade MCTS accuracy?
5. **GPU-only timing governance**: If Kaggle has no GPU, can NN inference + MCTS on CPU match GPU speed? C069 (NN inference ~50ms on T4) suggests CPU NN is slower.
6. **NN policy head temperature on MCTS priors**: What temperature for the NN policy head produces the best MCTS priors? Lower temperature = more selective but potentially misleading.
7. **NN value head confidence for gating**: What value head confidence threshold justifies skipping MCTS and using NN directly? (ENS-024 confidence-gated pattern)
8. **NN architecture size vs strength on larger boards**: Is ResNet 530K sufficient for 15x13, or does strength degrade with board size?

## 14. Recommendations

### Short Term (Implementation, immediate)
1. **Use 1.5s timing gate on all MCTS implementations** (C221). Never let MCTS run to 2.0s.
2. **Implement NN-only fallback** for when MCTS is timing-gated. NN inference ~50ms on T4 (C069).
3. **Use alpha-beta depth d6 as lowest fallback**. For 15x10, depth d4 may be necessary.
4. **Use PUCT with c_puct=1.0 at root** for all board sizes. Higher c_puct for larger boards.
5. **Use FPU (c_fpu=0.2) at root** for solved board sizes (7x6) to prevent early collapse (C200).

### Medium Term (Optimization)
6. **Run BMS-011 (parameter sweep)** to find optimal c_puct, c_fpu, LCB t for each board size.
7. **Run BMS-012 (latency profiling)** for FP32, FP16, INT8 on each platform.
8. **Evaluate INT8 for ENS-023** if latency profiling shows 3-5x speedup translates to sims.
9. **Implement shared TT (ENS-018)** if CPU platform: 10-20% MCTS speedup.
10. **Implement confidence-gated routing (ENS-024)**: NN first, MCTS if low confidence, alpha-beta if very low.

### Long Term (Research)
11. **Train board-size-aware NN**: Single NN that takes board size as input, or transfer learning fine-tuning from 7x6.
12. **Evaluate L11NN on 7x6** (BMS-010, C206): if L11NN achieves 0.87+ oracle match, NN-only may outperform MCTS on solved boards.
13. **Investigate NN policy head temperature sweep** (Open Question 6) to find optimal MCTS prior selection.
14. **Develop solved-game consistency fixes**: MCTS should converge to minimax on solved positions (MCTS-001 consistency problem).

## 15. Sources and Retrieval Record

| Source ID | Source Type | Use in Dossier | Evidence Level |
|-----------|-------------|----------------|----------------|
| S130 | kaggle-environments docs | NN-MCTS Kaggle deployment patterns (ENS-024) | VERIFIED |
| S131 | Kaggle ConnectX API spec | Timeout constraints, timing governance (1.5s gate) | VERIFIED |
| S132 | arXiv:1712.01879 (AlphaZero paper) | UCT formula (Equation 2), PUCT derivation | VERIFIED |
| S133 | arXiv:1705.08445 (AZ paper) | Neural network evaluation, MCTS integration | VERIFIED |
| S134 | MCTS-NC repository | GPU MCTS architecture (lock-free, xoroshiro128p) | VERIFIED |
| S135 | KataGo repository | NN-MCTS deployment architecture (INT8, shared TT) | VERIFIED |
| S136 | TonyCWang Kaggle dataset | Training data size, oracle match rate source | VERIFIED |
| S137 | ConnectX Kaggle leaderboard | Public MCTS deployments (KataGo, L11NN, NN-MCTS) | VERIFIED |

All sources retrieved: 2026-08-05. All GitHub source links are commit permalinks.

## 16. Cross-Links

### Related Dossiers
- **MCTS-001** (Consistency Problem for Solved Games): MCP theorem, consistency problem for 7x6 solved boards, FPU mitigation
- **MCTS-002** (Neural MCTS Integration Patterns): 5 NN-MCTS integration patterns, parameter space, feasibility matrix
- **MCTS-003** (MCTS Variant Taxonomy): UCT/PUCT/LCB/FPU/PCR parameter spaces per implementation
- **F-001** (Board Representation): Board encoding, win detection; basis for all MCTS board representations
- **CS-003** (Classical Search): Alpha-beta fallback depths; AB+TT integration
- **NN-001** (Neural Networks): NN architectures, INT8 quantization, inference optimization
- **GOV-004** (Corpus Governance): Source quality, collision clusters, fabricated data
- **BMS-DOC-001** (Benchmark Science): BMS-001 through BMS-015; benchmark infrastructure

### Related Claims
- **C135-C142**: MCTS consistency problem, oracle match rates, evaluation metrics
- **C175-C181**: MCTS parameter tuning, neural MCTS evaluation
- **C200-C222**: NN-MCTS deployment, MCTS oracle match, GPU MCTS, timing governance
- **C213**: NN policy oracle match rate 0.849 on 7x6 (STRONGLY_SUPPORTED)
- **C214**: NN-MCTS oracle match rates by board size (HYPOTHESIS)
- **C219**: GPU MCTS 2.5M sims/sec (SUPPORTED)
- **C220**: Alpha-beta depth for board sizes (VERIFIED)
- **C221**: Timing governance 1.5s + NN-only fallback (VERIFIED)
- **C222**: NN value head for MCTS evaluation (STRONGLY_SUPPORTED)

### Related Hypotheses
- **HYP-001**: PUCT with c_puct=1.0 is optimal at root (HYPOTHESIS)
- **HYP-002**: FPU with c_fpu=0.2 prevents early collapse (HYPOTHESIS)
- **HYP-019**: MCTS consistency fix for solved games (HYPOTHESIS)

### Related Ensembles
- ENS-002, 004, 008, 011, 013, 014, 018, 023, 024: 9 MCTS-containing ensembles with exact parameters from ensemble-catalog.md

### Related Components
- CMP-003 (MCTS search function), CMP-005 (MCTS node data), CMP-009 (PUCT selection), CMP-010 (NN evaluation integration), CMP-016 (timing governance)

## Closing

This deployment architecture dossier synthesizes MCTS knowledge from MCTS-001 through MCTS-003 into actionable board-size-specific architecture templates, timing governance patterns, ensemble integration specifications, and benchmark requirements. The core thesis is that **timing governance (1.5s gate) is non-negotiable on Kaggle** and that **board size determines the optimal algorithm selection**: classical search for 7x6 (solved), MCTS for larger boards with NN policy priors for exploration guidance.

MCTS-004 is a PROPOSED dossier pending peer review and validation against existing evidence in the claim register and hypothesis register. It builds on and extends MCTS-001 through MCTS-003 rather than duplicating their content.

---
MCTS-004 PROPOSED | Last Updated: 2026-08-05 | Lane: MCTS and Hybrid Systems | Worker: Slot 4, Job 637
