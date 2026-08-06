# Round 49 — ConnectX Research Nexus Synthesis

> **Batch**: batch-00108-20260806-022912
> **Date**: 2026-08-06
> **Hopper Target**: 70
> **Previous Round**: 48 (commit 8be6b2a)
> **Current Round**: 49

## Batch Overview

6 worker result files consumed from batch-00108:
- Worker-06, Job 619: Slot 6, BENCHMARK_SCIENCE (23:06-23:43)
- Worker-05, Job 594: Slot 5, CONTENDERS_BASELINES (23:28-23:51)
- Worker-06, Job 620: Slot 6, BENCHMARK_SCIENCE (23:43-00:13)
- Worker-01, Job 592: Slot 1, SOURCE_DOSSIERS (21:40-00:55)
- Worker-06, Job 621: Slot 6, BENCHMARK_SCIENCE (00:20-01:34)
- Worker-04, Job 644: Slot 4, MCTS_AND_HYBRID_SYSTEMS (22:44-01:34)

## Worker Results

| Worker | Job | Lane | Result | Files Produced |
|--------|-----|------|--------|---------------|
| Worker-05 | 594 | CONTENDERS_BASELINES | **ACCEPTED** | CB-001 expanded (+179 lines) |
| Worker-01 | 592 | SOURCE_DOSSIERS | **ACCEPTED** | CS-006 new (589 lines) |
| Worker-06 | 619 | BENCHMARK_SCIENCE | **PARTIAL ACCEPT** | BMS-DOC-008 created (372 lines) |
| Worker-06 | 620 | BENCHMARK_SCIENCE | **PARTIAL ACCEPT** | BMS-DOC-008 duplicate (same as 619) |
| Worker-06 | 621 | BENCHMARK_SCIENCE | **REJECTED** | Write tool unavailable |
| Worker-04 | 644 | MCTS_AND_HYBRID_SYSTEMS | **REJECTED** | MCTS-008 already in R48 commit |

## Dossiers Created

### CS-006: Move Ordering and Search Optimization

- **Path**: `research/dossiers/classical-search/CS-006-move-ordering-and-search-optimization.md`
- **Size**: 589 lines, ~34 KB
- **Sections**: 20 (hierarchy, implementation patterns, speedup analysis, pruning, board-size adaptability, ensemble integration, failure modes, feasibility matrix, benchmark requirements, open questions, recommendations, sources, cross-links)
- **Primary Sources**: S124 (Tromp), S030 (rowspire), S123 (Kamide), S050 (QveenCoder), S052 (ariaborin)
- **Total Sources**: 16 with direct URLs
- **Code Samples**: 2 adapted reference sketches + 2 conceptual pseudocode blocks
- **Key Verifications**: C008 (center-first 3-5x), C009 (full hierarchy 10-30x), C033 (Numba JIT)
- **Status**: PROPOSED

### BMS-DOC-008: Board-Size Generalization Benchmark Protocol

- **Path**: `research/dossiers/benchmarking/BMS-DOC-008-board-size-generalization-benchmark-protocol.md`
- **Size**: 634 lines after synthesis repair (original: 372 lines)
- **Sections**: 16 (executive summary, significance, source map, position sets, opponent selection, evaluation criteria, statistical methodology, resource-constrained evaluation, failure modes, performance evidence, board-size applicability, integration opportunities, pros/cons, feasibility matrix, sources, cross-links)
- **Primary Sources**: S005 (Kaggle spec), S006 (Kaggle interpreter), S077 (Kaggle docs), S079 (test_connectx.py)
- **Total Sources**: 15 primary + 4 theoretical references with direct URLs
- **Synthesis Repair**: Added source table with direct URLs (§15) and cross-links (§16) to meet dossier quality requirements
- **Status**: PROPOSED

## Dossiers Expanded

### CB-001: Kaggle Official Builtin Agents
- **Delta**: +179 lines, -31 lines (net +173)
- **Additions**: marcpaulo15/RL-connect4 PPO hyperparameters (buffer=2000, C1=0.75, C2=0.04, lr=1e-4, 320 iterations), Widnyana/connect4 TensorFlow Pure Neural architecture, two-head policy+value details, PPO beats 1-step lookahead 84% of time

### GOV-009: Governance Master Report
- **Delta**: +275 lines, -114 lines (net +161)
- **Additions**: P0 milestone (5/5 P0 test artifacts deleted), CS-005 8x expansion, Cluster F identification, remediation plateau analysis (75% across R44-R46)

## Source Collisions

No new source ID collisions introduced in R49. All new source IDs verified against the existing ledger.

7 collision clusters persist (A-G, 41+ IDs affected):
- **Cluster A**: S091-S093 (katac4 / TensorRT)
- **Cluster B**: S094-S097 (Tromp methodology)
- **Cluster C**: S109-S117 (NeuralConnect4 / Gemu03 / AZAL — S117 fabricated)
- **Cluster D**: S118-S120 (connectpuct benchmark)
- **Cluster E**: S130-S146 (NN-003/NN-004 overlap)
- **Cluster F**: S158-S169 (NN-004/RI-002/Kamide overlap) — 7 rounds unresolved
- **Cluster G**: S174-S176 (NN-005/RI-007 overlap) — 1 round unresolved

## Leaderboards Updated

- **Technique leaderboard**: CS-006 adds "Move ordering hierarchy" (ranked by evidence maturity, board coverage, Kaggle feasibility)
- **Benchmark leaderboard**: BMS-DOC-008 adds board-size generalization protocol (BMS-B001 through BMS-B016 implied)

## Future Experiments

- **BMS-C001 through BMS-C007** (from CS-006): Move ordering hierarchy benchmarks
  - BMS-C001: Move ordering hierarchy win rate vs sequential
  - BMS-C002: TT hit rate vs table size
  - BMS-C003: Killer heuristic depth gain
  - BMS-C004: History heuristic depth gain
  - BMS-C005: Center-first adaptivity across board sizes
  - BMS-C006: Fork detection effectiveness
  - BMS-C007: Quiescence search blunder rate

- **BMS-B001 through BMS-B016** (from BMS-DOC-008): Board-size benchmark protocol
  - T1: Position suite (910 positions across 8 board sizes)
  - T2: Opening play (720 games)
  - T3: Midgame strength (600 games)
  - T4: Endgame quality (23K positions)
  - T5: Transfer learning measurement (3 experiments)

## Files Changed

| File | Action | Delta |
|------|--------|-------|
| RESEARCH_REPORT.md | Modified | +76 (R49 changes section, header/footer update) |
| research/NEXUS.md | Modified | +15 (R49 header, corpus stats, R49 changes section) |
| research/README.md | Modified | +2 (R49 round report entry) |
| research/dossiers/classical-search/CS-006-move-ordering-and-search-optimization.md | New | +589 lines |
| research/dossiers/benchmarking/BMS-DOC-008-board-size-generalization-benchmark-protocol.md | New + Repair | +634 lines (372 + 262 repair) |
| research/dossiers/contenders/CB-001-kaggle-official-builtin-agents.md | Expanded | +179, -31 |
| research/dossiers/governance/GOV-009-R46-master-governance-report-and-gap-repair.md | Expanded | +275, -114 |
| research/iterations/round-049.md | New | This file |

## Next Research Targets

1. **Cluster F/G remediation**: Source ID re-indexing for NN-004 (S158-S169→S166-S177) and RI-007 (S174-S183)
2. **BMS-C001 through BMS-C007**: Execute move ordering hierarchy benchmarks
3. **BMS-B001 through BMS-B016**: Execute board-size generalization benchmark protocol
4. **15×13 solving**: No solver exists for 15×13 — priority research gap
5. **Neural-guided move ordering**: Investigate neural policy injection into classical move ordering (§11.1 of CS-006)
6. **NN-only fallback for 15×13**: Validate that NN-only inference <50ms on Kaggle CPU

---

*Round 49 synthesis complete. 2 new dossiers, 2 expanded, 7 files changed. Dossier quota met (4 substantive changes). Governance plateau continues. 7 collision clusters persist.*