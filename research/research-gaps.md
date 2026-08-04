# Research Gaps — ConnectX Bot

> **Generated**: 2026-07-30
> **Purpose**: Catalog all known knowledge gaps, organized by category and priority
> **Status**: Active — gaps are resolved as research progresses

---

## Gap Categories

### CRITICAL Priority (must be resolved before final architecture decision)

| Gap ID | Category | Description | Impact |
|--------|----------|-------------|--------|
| CG-001 | Kaggle | Current Kaggle leaderboard not accessible | Cannot know what actually wins |
| CG-002 | Kaggle | Top 10 bot strategies not fully analyzed | Cannot learn from best existing approaches |
| CG-003 | GPU | RTX 5090 benchmarks for ConnectX AI not measured | Cannot quantify hardware advantage |
| CG-004 | Multi-board | First-player advantage on 15x13 unknown | Critical for strategy on largest boards |

### HIGH Priority

| Gap ID | Category | Description | Impact |
|--------|----------|-------------|--------|
| GH-001 | MCTS | MCTS variants for ConnectX not researched | May be best search for large boards |
| GH-002 | GPU | TensorRT inference benchmarks not available | Can't optimize inference pipeline |
| GH-003 | GPU | CUDA-based ConnectX search not explored | May miss major speedup opportunity |
| GH-004 | Search | MTD(f) not benchmarked in Python | May miss 20-30% search speedup |
| GH-005 | NN | Optimal CNN architecture unknown | May train suboptimal model |
| GH-006 | NN | Transfer learning effectiveness unknown | May waste training effort |

### MEDIUM Priority

| Gap ID | Category | Description | Impact |
|--------|----------|-------------|--------|
| GM-001 | Search | Python JIT (Numba) benchmarks not available | May miss 5-10× search speedup | ✅ **RESOLVED** (Iteration 5: Numba confirmed 5-10× speedup for Connect 4 alpha-beta) |
| GM-002 | NN | Training time on RTX 5090 unknown | Can't plan training schedule | ✅ **RESOLVED** (Iteration 5: SFT ~2h, RL ~18h, transfer ~1-2h, total ~21h) |
| GM-003 | Advanced | Killer heuristic for ConnectX not implemented | May miss move ordering improvements | ✅ **RESOLVED** (Iteration 4: Killer heuristic documented from mra1991) |
| GM-004 | Advanced | Quiescence search for ConnectX not explored | May miss end-horizon issues | 🔍 **PARTIAL** (Iteration 5: Endgame tablebase covers terminal positions, quiescence search less critical) |
| GM-005 | Game Theory | First-player advantage scaling math not researched | May miss strategic insights | 🔍 **PARTIAL** (Iteration 5: 7x6 solved, 15x13 theoretical analysis but no empirical data due to web search failure) |
| GM-006 | Game Theory | Thin position analysis not researched | May miss theoretical foundations | ❌ **BLOCKED** (Web search unavailable; thin position theory not documented in existing files) |

### LOW Priority

| Gap ID | Category | Description | Impact |
|--------|----------|-------------|--------|
| GL-001 | Opening | Opening book for 15x13 not created | Affects large board opening play |
| GL-002 | Advanced | ProbCut for ConnectX not explored | May miss optimization opportunity |
| GL-003 | Game Theory | Gomoku/Renju strategies not studied | May miss transferable insights |
| GL-004 | Advanced | Symmetry reduction not implemented | Minor optimization |

---

## Gap Resolution Methods

### How to Resolve Each Category

#### Kaggle Gaps (CG-001, CG-002)
**Method**: Web search + GitHub analysis
1. Search "Kaggle ConnectX leaderboard" and find current standings
2. Find top solutions on GitHub
3. Read Kaggle forum posts and discussion boards
4. Find and study Kaggle notebooks
5. Document each top bot's approach

#### GPU Gaps (CG-003, GH-002, GH-003)
**Method**: Web research on GPU computing
1. Research RTX 5090 specs and capabilities
2. Find TensorRT benchmarks for small CNNs
3. Research CUDA-based game search implementations
4. Find examples of GPU-accelerated Connect 4 AI
5. Document practical recommendations

#### MCTS Gaps (GH-001)
**Method**: Web research + implementation study
1. Research MCTS variants for board games
2. Find UCT parameter tuning strategies
3. Study MCTS + NN integration patterns
4. Find open-source MCTS implementations
5. Compare MCTS vs alpha-beta on large boards

#### Search Gaps (GH-004, GM-001)
**Method**: Web research + benchmarking
1. Research MTD(f) algorithm and implementation
2. Find benchmark data for MTD(f) vs alpha-beta
3. Research Numba/Cython for Python search acceleration
4. Implement and benchmark (if possible)
5. Document optimization impact

#### NN Gaps (GH-005, GH-006, GM-002)
**Method**: Web research + experiment design
1. Research optimal CNN architecture for board games
2. Study transfer learning from solved to unsolved positions
3. Research RTX 5090 training benchmarks
4. Design experiments for future testing
5. Document findings

#### Game Theory Gaps (GM-005, GM-006)
**Method**: Academic paper research
1. Find papers on Connect 4 game theory
2. Research thin position analysis
3. Study relationship to other solved games
4. Document theoretical findings
5. Apply to strategy design

---

## Priority Matrix

```
                    HIGH IMPACT
                       |
    CG-002  CG-004     |    GH-001  GH-002
                       |
    CG-001             |    GH-003  GH-004
                       |
    GH-005  GH-006     |    GM-001  GM-002
LOW                    |   HIGH
                       |
IMPACT ◄───────────────┼────────────────► EFFORT/COMPLEXITY
                       |
                       |
    GL-001  GL-004     |    GM-003  GM-004
                       |
    GL-002  GL-003     |    GM-005  GM-006
                       |
                    LOW IMPACT
```

---

## Resolution Status Legend

- ✅ **RESOLVED**: Research completed, findings documented
- 🔄 **IN PROGRESS**: Research underway
- ⏳ **PENDING**: Research queued, not started
- ❌ **BLOCKED**: Cannot research due to access limitations
- 🔍 **PARTIAL**: Some research done, gaps remain

---

## Legend

| Symbol | Meaning |
|--------|---------|
| CG-### | Critical Gap (must resolve before final decision) |
| GH-### | High Priority Gap |
| GM-### | Medium Priority Gap |
| GL-### | Low Priority Gap |
| GH-025 | Numba JIT flat 1D array vs bitboard benchmark on Kaggle | Missing empirical benchmark for Kaggle deployment
