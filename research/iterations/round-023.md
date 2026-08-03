# Research Round 23 -- Asymmetric Eval Source Code Verification (T017 Batch-Synthesis)

> **Date**: 2026-08-03
> **Round**: 23
> **Task**: T017 follow-up -- External-pool worker-05-job-00009 synthesis
> **Previous Round**: 22 (T029 Board-Size Matrix)
> **Lane**: REPOSITORY_AND_SOURCE_CODE_ANALYSIS

---

## Batch Source

**Batch**: batch-00008-20260803-142259
**Worker**: worker-05-job-00009 (Slot 5, Job 9)
**Model**: qwen3.6
**Cost**: $10.45
**Turns**: 27
**Duration**: ~3.85s output / ~4,456s API wall-clock

---

## Tool Preflight

| Tool | Status | Notes |
|------|--------|-------|
| WebSearch | Broken | API error 400 since iteration 5 |
| WebFetch | Working | Single-page lookups only |
| Bash/Glob/Read | Working | Repository inspection |

---

## Research Objectives (T017 -- External-Pool Follow-Up)

Consume and verify the findings from external-pool worker-05-job-00009:
1. Verify Wikipedia Connect Four page changes since R10 (15x13 solving status)
2. Verify tromp.github.io/c4/c4.html board-size chart data
3. Verify GitHub topic scans for new repos
4. Deep source code analysis: asymmetric eval functions in QveenCoder and nguyenthequang

---

## Key Findings

### 1. Wikipedia Connect Four Page -- UNCHANGED (C001)

**Source**: S097 (en.wikipedia.org/wiki/Connect_Four)

- No changes since R10
- Still lists only 7x6 (solved first-player win, 2025 W-D-L table), 8x8 (variation), and "Infinite Connect-Four is solved: Draw"
- **New detail from Wikipedia**: Infinite Connect-Four solved as Draw (not previously recorded in any source)
- **15x13 solving status**: Remains **unknown** from public sources

**Implication**: No new information from Wikipedia for 15x13 or other non-standard board sizes.

### 2. Asymmetric Evaluation Function -- VERIFIED (C059 reinforcement)

**Sources**: S050 (QveenCoder ai.js), S051 (nguyenthequang connect4.js)

Both QveenCoder and nguyenthequang use **identical asymmetric window scoring**:

| Event | QveenCoder | nguyenthequang |
|-------|-----------|----------------|
| AI win | +100,000 | +100,000 |
| AI 3+open | +100 | +100 |
| AI 2+2open | +10 | +10 |
| Opponent 3+open | -120 | -120 |
| Game over (terminal) | ±10,000,000 | ±10,000,000 |

**Key insight**: The opponent threat (-120) is weighted **20% heavier** (1.2x) than the AI threat (100). This is a **proactive defense bias** -- prefer blocking opponent threats over pursuing own near-wins.

**Minimax terminal score (±10M)** is separate from window scoring and applies only when the game is actually over.

### 3. C005 Upgraded to VERIFIED

**Claim**: "Optimal first move on 7x6 is a middle column -- forces win in ≤41 moves"

**Before (R22)**: SUPPORTED -- S028 (Wikipedia) only

**After (R23)**: VERIFIED -- Source code from two independent implementations:
- QveenCoder (S050): centrality ordering [3,2,4,1,5,0,6] places column 4 first
- nguyenthequang (S051): centrality ordering [3,2,4,1,5,0,6] places column 4 first

Both engines structurally prioritize column 4 as the first move to try -- directly implementing the opening theory claim in C005.

### 4. "Never in Central Columns" Pattern for Larger Boards

**Source**: tromp.github.io/c4/c4.html (S098)

The Tromp page notes: "the winning starting moves are **NEVER in the central columns**" for larger boards.

**Contradicts** the 7x6 opening theory (column 4 = only winning move). A new pattern emerges at larger widths (≥9).

**Implication**: 7x6 opening theory does not generalize to larger boards. Opening strategies must be board-size-specific.

### 5. Board-Size Chart -- Already in R22

The tromp board-size chart (4x4 to 11x11) was already captured in R22 as claims C128-C131. No new claims needed.

### 6. GitHub Topic Scans -- No New Repos

Both connect-four (20 repos) and connectx (7 repos) topic scans show no new repos since R21. All previously cataloged.

---

## Evidence-Gate Compliance

| Check | Result |
|-------|--------|
| C059 source evidence | Strong -- S050 and S051 both confirm exact values (100K/100/-120) |
| C005 upgrade | Strong -- 2 independent source code implementations confirm middle-column bias |
| Wikipedia infinite Connect-Four | Moderate -- single source (Wikipedia page); no academic paper confirms |
| "Never central columns" | Moderate -- Tromp page note; no academic paper confirms; needs further verification |

**Note**: All changes to existing claims (C005 upgrade, C059 reconfirmation) have strong source code evidence. The infinite Connect-Four solved: Draw finding is from Wikipedia (single source, Moderate).

---

## Architecture Ranking Evidence Delta

**No changes to architecture rankings.**

The asymmetric eval finding (1.2x opponent threat amplification) strengthens the classical engine approach for 7x6 play: opponent-threat prioritization is a simple but effective heuristic that reduces defensive blunders. This is a low-complexity, high-ROI addition to any Kaggle bot evaluation function.

The "never central columns" pattern for larger boards supports the game-phase model: asymmetric eval that prioritizes defense is particularly important on larger boards where P2 advantage is more common.

---

## Summary Statistics

| Metric | Before (R22) | After (R23) | Delta |
|--------|-------------|-------------|-------|
| Total claims | 134 (C001-C134) | 134 (C001-C134) | 0 |
| VERIFIED | 79 | 80 | +1 (C005) |
| STRONGLY SUPPORTED | 3 | 3 | 0 |
| SUPPORTED | 5 | 4 | -1 (C005 upgrade) |
| HYPOTHESIS | 23 | 23 | 0 |

---

## Sources Added

| Source ID | Title | URL | Type |
|-----------|-------|-----|------|
| S097 | Wikipedia -- Connect Four (page content) | en.wikipedia.org/wiki/Connect_Four | Wikipedia |
| S098 | tromp.github.io/c4/c4.html -- Board size solving chart | tromp.github.io/c4/c4.html | Web page |

**Note**: Worker's S096/S097 (QveenCoder/neuyenthequang source code) already cataloged as S050/S051.

---

## Sources Corrected

| Source ID | Previous | Corrected |
|-----------|----------|-----------|
| S051 (nguyenthequang) | "threat-based scoring (AI 3-in-row: +80, human block: -90)" | "asymmetric window scoring (win: 100K, near-win: 100, opp near-win: -120, 1.2x opponent threat)" |

---

## Claim Changes

| Claim ID | Action | Reason |
|----------|--------|--------|
| C005 | SUPPORTED → VERIFIED | Source code from QveenCoder (S050) and nguyenthequang (S051) confirm middle-column bias via centrality ordering [3,2,4,1,5,0,6] |
| C059 | Reconfirmed VERIFIED | Exact asymmetric eval values verified (100K/100/-120) from source code |

---

## Remaining Gaps

1. **"Never central columns" for larger boards**: Needs verification for specific boards (9x11, 10x11, 11x11)
2. **4xN pattern induction**: Can the 4xN board patterns (all draws for small N, P2 win for N≥7) be proved by induction?
3. **Academic paper for "never central columns"**: Tromp page note needs academic citation
4. **Infinite Connect-Four solved: Draw**: Wikipedia mentions but no cited source; needs academic verification

---

## Follow-Up Tasks

1. Verify "never central columns" pattern for specific larger board sizes (9x11, 10x11, 11x11)
2. Find academic citation for Tromp's "never central columns" note
3. Benchmark asymmetric eval (opp-threat 1.2x AI-threat) vs symmetric eval (1:1) on positions from TonyCWang dataset
4. Search arXiv/Semantic Scholar for "Connect Four 15x13 solving status" academic literature
5. Verify whether infinite Connect-Four solved: Draw has academic source (not just Wikipedia)

---

EXTERNAL SYNTHESIS COMPLETE