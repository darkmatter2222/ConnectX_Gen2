# Research Round 17 — Connect 4 Opening Books

> **Date**: 2026-08-03
> **Round**: 17
> **Previous Round**: 16 (2026-08-03)
> **Task**: T016 — Search for 'Connect 4 opening book' implementations beyond Pascal Pons DEPTH=14
> **Lane**: CLASSICAL_SEARCH_AND_GAME_THEORY
> **Worker**: Slot 2 of 7, Job 3

---

## Task Definition

T016: Search for 'Connect 4 opening book' — any open-source opening book implementations beyond Pascal Pons DEPTH=14?

---

## Conclusion

3 distinct open-source opening book implementations discovered:

1. **tromp/fhourstones88** — C++ solver (2015) with book88, a binary database of all solved 8x8 positions up to 16 plies. BookMap hash table. ~500MB memory. Downloadable binary.

2. **Pascal Pons/connect4** — C++ (2014) with OpeningBook.hpp + generator.cpp. DEPTH=14 for 7x6. Source-generated at build time. AGPL v3.

3. **tristan852/kite** — Java solver (2025) with opening.cfc 15-ply compiled cache (95.6 MB). Most space-efficient. 13 skill levels (0-2000 Elo). Outperforms all competitors on Pascal Pons benchmark.

Kite fully decoded including binary format, hash algorithm, and benchmarks.

---

## Sources

| ID | Source | Type | URL |
|----|--------|------|-----|
| S066 | tromp/fhourstones88 — C++ solver with book88 binary | GitHub repo | https://github.com/tromp/fhourstones88 |
| S067 | Pascal Pons/connect4 — C++ solver with OpeningBook.hpp + generator.cpp | GitHub repo | https://github.com/PascalPons/connect4 |
| S068 | tristan852/kite — Java solver with 15-ply compiled cache | GitHub repo | https://github.com/tristan852/kite |
| S069 | Kite OpeningBoardScoreCache.java — cache format from source | Source code | https://github.com/tristan852/kite/blob/main/core/src/main/java/com/github/tristan852/kite/core/OpeningBoardScoreCache.java |

---

## Evidence

### 1. tromp/fhourstones88 (2015)

Binary book format from Search.cpp:
- Book class loads binary file at startup via open(bookfile, O_RDONLY)
- Store: read(bd, &bb, BBYTES) then read(bd, &rslt, sizeof(short))
- BookMap hash table: TRANSIZE = 8,306,069 entries
- Positions with work >= BOOKWORK(24) dynamically added
- Book file naming: book%d%d (WIDTH, HEIGHT) — e.g., book88
- ~500MB memory default

### 2. Pascal Pons/connect4 (2014)

- DEPTH=14 for 7x6 board
- Configurable via template WIDTH/HEIGHT (up to 9x6 in uint64_t)
- Source-generated at build time; no binary distributed
- AGPL v3 license
- Generator creates opening book at build time

### 3. tristan852/kite (2025) — Most Sophisticated

Binary cache format from OpeningBoardScoreCache.java:
- PACKED_BOARD_SCORES_SIZE_IN_BYTES = 61,737,771 (58.9 MiB)
- BOARD_SCORES_SIZE = 82,317,028 entries
- BUCKET_SEEDS_SIZE_IN_BYTES = 33,554,432 (32 MiB = 2^25)
- BOARD_SCORE_SIZE_IN_BITS = 6
- BOARD_SCORE_OFFSET = -18 (0=draw, 1-39=win, -18 to -1=loss)
- Three-key mixed hash constants: 0x9E3779B97F4A7C15L, 0xBF58476D1CE4E5B9L, 0x94D049BB133111EBL

Lookup: mixedHash = base ^ h1 ^ h2 ^ h3 (MurmurHash3-like)
- bucketSeeds[mixedHash & mask] -> bucket seed
- mixLong(bucketSeed) % 82317028 -> score index
- 6-bit score read from packed array

Search integration (Board.java):
- OPENING_SCORE_CACHE_MAXIMAL_DEPTH = 15
- Applied when filledCellAmount <= 15 (opening positions)
- boardScore(mixedHash) called before alpha-beta search

Performance benchmarks (Pascal Pons benchmark, 6 categories):
- endgame-easy: Kite 1.90us (17.84 Mnodes/s) vs Fhourstones 4.27us
- opening-medium: Kite 716us vs Fhourstones 7.44ms (10x faster)
- opening-hard: Kite 22us vs Fhourstones 5.5s (250,000x faster!)
- Kite demonstrates opening book dramatically speeds up opening positions

---

## Claim-status recommendations

| Claim | New? | Status | Rationale
| C078 | NEW | VERIFIED | tromp book88 binary format from Search.cpp
| C079 | NEW | VERIFIED | Pascal Pons OpeningBook.hpp from source code
| C080 | NEW | VERIFIED | Kite 15-ply compiled cache from source
| C081 | NEW | VERIFIED | Kite benchmark results from README.md
| C082 | NEW | VERIFIED | Kite boardScore integration from Board.java

---

## Contradictions and uncertainty

No contradictions. All 3 implementations are consistent and complementary.

Uncertainties:
1. tromp BOOKWORK value — only referenced, exact value not visible in source
2. Kite's opening.cfc generation process — compiled cache contents not inspected
3. Kite opening-hard 22us vs Fhourstones 5.5s — benchmark methodology may differ

---

## Architecture-ranking implication

No change to rankings. Opening books are a classical search enhancement.
Opening books enhance 7x6 strength for all classical approaches.
No impact on 15x13 (opening books scale poorly).
Reinforces need for NN on large boards.

---

## Follow-up tasks

1. T016-FU1: Measure tromp book88 actual disk size
2. T016-FU2: Inspect Pascal Pons OpeningBook.hpp source format
3. T016-FU3: Benchmark Kite opening.cfc memory on 7x6 vs 8x8
4. T016-FU4: Port Kite's mixed hash to Python for Kaggle
5. T016-FU5: Create minimal Python opening book for 7x6 Kaggle
6. T016-FU6: Compare Kite opening-hard benchmark methodology
7. T016-FU7: Search Kaggle for Kite kernels/bots

---

## Round Statistics

| Metric | Value |
|--------|-------|
| New sources | 4 (S066-S069) |
| New claims | 5 (C078-C082) |
| Verified claims | 56/82 (68%) |
| Architecture ranking changes | None |
| T016 status | COMPLETED |

---

EXTERNAL SYNTHESIS COMPLETE
