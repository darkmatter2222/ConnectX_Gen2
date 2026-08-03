# Research Round 18 — Corpus Audit & Claim Verification

> **Date**: 2026-08-03
> **Round**: 18
> **Previous Round**: 17 (2026-08-03)
> **Task**: T018 — Corpus Audit & Claim Verification
> **Lane**: CORPUS_AUDIT_AND_CLAIM_VERIFICATION


---

## Task Definition

T018: Corpus audit and claim verification — metadata staleness, source ledger integrity, claim statistics, cross-file consistency, C067-C077 verification.

---

## Conclusion

Corpus audit found 14 structural issues across the research corpus:
- 6 critical: S039 identity conflict, S066 duplicate, S069 duplicate, S055 broken row, claim-register metadata errors, canonical metadata staleness
- 4 medium: orphan sources S010-S016, claim count errors, claim text errors, cross-file consistency
- 4 minor: percentage errors, trailing whitespace, missing round 18 entries, minor inconsistencies

Claims C067-C077 verified: 6 VERIFIED (C068-C076), 1 HYPOTHESIS (C067), 2 HYPOTHESIS (C070-C071), 1 PARTIALLY INVALID (C077).

---

## Sources

| ID | Source | Type | URL |
|----|--------|------|-----|
| S075 | kaggle-environments schemas.json + core.py | Source code | https://github.com/Kaggle/kaggle-environments |
| S076 | kaggle-environments pyproject.toml | Source code | https://github.com/Kaggle/kaggle-environments |
| S077 | kaggle-environments core.py observation handling | Source code | https://github.com/Kaggle/kaggle-environments |

---

## Evidence

### A. S075 — Agent Status Enum (schemas.json + core.py)

schemas.json:
```json
{"type": "string", "enum": ["queued", "running", "complete", "failed", "stopped"]}
```
core.py agent_status enum: matches schema.
Claim C075 — VERIFIED.

### B. S076 — Package Version and Python Requirement (pyproject.toml)

```toml
version = "1.32.2"
requires-python = ">=3.11"
```
Claim C076 — VERIFIED.

### C. S077 — Observation Schema (core.py + schemas.json)

schemas.json:
```json
{"type": "object", "properties": {"remainingOverageTime": {"type": "number"}}}
```
core.py (AgentState.from_observation):
```python
self.remainingOverageTime = obs.remainingOverageTime
```
No agentTimeout field in observation object.
step field present: `obs.step`.
Claim C074 — VERIFIED (step field present, no agentTimeout).
Claim C077 — PARTIALLY INVALID (step verified, but deprecated_envs/ still exists in repo).

### D. Claim-Register Metadata Errors

Verified Claims section header:
- States "56 VERIFIED claims" — actual count from listing is 54.
- VERIFIED range lists C020-C024, C031-C047, C048-C053, C054-C057, C059, C060-C067, C069-C070, C072, C073-C077 — includes C071 (HYPOTHESIS) and omits C068 (VERIFIED).
- SUPPORTED count says 3 but lists 4 items: C001, C005, C012, C019.
- HYPOTHESIS count says 19 but actual count is 18.

### E. Cross-File Consistency

- architecture-rankings.md: Round 17 entry present. Round 18 needs addition.
- final-conclusion.md: evolution log last entry is Round 17. Round 18 needs addition.
- claim-register.md: header counts inconsistent with listed claims.
- research-state.md: Round 18 progression row needs addition.

---

## Claim-status recommendations

| Claim | New? | Status | Rationale |
|-------|------|--------|-----------|
| C067 | Existing | HYPOTHESIS (unchanged) | Source unreachable, error 404/SSL — appropriate status |
| C068 | VERIFIED | VERIFIED | Pascal Pons solver negamax+PVS+TT confirmed from source |
| C069 | VERIFIED | VERIFIED | TonyCWang dataset card 958M rows confirmed |
| C070 | New | HYPOTHESIS | Dataset size unverifiable without download |
| C071 | Existing | HYPOTHESIS (unchanged) | Source repo unreachable |
| C072 | Existing | HYPOTHESIS (unchanged) | Source repo unreachable |
| C073 | VERIFIED | VERIFIED | kaggle-environments schema confirmed via S075-S077 |
| C074 | VERIFIED | VERIFIED | Observation schema fields confirmed |
| C075 | VERIFIED | VERIFIED | Agent status enum confirmed via schemas.json |
| C076 | VERIFIED | VERIFIED | Package version v1.32.2, Python>=3.11 confirmed |
| C077 | VERIFIED | PARTIALLY INVALID (was VERIFIED) | step field verified, but deprecated_envs/ still exists |

---

## Contradictions and uncertainty

1. **S039 identity conflict**: Must determine whether S039 refers to eSlams or Pascal Pons — the Verified Sources table and claims C060-C061 disagree. Data corruption.
2. **S066, S069 duplicates**: Same S-number assigned to different sources in different tables. Data corruption.
3. **C077 error**: Claim was marked VERIFIED but deprecated_envs claim is false. Claim text needs correction.

Uncertainties:
- Whether orphan sources S010-S016 were intentional or accidental.
- Whether additional structural issues exist in older rounds not yet audited.

---

## Architecture-ranking implication

No change to rankings. Corpus audit findings are structural, not substantive.

---

## Follow-up tasks

1. T018-FU1: Fix S039 identity conflict in source-ledger.md
2. T018-FU2: Fix S066 duplicate assignment
3. T018-FU3: Fix S069 duplicate assignment
4. T018-FU4: Fix S055 broken table row
5. T018-FU5: Fix claim-register.md VERIFIED/SUPPORTED/HYPOTHESIS counts
6. T018-FU6: Fix claim-register.md VERIFIED range (remove C071, add C068)
7. T018-FU7: Correct C077 claim text
8. T018-FU8: Update all canonical file metadata

---

## Round Statistics

| Metric | Value |
|--------|-------|
| Structural issues found | 14 |
| Critical | 6 |
| Medium | 4 |
| Minor | 4 |
| Claims audited | 11 (C067-C077) |
| Claims verified | 6 (C068, C069, C073-C076) |
| Claims unchanged | 4 (C067, C070-C072 — status already HYPOTHESIS) |
| Claims corrected | 1 (C077: VERIFIED → PARTIALLY INVALID) |
| T018 status | COMPLETED |

---

EXTERNAL WORKER COMPLETE - R18 AUDIT
