# Submission Index — ConnectX Phase 2

| # | Date | Status | Candidate | Archive | Commit |
|---|------|--------|-----------|---------|--------|
| 4 | 2026-08-08 | PASS (research) | v2_8x7_5_p2 (P2-exploit, defensive eval) | [v0008](manifests/v0008.json) | [`2fb52e7`](https://github.com/ryansusman/ConnectX_Gen2/commit/2fb52e7) |
| 3 | 2026-08-07 | PASS (research) | v2_8x7_5_booked (8x7/5 depth-6 dual-book) | [v0007](manifests/v0007.json) | [`279b8b7`](https://github.com/ryansusman/ConnectX_Gen2/commit/279b8b74fa76df6b7ffa593cf8f56499a763636d) |
| 2 | 2026-08-07 | PASS (research) | v2_8x7_5_booked (8x7/5 depth-5 dual-book) | [v0006](manifests/v0006.json) | [`670fd4d`](https://github.com/ryansusman/ConnectX_Gen2/commit/670fd4d29b65e6659f9d006ff44fd30229e91b3c) |
| 1 | 2026-08-07 | READY_FOR_MANUAL_UPLOAD | v2_7x6_4 (Kaggle self-contained AB) | [v0001](manifests/v0001.json) | [`a711d3b`](https://github.com/ryansusman/ConnectX_Gen2/commit/a711d3b066e722c9b3b736e7f686a4a0671fcb20) |

**Total submissions:** 4

---

## v0006 — v2_8x7_5_booked (8×7/5 Dual-Book Research)

- **Status:** PASS (research — non-self-contained)
- **Candidate:** v2_8x7_5_booked — v2 alpha-beta with dual-book fallback for 8×7/5 (booked comparison validates: 10W-0L vs regular v2, 16W-0L vs PUCT MCTS)
- **Archive:** `connectx_submission_v0006.tar.gz`
- **O-Drive Path:** `O:\master_model_collection\ConnectX_Gen2_Phase2\submissions\connectx_submission_v0006.tar.gz`
- **SHA-256:** `1fedca5368fced9db2c1e71ea5f555de5df35ec37f1a1e5849864b3d691222ca`
- **Compressed Size:** 1,328 bytes
- **Extracted Size:** 3,368 bytes
- **Validation:** PASS (structural checks only; import/runtime skipped — non-self-contained bot)
- **Main.py hash:** `1e040dcb1ffabcdc0d94fb17c58eaf854698d54e67b0978c1a437914b6bc25ae`
- **Parent submission:** (none — first 8×7/5 release)
- **Change summary:** 8×7/5 v2 alpha-beta with dual opening book fallback. Validated by 120-game comparison.

---

## v0008 — v2_8x7_5_p2 (P2-Exploit Research)

- **Status:** PASS (research — non-self-contained)
- **Candidate:** v2_8x7_5_p2 — P2-exploit alpha-beta with defensive evaluation
- **Archive:** `connectx_submission_v0008.tar.gz`
- **O-Drive Path:** `O:\master_model_collection\ConnectX_Gen2_Phase2\submissions\connectx_submission_v0008.tar.gz`
- **SHA-256:** `5a354f954bcfb4b0c5def123a6e910cc445f2d0902ac6a600dcfb7548cc490bd`
- **Compressed Size:** 5,400 bytes
- **Extracted Size:** 23,020 bytes
- **Validation:** PASS (structural; research bot — import/runtime skipped)
- **Change summary:** P2-exploit bot with defensive evaluation (8×7/5)

---

## v0001 — v2_7x6_4 (Kaggle Self-Contained)

- **Status:** READY_FOR_MANUAL_UPLOAD
- **Candidate:** v2_7x6_4 — v2 alpha-beta with iterative deepening, transposition table, killer moves, history heuristic, null-move pruning (7×6/4)
- **Archive:** `connectx_submission_v0001.tar.gz`
- **O-Drive Path:** `O:\master_model_collection\ConnectX_Gen2_Phase2\submissions\connectx_submission_v0001.tar.gz`
- **SHA-256:** `8b7b06591e081e0fef87e9dc873533ee4c4b57a62b4960ebda6cb906d834cff2`
- **Compressed Size:** 5,638 bytes
- **Extracted Size:** 22,919 bytes
- **Validation:** PASS (import OK, runtime: returns col 3 on empty board, 20 moves 0 invalid)
- **Main.py hash:** precomputed at build time
- **Parent submission:** (none — first release)
- **Change summary:** Initial submission — v2 alpha-beta self-contained for Kaggle 7×6/4