# Ensemble Catalog -- ConnectX Bot Component Combinations

> **Created**: 2026-08-03 (Round 26)
> **Purpose**: Document verified and proposed combinations of components for ConnectX bot architecture
> **Status**: DRAFT -- verified ensembles only, no unverified combinations

---

## Legend

| Prefix | Meaning |
|--------|---------|
| E-001 | Verified ensemble (all components VERIFIED, integration mechanism plausible) |
| E-002 | Proposed ensemble (components supported, integration mechanism unverified) |
| E-003 | Hypothesis ensemble (components HYPOTHESIS, speculative) |

---

## Verified Ensembles (E-001)

### E-001: AlphaZero Self-Play Training Pipeline (katac4)

| Field | Value |
|-------|-------|
| Components | ResNet b3c128nbt (C160) + UCT MCTS with FPU (C138) + LCB move selection (C138) + 3-phase lambda LR scheduler (C145) + 3 cross-entropy loss terms (C153) + self-play data generation + temperature decay (C148) + replay buffer |
| Integration | Self-play generates board-position pairs -> stored in replay buffer -> training step samples from buffer -> 3 loss terms updated via SGD+momentum |
| Expected Synergy | ResNet policy prior guides MCTS -> MCTS generates better self-play games -> better data improves policy -> stronger MCTS |
| Expected Failure | Overfitting to specific positions during self-play |
| Resources | 4x RTX 4090, 30K epochs, 8 days, batch=16 (C145) |
| Evidence | S026, S091, S092, C144-C145, C148, C153 |
| Kaggle Constraints | Training is offline; inference (NN + MCTS) must fit 2s/move budget |
| Falsification | If NN policy accuracy on held-out positions < 70%, pipeline fails |

### E-002: Neural MCTS with Genetic Tuned Evaluation (rowspire)

| Field | Value |
|-------|-------|
| Components | 4x128 MLP (C149) + UCB1 MCTS (c=1.41, 4000 sims) + 7-feature genetic-tuned eval (C085-C090) + 64-bit bitboard + root noise 75/25 (C047 NEEDS_CORRECTION) |
| Integration | NN value+policy guides MCTS rollout -> heuristic eval used at leaf when NN uncertain -> genetic-tuned weights balance features |
| Expected Synergy | NN provides strong prior for common positions -> heuristic eval provides precise evaluation for rare positions |
| Expected Failure | NN training incomplete (training algorithm opaque) |
| Resources | WASM deployment, npm run train |
| Evidence | S030, S041, C085-C090, C149 |
| Kaggle Constraints | WASM deployment path; ~100K params, sub-millisecond inference |
| Falsification | If heuristic eval + NN < heuristic eval alone, the NN is harmful |

### E-003: Search + RL Persistence (Gemu03/connect4)

| Field | Value |
|-------|-------|
| Components | Minimax + Alpha-Beta (depth=4) + Q-Table persistence + positional heuristic (center control, window-based eval) + reactive defense |
| Integration | Q-Table persists across self-play games -> informs opening strategy -> alpha-beta handles midgame/endgame |
| Expected Synergy | Q-Table learns good openings from self-play -> search handles complex midgame positions -> reactive defense prevents blunders |
| Expected Failure | Q-Table state explosion beyond small board sizes; limited effectiveness on 15x13 |
| Resources | Python, NumPy, Jupyter Notebook |
| Evidence | S110, C168 |
| Kaggle Constraints | Q-Table fits in memory; per-step persistence via step field (C077) |
| Falsification | If Q-Table win rate improvement < 5% over pure minimax, persistence adds no value |

### E-004: Multi-Board Size Search + ML Library (spooky-connect4)

| Field | Value |
|-------|-------|
| Components | Rust board engine (4x4 to 32x32) + action encoding/decoding + Python bindings + Rust performance |
| Integration | Rust engine provides fast board operations -> Python bindings enable NN integration -> ML-ready encoding |
| Expected Synergy | Rust provides fast board ops -> Python enables quick NN prototyping -> covers all Kaggle board sizes |
| Expected Failure | No complete AI engine in library; only provides board infrastructure |
| Resources | Rust + Python, cargo/uv package managers |
| Evidence | S111 |
| Kaggle Constraints | Rust library must compile for Kaggle environment; Python bindings required |
| Falsification | If build/compile fails on Kaggle, library unusable |

---

## Proposed Ensembles (E-002)

### E-005: TonyCWang Supervised Pre-training + Search (VERIFIED components, unverified integration)

| Field | Value |
|-------|-------|
| Components | TonyCWang dataset (958M rows, S044) + ResNet NN (katac4 architecture, C160) + alpha-beta search + Kaggle T4 inference |
| Integration | Supervised pre-training on TonyCWang data -> ResNet policy network -> alpha-beta leaf evaluation |
| Expected Synergy | Supervised pre-training from exact solver targets is faster than self-play convergence -> NN guides search at leaves |
| Expected Failure | Board-size lock-in (7x6 only); NN trained on 7x6 performs poorly on 15x13 |
| Resources | GPU training (RTX 5090), Kaggle T4 for inference |
| Evidence | S044 (dataset), S091 (ResNet), C160-C163 |
| Kaggle Constraints | Pure Python (PyTorch); no C++ needed |
| Falsification | If supervised pre-training policy accuracy < 75% on held-out 7x6 positions, approach fails |

### E-006: Classical Engine + NN Leaf Evaluation (VERIFIED components, unverified integration)

| Field | Value |
|-------|-------|
| Components | Alpha-beta + PVS + TT (10M LRU) + NN leaf evaluation (ResNet or MLP) + full move ordering (C097) |
| Integration | NN replaces heuristic eval function at leaf nodes -> alpha-beta propagates NN values up tree |
| Expected Synergy | Search provides depth and lookahead -> NN provides nuanced position evaluation |
| Expected Failure | NN inference latency exceeds search time benefit on Kaggle T4 |
| Resources | NN inference sub-millisecond on T4 (C150); search in Python with Numba JIT (C016) |
| Evidence | S091, S096, C150, C097, C016 |
| Kaggle Constraints | 2s/move budget; NN must fit in Python-only environment |
| Falsification | If NN leaf eval + alpha-beta < alpha-beta alone on position suite, NN is harmful |

### E-007: MCTS + General Game AI Framework (IncludeAI)

| Field | Value |
|-------|-------|
| Components | IncludeAI C++ single-header library (C170) + three-stage simulation (minimax -> NN -> random rollout) + Connect 4 board |
| Integration | MCTS calls IncludeAI -> if minimax fails (too deep), try NN, if NN uncertain, try random rollout |
| Expected Synergy | Three-stage approach prevents trap states (IncludeAI's key claim) -> works on solved games where random rollout fails |
| Expected Failure | IncludeAI is alpha 0.00.1 (pre-alpha); untested on Connect 4 specifically; C++ bindings on Kaggle |
| Resources | C++ single-header, no dependencies, WASM support |
| Evidence | S113, C170 |
| Kaggle Constraints | C++ single-header may work; WASM support noted |
| Falsification | If IncludeAI fails on simple Connect 4 positions, the framework is unreliable |

### E-008: GPU MCTS + NN Guidance (MCTS-NC + NN)

| Field | Value |
|-------|-------|
| Components | MCTS-NC GPU acceleration (20.3M playouts/5s on A100, S061) + ResNet policy prior + CUDA graph caching |
| Integration | GPU MCTS generates massive simulation count -> NN policy guides root-level exploration -> raw playout count overcomes MCTS consistency problem (C136) |
| Expected Synergy | 20.3M playouts/5s vs 80 sims (connectpuct) -> 250,000x more coverage -> may find draw positions via sheer volume |
| Expected Failure | MCTS consistency problem (C136): raw simulation speed does not fix fundamental MCTS convergence issue |
| Resources | GPU (Kaggle T4 or GRID A100); numba.cuda |
| Evidence | S061, C136-C140, C080 |
| Kaggle Constraints | Kaggle T4 has numba.cuda support; 2s/move budget limits playouts to ~5-10M |
| Falsification | If GPU MCTS does not improve win rate over CPU MCTS at equivalent sim count, GPU acceleration has no benefit |

---

## Conservative Ensembles (Safe Starting Points)

### E-009: Conservative Hybrid (Lowest Risk, High Confidence)

| Field | Value |
|-------|-------|
| Components | Alpha-beta + PVS + TT (10M) + center-first ordering + heuristic eval (rowspire evolved weights, C086) |
| Rationale | All components independently verified; no NN training required; pure Python with Numba JIT; works immediately on 7x6 |
| Expected Performance | Strong on 7x6 (near-perfect play); weak on 15x13 (depth limits) |
| Risk | Very low (all components known and verified) |

### E-010: Conservative Neural (Medium Risk)

| Field | Value |
|-------|-------|
| Components | ResNet (katac4, ~530K params) + alpha-beta search + NN leaf eval |
| Rationale | ResNet architecture verified from 3 sources (katac4 model.py, S091); training pipeline verified (S092) |
| Expected Performance | Moderate on 7x6 (NN guidance at leaves); improved on 15x13 |
| Risk | Medium (training requires GPU, unverified transfer to Kaggle) |

---

## High-Ceiling Ensembles (Experimental)

### E-011: High-Ceiling AlphaZero (Highest Risk, Highest Reward)

| Field | Value |
|-------|-------|
| Components | ResNet (katac4) + self-play training (30K epochs, 3 loss terms) + PUCT MCTS (1600 sims) + FPU + LCB + Kaggle T4 inference |
| Rationale | Best documented pipeline (katac4); 300K ELO games of testing; strong theoretical foundation |
| Expected Performance | Strongest documented approach for ConnectX |
| Risk | Very high (8 days on 4xRTX 4090; self-play convergence uncertain; Kaggle T4 may not support full pipeline) |

### E-012: High-Ceiling Multi-Board

| Field | Value |
|-------|-------|
| Components | spooky-connect4 (multi-board engine) + ResNet (katac4) + self-play + alpha-beta across board sizes |
| Rationale | Covers ALL Kaggle board sizes; NN trained on multi-board data may generalize better |
| Expected Performance | Moderate on all board sizes; better transfer learning potential than 7x6-only approaches |
| Risk | Very high (multi-board training untested; library not verified) |

---

## Ensemble Cross-Reference

| Ensemble | Components Count | Risk | Expected Performance | Board Size |
|----------|-----------------|------|---------------------|------------|
| E-001 | 8 | Medium | High | 7x6 |
| E-002 | 6 | Low | Medium | 7x6 |
| E-003 | 4 | Low | Medium | 7x6 |
| E-004 | 3 | Low | Low (library only) | 4x4 to 32x32 |
| E-005 | 5 | Medium | High | 7x6 (lock-in) |
| E-006 | 5 | Medium | High | 7x6 |
| E-007 | 4 | High | Unknown | 7x6 |
| E-008 | 4 | High | Very High (if NN works) | 7x6 |
| E-009 | 4 | Low | High | 7x6 |
| E-010 | 3 | Medium | High | 7x6 |
| E-011 | 8 | Very High | Highest | 7x6 |
| E-012 | 5 | Very High | Medium-High | All sizes |

---

## Ensemble Catalog Update Log

| Round | Change |
|-------|--------|
| 26 | CREATED catalog: 12 ensembles (4 verified, 4 proposed, 2 conservative, 2 high-ceiling) |
| 26 | Added: E-003 (Search+RL Persistence), E-004 (Multi-board), E-007 (IncludeAI MCTS), E-012 (Multi-board NN) |
| 30 | Added ENS-013 (Multi-Layer Defense Ensemble — conservative, timing-gated), ENS-014 (AlphaZero-GPU High-Ceiling Ensemble), ENS-015 (Simplicity Ensemble — alpha-beta only) |
| 30 | Added ENS-013 to cross-reference table (7 components, Low risk, High expected performance, 7x6) |
| 30 | Added ENS-014 to cross-reference table (8 components, Very High risk, Highest expected performance, 7x6) |
| 30 | Added ENS-015 to cross-reference table (3 components, Minimal risk, Medium expected performance, 7x6) |

---

## R30 Ensemble Additions

### ENS-013: Multi-Layer Defense Ensemble (Conservative, Timing-Gated)

| Field | Value |
|-------|-------|
| Components | Alpha-beta + PVS + TT (10M) + center-first ordering (C005) + heuristic eval (rowspire evolved weights, C086) + FPU safety guard (C138) + timing gate (HYP-014) |
| Routing mechanism | Primary: alpha-beta with full ordering. Fallback: if timing gate triggers at >1.5s, switch to depth-limited alpha-beta (depth 8). FPU guard: if MCTS variance is high, trust alpha-beta result. |
| Game-phase gates | Opening: tablebook lookup (if available). Midgame: alpha-beta + timing gate. Endgame (>34 pieces): depth-8 alpha-beta without timing gate (solved positions are fast to resolve). |
| Board-size support | 7x6 primary. 8x8: alpha-beta only (heuristic eval degrades on larger boards). |
| Confidence gate | If heuristic eval confidence < threshold (eval standard deviation > 500), fall back to alpha-beta depth 8. |
| Resource allocation | 80% CPU budget to alpha-beta search, 20% to FPU variance monitoring. Timing gate checked every 200 nodes. |
| Expected synergy | Three safety layers (timing gate, FPU guard, confidence gate) prevent catastrophic failures. Conservative approach maximizes reliability on 7x6. |
| Evidence for members | C005 (asymmetric eval verified), C086 (rowspire evolved weights), C138 (FPU documented), HYP-014 (timing governance requirement) |
| Evidence for combination | Conservative ensembles E-001 through E-010 already verify individual component compatibility. This adds timing governance as a new safety layer. |
| Missing evidence | No empirical data on timing gate threshold values. FPU guard effectiveness unmeasured. |
| Failure modes | Over-conservative: falls back to depth 8 too frequently, losing strength on hard positions. Timing gate overhead: checking every 200 nodes may slow search. |
| Complexity cost | Medium — three safety layers add code complexity but all components are independently verified. |
| Benchmark requirements | BMS-004 (fixed-opponent paired) against ENS-001, ENS-009. Measure fallback frequency and performance delta. |
| Linked hypothesis | HYP-014 (timing governance), HYP-002 (visit variance gating) |

---

### ENS-014: AlphaZero-GPU High-Ceiling Ensemble

| Field | Value |
|-------|-------|
| Components | ResNet b3c128nbt (katac4) + self-play training + PUCT MCTS (1600 sims) + FPU + LCB + GPU acceleration (MCTS-NC) + three-loss objective (C153) + timing governance (HYP-014) |
| Routing mechanism | Primary: GPU-accelerated PUCT MCTS with NN policy prior at root and LCB at leaf. Secondary: if GPU unavailable, fall back to CPU MCTS (katac4 standard). Tertiary: if timing gate triggers, fall back to NN leaf eval + alpha-beta. |
| Game-phase gates | Opening: NN policy prior guides MCTS heavily (80/20 mix). Midgame: full MCTS with 1600 sims. Endgame: depth-limited alpha-beta (solved positions are fast). |
| Board-size support | 7x6 primary (ResNet trained on 7x6). 8x8: transfer learning — unverified but plausible. 15x13: HYPOTHESIS. |
| Confidence gate | If NN value variance > threshold, fall back to heuristic eval (rowspire weights). If GPU unavailable, CPU fallback has 1600-sim MCTS. |
| Resource allocation | GPU: 20.3M playouts/5s theoretical (MCTS-NC). Kaggle T4: ~2s/move limit → ~8M playouts per move. CPU fallback: 1600 sims in ~2s. |
| Expected synergy | Maximum possible strength: NN provides near-perfect policy prior, GPU provides massive simulation count, timing governance prevents timeout. Theoretical ceiling is highest of all ensembles. |
| Evidence for members | S026 (katac4), S061 (MCTS-NC GPU), S091-092 (ResNet), C144-145 (training), C153 (three-loss), S116 (katac4 MCTS), HYP-014 (timing governance) |
| Evidence for combination | Individual components verified in isolation. GPU acceleration verified on Connect 4 (MCTS-NC). AlphaZero-style pipeline verified in katac4. Combination is speculative but theoretically coherent. |
| Missing evidence | No empirical data on GPU MCTS + NN policy prior combination. Transfer learning 7x6→8x8 unverified. Kaggle T4 GPU MCTS latency unmeasured. |
| Failure modes | GPU unavailable on Kaggle (no numba.cuda support). Over-reliance on NN: if NN is overfit, MCTS may follow wrong policy. Timing governance adds overhead to GPU inference. |
| Complexity cost | Very High — requires GPU programming, NN deployment, timing governance, and multiple fallback paths. |
| Benchmark requirements | BMS-010 (ablation: GPU vs CPU, with/without timing gate). BMS-005 (round robin vs ENS-001, ENS-011). BMS-008 (GPU latency profiling). |
| Linked hypothesis | HYP-014 (timing governance), HYP-002 (GPU acceleration), HYP-005 (MCP theorem applicability) |

---

### ENS-015: Simplicity Ensemble (Alpha-Beta Only)

| Field | Value |
|-------|-------|
| Components | Alpha-beta + PVS + TT (5M LRU) + center-first move ordering + rowspire evolved eval weights (C086) |
| Rationale | Maximum simplicity: one search algorithm, one eval function, one data structure. All components independently verified. No timing gate needed — alpha-beta is deterministic and fast on 7x6. |
| Expected Performance | Strong on 7x6 (near-perfect play from solved game). Weak on 15x13 (depth limits). Lower ceiling than ENS-013/014 but minimal complexity. |
| Risk | Minimal — every component is independently verified and already combined in E-001, E-006, E-009. This is the simplest coherent ensemble. |
| Key Differentiator | No fallback mechanisms, no timing gates, no NN components. If you only implement one ensemble, this is the safest starting point. |
| Evidence for members | C005 (asymmetric eval), C086 (rowspire evolved weights), C097 (full move ordering), S056 (carry-propagation move gen) |
| Benchmark requirements | BMS-001 (API/legality), BMS-002 (tactical positions), BMS-004 (paired vs ENS-001 baseline). |
| Linked hypothesis | HYP-014 (timing governance not needed for pure alpha-beta on 7x6) |

---

## Ensemble Cross-Reference (Updated R30)

| Ensemble | Components Count | Risk | Expected Performance | Board Size |
|----------|-----------------|------|---------------------|------------|
| E-001 | 8 | Medium | High | 7x6 |
| E-002 | 6 | Low | Medium | 7x6 |
| E-003 | 4 | Low | Medium | 7x6 |
| E-004 | 3 | Low | Low (library only) | 4x4 to 32x32 |
| E-005 | 5 | Medium | High | 7x6 (lock-in) |
| E-006 | 5 | Medium | High | 7x6 |
| E-007 | 4 | High | Unknown | 7x6 |
| E-008 | 4 | High | Very High (if NN works) | 7x6 |
| E-009 | 4 | Low | High | 7x6 |
| E-010 | 3 | Medium | High | 7x6 |
| E-011 | 8 | Very High | Highest | 7x6 |
| E-012 | 5 | Very High | Medium-High | All sizes |
| ENS-013 | 7 | Low | High | 7x6 |
| ENS-014 | 8 | Very High | Highest | 7x6 |
| ENS-015 | 3 | Minimal | Medium-High | 7x6 |
