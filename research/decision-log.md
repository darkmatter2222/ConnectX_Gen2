# Decision Log — ConnectX Bot Research

> **Current Round**: 6
> **Last Updated**: 2026-08-02

---

## Architecture Decisions

| Decision | Round | Choice | Rationale | Alternative Considered | Reversible |
|----------|-------|--------|-----------|----------------------|------------|
| Leading approach | 1 | Hybrid NN + Search | 7x6 solved (book), 15x13 needs NN guidance | Pure search (limited depth), Pure NN (lacks precision) | No — foundational choice |
| Search algorithm | 1 | MTD(f) / PVS | Most efficient for Connect 4 with transposition table | Alpha-beta, NegaMax | No — algorithm choice is hard to change mid-implementation |
| NN training method | 1 | Two-stage SFT→RL | Most effective pipeline proven in AlphaZero literature | Pure RL, supervised only | Yes — can switch back |
| Hardware strategy | 1 | RTX 5090 for training, CPU for inference | Best balance; Kaggle doesn't provide GPU | CPU-only, cloud GPU rental | Yes — can use Kaggle T4 for training |
| Game-phase model | 5 | Opening (book) → Midgame (search) → Endgame (DB) | Proven by BitBully and engine literature | Single-model approach | Yes — simpler model if game-phase fails |
| Evaluation strategy | 5 | Manual weights (80% optimal) then NN fine-tuning | Manual tuning achieves 80% of optimal | NN-only learning from scratch | Yes — can switch to NN-only |
| WebSearch abandonment | 5 | Switch to WebFetch only | WebSearch API error 400 confirmed across all agents | Continue attempting WebSearch | Yes — can retry WebSearch in future |
| Source verification standard | 6 | All internal-knowledge repos must be verified via WebFetch | S007 (BitBully), S008 (mra1991) URLs returned 404 | Continue citing unverified sources | Yes — if URLs are found |
| GitHub topics sort method | 8 | Sort by `updated` (descending) instead of `stars` | connectpuct, rowspire, kite all newly discovered via sorted-by-update scan | Sort by stars | Yes — stars may surface different repos |
| arXiv as Böck source | 8 | arXiv yields zero results for "Connect Four solved" — try ICAPS, JOCIG, Google Scholar | arXiv search returned 0 results | Only use arXiv | Yes — arXiv is not the only venue |
| Tromp Fhourstones as 8x8 solver | 9 | tromp/fhourstones88 is Tromp's original 8x8 solver C++ code; book88 binary stores ≤16 ply positions | Verified 8x8 solving; book88 provides concrete training data source | Only use Fhourstones for 7x6 | Yes — 8x8 data may inform 7x6 |
| katac4 KataGo technique mapping | 9 | katac4 implements pre-activation ResNet, nested bottleneck, mixed spatial pooling, CUDA graph caching | First concrete KataGo port for Connect 4 | Standard ResNet | Yes — KataGo-specific optimizations |
| katac4 training as reference | 9 | 30K epochs, 3 loss terms, self-play workers, temperature decay, 3-phase lambda scheduler | Full training pipeline revealed; validates AlphaZero-style training for Connect 4 | Simpler training schedules | Yes — training compute requirement |
| Alpha-beta+MCTS hybrid viable | 9 | haithameleuch/connect-four-ai: alpha-beta depth-3 with Monte Carlo leaf (250 playouts), no heuristic | Hybrid search is practical without MCTS tree; statistical leaf evaluation | Pure heuristic leaf eval | Yes — evaluation function design |
| ICAPS/JOCIG/Google Scholar abandonment | 9 | All three venues unworkable: ICAPS DNS fail, JOCIG DNS fail, Google Scholar 404 | No external academic venue retrievable via WebFetch | Continue trying external venues | No — all 3 venues dead for this research |
| rowspire training algorithm is opaque | 10 | Full source code (14 files) analyzed; no training code found; npm run train invokes un-publish code | Training mechanism is the single largest gap in understanding rowspire | Rowspire training is available; it is not | No — training code is not on GitHub |
| eSlams is evaluation framework, not bot | 10 | ElectronicSlams/eSlams supports 50 arenas incl. Connect Four "standard" | Provides evaluation infrastructure but not a ConnectX bot | eSlams is a Connect 4 AI | No — it is a framework, not a bot |
| Rowspire 7-feature evaluation is the strongest manual eval baseline | 10 | 7 features with genetic-tuned weights: center control, piece count, threats, mobility, vertical/horizontal control, defensive score | Provides a strong manual eval design for Kaggle | Manual eval is weak without tuning | Yes — weights could be manually set to reasonable values |
| Wikipedia opening theory confirmed | 10 | Center column = first-player win ≤41, adjacent = draw, edge = loss 40-42 | Validates center-first move ordering for Kaggle | Opening theory may not generalize to 15x13 | Yes — only applies to 7x6 |

---

## Tool Decisions

| Decision | Round | Choice | Rationale | Reversible |
|----------|-------|--------|-----------|------------|
| Sub-agent web access | 5 | Prohibited in sub-agents | Sub-agents cannot use WebSearch (same API error) | Yes — if WebSearch is fixed |
| Parent loop web search | 5 | Limited to WebFetch | WebFetch works for single-page lookups | Yes — can retry WebSearch |
| Research methodology | 5 | Internal knowledge + source analysis | Only viable path given tool constraints | Yes — if tools are restored |

---

## Strategy Decisions

| Decision | Round | Choice | Rationale | Alternative | Reversible |
|----------|-------|--------|-----------|-------------|------------|
| Board representation priority | 5 | Python 1D array for Kaggle | Matches observation format; simple | C++ bitboards, 2D arrays | Yes — can optimize later |
| Numba adoption | 5 | Accept first-call JIT penalty | Numba gives 5-10× speedup; first call ~0.5-1s overhead | Cython, pure Python | Yes — can switch back |
| Move ordering strategy | 5 | Center-first + full ordering | 10-30× effective speedup from move ordering | Random ordering, alphabetical | Yes — can change |

---

## Decision Evolution

| Decision | Round 1 | Round 5 | Change? | Reason |
|----------|---------|---------|---------|--------|
| Leading approach | Hybrid NN + Search (Medium confidence) | Hybrid NN + Search (High confidence) | Confidence upgraded | More evidence from game-phase model |
| C++ search core | Recommended (Week 3-4) | Downgraded (Python constraint) | Approach changed | Kaggle Python submission makes C++ bindings complex |
| MCTS approach | Not ranked separately | Upgraded to #2 (Medium-High) | Ranking changed | Stronger evidence for large boards |
| Pure search | Ranked #4 (Medium) | Ranked #4 (Medium) | No change | Good baseline but weak on 15x13 |
| WebSearch | Not tested | Confirmed broken | Tool limitation | API error 400 |

---

## Pending Decisions

| Question | Options | Factors | Status |
|----------|---------|---------|--------|
| Best search algorithm for Python? | PVS vs MTD(f) vs alpha-beta | MTD(f) 20-30% faster but more TT re-searches | Pending empirical benchmark |
| NN architecture for 15x13? | CNN vs CNN+attention vs transformer | CNN proven for 7x6; attention may help generalization | Pending |
| Transfer learning strategy? | Direct 7x6→15x13 vs progressive | Progressive training may close gap from 32% to 10% | Pending empirical test |
| Training data size? | 100K vs 500K vs 1M positions | Larger = better generalization but longer training | Pending |
| Deployment target? | Kaggle T4 vs RTX 5090 | T4 has 16GB vs 32GB; slower but free | Pending |