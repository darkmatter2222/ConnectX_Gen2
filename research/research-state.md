# Research State — ConnectX Bot

> **Current Round**: 10
> **Last Updated**: 2026-08-02
> **Previous Round**: 9 (2026-08-02)
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

---

## Research Corpus

- **Legacy documents**: ~30 research files in `research/` (preserved, indexed in README)
- **Canonical files**: research-state.md (this file), research-trajectory.md, final-conclusion.md, research-gaps.md
- **Iteration reports**: iterations/round-NNN.md (starting with round 6)

---

## Next Round Focus Areas

1. **rowspire training algorithm** — `npm run train` is opaque; no training code in repo. Try npm registry, Docker images, or infer from weight structure.
2. **rowspire genetic tuning weights** — the actual weight values are loaded from an external source, not in repo. Try resources/ directory, npm package, or Docker container.
3. **rowspire resources/** — README mentions a `resources/` directory that may contain pre-trained weights or config files.
4. **eSlams deep-dive** — understand the Connect Four arena implementation to see if it can be used for local bot evaluation.
5. **New GitHub topics scan** — `connect-four-ai`, `mcts`, `alpha-zero`, `minimax`, `negamax`, `connect-four-engine` topic scans for new repos.
6. **rowspire evaluation weights** — the genetic-tuned weight values are not in source code. Could be in JSON config, binary file, or generated at runtime.
7. **James Dow Allen's "The Complete Book of Connect Four"** — 403 Forbidden on fabpedigree.com; try alternative sources.
8. **ICAPS/JOCIG fallback** — try Semantic Scholar, DBLP, or DOI lookups for Böck database paper.