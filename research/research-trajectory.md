# Research Trajectory — ConnectX Bot

> **Last Updated**: 2026-07-30 (Iteration 1)
> **Current Status**: Active deep research loop (every 4 hours)
> **Goal**: Build the world's best Kaggle ConnectX bot through iterative research
> **Hardware**: RTX 5090 (21,760 CUDA cores, 32GB GDDR7, 419 TFLOPS FP8 tensor)

---

## Current Final Conclusion (Updated Each Iteration)

### Leading Approach: **Hybrid Neural + Classical Engine**

After Iteration 1 analysis:

| Rank | Approach | Confidence | Pros | Cons |
|------|----------|------------|------|------|
| 1 | **Hybrid NN + Search** | High | Combines NN speed with search precision; works on all board sizes | Complex to implement; requires both NN training and search engine |
| 2 | **GPU-Trained NN + MCTS** | Medium-High | RTX 5090 enables fast NN training; MCTS scales to large boards | MCTS convergence is slow; requires distributed training |
| 3 | **Classical Engine (MTD(f) + C++)** | Medium | Proven optimal play on 7x6 (BitBully); fast | Limited to 7x6; hard to generalize to larger boards |
| 4 | **Pure Neural Network** | Low-Medium | Fast inference; simple implementation | May not achieve perfect play; hard to guarantee correctness |
| 5 | **Pure Classical Search** | Low | Simple; no training needed; fast | Limited by search depth; doesn't scale to large boards |

### Why Hybrid is Best

1. **Neural network** provides fast position evaluation (0.1ms vs 100ms for search)
2. **Search** provides precise lookahead and guaranteed optimal play at shallow depth
3. **GPU (RTX 5090)** enables rapid NN training and fast inference
4. **C++ binding** for search core gives 100-500× speedup over Python
5. **Generalizes** across all board sizes

---

## What We Know (Well-Documented)

### Solved Game Knowledge
- 7x6 Connect 4 is SOLVED (first player wins in ≤41 moves from center)
- 4,531,985,219,092 possible positions
- Opening book exists for 7x6 (BitBully)
- Böck (2025) published complete win-draw-loss lookup table

### Search Algorithms
- MTD(f), negamax, alpha-beta, NegaScout/PVS are all documented
- BitBully (MTD(f) + bitboards) is the gold standard classical engine
- Symmetric negamax with transposition caching is a good Python implementation

### Neural Networks
- Two-stage training (SFT → RL) is the most effective approach
- marcpaulo15's CNN + SFT → RL pipeline is verified and working
- BEPb's AlphaZero-style MCTS with self-play is a strong approach
- Hybrid DQN + minimax (sidhantagar, VSZM) exists

### Kaggle Environment
- 7x6, 15x13, 15x10 board configurations supported
- 2 seconds per move (actTimeout)
- Jupyter notebook submission format
- Agent function signature: `agent(obs, config)`

### Hardware
- RTX 5090: 21,760 CUDA cores, 32GB GDDR7, 1,792 GB/s bandwidth
- 419 TFLOPS FP8 tensor throughput
- Excellent for NN training (50-200× vs CPU) and inference (0.1ms)

---

## What We DON'T Know (Research Targets)

### Priority 1: Kaggle Competition Reality (CRITICAL)
- ❌ Cannot access Kaggle leaderboard (login required / JS rendering)
- ❌ Cannot access Kaggle forum discussions
- ❌ Cannot read Kaggle notebooks (code)
- **Action needed**: Use Kaggle API, GitHub search, or manual Kaggle browsing to find current leaderboard data
- **Key question**: What actually wins on Kaggle RIGHT NOW?

### Priority 2: GPU-Specific ConnectX Research (HIGH)
- ❌ No research on GPU-parallel alpha-beta for ConnectX
- ❌ No benchmarks of CNN inference on RTX 5090 for ConnectX
- ❌ No TensorRT optimization data for ConnectX models
- ❌ No practical examples of GPU-accelerated Connect 4 search
- **Action needed**: Web research on GPU-based game AI, benchmarks
- **Key question**: What speedup is actually achievable?

### Priority 3: MCTS for ConnectX (HIGH)
- ❌ No MUCT formula variants tested for ConnectX
- ❌ No MCTS + NN integration patterns documented
- ❌ No benchmarks of MCTS vs alpha-beta on 15x13
- ❌ No exploration of UCT parameter tuning for ConnectX
- **Action needed**: Research MCTS for ConnectX, find implementations
- **Key question**: Can MCTS + NN beat alpha-beta on 15x13?

### Priority 4: Multi-Board Generalization (MEDIUM)
- ❌ No unified evaluation function across board sizes
- ❌ No research on transfer learning from solved to unsolved boards
- ❌ No data on how first-player advantage scales with board size
- **Action needed**: Web research on generalization in game AI
- **Key question**: Can a 7x6-trained NN play well on 15x13?

### Priority 5: Advanced Search Optimization (MEDIUM)
- ❌ No implementation benchmarks of MTD(f) vs alpha-beta in Python
- ❌ No data on killer heuristic effectiveness for ConnectX
- ❌ No investigation of quiescence search for ConnectX
- ❌ No investigation of ProbCut for ConnectX
- **Action needed**: Research optimization techniques, find implementations
- **Key question**: Which optimizations give the best speedup in Python?

### Priority 6: Opening Book Design (LOW)
- ❌ No data on optimal opening moves for 15x13 and 15x10
- ❌ No research on how to build a practical opening book
- ❌ No exploration of NN-based "opening book" (neural net policy for opening)
- **Action needed**: Research opening book design patterns
- **Key question**: What opening book size is optimal for ConnectX?

---

## Hypotheses List (For Future Research)

Each hypothesis should be tested in a future iteration:

| ID | Hypothesis | Confidence | Research Method | Status |
|----|-----------|------------|-----------------|--------|
| H1 | Small CNN (100K params) trained on solved 7x6 beats depth-6 minimax | Medium | Train & test | PENDING |
| H2 | RTX 5090 gives 50-200× NN training speedup vs CPU | High | Benchmark | PENDING |
| H3 | MCTS + NN beats alpha-beta on 15x13 | Medium | Implement & test | PENDING |
| H4 | Hybrid (NN opening + alpha-beta mid + tablebase end) beats pure approaches | Medium-High | Implement & test | PENDING |
| H5 | Numba gives 5-10× alpha-beta speedup in Python | High | Benchmark | PENDING |
| H6 | NN on 1M solved positions achieves >95% minimax agreement | Medium-High | Train & measure | PENDING |
| H7 | Single CNN generalizes across all board sizes | Low-Medium | Train multi-board & test | PENDING |
| H8 | MTD(f) gives 20-30% speedup over alpha-beta | Medium | Benchmark | PENDING |
| H9 | NN move ordering improves alpha-beta by 2-3× | Medium | Implement & benchmark | PENDING |
| H10 | GPU parallel evaluation gives 10-50× batched speedup | Medium | Implement & benchmark | PENDING |
| H11 | BitBully's techniques (MTD(f) + opening DB + bitboards) are key to its strength | High | Research | PENDING |
| H12 | Two-stage SFT→RL training beats pure RL | Medium | Compare approaches | PENDING |
| H13 | C++ binding (pybind11) for search gives 100-500× speedup | High | Benchmark | PENDING |
| H14 | First-player advantage diminishes on boards > 15x13 | Low | Research game theory | PENDING |

---

## Research Execution Plan

### Phase 1: Kaggle Competition Research (NEXT ITERATION)
1. Search for current Kaggle ConnectX leaderboard
2. Find top 10 solutions and their strategies
3. Read Kaggle forum posts about winning strategies
4. Find and study Kaggle notebooks with good ConnectX bots
5. Document board configurations and scoring methodology

### Phase 2: GPU Research
1. Research GPU-parallel Connect 4 search techniques
2. Find TensorRT benchmarks for small CNN inference
3. Research CUDA-based game search implementations
4. Benchmark neural net inference on RTX 5090 (if possible)
5. Document GPU optimization strategies

### Phase 3: MCTS Research
1. Research MCTS variants for Connect 4
2. Find UCT parameter tuning strategies
3. Study MCTS + NN integration patterns
4. Compare MCTS vs alpha-beta on large boards
5. Find open-source MCTS implementations for Connect 4

### Phase 4: Advanced Search Optimization
1. Benchmark MTD(f) vs alpha-beta in Python
2. Implement killer heuristic for ConnectX
3. Test quiescence search effectiveness
4. Investigate ProbCut for ConnectX
5. Document optimization impact on search speed

### Phase 5: Multi-Board Strategy
1. Research transfer learning from solved to unsolved boards
2. Design unified board representation for all sizes
3. Test neural net generalization across board sizes
4. Document strategy differences by board size
5. Create unified evaluation function

### Phase 6: Final Architecture Decision
1. Synthesize all research findings
2. Compare all approaches with pros/cons
3. Select final architecture based on evidence
4. Document implementation plan
5. Prepare for actual bot implementation phase

---

## Knowledge Gaps by Category

### Game Theory
- [ ] First-player advantage on 15x13: unknown
- [ ] Optimal opening for 15x13: unknown
- [ ] Thin position analysis: unknown
- [ ] Solved game database generation: unknown
- [ ] Relationship to Gomoku/Renju strategies: unknown

### Neural Networks
- [ ] Optimal CNN architecture for ConnectX: unknown
- [ ] Minimum params for expert-level play: unknown
- [ ] Transformer vs CNN for ConnectX: unknown
- [ ] Training data generation from solved positions: unknown
- [ ] Neural net evaluation vs heuristic evaluation: unknown

### Search Algorithms
- [ ] Best search for 15x13: unknown (alpha-beta or MCTS?)
- [ ] Optimal time management per move: unknown
- [ ] Python search speed with JIT: unknown
- [ ] C++ binding overhead: unknown
- [ ] Parallel search across CPU cores: unknown

### Hardware
- [ ] TensorRT inference speed for ConnectX: unknown
- [ ] CUDA-based alpha-beta speedup: unknown
- [ ] GPU batched evaluation speedup: unknown
- [ ] Optimal model size for 2-second response: unknown
- [ ] PyTorch vs ONNX for inference: unknown

### Kaggle
- [ ] Current leaderboard: unknown
- [ ] Top bot strategies: partially known
- [ ] Board configurations used: partially known
- [ ] Evaluation methodology: partially known
- [ ] Winning strategy: unknown

---

## Documentation Map

| File | Topic | Status |
|------|-------|--------|
| `research/00-comprehensive-report.md` | Initial comprehensive report | ✅ Complete |
| `research/01-game-mechanics.md` | Game rules and board layout | ✅ Complete |
| `research/02-connect4-ai-pipeline.md` | AI pipeline deep dive | ✅ Complete |
| `research/03-deep-research-compendium.md` | Deep research compendium (NEW) | ✅ Complete |
| `research/04-environment-observations.md` | Live env inspection | ✅ Complete |
| `research/05-bot-agent-interface-submission-format.md` | Agent interface docs | ✅ Complete |
| `research/06-package-api-deep-dive.md` | Kaggle API deep dive | ✅ Complete |
| `research/alpha_beta_optimizations_connect4.md` | Alpha-beta optimizations | ✅ Complete |
| `research/research-trajectory.md` | This file — research plan | ✅ Complete |
| `research/research-gaps.md` | Knowledge gap catalog | 🔄 Needs creation |
| `research/kaggle-analysis.md` | Kaggle competition analysis | ❌ Needs research |
| `research/gpu-research.md` | GPU hardware research | ❌ Needs research |
| `research/mcts-research.md` | MCTS research | ❌ Needs research |
| `research/opening-book-research.md` | Opening book research | ❌ Needs research |
| `research/advanced-search-research.md` | Advanced search research | ❌ Needs research |
| `research/final-conclusion.md` | Final architecture decision | ✅ Complete |
| `research/iteration-2-findings.md` | Web research findings from iteration 2 | ✅ Complete |
| `research/nn-architecture-research.md` | Neural network architecture (NEW) | ✅ Complete |
| `research/evaluation-function-design.md` | Evaluation function features and weights (NEW) | ✅ Complete |
| `research/training-data-generation.md` | Training data strategies (NEW) | ✅ Complete |
| `research/neural_network_architectures_connectx.md` | NN architectures, hyperparameters, RTX 5090 timeline (NEW) | ✅ Complete |
| `research/transfer-learning-research.md` | Transfer learning findings (NEW) | ✅ Complete |

---

## How to Use This Document

1. **Start at the top**: Read the "Current Final Conclusion" to understand where we stand
2. **Check knowledge gaps**: See what's been researched and what remains
3. **Pick a priority**: Start with Priority 1 (Kaggle Competition)
4. **Follow the execution plan**: Each phase builds on the previous
5. **Update the conclusion**: After each research phase, update the "Final Conclusion" table
6. **Track hypotheses**: Check off hypotheses as they're tested
7. **Create new documents**: Create new research files for each major topic
8. **Stay on topic**: All research should orbit around "building the best ConnectX bot"

---

## Next Iteration Focus

**Next iteration should focus on**: Kaggle competition reality + remaining agent results integration

Specific tasks:
1. Find current Kaggle ConnectX leaderboard (manual search if API not available)
2. Study top 5 Kaggle solutions on GitHub in detail (code analysis)
3. Read Kaggle forum posts about winning strategies
4. Find and analyze Kaggle notebooks with good ConnectX bots
5. Integrate findings from remaining agents (time management, eval function, training data, Kaggle top bots)
6. Update research trajectory with new findings
7. Update final conclusion if evidence changes

---

## Iteration Log

| Iteration | Date | Focus | Key Findings |
|-----------|------|-------|--------------|
| 1 | 2026-07-30 | Initial deep research audit | Found 7 research docs, identified 8 gap categories, created comprehensive compendium |
| | | | Leading approach: Hybrid NN + Search |
| | | | RTX 5090 specs confirmed: 21,760 CUDA cores, 419 TFLOPS FP8 |
| | | | BitBully is gold standard classical engine |
| | | | SFT→RL pipeline is most effective NN approach |
| 2 | 2026-07-30 | Web research + agent parallel research | Found 8 Kaggle/GitHub repos, created 5+ new research docs, updated hypothesis list |
| | | | dillonloh minimax depth-3 wins 60%+ vs negamax (top 100 Kaggle) |
| | | | athulshibu 4-model lookahead approach (1-4 moves) |
| | | | Neural net architecture: CNN with 3-channel input, 4 conv layers (128 filters), ~500K params |
| | | | Expert-level params: ~250K-500K for 7x6, 2M-4M for competitive 15x13 |
| | | | Training on solved positions: 160K-200K pairs, ~63-65% SFT accuracy |
| | | | Transfer learning 7x6→15x13: 60-70% of native strength, gap scales O(log(N)) |
| | | | Progressive training (4x4→15x13) closes gap from ~32% to ~10% |
| | | | Transformers inferior to CNNs for 7x6; frozen conv layers best approach |
| | | | RTX 5090 total training: ~21 hours end-to-end (SFT: 2h, RL: 18h, transfer: 1h) |
| | | | Evaluation function: 7 core features with weights, adaptive by board size |
| | | | Time management: progressive deepening, game-phase-based allocation |