# Round 35 — ConnectX Research Program

**Batch ID**: batch-00001-20260804-211421
**Date**: 2026-08-04
**Workers Consumed**: 1 (slot 7, job 52, lane NEXUS_GOVERNANCE_MASTER_REPORT_AND_GAP_REPAIR)
**Workers Rejected**: 0
**Previous Round**: 34 (neural MCTS benchmarks, 4 new hypotheses, 6 new ensembles)

---

## Executive Summary

Round 35 marks the **first V10 dossier synthesis** in the ConnectX research program. After 34 rounds of iterative claim extraction, source ledger maintenance, and governance audits, the corpus finally has:

1. A **hierarchical index** (NEXUS.md) linking all claims, sources, hypotheses, ensembles, and contenders
2. A **dossier hierarchy** with 11 directories (3 pre-existing empty, 8 newly created)
3. The **first substantive dossier** (GOV-001) — a 22-finding governance audit
4. **10 new VERIFIED governance claims** (C206–C215) documenting corpus structural defects
5. **Source ledger repairs**: S121–S126 added, S117/S120 [RETRACTED], S127 corrected citation
6. **RESEARCH_REPORT.md complete rewrite** incorporating all R30–R35 findings

---

## Worker Result

### Slot 7 (NEXUS_GOVERNANCE_MASTER_REPORT_AND_GAP_REPAIR)

- **worker-07-job-00052**: Complete corpus governance audit producing GOV-001 dossier
- **Exit code**: 0 (success)
- **Model**: qwen3.6
- **Duration**: ~25 minutes (1.5s API, 23 turns, 1M+ input tokens, 8.8K output tokens)

**Accepted findings**: All 22 governance findings accepted as VERIFIED.

**Dossier created**: `research/dossiers/governance/GOV-001-corpus-governance-audit-round-34.md`

---

## Corpus Corrections

### New Claims (10 VERIFIED)

| Claim | Title | Status |
|-------|-------|--------|
| C206 | Source ID collision rate ~10% (4 clusters, 27+ IDs) | VERIFIED |
| C207 | Fabricated data persistence in source ledger | VERIFIED |
| C208 | Master report staleness (6 days, 5 rounds) | VERIFIED |
| C209 | Missing NEXUS.md corpus index | VERIFIED |
| C210 | Empty/missing dossier directories (11 dirs, 0% completion) | VERIFIED |
| C211 | Benchmark blueprint section numbering errors | VERIFIED |
| C212 | Legacy file proliferation (~30 untracked files) | VERIFIED |
| C213 | README.md round report gaps (24/34 listed) | VERIFIED |
| C214 | Header-body inconsistency across canonical files | VERIFIED |
| C215 | 15×13 board-size source persistence error (LOW since R1) | VERIFIED |

### Source Ledger Updates

| Source ID | Action | Details |
|-----------|--------|---------|
| S121 | Added | Kamide/connect-n — adaptive scoring minimax |
| S122 | Added | Kamide/connect-n — Web Worker deployment |
| S123 | Added | Kamide/connect-n — full source analysis |
| S124 | Added | Tromp fhourstones88 — complete search system |
| S125 | Added | miksipiksic/pyvezi — bitmask minimax |
| S126 | Added | Pascal Pons/search.cpp — negamax reference |
| S117 | [RETRACTED] | Fabricated 40-40-20 phase distribution |
| S120 (first) | [RETRACTED] | Fabricated "uniform random" methodology |
| S127 | Added | Artho MCP theorem — corrected citation |

---

## Files Changed

| File | Action | Summary |
|------|--------|---------|
| `RESEARCH_REPORT.md` | **Rewritten** | Complete rewrite incorporating R30–R35 findings; new sections: board-size solving matrix, data governance, technique leaderboard, proven/supported table |
| `research/README.md` | Updated | R35 round report entry; NEXUS.md added to canonical files |
| `research/NEXUS.md` | **NEW** | Corpus-level hierarchical index with cross-link map, collision ledger, dossier index |
| `research/dossiers/governance/` | Created | New dossier directory |
| `research/dossiers/governance/GOV-001.md` | **NEW** | First substantive dossier — 22-finding governance audit |
| `research/claim-register.md` | Updated | C206–C215 added (10 VERIFIED); header statistics updated to 215 claims, 96 VERIFIED |
| `research/source-ledger.md` | Updated | S121–S127 added; S117/S120 [RETRACTED]; Retraction Ledger and Sources Added Round 35 sections |
| `research/research-state.md` | Updated | R35 round entry; Governance Status section with 22 findings (4 CRITICAL, 8 HIGH, 6 MEDIUM, 4 LOW) |

---

## Governance Findings Summary

**GOV-001 identified 22 structural defects across the corpus:**

| Severity | Count | Primary Defects |
|----------|-------|-----------------|
| CRITICAL | 4 | Source ID collisions (27+ IDs), fabricated data persistence, broken MCP citation, source ledger incompleteness |
| HIGH | 8 | Master report staleness, header inconsistency, missing NEXUS.md, empty/missing dossier dirs, benchmark numbering |
| MEDIUM | 6 | Legacy proliferation, claim status discrepancy, iteration gaps, ledger header stale, queue fragmentation, contention |
| LOW | 4 | Ensemble cross-reference gaps, experiment-ensemble orphaning, hypothesis terminology, board-size source persistence |

**Remediation status (R35):**
- DONE: S117/S120 [RETRACTED] flags added
- DONE: NEXUS.md created
- DONE: Dossier directories created
- PENDING (R36): Source ID collision resolution (4 clusters, 27+ IDs)
- PENDING (R36): Benchmark blueprint section numbering fix
- PENDING (R36): arXiv:1203.2285 replacement
- PENDING (R37): Header reconciliation across canonical files
- PENDING (R37): Legacy file audit and categorization

---

## Next Research Targets

1. **Source ID collision resolution** (CRITICAL) — 4 clusters, 27+ IDs need unique assignment
2. **Contender dossiers** (HIGH) — 16 contenders (BOT-001 through BOT-016), 0 dossiers
3. **Classical search dossiers** (HIGH) — kamade, tromp, pyvezi, Pascal Pons engines
4. **Neural architecture dossiers** (HIGH) — katac4, rowspire, NeuralConnect4, MCTS-NC
5. **Governance automation** (MEDIUM) — automated fabrication detection (EXP-035)
6. **Board-size solving experiment** (MEDIUM) — 15×13 first-player unknown since R1

---

*End of Round 35 Report.*