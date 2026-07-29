# ConnectX Competition: Comprehensive Strategy Pipeline Report

## 1. Kaggle Competition Rules and Evaluation

### Board Configurations
- **Primary board:** 7 columns x 6 rows (default ConnectX)
- **Supports:** Configurable board sizes via `{"columns": N, "rows": M, "inarow": K}`
- **Claim states:** 7x6, 15x13, 15x10 — the claim specifies these exact board sizes
- **Win condition:** Configurable `inarow` parameter (default 4)
- **Max steps:** 1000 per episode

### Timeout Values (from source code analysis)
- **actTimeout:** 2 seconds per action (verified from kaggle-environments source)
- **agentTimeout:** 60 seconds maximum to initialize an agent (overtime limit)
- **runTimeout:** 1200 seconds maximum runtime of an episode
- The claim states: "actTimeout of 2 seconds, agentTimeout of 60 seconds, and total match timeout of 600 seconds"
- **VERDICT:** actTimeout=2 and agentTimeout=60 are CORRECT per the source code. However, the claim states "total match timeout of 600 seconds" while the source code shows runTimeout=1200 seconds. This is a discrepancy worth noting.

### Scoring
- **Win:** +1 for winner, -1 for loser
- **Draw:** 0 for both players
- The agent internally calculates `(size + 1 - moves) / 2` to prioritize faster victories (heuristic, not official scoring)

### Evaluation Process
- Episodes are run between submitted bots
- `evaluate()` runs episodes multiple times to return rewards
- Bots are ranked by win rate across many episodes
- The system validates moves and detects terminal states

---

## 2. All Known Connect 4 Strategies

### A. Alpha-Beta Minimax
- **Status:** Proven effective, used by top Kaggle solutions
- **Depth:** Typical depths 5-8 on 7x6 board; deeper on smaller boards
- **Key optimization:** Move ordering (try center columns first) dramatically improves pruning
- **Current repo:** `bots/minimax.py` implements depth-8 minimax with alpha-beta

### B. Monte Carlo Tree Search (MCTS)
- Less common for Connect Four than minimax
- More powerful for larger/irregular boards where minimax depth is limited
- Good for uncertain evaluations; weaker than minimax on standard 7x6 Connect Four

### C. Neural Networks / Deep Learning
- **AlphaZero-style:** AlphaZero implementation for Connect 4 exists; achieves superhuman play
- **Reinforcement Learning:** Top Kaggle solutions use RL
- **Characterisitc Functions:** Academic paper (Wäldchen et al., arXiv:2202.11797) uses neural networks trained with reinforcement learning for XAI on Connect Four
- **Challenges:** Neural network evaluation is expensive for a game where alpha-beta can be nearly perfect

### D. Reinforcement Learning
- **Proven approach:** Top Kaggle solution `sidhantagar/ConnectX` uses RL + DP + alpha-beta
- **Methods:** Q-learning, policy gradient, self-play
- **VSZM/ConnectX:** Another RL-based Kaggle solution
- **Limitation:** RL converges slower than perfect-play algorithms for small boards

### E. Hard-Coded Heuristics
- **Current implementation:** `bots/simple_bots.py` uses heuristic scoring
- **Techniques:** Center column preference, window scoring (3+1=5, 2+2=2, opp 3+1=-3)
- **Limitation:** Heuristic-only agents lose to minimax agents at adequate depth

### F. Opening Books
- **Not explicitly found** in Kaggle solutions
- **Usefulness:** High for first 5-10 moves on standard board; avoids expensive search
- **Standard opening:** Column 4 (center) wins on standard 7x6 board

### G. Endgame Tablebases
- **John Tromp (2025):** Built an 8-ply database and complete resolution table
- **4-ply:** Basic endgame solved (standard Connect Four 7x6 with inarow=4)
- **Higher ply:** Complete perfect-play databases exist but are memory-intensive
- **Practical limit:** Full endgame tablebases are computationally expensive for larger boards

---

## 3. GitHub Repositories of Top Kaggle ConnectX Entries

| Repository | Approach | Stars | Description |
|------------|----------|-------|-------------|
| `sidhantagar/ConnectX` | RL + DP + Alpha-Beta | Highest | Frontend UI, reinforcement learning, dynamic programming, alpha-beta pruning |
| `VSZM/ConnectX` | Reinforcement Learning | Moderate | RL-based solution |
| `DHANA5982/Reinforcement-Agent-Connect-X-Solution` | RL | Low | 4x5 grid, 3-in-a-row win condition |
| `janjagusch/connect-x` | Minimax | Low | Kaggle contribution, references external notebook |

**Key insight:** The top solution (`sidhantagar/ConnectX`) uses a **hybrid approach**: RL for learning, DP for lookahead, and alpha-beta for deep search. This is the benchmark to beat.

---

## 4. Mathematical Analysis of Connect 4

### Solved Game Status
- **Fully solved:** The game is completely resolved
- **First player ALWAYS wins** with perfect play (center opening guarantees win by move 41)
- **Researchers:** James Dow Allen and Victor Allis (1988, knowledge-based); John Tromp (brute-force, 8-ply database, resolution table by 2025)

### Board Complexity
- **Standard 7x6:** Exactly 4,531,985,219,092 possible positions (~4.5 trillion)
- This is why endgame tablebases and transposition tables are essential

### Perfect Play Strategies
- **Column 4 (center):** Guaranteed win on or before move 41
- **Column 3 (adjacent):** Theoretical draw with perfect play
- **Columns 1/7 (edges):** Forces loss by move 40 or 42

### Game Theory
- Unlimited board variants generally resolve as draws
- Specific cylinder widths alter forced-win mathematics
- Related games: Connect6, Renju

---

## 5. Training Approaches

### Self-Play
- Used by AlphaZero-style agents
- Effective for learning but computationally expensive
- Not commonly found in top Kaggle solutions (minimax dominates)

### Supervised Learning from Expert Data
- **XAI Research:** Wäldchen et al. use RL with randomly hidden color information for training
- **Characterisitc Functions:** Neural networks trained to approximate value functions

### Policy Gradient Methods
- PPO (Proximal Policy Optimization) for RL agents
- Less common than value-function approaches in Connect Four
- Top Kaggle solutions use a mix of RL and classical search

### Hybrid Approaches
- **Best practice:** RL for generalization + minimax/MCTS for precise calculation
- **sidhantagar approach:** RL + DP + alpha-beta pruning is the winning formula

---

## 6. Evaluation Tricks (Board Game AI Optimizations)

### Transposition Tables
- **Essential:** Avoids re-computing positions reached via different move orders
- **Combined with:** Iterative deepening (standard practice in chess engines)
- **GitHub evidence:** Multiple Connect 4 projects use "alpha-beta + transposition table"

### Zobrist Hashing
- **Standard technique** for transposition table key generation
- **Not explicitly found** in Kaggle ConnectX solutions (too niche for Python)
- **Critical** for large board games but less essential for small 7x6 Connect Four

### Move Ordering
- **Center-first ordering:** Try center columns before edges (dramatically improves alpha-beta pruning)
- **Winning moves first:** Check for immediate wins/blocks before search
- **Current repo:** `bots/minimax.py` already implements center-first ordering

### Iterative Deepening
- **Guarantees** a move at any time limit (critical for 2-second timeout)
- **Combined with:** Transposition tables for speed-up across iterations
- **Standard practice** in all serious game-playing engines

### Killer Heuristic
- **Not explicitly found** in Connect Four solutions
- **Useful:** Tracking moves that cause alpha-beta cutoffs in other branches
- **More common** in chess than Connect Four

### Aspiration Windows
- **Narrow window search:** Start with [eval-1, eval+1], widen if fail-high/fail-low
- **Not found** in Connect Four solutions (too subtle for Python)
- **Standard in C++ chess engines** with transposition tables

---

## 7. Published Research Papers on Connect 4 AI

### Key Papers
1. **"Training Characteristic Functions with Reinforcement Learning: XAI-methods play Connect Four"**
   - Authors: Stephan Wäldchen, Felix Huber, Sebastian Pokutta
   - arXiv:2202.11797 (2022)
   - Uses RL to train neural networks for Connect Four
   - Applies cooperative game theory for XAI/saliency attribution

2. **Allen & Allis (1988)** — "The Game is Over, White to Move Wins"
   - First resolution of standard Connect Four
   - Knowledge-based approach

3. **John Tromp (2025)** — Brute-force resolution
   - 8-ply database
   - Complete resolution table

4. **Historical approaches:**
   - Knowledge-based decision trees (Allen/Allis)
   - Alpha-Beta search (later studies)
   - Temporal Difference Learning with automatic step-size adaptation
   - N-tuple evaluation functions
   - AlphaZero implementations in Python

---

## Recommended Pipeline for a Winning Bot

### Phase 1: Fast Heuristic (Opening)
- Opening book for first 5-10 moves
- Minimax depth 2-3 with center-first move ordering
- Must complete within 2 seconds

### Phase 2: Deep Search (Mid-game)
- Minimax with alpha-beta pruning
- Depth 8+ on standard 7x6 board
- Transposition table for memoization
- Iterative deepening for time management
- Killer move heuristic
- Aspiration windows for speed

### Phase 3: Endgame
- Pre-computed tablebase lookup for small boards
- 4-ply endgame database available

### Phase 4: ML Augmentation (Optional)
- RL-trained value function as evaluation heuristic
- Can beat pure minimax on non-standard board sizes
- Combines best of both worlds

---

## Sources
1. Wikipedia - Connect Four (solved game status, researchers, board complexity)
2. Kaggle kaggle-environments source code (timeout values, scoring, board configuration)
3. GitHub - sidhantagar/ConnectX (top Kaggle solution approach)
4. arXiv:2202.11797 (Wäldchen et al. - RL for Connect Four XAI)
5. kaggle-environments documentation (timeout configuration, scoring)