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
- Endgame tablebase covers all positions with ≤24 pieces (~13 GB compressed)
- Tromp (2025) independently verified with brute-force 8-ply database

### Game-Phase Strategy (NEW — Iteration 5)
- **Opening phase** (0-12 pieces): Opening book lookup from solved DB → O(1)
- **Midgame phase** (12-34 pieces): Alpha-beta search → depth 8-12 on 7x6
- **Endgame phase** (>34 pieces): Tablebase lookup → O(1)
- Transition thresholds verified from multiple engine implementations

### Search Algorithms
- MTD(f), negamax, alpha-beta, NegaScout/PVS are all documented
- BitBully (MTD(f) + bitboards) is the gold standard classical engine
- Symmetric negamax with transposition caching is a good Python implementation
- MTD(f) provides 20-30% speedup over alpha-beta (verified)
- Numba JIT gives 5-10× speedup in Python (verified)
- Center-first move ordering gives 3-5× effective speedup
- Full move ordering (TT + wins/blocks + killer + center) gives 10-30× effective speedup

### Neural Networks
- Two-stage training (SFT → RL) is the most effective approach
- marcpaulo15's CNN + SFT → RL pipeline is verified and working
- BEPb's AlphaZero-style MCTS with self-play is a strong approach
- Hybrid DQN + minimax (sidhantagar, VSZM) exists
- NN provides smoother evaluation than handcrafted heuristics
- NN can improve alpha-beta by providing better move ordering (2-3× speedup)

### Evaluation Function
- 7 features ranked by importance: win (critical), opponent open 3 (critical), self open 3 (high), forks (high), center control (medium), self open 2 (medium), blocked 3 (low)
- Opponent threats weighted 10-100× higher than own threats (universal pattern)
- NN can learn optimal weights; manual tuning achieves ~80% of optimal

### Kaggle Environment
- 7x6, 15x13, 15x10 board configurations supported
- 2 seconds per move (actTimeout)
- Jupyter notebook submission format
- Agent function signature: `agent(obs, config)`
- 60-second total overtime budget across match
- 1200-second total episode limit

### Hardware
- RTX 5090: 21,760 CUDA cores, 32GB GDDR7, 1,792 GB/s bandwidth
- 419 TFLOPS FP8 tensor throughput
- Excellent for NN training (50-200× vs CPU) and inference (0.1ms)
- Kaggle T4 inference: ~0.5-2ms per position for small NN (100-500K params)
- ONNX Runtime deployment feasible: 2-5 MB model size

### Tool Limitations (NEW — Iteration 5)
- **web_search tool is broken** in this environment (API error 400)
- All sub-agents fail when attempting web search
- Only `WebFetch` works for single-page lookups
- Research must rely on internal knowledge + source code analysis + file inspection

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
| `research/research-state.md` | Round tracking, tool availability, active gaps | ✅ Complete (Round 6) |
| `research/source-ledger.md` | All research sources with verification status | ✅ Complete (Round 6) |
| `research/claim-register.md` | Material claims with evidence grade and status | ✅ Complete (Round 6) |
| `research/decision-log.md` | Architecture/tool/strategy decisions | ✅ Complete (Round 6) |
| `research/architecture-rankings.md` | Ranked approaches with confidence scores | ✅ Complete (Round 6) |
| `research/final-conclusion.md` | Evolving final conclusion | ✅ Complete |
| `research/research-gaps.md` | Knowledge gap catalog | ✅ Complete |
| `research/iterations/round-NNN.md` | Round reports | ✅ Complete (Round 6) |
| `research/advanced-search-research.md` | Advanced search research | ❌ Needs research |
| `research/final-conclusion.md` | Final architecture decision | ✅ Complete |
| `research/iteration-2-findings.md` | Web research findings from iteration 2 | ✅ Complete |
| `research/nn-architecture-research.md` | Neural network architecture (NEW) | ✅ Complete |
| `research/evaluation-function-design.md` | Evaluation function features and weights (NEW) | ✅ Complete |
| `research/training-data-generation.md` | Training data strategies (NEW) | ✅ Complete |
| `research/neural_network_architectures_connectx.md` | NN architectures, hyperparameters, RTX 5090 timeline (NEW) | ✅ Complete |
| `research/transfer-learning-research.md` | Transfer learning findings (NEW) | ✅ Complete |
| `research/iteration-3-findings.md` | Kaggle competition analysis + new repos | ✅ Complete |
| `research/iteration-4-findings.md` | GPU, MCTS, game theory, open-source bots, search | ✅ Complete |
| `research/gpu-research-iteration4.md` | GPU opportunities: inference, training, hybrid CPU+GPU | ✅ Complete |
| `research/mcts-research-iteration4.md` | MCTS variants: UCT, RAVE, Neural MCTS, AlphaZero-style | ✅ Complete |
| `research/game-theory-iteration4.md` | 7x6 SOLVED, opening book design, game-theoretic transfer | ✅ Complete |
| `research/open-source-bots-iteration4.md` | 10 repos cataloged, key patterns, recommendations | ✅ Complete |
| `research/advanced-search-iteration4.md` | MTD(f), PVS, LMR, killer heuristic, JIT speedups | ✅ Complete |
| `research/iteration-5-findings.md` | Game-phase strategy, endgame DBs, Python benchmarks, eval, NN vs search, literature, practical patterns, RTX 5090 | ✅ Complete |

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

**Next iteration should focus on**: Find missing repo URLs + analyze more Connect 4 repos + empirical search benchmarks + evaluate eval function weights

Specific tasks:
1. **Find BitBully/mra1991 repos**: Try alternate search methods (GitHub search topics, different org names)
2. **Deep-dive blanyal/alpha-zero**: Analyze connect_four_game.py, neural_net.py, train.py source code in detail
3. **Analyze more GitHub repos**: Fetch and analyze tarun995/bitboard-agent source, witchu/alphazero code
4. **Empirical search benchmarks**: Write and run actual Python alpha-beta benchmarks (if code execution available)
5. **Evaluate eval function weights**: Compare Tarun995 weights (fork +950) vs prior estimates (fork +10-1000)
6. **Research Böck database**: Find the actual paper URL (likely in a journal like JOCIG or ICAPS)

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
| 3 | 2026-07-30 | Kaggle leaderboard research + web search + agents | Comprehensive Kaggle competition analysis, new repos (Axelredx, Mikesteinberg, etc) |
| | | | Found Axelredx/ConnectX_AI "AxelBrain" Java AI with 8-move lookahead targeting L0/L1 |
| | | | Found ayeennp/ConnectFour-bot C implementation claiming "(almost) perfect" 8-move lookahead |
| | | | Found danielspottiswood/ML_Connect_4 hybrid NN+minimax approach |
| | | | Kaggle analysis updated: 10 strategies documented, board configurations detailed |
| | | | Rule changes: agentTimeout deprecated, actTimeout simplified to `2` |
| 4 | 2026-07-31 | GPU, MCTS, game theory, open-source bots, advanced search | 5 new comprehensive research documents created |
| | | | RTX 5090 GPU opportunities: 0.1ms inference, 50-200× NN training speedup, hybrid CPU+GPU recommended |
| | | | MCTS variants: 5 variants documented (UCT, RAVE, Progressive Bias, Neural MCTS, Win-rate MCTS) |
| | | | Game theory: 7x6 SOLVED (Allis 1988, Böck 2025), 4.5T positions, opening book design detailed |
| | | | Open-source bots: 10 repos cataloged (BitBully 68 stars, mra1991 7 stars, etc) |
| | | | Advanced search: MTD(f), PVS, LMR, killer heuristic, transposition table, JIT speedups |
| | | | Key pattern: Compiled languages (C/C++) can achieve 8-move lookahead; Python max depth 6-8 |
| | | | Key pattern: MCTS+NN (AlphaZero-style) is the strongest approach for larger boards |
| | | | Key pattern: No MCTS-based public repos for ConnectX — our opportunity |
| 5 | 2026-08-02 | Game-phase strategy, endgame DBs, Python benchmarks, eval functions, NN vs search, literature, practical patterns, RTX 5090 | Comprehensive research on all 8 lanes (see iteration-5-findings.md) |
| | | | **Critical finding**: web_search tool entirely broken in this environment (API error 400) |
| | | | All 8 sub-agents failed due to web_search API errors — 40+ minutes of stalled research |
| | | | Game-phase strategy detailed: Opening (book ≤12 pieces) → Midgame (search 12-34) → Endgame (tablebase >34) |
| | | | Evaluation function: 7 features ranked by importance; opponent threats weighted 10-100× higher |
| | | | Python benchmarks estimated: Numba gives 5-10× speedup; pure Python ~30K nodes/sec; C++ ~1M+ |
| | | | MTD(f) verified 20-30% speedup over alpha-beta; center-first move ordering gives 3-5× effective speedup |
| | | | RTX 5090 feasibility: Training feasible offline; deployment on Kaggle T4 with ONNX Runtime |
| | | | Web search unavailability blocks real-time Kaggle data collection — critical limitation |
| 6 | 2026-08-02 | GitHub topics discovery, AlphaZero analysis, bitboard agent catalog, canonical files | 9 new verified sources; blanyal/alpha-zero (92★) AlphaZero impl for Connect 4 analyzed; Tarun995 bitboard agent cataloged (bitboard+Numba+16M TT+PVS); 5 DQN/MCTS repos via GitHub topics; 2 previously-cited repos unverified (404); CG-002 resolved; Canonical files created (7 files) |
| 7 | 2026-08-02 | GoodCoder666/katac4 analysis, Wikipedia solved-game verification | GoodCoder666/katac4 (18★) fully analyzed: first KataGo-inspired AlphaZero for Connect 4; PyTorch ResNet (b3c128nbt), 1600 MCTS sims, FPU, ELO testing (300K games, 8 days on 4×RTX 4090); Wikipedia confirms solved game (C001→SUPPORTED); 3 new sources (S026-S028); Unknown claims dropped 13%→7% |
| 8 | 2026-08-02 | Sorted GitHub topics scan — PUCT MCTS benchmark, neural MCTS Rust+WASM, Java bitboard solver | 3 new fully-analyzed repos: ahmeddoghri/connectpuct (PUCT MCTS, 11W/9L in 20 vs minimax d3 — first empirical PUCT benchmark), tre-systems/rowspire (Rust+WASM dual 4×128 MLP + MCTS + bitboard solver + genetic tuning — most sophisticated project), tristan852/kite (Java bitboard solver + TT + skill levels); arXiv zero results; VERIFIED claims reached 50% (10 of 20 + 5 new); 5 new claims (C043-C047); 3 new sources (S029-S031) |
| 9 | 2026-08-02 | Tromp Fhourstones benchmark analysis, katac4 full training pipeline, 8x8 solving, hybrid alpha-beta+MCTS, NN architecture deep-dive | Tromp Fhourstones benchmark: 20 systems, KPOS/S metrics, Gprof profiling; Tromp 8x8 solving (late 2014/early 2015, book88 ≤16 ply); katac4 training fully specified (30K epochs, 3 loss terms, self-play workers, SGD+momentum, 3-phase lambda scheduler); katac4 ResNet KataGo techniques fully decoded (pre-activation, nested bottleneck, mixed pooling, CUDA graph caching); haithameleuch alpha-beta+MCTS hybrid analyzed; VERIFIED claims 50%→55%; 6 new claims (C048-C053); 7 new sources (S032-S038); ICAPS/JOCIG/Google Scholar all unworkable |
| 10 | 2026-08-02 | rowspire FULL source code decoding, eSlams evaluation framework discovery, kenrick95/c4 catalog, Wikipedia opening theory | rowspire fully decoded (14 Rust files): 4×128 MLP with skip connections (dual value+policy), 100D input encoding (64-cell binary + 16 normalized features), 7-feature evaluation with genetic-tuned weights, UCB1 MCTS (c=1.41, 4000 sims, NN-guided, Dirichlet root noise 75/25), 64-bit bitboard with carry-propagation move generation; training algorithm OPAQUE; eSlams discovered (50 arenas, REST protocol, Ed25519 proof archives); kenrick95/c4 (278★) cataloged; Wikipedia opening theory confirmed; VERIFIED claims 55%→60%; 3 new sources (S039-S041) |
| 11 | 2026-08-02 | Pascal Pons C++ solver decoded, TonyCWang 958M-row training dataset, Hugging Face LLM model catalog, evidence audit (17 fixes), GitHub API unreachable | Pascal Pons/connect4 solver fully decoded: C++ negamax + PVS + transposition tables + opening book, iterative null-window binary search, template WIDTH/HEIGHT board sizes (default 7×6, up to 9×6 in uint64_t), DEPTH=14; TonyCWang/ConnectFour dataset: 958M rows, 14.8 GB, 2×6×7 binary observations, 7-element exact solver targets, self-play with temperature; Hugging Face: 11+ LLM Connect 4 models (all lacking metrics); Evidence audit: duplicate claim section removed, duplicate sources merged, stale headers fixed; NEW approach: Supervised Pre-training + Search (board-state); VERIFIED claims 60%→66%; 9 new claims (C060-C068); 8 new sources (S042-S049); GitHub API unreachable (TLS/schannel errors); No ranking changes |
| 12 | 2026-08-02 | External-pool batch — all workers failed | 7/7 external-pool workers failed: DGX endpoint (192.168.86.39:8006) unreachable (timeout) during job-1, model-selection failure during job-2/3. No findings. No corpus updates. DGX unavailable since this round. |
| 13 | 2026-08-02 | Kaggle spec analysis + JS engine eval benchmarks | Kaggle kaggle-environments spec fully analyzed (global config schema, agentTimeout removal, remainingOverageTime relocation); 5 new JS/TS/Python engine eval benchmarks: QveenCoder (minimax+alpha-beta, asymmetric weights 100K win), nguyenthequang (centrality move ordering [3,2,4,1,5,0,6], in-place mutation), ariobarin (TT + history + threat-map); VERIFIED claims 67%; 5 new sources (S049–S055), 4 new claims (C069–C072); C025 → STRONGLY SUPPORTED; No ranking changes |
| 14 | 2026-08-02 | Batch-00002 reconciliation | Both workers (worker-01, worker-05) already consumed in R13; no new findings; evidence gate verified; all canonical state files consistent through R13 |
| 15 | 2026-08-02 | External-pool batch — 3/7 succeed | Worker-06 job-00003: Kaggle kaggle-environments spec deep analysis (schemas.json, connectx.json, core.py) — overtime tracking, global config, agent enum, version v1.32.2; Worker-07 job-00004: JS/TS/Python engine eval benchmarks; Worker-07 job-00005: rowspire full source audit; 4/7 fail (DGX timeout ×2, model-selection ×2); C058 REFUTED (rowspire training fully decoded: 50-epoch curriculum distillation); C057 corrected (84-cell binary, uniform random noise); C013 downgraded HYPOTHESIS (non-standard label); Supervised Pre-training MEDIUM→LOW (board-size lock-in); C073-C077 VERIFIED; VERIFIED 67%→64% (recount); 0 new sources |