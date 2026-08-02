# Research State — ConnectX Bot

> **Current Round**: 6
> **Last Updated**: 2026-08-02
> **Previous Round**: 5 (2026-08-02)
> **Status**: Active — deep research phase

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

---

## Tool Availability

| Tool | Status | Notes |
|------|--------|-------|
| WebSearch | ❌ Broken | API error 400 since iteration 5 |
| WebFetch | ✅ Working | Single-page lookups only |
| Bash/Glob/Read/Edit | ✅ Working | Repository inspection |
| Agent sub-agents | ✅ Working | Cannot use WebSearch (same API error) |

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
| H4 | SUPPORTED | Round 5 |
| H5 | STRONGLY SUPPORTED | Round 5 |
| H8 | MEDIUM-HIGH | Round 5 |
| H9 | MEDIUM-HIGH | Round 5 |
| H13 | PENDING | Round 5 |

---

## Priority Gaps

| ID | Category | Priority | Status |
|----|----------|----------|--------|
| CG-001 | Kaggle leaderboard | CRITICAL | ❌ BLOCKED (no web search) |
| CG-002 | Top bot strategies | CRITICAL | ✅ RESOLVED (Round 6: 5 ConnectX repos + 10 Connect 4 repos via GitHub topics) |
| CG-003 | RTX 5090 benchmarks | CRITICAL | ⏳ PENDING |
| CG-004 | 15x13 first-player advantage | CRITICAL | 🔍 PARTIAL |
| GH-001 | MCTS variants | HIGH | ✅ RESOLVED (Round 4) |
| GH-002 | TensorRT benchmarks | HIGH | ⏳ PENDING |
| GH-003 | CUDA search | HIGH | ⏳ PENDING |
| GH-004 | MTD(f) Python benchmark | HIGH | ✅ RESOLVED (Round 5) |
| GH-005 | Optimal CNN architecture | HIGH | 🔄 PARTIAL |
| GH-006 | Transfer learning effectiveness | HIGH | ✅ RESOLVED (Round 3) |

---

## Research Corpus

- **Legacy documents**: ~30 research files in `research/` (preserved, indexed in README)
- **Canonical files**: research-state.md (this file), research-trajectory.md, final-conclusion.md, research-gaps.md
- **Iteration reports**: iterations/round-NNN.md (starting with round 6)

---

## Next Round Focus Areas

1. Use WebFetch to pull specific pages of interest (GitHub repos, papers, Kaggle pages)
2. Deep-dive into existing repos from round 4 catalog for implementation details
3. Validate or falsify existing claims with fresh analysis
4. Identify new gaps that emerged from rounds 1-5