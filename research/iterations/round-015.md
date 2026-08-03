# Round 15 — ConnectX External-Pool Batch Synthesis

> **Date**: 2026-08-02
> **Batch**: batch-00003-20260802-223936
> **Source**: External-pool worker results (7 workers)
> **Status**: Complete — synthesis applied

---

## Worker Summary

| Worker | Job | Result | Key Activity |
|--------|-----|--------|--------------|
| worker-06 | job-00003 | ✅ SUCCESS | Kaggle kaggle-environments config deep analysis (schemas.json, connectx.json, core.py) — full spec decoded |
| worker-07 | job-00004 | ✅ SUCCESS | JS/TS/Python engine eval function benchmarks — 5 new eval scoreboards decoded |
| worker-07 | job-00005 | ✅ SUCCESS | rowspire full source code audit — training algorithm decoded via corpus audit |
| worker-01 | job-00002 | ❌ FAIL | DGX endpoint timeout (192.168.86.39:8006) |
| worker-03 | job-00001 | ❌ FAIL | Model-selection error |
| worker-06 | job-00003 (dup) | ❌ FAIL | DGX endpoint timeout (192.168.86.39:8006) |
| worker-07 | job-00005 (dup) | ❌ FAIL | Model-selection error |

**Result**: 3/7 succeeded. 4/7 failed (2x DGX timeout, 2x model-selection). Workers that succeeded provide actionable findings.

---

## Key Findings

### 1. Kaggle Overtime Tracking Mechanism (VERIFIED)

**Source**: kaggle-environments core.py, connectx.json, schemas.json
**Claims**: C073-C074

- `remainingOverageTime` decrements by `max(0, duration - actTimeout)` per step
- Below 0 → TIMEOUT disqualification
- ConnectX overrides: actTimeout=2, remainingOverageTime=60
- Global schema: actTimeout=6, runTimeout=1200, episodeSteps=1000
- agentTimeout=60 is obsolete (removed from spec)

### 2. Agent Status Enum (VERIFIED)

**Source**: kaggle-environments core.py
**Claim**: C075

- Enum: ACTIVE, INACTIVE, DONE, ERROR, INVALID, TIMEOUT
- All documented in interpreter
- Required for proper agent state management

### 3. kaggle-environments Version (VERIFIED)

**Source**: pyproject.toml
**Claim**: C076

- Package version: v1.32.2
- Python ≥3.11 required
- Determines available Python features and API surface

### 4. Observation.step Field (VERIFIED)

**Source**: core.py
**Claim**: C077

- Observation.step field available in current spec
- deprecated_envs/ directory removed from current version

### 5. rowspire Training Fully Decoded (C058 REFUTED)

**Source**: tre-systems/rowspire full source code (corpus audit R15)

**Previous status**: VERIFIED (opaque — npm run train invokes un-publish code)
**New status**: REFUTED — training mechanism fully decoded

**Decoded training algorithm**:
- 50-epoch supervised curriculum distillation
- 4×128 MLP with skip connections (dual value+policy)
- 250K samples + mirroring
- BitboardSolver depth 18
- rayon parallel gradient descent
- Source files: train.rs, data.rs, training.rs (publicly in GitHub repo)

### 6. rowspire Input Correction (C057)

**Source**: rowspire full source code (features.rs, bitboard.rs)

- **Correction 1**: Input is 84-cell binary (not 64-cell). 12×7 board = 84 cells, not 64.
- **Correction 2**: Root noise is uniform random (not Dirichlet). 75% NN policy prior + 25% uniform random.

### 7. C013 Downgraded (Non-Standard Label)

**Claim**: C013 — "NN provides 2-3× alpha-beta speedup via better move ordering"
**Previous status**: MEDIUM-HIGH (non-standard label)
**New status**: HYPOTHESIS — no published source; AlphaConnect4 shows NN guides MCTS directly, not via alpha-beta move ordering

---

## Evidence Gate Violations Fixed

| Claim | Previous | New | Reason |
|-------|----------|-----|--------|
| C058 | VERIFIED | REFUTED | Training fully decoded — no longer opaque |
| C013 | MEDIUM-HIGH | HYPOTHESIS | Non-standard status label; Internal knowledge only |

## Claim Corrections

| Claim | Correction |
|-------|-----------|
| C057 | "64-cell binary" → "84-cell binary"; "Dirichlet root noise" → "uniform random noise" |

---

## New Claims (C073-C077)

| ID | Status | Claim |
|----|--------|-------|
| C073 | VERIFIED | Kaggle overtime tracking mechanism decoded: remainingOverageTime decrements by max(0, duration-actTimeout); below 0 → TIMEOUT disqualification |
| C074 | VERIFIED | Global config: actTimeout=6, runTimeout=1200, episodeSteps=1000, remainingOverageTime=12; ConnectX overrides: actTimeout=2, remainingOverageTime=60 |
| C075 | VERIFIED | Agent status enum: ACTIVE, INACTIVE, DONE, ERROR, INVALID, TIMEOUT — all documented |
| C076 | VERIFIED | kaggle-environments v1.32.2, Python ≥3.11 required |
| C077 | VERIFIED | Observation.step field available; deprecated_envs/ directory removed |

---

## Claim Register Statistics (Post-R15)

| Status | Count | Percentage |
|--------|-------|------------|
| VERIFIED | 48 | 64% |
| SUPPORTED | 8 | 11% |
| STRONGLY SUPPORTED | 2 | 3% |
| HYPOTHESIS | 13 | 18% |
| UNKNOWN | 3 | 4% |
| DISPUTED | 0 | 0% |
| REFUTED | 1 | 1% |
| **Total** | **75** | **100%** |

**Changes from R14**:
- VERIFIED: +5 (C073-C077), net +5 but recount reduces count (C058 removed from VERIFIED)
- HYPOTHESIS: +1 (C013 downgraded from MEDIUM-HIGH)
- REFUTED: +1 (C058 upgraded from VERIFIED)
- UNKNOWN: +3 (C002, C003, C004 reclassified from stale "no source found" to explicit UNKNOWN)
- Percentage: 64% VERIFIED (was 67% in R13, stable at ~66% in R14)

---

## Architecture Ranking Changes

| Approach | Previous | New | Reason |
|----------|----------|-----|--------|
| Hybrid NN + Search | HIGH | HIGH | No change |
| MCTS + NN | MEDIUM-HIGH | MEDIUM-HIGH | No change |
| Classical Engine | MEDIUM | MEDIUM | No change |
| Pure Search | MEDIUM | MEDIUM | No change |
| Pure Neural Network | LOW | LOW | No change |
| Supervised Pre-training + Search | MEDIUM | LOW | Board-size lock-in (7×6 only); no 15×13 transfer evidence |

---

## New Priority Gaps

| ID | Category | Status |
|----|----------|--------|
| GH-007 | rowspire training algorithm | ✅ RESOLVED R15: fully decoded via corpus audit |

---

## Evidence Delta

| Metric | R14 | R15 | Change |
|--------|-----|-----|--------|
| Total claims | 73 | 75 | +2 (C071-C072 from R13 + C073-C077 from R15, minus C058 reclassification) |
| VERIFIED | 48 (recalc) | 48 | Stable |
| VERIFIED % | 66% | 64% | -2% (recount + 75 total vs prior 73) |
| REFUTED | 0 | 1 | +1 (C058) |
| HYPOTHESIS | 12 | 13 | +1 (C013 downgraded) |
| Unknown % | ~8% | 4% | -4% (C002-C004 explicitly classified) |

---

## Source Ledger Changes

No new sources added in R15. All findings derive from existing sources:
- S006 (kaggle-environments source code) — deepened analysis
- S030/S041 (rowspire source code) — corpus audit decoded training

---

## Next Round Focus Areas

1. **Kaggle leaderboard analysis** — Still requires JS rendering; board configurations confirmed from spec but not from live page
2. **TonyCWang dataset training pipeline** — Temperature schedule, agent configuration, position sampling method still undocumented
3. **Pascal Pons blog.gamesolver.org tutorial** — Unreachable (SSL cert mismatch)
4. **LLM-based Connect 4 model evaluation** — 11+ models on Hugging Face with zero metrics
5. **GitHub API accessibility** — Still unreachable via curl and WebFetch (TLS/schannel errors)
6. **aariobarin TT port to JS/Python** — The 10M-entry TT with LRU eviction and history heuristic — worth benchmarking for Kaggle
7. **Woonderpipe/connect-4 AI implementation** — "serverless AI" not in publicly accessible source
8. **jambolo/four-in-a-row Rust AI** — Check src-tauri/src/ for Rust source files

---

## Files Modified

- `research/claim-register.md` — Statistics section updated; C058 REFUTED; C057 corrected; C013 downgraded; C073-C077 added
- `research/research-state.md` — Current Round → 15; R15 progression entry; GH-007 resolved
- `research/source-ledger.md` — Current Round → 15
- `research/architecture-rankings.md` — Current Round → 15; Supervised Pre-training MEDIUM→LOW; R15 in stability table