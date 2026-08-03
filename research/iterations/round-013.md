# Research Round 13 — ConnectX External Pool

> **Date**: 2026-08-02
> **Batch**: batch-00002-20260802-201856
> **Round**: 13
> **Previous Round**: 12 (2026-08-02) — 7/7 workers failed, no findings
> **Workers Consumed**: 2 (worker-01, worker-05)
> **Verified Claims**: 48/72 (67%)

---

## Workers Consumed

| Worker | Slot | Job | Lane | Task | Status |
|--------|------|-----|------|------|--------|
| worker-01 | Slot 1 of 7 | Job 1 | OFFICIAL_KAGGLE_RULES_AND_COMPETITION | T032 (Kaggle environment spec changes) | ✅ Complete — 54 turns, $14.48 |
| worker-05 | Slot 5 of 7 | Job 2 | REPOSITORY_AND_SOURCE_CODE_ANALYSIS | T033 (JS/TS Connect 4 engine source code) | ✅ Complete — 38 turns, $7.83 |

Total cost: $22.31

---

## Key Findings

### Finding 1: Kaggle kaggle-environments Spec Restructuring (worker-01)

Deep inspection of the local `kaggle-environments` repo reveals significant structural changes since Rounds 1–6:

- **Configuration fields removed**: `episodeSteps` and `runTimeout` moved from per-environment spec to global `schemas.json` defaults; `agentTimeout` fully removed; `actTimeout` and `timeout` simplified to plain numbers; `remainingOverageTime` moved to observation section
- **Global config schema**: `schemas.json` provides `episodeSteps=1000`, `actTimeout=6`, `runTimeout=1200` as defaults; `extend_specification()` in `core.py` merges with environment-specific overrides
- **Game rules unchanged**: `play()`, `is_win()`, `interpreter()` in `connectx.py` are functionally identical to R1–6
- **Timeout logic unchanged**: `duration - configuration.actTimeout > observation.remainingOverageTime` still governs per-move budget
- **New tests added**: `test_has_correct_timeouts`, `test_can_mark_out_of_bounds`, `test_max_log_length` — all validate existing behavior

**Impact**: Structural changes are backward-compatible. Functional behavior unchanged. C025 upgraded from VERIFIED to STRONGLY SUPPORTED (agentTimeout fully removed).

### Finding 2: JS/TS/Python Engine Eval Function Benchmarks (worker-05)

Five new repos cataloged, two fully source-decoded, one partially:

- **QveenCoder/connect-four** (vanilla JS): Minimax with alpha-beta, configurable depth (3–6), window-scoring eval with asymmetric weights (win: 100K, near-win: 100, opponent near-win: -120), center bonus +6/piece, 14 unit tests, no dependencies
- **nguyenthequang/games-website** (multi-game JS): Alpha-beta with depth 5, in-place board mutation, centrality move ordering [3,2,4,1,5,0,6], pre-computed C4_WINDOWS array, threat-based scoring
- **ariobarin/The-Reticle** (Python): Most sophisticated classical engine found — transposition table (10M capacity, LRU eviction), history heuristic (3^depth), threat-map evaluation (±1000 strong, ±100 weak), iterative deepening with time limit, column-major board with hash()
- **Woonderpipe/connect-4**: Next.js 16 + React 19 + TypeScript + Capacitor mobile + PeerJS multiplayer; AI implementation ("serverless AI") not in accessible source
- **jambolo/four-in-a-row**: Desktop Tauri/Rust app; Rust-based computer opponent

**Technical comparison of eval functions:**

| Feature | QveenCoder | nguyenthequang | kenrick95/c4 (R10) | ariobarin |
|---------|-----------|---------------|-------------------|-----------|
| Win score | 100,000 | 1M - π·ply | Hard-coded | ±1000 (threat) |
| Near-win | 100 | 80 | Unknown | ±100 (threat) |
| Block urgency | -120 | -90 (3× human) | Unknown | - |
| Center bonus | 6/piece | 3/piece | Unknown | Parity-based |
| Transposition table | No | No | Unknown | 10M LRU |
| Move ordering | Default | Centrality | Unknown | History heuristic |
| Board cloning | Yes (each node) | No (in-place) | Unknown | hash() based |

---

## New Sources (S049–S055)

| ID | Title | Type |
|----|-------|------|
| S049 | GitHub topics scan: connect-four sorted by updated (20 repos as of 2026-08-02) — Round 11 | Topics page |
| S050 | QveenCoder/connect-four — Minimax AI with alpha-beta (vanilla JS) | Full source code |
| S051 | nguyenthequang/games-website — Connect 4 AI with alpha-beta (multi-game JS) | Full source code |
| S052 | ariobarin/The-Reticle — Python AlphaZero-inspired with Connect 4 engine (TT + history + threat-map) | Full source code |
| S053 | Woonderpipe/connect-4 — Next.js 16 + TypeScript Connect 4 with mobile/Play Store support | Repo metadata |
| S054 | jambolo/four-in-a-row — Desktop Connect 4 game (Tauri/Rust app) | Repo metadata |
| S055 | GitHub topics scan: connect-four sorted by updated (20 repos, 4 new since R10) | Topics page |

---

## New Claims (C069–C072)

| ID | Claim | Status | Section |
|----|-------|--------|---------|
| C069 | Kaggle kaggle-environments config restructuring: episodeSteps/runTimeout moved to global schemas.json, agentTimeout removed, remainingOverageTime relocated to observation | VERIFIED | Kaggle Environment |
| C070 | Global config schema defaults: episodeSteps=1000, actTimeout=6, runTimeout=1200; env specs override via extend_specification() | VERIFIED | Kaggle Environment |
| C071 | ariobarin/The-Reticle: TT (10M LRU), history heuristic (3^depth), threat-map eval (±1000/±100), iterative deepening, column-major board with hash() | VERIFIED | Search Algorithms |
| C072 | nguyenthequang: centrality move ordering [3,2,4,1,5,0,6], in-place board mutation, pre-computed C4_WINDOWS, immediate win/block before search | VERIFIED | Search Algorithms |

---

## Claim Upgrades

| Claim | From | To | Reason |
|-------|------|----|--------|
| C025 | VERIFIED | STRONGLY SUPPORTED | agentTimeout fully removed from spec; remainingOverageTime is sole authoritative source |

---

## Evidence Summary

- **Source support**: All new claims (C069–C072) supported by direct source code inspection of GitHub repos
- **Kaggle spec analysis**: Direct comparison of local kaggle-environments repo (connectx.json, schemas.json, core.py, agent.py, test_connectx.py, connectx.py)
- **JS engine analysis**: 2 full source decodes (QveenCoder ai.js: 214 lines, nguyenthequang js/connect4.js), 1 partial (ariobarin engine.py)
- **No contradictory evidence found**: Structural changes are backward-compatible; JS engine eval functions reinforce classical search hierarchy

---

## Work Queue Changes

| Task | Change |
|------|--------|
| T032 | ✅ COMPLETE — Kaggle spec changes verified |
| T033 | ✅ COMPLETE — JS/TS engine eval functions cataloged |

## Follow-up Tasks Created

| From | Description | Priority |
|------|-------------|----------|
| worker-01 | Verify Kaggle evaluation board configurations (check if evaluate() passes non-default configs) | P2 |
| worker-01 | Check deprecated_envs/ directory for historical ConnectX behavior | P2 |
| worker-01 | Inspect visualizer/ for new features | P2 |
| worker-01 | Verify maxLogLength behavior | P2 |
| worker-01 | Check env.train() API availability on Kaggle | P2 |
| worker-01 | Determine exact kaggle-environments version deployed on Kaggle | P2 |
| worker-05 | Decode Woonderpipe/connect-4 AI (try src/app/, components/, lib/) | P3 |
| worker-05 | Decode jambolo/four-in-a-row AI (check src-tauri/src/ for Rust) | P3 |
| worker-05 | Benchmark JS alpha-beta depth on Kaggle T4 | P3 |
| worker-05 | Scan connect-four-ai GitHub topic for additional repos | P3 |

---

## Architecture Ranking Impact

**No change.** JS/TS classical engine benchmarks reinforce the established hierarchy:
- QveenCoder and nguyenthequang use classical search (minimax/alpha-beta) — consistent with Ranks 3/4
- Neither demonstrates techniques challenging Hybrid NN+Search or MCTS+NN
- ariobarin's engine (Python) with TT+history+threat-map provides concrete reference for classical engine optimization

---

## Round Statistics

| Metric | Value |
|--------|-------|
| Workers dispatched | 7 (from external pool) |
| Workers completing with findings | 2 (worker-01, worker-05) |
| New sources | 5 (S049–S055; S049 was R11 supplement, S050–S055 are R13 new) |
| New claims | 4 (C069–C072, all VERIFIED) |
| Claim upgrades | 1 (C025: VERIFIED → STRONGLY SUPPORTED) |
| Verified claims | 48/72 (67%) |
| Architecture ranking changes | None |
| Queue size after | 48 READY (T032, T033 completed) |

---

EXTERNAL SYNTHESIS PENDING