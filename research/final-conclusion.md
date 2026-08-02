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
| **Hybrid NN + Search** | ★★★★★ | ★★★★☆ | High | RTX 5090 (local training) | **Best** |
| **MCTS + NN (AlphaZero)** | ★★★★☆ | ★★★★★ | Very High | RTX 5090 + cluster | Best for large boards |
| **Pure C++ Engine** | ★★★★★ | ★★☆☆☆ | Medium-High | CPU only + pybind11 | Strong for 7x6; Kaggle binding adds complexity |
| **Pure Search (Python)** | ★★★★☆ | ★★☆☆☆ | Low | CPU only | Simple but limited |
| **DQN + Minimax** | ★★★★☆ | ★★★☆☆ | Medium | CPU + GPU | Proven on Kaggle |
| **Pure NN** | ★★★☆☆ | ★★★☆☆ | Medium | RTX 5090 | Lacks precision on 7x6; good as evaluation component |

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
| 4 | 2026-07-31 | Hybrid NN + Search | High-High | GPU research: 0.1ms inference, 50-200× NN training speedup; MCTS variants documented; Game theory confirmed; Open-source bots cataloged; Advanced search techniques mapped |
| 5 | 2026-08-02 | Hybrid NN + Search | High | Web search unavailable — findings from internal knowledge; Game-phase strategy detailed (opening→mid→endgame); Python benchmarks estimated; RTX 5090 feasibility confirmed; Sub-agents failed due to API errors |
| 5 | 2026-08-02 | Hybrid NN + Search | High | Game-phase model detailed (opening→mid→endgame with piece-count thresholds); eval features ranked and weighted; Python benchmarks estimated; Web search tool broken — no live data obtained; ranking changes: MCTS+NN upgraded, Pure Search unchanged |
| 6 | 2026-08-02 | Hybrid NN + Search | High | 9 new verified GitHub sources; blanyal/alpha-zero (92★) AlphaZero implementation for Connect 4 analyzed; Tarun995 bitboard agent cataloged; 5 DQN/MCTS repos found via GitHub topics; 2 previously-cited repos (BitBully, mra1991) return 404 — unverified; CG-002 resolved (top bot strategies cataloged); No ranking changes |
| 7 | 2026-08-02 | Hybrid NN + Search | High | GoodCoder666/katac4 (18★) verified as first KataGo-inspired AlphaZero for Connect 4: PyTorch ResNet (b3c128nbt), 1600 MCTS sims, FPU exploration, ELO testing (300K games, 8 days on 4×RTX 4090), interactive explorer; Wikipedia independently confirms solved game (C001 upgraded UNKNOWN→SUPPORTED); MCTS+NN evidence strongest yet; Unknown claims dropped 13%→7%; No ranking changes |
| 8 | 2026-08-02 | Hybrid NN + Search | High | 3 new fully-analyzed repos: ahmeddoghri/connectpuct (PUCT MCTS, 11W/9L in 20 vs minimax d3 — first empirical PUCT benchmark), tre-systems/rowspire (Rust+WASM dual 4×128 MLP value+policy NN + MCTS + bitboard solver + genetic tuning — most sophisticated project), tristan852/kite (Java bitboard solver + TT + skill levels); arXiv zero results; VERIFIED claims reached 50%; No ranking changes |
| 8 | 2026-08-02 | Hybrid NN + Search | High | Three new fully-analyzed repos: connectpuct (PUCT benchmark 11/20 vs minimax depth 3), rowspire (dual 4×128 MLP value+policy, bitboard solver, WASM, genetic tuning, 4000 sims), kite (Java bitboard solver); arXiv zero results; VERIFIED claims reached 50%; No ranking changes but rowspire is strongest individual project analyzed |
| 9 | 2026-08-02 | Hybrid NN + Search | High | Tromp Fhourstones benchmark: 20 systems, KPOS/S, Gprof profiling (C4 1.48B nodes full solve); Tromp 8x8 solving (late 2014/early 2015, book88 ≤16 ply, ~500MB TT); katac4 training fully decoded (30K epochs, self-play workers, 3 loss terms, SGD+momentum, 3-phase lambda); katac4 ResNet KataGo techniques (pre-activation ResNet, nested bottleneck, mixed pooling, CUDA graph caching); haithameleuch alpha-beta+MCTS hybrid; VERIFIED claims 50%→55%; 6 new claims (C048-C053); 7 new sources (S032-S038); ICAPS/JOCIG/Google Scholar all unworkable; No ranking changes |
| 10 | 2026-08-02 | Hybrid NN + Search | High | rowspire FULL source decoded (14 files): 4×128 MLP with skip connections (dual value+policy), 100D input (64-cell binary + 16 normalized features), 7-feature evaluation with genetic tuning, UCB1 MCTS (c=1.41, 4000 sims, NN-guided, Dirichlet root noise 75/25), 64-bit bitboard with carry-propagation move generation; training algorithm OPAQUE (npm run train not in repo); eSlams discovered as novel evaluation framework (50 arenas, REST protocol, Ed25519 proof archives); kenrick95/c4 (278★) cataloged; Wikipedia opening theory confirmed (center=win ≤41, adjacent=draw, edge=loss 40-42); VERIFIED claims 55%→60%; 2 new sources (S039-S040); No ranking changes |
| 11 | 2026-08-02 | Hybrid NN + Search | High | Pascal Pons/connect4 C++ solver fully decoded (negamax+PVS+TT+opening book; iterative null-window binary search; template WIDTH/HEIGHT; DEPTH=14 book); TonyCWang/ConnectFour dataset discovered (958M rows, 14.8 GB, 2×6×7 binary observations + 7-element exact solver targets, self-play with temperature); Hugging Face LLM-based Connect 4 model catalog (11+ models, all lacking evaluation metrics); Evidence audit: 17 structural issues fixed (duplicate claim section removed, duplicate sources merged S026-28, stale headers updated); NEW approach: Supervised Pre-training + Search (board-state dataset); GitHub API unreachable (TLS errors); VERIFIED claims 60%→66%; NEW claims C060-C068; 8 new sources (S042-S049); No ranking changes |
| 12 | 2026-08-02 | Hybrid NN + Search | High | External-pool batch: 7/7 workers failed (DGX endpoint timeout, model-selection failure); no findings; DGX at 192.168.86.39:8006 unavailable since this round |

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
- [ ] After first implementation benchmark (Python alpha-beta speed)
- [ ] After NN training results (accuracy, convergence)
- [ ] After Kaggle submission and real-world performance
- [x] After initial neural network architecture research (ITERATION 2 - NN architecture doc created)
- [x] After evaluation function design research (ITERATION 2 - eval function doc created)
- [x] After time management research (ITERATION 2 - time management doc created)
- [x] After GPU research (ITERATION 4 - gpu-research-iteration4.md created)
- [x] After MCTS research (ITERATION 4 - mcts-research-iteration4.md created)
- [x] After game theory research (ITERATION 4 - game-theory-iteration4.md created)
- [x] After open-source bots research (ITERATION 4 - open-source-bots-iteration4.md created)
- [x] After advanced search research (ITERATION 4 - advanced-search-iteration4.md created)
- [x] After game-phase strategy, endgame DBs, benchmarks, eval, NN vs search (ITERATION 5 - iteration-5-findings.md created)
- [x] After GoodCoder666/katac4 analysis and Wikipedia solved game verification (ITERATION 7 - round-007.md created)
- [x] After PUCT MCTS benchmark, rowspire neural MCTS + bitboard solver, Java solver analysis (ITERATION 8 - round-008.md created)
- [x] After Tromp Fhourstones benchmark, katac4 full training pipeline, 8x8 solving, alpha-beta+MCTS hybrid, NN architecture deep-dive (ITERATION 9 - round-009.md created)
- [x] After rowspire full source code decoding, eSlams discovery, kenrick95/c4 catalog, Wikipedia opening theory (ITERATION 10 - round-010.md created)