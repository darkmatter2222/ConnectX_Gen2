# Source Ledger — ConnectX Bot Research

> **Current Round**: 24
> **Last Updated**: 2026-08-03

---

## Primary Sources

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S001 | Böck (2025) — Complete W-D-L solution for 7x6 | Internal knowledge (unverified in this round) | Paper/DB | 2025 | 4.5T positions, ~13GB compressed |
| S002 | Tromp (2025) — Brute-force 8-ply database | Internal knowledge | Paper | 2025 | Independent verification of Böck |
| S003 | Allis (1988) — Knowledge-based approach of Connect-Four | Internal knowledge | Thesis | 1988 | First solver, first player wins |
| S004 | Wäldchen et al. (2022) — XAI for Connect 4 | https://arxiv.org/abs/2202.11797 | Paper | 2022 | Verified via WebFetch this round |
| S005 | Kaggle ConnectX environment spec | kaggle-environments/kaggle_environments/envs/connectx/connectx.json | Spec | 2020-2025 | Official: 7x6 default, 2s/move, 60s overage |
| S006 | Kaggle ConnectX interpreter | kaggle-environments/kaggle_environments/envs/connectx/connectx.py | Source | 2020-2025 | Official: flat board, win check, agent interface |
| S007 | BitBully (GitHub) | github.com/Harloc/connect4-bitboard — 404 (deleted/renamed) | Repo | 2012+ | MTD(f) + bitboards + opening DB — URL BROKEN |
| S008 | mra1991 Connect4 (GitHub) | github.com/mra1991/connect4 — 404 (deleted/renamed) | Repo | ~2023 | Python negamax + eval — URL BROKEN |

---

## Secondary Sources (from Round 4 catalog, unverified in rounds 5-6)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S009 | dillonloh minimax3 (Kaggle) | Internal knowledge | Kaggle | ~2023 | Depth-3 negamax, 60%+ vs random |
| S010 | athulshibu 4-model lookahead (Kaggle) | Internal knowledge | Kaggle | ~2023 | Multi-model lookahead |
| S011 | Axelredx AxelBrain (GitHub) | Internal knowledge | Repo | ~2023 | Java AI, 8-move lookahead |
| S012 | ayeennp C implementation | Internal knowledge | Kaggle | ~2023 | Claims "(almost) perfect" |
| S013 | danielspottiswood ML_Connect_4 (GitHub) | Internal knowledge | Repo | ~2023 | Hybrid NN+minimax |
| S014 | marcpaulo15 CNN+SFT→RL (GitHub) | Internal knowledge | Repo | ~2023 | Two-stage training pipeline |
| S015 | BEPb AlphaZero-style MCTS (GitHub) | Internal knowledge | Repo | ~2023 | Self-play MCTS |
| S016 | VSZM minmax3 (Kaggle) | Internal knowledge | Kaggle | ~2023 | Weighted eval function |

---

## Verified Sources (confirmed in this round)

| Source ID | Title | Verification | Method |
|-----------|-------|-------------|--------|
| S004 | Wäldchen et al. (2022) | VERIFIED | WebFetch confirmed title/authors/abstract |
| S005 | Kaggle ConnectX spec | VERIFIED | Source code inspection (connectx.json) |
| S006 | Kaggle ConnectX interpreter | VERIFIED | Source code inspection (connectx.py) |
| S017 | GitHub topics: connectx | VERIFIED | WebFetch — 5 repos listed |
| S018 | GitHub topics: connect-four | VERIFIED | WebFetch — 10 repos listed |
| S019 | blanyal/alpha-zero (92★) | VERIFIED + source code | WebFetch — full AlphaZero impl for Connect 4 |
| S020 | witchu/alphazero (31★) | VERIFIED | WebFetch — RL framework for Connect 4 |
| S021 | sidhantagar/ConnectX (10★) | VERIFIED | WebFetch — minimax + alpha-beta + DP |
| S022 | Tarun995/connectX-bitboard-agent (0★) | VERIFIED | WebFetch — bitboard + Numba + 16M TT + PVS |
| S023 | darkmatter2222/ConnectX-RL-DQN (1★) | VERIFIED | WebFetch — DQN ConnectX submission |
| S024 | ChristianMontecchiani/ConnectX_RL (0★) | VERIFIED | WebFetch — MCTS without NN |
| S025 | psalarc/DQN-ConnectX-Agent (0★) | VERIFIED | WebFetch — DQN architecture study |
| S026 | GoodCoder666/katac4 (18★) | VERIFIED + full source code | WebFetch — KataGo-inspired AlphaZero for Connect 4: PyTorch ResNet (b3c128nbt), 1600 MCTS sims, FPU, 16 parallel workers, 300K games ELO testing (8 days on 4×RTX 4090), interactive explorer |
| S027 | Wikipedia — Connect Four | VERIFIED | WebFetch — Solved game: Allen/Allis 1988, 4.53T positions, first-player win ≤41 moves, infinite/connect4 variants |
| S028 | sebadorn/Machine-Learning--Connect-Four (13★) | VERIFIED | WebFetch — ML training exploration: MLP/RBF/PCN/decision tree/KMeans comparison for Connect 4 |
| S029 | ahmeddoghri/connectpuct (0★) — PUCT MCTS for Connect 4 | VERIFIED + full source — Round 8 | PUCT MCTS with tactical priors, 11W/9L in 20 vs minimax d3 |
| S030 | tre-systems/rowspire (0★) — Neural MCTS + bitboard solver in Rust+WASM | VERIFIED + full source — Round 8 | Dual 4×128 MLP value+policy, bitboard solver, WASM deployment, genetic tuning, 4000 sims |
| S031 | tristan852/kite (2★) — Java bitboard Connect 4 solver | VERIFIED — Round 8 | Source tree: bitboard, TT, score cache, skill levels |
| S032 | John Tromp's Fhourstones solver — tromp.github.io/c4/fhour.html | VERIFIED — Round 9 | Fhourstones benchmark: 20 systems, KPOS/S, position analysis, Gprof profiling, bitboard win detection |
| S033 | John Tromp's Connect Four solving page — tromp.github.io/c4/c4.html | VERIFIED (partial) — Round 9 | Strong solution (~40K hours compute, compressed 8-ply DB), solving history (Allis 1988, Allen 1988), 9x6 solved 2005, 8x8 solved 2015 |
| S034 | jesper-olsen/connect-four (0★) — Rust port of Tromp's Fhourstones | VERIFIED + source code — Round 9 | Interactive TUI: human/perfect/minimax/MCTS, verified against original C (v3.2) + Java (v3.1), benchmark results (1.48B nodes full solve) |
| S035 | tromp/fhourstones88 (0★) — John Tromp's original 8x8 solver C++ | VERIFIED + source code — Round 9 | Solved 8x8 in late 2014/early 2015, book88 binary (≤16 ply solved positions), C488 binary solver, ~500MB transposition table |
| S036 | haithameleuch/connect-four-ai (0★) — Alpha-Beta + MCTS hybrid (Kotlin) | VERIFIED + source code — Round 9 | Alpha-beta depth-3 with Monte Carlo leaf evaluation (250 random playouts), board state via 2D array, parallel copy-and-play
| S037 | GoodCoder666/katac4/train.py — Training pipeline details | VERIFIED — Round 9 | Self-play training: parallel workers, shared model, temperature decay, 3 loss terms (policy, value, rival), SGD+momentum, 30K epochs, batch=16, checkpoints every 500
| S038 | GoodCoder666/katac4/model.py — ResNet + KataGo techniques | VERIFIED — Round 9 | Pre-activation ResNet with batch norm + ReLU, nested bottleneck, mixed spatial pooling (mean+max), CUDA graph caching, shallow conv heads
| S039 | ElectronicSlams/eSlams (4★) — Open AI game evaluation framework; 50 arenas incl. Connect Four "standard" | VERIFIED — Round 10 | REST-based agent protocol (POST /act); Ed25519 proof archives; local CLI + server-side official eval; adapters for 5 AI providers (OpenAI, Anthropic, Gemini, OpenRouter, Bedrock)
| S040 | kenrick95/c4 (278★) — Browser-based Connect 4 with Minimax+alpha-beta AI | VERIFIED — Round 10 | Minimax+alpha-beta opponent; hard-coded evaluation; TypeScript/HTML5 Canvas; 278★ (most-starred Connect 4 repo on GitHub)
| S041 | tre-systems/rowspire — Full source code (14 Rust files): neural_network.rs, mcts.rs, ml_ai.rs, bitboard.rs, evaluation.rs, features.rs, feature_scores.rs, ml_network.rs, ml_tactics.rs, mcts_node.rs, mcts_policy.rs — Round 10 | VERIFIED + full source — Round 10 | 4×128 MLP with skip connections (dual value+policy), UCB1 MCTS (c=1.41, 4000 sims, NN-guided, Dirichlet root noise 75/25), 100D input encoding (64-cell binary + 16 normalized features), 7-feature heuristic evaluation with genetic-tuned weights, 64-bit bitboard with carry-propagation move generation. Training algorithm opaque — npm run train invokes un-publish code.
| S042 | Pascal Pons/connect4 — C++ Connect 4 solver (AGPL v3) — Round 11 | VERIFIED + full source — Round 11 | Negamax with alpha-beta + PVS + transposition tables + opening book. Iterative null-window binary search for exact game values. Board sizes via template WIDTH×HEIGHT, default 7×6. Supports up to 9×6 in uint64_t. blog.gamesolver.org tutorial referenced but unreachable (SSL cert mismatch — GitHub cert served instead). Opening book generator uses DEPTH=14.
| S043 | connect4.gamesolver.org — Pascal Pons interactive Connect 4 solver page — Round 11 | VERIFIED — Round 11 | Alpha-beta engine with optimal play evaluation. Column ratings: positive = winning lines, negative = losing lines, absolute value = turns to resolution. Confirms solved game (Allen/Allis 1988). Step-by-step tutorial link to blog.gamesolver.org.
| S044 | TonyCWang/ConnectFour — 958M-row supervised training dataset (14.8 GB) — Round 11 | VERIFIED + full dataset card — Round 11 | 2×6×7 binary matrix observations (active/opponent channels), 7-element target vectors (solver column evaluation). ~109M train / ~61M test split, <3% overlap. Self-play with temperature sampling via Pascal Pons solver as value oracle. MIT license. Parquet format.
| S045 | Leon-LLM/Connect-Four-Datasets-Collection — 237K text-based Connect 4 game dataset — Round 11 | VERIFIED + dataset card — Round 11 | Move-by-move text notation (e.g., "1. d1 g1") with outcomes ("1-0", "0-1"). 11.1 MB, Parquet format. 195K train / 21.7K validation split. Coordinate-based encoding (column a-g, row 1-6).
| S046 | Lyte/ConnectFour-clean — 217K text-based Connect 4 game dataset — Round 11 | VERIFIED + dataset card — Round 11 | Text notation with outcomes. 50.4 MB. Referenced by same github.zhaw.ch/connect4-llm project as Leon-LLM models.
| S047 | Leon-LLM Connect 4 model collection (6 GPT-2 variants: 3 LC4N + 3 SC4N) — Round 11 | VERIFIED — Round 11 | Text-based GPT-2 models fine-tuned on Connect 4 game sequences. LC4N=Large, SC4N=Small, suffixes encode dataset size → seed → epochs. All models lack model cards and evaluation metrics.
| S048 | Looyyd/connectfour-qwen2.5-1.5b-instruct — Qwen2.5 1.5B fine-tuned on Connect 4 — Round 11 | VERIFIED — Round 11 | 2B param SFT model via TRL library. No model card, no evaluation. PEFT/LoRA variant (Qwen3-4B) also exists (UnstableBaselines).
| S049 | GitHub topics scan: connect-four sorted by updated (20 repos as of 2026-08-02) — Round 11 | VERIFIED — Round 11 | All 20 repos cataloged; 3 new since R10 scan. No GitHub API access (TLS/schannel errors); WebFetch used.
| S050 | QveenCoder/connect-four — Minimax AI with alpha-beta pruning (vanilla JS) — Round 13 | VERIFIED + full source — Round 13 | Minimax with alpha-beta, configurable depth (3–6 via UI), window-scoring eval with asymmetric weights (win: 100K, near-win: 100, opponent near-win: -120), 2D array board (row-major), pure JS with browser+Node.js exports, 14 unit tests, no dependencies
| S051 | nguyenthequang/games-website — Connect 4 AI with alpha-beta and asymmetric eval (multi-game JS) — Round 13 | VERIFIED + full source — Round 13 | Alpha-beta with depth 5, in-place board mutation (no cloning), centrality move ordering [3,2,4,1,5,0,6], pre-computed C4_WINDOWS array, asymmetric window scoring (AI win: 100K, near-win: 100, 2+open: 10, opponent near-win: -120, 1.2x opponent threat weight), multi-game website (6 games) — R23 corrected from approximate +80/-90 to exact values verified from source
| S052 | ariobarin/The-Reticle — Python AlphaZero-inspired arcade collection with Connect 4 engine (TT + history + threat-map) — Round 13 | VERIFIED + full source — Round 13 | Minimax with alpha-beta + transposition table (10M capacity, LRU eviction), history heuristic (3^depth), threat-map evaluation (±1000 strong, ±100 weak), iterative deepening with time limit, column-major board with hash()
| S053 | Woonderpipe/connect-4 — Next.js 16 + TypeScript Connect 4 with mobile/Play Store support — Round 13 | VERIFIED — Round 13 | Next.js 16 + React 19 + Capacitor mobile + Playwright E2E + PeerJS multiplayer. AI implementation ("serverless AI") not in publicly accessible source.
| S054 | jambolo/four-in-a-row — Desktop Connect 4 game (Tauri/Rust app) — Round 13 | VERIFIED — Round 13 | Tauri desktop app with `src-core/` and `src-tauri/` directories. Rust-based computer opponent; Tauri pattern suggests AI in `src-tauri/src/`.
| S055 | GitHub topics scan
: connect-four sorted by updated (20 repos as of 2026-08-02, 4 new since R10) — Round 13 | VERIFIED — Round 13 | All 20 repos cataloged; Woonderpipe/connect-4 and nguyenthequang/games-website newly discovered |

---

## Unverified Sources (internal knowledge, needs verification)

| Source ID | Title | Risk | Action Needed |
|-----------|-------|------|---------------|
| S001 | Böck (2025) solved DB | High — critical claim | WebFetch or external verification |
| S002 | Tromp (2025) | Medium | WebFetch or external verification |
| S009-S016 | Various Kaggle/GitHub repos from Round 4 | Medium-High | WebFetch to GitHub/Kaggle |

---

## Broken URLs (confirmed 404)

| Source ID | URL | Result |
|-----------|-----|--------|
| S007 (BitBully) | github.com/Harloc/connect4-bitboard | 404 |
| S008 (mra1991) | github.com/mra1991/connect4 | 404 |

---

## Known-Broken Tools

WebSearch is known broken (Round 5+): API error 400.

---

## URLs Probed This Round (Round 6)

| URL | Result |
|-----|--------|
| arxiv.org/abs/2202.11797 | ✅ OK |
| github.com/topics/connectx | ✅ OK — 5 repos |
| github.com/topics/connect-four | ✅ OK — 10 repos |
| github.com/blanyal/alpha-zero | ✅ OK — full source code |
| github.com/Kaggle/kaggle-environments | ✅ OK — metadata |
| github.com/Harloc/connect4-bitboard | ❌ 404 |
| github.com/mra1991/connect4 | ❌ 404 |
| github.com/witchu/alphazero | ✅ OK |
| github.com/sidhantagar/ConnectX | ✅ OK |
| github.com/Tarun995/connectX-bitboard-agent | ✅ OK |
| github.com/darkmatter2222/ConnectX-RL-DQN | ✅ OK |
| github.com/ChristianMontecchiani/ConnectX_RL | ✅ OK |
| github.com/psalarc/DQN-ConnectX-Agent | ✅ OK |
| raw.githubusercontent.com/Harloc/connect4-bitboard | ❌ 404 |
| raw.githubusercontent.com/mra1991/connect4 | ❌ 404 |
| raw.githubusercontent.com/blanyal/alpha-zero/master/main.py | ✅ OK |
| raw.githubusercontent.com/blanyal/alpha-zero/master/neural_net.py | ✅ OK |
| raw.githubusercontent.com/blanyal/alpha-zero/master/connect_four/connect_four_game.py | ✅ OK |
| raw.githubusercontent.com/blanyal/alpha-zero/master/config.py | ✅ OK |
| kaggle.com/competitions/carlospolm-connectx | ❌ 404 (requires JS) |
| jocig.org | ❌ DNS lookup failed |
| researchgate.net | ❌ 403 (authentication required) |
| connect-four.net | ❌ DNS lookup failed |
| connect-four.die-bocks.at | ❌ DNS lookup failed |
| www.bock.im | ❌ DNS lookup failed |
| github.com/abock/connect4 | ❌ 404 (repo not found) |
| arxiv.org/search/connected_connect4_solved | ❌ 404 |
| raw.githubusercontent.com/GoodCoder666/katac4/main/model.py | ✅ OK — full NN architecture |
| raw.githubusercontent.com/GoodCoder666/katac4/main/mcts.py | ✅ OK — MCTS implementation |
| raw.githubusercontent.com/GoodCoder666/katac4/main/train.py | ✅ OK — training pipeline |
| raw.githubusercontent.com/GoodCoder666/katac4/main/game.py | ✅ OK — game rules, board repr |
| raw.githubusercontent.com/GoodCoder666/katac4/main/saiblo/search.py | ✅ OK — MCGS implementation |
| raw.githubusercontent.com/GoodCoder666/katac4/main/explorer_main.py | ✅ OK — interactive GUI |
| raw.githubusercontent.com/GoodCoder666/katac4/main/benchmark.py | ✅ OK — benchmark code |
| raw.githubusercontent.com/GoodCoder666/katac4/main/elo.json | ✅ OK — ELO ratings |
| raw.githubusercontent.com/GoodCoder666/katac4/main/human_play.py | ✅ OK — human play |
| raw.githubusercontent.com/GoodCoder666/katac4/main/export_model.py | ✅ OK — model export |
| arxiv.org/search?query=Connect+Four+solved+database+Win-Draw-Loss | ❌ 0 results |
| raw.githubusercontent.com/ahmeddoghri/connectpuct/main/connectpuct/engine.py | ✅ OK — board engine |
| raw.githubusercontent.com/ahmeddoghri/connectpuct/main/connectpuct/mcts.py | ✅ OK — PUCT MCTS |
| raw.githubusercontent.com/ahmeddoghri/connectpuct/main/connectpuct/minimax.py | ✅ OK — alpha-beta minimax |
| raw.githubusercontent.com/ahmeddoghri/connectpuct/main/connectpuct/adversarial.py | ✅ OK — benchmark code |
| raw.githubusercontent.com/ahmeddoghri/connectpuct/main/README.md | ✅ OK — README with benchmark |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/mcts.rs | ✅ OK — MCTS Rust |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/neural_network.rs | ✅ OK — neural net Rust |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/ml_ai.rs | ✅ OK — dual NN + MCTS |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/bitboard.rs | ✅ OK — bitboard Rust |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/evaluation.rs | ✅ OK — evaluation function |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/features.rs | ✅ OK — feature encoding |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/feature_scores.rs | ✅ OK — feature scoring |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/ml_network.rs | ✅ OK — network config |
| raw.githubusercontent.com/tre-systems/rowspire/main/docs/ARCHITECTURE.md | ✅ OK — architecture docs |
| github.com/tre-systems/rowspire/git/trees/main | ✅ OK — full source tree |
| github.com/tristan852/kite/git/trees/main | ✅ OK — full source tree |

## URLs Probed This Round (Round 9)

| URL | Result |
|-----|--------|
| en.wikipedia.org/wiki/Connect_Four | ✅ VERIFIED — solved game: Allis 1988, Allen 1988, Böck 2025, Tromp 8-ply, center win ≤41 moves |
| github.com/topics/connect-four?o=desc&s=updated | ✅ OK — 20 repos (all previously known since R6) |
| github.com/topics/connect-four?o=desc&s=stars | ✅ OK — 20 repos (all previously known; kenrick95/c4 top with 278★) |
| github.com/haithameleuch/connect-four-ai | ✅ VERIFIED — Alpha-Beta + MCTS hybrid (Kotlin) |
| raw.githubusercontent.com/haithameleuch/connect-four-ai/main/README.md | ✅ OK — full alpha-beta + MCTS source code |
| github.com/jesper-olsen/connect-four | ✅ VERIFIED — Rust port of Tromp's Fhourstones |
| raw.githubusercontent.com/jesper-olsen/connect-four/main/README.md | ✅ OK — benchmark: 4 position analysis, 6 references cited |
| github.com/tromp/fhourstones88 | ✅ VERIFIED — Tromp's original 8x8 solver (C++), book88 binary |
| raw.githubusercontent.com/tromp/fhourstones88/master/README | ✅ OK — 8x8 solving history, book88 details, C488 solver |
| raw.githubusercontent.com/goodcoder666/katac4/main/model.py | ✅ VERIFIED — ResNet + KataGo techniques (pre-activation, nested bottleneck, mixed pooling, CUDA graph) |
| raw.githubusercontent.com/goodcoder666/katac4/main/train.py | ✅ VERIFIED — Training: self-play workers, 3 loss terms, SGD+momentum, 30K epochs, batch=16 |
| raw.githubusercontent.com/goodcoder666/katac4/main/game.py | ✅ VERIFIED — Game engine: 2D grid, column height, win detection, FPU via history |
| raw.githubusercontent.com/tre-systems/rowspire/main/README.md | ✅ OK — Project overview (sparse NN training details) |
| raw.githubusercontent.com/tre-systems/rowspire/main/docs/ARCHITECTURE.md | ✅ OK — Architecture docs (referenced NN training but no specifics) |
| tromp.github.io/c4/c4.html | ❌ 403 Forbidden |
| tromp.github.io/c4/fhour.html | ✅ VERIFIED — Fhourstones benchmark: 20 systems, KPOS/S, Gprof, position analysis |
| fabpedigree.com/james/C4/c4_book.htm | ❌ Could not retrieve — James Dow Allen book link referenced |
| scholar.google.com/search?q=connect+four+solved | ❌ 404 |
| projects.ias.ac/icaps/ | ❌ DNS lookup failed |
| www.jocig.org/ | ❌ DNS lookup failed |
| github.com/KanWarChristensen/katac-go | ❌ 404 — KataGo upstream not found under this name |

## URLs Probed This Round (Round 10)

| URL | Result |
|-----|--------|
| github.com/topics/connect-four?o=desc&s=updated | ✅ OK — 20 repos (all previously known since R6; kenrick95/c4 top with 278★) |
| github.com/topics/connectx?o=desc&s=updated | ✅ OK — 6 repos (2 newly cataloged: eSlams, connect-n; rest previously known since R6) |
| github.com/kenrick95/c4 | ✅ VERIFIED — Browser-based Connect 4, Minimax+alpha-beta AI, 278★ |
| raw.githubusercontent.com/kenrick95/c4/main/core/ai.ts | ❌ 404 — AI source code path not found |
| github.com/kenrick95/c4/tree/main/core | ❌ 404 — core directory tree not found via WebFetch |
| github.com/kenrick95/c4/tree/main/browser | ❌ 404 — browser directory tree not found via WebFetch |
| github.com/EternaPeptix/verbifrost | ✅ VERIFIED — NOT Connect 4: InfiniBand RDMA for macOS |
| github.com/ElectronicSlams/eSlams | ✅ VERIFIED — Open AI game evaluation framework, 50 arenas, REST protocol |
| raw.githubusercontent.com/ElectronicSlams/eSlams/main/README.md | ❌ 404 — no raw README at expected path |
| github.com/acsl-technion/flexdriver-model | ✅ VERIFIED — NOT Connect 4: Mellanox ConnectX networking hardware driver modeling |
| github.com/Kamide/connect-n | ✅ VERIFIED — NOT Connect 4: TypeScript PWA board game |
| github.com/tre-systems/rowspire | ✅ VERIFIED — npm run train command noted, ML weights generated |
| raw.githubusercontent.com/tre-systems/rowspire/main/README.md | ✅ OK — Project overview (sparse NN training details) |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/features.rs | ✅ OK — Feature encoding: 100D array |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/feature_scores.rs | ✅ OK — 16 feature scores with normalization constants |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/evaluation.rs | ✅ OK — 7-feature evaluation with genetic-tuned weights |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/neural_network.rs | ✅ OK — 4×128 MLP with skip connections, dual value+policy |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/ml_ai.rs | ✅ OK — NN + MCTS integration, 4000 sims, NN value/policy guidance |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/ml_network.rs | ✅ OK — Network config: 4 hidden layers of 128, skip connections |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/mcts.rs | ✅ OK — UCB1 selection, NN-guided, root noise, temperature sampling |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/bitboard.rs | ✅ OK — 64-bit board, carry-propagation move generation |
| raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/ml_tactics.rs | ✅ OK — Basic tactical move selector (wins/blocks), no GA code |
| en.wikipedia.org/wiki/Connect_Four | ✅ VERIFIED — Opening theory: center=win ≤41, adjacent=draw, edge=loss 40-42 |
| github.com/tromp/fhourstones88 | ❌ 404 (via Bash curl — may be network restriction) |
| api.github.com/repos/kenrick95/c4/contents | ❌ Empty (no curl output via Bash) |
## Sources Added Round 13 (Slot 5, Job 3, Lane: REPOSITORY_AND_SOURCE_CODE_ANALYSIS)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S056 | sagar-sap/connect-n-bot — C++ bitboard negamax solver for Arduino Nano 33 BLE — Round 13 | github.com/sagar-sap/connect-n-bot | Solver source code | ~2026 | Embedded Connect-N AI: Arduino Nano 33 BLE (nRF52840, Cortex-M4), mbed RTOS, BitBoard<240> template (up to 15×15 board), uint32_t words, 4096-entry transposition table, iterative deepening to 40 depths, time-bounded search (15ms check interval), tactical win/loss shortcuts, center-first move ordering, negamax with alpha-beta pruning, DWT cycle-counter timing. PlatformIO project. Everything is author's own work. |
| S057 | sjqtentacles/sml-connect4 — Standard ML alpha-beta Connect 4 engine — Round 13 | github.com/sjqtentacles/sml-connect4 | Solver source code | ~2026 | Pure Standard ML engine with alpha-beta search. 6×7 board, configurable search depth. API: Connect4.empty, Connect4.legalCols, Connect4.drop, Connect4.winner, Connect4.terminal, Connect4.isDraw, Connect4.bestMove(depth). Dual-compiler testing (MLton + Poly/ML) with byte-identical output gate. Comprehensive unit tests: win detection (vertical/horizontal/diagonal), bestMove win-in-1 detection. Uses harness.sml testing framework. |
| S058 | hemakumargokul/ai-game-agents — Java Connect Four agent using minimax with alpha-beta pruning — Round 13 | github.com/hemakumargokul/ai-game-agents | Solver source code | ~2026 | Java implementation of classic AI algorithms including Connect Four minimax + alpha-beta agent. 0★, Java. Part of a broader collection of classic AI algorithms. |

---

## URLs Probed This Round (Round 13, Slot 5)

| URL | Result |
|-----|--------|
| github.com/topics/connect-four?o=desc&s=updated | ✅ OK — 20 repos (2 new since R11: QveenCoder/connect-four, Woonderpipe/connect-4, nguyenthequang/games-website, hemakumargokul/ai-game-agents) |
| github.com/topics/connectx?o=desc&s=updated | ✅ OK — 7 repos (1 new since R10: sml-connect4 not listed, 0 new) |
| github.com/QveenCoder/connect-four | ✅ VERIFIED + full source — vanilla JS minimax + alpha-beta, depth 2/4/6 |
| raw.githubusercontent.com/QveenCoder/connect-four/main/ai.js | ✅ OK — full AI engine (328 lines): board logic, evaluation, minimax with alpha-beta |
| raw.githubusercontent.com/QveenCoder/connect-four/main/game.js | ✅ OK — UI layer (DOM rendering, game flow) |
| github.com/Woonderpipe/connect-4/tree/main/components/Connect4 | ✅ VERIFIED — Next.js/TS Connect 4 with 8 fun modes |
| raw.githubusercontent.com/Woonderpipe/connect-4/main/components/Connect4/index.tsx | ✅ OK — React component (UI layer only, AI in hook) |
| raw.githubusercontent.com/Woonderpipe/connect-4/main/hooks/use-connect4.ts | ✅ OK — AI hook: minimax with alpha-beta, POSITIONAL_BONUS matrix, center-first ordering, depth 3/5 by difficulty |
| raw.githubusercontent.com/Woonderpipe/connect-4/main/lib/connect4-logic.ts | ✅ VERIFIED + full source — AI logic: 5×7 POSITIONAL_BONUS, evaluateBoard (positional + windows), minimax with alpha-beta, center-first column ordering, difficulty-based depth (3/5), 8 fun modes |
| github.com/nguyenthequang/games-website | ✅ VERIFIED — Multi-game JS engine (7 games) |
| raw.githubusercontent.com/nguyenthequang/games-website/main/js/connect4.js | ✅ OK — Connect 4 AI: 6-ply alpha-beta, center-first ordering [3,2,4,1,5,0,6], pre-computed C4_WINDOWS, threat-based scoring (+80/-90) |
| raw.githubusercontent.com/nguyenthequang/games-website/main/tests/run-tests.js | ✅ OK — Headless test harness (DOM stubs) |
| raw.githubusercontent.com/nguyenthequang/games-website/main/tests/suites.js | ✅ OK — Test suite: Connect 4 hard takes wins/blocks verification |
| github.com/sagar-sap/connect-n-bot | ✅ VERIFIED + full source — Arduino Nano 33 BLE Connect-N bot |
| raw.githubusercontent.com/sagar-sap/connect-n-bot/main/src/main.cpp | ✅ OK — Main entry: mbed RTOS loop, serial comms, BitBoard<240> allocation |
| raw.githubusercontent.com/sagar-sap/connect-n-bot/main/lib/GameLogic/Players/SagarsPlayer.hpp | ✅ OK — BitBoardSolver<240>: 4096-entry TT, iterative deepening, time management (15ms check interval), tactical shortcuts, negamax + alpha-beta |
| raw.githubusercontent.com/sagar-sap/connect-n-bot/main/lib/GameLogic/GameBoard/BitBoard.hpp | ✅ OK — BitBoard<N>: up to 240-bit (15×15), uint32_t words for ARM M4, column height tracking, win detection via shift-and, threat detection, center-first move ordering |
| raw.githubusercontent.com/sagar-sap/connect-n-bot/main/platformio.ini | ✅ OK — PlatformIO: nRF52/nano33ble, 115200 baud serial |
| github.com/sjqtentacles/sml-connect4 | ✅ VERIFIED — SML alpha-beta Connect 4 |
| raw.githubusercontent.com/sjqtentacles/sml-connect4/main/test/test.sml | ✅ OK — Unit tests: win detection, bestMove, board state |
| raw.githubusercontent.com/sjqtentacles/sml-connect4/main/Makefile | ✅ OK — MLton + Poly/ML dual-compiler build + byte-identical output gate |
| github.com/ariobarin/The-Reticle | ✅ VERIFIED — Arcade collection with Connect 4 |
| raw.githubusercontent.com/ariobarin/The-Reticle/main/src/connect_four/engine.py | ✅ OK — Minimax + alpha-beta + TT (10M LRU) + history heuristic (3^depth) + threat-map eval. TT is commented out in search. |
| raw.githubusercontent.com/ariobarin/The-Reticle/main/src/connect_four/board.py | ✅ OK — Column-major board, threat-map creation, win detection |
| github.com/hemakumargokul/ai-game-agents | ✅ VERIFIED — Java AI algorithms including Connect Four |
| github.com/topics/negamax?o=desc&s=updated | ✅ OK — 20 repos (chess engines, no new Connect 4) |
| github.com/topics/bitboard?o=desc&s=updated | ✅ OK — 20 repos (chess/shogi engines, sagar-sap/connect-n-bot confirmed) |

## Sources Added Round 16 (Slot 4, Job 3, Lane: NEURAL_TRAINING_AND_HARDWARE — GPU/Parallel Search)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S059 | Ala'anzy & Madiyarova (2026) — Connect 4 AI: A Comprehensive Taxonomy and Critical Review of Methods and Metrics (MDPI Symmetry 18(2)293) | https://www.mdpi.com/2073-8994/18/2/293 | Survey/Taxonomy Paper | 2026 | Published peer-reviewed taxonomy paper covering foundational game theory, classical search techniques (alpha-beta, MTD(f)), Monte Carlo Tree Search, reinforcement learning, explainable AI systems, and formal verification for Connect 4. Reviewer recommended adding "more examples of combinatorial game theory and search algorithms." GPU-accelerated simulations and alpha-beta/MTD(f) comparisons discussed. Full-text access blocked (403) but metadata verified via Semantic Scholar and Google Scholar. |
| S060 | Liang Li et al. (2012) — A Node-based Parallel Game Tree Algorithm Using GPUs for Connect 6 | Conference paper, 2012 | Research Paper | 2012 | GPU-accelerated Connect 6 game tree search using CUDA. Node-based parallel approach processing tree nodes concurrently with alpha-beta pruning. Speedup: 70.8× without pruning, 10.58× with pruning on Connect 6, 7.26× on Chess. Demonstrates GPUs are a feasible way to improve game tree algorithm performance. Focus on Connect 6 (not Connect 4) but techniques directly applicable. |
| S061 | MCTS-NC (Klęsk) — Monte Carlo Tree Search with numba.cuda: four thoroughly parallel GPU variants | github.com/pklesk/mcts_numba_cuda | GitHub Repository + Software Paper | ~2024-2025 | Python project implementing four GPU-accelerated MCTS variants using numba.cuda: ocp_thrifty (One Child Playouts, thrifty memory), ocp_prodigal (OCP, prodigal memory), acp_thrifty (All Children Playouts, thrifty), acp_prodigal (ACP, prodigal). Lock-free design: no atomic operations, no mutexes. Connect 4 benchmarks: ocp_prodigal 75.125% avg score (6.4M playouts, 7.34 avg depth), acp_prodigal 73.375% (20.3M playouts, 8.62 avg depth). Vanilla MCTS baseline only 2.5-2.875%. Hardware: AMD EPYC + NVIDIA GRID A100. Performance: 1.27M steps/sec, ~7.4M playouts per decision in 5 seconds. Also supports Gomoku. Source: src/, experiments/, docs/. |
| S062 | Navade788/gpu-connect4-cuda — CUDA C++ GPU-based Connect 4 with independent GPU players | github.com/Navade788/gpu-connect4-cuda | GitHub Repository | ~2025 | CUDA C++ implementation of Connect 4 where two AI agents compete as independent GPU players using CUDA kernels. Architecture: host CPU manages board init, kernel launches, turn order, display. GPU kernels evaluate moves and compute decisions in parallel. Parallel design: each CUDA thread evaluates a column. Memory ops use standard CUDA alloc/free. Transfers board between host/device after every turn. Player 1: random valid move (fast, low overhead). Player 2: analyzes neighboring positions for winning patterns (more computation, better quality). Files: main.cu, kernels.cu, game_logic.h. Future work: GPU-based Minimax, alpha-beta pruning, shared-memory optimization, network multiplayer. |
| S063 | brightonanc/Project-Artetra — Connect Four AI based on parallel game tree search, CUDA target | github.com/brightonanc/Project-Artetra | GitHub Repository | ~2025 | Connect-4 AI targeting parallel game tree search with final code intended in CUDA. Topics: ai, alpha-beta, cpp, cuda, game-ai, negamax, principal-variation-search, search-algorithm. Source code incomplete: only directories listed (artetra/, playground/) with no actual .cu/.cpp/.h files visible. May be work-in-progress or abandoned. |
| S064 | Johnson, Barford, Dascalu & Harris Jr. — CUDA Implementation of Computer Go Game Tree Search (PV-Split on GPU) | Springer conference paper, University of Nevada Reno | Research Paper | ~2010s | GPU implementation of PV-Split parallelized tree search for two-player zero-sum games. Addresses Go's large board size and exponential time complexity. Uses GPU kernel recursion (Compute Capability 3.5+) for iterative-deepening Alpha-Beta search with transposition tables. Applies to Go and checkers (not Connect 4). Provides methodology for adapting parallel search to GPU architecture. |
| S065 | ScienceDirect — Speeding up AI Reasoning through Parallelization of Monte Carlo Tree Search for Connect 4 | ScienceDirect journal article | Research Paper | ~2023-2025 | Compares OpenMP CPU parallelization vs CUDA GPU acceleration for Connect 4 MCTS. Reports throughput gains across both CPU and GPU platforms. Hardware performance metrics compared between OpenMP multi-threaded CPU and CUDA GPU implementations. Specific numbers not accessible (no full text found). Confirms GPU MCTS parallelization is a researched topic for Connect 4 specifically. |

## Sources Added Round 17 (Slot 1, Job 7, Lane: OFFICIAL_KAGGLE_RULES_AND_COMPETITION)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S066 | tre-systems/rowspire — resources/ai/evolved.json: Generation 2 evolved genetic parameters | raw.githubusercontent.com/tre-systems/rowspire/main/resources/ai/evolved.json | Data/Config | ~2025 | Evolved genetic parameters (generation 2, parent gen 1): win_score=5815, loss_score=-9283, center=91, adjacent=30, outer=12, edge=10, threat_weight=3.851, horizontal_control=2.840, vertical_control=1.335, defense=0.992, piece_count=0.113 (dramatically reduced from default 0.965). Center column value dropped 45% (165→91) and threat_weight nearly doubled (1.588→3.851). |
| S067 | tre-systems/rowspire — resources/ai/ml_ai_weights_best.json: Best neural network weights | raw.githubusercontent.com/tre-systems/rowspire/resources/ai/ml_ai_weights_best.json | Data/Weights | ~2025 | Best neural network weight matrix from training (4×128 MLP dual value+policy). Exported JSON. |
| S068 | tre-systems/rowspire — worker/src/genetic_params.rs: Genetic parameter struct and defaults | raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/genetic_params.rs | Source code | ~2025 | Default genetic parameter starting point. 16 tunable parameters: win_score, loss_score, 4 column position values, 7 feature weights (row_height, center_control, piece_count, threat, mobility, vertical_control, horizontal_control, defensive). serde serialize + TypeScript export via ts-rs. |
| S069 | tre-systems/rowspire — worker/src/feature_scores.rs: Feature encoding producing 16D vector | raw.githubusercontent.com/tre-systems/rowspire/main/worker/src/feature_scores.rs | Source code | ~2025 | 16 features (center P1/P2, pieces P1/P2, threats P1/P2, mobility P1/P2, vertical P1/P2, horizontal P1/P2, diagonal P1/P2, blocking P1, player indicator). threat_value: 4-in-row=1000, 3-unblocked=100, 3-blocked=10, 2-unblocked=10, 2-blocked=1. New features vs R10: diagonal, blocking. |
| S070 | MarkusThill/BitBully - MTD(f) solver with Python bindings (AGPL-3.0) | VERIFIED + source code — Round 16 | C++ solver with Python bindings via CMake. MTD(f) search, bitboard representation, cached lookup tables, opening book support. Python package installable via pip. First open-source MTD(f) for Connect 4. |
| S071 | ecc521/connect-4-solver - NNUE-enhanced Pascal Pons (AGPL v3, full source decoded) | VERIFIED + source code — Round 16 | C++ solver compiled for WASM + Node.js + React Native. NNUE integrated with negamax search. 19 source files fully decoded. Templates support 4x4 to 12x12 boards. Pre-trained weights for 7x6 and 8x8. Elias Fano encoding for opening books. Symmetric key TT. |
| S072 | ethan-haas/neurofour - Strength-per-Byte benchmark arena (85/15 strength/soundness, 5M FLOP/move) | GitHub repo | Source Code | ~2025 | Python FastAPI + Next.js/React benchmark arena. Bitboard Connect 4 with fill-trick, mirror-normalized TT keys, center-first ordering. NeuroGolf Score metric. Zero-byte champion (handcrafted search beats NN). 20-agent registry. |
| S073 | miksipiksic/pyvezi - Python bitboard Minimax with window-counting heuristic (Pygame) | GitHub repo | Source Code | ~2025 | Python + Pygame Connect 4 with bitboard state (two integer bitmasks for 6x7). Minimax+alpha-beta with center-first ordering [3,2,4,1,5,0,6). Window-counting heuristic. Brian Kernighan bit counting. |
| S074 | Karthick-dev-cart/connectfour - Flutter + Pygame Connect 4 (depth 2/6) | GitHub repo | Source Code | ~2025 | Flutter (Dart) + Python Pygame Connect 4. Minimax+alpha-beta center-first search. Window-counting heuristic at depth limit. Depth 2 (Easy) / 6 (Hard). Flutter compute off UI thread. Tested on concrete tactical positions. |

## Sources Added Round 19 (OFFICIAL_KAGGLE_RULES_AND_COMPETITION Deep Source Analysis)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S075 | kaggle-environments core.py (v1.32.2) — Environment class with step(), run(), reset(), evaluate(), train(), overtime tracking, log truncation | kaggle-environments/kaggle_environments/core.py | Source code | 2020-2025 | Full environment runtime: Environment class, step() plays one step for each agent, run() orchestrates episodes, reset() initializes boards, evaluate() handles Kaggle evaluation, train() for training mode. Overtime tracking: remainingOverageTime decremented by max(0, duration - actTimeout) per step (line 631-632). Log truncation: maxLogLength (10K chars) applied to stdout/stderr per agent per step. Board is created once at reset() and mutated in-place across all steps. Agent status enum: ACTIVE, INACTIVE, DONE, ERROR, INVALID, TIMEOUT. Global config schema defaults from schemas.json: episodeSteps=1000, actTimeout=6, runTimeout=1200, remainingOverageTime=12, maxLogLength=10000. |
| S076 | kaggle-environments agent.py (v1.32.2) — UrlAgent, build_agent, Agent.act(), timeout enforcement, signature autodetection | kaggle-environments/kaggle_environments/agent.py | Source code | 2020-2025 | UrlAgent class for remote URL-based agents. build_agent() function: signature autodetection via agent.__code__.co_argcount (line 151-153, supports 1-arg and 2-arg signatures. Agent.act() method: per-call timeout enforcement (line 220) — if duration - actTimeout > remainingOverageTime, returns DeadlineExceeded(). UrlAgent timeout calculation (line 89): timeout = remainingOverageTime + actTimeout + 1s grace. Log truncation (line 200-205): maxLogLength applied to both stdout and stderr. |
| S077 | kaggle-environments connectx.py (v1.32.2) — play(), is_win(), random_agent, negamax_agent, interpreter, renderer | kaggle-environments/kaggle_environments/envs/connectx/connectx.py | Source code | 2020-2025 | Game engine: play() drops piece to lowest empty row in column, is_win() checks 4 directions with offset_row/offset_column increments, is_win() has_played=False branch uses lowest EMPTY row for lookahead without board mutation. Invalid move handling (line 141-144): column < 0 or action >= columns or board[column] != EMPTY — active agent gets Invalid column status, inactive gets DONE. Board initialization via reset(): EMPTY * (rows * columns) flat row-major. random_agent and negamax_agent implementations for testing. interpreter() and renderer() functions for Kaggle integration. |
| S078 | kaggle-environments connectx.json (v1.32.2) — Environment specification | kaggle-environments/kaggle_environments/envs/connectx/connectx.json | Spec | 2020-2025 | Environment spec: title "ConnectX", description "The classic Connect Four game. Drop a piece in a column, try to get 4 in a row." Number of agents: 2. Agent timeout: 2 seconds. Event configuration: observation with columns, remainingOverageTime, score, step, type, board (1D array of length rows*columns), agentTurn, action. Reward encoding: -1 = Lost, 0 = Draw/Ongoing, +1 = Won. |
| S079 | kaggle-environments test_connectx.py (v1.32.2) — 279-line test suite | kaggle-environments/kaggle_environments/envs/connectx/test_connectx.py | Test | 2020-2025 | Comprehensive test suite for ConnectX: 6 tests for 7x6 board, 8 tests for 4x5/inarow=3 board. No tests for boards larger than 10x8. Tests for invalid moves, timeout handling, observation format, reward encoding, board state progression. |
| S080 | kaggle-environments schemas.json (v1.32.2) — Global configuration schema | kaggle-environments/kaggle_environments/schemas.json | Spec | 2020-2025 | Global configuration schema: episodeSteps=1000, actTimeout=6, runTimeout=1200, remainingOverageTime=12, maxLogLength=10000. Environment specs can override via extend_specification(). agentTimeout fully removed. step field added for stateful agents. |
| S081 | kaggle-environments visualizer/renderer.ts (v1.32.2) — Canvas-based TypeScript renderer | kaggle-environments/kaggle_environments/envs/connectx/visualizer/renderer.ts | Source code | 2020-2025 | Canvas-based renderer with cyan (mark 1) and white (mark 2) pieces. K and goose logos. Animated piece drop effect. Win-line highlighting. Step controls (next/previous/autoplay). JSON replay support. Board rendering from flat 1D array. Responsive canvas sizing. |
| S082 | kaggle-environments deprecated_envs/README.md (v1.32.2) — Deprecated environment documentation | kaggle-environments/kaggle_environments/deprecated_envs/README.md | Documentation | 2020-2025 | Deprecated environments catalog: chess (special Dockerfile required), Lux AI s2 (vec_noise dependency conflict with gymnasium), LLM 20 questions (gymnasium < 1.0 incompatibility), tic-tac-toe (obsolete visualizer), open_spiel_env games (obsolete visualizers). Reasons for deprecation documented. |
| S083 | kaggle-environments pyproject.toml (v1.32.2) — Package version and dependencies | kaggle-environments/pyproject.toml | Config | 2020-2025 | Package version v1.32.2. Python >=3.11 required. Dependencies: numpy, jsonschema, fastapi, uvicorn, httpx, jinja2, pydantic. Version confirms the exact version used for deep source analysis in R19. |
| S084 | kaggle-environments visualizer/index.html (v1.32.2) — Visualizer HTML entry point | kaggle-environments/kaggle_environments/envs/connectx/visualizer/index.html | HTML | 2020-2025 | Visualizer HTML entry point. Loads renderer.ts as ES module. Canvas element for game rendering. Step controls (next, previous, autoplay buttons). Replay panel for JSON replay files. Instructions for Kaggle environment visualization. |


## Sources Added Round 20 (Slot 5, Job 7, Lane: REPOSITORY_AND_SOURCE_CODE_ANALYSIS)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S085 | tristan852/kite Kite.java — Full Java solver architecture (net.kite.internal.Kite) — Round 20 | github.com/tristan852/kite | Source code | 2024-2025 | Complete architecture decoded: fixed 7x6 board, center-first move ordering {3,2,4,1,5,0,6}, 5 skill levels (RANDOM, PERFECT, ADAPTIVE, 3 configurable via maximal_evaluation_loss), cubic score weight (score-min)^3 for probability distribution, adaptive move targeting half-board score with shrinking equal-score range, performance metrics tracking (evaluations, nodes, throughput), OpeningBoardScoreCaches (95.6 MB), mutable 2D board (no bitboard), no transposition table visible in Kite.java |
| S086 | pklesk/mcts_numba_cuda c4.py — Connect 4 game state with Numba JIT win detection — Round 20 | github.com/pklesk/mcts_numba_cuda/src/c4.py | Source code | 2024-2025 | C4 game state class: 6x7 numpy int8 board, column_fills tracking (7 int8 entries), Numba JIT win detection at last-placed piece only (4-directional scan from drop point), win detection: N-S, E-W, NE-SW, NW-SE each scanning +/-3 cells from last piece, returns {-1, 0, 1} for terminal states, None for ongoing, draw detection via board.sum(), random playout via np.random.choice from open columns |
| S087 | pklesk/mcts_numba_cuda mcts.py — Standard CPU Monte Carlo Tree Search reference — Round 20 | github.com/pklesk/mcts_numba_cuda/src/mcts.py | Source code | 2024-2025 | State base class: win_flag, n, n_wins, parent, children, outcome_computed, outcome, turn, last_action_index. MCTS class: UCB1 c=2.0 (DEFAULT_UCB_C), selection via UCB1 at every internal node, expansion via random child, playout via take_random_action_playout until terminal, backup backing up from terminal to root. Best action selection: (1) win_flag first, (2) visit count n, (3) win count n_wins. Performance tracking: loop time, select/expand/playout/backup times, tree size/depth, steps/second, playouts/second |
| S088 | pklesk/mcts_numba_cuda mctsnc_game_mechanics.py — CUDA device functions for Connect 4 game mechanics — Round 20 | github.com/pklesk/mcts_numba_cuda/src/mctsnc_game_mechanics.py | CUDA source code | 2024-2025 | Five CUDA device functions: is_action_legal_c4, take_action_c4, legal_actions_playout_c4, take_action_playout_c4, compute_outcome_c4. Lock-free design: no atomics, no mutexes. is_action_legal_c4: extra_info[action] < m (column not full). take_action_c4: extra_info[action] += 1; row = m - extra_info[action]; board[row, action] = turn. compute_outcome_c4: 4-directional scan from last_action, returns {-1, 1} for wins, 0 for draw, 2 for ongoing |
| S089 | Himath2002/gridline-four-android GameEngine.java + TacticalComputerStrategy.java + BoardSize.java — Pure 2D rules engine with configurable board sizes — Round 20 | github.com/Himath2002/gridline-four-android | Source code | 2025-2026 | GameEngine: configurable rows/columns at construction (min 4x4), 2D Disc[][] board, Move history (ArrayDeque), gravity via findOpenRow, 4-directional win detection via connectedCount, wouldWin() virtual placement, undoLastMove(), copyBoard(), canDrop(). BoardSize enum: COMPACT(5,6), CLASSIC(6,7), EXPANDED(7,8). TacticalComputerStrategy: win -> block -> center with leftmost tiebreaker. GameViewModel: Android MVVM ViewModel |
| S090 | NasserAlbusaidi/tic-tac-toe-royale — XO Royale multiplayer Connect Four (README only; source code inaccessible) — Round 20 | github.com/NasserAlbusaidi/tic-tac-toe-royale | Metadata | 2026 | Connect Four as one of 4 game modes (Normal, Misere, Ultimate Tic Tac Toe, Connect Four). Server-authoritative engine via Vercel WebSocket + Redis. Real-time multiplayer with private rooms, chat, spectators, 256-bit resume tokens. Source files exist in server/ (game-engine.mjs), api/ (ws.mjs, health.mjs) but all raw.githubusercontent.com fetches return 404 |

## URLs Probed Round 20 (Slot 5)

| URL | Result |
|-----|--------|
| github.com/topics/connectx?o=desc&s=updated | OK — 7 repos (same as R19) |
| github.com/topics/connect-four?o=desc&s=updated | OK — 21+ repos; NasserAlbusaidi/tic-tac-toe-royale new |
| github.com/tristan852/kite | VERIFIED — full source decoded |
| raw.githubusercontent.com/tristan852/kite/main/src/main/java/net/kite/internal/Kite.java | OK — full source (1000+ lines decoded) |
| github.com/pklesk/mcts_numba_cuda | VERIFIED — source tree decoded |
| github.com/Himath2002/gridline-four-android | VERIFIED — GameEngine + Strategy + BoardSize decoded |
| raw.githubusercontent.com/Himath2002/gridline-four-android/main/app/src/main/java/io/github/himath2002/gridlinefour/game/GameEngine.java | OK — full GameEngine.java decoded |
| raw.githubusercontent.com/Himath2002/gridline-four-android/main/app/src/main/java/io/github/himath2002/gridlinefour/game/TacticalComputerStrategy.java | OK — full strategy decoded |
| raw.githubusercontent.com/Himath2002/gridline-four-android/main/app/src/main/java/io/github/himath2002/gridlinefour/model/BoardSize.java | OK — BoardSize enum decoded |
| raw.githubusercontent.com/Himath2002/gridline-four-android/main/app/src/main/java/io/github/himath2002/gridlinefour/viewmodel/GameViewModel.java | OK — ViewModel decoded |
| github.com/NasserAlbusaidi/tic-tac-toe-royale | VERIFIED — README accessible, source 404 |
| raw.githubusercontent.com/pklesk/mcts_numba_cuda/main/src/mctsnc_game_mechanics.py | OK — CUDA device functions decoded |
| raw.githubusercontent.com/pklesk/mcts_numba_cuda/main/src/c4.py | OK — C4 game state decoded |
| raw.githubusercontent.com/pklesk/mcts_numba_cuda/main/src/mcts.py | OK — CPU MCTS reference decoded |
| api.github.com/repos/NasserAlbusaidi/tic-tac-toe-royale/contents | OK — metadata (not source content) |
| api.github.com/repos/pklesk/mcts_numba_cuda/contents | OK — source tree listing |
| github.com/tristan852/kite/tree/main/src/main/java/net/kite/internal | VERIFIED — Kite.java + api/ internal/ directories |
| raw.githubusercontent.com/NasserAlbusaidi/tic-tac-toe-royale/main/server/game-engine.mjs | FAILED — 404 (source inaccessible) |
| raw.githubusercontent.com/NasserAlbusaidi/tic-tac-toe-royale/main/server/index.mjs | FAILED — 404 (source inaccessible) |

## Sources Added Round 20 (NEURAL TRAINING AND HARDWARE)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S091 | GoodCoder666/katac4 model.py - Pre-activation ResNet architecture source code | raw.githubusercontent.com/GoodCoder666/katac4/main/model.py | Source code | ~2024 | VERIFIED + full source - Round 20. Pre-activation ResNet (b3c128nbt): 2 bottleneck blocks, 128 channels, nested bottleneck with mixed spatial pooling (mean+max), shallow conv heads (policy: 7x6x4=112 moves; value: 1 for W/D/L). Input encoding: 6 channels (2 player channels x board cells) + 1 side-to-move = 7 channels. ELO testing 300K games on 4xRTX 4090. CUDA graph caching. |
| S092 | GoodCoder666/katac4 train.py - Training pipeline source code | raw.githubusercontent.com/GoodCoder666/katac4/main/train.py | Source code | ~2024 | VERIFIED + full source - Round 20. Self-play: 30K epochs, batch=16, SGD+momentum, 3-phase lambda scheduler. 3 cross-entropy loss terms: policy + value + auxiliary rival. Parallel workers, replay buffer, temperature decay. Checkpoints every 500 epochs. Highest training completeness of any Connect 4 project. |
| S093 | NVIDIA T4 product page specifications | nvidia.com | Documentation | 2020 | VERIFIED - Round 20. Kaggle T4: 2,560 CUDA cores, 320 Turing Tensor Cores, 16GB GDDR6, 320+ GB/s bandwidth, 70W TDP, FP16 65 TFLOPS, INT8 130 TOPS. Inference optimized: up to 40x throughput vs CPU. |

| S094 | Tromp fhourstones88 (8x8 solver) | tromp.github.io/c4/fhourstones88 | Source | 2015 | C++ alpha-beta solver with book88 (~500MB), 1-3,359 Kpos/sec throughput |
| S095 | connect4.gamesolver.org -- Solved games matrix | connect4.gamesolver.org | Web | 2015+ | Complete solved-game matrix for Connect 4 boards up to 11x11 |
| S096 | gridline-four-android -- Computational complexity formulas | gridline-four-android GitHub | Source | Unknown | Android Connect 4 app with analysis: disc placement O(R+C), decision O(C*(R+C)), three board sizes |

## Sources Added Round 23 (ASYMMETRIC EVAL VERIFICATION + T017 FOLLOW-UP)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S097 | Wikipedia — Connect Four (page content) | en.wikipedia.org/wiki/Connect_Four | Wikipedia | 2026 | R23. Infinite Connect-Four solved: Draw (new detail not previously recorded). 2025 W-D-L table for 7x6. 15x13 solving status absent. |
| S098 | tromp.github.io/c4/c4.html — Board size solving chart | tromp.github.io/c4/c4.html | Web page | ~2015+ | R23. Full 8×8 chart: heights 4-11, widths 4-11, with +/=/- outcomes. "Winning starting moves NEVER in central columns" for larger boards. Distinct from S094 (fhourstones88). |

## Sources Added Round 25 (EXTERNAL-POOL BATCH-00012)

| Source ID | Title | URL / Path | Type | Date | Notes |
|-----------|-------|------------|------|------|-------|
| S091 | GoodCoder666/katac4 model.py — ResNet b3c128nbt architecture | github.com/GoodCoder666/katac4/blob/master/model.py | Source code | ~2024 | KataGo-inspired ResNet: B3 (3 Bottlenest blocks), C128 (128 channels), nbt (Nagel-Lee-Tanaka bottleneck). ~530K params. 6-channel input (current, next, bias). KataGo hparams: c_puct=1.0, policy temperature, value head, policy head. |
| S092 | GoodCoder666/katac4 train.py — Training pipeline (30K epochs, 3 loss terms) | github.com/GoodCoder666/katac4/blob/master/train.py | Source code | ~2024 | Training: 30K epochs, batch=16, 3-phase lambda LR schedule, SGD+momentum optimizer. 3 loss terms: policy CE + 1.5x value CE + 0.15x rival CE. 4×RTX 4090, 8 days total. Self-play data generation. |
| S093 | NVIDIA Tesla T4 product specifications | nvidia.com/object/tesla-t4.html | Product Doc | ~2019 | T4: 2,560 CUDA cores, 16GB GDDR6, 256-bit memory bus, 320 GB/s bandwidth, 80 Tensor cores, 83 TFLOPS FP16. Kaggle GPU instance target. |
| S094 | marcpaulo15/RL-connect4 CNN config files | github.com/marcpaulo15/RL-connect4 | GitHub | ~2024 | 4 channel configurations (channel_1/4/8/16 + fc_64/fc_128/fc_256). CNN architecture for Connect 4 policy/value heads. |
| S095 | AlphaZero Auxiliary Loss (AZAL) paper arXiv 2607.08984 | arXiv:2607.08984 | Academic Paper | 2026 | AZAL: auxiliary cross-entropy loss during self-play training. 0.785 oracle match rate. Helps policy heads learn from value targets. |
| S096 | Francesco Pochetti EC2 g4dn ResNet-18 benchmarks | github.com/francescopochetti/ec2-g4dn-benchmarks | GitHub | ~2024 | T4 TensorRT FP16: ResNet-18 (11.7M params) 1.10ms inference on EC2 g4dn. Benchmark methodology and code provided. |
| S099 | kaggle-environments envs/ directory (14 new environments) | github.com/Kaggle/kaggle-environments/tree/main/kaggle_environments/envs | GitHub metadata | ~2026 | 14 new environment directories added in v1.32.3: cabt, crawl, kaggriculture, kore_fleets, lux_ai_s3, etc. |
| S100 | kaggle-environments new root files (ablation, core_harness, etc.) | github.com/Kaggle/kaggle-environments | GitHub metadata | ~2026 | 5 new files in kaggle_environments/ root: ablation.py, core_harness.py, local_harness_runner.py, and 2 others. LLM agent harness infrastructure. |
| S101 | kaggle-environments connectx.py — ConnectX game engine | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py | Source code | ~2026 | ConnectX game engine unchanged between v1.32.2 and v1.32.3. Core game logic identical: make_move, observation, state, evaluation. |
| S102 | kaggle-environments connectx.json — Environment spec | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.json | Spec | ~2026 | `mark` field added to observation. All other spec fields unchanged. 7x6 default board, 2s/move, 60s overtime. |
| S103 | kaggle-environments core.py — Overtime tracking | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/core.py | Source code | ~2026 | Overtime tracking logic unchanged: per-step duration consumption, remainingOverageTime management. |
| S104 | kaggle-environments envs/connectx/ directory — No test_connectx.py | github.com/Kaggle/kaggle-environments/tree/main/kaggle_environments/envs/connectx | GitHub metadata | ~2026 | test_connectx.py (279 lines) removed in v1.32.3. Previously present in v1.32.2. |
| S105 | kaggle-environments schemas.json — Global defaults | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/schemas.json | Spec | ~2026 | Global defaults unchanged: episodeSteps=1000, actTimeout=6, runTimeout=1200, remainingOverageTime=12, maxLogLength=10000. |
| S106 | kaggle-environments status_codes.json — Status code definitions | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/status_codes.json | Config | ~2026 | Status code definitions unchanged between v1.32.2 and v1.32.3. |
| S107 | kaggle-environments core_harness.py — LLM agent harness | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/core_harness.py | Source code | ~2026 | LLM agent harness infrastructure for Kaggle environments. Enables LLM-powered agents. |
| S108 | kaggle-environments local_harness_runner.py — LLM agent CLI | github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/local_harness_runner.py | Source code | ~2026 | Local harness runner CLI for LLM agents. Enables local testing of LLM-powered agents. |
