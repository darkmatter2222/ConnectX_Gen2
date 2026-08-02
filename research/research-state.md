# Research State — ConnectX Bot

> **Current Round**: 11
> **Last Updated**: 2026-08-02
> **Previous Round**: 10 (2026-08-02)
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
| 10 | 2026-08-02 | Complete | rowspire FULL source decoded (14 files): 4×128 MLP + skip connections (dual value+policy), 100D input (64-cell binary + 16 normalized features), 7-feature evaluation with genetic tuning, UCB1 MCTS (c=1.41, 4000 sims, NN-guided, Dirichlet root noise 75/25), 64-bit bitboard; training OPAQUE; eSlams evaluation framework discovered (50 arenas, REST protocol, Ed25519 proof); kenrick95/c4 (278★) cataloged; Wikipedia opening theory confirmed; VERIFIED claims 55%→60%; 3 new sources (S039-S041) |
| 11 | 2026-08-02 | Complete | Pascal Pons/connect4 C++ solver fully decoded (negamax+PVS+TT+book; iterative binary search); TonyCWang/ConnectFour dataset (958M rows, 2×6×7 binary matrices, 7-element target vectors, exact solver evaluations); Hugging Face LLM-based Connect 4 model catalog (11+ models, all lacking metrics); evidence audit (17 structural issues fixed: duplicate sections, duplicate sources, stale headers); GitHub API unreachable (TLS/schannel error); VERIFIED claims 60%→66%; 9 new claims (C060-C068); 8 new sources (S042-S049) |

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
| CG-004 | 15x13 first-player advantage | CRITICAL | 🔍 PARTIAL — Wikipedia confirms 7x6, not 15x13; 8x8 solved |
| GH-001 | MCTS variants | HIGH | ✅ RESOLVED (Round 7: 3 MCTS implementations analyzed, including katac4 with FPU/adaptive CPUCT) |
| GH-002 | TensorRT benchmarks | HIGH | ⏳ PENDING |
| GH-003 | CUDA search | HIGH | ⏳ PENDING |
| GH-004 | MTD(f) Python benchmark | HIGH | ✅ RESOLVED (Round 5) |
| GH-005 | Optimal CNN architecture | HIGH | ✅ RESOLVED (katac4 ResNet fully decoded in R9; rowspire fully decoded in R10) |
| GH-006 | Transfer learning effectiveness | HIGH | ✅ RESOLVED (Round 3) |
| GH-007 | rowspire training algorithm | HIGH | ❌ STILL UNKNOWN — npm run train is opaque; no training code in GitHub repo |
| GH-008 | rowspire genetic tuning weights | MODERATE | ⏳ UNKNOWN — weights loaded externally; not in source code |
| GH-009 | rowspire resources/ directory | MODERATE | ⏳ PENDING — may contain pre-trained weights |
| GH-010 | TonyCWang dataset training pipeline | MODERATE | 🔍 PARTIAL — 958M rows generated via Pascal Pons solver self-play with temperature; but exact temperature schedule and self-play agent configuration undocumented |
| GH-011 | GitHub API access | HIGH | ❌ NEW IN R11 — GitHub API (api.github.com) now unreachable via curl and WebFetch (TLS/schannel certificate errors); same network restriction that blocked R10 raw.githubusercontent.com fetches |
| GH-012 | LLM-based Connect 4 model evaluation | LOW | 🔍 PARTIAL — 11+ models on Hugging Face; all lack evaluation metrics; no evidence of competitive viability; text-based approach theoretically inferior to board-state for ConnectX |

---

## Research Corpus

- **Legacy documents**: ~30 research files in `research/` (preserved, indexed in README)
- **Canonical files**: research-state.md (this file), research-trajectory.md, final-conclusion.md, research-gaps.md
- **Iteration reports**: iterations/round-NNN.md (starting with round 6)

---

## Next Round Focus Areas

1. **TonyCWang dataset training details** — The self-play temperature schedule, agent configuration, and position sampling method are undocumented. Try fetching more dataset card details or contacting dataset author.
2. **Pascal Pons blog.gamesolver.org tutorial** — The step-by-step tutorial referenced in Pascal Pons' README is unreachable (SSL cert mismatch). Try alternative URLs or cached versions.
3. **rowspire training algorithm** — Still opaque. `npm run train` is un-publish code. No new leads discovered in R11.
4. **rowspire genetic tuning weights** — Still loaded externally, not in repo.
5. **LLM-based Connect 4 model evaluation** — 11+ models on Hugging Face with zero metrics. Could try inference on sample models to measure move-prediction accuracy.
6. **GitHub API accessibility** — GitHub is unreachable via curl and WebFetch (TLS/schannel errors). If this resolves, resume topic-based repo discovery.
7. **S005/S006 Kaggle ConnectX spec internal paths** — Consider adding GitHub API links as web-accessible fallback URLs.