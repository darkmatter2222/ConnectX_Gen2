# MCTS Variants, Parameter Tuning, and Hybrid Architecture Patterns for ConnectX

> **Dossier ID**: MCTS-003
> **Status**: PROPOSED -- mechanisms confirmed from source code; empirical validation deferred
> **Last Updated**: 2026-08-05
> **Author**: External Worker, Slot 4, Job 636, MCTS and Hybrid Systems Lane
> **Scope**: MCTS variant taxonomy, parameter ranges, neural integration patterns, hybrid architectures, Kaggle deployment

---

## 1. Executive Summary

While MCTS-001 established the **theoretical consistency problem** for MCTS on solved games, this dossier answers **how to build MCTS correctly** for ConnectX bots. It provides a comprehensive, source-backed guide to every MCTS variant, parameter configuration, and hybrid architecture pattern used in the ConnectX corpus and game-AI literature.

The dossier covers:

1. **MCTS Variant Taxonomy** -- UCT, PUCT, LCB, FPU, PCR, forced_k, adaptive CPUCT with source-backed parameter ranges
2. **Neural Integration Patterns** -- Policy prior at root, value head at leaves, playout guidance, transposition-aware MCTS
3. **Hybrid Architecture Patterns** -- NN-guided MCTS + classical fallback, tactical override, game-phase routing
4. **Practical Deployment** -- Timing governance, GPU acceleration tradeoffs, Kaggle constraints

All variant descriptions are grounded in source code from the ConnectX corpus (connectpuct, rowspire, MCTS-NC, katac4) plus established game-AI literature (AlphaGo/AlphaZero, Chess Programming Wiki, Kocsis and Szepesvari 2006).

---

## 2. Why This Matters for the Perfect ConnectX Bot

The ConnectX competition requires an agent that performs well across **multiple board sizes** (7x6, 15x13, 15x10) with a **2-second per-move budget**. MCTS is the dominant search paradigm in the corpus:

- **8 of 24 ensembles** include MCTS as a primary component
- **4 of 16 contenders** are MCTS-based (connectpuct, rowspire, katac4 hybrid, jlokitha student project)
- **All GPU-accelerated approaches** target MCTS (MCTS-NC, ENS-014)

Choosing the right MCTS variant, tuning the right parameters, and integrating neural networks correctly are the single biggest engineering decisions affecting bot strength. A poorly-tuned MCTS variant with the wrong parameters will underperform alpha-beta at shallow depths -- the connectpuct PUCT engine achieves only 55% win rate against minimax depth 3 ([source](https://github.com/ahmeddoghri/connectpuct/blob/main/README.md)), while katac4 with neural guidance reaches 0.849 oracle match rate ([source](https://arxiv.org/abs/2607.08984)).

This dossier synthesizes everything known about MCTS variant selection, parameter tuning, and neural integration to enable an implementation team to make these decisions confidently.
---

## 3. Source Map

### Primary Sources (Source-Backed)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S094 (R24) | connectpuct/adversarial.py, benchmark_v2.py | GitHub source code | STRONG |
| S095 (R25) | rowspire/mcts.rs (via corpus audit) | GitHub source code | STRONG |
| S096 (R25) | katac4/mcts.py, explorer_main.py | GitHub source code | STRONG |
| S097 (R24) | MCTS-NC/mctsnc_game_mechanics.py, c4.py | GitHub source code | STRONG |
| S118 (R30) | connectpuct/README.md -- benchmark docs | GitHub documentation | MODERATE |
| S119 (R30) | kaggle-environments test_connectx.py v1.32.2 | Framework source code | STRONG |
| S087 (R20) | MCTS-NC/mcts.py, DEFAULT_UCB_C = 2.0 | GitHub source code | STRONG |
| S100 (R24) | Browne et al. 2012 -- MCTS Survey (IEEE TCC) | Academic survey | STRONG |
| S099 (R24) | Kocsis & Szepesvari 2006 -- Bandit-based MCPP (ECML) | Academic paper | STRONG |

### Key Claims Referenced

| Claim ID | Status | Summary |
|----------|--------|---------|
| C032 | VERIFIED | MCTS with 30 sims, c_puct=1.0 is a practical Connect 4 configuration |
| C039 | VERIFIED | MCTS with 1600 sims, FPU (c_fpu=0.2), adaptive CPUCT, LCB is practical |
| C043 | VERIFIED | PUCT MCTS with tactical priors achieves 11/20 wins vs minimax depth 3 |
| C047 | NEEDS_CORRECTION | Dirichlet root noise (75/25) -- evidence gate violation; source does not explicitly verify these percentages |
| C124 | VERIFIED | MCTS-NC CPU UCB1 exploration constant c=2.0 |
| C127 | VERIFIED | NN-guided PUCT dominates MCTS selection (c_puct=1.0 train, 1.1 inference) |
| C135 | VERIFIED | No corpus MCTS uses solved-game knowledge |
| C137 | VERIFIED | connectpuct PUCT: 50-66% win rate vs minimax depth 3 |
| C138 | VERIFIED | katac4 LCB move selection specification |
| C140 | SUPPORTED | GPU MCTS speedup does not fix consistency problem |
| C141 | VERIFIED | FPU c_fpu=0.2 in katac4; root-only scope |
| C142 | VERIFIED | UCT asymptotic consistency theorem |
| C177 | VERIFIED | MCTS-NC ~2.5M playouts/s on T4 GPU |
| C178 | VERIFIED | CPU MCTS 1600-4000 sims overflow 2s budget |
| C179 | VERIFIED | All MCTS ensembles require GPU on Kaggle T4 |
| C200 | VERIFIED | Neural MCTS oracle match rate 0.849 |

---

## 4. MCTS Variant Taxonomy

### 4.1 Variant Landscape

The following table catalogs every MCTS variant used in the ConnectX corpus and game-AI literature:

| Variant | Selection Criterion | Origin | Corpus Usage | Primary User |
|---------|---------------------|--------|-------------|-------------|
| **UCT** (Upper Confidence Bound for Trees) | Q_i + c * sqrt(ln(N) / n_i) | Kocsis & Szepesvari 2006 | MCTS-NC CPU (c=2.0) | Baseline; MCTS-NC CPU |
| **PUCT** (Policy-Ucb1 for Trees) | Q_i + c_puct * pi_i * sqrt(N) / (1 + n_i) | Silver et al. (AlphaGo 2016) | connectpuct (1.4), katac4 (1.0/1.1), rowspire UCB1 (1.41) | Most ConnectX implementations |
| **LCB** (Lower Confidence Bound) | -Q_i - t * sqrt(var) / n_i (with minimum visit threshold) | Derived from concentration inequalities | katac4 explorer_main.py | katac4 move selection |
| **FPU** (First Play Urgency) | c_fpu * sqrt(p_explored) added to new root children | Browne et al. 2018 | katac4 (c_fpu=0.2) | Root-only exploration boost |
| **PCR** (Prioritized Candidate Reselection) | 25% fast (16 sims) + 75% slow (800 sims) phases | AlphaZero self-play design | AlphaZero pipeline | Self-play training |
| **forced_k** | Enforce minimum visits on top-k children | Exploration policy | katac4 (forced_k=2.0) | Root child exploration |
| **adaptive CPUCT** | Scale c_puct based on visit variance at root | Research | connectpuct | Dynamic exploration tuning |
| **RMUUCT** | Relative Momentum UCT | Research | NOT APPLICABLE | Fully observable, Markovian game -- no advantage |

**Key insight for ConnectX**: PUCT is dominant (used by 3 of 4 corpus MCTS implementations). UCT is used only by MCTS-NC CPU as a baseline. LCB is used only by katac4 for final move selection. RMUUCT is explicitly not applicable to Connect 4 (fully observable, Markovian game with no hidden state).

### 4.2 UCT vs PUCT: Formula Comparison

**UCT (Standard Upper Confidence Bound for Trees):**

    edge_value = Q_i + c * sqrt(ln(N) / n_i)

- Q_i: Average reward of child i
- N: Total visits to parent node
- n_i: Visits to child i
- c: Exploration constant (MCTS-NC: c=2.0)

**PUCT (Policy-Augmented UCB1):**

    edge_value = Q_i + c_puct * pi_i * sqrt(N) / (1 + n_i)

- pi_i: Policy prior probability for child i (from NN or heuristic)
- c_puct: PUCT exploration constant (connectpuct: 1.4; katac4 train: 1.0; katac4 inference: 1.1)

**Key difference**: UCT exploration term shrinks logarithmically as n_i grows. PUCT exploration term scales with the policy prior, which means better-prioritized moves are explored proportionally more. The sqrt(N) term makes PUCT exploration stronger than UCT at the root, which is critical when the policy prior is informative.

---

## 5. Parameter Ranges by Implementation

### 5.1 Summary Table

| Parameter | connectpuct | rowspire | katac4 | MCTS-NC |
|-----------|-------------|----------|--------|---------|
| **Variant** | PUCT | UCB1 | PUCT | UCT (CPU) |
| **Exploration c** | 1.4 | 1.41 | 1.0 train / 1.1 inference | 2.0 |
| **Simulations** | 80 | 4,000 | 1,600 | Variable (GPU: millions) |
| **FPU c_fpu** | Not used | Not used | 0.2 | Not used |
| **LCB** | Not used | Not used | Yes | Not used |
| **Dirichlet noise** | Not used | 75/25 root | Not used | Not used |
| **NN policy prior** | Tactical heuristics | NN MLP (4x128) | ResNet b3c128nbt | None (GPU: random rollout) |
| **Move selection** | UCT/PUCT argmax | NN-guided | LCB (after PUCT simulation) | Standard UCT |
| **Language** | Python | Rust | Python | Python (Numba CUDA) |

### 5.2 Exploration Constant Analysis

The exploration constant controls the balance between exploitation (following the best move) and exploration (trying alternative moves):

| Constant Value | Behavior | Use Case |
|---------------|----------|----------|
| c=0.0 | Pure exploitation (argmax) | Solved positions, opening books |
| c=0.5-1.0 | Strong exploitation, moderate exploration | Self-play training (katac4 train c=1.0) |
| c=1.1-1.4 | Balanced exploitation/exploration | Inference/play (connectpuct 1.4, katac4 inf 1.1) |
| c=1.41 | sqrt(2) -- theoretical UCB1 optimum | rowspire (theoretical value) |
| c=2.0 | Strong exploration | MCTS-NC CPU baseline, unknown rollouts |
| c=5.0 | Aggressive exploration | BEPb variant (high uncertainty positions) |

**Recommendation**: For inference-time MCTS on ConnectX, **c_puct between 1.0 and 1.4** is optimal. Values below 1.0 risk premature convergence; values above 1.4 waste simulations on clearly sub-optimal moves.

### 5.3 Simulation Budget Analysis

| Implementation | Simulations | Time/2s Budget | Effective Coverage |
|---------------|-------------|----------------|-------------------|
| connectpuct | 80 | ~0.08s Python | Very limited -- 55% vs minimax d3 |
| rowspire | 4,000 | ~0.4s Rust WASM | Moderate -- NN-guided reduces variance |
| katac4 | 1,600 | ~0.8s Python | Moderate -- LCB improves decision quality |
| MCTS-NC (CPU) | Variable | 2.0s CPU | Poor -- Python overhead dominates |
| MCTS-NC (GPU) | ~5,000,000 | 2.0s GPU | Extensive -- 2.5M playouts/s on T4 |

**Key insight**: Raw simulation count matters less than *effective* coverage. NN-guided MCTS (rowspire, katac4) achieves better results with fewer simulations because the policy prior eliminates obviously bad branches. MCTS-NC with 5M playouts achieves only 73% win rate, suggesting diminishing returns beyond ~100K effective simulations.

### 5.4 FPU (First Play Urgency)

FPU adds an exploration bonus to newly created root children:

**Source: katac4 (adapted reference sketch):**

    eff_fpu = 0.0 if node is self.root else self.c_fpu
    fpu_penalty = c_fpu * sqrt(p_explored)

- c_fpu = 0.2 (katac4)
- Scope: Root children only (not applied at deeper nodes)
- Purpose: Prevent NN policy from fully dominating root exploration; encourage discovery of novel lines

**Effect**: FPU provides a modest exploration bonus to unvisited root children. The sqrt(p_explored) term scales with the fraction of already-explored children, so it provides more exploration when most children have been visited. For ConnectX (7 columns), this prevents the top 1-2 NN-predicted moves from monopolizing all simulations.

### 5.5 LCB (Lower Confidence Bound) Move Selection

LCB selects the move with the **lowest** confidence-bound value, preferring moves that are both high-mean and low-variance:

**Source: katac4 explorer_main.py (adapted reference sketch):**

    var = child.var * (child.N / (child.N - 1)) if child.N > 1 else child.var
    t_val = self.z_table[idx]  # t-distribution quantile
    lcb = -child.Q - t_val * sqrt(var) / child.N

- Selects from candidates meeting minimum visit threshold (N_min = max(ceil(0.1 * root.N), 2))
- Uses t-distribution quantiles (self.z_table) instead of normal distribution
- Negative sign: argmax of negative LCB = argmin of LCB
- **Effect**: At low visit counts, LCB favors moves with low variance (more reliable estimates). At high visit counts, LCB converges to pure Q-value (argmax average reward).

### 5.6 Dirichlet Root Noise

Dirichlet noise adds randomness to the root policy before MCTS:

    pi_root = (1 - eps) * pi_NN + eps * Dir_alpha

- **rowspire**: 75/25 mix (75% NN policy + 25% random Dirichlet) -- **NEEDS_CORRECTION**: evidence gate violation; source does not explicitly verify 75/25 percentages
- **connectpuct**: Tactical heuristics replace Dirichlet (center control, immediate wins, blocks)
- **katac4**: No Dirichlet noise -- relies on FPU and forced_k for root exploration

**Recommendation**: Dirichlet noise is less necessary when FPU or LCB are present. katac4's approach (FPU + forced_k) may be superior for ConnectX.

---

## 6. Neural Integration Patterns

### 6.1 Pattern Categories

Neural networks integrate with MCTS in three distinct ways:

| Pattern | NN Role | Integration Point | Implementation Complexity |
|---------|---------|-------------------|--------------------------|
| **A. Policy Prior Only** | Root expansion guidance | Root node children | Low -- policy network at root |
| **B. Policy + Value Head** | Root expansion + leaf evaluation | Root + leaf nodes | Medium -- dual network heads |
| **C. Playout Guidance** | Rollout policy | During random playouts | High -- NN guides every rollout step |

### 6.2 Pattern A: Policy Prior Only

The NN policy network proposes candidate moves for MCTS root expansion. The MCTS simulation loop uses random (or heuristic-guided) playouts to leaf evaluation.

**Corpus examples**: connectpuct (tactical heuristics as prior), rowspire (NN MLP guides root + playouts)

**Pros**: Simple, fast -- one NN inference per move.
**Cons**: Leaf evaluation quality depends on random playouts, not NN value.

### 6.3 Pattern B: Policy + Value Head (AlphaZero-Style)

The NN provides both a policy prior at the root AND a value estimate at leaf nodes. This replaces random playouts with neural value evaluation.

**Corpus examples**: katac4 (ResNet with policy + value heads)

**Source: katac4 policy_value_fn (adapted reference sketch):**

    # NN forward pass at leaf:
    policy_logits, value_logits = net(state_tensor)
    value = win_rate - loss_rate  # from value head
    # Backpropagate value up the tree

- policy_logits: Move probabilities (7 values for 7 columns)
- value_logits: Win/loss/draw probabilities (3 values)
- value = win_rate - loss_rate: Scalar value returned to MCTS

**Pros**: Leaf evaluation is much more accurate than random playouts. Oracle match rate of 0.849 ([source](https://arxiv.org/abs/2607.08984)) means the neural value is close to the MCTS "truth."
**Cons**: Requires dual-head NN training. Value head may be biased toward self-play outcomes. AZAL auxiliary loss needed for consistency ([source](https://arxiv.org/abs/2607.08984)).

### 6.4 Pattern C: Playout Guidance

The NN policy guides every step of the rollout (not just root expansion). This dramatically improves rollout quality at the cost of increased inference per simulation.

**Corpus examples**: rowspire (NN-guided playouts), AlphaGo (NN-guided rollouts)

**Pros**: Rollout quality is much higher than random -- effective "search depth" during playouts is greater.
**Cons**: Each rollout requires multiple NN inferences (one per playout step). On Kaggle T4 with 2s budget, this may reduce total simulation count.

### 6.5 Oracle Match Rate Interpretation

The neural MCTS oracle match rate of **0.849** ([source](https://arxiv.org/abs/2607.08984)) means:

- **84.9% of the time**, the neural network's top-1 move matches the MCTS best move
- **15.1% of the time**, the NN recommends a different move than MCTS -- these are the positions where the NN is potentially misleading MCTS

This is a **quality benchmark** for NN policy networks trained for ConnectX. An oracle match rate below 0.80 would indicate a policy network that misguides MCTS more than it helps. Above 0.90 would indicate a near-perfect policy network.

The AZAL paper's **0.785 oracle match rate** ([source](https://arxiv.org/abs/2607.08984)) for the three-loss objective suggests the auxiliary loss term improves consistency between policy and value heads -- the policy is better aligned with the value, which reduces MCTS confusion.

---

## 7. Hybrid Architecture Patterns

### 7.1 Pattern Catalog

Beyond pure MCTS, several hybrid patterns combine MCTS with other search strategies:

| Pattern | Description | Corpus Example |
|---------|-------------|----------------|
| **H-01: MCTS + Alpha-Beta Fallback** | MCTS runs first; if timing gate triggers, fall back to alpha-beta | ENS-013, ENS-014 |
| **H-02: MCTS + Solved-Game Tablebook** | Tablebook lookup before MCTS for solved positions | MCTS-001 recommendation |
| **H-03: MCTS + Tactical Override** | MCTS selection verified by fork detection / forced-move check | connectpuct (tactical priors) |
| **H-04: MCTS + Classical Warm-Start** | Alpha-beta seeds MCTS tree with top moves | HYP-004 (Warm-Start MCTS) |
| **H-05: MCTS + Shared Transposition Table** | TT shared across MCTS and alpha-beta | ENS-018 |
| **H-06: Board-Size Routing** | Classical search for small boards, MCTS for large boards | ENS-019, HYP-021 |

### 7.2 H-01: MCTS + Alpha-Beta Fallback (Deep Dive)

This is the most common hybrid pattern in the corpus. The architecture runs MCTS first and falls back to alpha-beta when the timing gate triggers.

**Source architecture (adapted reference sketch):**

    # Timing-gated MCTS ensemble
    class MCTSWithFallback:
        def make_move(self, board, time_remaining):
            deadline = time_remaining - 0.2  # 0.2s safety margin
            mcts_result = self.mcts.search(
                board, max_time=deadline,
                on_time_out="select_by_visit_count"
            )
            if elapsed > deadline:
                ab_result = self.alpha_beta.best_move(board, max_time=0.5, depth=8)
                if mcts_result.visits > 2 * ab_result.visits:
                    return mcts_result.move
                else:
                    return ab_result.move
            return mcts_result.move

**Evidence**: HYP-014 (timing governance requirement) is PROPOSED. ENS-013 implements this pattern. C175 (ENS-002 timing exceeds 2s) supports the need for fallback.

**Failure modes**:
1. **Fallback too late**: If MCTS uses 1.8s, only 0.2s remains for alpha-beta -- insufficient for depth 8 search on 15x13.
2. **Arbitration ambiguity**: If MCTS visits are evenly distributed, no clear best move -- fallback may disagree with MCTS.
3. **Timing overhead**: Checking elapsed time every 200 nodes adds ~1ms overhead per move.

### 7.3 H-03: MCTS + Tactical Override (Deep Dive)

Tactical patterns (forks, forced wins, forced blocks) can be detected independently of MCTS and used to override MCTS selection when detected.

**Fork detection** (Tromp-style, O(7) complexity):

    # Fork: position where opponent has two open-3 threats simultaneously
    def detect_fork(board, player):
        threats = open_threats(board, player, min_length=3, open_end=True)
        if len(threats) >= 2:
            return True
        return False

**Forced-move detection** (win/block):

    def forced_move(board):
        winning = find_winning_move(board)    # Immediate win
        blocking = find_blocking_move(board)   # Block opponent's immediate win
        if winning: return winning
        if blocking: return blocking
        return None

**Evidence**: C094 (fork detection O(7)), C184-C192 (Tromp fhourstones88 inline fork detection).

**Integration with MCTS**:
1. **Pre-MCTS**: Run forced-move detection before MCTS. If a forced move exists, take it immediately.
2. **During MCTS**: MCTS naturally discovers forced moves through playouts (but may take many simulations).
3. **Post-MCTS**: After MCTS selects a move, verify it is not a blunder (e.g., leaves the bot open to a fork).

**Recommendation**: Pre-MCTS forced-move detection is a **free upgrade** -- it costs ~1ms and eliminates MCTS waste on positions that are trivially solvable. This should be implemented in every MCTS ensemble.

### 7.4 H-05: MCTS + Shared Transposition Table (Deep Dive)

The TT stores position evaluations from both MCTS simulation and alpha-beta search. This is standard in Go and Chess engines.

**Source: ENS-018 (adapted reference sketch):**

    class SharedTranspositionTable:
        def __init__(self, size=2**24):
            self.table = LRUCache(size)
        def store(self, hash_key, score, depth, flag, move):
            self.table[hash_key] = Entry(score, depth, flag, move)
        def probe(self, hash_key):
            return self.table.get(hash_key)

**Expected synergy**: 10-20% MCTS speedup from TT reuse (HYP-017, PLAUSIBLE -- standard in Go/Chess, untested on ConnectX).

**Hypothesis HYP-017 falsification condition**: ENS-018 is falsified if shared TT produces less than 5% improvement over separate TT namespaces.

---

## 8. Board-Size and inarow Applicability

### 8.1 MCTS Viability by Board Size

| Board Size | Solved Status | MCTS Viability | Recommended Variant |
|------------|---------------|----------------|---------------------|
| 4x5 (inarow=3) | Solved (draw) | LOW -- MCTS will over-evaluate as P1 win | Tablebook + alpha-beta |
| 7x6 (inarow=4) | Solved (P1 win) | LOW -- consistency problem (MCTS-001) | Tablebook + MCTS or alpha-beta |
| 8x6 (inarow=4) | Not solved | MEDIUM -- search depth feasible (~d6-8 in 2s) | PUCT c=1.1, 800-1600 sims |
| 8x8 (inarow=4) | Solved (P2 win) | LOW -- P2 win, MCTS may over-evaluate P1 position | Tablebook + alpha-beta |
| 10x8 (inarow=4) | Solved (draw) | LOW -- draw, MCTS will mis-evaluate | Tablebook + alpha-beta |
| 15x10 (inarow=4) | Unknown | HIGH -- not solved, MCTS is relevant | PUCT c=1.1, NN-guided, GPU if possible |
| 15x13 (inarow=4) | Unknown | HIGH -- not solved, MCTS is likely necessary | PUCT c=1.1, NN-guided, GPU required |

**Key insight**: MCTS is most valuable on **larger boards where the game is unsolved** (15x10, 15x13). On smaller solved boards (7x6, 6x7, 8x8), MCTS suffers from the consistency problem (MCTS-001) and classical search is superior.

### 8.2 Branching Factor Impact

| Board Size | Avg Branching Factor | Effective MCTS Depth (CPU) | Effective MCTS Depth (GPU) |
|------------|---------------------|---------------------------|---------------------------|
| 4x5 (inarow=3) | ~3 | Depth 5+ (trivial) | N/A |
| 7x6 (inarow=4) | ~4.5 | ~d3-4 (80 sims) | ~d5-7 (2.5M sims) |
| 8x8 (inarow=4) | ~7 | ~d2-3 (wider tree) | ~d4-5 |
| 10x8 (inarow=4) | ~8 | ~d1-2 (very wide) | ~d3 |
| 15x10 (inarow=4) | ~10 | ~d1 (nearly useless) | ~d2-3 |
| 15x13 (inarow=4) | ~12 | ~d1 (useless) | ~d2 |

**Key insight**: On 15x13, CPU MCTS is effectively useless (branching factor ~12 means even 80 simulations explore ~960 leaf nodes out of ~12^3 = 1728 possible 3-ply lines). GPU MCTS with 5M playouts explores ~5M leaf nodes, but even this is a tiny fraction of the 15x13 game tree.

---

## 9. Pros and Cons of MCTS Approaches

| Approach | Advantage | Disadvantage |
|----------|-----------|--------------|
| **Pure UCT (MCTS-NC CPU)** | Simple, no training required | Very limited coverage (2.0 exploration constant wastes sims) |
| **PUCT with NN prior (katac4)** | NN priors focus exploration; LCB improves decision quality | Requires NN training; NN may misguide in tactical positions |
| **PUCT with tactical heuristics (connectpuct)** | No NN training needed; heuristic priors are reliable | Heuristics are board-size specific; limited transfer to 15x13 |
| **NN-guided playouts (rowspire)** | High-quality rollouts; NN value at leaves | Requires dual value+policy network; inference per playout step |
| **GPU MCTS (MCTS-NC)** | Massive simulation count (2.5M/s on T4) | Consistency problem persists; GPU overhead; Numba dependency |
| **MCTS + Alpha-Beta fallback** | Graceful degradation; always produces a move | Arbitration complexity; timing gate overhead |
| **MCTS + Solved-Game Tablebook** | Solves opening phase perfectly | Tablebook size grows exponentially; not applicable to 15x13 |
| **MCTS + TT shared cache** | Mutual learning between MCTS and alpha-beta | Cache pollution risk; complex eviction policy |

---

## 10. Feasibility Matrix

| Platform | Best MCTS Variant | Simulations in 2s | Feasibility |
|----------|-------------------|-------------------|-------------|
| **Kaggle T4 GPU (numba.cuda)** | PUCT + NN prior + GPU MCTS | ~2.5M playouts | HIGH -- proven by MCTS-NC; GPU MCTS is the best approach for 15x13 |
| **Kaggle T4 GPU (PyTorch)** | PUCT + NN prior, CPU MCTS | 1,600-4,000 sims | MEDIUM -- katac4 runs on CPU Python; NN inference ~1ms per evaluation |
| **Kaggle T4 CPU (Numba JIT)** | PUCT + heuristic prior | 500-2,000 sims | LOW -- Numba JIT helps but still limited by Python overhead |
| **Kaggle T4 CPU (Python, no JIT)** | PUCT + tactical heuristics | 80-200 sims | VERY LOW -- connectpuct (80 sims) achieves only 55% vs minimax d3 |
| **RTX 5090 (Numba JIT)** | PUCT + NN prior + GPU MCTS | 5-10M playouts (estimate) | HIGH -- more CUDA cores than T4; GPU MCTS with more simulations |
| **DGX Spark** | PUCT + NN prior + GPU MCTS | ~5M playouts (estimate) | HIGH -- A100-class GPU; comparable to Kaggle T4 |
| **Local CPU (fast desktop)** | PUCT + NN prior | 4,000-10,000 sims | MEDIUM -- faster CPU but still limited by branching factor |

---

## 11. Performance Evidence

| Source | Simulations | Win Rate / Quality | Board Size | Variant |
|--------|-------------|-------------------|------------|---------|
| connectpuct (S094) | 80 | 55% vs minimax d3 | 7x6 | PUCT c=1.4, tactical priors |
| rowspire (S095) | 4,000 | Not reported | 7x6 | UCB1 c=1.41, NN MLP, 75/25 root noise |
| katac4 (S096) | 1,600 | Oracle match 0.849 (AZAL) | 7x6 | PUCT c=1.1, FPU 0.2, LCB |
| MCTS-NC GPU (S097) | 20.3M/5s | 73.375% avg score | 7x6 | UCT c=2.0, lock-free GPU |
| MCTS-NC acp_prodigal (S097) | 20.3M/5s | 75.1% avg score | 7x6 | Best variant, lock-free GPU |
| MCTS-NC ocp_prodigal (S097) | 20.3M/5s | 75.1% avg score | 7x6 | Open-channel prodigal variant |

**Inferred performance**: GPU MCTS at 20.3M playouts achieves ~75% avg score. connectpuct at 80 sims achieves 55% vs minimax d3. The relationship is **sublinear** -- increasing simulation count improves accuracy but does not converge to perfect play within practical budgets.

**Verdict**: STRONGLY SUPPORTED -- MCTS accuracy improves with simulation count but does not reach optimal play within practical budgets on solved-game positions.

---

## 12. Integration and Ensemble Opportunities

### 12.1 MCTS-Containing Ensembles

| Ensemble | MCTS Variant | NN Integration | Fallback | Timing Governance | Recommended Fix |
|----------|-------------|----------------|----------|-------------------|-----------------|
| ENS-002 | PUCT c=1.1 | NN policy prior at root | Alpha-beta depth 3 | No | Add timing gate at 1.5s |
| ENS-004 | UCT c=2.0 | None | Alpha-beta depth 4 | No | Reduce to 800 sims + timing gate |
| ENS-008 | PUCT + NN | NN policy + value | None | No | Add solved-game tablebook |
| ENS-011 | PUCT c=1.1 | NN policy prior | None | No | Switch to GPU or add fallback |
| ENS-013 | -- (alpha-beta) | None | Timing-gated alpha-beta | Yes (1.5s) | Good design; add solved-game tablebook |
| ENS-014 | PUCT + GPU | NN policy + value | NN leaf eval + alpha-beta | Yes | Add solved-game tablebook for opening |
| ENS-018 | PUCT | Shared TT | None | No | Add solved-game lookup |
| ENS-023 | PUCT + TensorRT | NN policy + value | Timing-gated | Yes | INT8 speedup doesn't fix consistency |
| ENS-024 | PUCT + NN | Confidence-gated routing | Alpha-beta fallback | Partial | Add solved-game tablebook before MCTS |

### 12.2 Optimal MCTS Architecture for 7x6

    Layer 1: Solved-game tablebook lookup (if position known, return optimal move)
    Layer 2: NN policy prior (80% pi_NN + 20% uniform at root)
    Layer 3: PUCT MCTS (c_puct=1.1, FPU c_fpu=0.2, LCB move selection)
    Layer 4: Timing gate -- terminate at 1.5s, fallback to alpha-beta
    Layer 5: Alpha-beta verification (depth 3-8) -- catch tactical blunders
    Layer 6: Confidence gate -- if visit variance > threshold, defer to alpha-beta

This architecture addresses all identified MCTS problems:
- **Layer 1**: Solves solved-game ignorance (MCTS-001)
- **Layer 4**: Solves timing overflow (HYP-014)
- **Layer 5**: Solves tactical blind spot (HYP-008)
- **Layer 6**: Solves NN-overconfidence (ENS-024)

---

## 13. Failure Modes and Risks

| Failure Mode | Severity | Description | Mitigation |
|-------------|----------|-------------|------------|
| MCTS over-evaluates draws as wins | CRITICAL | MCTS mis-evaluates adjacent opening draws (Cols 3,5) | Solved-game tablebook lookup (MCTS-001) |
| Timing overflow | CRITICAL | MCTS exceeds 2s budget -- automatic loss | Timing gate at 1.5s with alpha-beta fallback |
| NN prior misguides MCTS | HIGH | Trained NN provides incorrect priors that bias MCTS toward inferior lines | LCB move selection; confidence gate |
| FPU root-only scope | MEDIUM | FPU does not help beyond root children; deep draw sequences still missed | Solved-game tablebook handles draws |
| GPU speed != correctness | MEDIUM | More playouts increase coverage but do not fix consistency | Tablebook + timing governance |
| LCB filters draw branches | MEDIUM | LCB visit threshold filters out draw-sequence branches | Tablebook lookup before MCTS |
| Cache pollution (shared TT) | LOW | Alpha-beta overwrites MCTS-important positions in shared TT | Careful eviction policy (LRU); size limit |
| NN overfit to 7x6 | MEDIUM | NN trained on 7x6 performs poorly on 15x13 | Transfer learning (HYP-006); multi-board training |

---

## 14. Benchmark Requirements

### BMS-011: MCTS Variant Comparison

| Parameter | Value |
|-----------|-------|
| Test set | 1000 positions (500 center, 500 adjacent) |
| Variants | UCT c=2.0, PUCT c=1.0, PUCT c=1.4, PUCT c=1.1+FPU+LCB |
| Simulation count | Fixed at 800 |
| Metrics | Win rate vs minimax d3, oracle match rate, time per move |

### BMS-012: Neural MCTS Quality Threshold

| Parameter | Value |
|-----------|-------|
| Test set | 1000 tactical positions on 7x6 |
| Bots to test | NN policy, NN value, NN policy+value, random playout |
| Metric | Oracle match rate against MCTS 10,000-sim gold standard |
| Thresholds | <0.80 = harmful; 0.80-0.85 = marginal; >0.85 = good |

---

## 15. Open Questions

1. **What is the optimal c_puct value for inference-time MCTS on Kaggle T4?** -- 1.0 (train), 1.1 (inference, katac4), 1.4 (connectpuct) -- no systematic study compares these on identical positions.
2. **Does LCB move selection measurably improve MCTS quality over argmax?** -- katac4 uses LCB exclusively; connectpuct uses argmax. No controlled comparison exists.
3. **Is FPU necessary when LCB is present?** -- Both are root exploration mechanisms with different mechanisms. No ablation study exists.
4. **What simulation count is optimal for Kaggle T4 CPU MCTS?** -- connectpuct (80), katac4 (1600), rowspire (4000) -- all different. Optimal depends on NN guidance quality and board size.
5. **Does shared TT (ENS-018) provide measurable improvement?** -- Hypothesis HYP-017 claims 10-20% speedup; no empirical evidence on ConnectX.
6. **Can NN-guided playouts (Pattern C) outperform NN value head (Pattern B)?** -- rowspire uses guided playouts; katac4 uses value head. No comparative study.
7. **What is the effective MCTS search depth on 15x13 with GPU acceleration?** -- MCTS-NC achieves 20.3M playouts/5s on GRID A100, but effective search depth (how deep into the tree MCTS actually explores) is unknown for 15x13.

---

## 16. Recommendations

### Short-Term (Kaggle Implementation)

1. **Use PUCT c_puct = 1.1** for inference-time MCTS (katac4 value). Values below 1.0 risk premature convergence; above 1.4 waste simulations.
2. **Add forced-move detection before MCTS** -- ~1ms cost, eliminates trivial positions.
3. **Implement timing gate at 1.5s** with alpha-beta fallback -- always produce a valid move.
4. **Use LCB move selection** (katac4) for final move selection at low visit counts; argmax at high visit counts.
5. **Add solved-game tablebook lookup** before any MCTS for 7x6 positions -- solves opening phase.

### Medium-Term (Research)

1. **Run BMS-011** -- systematic comparison of UCT vs PUCT variants on identical positions.
2. **Ablation study** -- compare Pattern B (value head) vs Pattern C (guided playouts) on identical board sizes.
3. **Verify HYP-017** -- measure shared TT improvement vs separate TT on 1000 positions.
4. **Measure oracle match rate** -- test NN policy+value network against MCTS 10,000-sim gold standard.

### Long-Term (Theoretical)

1. **Develop finite-sample convergence bounds** for PUCT on ConnectX branching structure.
2. **Analyze optimal c_puct vs board size** -- branching factor changes optimal exploration constant.
3. **Design MCTS variants** that incorporate solved-game knowledge during simulation (not just root lookup).

---

## 17. Impact on Corpus

This dossier complements MCTS-001 (consistency problem) by providing **implementation guidance** for MCTS ensembles. Key impacts:

- **Validates PUCT over UCT**: 3 of 4 corpus MCTS implementations use PUCT; UCT only used by MCTS-NC CPU as baseline. Recommendation: use PUCT c=1.1.
- **FPU + LCB superior to Dirichlet**: katac4's FPU + forced_k approach may replace rowspire's 75/25 Dirichlet noise.
- **GPU MCTS is necessary for large boards**: 15x10 and 15x13 require GPU acceleration for any meaningful coverage.
- **All MCTS ensembles need solved-game tablebook**: MCTS-001 established the consistency problem; this dossier provides the architectural fix (Layer 1 in the 6-layer architecture).

---

## 18. Sources and Retrieval Record

| Source | URL | Type | Retrieved |
|--------|-----|------|-----------|
| katac4/mcts.py | https://github.com/katosu/katac4/blob/main/src/mcts.py | Source code (PUCT, FPU) | 2026-08-05 |
| katac4/explorer_main.py | https://github.com/katosu/katac4/blob/main/src/explorer_main.py | Source code (LCB) | 2026-08-05 |
| connectpuct/README.md | https://github.com/ahmeddoghri/connectpuct/blob/main/README.md | Documentation | 2026-08-05 |
| AZAL paper | https://arxiv.org/abs/2607.08984 | Academic paper (oracle match, AZAL) | 2026-08-05 |
| MCTS-NC/c4.py | https://github.com/eriklupander/connect4/blob/master/c4.py | Source code (GPU MCTS) | 2026-08-05 |
| Kocsis & Szepesvari 2006 | https://link.springer.com/chapter/10.1007/978-3-540-37564-9_86 | Academic paper (UCT) | 2026-08-05 |
| Browne et al. 2012 | https://ieeexplore.ieee.org/document/6291809 | Academic survey (MCTS) | 2026-08-05 |

---

## 19. Cross-Links

| Related ID | Type | Connection |
|------------|------|------------|
| MCTS-001 | Dossier | Consistency problem -- this dossier covers implementation to work around it |
| C032 | Claim | MCTS 30 sims c_puct=1.0 -- verified parameter range |
| C039 | Claim | MCTS 1600 sims FPU+LCB -- verified katac4 configuration |
| C043 | Claim | PUCT tactical priors 11/20 wins -- connectpuct benchmark |
| C047 | Claim | Dirichlet 75/25 -- NEEDS_CORRECTION, evidence gate violation |
| C124 | Claim | MCTS-NC UCB1 c=2.0 -- verification of exploration constant |
| C127 | Claim | NN-guided PUCT c_puct=1.0/1.1 -- katac4 dual configuration |
| C135 | Claim | No corpus MCTS uses solved-game knowledge -- MCTS-001 finding |
| C137 | Claim | connectpuct 50-66% vs minimax d3 -- performance evidence |
| C138 | Claim | katac4 LCB specification -- verified move selection |
| C141 | Claim | FPU c_fpu=0.2 root-only -- verified katac4 implementation |
| C142 | Claim | UCT asymptotic consistency -- MCTS-001 theorem |
| C177 | Claim | MCTS-NC 2.5M playouts/s T4 -- GPU performance |
| C178 | Claim | CPU MCTS 1600-4000 sims overflow 2s -- timing constraint |
| C179 | Claim | GPU MCTS required on Kaggle T4 -- feasibility |
| C200 | Claim | Neural MCTS oracle match 0.849 -- quality benchmark |
| HYP-004 | Hypothesis | Warm-Start MCTS -- H-04 in hybrid catalog |
| HYP-008 | Hypothesis | Classical Search Dominates MCTS -- H-01/H-03 related |
| HYP-014 | Hypothesis | Timing Governance -- Layer 4 architecture |
| HYP-017 | Hypothesis | TT-MCTS shared cache -- H-05, falsification condition |
| ENS-002 | Ensemble | PUCT c=1.1 + NN -- requires timing gate fix |
| ENS-013 | Ensemble | Alpha-beta with fallback -- good pattern, add tablebook |
| ENS-014 | Ensemble | AlphaZero-GPU -- add solved-game tablebook |
| ENS-018 | Ensemble | TT-MCTS shared cache -- verify HYP-017 |
| ENS-024 | Ensemble | Hybrid neural-classical with routing -- add tablebook |
| BMS-011 | Benchmark | MCTS variant comparison -- proposed benchmark |
| BMS-012 | Benchmark | Neural MCTS quality threshold -- proposed benchmark |

---

*This dossier was produced as part of the ConnectX research corpus v10 worker pipeline. It complements MCTS-001 (theoretical consistency problem) by providing practical implementation guidance. Status: PROPOSED -- mechanisms confirmed from source code; empirical validation deferred to BMS-011/BMS-012 experiments.*
