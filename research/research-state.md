# Research State -- ConnectX Bot

> **Current Round**: 44 (2026-08-05)
> **Last Updated**: 2026-08-05 19:00 ET
> **Previous Round**: 43 (2026-08-05, KAGGLE-CONNX-SPEC created, GOV-005 R42 governance)
> **Status**: Active -- dossier synthesis phase; 35 dossier files (30 substantive) across 12 directories, 5 source ID collision clusters (Cluster E: CRITICAL), governance remediation at 73%, Write tool availability restored to 100%

---

## Round Progression

| Round | Date | Status | Key Activity |
|-------|------|--------|--------------|
| 1 | 2026-07-30 | Complete | Initial deep research audit, compendium created |
| 2 | 2026-07-30 | Complete | Web research, agent parallel research, 5+ new docs |
| 3 | 2026-07-30 | Complete | Kaggle competition analysis, new repos |
| 4 | 2026-07-31 | Complete | GPU, MCTS, game theory, open-source bots, search |
| 5 | 2026-08-02 | Complete | Game-phase strategy, endgame DBs, benchmarks, eval |
| 6 | 2026-08-02 | Complete | GitHub topics discovery, AlphaZero analysis, bitboard agent catalog; canonical files created |
| 7 | 2026-08-02 | Complete | GoodCoder666/katac4 (18 star) KataGo-inspired AlphaZero fully analyzed; Wikipedia confirms solved game; C001/C005 upgraded to SUPPORTED; 3 new sources (S026-S028) |
| 8 | 2026-08-02 | Complete | 3 new repos via sorted GitHub topics: connectpuct (PUCT benchmark 11/20), rowspire (
NN-001: Neural Network Architectures, Training Pipelines, and Data [READY, 44.6KB]
neural MCTS + bitboard solver Rust+WASM), kite (Java bitboard solver); arXiv zero results; 5 new claims (C043-C047); 3 new sources (S029-S031) |
| 9 | 2026-08-02 | Complete | Tromp Fhourstones benchmark (20 systems, KPOS/S, Gprof profiling); Tromp 8x8 solver (book88, <=16 ply); haithameleuch alpha-beta+MCTS hybrid; katac4 training pipeline fully decoded (self-play workers, 3 loss terms, 30K epochs); VERIFIED claims 50%--55%; 7 new sources (S032-S038); 6 new claims (C048-C053); ICAPS/JOCIG/Google Scholar all unworkable |
| 10 | 2026-08-02 | Complete | rowspire FULL source decoded (14 files): 4x128 MLP + skip connections (dual value+policy), 100D input (64-cell binary + 16 normalized features), 7-feature evaluation with genetic tuning, UCB1 MCTS (c=1.41, 4000 sims, NN-guided, Dirichlet root noise 75/25), 64-bit bitboard; training OPAQUE; eSlams evaluation framework discovered (50 arenas, REST protocol, Ed25519 proof); kenrick95/c4 (278 star) cataloged; Wikipedia opening theory confirmed; VERIFIED claims 55%--60%; 3 new sources (S039-S041) |
| 11 | 2026-08-02 | Complete | Pascal Pons/connect4 C++ solver fully decoded (negamax+PVS+TT+book; iterative binary search); TonyCWang/ConnectFour dataset (958M rows, 2x6x7 binary matrices, 7-element target vectors, exact solver evaluations); Hugging Face LLM-based Connect 4 model catalog (11+ models, all lacking metrics); evidence audit (17 structural issues fixed: duplicate sections, duplicate sources, stale headers); GitHub API unreachable (TLS/schannel error); VERIFIED claims 60%--66%; 9 new claims (C060-C068); 8 new sources (S042-S049) |
| 12 | 2026-08-02 | Complete | External-pool batch: 7/7 workers failed (DGX endpoint timeout, model-selection failure); no findings; DGX at 192.168.86.39:8006 unavailable since this round |
| 14 | 2026-08-02 | Complete | Batch-00002 reconciliation: both workers (worker-01, worker-05) already consumed in R13; no new findings; evidence gate verified |
| 15 | 2026-08-02 | Complete | External-pool batch: 7 worker results consumed |
| 16 | 2026-08-03 | Complete | GPU/Parallel Search + Corpus Audit: 7 sources (S059-S065), 7 claims (C078-C084). T011 VERIFIED. Key: Liang Li et al. 2012 Connect 6 GPU search 70.8x speedup; MCTS-NC Klens four GPU MCTS variants 75% avg score; Pascal Pons solver corrections (no PVS, static constexpr board sizes); rowspire training completeness verified (bin/train.rs entry point, core loop in rowspire_ai_core external crate); T014 Connect 4 engine ELO -- NEGATIVE RESULT (no formal multi-engine tournament ELO exists); Partial data: katac4 b3c128_v1 ~1080-->~1178 (self-comparison only). Corpus audit: R15 stat table recount fixed (VERIFIED 48-->51, SUPPORTED 8-->9, VERIFIED% 64%-->66%). R15 evidence gate violations (C006-C010, C026 -- Internal knowledge only) deferred to R17. |
| 16 | 2026-08-03 | Complete | Repository and Source Code Analysis (Slot 5): 5 new sources (S070-S074: BitBully MTD(f), ecc521 NNUE, neurofour benchmark, pyvezi bitboard, Karthick-Flutter). 11 new repos found via topic scan. 5 deep source code analyses. Zero-byte champion (search beats NN on tight budgets). Center-first ordering universal. C085-C089 (3 VERIFIED, 2 SUPPORTED). Classical Engine MEDIUM to MEDIUM-HIGH (Python bindings eliminate C++ binding complexity). |
| 18 | 2026-08-03 | Complete | MCTS Algorithms and Self-Play: 19 new verified claims (C083-C101). Three parallel agents: PUCT dominates MCTS selection (c_puct=1.0 train, 1.1 inference). FPU c_fpu=0.2 prevents NN policy domination. Adaptive CPUCT scales with visit variance. LCB move selection via t-distribution quantiles. PCR: 25% fast (16 sim) + 75% slow (800 sim). Solved game self-play convergence problem. Solver-distilled training (rowspire) more efficient than self-play. Pure MCTS smart rollouts: 55% vs depth-3 minimax. RMUUCT not applicable. Dirichlet alpha=0.8. Forced_k=2.0 child exploration. BEPb c_puct=5.0 highest. Multi-loss training (policy + 1.5*value + 0.15*opponent). Simulation speeds: Python 50-400, NN-Python 4000-10000, Rust WASM 20000-60000, GPU millions. |
| 17 | 2026-08-03 | Complete | R15 corpus audit corrections applied: C006-C010 and C026 downgraded from SUPPORTED to HYPOTHESIS (evidence gate violations -- Internal knowledge only, no published source). GPU inference bottleneck: NN inference negligible regardless of hardware; search tree is bottleneck; Numba JIT/bitboard optimization yields orders of magnitude more ROI than GPU inference. AlphaZero auxiliary loss paper (0.785 oracle match) identified as verification path. 12 workers across 4 slots all successful. |
| 19 | 2026-08-03 | Complete | OFFICIAL_KAGGLE_RULES_AND_COMPETITION Deep Source Analysis: 10 new VERIFIED claims (C102-C111), 10 new sources (S075-S084). Core findings: (1) Overtime enforcement from core.py line 631-632: per-step overage consumption via max(0, duration - actTimeout). (2) Agent timeout from agent.py line 220: per-call DeadlineExceeded() check. (3) UrlAgent timeout calc from agent.py line 89: remainingOverageTime + actTimeout + 1s grace. (4) Board is mutable single list across all steps -- no cloning. (5) maxLogLength: 10K chars per agent per step, ~20MB per episode. (6) Visualizer: Canvas-based TS renderer with cyan/white pieces, animated drop, win-line highlighting, step controls, JSON replay. (7) Deprecated environments: chess (Dockerfile), Lux AI s2 (dep conflict), LLM 20Q (gymnasium), tic-tac-toe (obsolete visualizer). (8) Agent signature autodetection: 1-arg or 2-arg both work via co_argcount. (9) Invalid move: board[column] != EMPTY check with 3 conditions, active agent = Invalid column status, inactive = DONE. (10) is_win has_played=False branch: lowest EMPTY row instead of just-placed mark row. Board is flat row-major, pieces: EMPTY=0, P1=1, P2=2. Play() drops to lowest empty row. CG-001, CG-002, CG-005 RESOLVED. T032, T005, T006, T051-T057 COMPLETE. VERIFIED 63-->66 (69%). |
| 19 | 2026-08-03 | Complete | External-pool batch (8 workers): 7×6 confirmed as only board with test evidence in kaggle-environments v1.32.2 (6 tests for 7×6, 8 for 4×5/inarow=3; 15×13/15×10 have ZERO evidence). obs.board is flat 1D array (not 2D). 3 opening book implementations decoded (tromp book88 ~500MB, Pascal Pons DEPTH=14, Kite 15-ply 95.6MB with 250,000× speedup). TonyCWang data generation corrected: uniform random + depth-18 solver (not self-play). C027/C028 downgraded HYPOTHESIS (evidence gate); C056 upgraded STRONGLY SUPPORTED (16 features fully decoded). No engine ELO exists. CG-001 RESOLVED. 7 new VERIFIED claims (C104-C106, C110-C113), 3 HYPOTHESIS (C107-C109). VERIFIED 66→68, STRONGLY SUPPORTED 2→3, SUPPORTED 4→5, HYPOTHESIS 19→22. |
| 20 | 2026-08-03 | Complete | NEURAL TRAINING AND HARDWARE (Lane 4): Neural network architecture comparison completed across 3 fully verified implementations (ResNet katac4 vs MLP rowspire vs CNN marcpaulo15). 5 new VERIFIED claims (C114-C117), 1 SUPPORTED (C118). Key: katac4 ResNet pre-activation with 2 bottleneck blocks (128 channels), 3-phase lambda scheduler, 30K epochs, 3 cross-entropy loss terms (policy+value+rival) - highest training completeness. Kaggle T4 GPU specs verified (2560 CUDA cores, 320 Turing TCs, 16GB GDDR6). GPU MCTS on GRID A100 achieves 20.3M playouts in 5s with 73.375% avg win rate - lock-free design. GPU inference estimates: NN inference 0.05-2ms on RTX 5090; Numba JIT/bitboard yield 10-100x more ROI than GPU inference acceleration. 3 new sources (S091-S093). VERIFIED 69->71. |
| 21 | 2026-08-03 | Complete | External-Pool Batch Synthesis (batch-00006): 13 workers dispatched. 7 produced usable findings (board representation comparison, MCTS variant analysis, adversarial corrections, corpus audit). 5 produced stale R16-R19 results. 1 API error (worker-04 job-4). 1 premature completion (worker-06 job-10). 2 new VERIFIED claims (C126: board representation comparison — 4 implementations documented; C127: NN-guided PUCT dominates MCTS, RMUUCT inapplicable). 6 claim corrections (C044/C047 → NEEDS_CORRECTION; C071 → NEEDS_CORRECTION; C092 → FALSIFIED; C097 → CORRECTED; C099 → UNVERIFIABLE). R20 sources S085-S090 already in ledger. No new R21 sources. VERIFIED 73 (C126, C127 added). |
| 22 | 2026-08-03 | Complete | T029 Connect 4 Engine Performance on Non-7x6 Boards: Complete board size matrix (4x4 to 11x11) from connect4.gamesolver.org. 8x8 solved as P2 win (Tromp, late 2014/2015, book88 ~500MB, column 4 universal P2 reply). 9x6 solved Nov 2005 (~2E13 positions, 2,000 CPU-hours). 10x8 is draw. 15x13/15x10 no results (HYPOTHESIS). Computational complexity O(R+C) disc placement, O(C*(R+C)) decision. Board representation scaling across 5 implementations. Claims C128-C134 added (6 VERIFIED, 1 HYPOTHESIS). VERIFIED 73-->79, HYPOTHESIS 22-->23. |
| 23 | 2026-08-03 | Complete | T017 Worker Result (batch-00008) -- External-Pool Batch Synthesis: Asymmetric eval source code verification -- QveenCoder (S050) and nguyenthequang (S051) both implement identical asymmetric window scoring: win:100K, near-win:100, opponent near-win:-120 (1.2x opponent threat amplification = proactive defense bias). C005 upgraded from SUPPORTED to VERIFIED (middle-column opening win confirmed by source code from 2 independent implementations). C059 reconfirmed VERIFIED. Wikipedia Connect Four page unchanged since R10 (15x13 solving status still unknown); infinite Connect-Four solved: Draw (new detail). Tromp board-size chart 4x4-11x11 already captured in R22. GitHub topic scans: no new repos since R21. "Winning moves never in central columns" pattern for larger boards. 1 new source (S094 Wikipedia). VERIFIED 79->80, SUPPORTED 5->4. |
| 24 | 2026-08-03 | Complete | External-Pool Batch (batch-00011): All 7 workers failed identically -- DGX endpoint (192.168.86.39:8006) unreachable. Slots 2 and 6 dispatched (jobs 12-14, 21-24). Same failure pattern since R12. No new findings, no new sources, no claim changes. DGX unavailable for 13th consecutive round. VERIFIED 80, unchanged. |
| 25 | 2026-08-03 | Complete | External-Pool Batch (batch-00012): 5/5 workers succeeded. 14 new VERIFIED claims (C143-C154), 7 new SUPPORTED claims (C155-C158, C165-C166), 2 NEW CLAIMS (C160-C163 from Neural worker). Key: (1) C110 REFUTED — S044 directly contradicts claim about TonyCWang dataset ("NOT self-play" vs S044 "Self-play with temperature sampling"). (2) C128-C131 downgraded NEEDS_CORRECTION — gamesolver.org does not contain board-size matrix data; source attribution fails. (3) C134 downgraded SUPPORTED — O-notation correct derivation but no explicit source. (4) kaggle-environments v1.32.3: mark field added, deprecated_envs removed, test_connectx.py removed. (5) ResNet (katac4) fully specified: b3c128nbt, 3 Bottlenest blocks, 128 channels, ~530K params. (6) T4 TensorRT FP16: 1.10ms ResNet-18, sub-1ms for target sizes. (7) 14 new sources (S091-S096, S099-S108). VERIFIED 80→79 (C110→REFUTED, C128-C131→NEEDS_CORRECTION, C134→SUPPORTED, but +18 new VERIFIED). |
| 30 | 2026-08-04 | Complete | External-Pool Batch (batch-00016): 5/5 workers succeeded. Key: (1) C139 upgraded HYPOTHESIS→VERIFIED (adjacent opening draw unidentifiable by MCTS). (2) C136/C007/C150 downgraded NEEDS_CORRECTION (source ID collision R24/R25 overlap). (3) HYP-014 added (MCTS timing governance requirement). (4) ENS-013/014/015 added (3 new ensembles). (5) R30 source collision audit: 8 IDs (S094-S097, S101-S102) used by both R23/R24 and R25 batches. R31: C177-C179/C181 VERIFIED (GPU MCTS benchmark, CPU MCTS overflow); C180 HYPOTHESIS (ensemble arbitration required for 3+ components). All MCTS ensembles require GPU on Kaggle T4. ENS-018 added (TT-MCTS shared cache). Total claims: 181 (C001-C181). Total hypotheses: 17 (HYP-001-HYP-017). VERIFIED: 72 (63%). NEEDS_CORRECTION: 18 (17%). |
| 31 | 2026-08-04 | Complete | External-Pool Batch (ENS/HYBRID lane): Timing budget audit for all MCTS-containing ensembles. C177-VERIFIED (MCTS-NC ~2.5M playouts/s on T4 GPU). C178-VERIFIED (CPU MCTS 1600-4000 sims overflow 2s budget). C179-VERIFIED (all inference-time MCTS ensembles require GPU). C180-HYPOTHESIS (ensemble arbitration protocol required for 3+ component ensembles). C181-VERIFIED (ENS-013/015 alpha-beta-only are timing-safe on CPU). HYP-015 (MCTS GPU acceleration requirement). HYP-016 (CPU fallback degradation). HYP-017 (TT-MCTS shared cache). Total claims: 181 (C001-C181). Total hypotheses: 17 (HYP-001-HYP-017). VERIFIED: 73 (63%). NEEDS_CORRECTION: 18 (17%). |
| 31 | 2026-08-04 | Complete | Ensemble & Hybrid Audit: MCTS timing budget analysis confirmed all MCTS-enabling ensembles require GPU acceleration on Kaggle T4. Added ENS-018 (TT-MCTS shared cache). Formalized ensemble arbitration protocol. Key claims: C177-C181 (4 VERIFIED, 1 HYPOTHESIS). Key hypotheses: HYP-015 through HYP-017 (3 new). GPU acceleration is now a hard architectural constraint for all MCTS ensembles. |
| 32 | 2026-08-04 | Complete | External-Pool Batch (batch-00017): 13/13 workers succeeded across all 7 lanes. Key: (1) C139 HYPOTHESIS→VERIFIED (adjacent opening draw, 3 independent sources). (2) HYP-003 LOW→MEDIUM confidence. (3) Tromp fhourstones88 complete search system fully analyzed: NO MTD(f), NO PVS, standard full-window alpha-beta (C006/C007 NEEDS_CORRECTION). (4) Kamide/connect-n new engine: adaptive scoring minimax in Web Worker. (5) miksipiksic/pyvezi: bitmask board representation. (6) 5 adversarial review workers confirm source ID namespace collision (8+ IDs). (7) Benchmark specification: 19 opponents, 6 tiers, Elo 0–1900. (8) Corpus hygiene: 5 structural defects found. C184–C199 added (VERIFIED). New sources S123–S126. New contenders BOT-013/BOT-014. Total claims: ~195. Total hypotheses: 17. VERIFIED: 79 (64%). NEEDS_CORRECTION: 20. |
| 33 | 2026-08-04 | Complete | External-Pool Batch (batch-00018): 9/9 workers succeeded across 3 lanes (corpus governance, timing audit, benchmark science). Key: (1) Source ID collision audit: 4 clusters (S091-S093 R16/R25, S094-S097 R23/R25, S109-S117 R25/R30, S118-S120 R30 self-duplicate). (2) Fabricated data: S117 (40-40-20 phase distribution invented), S120 ("uniform random" methodology fabricated — actual: self-play with temperature schedule). (3) arXiv:1203.2285 verified as astrophysics paper (not game theory MCP theorem). (4) Benchmark blueprint completed: 12 suites (BMS-001 through BMS-012). (5) 3 new hypotheses: HYP-018 (phase-bias in self-play), HYP-019 (source attribution integrity), HYP-020 (fabricated data detection). (6) C151→NEEDS_CORRECTION, C172→NEEDS_CORRECTION, C136 updated. (7) 7 new experiments EXP-026 through EXP-032. Total claims: ~200. Total hypotheses: 20 (HYP-001 through HYP-020). VERIFIED: ~74. NEEDS_CORRECTION: 22. |
| 34 | 2026-08-04 | Complete | External-Pool Batch (batch-00019): 17/17 workers across 7 lanes. Key: (1) C200-VERIFIED (neural MCTS 0.849 oracle match benchmark), C201-VERIFIED (AZAL three-loss objective), C202-VERIFIED (TensorRT INT8 3-5x latency reduction), C205-VERIFIED (DQN tactical weakness). (2) C132/C175/C176/C195 updated: MTD(f) hypothesis, PVS hypothesis, MCTS MCP theorem hypothesis, NN depth hypothesis. (3) C203-HYPOTHESIS (board-size adaptive routing), C204-HYPOTHESIS (phase-boundary calibration). (4) 4 new hypotheses: HYP-021 (board-size routing), HYP-022 (phase-boundary calibration), HYP-023 (TensorRT INT8 advantage), HYP-024 (NNUE vs DQN tactical). (5) 6 governance issues identified: source ID collision rate ~10%, fabricated data mechanism, MCTS MCP citation broken, header inconsistency, broken MCP citation, governance tasks. (6) Board-size solving: 8x8 P2 win, 9x6 solvable, 10x8 draw. Total claims: 205. Total hypotheses: 24 (HYP-001 through HYP-024). VERIFIED: 86. NEEDS_CORRECTION: 22. |
| 35 | 2026-08-04 | Complete | First V10 dossier synthesis: NEXUS.md corpus index created (first hierarchical index). Dossier hierarchy established: 11 directories (3 pre-existing empty, 8 newly created). GOV-001 governance audit dossier created: 22 structural defects (4 CRITICAL, 8 HIGH, 6 MEDIUM, 4 LOW) verified across entire corpus. 10 new governance claims (C206–C215) all VERIFIED. Source ledger updated: S121–S126 added (4 missing from R32), S117/S120 marked [RETRACTED], S127 (Artho MCP) added as corrected citation. Work queue: 78 governance tasks defined (FU-052 through FU-078). Claim count: 215 (C001–C215). VERIFIED: 96 (45%). NEEDS_CORRECTION: 22. |
| 36 | 2026-08-04 | Complete | External-pool batch-00002 synthesis: 2 new dossiers created (MCTS-001 on MCTS consistency problem, BMS-DOC-001 on benchmark science and tournament design), 1 duplicate governance dossier removed (GOV-R34-001 merged back into GOV-001). 2 workers rejected (one produced .js file, one produced no output). Dossiers now: 3 (GOV-001, MCTS-001, BMS-DOC-001). Corpus governance defects remain active (source ID collisions, fabricated data S117/S120, broken arXiv:1203.2285 citation). MCTS dossier recommends HYP-008 PROPOSED→STRONGLY SUPPORTED, C175 HYPOTHESIS→STRONGLY SUPPORTED. D-CBL-001 (contender baseline dossier) deferred to next batch. |
| 37 | 2026-08-05 | Complete | External-pool batch-00096 synthesis: 3 substantive dossiers created (MCTS-002 neural integration patterns, D-034 new reference sources, CS-003 classical search/solver engineering), 1 governance audit expanded (GOV-004 comprehensive corpus audit). 3 thin outputs rejected. Source count: 127→131 (S128-S131). Claim count: 215→225 (C216-C225). Dossiers now: 9 across 9 directories. Governance remediation rate: 14% (R35) → 41% (R36) → 55% (R37). Three new benchmark requirements added (BMS-011 through BMS-013). |
| 38 | 2026-08-05 | Complete | Phase 1 — Governance gap repair: NEXUS.md dossier index (9->14), RESEARCH_REPORT.md header (225->222 claims, 9->14 dossiers), claim-register header (C001-C215->C001-C222, 215->222 total), benchmark-blueprint header (R35->R37). Added MCTS-003 and RI-001 to NEXUS index. 6 remaining governance gaps identified (source ID collisions, fabricated data, empty directories, thin rejected file, header-vs-body count drift, legacy file cleanup). Phase 2 — Batch-00097 total rejection: all 8 workers failed (4: Write tool unavailable, 4: no output produced). 0 new dossiers, 0 new claims, 0 new sources. Dossiers: 14 (unchanged from uncommitted R38 changes). Governance remediation: 55% (unchanged). |
| 39 | 2026-08-05 | Complete | Phase 1 — NN-001 dossier: neural network architectures dossier (654 lines, 18 sources, feasibility matrix, board-size applicability). Neural directory no longer empty. Dossiers: 15 across 13 directories (2 empty: ensembles, training-data). Phase 2 — mcts-004 rejected (thin, executive summary only). Batch-00098: 13 workers dispatched, 1 substantive dossier accepted (NN-001). Governance remediation at 55%. |
| 40 | 2026-08-05 | Complete | Batch-00099 synthesis: 3 new substantive dossiers created (CS-004: search algorithm comparison, 761 lines; RI-001: katac4 reference implementation, 771 lines; MCTS-003 expanded: 8 variant taxonomy, 607 lines). 18 workers dispatched; 9 passed, 9 failed (Write tool unavailable: 4, no output: 2, infrastructure issues: 3). Self-corrections: C006/C007 NEEDS_CORRECTION (no MTD(f)/PVS in Tromp/Pascal Pons), C047 NEEDS_CORRECTION (Dirichlet 75/25 unverified). Dossiers: 17 across 11 directories (2 empty: ensembles, training-data). Governance remediation at 55% (unchanged). |
| 41 | 2026-08-05 | Complete | Batch-00100 synthesis: 6 new substantive dossiers created (NN-001: neural architectures, 786 lines; CS-001: opening book engineering, 591 lines; CS-002: board representation and move generation, 718 lines; CS-003: classical search algorithm engineering, 795 lines; MCTS-004: MCTS deployment architecture, 632 lines; DOS-006: contender deep profiles, substantive). 22 workers dispatched across 7 lanes; 22/22 exit code 0 (Write tool fully restored). Dossiers: 24 across 12 directories (2 empty: ensembles, training-data). Governance remediation at 55%.
| 42 | 2026-08-05 | Complete | Batch-00101 synthesis: 1 new dossier (MCTS-005: hybrid search systems, 680 lines, ~35KB, 4 core mechanisms verified across katac4/connectpuct/rowspire/MCTS-NC), 2 expansions (NN-002: NNUE source decode 7x6/8x8 with incremental accumulator, 84x speedup; BMS-DOC-002: MCP theorem depth added). 8 workers dispatched across 7 lanes; 3 wrote dossiers (NN-002, BMS-DOC-002, MCTS-005), 3 produced governance findings (233 total: FU-001–FU-088, FU-101–FU-109, ~36 additional), 2 failed to write (Write tool unavailable: CS-005, RI-002). Source ID collision cluster E detected (S132-S139 cross-batch collision, HIGH risk). Dossiers: 25 across 12 directories (2 empty: ensembles, training-data). Governance findings: 262+. New experiments: EXP-NN-001–005, EXP-TS-001–004, BMS-016–021.
| 43 | 2026-08-05 | Complete | NN-002 expanded (NNUE decode, ResNet, inference optimization), MCTS-005 created, CBL-001 comprehensive contender analysis created, DOS-007 Kaggle competitive analysis created, BMS-DOC-003 ensemble benchmarking created, 3 test files archived, source collision cluster E remediation (S136-S141→S142-S146). Dossiers: 31 across 12 directories (3 empty: ensembles, training-data, kaggle). Governance findings: FU-001–FU-109+.
---

## Tool Availability

| Tool | Status | Notes |
|------|--------|-------|
| WebSearch | Broken | API error 400 since iteration 5 |
| WebFetch | Working | Single-page lookups only; used extensively in R19 for source analysis |
| Bash/Glob/Read | Working | Repository inspection |
| Agent sub-agents | Working | Cannot use WebSearch (same API error) |

---

## Leading Architecture

**Hybrid Neural + Classical Search** (confidence: HIGH)

Combined with game-phase strategy:
- Opening (0-12 pieces): Tablebook / NN policy
- Midgame (12-34 pieces): Alpha-beta / PVS search
- Endgame (>34 pieces): Solved database lookup

---

## Active Hypotheses

| ID | Status | Last Reviewed |
|----|--------|---------------|
| H1 | PENDING | Round 5 |
| H2 | PENDING | Round 5 |
| H3 | PENDING | Round 5 |
| HYP-015 | PROPOSED | R37 |
| HYP-016 | PROPOSED | R37 |
| HYP-017 | PROPOSED | R37 |
| HYP-018 | PROPOSED | R37 |
| HYP-019 | PROPOSED | R37 |
| HYP-020 | PROPOSED | R37 |
| HYP-021 | PROPOSED | R37 |
| HYP-022 | PROPOSED | R37 |
| HYP-023 | PROPOSED | R37 |
| HYP-024 | PROPOSED | R37 |

---

## Dossier Statistics

| Category | Count | Description |
|----------|-------|-------------|
| Total dossiers | 31 | Across 12 directories |
| Governance | 4 | GOV-001 through GOV-004 |
| MCTS | 5 | MCTS-001 through MCTS-005 |
| Classical Search | 5 | CS-001 through CS-004, board-representation-and-move-generation |
| Foundations | 1 | Board representation and win detection |
| Benchmarking | 3 | BMS-DOC-001, BMS-DOC-002, BMS-DOC-003 |
| Contenders | 5 | D-CBL-001, DOS-006, DOS-007, CBL-001, contender-roster entries |
| Neural | 2 | NN-001, NN-002 |
| Reference | 2 | D-034, RI-001 |
| Empty directories | 3 | ensembles, training-data, kaggle |

---

## Key Findings

- 7×6 is solved: first player wins by move 41
- 8×8 is solved: second player wins
- 9×6 is solved: first player wins
- 10×8 is solved: draw
- 15×13 and 15×10: unsolved (LOW confidence)
- Neural MCTS 0.849 oracle match (C200)
- TensorRT INT8 provides 3-5x latency reduction (C202)
- DQN shows tactical weakness vs alpha-beta (C205)
- 5 source ID collision clusters (30+ IDs, Cluster E includes S130–S146)
- S117 and S120 confirmed fabricated
- NN-002 NNUE decode: 7x6 (21,761 params, ~87 KB), 8x8 (45,057 params, ~180 KB), ~84x incremental speedup
- 31 dossiers across 12 directories; 146+ sources; 24 hypotheses; 24 ensembles; 16 contenders
- Governance remediation at 55% (12/22 GOV-001 findings)
- NN-003: Temperature decay formula corrected from T=1.0 to T=0.5 to katac4 formula max(1.03, 1.35*pow(0.66, step/bs)); 8 new sources (S150-S157)

---

*Last updated: 2026-08-05 16:00 ET (Round 43)*
