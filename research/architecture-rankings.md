# Architecture Rankings — ConnectX Bot

> **Current Round**: 11
> **Last Updated**: 2026-08-02

---

## Current Rankings (Post Round 11)

| Rank | Approach | Confidence | 7x6 Strength | 15x13 Strength | Evidence Grade | Major Unknowns |
|------|----------|------------|-------------|----------------|---------------|----------------|
| 1 | Hybrid NN + Search | HIGH | ★★★★★ | ★★★★☆ | SUPPORTED | NN quality on 15x13, transfer learning effectiveness |
| 2 | MCTS + NN (AlphaZero) | MEDIUM-HIGH | ★★★★☆ | ★★★★★ | SUPPORTED | MCTS convergence speed, self-play cost, Kaggle feasibility |
| 3 | Classical Engine (MTD(f) + Python/C++) | MEDIUM | ★★★★★ | ★★☆☆☆ | SUPPORTED | C++ binding complexity on Kaggle, 15x13 depth |
| 4 | Pure Search (Python alpha-beta + heuristics) | MEDIUM | ★★★★☆ | ★★☆☆☆ | SUPPORTED | Depth limits on 15x13, eval function quality |
| 5 | Pure Neural Network | LOW | ★★★☆☆ | ★★★☆☆ | HYPOTHESIS | NN precision without search, generalization |
| 6 | Supervised Pre-training + Search | MEDIUM | ★★★★☆ | ★★★☆☆ | SUPPORTED | Board-state dataset transfer to ConnectX, target encoding mapping |

---

## Score Breakdown

### 1. Hybrid NN + Search — Confidence: HIGH

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 5/5 | NN eval at leaves + search = near-perfect |
| 15x13 expected strength | 4/5 | NN guidance enables deeper effective search |
| Tactical correctness | 5/5 | Search guarantees optimal play when it can see win |
| Robustness | 4/5 | Works across all board sizes |
| Kaggle compliance | 4/5 | Pure Python (NN + search) — no C++ needed |
| Inference latency | 4/5 | NN ~0.5-2ms + search ~0.1-2s = within 2s budget |
| Offline compute | 3/5 | Training requires RTX 5090 or similar (21h end-to-end) |
| RTX 5090 feasibility | 4/5 | Training feasible offline; deployment on Kaggle T4 |
| Engineering complexity | 3/5 | Requires NN training + search engine + integration |
| Verification difficulty | 3/5 | Hard to prove optimality; empirical testing required |
| Overfitting risk | 3/5 | NN may overfit 7x6; transfer learning needed |
| Reproducibility | 3/5 | Training is deterministic; self-play varies |
| Evidence grade | SUPPORTED | Multiple sources (AlphaZero, BEPb, marcpaulo15) |
| Major unknowns | NN quality on 15x13, transfer learning gap | |
| **Evidence For** | • NN + search beats pure search (literature) • 7x6 solved → NN can learn optimal play • RTX 5090 enables fast training | |
| **Evidence Against** | • NN training may not converge to expert level • 21h training time is substantial • Overfitting risk on 7x6 → 15x13 transfer | |
| Score change rationale | Confidence upgraded from MEDIUM-HIGH → HIGH (Round 5) due to game-phase model evidence | |

### 2. MCTS + NN (AlphaZero) — Confidence: MEDIUM-HIGH

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 4/5 | MCTS can explore near-optimally on 7x6 |
| 15x13 expected strength | 5/5 | MCTS scales better than alpha-beta on large boards |
| Tactical correctness | 4/5 | MCTS doesn't guarantee optimality but converges |
| Robustness | 4/5 | Proven on Go, Shogi, Chess |
| Kaggle compliance | 3/5 | Requires NN inference + MCTS within 2s/move |
| Inference latency | 3/5 | NN ~0.5ms + thousands of MCTS rolls = may exceed 2s |
| Offline compute | 2/5 | Self-play training requires massive compute |
| RTX 5090 feasibility | 3/5 | Training feasible but 50K+ games self-play = ~18h+ |
| Engineering complexity | 2/5 | Complex: MCTS + NN + self-play loop |
| Verification difficulty | 2/5 | Hard to verify without running |
| Overfitting risk | 2/5 | Self-play may converge to local optimum |
| Reproducibility | 3/5 | Self-play is stochastic but reproducible |
| Evidence grade | SUPPORTED | AlphaZero literature, BEPb, GoodCoder666/katac4 (R7) |
| Major unknowns | MCTS moves per 2s budget on 15x13, NN quality needed | |
| **Evidence For** | • MCTS + NN wins Go, Shogi, Chess • GoodCoder666/katac4 (18★): KataGo-inspired engine with 1600 sims, FPU, ELO-tested on 300K games, 8 days on 4×RTX 4090 • Training on randomized 9×9–12×12 boards shows generalization • blanyal/alpha-zero (92★): full AlphaZero impl • tre-systems/rowspire (0★): dual 4×128 MLP value+policy, bitboard solver, WASM deployment, 4000 sims, genetic tuning • No MCTS-based public repos for ConnectX (opportunity) • NN policy guides MCTS efficiently • PUCT benchmark (11/20 vs minimax) validates MCTS strength (connectpuct) | |
| **Evidence Against** • AlphaZero required 8×V100 for training • 2s/move may not allow enough MCTS rolls (katac4 uses 1600 sims but on larger boards) • Self-play convergence is slow | |
| Score change rationale | MEDIUM-HIGH (Round 7) — GoodCoder666/katac4 provides strongest evidence yet for MCTS+NN: advanced KataGo techniques (FPU, adaptive CPUCT, LCB), 1600 simulations, ELO-based benchmarking, generalization across board sizes. No change in rank. | |

### 3. Classical Engine (MTD(f) + C++) — Confidence: MEDIUM

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 5/5 | Perfect play (solved game) |
| 15x13 expected strength | 2/5 | Limited search depth on large board |
| Tactical correctness | 5/5 | MTD(f) provably finds optimal when depth sufficient |
| Robustness | 3/5 | Excellent on 7x6, weak on 15x13 |
| Kaggle compliance | 3/5 | C++ binding adds complexity; Python constraint |
| Inference latency | 5/5 | C++ search: ~0.001s on 15x13 depth 3 |
| Offline compute | 5/5 | No training needed |
| RTX 5090 feasibility | N/A | Pure CPU approach |
| Engineering complexity | 3/5 | Pybind11 binding overhead |
| Verification difficulty | 2/5 | Can verify against tablebase on 7x6 |
| Overfitting risk | 5/5 | N/A — no learning component |
| Reproducibility | 5/5 | Deterministic search |
| Evidence grade | SUPPORTED | BitBully, allis1988, Bock 2025 |
| Major unknowns | 15x13 search depth achievable in 2s, C++ on Kaggle | |
| **Evidence For** • BitBully perfect on 7x6 • C++ 50-100× faster than Python • MTD(f) 20-30% faster than alpha-beta | |
| **Evidence Against** • Kaggle Python submission makes C++ complex • 15x13 depth limits: depth 3-5 insufficient for expert play • No tablebase for 15x13 | |
| Score change rationale | Downgraded from MEDIUM-HIGH → MEDIUM (Round 5) — Kaggle Python constraint makes C++ binding less attractive | |

### 4. Pure Search (Python alpha-beta) — Confidence: MEDIUM

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 4/5 | Depth 8-12 with Numba JIT |
| 15x13 expected strength | 2/5 | Depth 2-3 only |
| Tactical correctness | 3/5 | Depends on eval function quality |
| Robustness | 3/5 | Good baseline but limited |
| Kaggle compliance | 5/5 | Pure Python — no dependencies |
| Inference latency | 4/5 | Numba JIT gives ~0.1s depth 5 on 15x13 |
| Offline compute | 5/5 | No training needed |
| RTX 5090 feasibility | N/A | Pure CPU approach |
| Engineering complexity | 4/5 | Simple: search + eval function |
| Verification difficulty | 4/5 | Can verify against tablebase on 7x6 |
| Overfitting risk | 5/5 | N/A — no learning component |
| Reproducibility | 5/5 | Deterministic search |
| Evidence grade | SUPPORTED | Multiple Kaggle implementations, mra1991 |
| Major unknowns | Eval function quality, depth on 15x13 | |
| **Evidence For** • Simplest implementation • Numba 5-10× speedup • dillonloh depth-3 beats negamax 60%+ on Kaggle | |
| **Evidence Against** • 15x13 depth 2-3 is weak • Eval function may miss complex patterns | |
| Score change rationale | No change (Round 5) — still a good baseline but not competitive for large boards | |

### 5. Pure Neural Network — Confidence: LOW

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 3/5 | NN memorization vs true reasoning |
| 15x13 expected strength | 3/5 | May generalize better than search |
| Tactical correctness | 2/5 | NN makes tactical errors without search |
| Robustness | 2/5 | NN can be brittle |
| Kaggle compliance | 4/5 | Pure Python NN inference |
| Inference latency | 5/5 | ~0.5-2ms per evaluation |
| Offline compute | 2/5 | Requires significant training |
| RTX 5090 feasibility | 3/5 | Training feasible but convergence uncertain |
| Engineering complexity | 4/5 | Simpler than hybrid (no search engine) |
| Verification difficulty | 1/5 | Very hard to verify without search |
| Overfitting risk | 1/5 | High risk on small datasets |
| Reproducibility | 3/5 | Training is deterministic but stochastic initialization |
| Evidence grade | HYPOTHESIS | Limited evidence for ConnectX specifically |
| Major unknowns | NN precision without search, generalization to unseen positions | |
| **Evidence For** • Fastest inference • Simplest architecture • Can learn complex patterns from data | |
| **Evidence Against** • Lacks precision (63-65% minimax agreement) • No pure-NN ConnectX top 100 Kaggle bots found • NN alone cannot guarantee optimal play | |
| Score change rationale | Downgraded from LOW-MEDIUM → LOW (Round 5) — NN alone lacks precision for competitive play | |

### 6. Supervised Pre-training (Board-State) — Confidence: MEDIUM

| Factor | Rating | Notes |
|--------|--------|-------|
| 7x6 expected strength | 5/5 | Ground-truth optimal evaluations from Pascal Pons solver; supervised pre-training achieves perfect policy on solved positions |
| 15x13 expected strength | 3/5 | Dataset is 7×6 only; needs transfer learning or generalization |
| Tactical correctness | 5/5 | Exact optimal column evaluations; solver provides definitive answers |
| Robustness | 4/5 | Proven dataset generation method; 958M records provides broad coverage |
| Kaggle compliance | 4/5 | Board-state input (2×6×7 tensor) needs reshape for flat 1D observation; otherwise pure Python PyTorch |
| Inference latency | 5/5 | Small ResNet (~200K params) on 2×6×7 → ~0.5ms inference |
| Offline compute | 2/5 | Supervised pre-training requires GPU (958M records); 958M rows × 2×6×7 × 4 bytes ≈ 14.8 GB dataset |
| RTX 5090 feasibility | 4/5 | Training feasible on RTX 5090; 958M records is large but manageable with batching |
| Engineering complexity | 3/5 | ResNet encoder + policy head; simpler than AlphaZero (no self-play loop) |
| Verification difficulty | 1/5 | Can verify against solver on 7×6 positions |
| Overfitting risk | 3/5 | Dataset covers all positions reachable by self-play; solver provides ground truth |
| Reproducibility | 4/5 | Dataset is fixed; training is deterministic with same architecture |
| Evidence grade | VERIFIED | S042-S044 (Pascal Pons solver, TonyCWang dataset card) |
| Major unknowns | Training convergence on 958M records, generalization to non-solved positions, transfer to 15×13 | |
| **Evidence For** • TonyCWang/ConnectFour: 958M rows of exact optimal evaluations • Pascal Pons solver confirmed via source code (negamax + PVS + TT + book) • Board-state input maps directly to ResNet architecture • Targets are ground truth, not learned estimates — faster convergence than AlphaZero self-play | |
| **Evidence Against** • Dataset is 7×6 only (Connect 4, not general ConnectX) • Self-play with temperature may miss some board positions • 958M records requires significant training infrastructure | |
| Score change rationale | NEW — Round 11 introduces this approach via TonyCWang dataset discovery (958M solver-generated training pairs). Theoretically the strongest training strategy for 7×6 ConnectX if supervised pre-training converges. Not directly ranked against search engines because this is a training strategy, not a runtime strategy — best used WITH a search engine (NN evaluation at leaves or NN-guided MCTS). | |

---

## Ranking Stability

| Round | Leader | Changes | Notes |
|-------|--------|---------|-------|
| 1 | Hybrid NN+Search | Initial | Based on 7x6 solved + 15x13 needs NN |
| 2 | Hybrid NN+Search | Confidence upgraded | More evidence from web research |
| 3 | Hybrid NN+Search | Confidence upgraded | Kaggle analysis supports hybrid |
| 4 | Hybrid NN+Search | MCTS+NN upgraded | MCTS evidence strengthened for large boards |
| 5 | Hybrid NN+Search | MCTS+NN upgraded, Classical downgraded | Game-phase model solidified |
| 6 | Hybrid NN+Search | No change — but 9 new verified sources added (blanyal/alpha-zero, Tarun995 bitboard, 5 DQN/MCTS repos); MCTS+NN evidence strengthened by 92-star AlphaZero impl; Internal-knowledge repos (BitBully, mra1991) unverified (404) |
| 7 | Hybrid NN+Search | No change — but GoodCoder666/katac4 (18★) verified as first KataGo-inspired AlphaZero for Connect 4; Wikipedia confirms solved game (C001 upgraded from UNKNOWN→SUPPORTED); MCTS+NN evidence strengthened by advanced techniques (FPU, adaptive CPUCT, LCB, 1600 sims, ELO testing); Unknown claims dropped from 13% to 7% |
| 8 | Hybrid NN+Search | No change — but rowspire (0★) provides strongest individual project yet: dual 4×128-layer MLP + MCTS + bitboard solver + WASM deployment + genetic tuning; connectpuct provides first PUCT benchmark (11/20 vs minimax depth 3); kite adds Java bitboard solver; VERIFIED claims reached 50%; 3 new sources (S029-S031) |
| 9 | Hybrid NN+Search | No change — but Tromp Fhourstones benchmark (20 systems, KPOS/S, Gprof) provides strongest classical search evidence yet; katac4 training fully decoded (30K epochs, 3 loss terms, self-play workers); katac4 ResNet fully decoded (pre-activation, nested bottleneck, mixed pooling); haithameleuch alpha-beta+MCTS hybrid verified; VERIFIED claims 50%→55%; 7 new sources (S032-S038); ICAPS/JOCIG/Google Scholar all unworkable |
| 10 | Hybrid NN+Search | No change — but rowspire fully decoded from source (14 Rust files): 4×128 MLP with skip connections, dual value+policy, 100D input encoding (64-cell binary + 16 normalized features), 7-feature evaluation with genetic-tuned weights, UCB1 MCTS (c=1.41, 4000 sims, root noise 75/25), 64-bit bitboard with carry-propagation move generation. Training algorithm remains opaque (npm run train is un-publish code). eSlams discovered as novel evaluation framework (50 arenas, REST protocol, Ed25519 proof archives). kenrick95/c4 (278★) cataloged: browser-based Minimax+alpha-beta. Wikipedia opening theory confirmed. VERIFIED claims 55%→60%. 3 new sources (S039-S041). |
| 11 | Hybrid NN+Search | No change — but Pascal Pons/connect4 solver fully decoded (C++ negamax + PVS + TT + opening book, iterative null-window binary search, template WIDTH/HEIGHT board sizes); TonyCWang/ConnectFour dataset discovered (958M rows, 14.8 GB, 2×6×7 binary observations + 7-element target vectors from solver); Hugging Face LLM-based Connect 4 model catalog (11+ models, all lacking evaluation metrics). NEW approach added: Supervised Pre-training + Search (board-state). Evidence audit: 17 structural issues fixed (duplicate claim section removed, duplicate sources merged, stale headers updated). VERIFIED claims 60%→66%. 9 new sources (S042-S048 added; S026-S028 deduplicated). |

---

## What Would Change the Ranking

| Scenario | Would Change? | How |
|----------|--------------|-----|
| NN training fails to converge | Yes | Drop Hybrid to #3, Pure Search to #1 |
| MCTS achieves 1000+ moves/2s on 15x13 | Yes | MCTS+NN may become #1 |
| C++ bindings work seamlessly on Kaggle | Yes | Classical Engine may jump to #1 on 7x6 |
| 15x13 first-player advantage proven weak | Yes | Search may become more viable on large boards |
| NN achieves >95% minimax agreement on 15x13 | Yes | Pure NN may jump significantly |
| Web search restored and reveals new winning strategies | Yes | Could dramatically change rankings |
| New solved game result for larger board | Yes | Would reshape game-phase model |