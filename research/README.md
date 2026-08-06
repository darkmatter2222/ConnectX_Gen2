# Research Repository — ConnectX Bot

> **Current Round**: 48
> **Goal**: Build the world's best Kaggle ConnectX bot through iterative research

---

## Canonical Files (authoritative)

| File | Purpose |
|------|---------|
| `research-state.md` | Current research state, round tracking, tool availability, priority gaps |
| `research-trajectory.md` | Research plan, knowledge gaps, trajectory, iteration log |
| `final-conclusion.md` | Evolving final conclusion about what architecture to build |
| `claim-register.md` | All material claims with status, evidence grade, source |
| `architecture-rankings.md` | Ranked approaches with confidence scores |
| `decision-log.md` | Architecture, tool, and strategy decisions with evolution |
| `source-ledger.md` | All research sources: primary, secondary, verified, unverified |
| `research-gaps.md` | Knowledge gap catalog with priority and resolution status |
| `research-program.md` | Research program framework, evidence hierarchy, hypothesis lifecycle, ensemble protocol |
| `NEXUS.md` | Corpus-level index: cross-link map, source collision map, fabricated data ledger, dossier index |
| `hypothesis-register.md` | All hypotheses with full lifecycle records (HYP-001 through HYP-024) |
| `idea-leaderboard.md` | Research-priority leaderboard with 0-5 scoring system |
| `component-catalog.md` | Reusable component catalog with compatibility matrix (CMP-001 through CMP-010) |
| `ensemble-catalog.md` | Ensemble catalog with comparison table (E-001 through E-012, ENS-013 through ENS-024) |
| `contender-roster.md` | Contender roster with classification (BOT-001 through BOT-016) |
| `benchmark-blueprint.md` | Benchmark design with 12 specified suites (BMS-001 through BMS-012) |
| `future-experiment-backlog.md` | Future experiment backlog with full specifications (EXP-001 through EXP-032) |

## Round Reports

| File | Round | Date | Summary |
|------|-------|------|---------|
| `iterations/round-001.md` | 1 | 2026-07-30 | Initial deep research audit — compendium created |
| `iterations/round-002.md` | 2 | 2026-07-30 | Web research, agent parallel — 5+ new docs |
| `iterations/round-003.md` | 3 | 2026-07-30 | Kaggle analysis, new repos |
| `iterations/round-004.md` | 4 | 2026-07-31 | GPU, MCTS, game theory, bots, search |
| `iterations/round-005.md` | 5 | 2026-08-02 | Game-phase, endgame, benchmarks, eval |
| `iterations/round-006.md` | 6 | 2026-08-02 | GitHub topics discovery; AlphaZero (blanyal 92★) fully analyzed; bitboard agent catalog; canonical files created |
| `iterations/round-007.md` | 7 | 2026-08-02 | GoodCoder666/katac4 (KataGo-inspired AlphaZero) fully analyzed; Wikipedia confirms solved game |
| `iterations/round-008.md` | 8 | 2026-08-02 | PUCT MCTS benchmark (11/20 vs minimax); rowspire neural MCTS + bitboard solver (Rust+WASM); Java bitboard solver |
| `iterations/round-009.md` | 9 | 2026-08-02 | Tromp Fhourstones benchmark (20 systems, KPOS/S); Tromp 8x8 solver (book88 ≤16 ply); katac4 full training pipeline; katac4 ResNet KataGo techniques; alpha-beta+MCTS hybrid; VERIFIED 55% |
| `iterations/round-010.md` | 10 | 2026-08-02 | rowspire FULL source decoded (14 files): 4×128 MLP, dual value+policy, 100D input, 7-feature eval, UCB1 MCTS; eSlams framework; kenrick95/c4; Wikipedia opening theory; VERIFIED 60% |
| `iterations/round-011.md` | 11 | 2026-08-02 | Pascal Pons C++ solver fully decoded (negamax+PVS+TT+book); TonyCWang 958M-row training dataset (board-state, exact solver targets); Hugging Face LLM catalog (11+ models); evidence audit (17 fixes: duplicates, stale headers); Supervised Pre-training + Search approach added; VERIFIED 60%→66% |
| `iterations/round-012.md` | 12 | 2026-08-02 | External-pool batch: 7/7 workers failed (DGX endpoint timeout, model-selection failure); no findings |
| `iterations/round-013.md` | 13 | 2026-08-02 | Kaggle kaggle-environments spec fully analyzed (global config schema, agentTimeout removal); 5 new JS/TS/Python engine eval benchmarks decoded; VERIFIED 67%; 5 new sources (S049–S055), 4 new claims (C069–C072); C025 → STRONGLY SUPPORTED |
| `iterations/round-014.md` | 14 | 2026-08-02 | Batch-00002 reconciliation: both workers (worker-01, worker-05) already consumed in R13; no new findings |
| `iterations/round-022.md` | 22 | 2026-08-03 | T029 Connect 4 Engine Performance on Non-7x6 Boards: Complete board size matrix (4x4 to 11x11); 8x8 solved P2 win; 9x6 solved; 10x8 draw; 15x13/15x10 no results |
| `iterations/round-023.md` | 23 | 2026-08-03 | T017 Worker Result (batch-00008): Asymmetric eval source code verification (QveenCoder S050, nguyenthequang S051); C005 upgraded to VERIFIED; 120/100 opponent-threat amplification (1.2x proactive defense bias) |
| `iterations/round-025.md` | 25 | 2026-08-03 | External-Pool Batch (batch-00012): 5/5 workers succeeded. 14 new VERIFIED claims (C143-C154). Key: C110 REFUTED... C128-C131 NEEDS_CORRECTION... C134 SUPPORTED... kaggle v1.32.3: mark field added, test_connectx.py removed... ResNet (katac4) fully specified... T4 TensorRT FP16 1.10ms... 14 new sources. |
| `iterations/round-026.md` | 26 | 2026-08-03 | Corpus audit: R25 source ID mismatch (S094-S098, S101-S102 overwritten), claim status inconsistencies, C001 upgraded to VERIFIED, C006-C010/C144-C162 downgraded to NEEDS_CORRECTION |
| `iterations/round-027.md` | 27 | 2026-08-03 | v9 corpus migration: 7 new canonical files; governance deep-dive: C171 agentTimeout deprecation, C172 version discrepancy, T121 remainingOverageTime behavior verified; 3 worker results (ensemble hypotheses, corpus audit, governance)
| `iterations/round-028.md` | 28 | 2026-08-04 | External-Pool Batch (batch-00009): 17 workers (ensemble, neural MCTS training, adversarial review, governance). 9 new sources (S109-S117: NeuralConnect4, Gemu03, katac4, AZAL, rowspire, MCTS-NC, TonyCWang card). 2 new claims: C173 (AZAL mechanism), C174 (AZAL 0.785 oracle match, VERIFIED). Corpus corrections: C144-C145 reinstated VERIFIED, C136 VERIFIED→SUPPORTED. 2 new hypotheses: HYP-009 (three-loss superiority), HYP-010 (temperature schedule). 7 new experiments (EXP-009 through EXP-015). |
| `iterations/round-030.md` | 30 | 2026-08-04 | External-Pool Batch (batch-00016): 5 workers (MCTS consistency, adversarial audit, ensemble hypotheses, corpus governance). C139 VERIFIED (adjacent opening draw unidentifiable by MCTS). 3 new sources (S118-S120), 1 new hypothesis (HYP-014 timing governance), 3 new ensembles (ENS-013/014/015), 2 new benchmarks (BMS-005 MCTS consistency, BMS-006 board-size coverage), 3 new experiments (EXP-016/017/018), 1 new contender (BOT-010), 8 source ID collisions identified (R23/R24 vs R25). Experiment count: 15→18. |
| `iterations/round-031.md` | 31 | 2026-08-04 | MCTS timing budget audit + ensemble arbitration. C177-C181 added (MCTS timing). HYP-015/016/017 added (GPU acceleration, CPU fallback, TT-MCTS). ENS-018 added (TT-MCTS shared cache). |
| `iterations/round-032.md` | 32 | 2026-08-04 | External-Pool Batch (batch-00017): 13/13 workers. C139 VERIFIED (adjacent opening draw, 3 independent sources). C184-C199 VERIFIED (Kamide engine, Tromp search system). C193-C194 NEEDS_CORRECTION (no MTD(f)/PVS). HYP-003 → MEDIUM. New sources S123-S126. New contenders BOT-013/BOT-014. Benchmark: 19 opponents, 6 tiers. 5 adversarial reviews confirm source ID collision. |
| `iterations/round-033.md` | 33 | 2026-08-04 | External-Pool Batch (batch-00018): 9/9 workers. Source ID collision audit (4 clusters, 27+ IDs). Fabricated data: S117 (40-40-20 phase distribution), S120 ("uniform random" fabricated). arXiv:1203.2285 = astrophysics (not MCP theorem). Benchmark blueprint: 12 suites (BMS-001-BMS-012). 3 new hypotheses: HYP-018 (phase-bias), HYP-019 (source attribution), HYP-020 (fabrication detection). C151→NEEDS_CORRECTION, C172→NEEDS_CORRECTION. 7 new experiments EXP-026-EXP-032. |
| `iterations/round-034.md` | 34 | 2026-08-04 | External-Pool Batch (batch-00019): 17/17 workers across 7 lanes. C200-C202/C205 VERIFIED (neural MCTS benchmarks). 4 new hypotheses (HYP-021-HYP-024: board-size routing, phase-boundary, TensorRT, NNUE). 6 new ensembles (ENS-019-ENS-024). 2 new contenders (BOT-015/BOT-016). 6 governance issues. Board-size solving matrix confirmed. |
| `iterations/round-035.md` | 35 | 2026-08-04 | First V10 dossier synthesis: NEXUS.md corpus index created. 11 dossier directories (3 empty, 8 newly created). GOV-001 governance audit dossier: 22 structural defects (4 CRITICAL, 8 HIGH, 6 MEDIUM, 4 LOW). 10 new governance claims (C206-C215) VERIFIED. Source ledger updated (S121-S126 added, S117/S120 [RETRACTED], S127 corrected citation). 5 new governance experiments (EXP-033-EXP-037). |
| `iterations/round-036.md` | 36 | 2026-08-04 | External-pool batch-00002 synthesis: 2 new dossiers created (MCTS-001 on MCTS consistency problem, BMS-DOC-001 on benchmark science). 1 duplicate governance dossier removed. 2 workers rejected (one produced .js, one produced no output). Total dossiers: 3 (GOV-001, MCTS-001, BMS-DOC-001). |
| `iterations/round-037.md` | 37 | 2026-08-05 | External-pool batch-00096 synthesis: 3 new dossiers (MCTS-002 neural MCTS integration, D-034 new reference sources, CS-003 classical search/solver engineering). 1 governance audit expanded (GOV-004 comprehensive corpus audit). 5 thin outputs rejected. Total dossiers: 9. Claims: 215→225. Sources: 127→131. Governance remediation: 55%. |
| `iterations/round-038.md` | 38 | 2026-08-05 | Phase 1 — Governance gap repair: NEXUS.md dossier index (9→14), RESEARCH_REPORT.md header (225→222 claims, 9→14 dossiers), claim-register header (C001-C215→C001-C222, 215→222 total), benchmark-blueprint header (R35→R37). MCTS-003 and RI-001 added to NEXUS index. Phase 2 — Batch-00097 total rejection: all 8 workers failed (4: Write tool unavailable, 4: no output). 0 new dossiers/claims/sources. Dossiers: 14 (unchanged). Governance remediation: 55% (unchanged). |
| `iterations/round-039.md` | 39 | 2026-08-05 | Batch-00098 synthesis: 1 new dossier (NN-001 neural networks — 654 lines, 18 sources, 5 code samples, feasibility matrix). 1 thin rejected (mcts-004, 1,480 bytes). Neural directory populated. Dossiers: 15. Empty dirs: 2 (ensembles, training-data). All canonical files updated by workers. |
| `iterations/round-040.md` | 40 | 2026-08-05 | Batch-00099 synthesis: 3 new dossiers (CS-004 search algorithm comparison 761 lines; RI-001 katac4 reference 771 lines; MCTS-003 variant taxonomy 607 lines). 18 workers dispatched, 9 passed, 9 failed. Dossiers: 17 across 11 directories. |
| `iterations/round-041.md` | 41 | 2026-08-05 | Batch-00100 synthesis: 6 new dossiers (NN-001 neural architectures 786 lines; CS-001 opening book engineering 591 lines; CS-002 board representation 718 lines; CS-003 search algorithm engineering 795 lines; MCTS-004 deployment architecture 632 lines; DOS-006 contender deep profiles). 22 workers dispatched, 22/22 exit code 0. Dossiers: 24 across 12 directories. |
| `iterations/round-043.md` | 43 | 2026-08-05 | NN-002 expanded, MCTS-005 created, CBL-001, DOS-007, BMS-DOC-003, governance findings FU-001–FU-109+ |
| `iterations/round-044.md` | 44 | 2026-08-05 | NN-002 expanded (NNUE 7x6/8x8 source decode), MCTS-005 hybrid search, CBL-001, DOS-007, BMS-DOC-003. 20+ experiments deferred. Governance remediation 68% (GOV-005). |
| `iterations/round-045.md` | 45 | 2026-08-05 | 1 new governance dossier (GOV-007 R43→R44 post-commit audit, VERIFIED). 7 pre-existing dossiers validated (NN-003, MCTS-007, KAGGLE-CONNX-SPEC, CS-005, bms-doc-004, bms-doc-005, GOV-005, GOV-006). Remediation 73%→75%. 3 test artifacts introduced. 5 unindexed files. |
| `iterations/round-046.md` | 46 | 2026-08-05 | 2 new substantive dossiers (NN-004 transfer learning ~37 KB, CON-001 new contenders ~37 KB). 6 dossiers expanded/validated. Governance remediation plateaus at 75% (6 rounds). 1 missing write (BMS-DOC-007). NN-004 source overlap with S160-S165 needs de-duplication. R20+ jobs from 7 workers. |
| `iterations/round-047.md` | 47 | 2026-08-05 | 2 new dossiers (MCTS-008 rollout strategy, bms-doc-007 statistical methodology) + 1 missing write (Kamide). NN-004 expanded (12 new sources S158-S169, board-size generalization). CS-005 expanded (adaptive scoring). Governance at 100% plateau. NEW Cluster F source collision (S158-S169 overlap RI-002/NN-004/Kamide). 7 NEXUS index gaps. |
| `iterations/round-048.md` | 48 | 2026-08-06 | 2 new substantive dossiers (NN-005 model compression ~31 KB, RI-007 3 new ref impls ~27 KB). NN-005: pruning, quantization, distillation, 10 new sources S174-S183. RI-007: Tarun995 Python bitboard, jesper-olsen Rust solver, haithameleuch Kotlin hybrid. NEW Cluster G collision (S174-S176 overlap RI-007/NN-005). Governance plateau at 100%. Dossier quota NOT met (2/3). Kamade still not persisted. Worker-02 produced empty file. 3 collision clusters (E, F, G). |

## Legacy Documents (evidence, preserved)

| File | Topic | Created |
|------|-------|---------|
| `00-comprehensive-report.md` | Initial comprehensive report | 2026-07-28 |
| `01-game-mechanics.md` | Game rules, board layout | 2026-07-28 |
| `02-connect4-ai-pipeline.md` | AI pipeline deep dive | 2026-07-28 |
| `03-deep-research-compendium.md` | Deep research compendium | 2026-07-30 |
| `04-environment-observations.md` | Live env inspection | 2026-07-28 |
| `05-bot-agent-interface-submission-format.md` | Agent interface docs | 2026-07-29 |
| `06-package-api-deep-dive.md` | Kaggle API deep dive | 2026-07-30 |
| `evaluation-function-design.md` | Eval features and weights | 2026-07-30 |
| `nn-architecture-research.md` | NN architecture | 2026-07-30 |
| `training-data-generation.md` | Training data strategies | 2026-07-30 |
| `neural_network_architectures_connectx.md` | NN hyperparameters, RTX timeline | 2026-07-30 |
| `transfer-learning-research.md` | Transfer learning findings | 2026-07-30 |
| `transfer-learning-domain-adaptation-connectx.md` | 7x6→15x13 transfer analysis | 2026-07-30 |
| `alpha_beta_optimizations_connect4.md` | Alpha-beta optimizations | 2026-07-30 |
| `gpu-research.md` | GPU hardware research | 2026-07-30 |
| `mcts-research.md` | MCTS research | 2026-07-30 |
| `advanced-search-research.md` | Advanced search research | 2026-07-30 |
| `opening-book-research.md` | Opening book research | 2026-07-30 |
| `gpu-research-iteration4.md` | GPU opportunities: inference, training, hybrid | 2026-07-31 |
| `mcts-research-iteration4.md` | MCTS variants: UCT, RAVE, Neural MCTS | 2026-07-31 |
| `game-theory-iteration4.md` | 7x6 SOLVED, opening book design, game transfer | 2026-07-31 |
| `open-source-bots-iteration4.md` | 10 repos cataloged | 2026-07-31 |
| `advanced-search-iteration4.md` | MTD(f), PVS, LMR, killer, JIT | 2026-07-31 |
| `iteration-2-findings.md` | Iteration 2 findings | 2026-07-30 |
| `iteration-3-findings.md` | Iteration 3 findings | 2026-07-30 |
| `iteration-4-findings.md` | Iteration 4 findings | 2026-07-31 |
| `iteration-5-findings.md` | Iteration 5 findings | 2026-08-02 |
| `benchmark_alpha_beta.py` | Alpha-beta benchmark script | 2026-07-30 |

## Test Files (evidence, preserved)

Test files from early development iterations (not executed):
`test_board_layout.py`, `test_bug.py`, `test_bug2.py`, `test_clean.py`, `test_final.py`, `test_full_game.py`, `test_renderer.py`, `test_win_trace.py`

---

## Research Summary

**Current Leading Approach**: Hybrid Neural + Classical Search (confidence: HIGH)

**Key Knowns**:
- 7x6 Connect 4 is SOLVED (first player wins from center)
- RTX 5090 available: 21,760 CUDA cores, 32GB GDDR7
- Kaggle: 2s/move, 60s overtime, arbitrary board sizes
- Game-phase strategy: Opening (book) → Midgame (search) → Endgame (tablebase)

**Key Unknowns**:
- Current Kaggle leaderboard (web search broken)
- Empirical benchmarks (NN training, inference speed)
- 15x13 first-player advantage
- Optimal NN architecture for ConnectX

**Tool Status**: WebSearch broken (Round 5+), WebFetch works, Bash/Read/Glob work
