# Final Conclusion Tracker — ConnectX Bot

> **Generated**: 2026-07-30 (Iteration 1)
> **Purpose**: Track the evolving final conclusion about what to build
> **Update Frequency**: After each research iteration

---

## Current Final Conclusion (Iteration 1)

### Recommended Architecture: **Hybrid Neural + Classical Engine**

After one iteration of deep research, the analysis points to a **hybrid architecture** that combines:

1. **Neural Network** (trained on RTX 5090) for position evaluation
2. **C++ Search Engine** (MTD(f) or PVS) for precise lookahead
3. **Opening Book** (from solved game database) for 7x6 opening moves
4. **MCTS with NN** for larger board sizes (15x13, 15x10)
5. **Endgame Database** for terminal positions

### Rationale

| Factor | Evidence |
|--------|----------|
| **7x6 is solved** | Böck (2025) provides complete solution → opening book = guaranteed optimal |
| **15x13 is unsolved** | No perfect solution available → MCTS + NN required |
| **RTX 5090 available** | 21,760 CUDA cores, 419 TFLOPS FP8 → NN training is fast |
| **2 seconds per move** | Plenty of time for alpha-beta at depth 8-12 on 7x6 |
| **Multiple board sizes** | Need unified approach that works on all boards |
| **Kaggle evaluation** | Tests against many opponent strategies → need versatility |

### Implementation Phases

#### Phase 1: Classical Engine (Week 1-2)
- Python alpha-beta with TT, move ordering, PVS
- Numba JIT for speedup
- Benchmark on all board sizes
- **Expected strength**: Strong for 7x6, weak for 15x13

#### Phase 2: C++ Search Core (Week 3-4)
- Port search to C++ with pybind11
- MTD(f) or PVS implementation
- Bitboard representation
- Opening book generation from solved positions
- **Expected strength**: Expert for 7x6, improved for larger boards

#### Phase 3: Neural Network (Week 5-8)
- Train CNN on solved 7x6 positions
- Policy net (move prediction)
- Value net (position evaluation)
- Transfer learning to larger boards
- **Expected strength**: Near-expert on 7x6, improving on larger boards

#### Phase 4: Hybrid Integration (Week 9-10)
- C++ search + NN evaluation at leaves
- GPU inference for NN
- Opening book for 7x6, NN for larger boards
- MCTS with NN for 15x13
- **Expected strength**: World-class on 7x6, strong on larger boards

#### Phase 5: Optimization (Week 11-12)
- TensorRT for inference
- GPU parallel evaluation
- Fine-tuning NN with self-play
- Benchmark and optimize
- **Expected strength**: The best possible ConnectX bot

---

## Approach Comparison Matrix

| Approach | 7x6 Strength | 15x13 Strength | Implementation Effort | Hardware Need | Overall |
|----------|-------------|----------------|----------------------|---------------|---------|
| **Hybrid NN + Search** | ★★★★★ | ★★★★☆ | High | RTX 5090 | **Best** |
| **Pure C++ Engine** | ★★★★★ | ★★☆☆☆ | Medium | CPU only | Strong for 7x6 |
| **MCTS + NN (AlphaZero)** | ★★★★☆ | ★★★★★ | Very High | RTX 5090 + cluster | Best for large boards |
| **Pure NN** | ★★★☆☆ | ★★★☆☆ | Medium | RTX 5090 | Good but not perfect |
| **Pure Search** | ★★★★☆ | ★★☆☆☆ | Low | CPU only | Simple but limited |
| **DQN + Minimax** | ★★★★☆ | ★★★☆☆ | Medium | CPU + GPU | Proven on Kaggle |

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Search algorithm** | MTD(f) / PVS | Most efficient for Connect 4 |
| **NN architecture** | CNN with FC heads | Proven in marcpaulo15, BEPb |
| **Training method** | SFT → RL (two-stage) | Most effective pipeline |
| **Hardware** | RTX 5090 for training, CPU for search | Best balance of speed and control |
| **Board size handling** | Unified NN + size-specific search | Generalizes across sizes |
| **Opening book** | From solved database (7x6), NN (others) | Optimal for 7x6, practical for others |
| **Language** | C++ for search, Python for orchestration | Best performance and flexibility |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| NN training fails to converge | Medium | High | Start with heuristic-based approach |
| C++ search is too slow | Low | Medium | Use Numba as intermediate step |
| Larger board performance poor | High | Medium | MCTS fallback for 15x13 |
| Time limit exceeded | Medium | High | Iterative deepening + time management |
| GPU availability issues | Low | Medium | Pure Python fallback with JIT |

---

## Comparison to Known Best

| Metric | BitBully (7x6) | Our Target | Gap |
|--------|----------------|------------|-----|
| Board support | 7x6 only | All sizes | Need to generalize |
| Search algorithm | MTD(f) + bitboards | MTD(f) + bitboards | Same |
| Performance | 197s/move (2012 hardware) | ~2s/move (target) | 100× faster (RTX 5090 + C++) |
| Play strength | Perfect | Near-perfect (7x6), strong (others) | 7x6: perfect, others: improving |
| Training | None (solved DB) | SFT → RL | Different approach |

---

## Evolution Log

| Iteration | Date | Leading Approach | Confidence | Key Evidence |
|-----------|------|-----------------|------------|--------------|
| 1 | 2026-07-30 | Hybrid NN + Search | Medium | 7x6 solved, 15x13 needs NN; RTX 5090 enables fast training |
| 2 | 2026-07-30 | Hybrid NN + Search | Medium-High | Confirmed SFT→RL pipeline, dillonloh depth-3 beats negamax 60%+; multiple new research docs |
| 3 | 2026-07-30 | Hybrid NN + Search | High | Axelredx 8-move lookahead Java AI targets L0/L1; ayeennp C implementation claims "(almost) perfect" 8-move; comprehensive Kaggle analysis; 10 strategies documented |

---

## Criteria for Updating This Document

This conclusion should be updated when:
1. New research reveals a better approach
2. Experiments show an approach is infeasible
3. Kaggle results show a clear winner
4. Hardware enables new possibilities
5. Time iteration (20-50 iterations) reveals a better strategy

## Next Update Triggers

- [x] After Kaggle competition analysis (ITERATION 2 - in progress)
- [ ] After GPU benchmarking (RTX 5090 actual performance)
- [ ] After MCTS research completion
- [ ] After first implementation benchmark (Python alpha-beta speed)
- [ ] After NN training results (accuracy, convergence)
- [ ] After Kaggle submission and real-world performance
- [x] After initial neural network architecture research (ITERATION 2 - NN architecture doc created)
- [x] After evaluation function design research (ITERATION 2 - eval function doc created)
- [x] After time management research (ITERATION 2 - time management doc created)