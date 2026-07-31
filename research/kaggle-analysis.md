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