# Source Ledger — ConnectX Bot Research

> **Current Round**: 6
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