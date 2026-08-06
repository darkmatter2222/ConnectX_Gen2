# Research Program — ConnectX Bot v9

> **Program Lead**: ConnectX External Research Pool
> **Current Round**: 44
> **Last Updated**: 2026-08-05
> **Prior State**: Round 43 (NN-002 expanded, MCTS-005, CBL-001, DOS-007, BMS-DOC-003 committed; NN-003, CS-005, MCTS-007, KAGGLE-CONNX-SPEC added; governance 73%)
> **Status**: Active deep research synthesis; 29 substantive dossiers across 12 directories, 5 source collision clusters, governance remediation 75%

---

## 1. Objective and Scope

Build the world's best Kaggle ConnectX bot through iterative, evidence-driven research.

This program operates in the **research-only phase**: we collect and verify evidence, generate falsifiable hypotheses, synthesize compatible components into explicit ensemble concepts, maintain a research-priority leaderboard of ideas, catalog future benchmark contenders, design a comprehensive future benchmark ladder, and preserve a clean canonical corpus.

All implementation, empirical execution, benchmarking, training, and inference are **deferred** to a later implementation phase.

**Scope**: ConnectX (Connect 4 on variable board sizes, default 7x6, inarow 4). Primary target: Kaggle competition environment (2s/move, 60s overtime, arbitrary board sizes, flat 1D array board representation).

---

## 2. Research-Only Boundary

This program operates under a strict research-only boundary:

- **Allowed**: Create or modify `.md` repository files only
- **Prohibited**:
  - Creating or executing bot or application source code
  - Scripts, notebooks, tests, or benchmark programs
  - Simulations, tournaments, or training/inference programs
  - Datasets, model weights, or binaries
  - Downloading or installing external packages or repositories
  - Running any repository code, games, tournaments, tests, benchmarks, or simulations

**Shell use is limited to**: read-only repository inspection, Git operations for committed Markdown, and bounded read-only public-source retrieval.

---

## 3. Evidence Hierarchy

| Tier | Standard | Example |
|------|----------|---------|
| **Tier 1: Authoritative Primary** | Peer-reviewed paper, official specification, direct source code inspection | Tromp 8x8 solver source code; Althöfer 2012 MCP theorem; kaggle-environments connectx.py source |
| **Tier 2: Two Independently Credible** | Two genuinely independent sources confirming the same fact | QveenCoder and nguyenthequang both implement identical asymmetric eval values |
| **Tier 3: Single Credible** | One credible source with strong methodology | Wikipedia article with citations; Hugging Face dataset card |
| **Tier 4: Not Evidence** | Model memory, speculation, unverified claims | "MTD(f) gives 20-30% speedup" without source code or published benchmark |

**Evidence gate rules**:
- Model memory is NOT evidence
- No ordinal performance ranking without direct measurement
- No strength inference from stars or implementation complexity
- No source-code existence as proof of competitive strength
- No combining copied or derivative sources as independent confirmation
- No silent conversion of estimates into facts
- No unsupported exact numbers
- Explicit applicability and comparability limits required
- Distinguish between fact and inference

---

## 4. Canonical Identifiers

| Prefix | Type | Example | File |
|--------|------|---------|------|
| C### | Claim | C148: katac4 ResNet architecture | claim-register.md |
| S### | Source | S029: connectpuct PUCT engine | source-ledger.md |
| HYP-### | Hypothesis | HYP-001: Conservative Ensemble | hypothesis-register.md |
| CMP-### | Component | CMP-001: Solved-Game Tablebook | component-catalog.md |
| ENS-### | Ensemble | ENS-001: Solved-Game + Alpha-Beta | ensemble-catalog.md |
| BOT-### | Contender | BOT-003: katac4 | contender-roster.md |
| BMS-### | Benchmark Suite | BMS-001: API, legality, deterministic replay | benchmark-blueprint.md |
| EXP-### | Experiment | EXP-001: Conservative vs Warm-Start MCTS | future-experiment-backlog.md |
| FR-### | Follow-up Research | FR-001: Re-verify Althöfer MCP theorem | round report |

---

## 5. Hypothesis Lifecycle

```
PROPOSED → RESEARCHING → PLAUSIBLE → EVIDENCE_SUPPORTED → CONTESTED / REJECTED / DEFERRED_EMPIRICAL
```

Each hypothesis must be:
- **Falsifiable**: explicit falsification condition with measurable criteria
- **Component-distinguished**: evidence for individual components separated from evidence for combinations
- **Scope-bounded**: board-size and game-phase scope explicitly stated

**Status definitions**:
- **PROPOSED**: Reasoned hypothesis, components have evidence, combination untested
- **RESEARCHING**: Actively being validated through literature review or analysis
- **PLAUSIBLE**: Components verified, combination mechanism theoretically sound, needs empirical test
- **EVIDENCE_SUPPORTED**: Falsification attempts exhausted; combination confirmed by evidence
- **CONTESTED**: Evidence supports contrary claim; hypothesis under review
- **REJECTED**: Falsified or proven inapplicable
- **DEFERRED_EMPIRICAL**: Requires empirical test that cannot be performed in research-only phase

---

## 6. Ensemble-Generation Protocol

Every substantive synthesis should produce:

1. **Conservative ensemble**: Only well-supported (VERIFIED) components
2. **High-ceiling ensemble**: Includes plausible advanced (HYPOTHESIS/PLAUSIBLE) components
3. **Simplicity ensemble**: Minimal resource-constrained variant
4. **Adversarial alternative**: Challenges the current leader directly

**Integration requirements for each ensemble**:
- Member component IDs
- Routing or arbitration mechanism
- Game-phase and board-size gates
- Confidence or tactical gates
- Resource allocation per component
- Expected synergy (with evidence for each member + evidence for combination
- Missing evidence
- Likely failure modes
- Complexity cost
- Benchmark requirements
- Linked hypothesis IDs

Ensembles are **hypotheses**, not recommendations. They define testable combinations of components that should be empirically validated before adoption.

---

## 7. Contender-Selection Protocol

No contender enters a top-strength tier based solely on:
- GitHub star count or repository popularity
- Source-code sophistication or language choice
- Implementation complexity

Contenders must have:
- **Published result evidence** (measured performance, not claims)
- **Availability** (source code, weights, or deployment accessible)
- **Reproducibility** (others can reproduce results)
- **Resource requirements** (compute, memory, time)

Contenders are classified as:
- **Benchmark candidate**: A system to measure against
- **Component candidate**: A technique or architecture to reuse

---

## 8. Benchmark-Design Protocol

Future benchmarks must define 12 suites (BMS-001 through BMS-012):

| Suite | Focus |
|-------|-------|
| BMS-001 | API, legality, and deterministic replay |
| BMS-002 | Tactical position suite |
| BMS-003 | 7x6 solver-oracle agreement |
| BMS-004 | Fixed-opponent paired matches |
| BMS-005 | Multi-contender round robin |
| BMS-006 | Adversarial and exploitability suite |
| BMS-007 | Multi-board and inarow generalization |
| BMS-008 | Timeout, latency, memory, and submission-size constraints |
| BMS-009 | Stochastic stability and seed sensitivity |
| BMS-010 | Ablation and component attribution |
| BMS-011 | Kaggle-environment emulation |
| BMS-012 | Regression and promotion gates |

**Metrics**: win/draw/loss, seat-adjusted score, Elo/Glicko/TrueSkill, Wilson confidence intervals, effect size, invalid-move rate, timeout rate, tactical solve rate, oracle agreement, latency p50/p95/p99, node throughput, memory/package size, reproducibility, ablation deltas, promotion/rejection criteria.

---

## 9. Corpus-Hygiene Rules

- **No invented sources**: Every source must be a real, verifiable entity with URL or path
- **No source-code existence as proof of strength**: Code exists does not mean it is competitive
- **No silent evidence conversion**: Estimates remain estimates; facts remain facts
- **Explicit ID namespace isolation**: Each round should use distinct source IDs to prevent cross-round confusion
- **Forward references prohibited**: Do not reference rounds that have not yet been completed
- **Statistical reconciliation**: Claim counts must be reconciled across all canonical files each round

---

## 10. Transition Criteria: Research → Implementation

The research phase ends and implementation begins when ALL of the following are met:

1. **PRIME hypotheses** (top 3 by research score) have EVIDENCE_SUPPORTED status
2. **Key ensemble** has been validated through planned benchmarks
3. **Evidence gap** is below acceptable threshold (fewer than 3 NEEDS_CORRECTION on critical components)
4. **Benchmark blueprint** is complete and executable
5. **Future experiment backlog** is specified with all prerequisite research complete

Until then: research only. No implementation.

---

## 11. Unresolved Decision Gates

| Gate | Status | Description |
|------|--------|-------------|
| DG-001 | OPEN | Source ID namespace isolation — S094-S098, S101-S102 overwritten, making R25 claims unreliable |
| DG-002 | OPEN | Claim reconciliation — research-state.md (80V) vs claim-register.md header (73V) discrepancy |
| DG-003 | OPEN | C139 validation — adjacent opening = draw? Critical for ENS-003 and HYP-003 |
| DG-004 | OPEN | Optimal phase boundary — 14 pieces for solved-game → search transition? |
| DG-005 | OPEN | MCP theorem applicability — is Connect 4 a Monte Carlo Perfect game? |
| DG-006 | OPEN | Transfer learning viability — 7x6→15x13 NN generalization? |

---

## 12. Current Corpus State (End of Round 26)

- **Total claims**: 166 (C001-C166 with gaps from ID reuse)
- **VERIFIED**: 73 (C001, C005, C020-C024, C031-C043, C048-C057, C059, C060-C070, C072-C077, C078-C091, C093, C102-C106, C111-C113, C114-C117, C119-C122, C124-C127, C133-C140, C142-C143)
- **STRONGLY SUPPORTED**: 3 (C016, C025, C056)
- **SUPPORTED**: ~11 (C012, C019, C123, C136-C138, C140, C155-C159, C165-C166)
- **HYPOTHESIS**: ~12 (C006-C011, C013-C015, C017-C018, C026-C029, C071, C107-C109, C132)
- **NEEDS_CORRECTION**: 10 (C006, C007, C010, C044, C047, C144, C145, C150, C151, C154, C162)
- **FALSIFIED**: 1 (C092)
- **CORRECTED**: 1 (C097)
- **UNVERIFIABLE**: 1 (C099)
- **REFUTED**: 1 (C110)
- **DISPUTED**: 1 (C058)

**Key research gap identified in R26**: MCTS consistency problem — no MCTS implementation uses solved-game knowledge (C135), and Althöfer's Monte Carlo Perfectness theorem suggests MCTS may not converge to correct values for Connect 4 (C136, C142).

**Leading architecture**: Hybrid Neural + Classical Search (confidence: HIGH)

**Important note**: Research rankings in this program are NOT empirical playing-strength rankings. They are research-priority assessments of evidence maturity.

---

*Research Program v9 — Active. Next round: Round 27 (ensemble validation research planning, source ID namespace isolation, claim reconciliation).*