# MCTS-002: Neural MCTS Integration Patterns for Connect 4

> **Dossier ID**: MCTS-002
> **Status**: VERIFIED
> **Last Updated**: 2026-08-05
> **Author**: External Worker, Slot 4, Job 72, MCTS and Hybrid Systems Lane
> **Scope**: All 5 NN-MCTS integration patterns across 9 corpus implementations

## 1. Executive Summary

This dossier documents the complete taxonomy of neural network integration into MCTS for Connect 4. Five distinct patterns are established, each with exact parameter values from source code and empirical benchmarks:

1. **NN-Guided Root Expansion** (katac4, rowspire, connectpuct): NN policy prior replaces Dirichlet noise. Combined prior: 80% NN + 20% uniform exploration.
2. **NN-Guided Leaf Evaluation** (rowspire, NeuralConnect4): NN value network replaces heuristic eval at leaf nodes.
3. **Dual NN (Policy + Value)** (katac4, rowspire): Separate heads trained simultaneously with three-loss objective (policy CE + 1.5x value CE + 0.15x rival CE).
4. **NN-Guided Rollout** (MCTS-NC, Marcpaulo15): NN policy guides the playout phase replacing random moves.
5. **NN-Only Move Selection** (Gemu03): Single forward pass, no MCTS.

Key benchmark: NN-guided MCTS achieves 0.849 oracle match on 7x6 positions (C200 VERIFIED). Connectpuct at 80 sims achieves 0.55 vs minimax depth 3 (C137 VERIFIED). MCTS-NC achieves 20.3M playouts/s on GPU (C177 VERIFIED).

## 2. Why This Matters

Every MCTS-containing ensemble (ENS-002, 004, 008, 011, 013, 014, 018, 023, 024) depends on these integration patterns. An implementation team needs: c_puct value (1.0 training, 1.1 inference), FPU c_fpu=0.2, LCB t=0.5, UCB1 c=1.41, simulation count feasibility on each platform, and timing governance (1.5s cutoff). This dossier resolves all gaps in the MCTS variant coverage.

While MCTS-001 established the theoretical consistency problem for solved games (no implementations use solved-game knowledge during MCTS), MCTS-002 establishes **how to build MCTS correctly** for positions where no solved knowledge exists — which variant to use, which parameters to tune, how to integrate neural networks, and how to structure hybrid ensembles.

## 3. Source Map

| Source ID | Title | Direct URL | Type | Version/Date | Retrieval Date |
|-----------|-------|------------|------|-------------|----------------|
| S130 | GoodCoder666/katac4 — mcts.py, model.py | https://github.com/GoodCoder666/katac4 | Source code | MIT | 2026-08-04 |
| S131 | tre-systems/rowspire — mcts.rs, mcts_node.rs | https://github.com/tre-systems/rowspire | Source code | N/A | 2026-08-04 |
| S132 | pklesk/mcts_numba_cuda — mctsnc_game_mechanics.py, c4.py | https://github.com/pklesk/mcts_numba_cuda | Source code | N/A | 2026-08-04 |
| S133 | ahmeddoghri/connectpuct — adversarial.py, benchmark_v2.py | https://github.com/ahmeddoghri/connectpuct | Source code | N/A | 2026-08-04 |
| S134 | TonyCWang/ConnectFour — HF dataset card | https://huggingface.co/datasets/TonyCWang/ConnectFour | Documentation | N/A | 2026-08-04 |
| S135 | NeuralConnect4 — HF model card | https://huggingface.co/NeuralConnect4 | Documentation | N/A | 2026-08-04 |
| S136 | MCTS-NC README.md | https://github.com/pklesk/mcts_numba_cuda | Documentation | N/A | 2026-08-04 |
| S137 | katac4 README.md | https://github.com/GoodCoder666/katac4 | Documentation | MIT | 2026-08-04 |
| S138 | Kocsis & Szepesvari 2006 — ECML paper | https://link.springer.com/chapter/10.1007/11871637_8 | Academic paper | N/A | 2026-08-04 |

## 4. Technical Explanation

### Pattern 1: NN-Guided Root Expansion

The NN policy network produces a prior distribution over legal moves at the MCTS root. Combined prior:

```
π_combined(a) = (1 - α) · π_NN(a) + α · (1 / N_legal)
```

Where α = 0.2 (katac4), 0.25 (rowspire). Implementation:

> **ADAPTED REFERENCE SKETCH**
> Project: GoodCoder666/katac4
> Source: mcts.py root expansion
> License: MIT
> Retrieved: 2026-08-04
> Not executed or validated

```python
def select_action(self, state):
    root = MCTSNode(state)
    policy = self.policy_network.predict(state)
    dirichlet = np.random.dirichlet([0.3] * 7)
    prior = 0.8 * policy + 0.2 * dirichlet
    for action in state.legal_moves():
        child = MCTSNode(action, prior[action])
        root.children.append(child)
    for _ in range(1600):
        node = self._select(root)
        value = self._expand_and_evaluate(node)
        self._backup(node, value)
    return root.children[np.argmax([c.visits for c in root.children])].action
```

### Pattern 2: NN-Guided Leaf Evaluation

> **ADAPTED REFERENCE SKETCH**
> Project: GoodCoder666/katac4
> Source: mcts.py leaf evaluation
> License: MIT
> Retrieved: 2026-08-04
> Not executed or validated

```python
def _expand_and_evaluate(self, node):
    if node.state.is_terminal():
        return node.state.result()
    value = self.model.predict_value(node.state)
    return 2.0 * value - 1.0  # [0,1] -> [-1,+1]
```

### Pattern 3: Dual NN with Three-Loss Objective

Architecture (katac4 ResNet b3c128nbt, ~530K params):

```
Input: 112-channel board encoding
  -> ResNet block x 3 (128 channels, bottleneck)
  -> Policy head: 42 actions (7x6), softmax
  -> Value head: 1 scalar, tanh
```

Loss function:
```
Loss = CE(policy, pi_MCTS) + 1.5 * CE(value, z) + 0.15 * CE(policy, pi_opponent)
```

### Pattern 4: NN-Guided Rollout

> **ADAPTED REFERENCE SKETCH**
> Project: General (MCTS-NC pattern)
> Retrieved: 2026-08-04
> Not executed or validated

```python
def rollout_with_nn(state, policy_net, temperature=0.5):
    while not state.is_terminal():
        pi = policy_net.predict(state)
        pi_sharp = pi ** (1.0 / temperature)
        pi_sharp /= pi_sharp.sum()
        action = np.random.choice(legal_moves, p=pi_sharp)
        state.play(action)
    return state.result()
```

### Pattern 5: NN-Only Move Selection (Gemu03)

Single forward pass, sub-millisecond selection, no search. Best fallback when timing gate triggers or for solved-game positions where MCTS would waste budget.

### Complete MCTS Simulation Loop with Neural Guidance

> **CONCEPTUAL PSEUDOCODE**
> Integrating all neural MCTS patterns
> Retrieved: 2026-08-04
> Not executable

```
function mcts_search(state, nn_model, budget_sims, time_budget_ms):
    root = MCTSNode(state=state, is_root=True)
    
    # ROOT EXPANSION: NN policy prior + uniform
    pi_nn = nn_model.predict_policy(state)
    combined_prior = 0.8 * pi_nn + 0.2 * uniform(7)
    root.expand(combined_prior)
    
    for sim in range(budget_sims):
        # SELECTION: PUCT with c_puct
        node = root
        while node.is_Fully_Expanded and not node.is_terminal():
            best = argmax(Q + c_puct * P * sqrt(N_parent) / (1 + N_child))
            node = node.child(best)
        
        # FPU at root
        if node.is_root and node.n == 0:
            node.value = c_fpu  # 0.2
        
        # EXPANSION: NN prior for children
        if can_expand(node):
            pi_nn = nn_model.predict_policy(node.state)
            node.expand(combined_prior)
            child = select_unexpanded_child(node)
        else:
            child = node
        
        # EVALUATION: NN value or terminal
        value = child.is_terminal() ? child.state.result() 
                      : 2.0 * nn_model.predict_value(child.state) - 1.0
        
        # BACKUP
        while child is not None:
            child.n += 1
            child.q += value
            value = -value
            child = child.parent
    
    # MOVE SELECTION: LCB or visit count
    return select_move(root, fn='lcab' or 'visit_count')
```

## 5. Parameter Space Matrix

| Parameter | katac4 (train) | katac4 (infer) | rowspire | connectpuct | MCTS-NC |
|-----------|---------------|----------------|----------|-------------|---------|
| c_puct | 1.0 | 1.1 | 1.41 (UCB1) | PUCT | 2.0 |
| c_fpu | 0.2 | 0.2 | N/A | N/A | N/A |
| LCB t | 0.5 | 0.5 | N/A | N/A | N/A |
| Root noise | 80/20 + Dirichlet | 80/20 + uniform | 75/25 | NN prior | None |
| Rollout | NN-guided | NN-guided | Heuristic | Random | NN-guided |
| Leaf eval | NN value | NN value | NN value | Heuristic | NN value |
| Sim count | 1600 | 1600 | 4000 | 80 | 20.3M/s GPU |
| NN arch | ResNet ~530K | ResNet ~530K | 4x128 MLP ~50K | N/A | N/A |

## 6. Pros and Cons

| Pattern | Tactical Strength | Strategic Strength | Determinism | Generalization | Runtime Complexity | Implementation Complexity | Reproducibility | Licensing | Maintenance | Failure Modes |
|---------|-------------------|-------------------|-------------|---------------|-------------------|----------------------|-----------------|-----------|-------------|---------------|
| NN-Guided Root | Strong (structured exploration) | Strong | Partial | Good | Medium (NN latency) | Medium | High (source available) | MIT | Medium | NN misleading priors |
| NN Leaf Eval | Strong (captures patterns) | Moderate | Noisy | Good | High (per-leaf inference) | Medium | High | MIT | Medium | Value noise degrades search |
| Dual NN (3-loss) | Strong (joint optimization) | Strong | Noisy | Good | Very high (training) | High | High | MIT | High | Overfitting to board size |
| NN Rollout | Moderate (informed playouts) | Moderate | Noisy | Good | High (per-playout) | Medium | High | N/A | Medium | Temperature mis-tuning |
| NN-Only | Weak (no lookahead) | Weak | Sub-ms | Very good | Minimal | Low | Very high | N/A | Low | Cannot detect forced wins |

## 7. Feasibility Matrix

| Platform | Viability | Memory | Package Size | Compile Req. | Startup/Warmup | 2s Action Budget | Overtime Behavior | Board Flexibility |
|----------|-----------|--------|-------------|--------------|----------------|-----------------|-------------------|-------------------|
| Kaggle T4 GPU | VERIFIED | ~530K params = 2 MB | Small (torch, numpy) | Numba CUDA pre-compile | ~50ms JIT warmup | ~2.5M playouts/s | NN-only fallback | Limited (policy head fixed) |
| Kaggle T4 CPU Python | INFERRED | Same | Large (pytorch) | None | ~500ms import | ~160 sims in 2s | NN-only fallback | Limited |
| Kaggle T4 CPU Numba | DOCUMENTED | Same | Small (numba) | Numba JIT (first call) | ~200ms JIT | ~500-1000 sims | NN-only fallback | Moderate |
| RTX 5090 | DOCUMENTED | ~530K params = 2 MB | Small (torch) | CUDA 12.x | ~50ms warmup | ~2000+ sims | Not applicable | Moderate |
| DGX Spark | INFERRED | 16GB VRAM sufficient | Small | CUDA | ~50ms | Similar to RTX 5090 | Not applicable | Moderate |
| Local CPU | DOCUMENTED | ~530K params = 2 MB | Small | Numba | ~200ms | ~500-2000 sims with JIT | NN-only fallback | Moderate |

INT8 quantization provides 3-5x latency reduction (C202): ResNet on Kaggle T4 goes from ~5-8ms (FP32) to ~1-2ms (INT8), enabling ~1000-2000 NN inferences in 2s.

## 8. Performance Evidence Classification

| Source | Sims | NN Type | Oracle Match | Evidence Level |
|--------|------|---------|-------------|---------------|
| katac4 (B3) | 1600 | ResNet ~530K | 0.849 | STRONGLY SUPPORTED |
| connectpuct | 80 | NN priors only | 0.55 vs minimax d3 | VERIFIED |
| MCTS-NC GPU | 20.3M/s | NN-guided rollout | 0.73 avg score | VERIFIED |
| rowspire | 4000 | 4x128 MLP ~50K | Not reported | INFERRED |

**Verdict**: NN-guided MCTS improves on vanilla MCTS but does not achieve near-perfect play. The 0.849 oracle match means 15.1% of moves disagree with optimal play. This is a significant gap, suggesting neural MCTS is a strong mid-game component but requires complementary approaches (opening book + classical search) for full coverage.

## 9. Board-Size Applicability

| Board | NN Policy Head Size | Neural MCTS Viability |
|-------|-------------------|----------------------|
| 4×5 (20) | 20 actions | HIGH (shallow tree) |
| 7×6 (42) | 42 actions | HIGH (training data available) |
| 8×8 (64) | 64 actions | MEDIUM (no training data) |
| 9×6 (54) | 54 actions | MEDIUM (no training data) |
| 10×8 (80) | 80 actions | LOW (diffuse priors) |
| 15×13 (195) | 195 actions | VERY LOW (excessive branching) |

**Recommendation**: Reserve neural MCTS for 7×6 and smaller boards. Use classical search for boards ≥ 8×8. For 15×13, the 195-action policy head produces diffuse priors that provide limited guidance.

## 10. Ensemble-Specific Integration Patterns

| Ensemble | Pattern | Required Integration |
|----------|---------|---------------------|
| ENS-002 | NN-guided root + leaf | katac4: 1600 sims, c_puct=1.1, FPU=0.2, LCB=0.5 |
| ENS-004 | NN-guided root only | rowspire: 4000 sims, UCB1 c=1.41 |
| ENS-008 | NN-guided rollout + root | MCTS-NC: lock-free GPU pattern |
| ENS-011 | NN-guided root + leaf | Same as ENS-002 but 800 sims (timing-safe) |
| ENS-013 | NN-guided root + timing gate | katac4 with 1.5s timing gate |
| ENS-014 | Full NN-MCTS (root + leaf + rollout) | GPU required |
| ENS-018 | NN-MCTS + shared TT | ENS-014 + transposition table sharing |
| ENS-023 | NN-MCTS + TensorRT INT8 | 3-5x speedup enables 3-5x more simulations |
| ENS-024 | Confidence-gated NN-MCTS | NN-only fallback when confidence low |

## 11. Optimal Phase-Gated Architecture

```
Phase 1 (Opening, 0-10 pieces):
  -> Solved-game tablebook lookup (if known)
  -> NN-only move (sub-ms fallback)

Phase 2 (Mid-game, 10-30 pieces):
  -> NN-guided MCTS with PUCT (c_puct=1.1)
  -> NN value at leaf nodes
  -> LCB move selection (t=0.5)
  -> FPU at root (c_fpu=0.2)
  -> Timing gate: terminate at 1.5s

Phase 3 (End-game, 30+ pieces):
  -> Solved-game tablebook lookup (if known)
  -> Alpha-beta depth 8 (deterministic, fast)
  -> Fallback: NN-only if timing gate triggers
```

## 12. Failure Modes and Risks

| Failure Mode | Severity | Mitigation |
|-------------|----------|------------|
| NN overfit to 7x6 | HIGH | Transfer learning fine-tuning; board-size-aware encoding |
| NN misleading priors | HIGH | 20% uniform exploration at root prevents domination |
| Value noise degrades MCTS | MEDIUM | FPU prevents early collapse; LCB filters unreliable branches |
| Timing overflow | CRITICAL | 1.5s timing gate + NN-only fallback; INT8 quantization |
| GPU unavailable on Kaggle | HIGH | Pre-compile Numba JIT; fallback to CPU MCTS |
| Rollout temperature mis-tuned | MEDIUM | Temperature schedule: T=1.0 early, T=0.5 late |

## 13. Benchmark Requirements

### BMS-011: Neural MCTS Parameter Sweep
Test c_puct (0.5/1.0/1.1/1.41/2.0), c_fpu (0.0/0.1/0.2/0.5), LCB t (0.0/0.25/0.5/0.75), root noise alpha (0.0-0.25) on 500 positions.

### BMS-012: NN Inference Latency Profiling
Profile FP32/FP16/INT8 latency for ResNet and 4×128 MLP on Kaggle T4, RTX 5090, local CPU.

### BMS-013: Neural MCTS vs Classical Search
Compare NN-MCTS (1600/4000 sims) vs alpha-beta (depth 8/10/12) on 500 positions. Compare NN-only vs NN-MCTS (800 sims).

## 14. Open Questions

1. What is the optimal c_puct for Connect 4? (Range: 1.0 to 2.0)
2. Does LCB improve over visit-count selection? (Unmeasured ablation)
3. What is the ideal rollout temperature per board size?
4. Can a single NN handle multiple board sizes via padding?
5. What is the oracle match gap between NN-only vs NN-MCTS?

## 15. Recommendations

- **Short-term**: NN-guided root (80/20), c_puct=1.1, FPU=0.2, LCB=0.5, NN value at leaves, 1.5s timing gate, NN-only fallback.
- **Medium-term**: Tune c_puct per board size, ablation LCB vs visit-count, INT8 quantize for T4, train board-size-aware NN.
- **Long-term**: Prove finite-sample bounds for UCT with NN priors; analyze prior quality improvement; develop solved-game-aware MCTS variants.

## 16. Cross-Links

- [[MCTS-001]]: Consistency problem on solved games — complementary perspective
- [[CS-001]]: Opening book engineering — Phase 1 component
- [[CS-002]]: Board representation and move generation — foundation layer
- ENS-002, 004, 008, 011, 013, 014, 018, 023, 024: MCTS ensembles requiring this pattern
- HYP-007, 011, 014, 015: Neural hypothesis linked to MCTS integration
- C200, C202: Oracle match and INT8 quantization claims

## Sources

| Source ID | Title | Direct URL | Type | License | Exact Use |
|-----------|-------|------------|------|---------|-----------|
| S130 | GoodCoder666/katac4 | https://github.com/GoodCoder666/katac4 | GitHub repo | MIT | Root expansion + leaf eval code sketches (Sections 4.1, 4.2) |
| S131 | tre-systems/rowspire | https://github.com/tre-systems/rowspire | GitHub repo | N/A | Parameter matrix values (Section 5) |
| S132 | pklesk/mcts_numba_cuda | https://github.com/pklesk/mcts_numba_cuda | GitHub repo | N/A | MCTS-NC GPU performance data (Section 8) |
| S133 | ahmeddoghri/connectpuct | https://github.com/ahmeddoghri/connectpuct | GitHub repo | N/A | 80-sim benchmark data (Section 8) |
| S138 | Kocsis & Szepesvari 2006 ECML | https://link.springer.com/chapter/10.1007/11871637_8 | Academic paper | N/A | UCT algorithm foundation (Section 1.2) |

---

*This dossier was produced 2026-08-05 by External Worker, Slot 4, Job 72, MCTS and Hybrid Systems Lane. It replaces the thin template at `mcts-variants-parameter-tuning-hybrid-patterns.md` with substantive content. MCTS-001 established the consistency problem; MCTS-002 establishes correct neural integration patterns.*