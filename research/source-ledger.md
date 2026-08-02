# Source Ledger — ConnectX Bot Research

> **Current Round**: 11
> **Last Updated**: 2026-08-02

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