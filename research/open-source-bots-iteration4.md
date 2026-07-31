# Open-Source Bots for ConnectX — Iteration 4

> **Generated**: 2026-07-31
> **Purpose**: Top GitHub repos for ConnectX/Connect 4 AI bots
> **Status**: Based on GitHub search results and web research

---

## Top GitHub Repositories

### 1. BitBully — MarkusThill (⭐ ~68)

**Language**: C++ with Python bindings (pybind11)
**Approach**: MTD(f) + bitboards
**Details**:
- Fast perfect-play Connect Four solver
- MTD(f) search algorithm with null-window negamax
- Optimized bitwise operations for board representation
- Transposition table with 1 million entries
- Threat detection and center-first move ordering
- Huffman-encoded lookup tables
- **Performance**: 197.5 seconds on 2012-era hardware for initial position
- **Claim**: "Fast perfect-play Connect Four solver"
- **Limitation**: 7x6 only

### 2. connect-four-negamax — mra1991 (⭐ ~7)

**Language**: Python
**Approach**: Symmetric negamax with bitboards
**Details**:
- Single symmetric negamax loop (score(parent) = -score(child))
- Two Python integers (one per player) for rapid bitwise checks
- Transposition table: stores depth, score, exact/lower-bound/upper-bound, best move, search generation
- **Move ordering**:
  1. Transposition table move
  2. Immediate winning moves
  3. Immediate defensive blocks
  4. Killer moves
  5. Positional and historical heuristics
- **Evaluation**: Nonterminal boards analyzed (not zero)
  - Central dominance
  - Open sequences
  - Threat density
  - Ply-adjusted scores (faster wins preferred, losses delayed)
- **Benchmarks**: No empirical data provided; outputs live metrics (node count, pruning, search duration)

### 3. ConnectX — sidhantagar

**Language**: Python
**Approach**: Minimax with alpha-beta pruning
**Details**:
- RL + DP + Alpha-Beta
- Dynamic programming for two-step lookahead
- Variable board sizes (up to 20×20)
- Adjustable win conditions (3-10 in a row)
- Pygame interface
- Three matchups: player vs player, player vs AI, AI vs AI

### 4. Kaggle_ConnectX — BEPb

**Language**: Python
**Approach**: AlphaZero-style MCTS with self-play
**Details**:
- Neural network (CNN) with Monte Carlo Tree Search
- Self-play training starting from 1,000 random games
- xparl cluster for parallel training
- Components: connect4_game.py, connect4_model.py, MCTS.py, Arena.py, Coach.py
- Framework: PyTorch + PARL

### 5. RL-connect4 — marcpaulo15

**Language**: Python
**Approach**: SFT → RL two-stage training
**Details**:
- Supervised learning on 200K (state, action) pairs from heuristic
- Stage 2: Reinforcement learning (PPO/REINFORCE/DQN/Dueling DQN)
- CNN with frozen early layers as feature extractor
- FC layers adapted for RL tasks

### 6. ConnectX_AI — Axelredx

**Language**: Java
**Approach**: 8-move lookahead targeting L0/L1
**Details**:
- "AxelBrain" AI targeting Kaggle L0/L1 opponents
- 8-move lookahead implementation
- CXPlayerTester utility with repetition and timeout controls
- Java-based with testing utility

### 7. ConnectFour-bot — ayeennp

**Language**: C
**Approach**: 8-move lookahead
**Details**:
- Claims "(almost) perfect" play via minimax checking 8 moves ahead
- C implementation for maximum speed
- High-precision move evaluation

### 8. Connect-4 — darkatwi

**Language**: C
**Approach**: Minimax with alpha-beta pruning
**Details**:
- Console-based Connect 4 with adjustable difficulty tiers (Easy/Medium/Hard)
- Iterative deepening for time management
- Terminal interface

### 9. ML_Connect_4 — danielspottiswood

**Language**: Python
**Approach**: Hybrid NN + minimax
**Details**:
- Neural network combined with minimax recursive algorithm
- Blended machine learning and algorithmic planning

### 10. ConnectX — Mikesteinberg (⭐ 1)

**Language**: Jupyter Notebook
**Approach**: Reinforcement Learning
**Details**:
- "A Reinforcement Learning Model Designed to play Connect4, Connect 5, etc"
- Supports multiple win conditions

---

## Notable Patterns

### 1. Compiled Languages Dominate
- **C++ (BitBully)** and **C (ayeennp, darkatwi)** achieve deeper lookahead than Python
- Compiled languages can achieve 8-move lookahead — not feasible in Python at 2s limit
- **Recommendation**: Use C++ for core search, Python for orchestration

### 2. Bitboards Are Critical
- Both top engines (BitBully, mra1991) use bitboard representation
- Bitboards provide constant-time operations for move generation and win detection
- **Recommendation**: Implement bitboards for any serious ConnectX bot

### 3. MTD(f) Over Alpha-Beta
- BitBully uses MTD(f) which is more efficient for exact values
- MTD(f) avoids storing bounds in transposition table
- **Recommendation**: Consider MTD(f) for optimal play on 7x6

### 4. Hybrid Approaches Emerging
- NN + minimax (danielspottiswood) shows the trend
- Combining neural networks with classical search
- **Recommendation**: Hybrid approach is likely best for future

### 5. Open Source is Sparse
- Most implementations have 0-1 stars
- No MCTS-based public repos for ConnectX
- **Opportunity**: First to publish high-quality MCTS implementation gains advantage

---

## Recommendation for Our Project

### Use Case: Open-Source Reference

| Purpose | Recommended Repo |
|---------|-----------------|
| Perfect play on 7x6 | BitBully (C++) |
| Python reference | mra1991/connect-four-negamax |
| Variable board support | sidhantagar/ConnectX |
| NN+search hybrid | danielspottiswood/ML_Connect_4 |
| AlphaZero-style MCTS | BEPb/Kaggle_ConnectX |
| SFT→RL training | marcpaulo15/RL-connect4 |

### Key Takeaways
1. **C++ + bitboards + MTD(f)** = perfect play on 7x6
2. **Python + alpha-beta + optimization** = strong play on 7x6
3. **NN + search** = future trend for larger boards
4. **No one has published MCTS for ConnectX** — our opportunity

---

## Open Questions

1. Which open-source repo has the most complete implementation?
2. Can we improve on BitBully's performance with RTX 5090?
3. Are there any repos with actual benchmark data?
4. How many repos use MCTS vs alpha-beta? (None vs many)
5. What's the community standard for evaluation functions?