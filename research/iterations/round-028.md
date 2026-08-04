# Round 28 — External-Pool Batch Synthesis (batch-00009)

> **Round**: 28
> **Date**: 2026-08-04
> **Batch**: batch-00009-20260804-061439
> **Prior Round**: 27 (v9 corpus migration)
> **Model**: qwen3.6

---

## Executive Summary

Round 28 processes **17 worker results** from external-pool batch-00009. Workers span 6 slots (01-07) with 4 lanes: ensemble/hybrid hypotheses, neural MCTS training, adversarial review/corpus audit, governance/corpus hygiene, classical search, and benchmark science.

**Key findings**:
1. **9 new sources added** (S109-S117): NeuralConnect4, Gemu03, katac4 full source, AZAL paper, rowspire curriculum distillation, MCTS-NC GPU, TonyCWang dataset card, spooky-connect4, sml-connect4
2. **2 new claims** (C173: AZAL mechanism SUPPORTED, C174: AZAL 0.785 oracle match rate VERIFIED)
3. **3 corpus corrections**: C144-C145 reinstated VERIFIED, C136 downgraded VERIFIED→SUPPORTED
4. **2 new hypotheses** (HYP-009: Three-Loss Objective Superiority, HYP-010: Temperature Schedule Threshold)
5. **7 new experiments** (EXP-009 through EXP-015): three-loss ablation, temperature schedule, AZAL training, mixing ratio, NeuralConnect4 vs katac4, Gemu03 hybrid validation, MCTS consistency budget
6. **Total experiments**: 15 (EXP-001 through EXP-015), 14 SPECIFIED, 1 BLOCKED

---

## Worker Results

### Worker 1 — Corpus Governance (Jobs 1-2)

**Findings**:
- Claim register integrity crisis: header counts don't match detail rows
- Claim ID collision: C167-C170 used by both R26 (GitHub topics scan) and R27 (board representation)
- Research-state.md shows 3 rounds stale (R25-R27 not in table)
- Recommendation: implement source ID namespace isolation (EXP-008)

**Corrections applied**: None from W01 (R27 already applied these)

### Worker 2 — Baseline Contenders (Job 2)

**Findings**:
- 45 baseline opponents cataloged across 6 categories
- 2 new repos: NeuralConnect4 (ha22yx), Gemu03 (search+RL hybrid)
- Source IDs: S109-S113 (NeuralConnect4, Gemu03, connectx.json deprecation, local pyproject.toml, sml-connect4)

**New sources**: S109-S113 ✓ added to ledger

### Worker 3 — Classical Search (Job 2)

**Findings**:
- T022 (board representation comparison) marked COMPLETE
- No new claims or sources from this worker

### Worker 4 — Neural MCTS Training (Jobs 1-2)

**Findings**:
- 4 training paradigms synthesized with completeness ranking
- AZAL paper (arXiv 2607.08984) fully analyzed: 0.785 oracle match rate
- Three-loss objective: policy CE + 1.5× value CE + 0.15× rival CE
- 80/20 NN policy prior mixing at MCTS root (pi_combined = 0.8 * pi_NN + 0.2 * uniform)
- 16 parallel self-play workers, replay buffer decoupling
- Temperature schedule: T=1.0 for first 10 moves, T=0.5 for remaining

**New sources**: S114-S117 ✓ added to ledger
**New claims**: C173 (AZAL mechanism), C174 (AZAL 0.785 oracle match) ✓ added
**New hypotheses**: HYP-009, HYP-010 ✓ added
**New experiments**: EXP-009 through EXP-015 ✓ added

### Worker 5 — Ensemble/Hybrid Hypotheses (Jobs 1, 3, 4)

**Findings**:
- Conservative ensemble: Classical-first with neural tie-breaker
- High-ceiling ensemble: Two-stage training → hybrid runtime
- 7 ensemble specifications generated
- Board-size routing: 7x6 (classical), 8x8+ (neural-guided MCTS)

**Status**: W05 job-4 incomplete (387 chars before termination)

### Worker 6 — Benchmark Science (Jobs 1-2)

**Findings**:
- Tournament design methodology
- Insufficient progress for new claims/sources

### Worker 7 — Adversarial Review (Jobs 1-4)

**Findings**:
- 24-51 claims audited per job across the corpus
- C001 confirmed VERIFIED (Wikipedia independently confirms solved game)
- C006-C010 need evidence gate review
- C136 Althöfer MCP citation lost (theory real but citation incorrect) → SUPPORTED

---

## Corpus Corrections

### C144/C145 Reinstatement

R26 incorrectly downgraded C144 (katac4 ResNet architecture) and C145 (katac4 training pipeline) from NEEDS_CORRECTION. W04 independently verified S091 (katac4 model.py) and S092 (katac4 train.py) — both sources match R25 descriptions.

**Action**: C144 → VERIFIED (reinstated), C145 → VERIFIED (reinstated)

### C136 Citation Correction

R27 correctly identified that the arXiv citation for Althöfer's Monte Carlo Perfectness paper (arXiv:1203.2285) is wrong (it is astrophysics). The theoretical result about MCP is real but the citation is lost.

**Action**: C136 → SUPPORTED (not VERIFIED, per R27)

### C174 New VERIFIED Claim

The AZAL paper's abstract (arXiv 2607.08984) confirms 0.785 oracle match rate on Connect Four. This is a direct, verifiable finding.

**Action**: C174 → VERIFIED

---

## New Sources

| Source ID | Title | Type | Notes |
|-----------|-------|------|-------|
| S109 | ha22yx/NeuralConnect4 — AlphaZero-style pipeline | Source code | Second AZ-style pipeline for Connect 4 |
| S110 | gemu03/connect4 — Search + RL hybrid | Kaggle submission | Search + RL hybrid approach |
| S111 | katac4 full source (model.py, train.py, mcts.py, explorer_main.py) | Source code | Complete AlphaZero-style pipeline |
| S112 | Arunesh-Tanwar/Connect-Four-Game — Classical search | Source code | Classical baseline |
| S113 | spooky2008/connect4 — Halloween Connect 4 bot | Source code | Classical search alternative |
| S114 | AZAL arXiv 2607.08984 — Oracle consistency | Academic paper | Auxiliary cross-entropy loss training |
| S115 | rowspire curriculum distillation details | Source code | 50-epoch SFT, 250K samples, mirroring |
| S116 | MCTS-NC GPU parallel MCTS (numba.cuda) | Source code | 20.3M playouts/5s on GRID A100 |
| S117 | TonyCWang dataset card — generation methodology | Dataset card | Uniform random + depth-18 solver targets |

---

## New Claims

| Claim ID | Claim | Status | Sources |
|----------|-------|--------|---------|
| C173 | AZAL auxiliary loss mechanism: policy heads learn from value targets during self-play | SUPPORTED | S114 |
| C174 | AZAL paper confirms 0.785 oracle match rate on Connect Four | VERIFIED | S114 |

---

## New Hypotheses

### HYP-009: Three-Loss Objective Superiority

**Status**: PROPOSED
**Evidence for**: C153 VERIFIED (katac4 three-loss), C145 VERIFIED (training pipeline)
**Evidence against**: The 0.15× rival CE weight may be too small to produce a meaningful difference
**Falsification**: Two-loss model achieves ≥95% of three-loss win rate
**Confidence**: LOW

### HYP-010: Temperature Schedule Threshold Optimality

**Status**: PROPOSED
**Evidence for**: C151 VERIFIED (TonyCWang T=1.0→0.5 schedule), S117 (dataset card)
**Evidence against**: The move-count boundary is board-size dependent; may not generalize
**Falsification**: T=1.0 for first 5 moves achieves ≥95% of T=1.0 for 10 moves policy accuracy
**Confidence**: LOW

---

## New Ensembles

No new ensembles from this batch. Existing ensembles (ENS-001 through ENS-006) already cover the key design space. W05's ensemble specifications (EN-001 through EN-007) were consolidated into existing ENS entries.

---

## Future Experiments

7 new experiments added (EXP-009 through EXP-015):

| ID | Purpose | Status |
|----|---------|--------|
| EXP-009 | Three-loss vs two-loss objective ablation | SPECIFIED |
| EXP-010 | Temperature schedule comparison (5/10/20/all moves) | SPECIFIED |
| EXP-011 | AZAL auxiliary loss on self-play | SPECIFIED |
| EXP-012 | 80/20 policy prior mixing ratio verification | SPECIFIED |
| EXP-013 | NeuralConnect4 vs katac4 training comparison | SPECIFIED |
| EXP-014 | Gemu03 Search+RL hybrid validation | SPECIFIED |
| EXP-015 | MCTS consistency budget analysis | SPECIFIED |

**Total experiments**: 15 (EXP-001 through EXP-015), 14 SPECIFIED, 1 BLOCKED

---

## Claim Status Changes

| Action | Claim IDs | Rationale |
|--------|-----------|-----------|
| REINSTATE VERIFIED | C144, C145 | R26 incorrectly downgraded; S091/S092 sources verified |
| DOWNGRADE VERIFIED→SUPPORTED | C136 | Althöfer MCP citation lost; theory real but citation incorrect |
| ADD VERIFIED | C174 | AZAL 0.785 oracle match rate verified from arXiv abstract |
| ADD SUPPORTED | C173 | AZAL mechanism (policy heads learn from value targets) |

**Net VERIFIED change**: +1 (C174), but C144/C145 reinstated were already VERIFIED in detail rows but listed as NEEDS_CORRECTION in header — no net change in VERIFIED count from reinstatement, only header correction.

---

## Benchmark-Blueprint Changes

- EXP-012 (80/20 mixing ratio) adds BMS-010 (ablation) test case for root expansion strategies
- EXP-015 (MCTS consistency budget) adds BMS-004 (fixed-opponent paired) test case for simulation count analysis

---

## Research-Queue Changes

- T022 (board representation comparison) marked COMPLETE
- 7 new follow-up research tasks from W04 findings
- No new tasks added to work-queue (all captured in experiment backlog)

---

## Corpus Hygiene

1. **Claim register header**: Updated to reflect R28 corrections (C171-C172 in VERIFIED, C173 in SUPPORTED, C174 in VERIFIED)
2. **Source ledger**: Added S109-S117 (9 new sources)
3. **Hypothesis register**: Updated total from 8 to 10, added HYP-009 and HYP-010 details
4. **Experiment backlog**: Updated total from 8 to 15, added EXP-009 through EXP-015 details
5. **Research-state**: Updated current round to 28, added R28 entry, updated claim statistics
6. **README**: Updated current round to 28, added round-028 entry

---

## Rejected Worker Results

- **W05 job-4**: Incomplete (387 characters, terminated early) — no findings
- **W06 job-2**: Minimal progress — no new claims or sources

---

## Next Round Focus Areas

1. **AZAL full-text analysis** — arXiv 2607.08984 abstract verified but full methodology not accessible; determine if auxiliary loss implementation exists on GitHub
2. **NeuralConnect4 source analysis** — ha22yx pipeline details (training objective, MCTS parameters) not yet fully specified
3. **Gemu03 Search+RL hybrid** — understand the specific search and RL components before EXP-014 execution
4. **Temperature schedule boundary** — investigate whether move-count boundary (10) generalizes to larger boards
4. **EXP-015 MCTS consistency** — determine simulation count threshold for ≥90% oracle agreement on 7x6
5. **DGX connectivity** — DGX endpoint (192.168.86.39:8006) unavailable for 14 consecutive rounds

---

*Round 28 complete. 17 workers processed, 9 new sources, 2 new claims, 2 corpus corrections, 2 new hypotheses, 7 new experiments. Total VERIFIED: 75. Total hypotheses: 10. Total experiments: 15.*