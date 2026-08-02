# Research State — ConnectX Bot

> **Current Round**: 9
> **Last Updated**: 2026-08-02
> **Previous Round**: 8 (2026-08-02)
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
| 7 | 2026-08-02 | Complete | GoodCoder666/katac4 (18★) KataGo-inspired AlphaZero fully analyzed; Wikipedia confirms solved game; C001/C005 upgraded to SUPPORTED; 3 new sources (S026-S028) |
| 8 | 2026-08-02 | Complete | 3 new repos via sorted GitHub topics: connectpuct (PUCT benchmark 11/20), rowspire (neural MCTS + bitboard solver Rust+WASM), kite (Java bitboard solver); arXiv zero results; 5 new claims (C043-C047); 3 new sources (S029-S031) |
| 9 | 2026-08-02 | Complete | Tromp Fhourstones benchmark (20 systems, KPOS/S, Gprof profiling); Tromp 8x8 solver (book88, ≤16 ply); haithameleuch alpha-beta+MCTS hybrid; katac4 training pipeline fully decoded (self-play workers, 3 loss terms, 30K epochs); VERIFIED claims 50%→55%; 7 new sources (S032-S038); 6 new claims (C048-C053); ICAPS/JOCIG/Google Scholar all unworkable |

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
| CG-001 | Kaggle leaderboard | CRITICAL | ❌ BLOCKED (no web search; Kaggle pages require JS) |
| CG-002 | Top bot strategies | CRITICAL | ✅ RESOLVED (Round 6-7: 5 ConnectX repos + 10 Connect 4 repos via GitHub topics; GoodCoder666/katac4 analyzed) |
| CG-003 | RTX 5090 benchmarks | CRITICAL | ⏳ PENDING |
| CG-004 | 15x13 first-player advantage | CRITICAL | 🔍 PARTIAL — Wikipedia confirms 7x6, not 15x13 |
| GH-001 | MCTS variants | HIGH | ✅ RESOLVED (Round 7: 3 MCTS implementations analyzed, including katac4 with FPU/adaptive CPUCT) |
| GH-002 | TensorRT benchmarks | HIGH | ⏳ PENDING |
| GH-003 | CUDA search | HIGH | ⏳ PENDING |
| GH-004 | MTD(f) Python benchmark | HIGH | ✅ RESOLVED (Round 5) |
| GH-005 | Optimal CNN architecture | HIGH | 🔄 PARTIAL (katac4 ResNet with gated pooling now known) |
| GH-006 | Transfer learning effectiveness | HIGH | ✅ RESOLVED (Round 3) |

---

## Research Corpus

- **Legacy documents**: ~30 research files in `research/` (preserved, indexed in README)
- **Canonical files**: research-state.md (this file), research-trajectory.md, final-conclusion.md, research-gaps.md
- **Iteration reports**: iterations/round-NNN.md (starting with round 6)

---

## Next Round Focus Areas

1. rowspire neural network training data — how were the MLP weights trained? (currently random)
2. PUCT c_puct sensitivity — 1.0 (blanyal) vs 1.4 (connectpuct) vs adaptive (katac4)
3. rowspire evaluation feature importance — genetic-tuned weights vs prior heuristics
4. Find the Böck database paper — try ICAPS, JOCIG, or Google Scholar via WebFetch — arXiv yields zero results; ICAPS/JOCIG DNS fail; Google Scholar 404
5. Connect 4 opening theory beyond center-column
6. Research KataGo upstream engine techniques — katac4 confirmed pre-activation ResNet, nested bottleneck, mixed pooling, CUDA graph caching (C051)
7. James Dow Allen's "The Complete Book of Connect Four" — what opening theory does it contain?
8. 8x8 Connect 4 solving details — what is book88? How does the 8x8 solve relate to 7x6?