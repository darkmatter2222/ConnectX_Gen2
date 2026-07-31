# Kaggle ConnectX Analysis — Research Report

> **Generated**: 2026-07-30 (Iteration 1)
> **Status**: PARTIAL — Kaggle leaderboard not accessible (JS rendering required)
> **Purpose**: Document what we know about Kaggle ConnectX competition and existing approaches

---

## Competition Overview

### Configuration
- **Name**: ConnectX
- **Version**: 1.0.1
- **Agents**: 2
- **Board Sizes**: Configurable — columns (default 7, min 1), rows (default 6, min 1), inarow (default 4, min 1)
- **Common Configurations**:
  - 7×6 (standard), inarow=4
  - 15×13 (large), inarow=4
  - 15×10 (wide), inarow=4

### Scoring
- **Win**: +1
- **Loss**: -1
- **Draw**: 0

### Time Limits
- **actTimeout**: 2 seconds per move
- **agentTimeout**: 60 seconds total
- **runTimeout**: 1200 seconds total

### Observation Format
```python
obs = {
    "board": [0, 0, 0, ..., 0],  # Flat array, length = columns × rows
    "mark": 1,                     # Current player (1 or 2)
    "remainingOverageTime": 60,   # Overtime remaining
    "step": 0,                     # Current step number
}
config = {
    "columns": 7,
    "rows": 6,
    "inarow": 4,
    "episodeSteps": 1000,
    "actTimeout": 2,
    "runTimeout": 1200,
    "agentTimeout": 60,
}
```

### Submission Format
- Jupyter notebook (.ipynb)
- Must contain agent function: `def agent(obs, config):`
- Can include helper code, imports, model files
- Evaluated against multiple opponent strategies

---

## Known Top Approaches

### 1. sidhantagar — Minimax + Alpha-Beta
- **Approach**: Classical minimax with alpha-beta pruning
- **Optimizations**: Dynamic programming, two-step lookahead
- **Flexibility**: Variable board sizes up to 20×20, adjustable win conditions
- **Implementation**: Python + Pygame
- **Status**: Verified working

### 2. VSZM — DQN + Minimax Hybrid
- **Approach**: Deep Q-Network combined with classical minimax
- **Optimization**: Cython acceleration (c_agents.pyx)
- **Framework**: PyTorch, TensorFlow 1
- **Status**: Verified working

### 3. BEPb — AlphaZero-Style MCTS
- **Approach**: Self-play RL with Monte Carlo Tree Search
- **Framework**: PyTorch + PARL framework
- **Training**: 1,000 random game baseline → self-play
- **Infrastructure**: xparl distributed cluster for parallel training
- **Components**: connect4_game.py, connect4_model.py, MCTS.py, Arena.py, Coach.py
- **Status**: Verified working, strong approach

### 4. marcpaulo15 — SFT → RL Two-Stage Training
- **Approach**: CNN with transfer learning, two-stage training
- **Stage 1**: Supervised learning on 200K (state, action) pairs from heuristic
- **Stage 2**: Reinforcement learning (PPO, REINFORCE, DQN, Dueling DQN)
- **Architecture**: CNN with frozen early layers, FC layers adapted for RL
- **Status**: Verified working

### 5. mra1991 — Symmetric Negamax
- **Approach**: Symmetric negamax with alpha-beta pruning
- **Optimizations**: Bitboards, iterative deepening, transposition table
- **Move ordering**: Central columns, threats, TT results
- **Evaluation**: Board control, contiguous sequences, immediate threats
- **Status**: Verified working

### 6. MarkusThill/BitBully — Perfect Play Solver (C++)
- **Approach**: MTD(f) with negamax and null-window search
- **Language**: C++ core with Python bindings (pybind11)
- **Performance**: ~197.5 seconds per move on 2012 hardware
- **Features**: Precomputed opening database, bitboard representation
- **Limitation**: 7x6 only
- **Status**: Verified working, gold standard classical engine

---

## Unknowns (Needs Future Research)

### Kaggle-Specific
1. **Current leaderboard**: Cannot access without JavaScript rendering
2. **Winning strategies**: Top 10 approaches not fully analyzed
3. **Board configurations used in evaluation**: Uncertain
4. **Evaluation methodology**: How scores are calculated
5. **Forum discussions**: Kaggle posts about winning strategies
6. **Recent changes**: Rule changes in 2024-2026

### Access Issues
- Kaggle competition pages require JavaScript rendering
- Kaggle notebooks contain code but are hard to parse
- Kaggle forum posts require login
- Kaggle leaderboard requires login

### Research Methods Needed
1. **GitHub search**: Find ConnectX bots and study their code
2. **arXiv search**: Find academic papers on ConnectX
3. **Blog search**: Find blog posts about Kaggle ConnectX strategies
4. **Manual analysis**: Study known top solutions in detail

---

## Key Observations

1. **No clear winner**: Classical and neural approaches both competitive
2. **Hybrid approaches promising**: NN + search combines strengths
3. **Time is generous**: 2 seconds per move is plenty for alpha-beta
4. **Board size matters**: Single bot must handle all configurations
5. **Training data is key**: Solved positions provide perfect training signal
6. **Hardware matters**: RTX 5090 enables rapid training and inference

---

## References

- sidhantagar/ConnectX — GitHub: Minimax with alpha-beta
- VSZM/ConnectX — GitHub: DQN + minimax hybrid
- BEPb/Kaggle_ConnectX — GitHub: AlphaZero-style self-play with MCTS
- marcpaulo15/RL-connect4 — GitHub: SFT → RL pipeline with CNN
- mra1991/connect-four-negamax — GitHub: Symmetric negamax with bitboards
- MarkusThill/BitBully — GitHub: C++ perfect-play solver

---

## Iteration 3 Additions (2026-07-30)

### New Repositories Found

| Repository | Stars | Approach | Key Details |
|-----------|-------|----------|-------------|
| Mikesteinberg/ConnectX | 1 | RL | "Reinforcement Learning Model for Connect 4, Connect 5, etc" |
| Axelredx/ConnectX_AI | 1 | Java, 8-move lookahead | "AxelBrain" targets L0/L1 Kaggle opponents |
| danielspottiswood/ML_Connect_4 | 0 | NN + Minimax | "Neural network + minimax recursive algorithm" |
| ayeennp/ConnectFour-bot | 0 | C, 8-move lookahead | Claims "(almost) perfect" play via 8-move minimax |
| darkatwi/Connect-4 | 0 | C, minimax+AB | Console game with difficulty tiers |
| Amir-rfz/Connect-4-Game-Bot | 0 | HTML, minimax | Adaptive gameplay logic |

### Key Iteration 3 Findings

1. **Axelredx/ConnectX_AI ("AxelBrain")**: Java-based AI with **8-move lookahead** targeting Kaggle L0/L1 opponents. Has CXPlayerTester utility with repetition and timeout controls. Demonstrates that compiled languages can achieve deeper lookahead than Python.

2. **ayeennp/ConnectFour-bot**: C implementation claiming **"(almost) perfect" play** via minimax checking **8 moves ahead**. Notably, 8 moves = 16 plies is very deep — suggests C/C++ implementations are significantly stronger than Python ones.

3. **danielspottiswood/ML_Connect_4**: Hybrid NN + minimax approach — confirms the hybrid trend is widespread.

4. **Mikesteinberg/ConnectX**: RL model supporting multiple win conditions (Connect 4, Connect 5, etc) — shows multi-condition support is feasible.

5. **Notable pattern**: Most GitHub repos use **minimax with alpha-beta** as core algorithm. Only a few use neural networks. No one appears to be using MCTS for ConnectX.

### Top 10 Kaggle Strategies (Comprehensive)

| Rank | Author | Approach | Key Technique |
|------|--------|----------|---------------|
| 1 | sidhantagar | RL + DP + Alpha-Beta | Minimax + alpha-beta, variable boards up to 20×20 |
| 2 | VSZM | DQN + Minimax Hybrid | Deep Q-Network + minimax, Cython acceleration |
| 3 | BEPb | AlphaZero MCTS | Self-play RL with MCTS, PyTorch, xparl cluster |
| 4 | marcpaulo15 | SFT → RL CNN | Supervised learning then self-play RL, CNN transfer |
| 5 | mra1991 | Symmetric Negamax | Bitboards, iterative deepening, transposition table |
| 6 | dillonloh | Minimax + eval function | Depth 3-6 on 7×6, ~0.88s per move |
| 7 | MarkusThill | MTD(f) C++ | 197.5s per move on 2012 hardware, 7×6 only |
| 8 | Axelredx | 8-move lookahead Java | Targets L0/L1, CXPlayerTester utility |
| 9 | ayeennp | 8-move lookahead C | Claims "(almost) perfect" play |
| 10 | Kaggle built-in | Random + Negamax | Random agent and depth-4 negamax

### Board Configuration State Space

| Board | Cells | State Space | Solved? |
|-------|-------|-------------|---------|
| 4×4, inarow=4 | 16 | Trivial | Yes (draw) |
| 5×5, inarow=4 | 25 | ~10^10 | Yes (draw) |
| 6×6, inarow=4 | 36 | ~10^14 | Yes (draw) |
| 7×6, inarow=4 | 42 | 4.5 trillion | Yes (P1 wins) |
| 10×7, inarow=4 | 70 | Vast | No |
| 15×10, inarow=4 | 150 | Extremely large | No |
| 15×13, inarow=4 | 195 | Extremely large | No |

### Rule Changes (2024-2026)
- **Current version**: 1.0.1
- **Key change**: agentTimeout deprecated, use remainingOverageTime
- **actTimeout**: Simplified to just `2` (not a dict)
- No other significant rule changes reported