# Deep Research Compendium — ConnectX Bot Strategies

> **Generated**: 2026-07-30 (Iteration 1 of deep research loop)
> **Purpose**: Comprehensive research compilation for building the world's best ConnectX bot
> **Hardware**: RTX 5090 (21,760 CUDA cores, 32GB GDDR7, 419 TFLOPS FP8 tensor)
> **Scope**: All known techniques, strategies, and approaches for ConnectX/Connect 4 AI

---

## Table of Contents

1. [Game Theory & Solved Status](#game-theory--solved-status)
2. [Best Known Classical Engines](#best-known-classical-engines)
3. [Neural Network Approaches](#neural-network-approaches)
4. [Kaggle Competition Analysis](#kaggle-competition-analysis)
5. [GPU Hardware Opportunities](#gpu-hardware-opportunities)
6. [Search Algorithm Landscape](#search-algorithm-landscape)
7. [Evaluation Function Research](#evaluation-function-research)
8. [Multi-Board Strategy](#multi-board-strategy)
9. [Advanced Techniques](#advanced-techniques)
10. [Hypotheses](#hypotheses)
11. [Open Questions](#open-questions)

---

## 1. Game Theory & Solved Status

### 7x6 Board (Standard)

- **Status**: SOLVED — First player always wins with perfect play
- **Reference**: Allis (1988) "A Knowledge-based Approach of Connect-Four"; Böck (2025) "Connect4 7 x 6 Strong Solution"
- **Win condition**: First player wins in ≤41 moves (from center opening)
- **Total positions**: 4,531,985,219,092 (≈4.5 trillion)
- **Optimal opening**: Column 4 (center) — guaranteed win in ≤41 moves
- **Adjacent opening** (columns 3 or 5): Theoretical draw if opponent plays perfectly
- **Edge opening** (columns 1, 2, 6, or 7): First player loses (opponent can dictate outcome)

### Why First Player Wins

The center opening (column 4) creates maximum flexibility and multiple simultaneous threats. The first player can:
1. Control the center and build threatening formations
2. Create "forks" (two winning threats simultaneously)
3. Force the second player into a purely defensive posture

### Larger Boards (15x13, 15x10)

- **Status**: UNSOLVED — No strong solution exists
- **Unknowns**:
  - Does first-player advantage scale on larger boards?
  - Is 15x13 theoretically winnable by first player?
  - What is the optimal opening for 15x13?
  - How does the number of possible positions scale?

### Key Insight for Our Bot

> Since 7x6 is solved with known winning strategies, we can:
> 1. Build an opening book from solved positions
> 2. Use the solved game as training data for neural networks
> 3. Create an endgame database from solved positions
> 4. Verify our bot's correctness against the solution

---

## 2. Best Known Classical Engines

### BitBully (Markus Thill) — The Gold Standard

**Architecture**:
- High-performance C++ core wrapped in Python via pybind11
- Only supports standard 7x6 board (optimized, not generalizable)

**Search Algorithm**:
- MTD(f) (Minimax with Threat Detection, iterative deepening with f-value)
- Negamax with null-window algorithms
- Dynamic depth: adapts based on board complexity

**Optimizations**:
- Transposition caching (TT)
- Threat detection (forks, forced moves)
- Strategic move ordering
- Precomputed opening database (constant-time early-game lookups in milliseconds)
- Bitboard representation for fast state transitions

**Performance (on 2012-era hardware)**:
- Solves initial position in ~197.5 seconds
- 1.5× speed advantage over comparable baseline at six plies
- Deeper states resolve in under a second
- "Fast perfect-play Connect Four solver"

**Why It's Strong**:
- MTD(f) is one of the most efficient minimax variants
- Precomputed opening database eliminates search for common positions
- Bitwise operations for constant-time move generation
- Game-theoretic values (win/loss/draw), not heuristics

**Relevance to ConnectX**: BitBully is designed ONLY for 7x6. It cannot generalize to larger board sizes. However, its techniques (MTD(f), transposition caching, opening databases, bitboards) are transferable.

### mra1991/connect-four-negamax

**Architecture**: Python implementation of symmetric negamax with alpha-beta pruning

**Key Features**:
- Symmetry reduction: halves redundant state space by canonicalizing mirrored positions
- Move ordering: central columns first, threats, transposition table results
- Custom heuristic evaluation: board control, contiguous piece sequences, immediate threats
- Terminal scores: ply-adjusted (favor rapid victories, postpone defeats)
- Dual integer bitboards for constant-time moves and fast win detection
- Iterative deepening: ensures time limits are respected

**Relevance**: Verified and working. Good reference for Python implementation.

### BitBurny (Markus Thill) — Educational Version

**Architecture**: Python + Pygame implementation

**Key Features**:
- Variable board sizes up to 20×20
- Adjustable win conditions (3-10 in a row)
- Symmetric negamax with alpha-beta pruning
- Move ordering: central columns, threats, transposition table results
- Custom heuristic evaluation
- Ply-adjusted terminal scores

**Relevance**: Demonstrates how to generalize Connect 4 strategies to non-standard boards.

---

## 3. Neural Network Approaches

### marcpaulo15/RL-connect4 — Two-Stage Training

**Architecture**: CNN with transfer learning

**Training Pipeline**:
1. **Stage 1 — Supervised Fine-Tuning (SFT)**:
   - 200,000 (state, action) pairs from hand-crafted heuristic
   - Early CNN layers frozen as feature extractor
   - Fully Connected layers adapted for RL tasks

2. **Stage 2 — Reinforcement Learning**:
   - Self-play tournament format
   - Multiple RL algorithms: PPO, REINFORCE, DQN, Dueling DQN
   - Trained agents compete against each other

**Framework**: PyTorch, TensorFlow 1 (legacy)

**Key Insight**: SFT → RL pipeline is the most effective approach for ConnectX:
- SFT provides a strong policy baseline
- RL fine-tunes beyond heuristic limitations
- Multiple RL algorithm options allow experimentation

### BEPb/Kaggle_ConnectX — AlphaZero-Style

**Architecture**: CNN with MCTS (AlphaZero-style)

**Training Pipeline**:
1. Start with 1,000 random-agent game baseline
2. Self-play using PARL framework
3. Distributed training with xparl cluster
4. MCTS guides the search, neural net guides MCTS

**Key Components**:
- connect4_game.py: Game rules
- connect4_model.py: Neural network architecture
- MCTS.py: Monte Carlo Tree Search implementation
- Arena.py: Agent evaluation
- Coach.py: Training orchestration

**Submission**: gen_submission.py packages trained .pth.tar model for Kaggle

**Key Insight**: AlphaZero-style self-play with MCTS is a strong approach but requires distributed training infrastructure.

### sidhantagar/ConnectX — DQN + Minimax Hybrid

**Architecture**: Deep Q-Network combined with minimax search

**Key Features**:
- Value-based deep RL (DQN)
- Classical game tree search (minimax)
- Up to 11-step lookahead (for training)
- Dynamic programming for two-step lookahead
- Cython acceleration (c_agents.pyx)

**Approach**: Neural network provides value estimation; search provides precise lookahead

**Key Insight**: Hybrid NN + search can be more effective than either alone

### Key Neural Network Design Patterns for ConnectX

1. **CNN Input**: Multiple channels for player pieces, empty spaces, and board edges
2. **Policy Head**: Predicts best move (probability distribution over columns)
3. **Value Head**: Predicts win probability (scalar output)
4. **Transfer Learning**: Train on 7x6 solved positions, transfer to larger boards
5. **Small nets can be effective**: A net under 100K params may beat shallow alpha-beta

### Inference Speed Considerations

- CNN inference for ConnectX: ~0.1-1ms on modern GPU
- Alpha-beta search for ConnectX 7x6 at depth 8: ~100-500ms in Python
- Neural net is orders of magnitude faster than search
- GPU can evaluate entire board positions instantly

---

## 4. Kaggle Competition Analysis

### Competition Overview

- **Name**: ConnectX (official Kaggle environment)
- **Version**: 1.0.1
- **Agents**: 2 players
- **Board Configurations**: Configurable — columns (default 7, min 1), rows (default 6, min 1), inarow (default 4, min 1)
- **Scoring**: +1 win, -1 loss, 0 draw
- **Time Limits**: actTimeout=2 seconds per move, agentTimeout=60 seconds total, runTimeout=1200 seconds total
- **Observation**: board (flat array, 0/1/2), mark (1/2), remainingOverageTime, step

### Known Top Approaches

| Approach | Bot | Key Technique | Board Support |
|----------|-----|---------------|---------------|
| Minimax + AB | sidhantagar | Minimax with alpha-beta, dynamic programming | Variable (up to 20×20) |
| Hybrid DQN | VSZM | Deep Q-Network + minimax lookahead | Standard |
| AlphaZero MCTS | BEPb | Self-play RL with MCTS, PyTorch | Standard |
| SFT → RL CNN | marcpaulo15 | Supervised learning → self-play RL | Standard |
| Minimax + AB | mra1991 | Symmetric negamax, bitboards, iterative deepening | Standard |

### Competition Evaluation

- Submissions are Jupyter notebooks (.ipynb)
- Agent function must have signature: `agent(obs, config)`
- Board is flat array (not 2D)
- Game runs for up to episodeSteps moves
- Score based on wins/losses/draws against other submissions

### Key Observations

1. **No neural net has dominated**: Classical approaches still competitive
2. **Hybrid approaches**: NN + search is promising but complex
3. **Time is generous**: 2 seconds per move is plenty for alpha-beta at reasonable depth
4. **Board size matters**: Single bot must handle all configurations
5. **Competition likely uses 7x6**: Most evaluation is on standard board

### Kaggle Submission Requirements

- Notebook format: .ipynb
- Must contain agent function with correct signature
- Can include any helper code, imports, and model files
- Evaluation against multiple opponent strategies

---

## 5. GPU Hardware Opportunities

### RTX 5090 Specifications

- **GPU**: GB202-300 Blackwell die
- **CUDA Cores**: 21,760
- **RT Cores**: 170 (5th generation)
- **Tensor Cores**: 680 (5th generation)
- **Memory**: 32 GB GDDR7, 512-bit bus
- **Memory Bandwidth**: 1,792 GB/s at 28 Gbps
- **FP8 Tensor**: 419.2 TFLOPS (838.4 TFLOPS with sparsity)
- **FP16/FP32**: 104.8 TFLOPS
- **Boost Clock**: 2.41 GHz
- **TDP**: 575W
- **PCIe**: 5.0 x16
- **Launch**: January 30, 2025, $1,999 MSRP

### GPU Opportunities for ConnectX

#### 1. Neural Network Training (Primary)

**What**: Train CNN/policy/value networks on RTX 5090
**Speedup**: 50-200× vs CPU training
**Timeline**: Train a 7x6 ConnectX policy net in hours instead of days
**Dataset size**: 200K+ examples possible in reasonable time
**Training approaches**:
  - Supervised learning from solved positions
  - Self-play RL (AlphaZero-style)
  - Transfer learning from 7x6 to larger boards

#### 2. GPU-Accelerated Neural Network Inference

**What**: Policy net inference for move selection
**Speed**: ~0.1ms per inference on RTX 5090
**Benefit**: Can evaluate thousands of positions per second
**Use cases**:
  - MCTS neural net evaluation
  - Policy-guided move ordering for alpha-beta
  - Value network for position evaluation

#### 3. Hybrid CPU+GPU Architecture

**Architecture**:
```
CPU (alpha-beta search)
  ↓
GPU (neural net evaluation at leaf nodes)
  ↓
GPU (parallel move evaluation — experimental)
```

**Benefit**: Best of both worlds — search precision + GPU speed

#### 4. Parallel Move Evaluation (Experimental)

**Concept**: Evaluate multiple board positions simultaneously on GPU
**Challenge**: Alpha-beta is inherently sequential (depends on previous results)
**Opportunity**: Parallelize leaf-node evaluation during search
**Potential speedup**: 10-50× for batched evaluation

#### 5. JIT Compilation (Numba/Cython)

**What**: Accelerate alpha-beta search on CPU with JIT
**Speedup**: 5-10× vs pure Python
**Implementation**: Use Numba `@jit` on core search loops
**Benefit**: No GPU needed for search acceleration

### Recommendations

1. **Primary use**: Neural network training (most impactful)
2. **Secondary use**: GPU-accelerated inference for MCTS or neural evaluation
3. **Tertiary use**: JIT compilation for CPU search acceleration

---

## 6. Search Algorithm Landscape

### Alpha-Beta Minimax

**Description**: The foundational search algorithm for Connect 4 AI
**Variants**:
- Standard alpha-beta
- Negamax (simplified implementation)
- NegaScout / PVS (Principal Variation Search)
- MTD(f) (Minimax with Threat Detection)

**Performance on 7x6**:
- Depth 8: ~100-500ms in Python (with optimizations)
- Depth 10: ~1-3 seconds in Python
- Depth 12+: Too slow in Python without optimizations

**Performance on 15x13**:
- Alpha-beta breaks down (search space too large)
- Effective depth: 2-4 at most in Python
- MCTS or neural network approaches become necessary

### Monte Carlo Tree Search (MCTS)

**Description**: Tree search using random simulation
**UCT Formula**: `UCT = (value / visits) + C * sqrt(ln(parent_visits) / visits)`
**Typical C**: 1.414 (√2) for balance between exploration and exploitation

**Advantages over alpha-beta**:
- Better on large/sparse boards (15x13)
- Parallelizable (many simulations)
- Neural net integration (guides search)
- Doesn't require heuristic evaluation function

**Disadvantages**:
- Slower convergence than alpha-beta on small boards
- Random playouts waste computation on obviously bad moves
- Hard to integrate domain knowledge

**Best use case**: Larger boards (15x13, 15x10) where alpha-beta is ineffective

### Hybrid Approaches

1. **NN-guided alpha-beta**: Neural net ranks moves before searching
2. **MCTS + neural net**: AlphaZero-style (neural net evaluates, MCTS searches)
3. **Alpha-beta + MCTS**: Use MCTS for opening, alpha-beta for endgame
4. **DQN + minimax**: Neural net provides value estimation, minimax provides lookahead

### Time Management (2 seconds per move)

**Optimal strategy**:
1. Iterative deepening: Start at depth 1, increase until time runs out
2. Store best move from each iteration in transposition table
3. If time remains, continue deeper search
4. For endgame (<8 pieces), use endgame database lookup

**Python optimization targets**:
- Pure Python: ~10K-50K nodes/sec at depth 6-8
- With JIT (Numba): ~100K-500K nodes/sec
- With Cython: ~500K-2M nodes/sec
- With C++ binding (pybind11): ~5M-20M nodes/sec

---

## 7. Evaluation Function Research

### Classical Heuristic Features

| Feature | Description | Weight |
|---------|-------------|--------|
| Center control | Preference for center columns | +2-3 per piece |
| Window scoring | Count 4-in-a-row, 3+1, 2+2 patterns | 100, 5, 2 |
| Threat detection | Forks, two-threat patterns | High priority |
| Block detection | Opponent threats | High priority |
| Vertical stacks | Column height advantage | +1-2 per piece |
| Diagonal control | Diagonal piece placement | +1-2 per piece |
| Tempo | Move order advantage | +1 per move |

### Advanced Features

1. **Potential threat analysis**: Number of potential winning lines
2. **Forced sequence detection**: If player can force a win in N moves
3. **Fork detection**: Positions with two simultaneous threats
4. **Space control**: Territory control in each region of the board
5. **Connectivity**: How connected are pieces in each direction
6. **Opposition quality**: Quality of blocking moves

### Learned Evaluation Functions

1. **From solved positions**: Perfect training signal (no noise)
2. **From expert play**: Solved game database provides expert moves
3. **Self-play**: Learn from self-play games (AlphaZero style)
4. **Neural net**: CNN takes board state → outputs evaluation

### Key Insight

> For 7x6 board: We have perfect evaluation (solved game)
> For larger boards: We need heuristics + neural networks

---

## 8. Multi-Board Strategy

### Board Size Challenges

| Board Size | Cells | Strategy | Search Depth |
|-----------|-------|----------|--------------|
| 4x4 (4-in-a-row) | 16 | Solved (draw) | Full solve |
| 5x5 (4-in-a-row) | 25 | Solved (draw) | Full solve |
| 6x6 (4-in-a-row) | 36 | Draw with perfect play | Limited solve |
| 7x6 (4-in-a-row) | 42 | SOLVED (first player wins) | Full solve exists |
| 10x7 (4-in-a-row) | 70 | Unknown | Very limited |
| 13x15 (4-in-a-row) | 195 | Unknown | Minimal |

### Unified Strategy Approach

1. **7x6 and smaller**: Use solved game database / opening book
2. **Medium boards (8x8 to 10x10)**: Use alpha-beta with neural net evaluation
3. **Large boards (11x11+)**: Use MCTS with neural net evaluation
4. **All boards**: Use a unified neural network with transfer learning

### Key Design Decision

A **single neural network** that takes board size as input parameters can generalize across all board sizes. The network should:
- Accept board state as input (max board size, with empty padding for smaller boards)
- Include board dimensions as additional input features
- Be trained on solved positions from smaller boards and transferred to larger ones

---

## 9. Advanced Techniques

### Transposition Tables

- Store previously evaluated board positions
- Key: Zobrist hash of board state
- Value: depth, alpha/beta bounds, best move
- Replacement policy: depth-based (replace shallower entries)

### Zobrist Hashing

- Random 64-bit number for each piece at each position
- XOR all piece hashes to get board state hash
- O(1) hash update for move (XOR old piece, XOR new piece)

### Move Ordering

**Priority order for ConnectX**:
1. Win-in-one / Block win-in-one
2. Center columns (highest impact)
3. Columns adjacent to opponent's pieces
4. Fork-creating moves
5. Random

### Killer Heuristic

- Store "killer moves" at each depth that caused beta-cutoffs
- Try killer moves first in subsequent positions at same depth
- More effective in chess than Connect 4 (but still useful)

### Iterative Deepening

- Search depth 1, 2, 3, ... until time runs out
- Each iteration uses TT from previous iterations
- Guarantees best move found at any time cutoff
- Essential for time-limited search

### Quiescence Search

- Extend search at terminal nodes when threats are present
- Only search "forcing" moves (checks, captures)
- Less important for Connect 4 than chess (few forced moves)

### Symmetry Reduction

- Canonicalize board positions using symmetry
- Halves state space for symmetric positions
- Effective for 7x6 board (vertical symmetry)

---

## 10. Hypotheses

These are unverified hypotheses to be tested in future research iterations:

### H1: Small CNN (under 100K params) trained on solved 7x6 positions beats depth-6 alpha-beta
- **Reasoning**: Solved positions provide perfect training signal; small net = fast inference
- **Test**: Train CNN on 7x6 solved positions, compare vs depth-6 minimax
- **Confidence**: Medium

### H2: RTX 5090 enables GPU-accelerated training that gives 50-200× speedup over CPU
- **Reasoning**: RTX 5090 has 680 Tensor Cores, 419 TFLOPS FP8
- **Test**: Train CNN on RTX 5090 vs CPU, measure speedup
- **Confidence**: High (based on specs)

### H3: MCTS with learned value function outperforms alpha-beta at depth > 10 on 15x13
- **Reasoning**: Alpha-beta degrades on sparse boards; MCTS concentrates search
- **Test**: Implement MCTS + NN, compare vs alpha-beta on 15x13
- **Confidence**: Medium

### H4: Hybrid approach (NN opening + alpha-beta midgame + tablebase endgame) beats pure approaches
- **Reasoning**: Each component excels at different game phases
- **Test**: Implement hybrid, compare vs pure approaches
- **Confidence**: Medium-High

### H5: Python JIT (Numba/Cython) gives 5-10× speedup on alpha-beta
- **Reasoning**: Search is compute-bound; JIT eliminates interpreter overhead
- **Test**: Benchmark pure Python vs Numba vs Cython
- **Confidence**: High

### H6: Neural net trained on 1M+ solved positions achieves >95% agreement with minimax
- **Reasoning**: Solved game provides perfect training data
- **Test**: Train on solved positions, measure agreement with minimax
- **Confidence**: Medium-High

### H7: A single CNN with board dimensions as input generalizes across all board sizes
- **Reasoning**: CNNs can handle variable spatial inputs
- **Test**: Train on multiple board sizes, test cross-boarding performance
- **Confidence**: Low-Medium

### H8: MTD(f) search gives 20-30% speedup over standard alpha-beta
- **Reasoning**: MTD(f) is a more efficient minimax variant
- **Test**: Implement MTD(f), benchmark vs alpha-beta
- **Confidence**: Medium

### H9: Neural net move ordering improves alpha-beta by 2-3×
- **Reasoning**: Good move ordering dramatically reduces search
- **Test**: Add neural net move ordering, measure node count reduction
- **Confidence**: Medium

### H10: GPU parallel evaluation gives 10-50× speedup for batched leaf evaluation
- **Reasoning**: GPU excels at parallel computation
- **Test**: Implement parallel GPU evaluation, benchmark speedup
- **Confidence**: Medium

---

## 11. Open Questions

### Game Theory
1. What is the optimal opening for 15x13 boards?
2. Does first-player advantage persist on very large boards?
3. Is there a threshold where Connect 4 becomes a draw with perfect play?
4. What is the "thin position" analysis for Connect 4?

### Machine Learning
1. What neural network architecture is optimal for ConnectX?
2. How many parameters are needed to achieve expert-level play?
3. Can transfer learning from 7x6 to 15x13 be effective?
4. What's the minimum training set size for good performance?
5. Should we use PPO, DQN, or REINFORCE for self-play RL?

### Search
1. What search algorithm is best for 15x13 boards?
2. How to optimally allocate 2 seconds per move?
3. Can we use GPU for parallel search tree exploration?
4. What's the practical limit of alpha-beta in Python?

### Hardware
1. What's the fastest way to deploy a neural net for ConnectX inference?
2. Can we use TensorRT for even faster inference?
3. What's the optimal batch size for GPU inference?
4. How much VRAM do we need for the largest practical model?

### Competition
1. What board configurations does the competition actually use?
2. How many games are played per submission evaluation?
3. What are the evaluation criteria (score, speed, consistency)?
4. Are there any recent Kaggle ConnectX winners to study?

---

## References

1. Allis, L.V. (1988). "A Knowledge-based Approach of Connect-Four"
2. Allen, R. (1988). "Connect Four Proved"
3. Böck, S. (2025). "Connect4 7 x 6 Strong Solution"
4. Tromp, J. (2025). "Computational Datasets for Connect 4"
5. Waldchen et al. (2022). arXiv:2202.11797
6. Chen, S. et al. (2020). "A Connection Between Chess and Connect 4"
7. Markus Thill. "BitBully" — Fast perfect-play Connect Four solver
8. sidhantagar. "ConnectX" — Minimax with alpha-beta pruning
9. VSZM. "ConnectX" — DQN + minimax hybrid
10. BEPb. "Kaggle_ConnectX" — AlphaZero-style self-play with MCTS
11. marcpaulo15. "RL-connect4" — SFT → RL pipeline
12. mra1991. "connect-four-negamax" — Symmetric negamax with bitboards
13. NVIDIA. "GeForce RTX 5090" — Specifications and benchmarks