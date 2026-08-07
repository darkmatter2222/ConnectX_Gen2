# Next Actions — ConnectX Phase 2

**Session:** Cycle 1
**Date:** 2026-08-06

## Immediate (this session)

1. ✅ Create phase2 control documents (in progress)
2. 🔄 Build ConnectX 7×6/4 rule engine (`connectx/engine.py`)
   - Board representation (flat array, 42 cells)
   - Legal move generation
   - Drop piece logic
   - Win detection (4 in a row: vertical, horizontal, both diagonals)
   - Draw detection (board full)
   - Deterministic state reproduction
   - Fixed legal starting positions support
3. ⏳ Write engine tests (`tests/test_engine.py`)
4. ⏳ Build baseline bots (`connectx/bots/`)
5. ⏳ Build tournament scheduler (`connectx/tournament.py`)
6. ⏳ Write integration tests
7. ⏳ Establish `.gitignore` and commit
8. ⏳ Set up venv at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`

## After engine is built and tested

9. Build seat-reversed paired evaluation
10. Build measured leaderboards
11. Add timing/overage enforcement
12. Register Kaggle builtin agents as baselines
13. Build bitboard alpha-beta bot (G1/G2 gate)
14. Build MCTS baseline