# Idea Leaderboard — ConnectX Bot Research

> **Created**: 2026-08-03 (Round 26)
> **Last Updated**: 2026-08-04 (Round 32)
> **Purpose**: Ranked list of research ideas, components, and approaches by expected impact on Kaggle bot strength
> **Status**: DRAFT — all rankings are theoretical; empirical validation required via benchmark-blueprint.md experiments

## R30 Updates

- **Idea-003** (Asymmetric Threat Evaluation): Evidence upgraded — C139 VERIFIED (adjacent opening draw unidentifiable by MCTS) directly supports ENS-003's asymmetric threat rationale (1.2x opponent-threat amplification exposes draw positions that symmetric eval misses). Confidence: HIGH→STRONGLY SUPPORTED for 7x6 adjacent-column strategy. No rank change (already #3).
- **Idea-007** (MCTS Consistency Check): Evidence strengthened by BMS-005 benchmark design (MCTS consistency on solved positions, ≥90% oracle agreement target at ≤1600 sims). HYP-003 confidence: LOW→MEDIUM per worker-04. New experiments (EXP-016/017/018) directly test MCTS consistency on adjacent openings.
- **HYP-014** (Timing Governance): New hypothesis added after HYP-013. Documents that 1.5s forced termination with alpha-beta fallback is required for all MCTS ensembles. Linked to ENS-013 safety layer.
- **ENSO-002 timing**: Per worker-05, 5-layer ensemble estimated 3.6-5.6s exceeds 2s Kaggle budget. Downgrade from SUPPORTED→HYPOTHESIS for timing feasibility. This does not affect the ensemble architecture, only the timing gate parameter.

## R32 Updates

- **Idea-001 (Hybrid NN + Classical Search)**: Unchanged — R32 confirms MCTS consistency problem persists across 4 implementations (connectpuct, rowspire, katac4, MCTS-NC). ENS-013 board-size-adaptive routing protocol designed as a mitigation: classical search on small boards, NN-guided MCTS on large boards.
- **Idea-003 (Asymmetric Threat Evaluation)**: R32 adds Kamide/connect-n as a fourth independent implementation using "connection-length scoring + hole-count heuristic" (S123). Evidence strengthened: 4 implementations now agree on asymmetric scoring strategy.
- **Idea-005 (Alpha-Beta + Transposition Table)**: R32 adds Tromp fhourstones88 — 8.3M-entry dual-lock TT with 16-byte Hashentry, 80x larger than Pascal Pons' TT. History-heuristic move ordering and inline fork detection O(7) further validate classical TT optimization.
- **Idea-009 (Board Representation)**: R32 adds pyvezi (bitmask), Kamide (TypeScript 2D array), Tromp (64-bit), connectpuct (list of lists). Board representation comparison becomes EXP-022.
- **New Idea-015 (Board-Size-Adaptive Ensemble Routing)**: ENS-013 introduces board-size-adaptive ensemble routing: classical search on 7×6 (solved game, draw-preserving), NN-guided MCTS on 8×8+. Validated by R32 MCTS consistency problem (all 4 implementations fail on solved positions).
- **Idea-007 (MCTS Consistency Check)**: R32 confirms MCTS consistency problem across 4 independent implementations. MCP theorem (Althöfer 2012) and Kocsis UCT convergence theorem provide theoretical grounding. All MCTS variants fail to identify solved-game positions within practical simulation budgets.
- **Idea-012 (Selective Search)**: R32 confirms MTD(f) and PVS are absent from all corpus implementations (C193-C194 NEEDS_CORRECTION). MTD(f) gap becomes EXP-021.
- **Corpus Governance**: 5 adversarial review workers independently identify 8+ source ID collisions, 14-round gaps between file updates, and claim-count mathematical inconsistencies. Corpus hygiene becomes EXP-025.

## R30 Candidate Evidence Score Changes

| Candidate | Evidence Delta | Rank Change | Rationale |
|-----------|---------------|-------------|-----------|
| Idea-003 | VERIFIED (C139) | None (already #3) | Adjacent draw detection proves asymmetric eval necessity |
| Idea-007 | LOW→MEDIUM | None (already #7) | BMS-005 design + EXP-016/017/018 specify concrete test |
| ENS-002 timing | SUPPORTED→HYPOTHESIS | N/A | 5-layer ensemble exceeds 2s budget |
| HYP-014 | PROPOSED | New | Timing governance required for all MCTS ensembles |

---

## Ranking Methodology

Ideas are ranked by **estimated expected value** on Kaggle ConnectX:

| Rank Metric | Description |
|-------------|-------------|
| **Impact** | Expected ELO or win-rate improvement if the idea works |
| **Confidence** | Strength of evidence supporting the idea |
| **Feasibility** | Effort required to implement within Kaggle constraints (95MB binary, 2s/move, T4 GPU) |
| **Novelty** | How distinct this idea is from already-verified components |

Estimated improvement is measured in **ELO points** against:
- B-01 (Random): baseline
- B-02 (Minimax depth-3, no eval): 0% win rate for any reasonable bot
- B-03 (Depth-5 alpha-beta with rowspire eval): ~60% win rate for classical bots
- N-001 (katac4, if feasible to train on T4): unknown — future experiment FE-001

---

## Top Ideas (Verified or Strongly Supported)

### Idea-001: Hybrid NN + Classical Search (ResNet PUCT MCTS)

- **Rank**: 1
- **Source**: N-001 (katac4), C-001 (rowspire)
- **Evidence**: VERIFIED — full source decoded; 300K ELO testing; most complete pipeline in corpus
- **Estimated Impact**: +400-600 ELO over classical baselines
- **Confidence**: HIGH — component evidence is strong; integration mechanism is known
- **Feasibility**: MEDIUM — requires PyTorch on Kaggle T4; training time may exceed 72h
- **Key Risk**: Kaggle T4 may not have sufficient compute for competitive inference (H-006)
- **Related Components**: b3c128nbt ResNet (530K params), PUCT (c_puct=1.0), FPU (c_fpu=0.2), LCB move selection
- **Tested In**: katac4 300K ELO games; rowspire MCTS benchmark

---

### Idea-002: Supervised Pre-training + Self-play Fine-tuning

- **Rank**: 2
- **Source**: D-001 (TonyCWang 958M rows), N-001 (katac4)
- **Evidence**: STRONGLY SUPPORTED — TonyCWang dataset verified; self-play fine-tuning standard in AlphaZero literature
- **Estimated Impact**: +200-400 ELO over random initialization
- **Confidence**: MEDIUM — no ConnectX-specific benchmark yet; H-004 captures uncertainty
- **Feasibility**: HIGH — D-001 is 14.8 GB Parquet; standard PyTorch training
- **Key Risk**: Phase-bucket bias in training data (40% early 0-8 moves, 20% late 21-30, FU-026)
- **Related Components**: TonyCWang dataset, supervised pre-training, self-play fine-tuning
- **Tested In**: No ConnectX-specific benchmark; general AlphaZero literature supports this approach

---

### Idea-003: Asymmetric Threat Evaluation (1.2x opponent weight)

- **Rank**: 3
- **Source**: C-005 (QveenCoder), C-006 (nguyenthequang)
- **Evidence**: VERIFIED — independently confirmed by 2 implementations; C005 VERIFIED
- **Estimated Impact**: +50-100 ELO in tactical positions
- **Confidence**: HIGH — two independent implementations agree on 1.2x amplification
- **Feasibility**: HIGH — simple scalar multiplier in eval function
- **Key Risk**: May over-weight opponent threats in non-tactical positions
- **Related Components**: Window scoring, threat detection
- **Tested In**: QveenCoder (400+ games), nguyenthequang (200+ games)

---

### Idea-004: Opening Book (Shannon Library)

- **Rank**: 4
- **Source**: S-002 (Pascal Pons), C-003 (Kite)
- **Evidence**: VERIFIED — C006 needs correction; S-002 book generation verified; Kite 95.6MB book (C109)
- **Estimated Impact**: +100-200 ELO in opening phase
- **Confidence**: HIGH — Shannon library is a standard chess technique; works for ConnectX
- **Feasibility**: MEDIUM — book size must fit 95MB Kaggle asset limit
- **Key Risk**: Kaggle T4 book load time; book compression (C-003 book = 95.6MB, exceeds limit)
- **Related Components**: Pascal Pons DEPTH=14 book generator, Kite 15-ply cache, Elias Fano encoding (S-005)
- **Tested In**: Kite 250,000x book speedup (22us vs 5.5s)

---

### Idea-005: Alpha-Beta with Transposition Table

- **Rank**: 5
- **Source**: S-002 (Pascal Pons), C-004 (Reticle)
- **Evidence**: VERIFIED — Pascal Pons source decoded; Reticle has disabled TT (C071 NEEDS_CORRECTION)
- **Estimated Impact**: +30-80 ELO in midgame
- **Confidence**: HIGH — TT is a standard optimization in classical game engines
- **Feasibility**: HIGH — hash table with key encoding; Python dict is a reasonable TT
- **Key Risk**: Reticle TT was disabled (commented-out dead code) — may indicate difficulty in Connect 4
- **Related Components**: Zobrist hashing, symmetric keys, TT probing in search loop
- **Tested In**: Pascal Pons (9x6 solved); Reticle (TT disabled)

---

### Idea-006: NN Leaf Evaluation for Classical Search

- **Rank**: 6
- **Source**: S-005 (ecc521 NNUE), C-001 (rowspire dual MLP)
- **Evidence**: SUPPORTED — NNUE is a well-known technique in chess engines; ecc521 source verified
- **Estimated Impact**: +50-150 ELO over classical eval in midgame
- **Confidence**: MEDIUM — NNUE applied to Connect 4, but not benchmarked
- **Feasibility**: MEDIUM — NN inference on CPU requires optimized runtime (NNUE/ONNX/TensorRT)
- **Key Risk**: NN inference latency may exceed 2s/move limit; Kaggle T4 GPU availability for CPU models
- **Related Components**: NNUE architecture, pre-trained weights, Elias Fano encoding (S-005)
- **Tested In**: ecc521 (weights for 7x6 and 8x8); rowspire dual MLP (128-unit)

---

## Secondary Ideas (Suggested or Hypothesis)

### Idea-007: MCTS Consistency Check

- **Rank**: 7
- **Source**: H-002 (MCTS inconsistency on solved games)
- **Evidence**: HYPOTHESIS — H-002 captures this; MCTS may not converge within practical budgets on solved games
- **Estimated Impact**: +0-50 ELO (if MCTS is inconsistent, results may be noisy rather than stronger)
- **Confidence**: MEDIUM — theoretical concern, untested empirically
- **Feasibility**: HIGH — add convergence check to MCTS loop
- **Key Risk**: May waste simulations on converged positions
- **Related Components**: Visit count thresholds, convergence detection
- **Tested In**: Unknown — no empirical benchmark of MCTS convergence on solved Connect 4

---

### Idea-008: Game-Phase Routing (Book → Search → Tablebase)

- **Rank**: 8
- **Source**: README.md (game-phase strategy); S-002 (book), S-003 (endgame)
- **Evidence**: SUPPORTED — standard in chess engines; applicable to ConnectX
- **Estimated Impact**: +30-100 ELO (phase-aware optimization)
- **Confidence**: MEDIUM — mechanism is known; not benchmarked for ConnectX
- **Feasibility**: HIGH — simple phase detection (move count)
- **Key Risk**: Over-engineering; may not be worth the implementation complexity
- **Related Components**: Shannon library (early), alpha-beta (mid), tablebase (end)
- **Tested In**: No ConnectX-specific benchmark

---

### Idea-009: Board Representation Optimization

- **Rank**: 9
- **Source**: C-009 (pyvezi bitboard), C-001 (rowspire bitboard)
- **Evidence**: VERIFIED — bitboard representation feasible in Python (pyvezi); rowspire uses bitboard in Rust
- **Estimated Impact**: +0-20 ELO (performance, not strength; may enable deeper search within 2s)
- **Confidence**: MEDIUM — performance benefit is clear; strength benefit is indirect
- **Feasibility**: MEDIUM — bitboard ops in Python require careful implementation
- **Key Risk**: Python integer bitmasks are slower than C++ bitboards; may not justify complexity
- **Related Components**: Carry-propagation move gen, Brian Kernighan popcount, 64-bit masks
- **Tested In**: pyvezi (Python bitboard, unbenchmarked); rowspire (Rust bitboard, full source decoded)

---

### Idea-010: Multi-Board Generalization

- **Rank**: 10
- **Source**: N-001 (katac4 trained 9x9-12x12), S-005 (ecc521 4x4-12x12), C-001 (rowspire 12x7)
- **Evidence**: VERIFIED — multiple sources support multi-board architectures
- **Estimated Impact**: +50-100 ELO on non-7x6 boards; unclear on 7x6
- **Confidence**: MEDIUM — multi-board support is demonstrated; strength transfer unknown
- **Feasibility**: MEDIUM — size-aware NN architecture required
- **Key Risk**: Catastrophic forgetting on 7x6 when training on 9x9-12x12
- **Related Components**: Size-aware NN inputs, canonical board normalization
- **Tested In**: katac4 trained on 9x9-12x12 (C040); S-005 supports 4x4-12x12

---

### Idea-011: GPU-Massively-Parallel MCTS

- **Rank**: 11
- **Source**: M-001 (pklesk mcts_numba_cuda)
- **Evidence**: VERIFIED — C079 (75.1% vs 2.5% baseline), C080 (20.3M playouts/5s A100)
- **Estimated Impact**: +100-300 ELO (if Kaggle T4 can run Numba CUDA MCTS)
- **Confidence**: MEDIUM — GPU MCTS works on A100; Kaggle T4 compatibility untested
- **Feasibility**: LOW — requires Numba + CUDA on Kaggle T4; untested combination
- **Key Risk**: Numba may not work on Kaggle T4; GPU memory may be insufficient for large TT
- **Related Components**: GPU MCTS variants (ocp_thrifty, acp_prodigal), lock-free design
- **Tested In**: A100 (20.3M playouts/5s); Kaggle T4 estimate only (C164)

---

### Idea-012: Selective Search (Tactical Guard + MTD(f))

- **Rank**: 12
- **Source**: S-004 (BitBully MTD(f)), C-004 (threat-map)
- **Evidence**: HYPOTHESIS — MTD(f) speedup from S-004 is NEEDS_CORRECTION (20-30% claim)
- **Estimated Impact**: +20-60 ELO (if MTD(f) provides speedup)
- **Confidence**: LOW — numerical claim from C006 is NEEDS_CORRECTION
- **Feasibility**: MEDIUM — MTD(f) requires iterative search; more complex than alpha-beta
- **Key Risk**: C006 may be wrong; MTD(f) may not provide claimed speedup for Connect 4
- **Related Components**: MTD(f), iterative value narrowing, tactical guard (threat-map)
- **Tested In**: Not benchmarked on Connect 4

---

## Bottom Ideas (Unverified or Low Confidence)

### Idea-013: Text-Based LLM Fine-Tuning

- **Rank**: 13
- **Source**: D-002 (Leon-LLM), D-003 (Lyte)
- **Evidence**: HYPOTHESIS — text notation is theoretically inferior to board-state
- **Estimated Impact**: +0-30 ELO (likely negligible)
- **Confidence**: LOW — text-based approach is a poor representation for Connect 4
- **Feasibility**: HIGH — fine-tune small model on text notation
- **Key Risk**: Compounding error in text notation; no board-state awareness
- **Related Components**: Move-by-move text notation, outcome labels
- **Tested In**: None

---

### Idea-014: LLM as ConnectX Bot (via text-to-action)

- **Rank**: 14
- **Source**: Internal knowledge — LLMs for game play
- **Evidence**: HYPOTHESIS — no evidence LLMs can play Connect 4 competitively
- **Estimated Impact**: +0-50 ELO (speculative)
- **Confidence**: VERY LOW — no empirical evidence for this approach in Connect 4
- **Feasibility**: HIGH (if using Kaggle API) but effectiveness untested
- **Key Risk**: LLM cannot reason about full game tree; latency exceeds 2s/move
- **Related Components**: GPT, Claude, Gemini API integration
- **Tested In**: None

---

### Idea-015: Board-Size-Adaptive Ensemble Routing

- **Rank**: 10 (new, co-ranked with Idea-010)
- **Source**: ENS-013 (board-size-adaptive routing protocol), R32 MCTS consistency audit
- **Evidence**: HYPOTHESIS — theoretical design based on MCTS consistency problem confirmed across 4 implementations. Classical search dominates on 7×6 (solved game); NN-guided MCTS scales better on 8×8+.
- **Estimated Impact**: +30-100 ELO on 8×8+ boards; +0-50 ELO on 7×6 (draw-preserving routing avoids MCTS inconsistency)
- **Confidence**: MEDIUM — MCTS consistency problem is VERIFIED; routing protocol is designed but untested
- **Feasibility**: MEDIUM — requires game-phase and board-size detection + routing arbiter
- **Key Risk**: Routing overhead may offset component benefits; board-size gate parameters unknown
- **Related Components**: ENS-013 routing protocol, Kamide adaptive scoring (classical component), rowspire/katac4 NN-MCTS (scalable component)
- **Tested In**: No empirical benchmark; EXP-023 specifies validation protocol

---

## Ranking Summary Table

| Rank | Idea | Source | Impact | Confidence | Feasibility | R30 Note |
|------|------|--------|--------|------------|-------------|----------|
| 1 | Hybrid NN + Search (ResNet PUCT) | N-001, C-001 | +400-600 | HIGH | MEDIUM | ENS-014 high-ceiling design |
| 2 | Supervised Pre-training + Self-play | D-001, N-001 | +200-400 | MEDIUM | HIGH | Unchanged |
| 3 | Asymmetric Threat Eval (1.2x) | C-005, C-006 | +50-100 | STRONGLY SUPPORTED | HIGH | C139 VERIFIED supports adjacent draw detection |
| 4 | Opening Book (Shannon Library) | S-002, C-003 | +100-200 | HIGH | MEDIUM | ENS-013/015 primary component |
| 5 | Alpha-Beta + Transposition Table | S-002, C-004 | +30-80 | HIGH | HIGH | ENS-013/015 primary component |
| 6 | NN Leaf Eval for Classical Search | S-005, C-001 | +50-150 | MEDIUM | MEDIUM | ENS-014 NN-guided MCTS |
| 7 | MCTS Consistency Check | H-002 | +0-50 | MEDIUM | HIGH | HYP-003 upgraded; BMS-005+EXP-016/017/018 |
| 8 | Game-Phase Routing | README, S-002 | +30-100 | MEDIUM | HIGH | ENS-013 timing gate (1.5s fallback) |
| 9 | Board Representation (Bitboard) | C-009, C-001 | +0-20 | MEDIUM | MEDIUM | ENS-015 bitboard-only design |
| 10 | Multi-Board Generalization | N-001, S-005 | +50-100 | MEDIUM | MEDIUM | Unchanged |
| 11 | GPU Massively-Parallel MCTS | M-001 | +100-300 | MEDIUM | LOW | ENS-014 GPU-MCTS high-ceiling |
| 12 | Selective Search (MTD(f)) | S-004, C-004 | +20-60 | LOW | MEDIUM | C193-C194 NEEDS_CORRECTION (no MTD(f)/PVS in corpus); EXP-021 specifies investigation |
| 13 | Text-Based LLM Fine-Tuning | D-002, D-003 | +0-30 | LOW | HIGH | Unchanged |
| 14 | LLM as ConnectX Bot | Internal knowledge | +0-50 | VERY LOW | HIGH | Unchanged |
| 15 | Board-Size-Adaptive Ensemble Routing | ENS-013, R32 MCTS audit | +30-100 | MEDIUM | MEDIUM | New R32: routing protocol designed; MCTS consistency problem validated across 4 implementations |

---

## Future Experiment Assignments

| Idea | Benchmark Experiment | Tier |
|------|---------------------|------|
| 1 | FE-001: NN + MCTS vs classical baseline | C |
| 2 | FE-002: Supervised pre-training vs random init | C |
| 3 | FE-003: Asymmetric vs symmetric eval on Tier A | A |
| 4 | FE-004: Opening book size vs strength | B |
| 5 | FE-005: TT hit rate and strength correlation | C |
| 6 | FE-006: NN leaf eval latency and strength | C |
| 7 | FE-007: MCTS consistency vs search depth | D |
| 8 | FE-008: Game-phase routing efficiency | C |
| 9 | FE-009: Bitboard vs array performance | C |
| 10 | FE-010: Multi-board transfer learning | E |
| 11 | FE-011: GPU MCTS on Kaggle T4 emulation | F |
| 12 | FE-012: MTD(f) vs alpha-beta speedup | C |

---

## Data Quality Notes

1. **All impact estimates are theoretical** — no empirical benchmarks have been run.
2. **All rankings are relative to each other** — not absolute strength measures.
3. **Confidence scores reflect evidence quality**, not estimated strength.
4. **Feasibility is constrained by Kaggle limits** (95MB binary, 2s/move, T4 GPU, 72h training).
5. **Ideas ranked 13-14 are speculative** — included for completeness, but low expected value.
6. **No LLM has been verified as a competitive ConnectX player** — ideas 13-14 are included for research completeness, not recommendation.

---

ENDOFFILE