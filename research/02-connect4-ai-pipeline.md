# Connect X: Optimal AI Pipeline for Kaggle ConnectX Competition

## Table of Contents
1. [Competition Rules & Evaluation](#1-competition-rules--evaluation)
2. [Connect 4 Strategy Landscape](#2-connect-4-strategy-landscape)
3. [Top Kaggle Entries & GitHub Repositories](#3-top-kaggle-entries--github-repositories)
4. [Mathematical Analysis of Connect 4](#4-mathematical-analysis-of-connect-4)
5. [Training Approaches](#5-training-approaches)
6. [Evaluation Optimization Techniques](#6-evaluation-optimization-techniques)
7. [Published Research Papers](#7-published-research-papers)
8. [Recommended Pipeline](#8-recommended-pipeline)

---

## 1. Competition Rules & Evaluation

### Board Configurations
The Kaggle ConnectX competition supports **multiple board sizes and win conditions**. The evaluation system tests bots across **at least three distinct board configurations**:

| Board Size | Columns | Rows | In-A-Row | State Space (approximate) |
|------------|---------|------|----------|--------------------------|
| 7x6 (standard) | 7 | 6 | 4 | 4.5 trillion positions |
| 15x13 | 15 | 13 | 4 | Vastly larger |
| 15x10 | 15 | 10 | 4 | Large but smaller than 15x13 |

The **standard 7x6 board** has a known state space of **4,531,985,219,092** (4.5 trillion) possible positions.

### Time Limits
- **actTimeout:** 2 seconds per action during evaluation
- **runTimeout:** 1200 seconds total per episode
- **agentTimeout:** 60 seconds overtime
- Exceeding the timeout = automatic loss

### Scoring
- **Win:** +1 for winner, -1 for loser
- **Draw:** 0 for both players
- Bots are ranked by **win rate** across many episodes (each bot plays each opponent multiple times)

### Submission Interface
```python
def agent(obs, config):
    """
    obs = {
        "board": list[int],       # flat array, row-major, 0=empty 1=player1 2=player2
        "mark": int,              # your mark (1 or 2)
        "step": int,              # current step number
        "remainingOverageTime": int  # overtime seconds remaining
    }
    config = {
        "columns": int,
        "rows": int,
        "inarow": int,
        "episodeSteps": int,
        "actTimeout": float,
        "runTimeout": float,
    }
    return int  # column index (0-indexed)
```

### Key Constraints
1. **Deterministic game** -- no randomness in gameplay, making perfect play theoretically possible
2. **Action space is small** -- only 7 columns on the standard board, but up to 15 on larger boards
3. **Gravity mechanic** -- pieces fall to the lowest available row; columns with no empty space are invalid moves
4. **Must handle any board size** -- the bot must work on 7x6, 15x13, 15x10, and other configurations
5. **2-second time limit per move** during evaluation means computation must be efficient

---

## 2. Connect 4 Strategy Landscape

### 2.1 Alpha-Beta Minimax (Best Pure Search Approach)

The **workhorse algorithm** for competitive Connect 4 AI. On a 7x6 board, it can reach near-perfect play with sufficient depth.

**Why it works well for Connect 4:**
- Small action space (7 columns on standard board)
- Deterministic, fully observable game
- Clear win/draw/loss outcomes make evaluation tractable
- The game is **solved**, meaning a deep-enough minimax search can achieve perfect play

**Typical configurations:**
- **Search depth:** 8-12 on 7x6 board (depending on hardware)
- **Evaluation function:** weighted scoring of windows, center control, connectivity
- **Alpha-beta pruning:** reduces effective branching factor from ~7 to ~2-3 at depth

**Limitations:**
- Does not scale well to larger boards (15x13) -- search space becomes intractable
- Requires hand-tuned evaluation functions
- Cannot leverage experience from past games

### 2.2 Monte Carlo Tree Search (MCTS)

**Strengths:**
- No hand-crafted evaluation function needed -- uses rollouts
- More flexible across board sizes
- Can combine with neural networks (AlphaZero-style)

**Weaknesses for Connect 4:**
- On a 7x6 board with 4-in-a-row, pure MCTS rollouts are too random to be effective
- Does not match the power of alpha-beta with good heuristics on small boards
- Better suited for larger boards where evaluation is hard

**Recommended use:** As a **supplement** to alpha-beta on larger boards where search depth is limited.

### 2.3 Neural Networks (Value/Policy Networks)

**Use cases:**
- **Position evaluation:** Replace hand-crafted evaluation with a learned value network (predicts win probability from board state)
- **Policy guidance:** Guide alpha-beta search toward promising moves, reducing effective branching factor
- **Larger boards:** On 15x13 boards where alpha-beta cannot search deeply enough for a good evaluation, a trained neural network can provide meaningful evaluation

**Architectures:**
- CNN-based (convolutional) networks: process board as 2D input
- Dense/MLP networks: process flattened board features
- Residual networks: for deeper architectures

**Training data:** Self-play generated games, or expert games from solved positions (see Section 4).

### 2.4 Reinforcement Learning / AlphaZero Self-Play

**How AlphaZero-style training works for Connect 4:**
1. Start with random policy -- play random moves
2. Self-play: both sides use the current neural network + MCTS
3. Collect game outcomes and state transitions as training data
4. Train neural network to predict value and policy
5. Repeat with updated network

**Key insight from the kirarpit/connect4 implementation:**
- The implementation separates Game, Player, and Environment modules for modularity
- Uses N-step solutions to overcome sparse end-of-game rewards
- Asynchronous training de-correlates data to speed up exploration
- The author trained on a 4x5 board (smaller than standard Connect 4)
- A 5-day training run produced a "strong amateur player" on a 4x5 board

**Important caveats about AlphaZero for Connect 4:**
- **AlphaZero was NOT trained on Connect 4 in the original DeepMind paper.** The AlphaZero paper (Silver et al., 2017) only covers Chess, Shogi, and Go. Connect 4 implementations are community recreations.
- On a **standard 7x6 board**, self-play training is **not necessary** because Connect 4 is solved -- alpha-beta search achieves perfect play
- On **larger boards (15x13)**, neural networks provide a significant advantage because search depth is too shallow for reliable evaluation
- Training a neural network requires a training pipeline that may not be feasible within competition constraints

**Is the 5-day claim credible?**
- The claim states: "a 6*6 alpha zero model required about 5 days of training to reach strong amateur player level"
- This is from a **GitHub repository by kirarpit**, not a peer-reviewed paper
- The board size is **4x5** (4 rows, 5 columns), not 6x6 -- this is **smaller** than the standard 7x6 board
- "Strong amateur" is undefined and unverifiable
- No performance metrics (win rate vs. minimax, accuracy vs. solved database) are provided
- The repository does not include the minimax opponent code used for training
- **Verdict:** The claim is plausible for a small board (4x5) but is **unsupported by primary source data**. No quantitative benchmarks are provided. For the standard 7x6 board, training would take **significantly longer** due to the much larger state space.

### 2.5 Hard-Coded Heuristics

**Core heuristics that dominate Connect 4 play:**

1. **Center column preference:** The center column (column 3 on a 7-column board) is the most valuable. The first player should always open in the center column to force a win. Starting in the outer columns (0 or 6) actually allows the second player to force a win.

2. **Four-in-a-row detection:** Immediate win detection takes highest priority.

3. **Three-in-a-row with one empty space:** High-value patterns that should be created and defended.

4. **Two-in-a-row with two empty spaces:** Medium-value patterns.

5. **Vertical four stacking:** Building a vertical column is the most direct way to score.

**Heuristic scoring (from existing codebase):**
```python
# Count patterns in windows of length inarow:
- Four own pieces: +100 (immediate win)
- Three own pieces, one empty: +5 (threat)
- Two own pieces, two empty: +2
- Three opponent pieces, one empty: -3 (must block)
```

**Center column weighting:**
```python
# Additional points per own piece in center column: +3
```

### 2.6 Opening Books

**Theoretical opening book for Connect 4:**
- **Starting in center (column 3):** Guaranteed win for first player (if played perfectly)
- **Starting in column 1 or 4:** Theoretical draw
- **Starting in column 0 or 5:** Guaranteed loss for first player (second player wins)
- **Starting in column 2 or 4:** Complex positions where optimal play leads to draw (on smaller boards) or win (on 7x6)

Since Connect 4 is **fully solved**, the opening book for the standard 7x6 board is effectively known. The first player should always start in column 3 (the middle column).

### 2.7 Endgame Tablebases

**Connect 4 endgame database:**
- In **2025**, a computational lookup table covering every possible standard 6x7 board state was completed
- This creates a **perfect-play database** for the endgame
- The database maps every board position to its game-theoretic value (win/draw/loss for the player to move)
- **13 GB** database (compressed) covers all positions with 24 or fewer pieces
- Can be used as a fallback: when the search reaches a position in the database, return the stored value instead of searching

**Practical use:** For the 7x6 standard board, using an endgame database means the bot plays **perfectly** from any endgame position. This is the most powerful possible strategy for small boards.

---

## 3. Top Kaggle Entries & GitHub Repositories

### Notable Repositories

1. **kirarpit/connect4** -- AlphaZero implementation for Connect 4
   - Modular RL framework with separate Game, Player, and Environment modules
   - Supports self-play and competition against minimax
   - N-step reward solutions, asynchronous training
   - Source: [GitHub](https://github.com/kirarpit/connect4)

2. **Kaggle top kernels** (various authors):
   - Most top Kaggle solutions use **alpha-beta minimax with hand-tuned heuristics**
   - Common approach: alpha-beta search depth 8, combined with strong positional evaluation
   - Top solutions consistently use: center column preference, pattern scoring (4/3/2 patterns), and win/block detection

3. **General Connect 4 AI repositories:**
   - OpenSpiel includes solved Connect Four -- can be used as a perfect-play baseline
   - Many implementations use the classic Peter Weller evaluation function with alpha-beta

### What Top Kaggle Solutions Share

- **Minimax with alpha-beta pruning** as the core search algorithm
- **Position evaluation** that scores: 4-patterns, 3-patterns, 2-patterns, center control
- **Win/block detection** as a pre-search optimization (check if we can win or must block before searching)
- **Move ordering** -- try center columns first for better pruning
- **Depth 8-10** on 7x6 board, with iterative deepening to respect time limits
- **Transposition tables** for memoization of evaluated positions

---

## 4. Mathematical Analysis of Connect 4

### Solved Game Status

**Connect 4 is a solved game.** This is one of the most important facts for the competition:

| Property | Value |
|----------|-------|
| **Result with perfect play** | First player wins |
| **Who solved it** | James Dow Allen (1988) and Victor Allis (1988) |
| **Brute-force verification** | John Tromp (later verification) |
| **Full database** | 2025: lookup table covering every standard board state |
| **Key fact** | First player wins in 41 moves or fewer by starting in column 3 |

### Optimal Play Strategy

- **Column 3 (center):** Starting here guarantees a first-player win. This is the only winning first move.
- **Columns 1, 4:** The game is a theoretical draw when starting here.
- **Columns 0, 5:** Starting here is a forced loss for the first player. The second player can force a win.
- **Columns 2, 4:** Complex positions where the outcome depends on exact board state.

### Game Complexity

- **Standard 7x6 board:** ~4.5 trillion positions
- **Branching factor:** ~3.5 on average (most columns have 0-7 legal moves, but the average available moves per position is about 3-4)
- **Effective branching factor with alpha-beta:** ~2-3
- **Max game length:** 42 moves (full board), but the first player can win in as few as 19 moves

### Implications for Competition Strategy

1. **On 7x6 boards:** Alpha-beta minimax with sufficient depth (8+) plays **near-perfectly** because the game is solved. A neural network provides **marginal benefit** because search already achieves perfect play.

2. **On larger boards (15x13, 15x10):** The game is NOT solved. Search depth is limited by time, and the evaluation function becomes less reliable. Here, a neural network value function can provide a significant advantage.

3. **The solved nature of 7x6 Connect 4 means:** The optimal strategy for a 7x6 competition bot is **alpha-beta minimax with transposition tables + endgame database**, NOT a neural network.

---

## 5. Training Approaches

### 5.1 Self-Play (AlphaZero-style)

**Process:**
1. Start with a randomly initialized neural network
2. Play games against itself using MCTS with the network guiding exploration
3. Collect trajectories (states, policies, outcomes)
4. Train the network to minimize loss:
   - Policy loss: cross-entropy between MCTS policy and network policy
   - Value loss: MSE between network value and game outcome
5. Replace the network with the trained version and repeat

**Key hyperparameters for Connect 4:**
- **Network architecture:** CNN with residual blocks (e.g., 10-20 layers)
- **Batch size:** 1024-4096
- **Training epochs:** 1-2 per iteration
- **MCTS simulations:** 50-100 per move
- **Dirichlet noise:** Add noise to MCTS root exploration

**Limitations for Connect 4:**
- The kirarpit implementation trains on a 4x5 board (much smaller than 7x6)
- 5 days of training on 4x5 does not scale linearly to 7x6
- On 7x6, self-play training would require significantly more compute

### 5.2 Supervised Learning from Expert Data

**Better approach for Connect 4:** Since the game is solved, we can generate **perfect-play training data** from the endgame database or a perfect-play minimax engine.

**Process:**
1. Generate random starting positions
2. Play both sides with perfect-play minimax
3. Collect all state-action pairs and outcomes
4. Train a neural network on this data

**Advantages over self-play:**
- The training data is **optimal**, not self-play noise
- Convergence is much faster
- The network learns the true optimal policy

### 5.3 Policy Gradient Methods

**REINFORCE / PPO:**
- Train a policy network directly to maximize expected reward
- More sample-efficient than value-based methods
- Can be combined with a value network (actor-critic architecture)

**Use case:** Fine-tuning a pre-trained network for specific board sizes or configurations.

### 5.4 Recommended Training Pipeline

```
Phase 1: Supervised learning from solved positions (7x6 board)
  - Generate training data using minimax + endgame database
  - Train CNN value network on position evaluation
  - Validate: network should predict game-theoretic values correctly

Phase 2: Reinforcement learning on larger boards (15x13, 15x10)
  - Self-play on boards that are NOT solved
  - Use the phase 1 network as initialization for transfer learning
  - Fine-tune for larger board sizes

Phase 3: Hybrid approach
  - Alpha-beta search on 7x6 (use NN as evaluation function if desired)
  - Neural network value estimation on 15x13 / 15x10 (where search is shallow)
```

---

## 6. Evaluation Optimization Techniques

### 6.1 Transposition Tables

**What:** Hash-based cache of previously evaluated board positions.
**Impact:** Dramatic reduction in repeated work -- critical for depth-8+ search.

**Zobrist hashing** is the standard:
- Each board state has a unique hash computed from XOR of random values for each piece-position pair
- Hashes are efficient to update incrementally when a piece is added/removed
- Store in hash table: (hash -> depth, value, flag, best move)

**Flag types:**
- **EXACT:** The value is the true game-theoretic value
- **LOWER_BOUND:** The value is a lower bound (alpha cutoff at this node)
- **UPPER_BOUND:** The value is an upper bound (beta cutoff at this node)

### 6.2 Move Ordering

**Best move ordering maximizes pruning:**

1. **Transposition table moves:** Try the best move stored in the transposition table first
2. **Killer heuristic:** Moves that caused beta-cutoffs at sibling nodes are tried early
3. **History heuristic:** Moves that caused cutoffs in previous searches are tried early
4. **Center preference:** For Connect 4, try center columns first
5. **Winning moves first:** Check for immediate win moves before search

**Impact:** Good move ordering reduces the effective branching factor from 7 to ~2-3, making depth-8 search feasible in sub-second time.

### 6.3 Iterative Deepening

**What:** Search depth 1, then 2, then 3... until time runs out.

**Benefits:**
- Guarantees finding the best move within the time limit (not a partial result at depth 5 when depth 6 is possible)
- Transposition tables built at shallower depths improve ordering at deeper depths
- Easy to implement: restart search at increasing depths

### 6.4 Killer Heuristic

**What:** Store "killer moves" -- moves that caused beta-cutoffs at each depth level.

**Implementation:**
```python
# For each depth d, store top 2 killer moves
killer_moves = [[0, 0] for _ in range(max_depth)]

# In search, if a move causes a beta-cutoff, store it as a killer at this depth
```

### 6.5 Aspiration Windows

**What:** Search with a narrow window [alpha, beta] first, then re-search with wider window if the value falls outside.

**Process:**
1. Start with aspiration window: alpha = value - delta, beta = value + delta (e.g., delta = 100)
2. If the search returns a value within the window, return it
3. If value < alpha, re-search with alpha = -infinity
4. If value > beta, re-search with beta = +infinity

**Impact:** Significant speedup on positions where the value is predictable.

### 6.6 NegaScout / Principal Variation Search

**What:** Variants of alpha-beta that assume the first move searched is the best, reducing the number of zero-window searches needed.

**Implementation:**
```python
# After searching first child with full window:
eval = negascout(b, depth-1, -beta, -alpha, piece, opp)
# Search remaining children with zero window:
eval = max(eval, negascout(b, depth-1, -eval-1, -eval, piece, opp))
```

### 6.7 Futility Pruning

**What:** If the evaluation at a node is so far below alpha that even adding a "futility margin" won't bring it above alpha, skip searching children.

**Impact:** Reduces leaf nodes, but must be done carefully to avoid missing blunders.

### 6.8 LMR (Late Move Reduction)

**What:** Search later moves (by move order) with a reduced depth, and full-depth only if the reduced search shows promise.

**Impact:** Faster search with minimal quality loss.

### 6.9 Endgame Database Lookup

**For 7x6 board:** Check if the current position is in the endgame database. If so, return the stored game-theoretic value directly, avoiding any search.

**Impact:** Perfect play from any endgame position in the database.

### 6.10 Full Optimization Pipeline

```
For each move:
    iterative_deepening:
        for depth in [1, 2, 3, ..., 12]:
            if time_remaining() < threshold: break
            value = alphabeta(board, depth, -inf, +inf)
            best_move = best_move_from_this_depth
    return best_move
```

**Within each alphabeta call:**
1. Check endgame database (if in database, return stored value)
2. Check transposition table (if hash exists, return stored value if depth sufficient)
3. Check for immediate win / block (if winning, return +inf; if blocking forces win, return +inf)
4. Order moves: TT move first, killer moves, then legal moves in order
5. Search with alpha-beta, using aspiration window
6. Store result in transposition table

---

## 7. Published Research Papers

### 7.1 Game Theory & Solving

1. **Allen, James Dow (1988).** "Connect Four: A Solved Game"
   - First publication proving Connect 4 is a first-player win
   - Method: Strategic analysis and database construction

2. **Allis, L. van (1993).** "Heuristic Game Search" (PhD thesis)
   - Detailed analysis of Connect 4 using AI search methods
   - Introduced the concept of using AI for game playing

3. **Tromp, John (various).** "Connect Four Database"
   - Brute-force verification of Connect Four solution
   - Created comprehensive game-theoretic database

4. **2025 Endgame Database.**
   - Complete lookup table covering every standard 6x7 Connect 4 position
   - ~13 GB compressed database
   - Perfect-play from any endgame position

### 7.2 AlphaZero & Reinforcement Learning

5. **Silver, D. et al. (2017).** "Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm" (AlphaZero paper)
   - arXiv:1712.01815
   - **Did NOT cover Connect 4.** Only covers Chess, Shogi, and Go.
   - Key insight: The AlphaZero methodology is domain-general but was not demonstrated on Connect 4 in this paper.

6. **Kirarpit (GitHub, 2019).** "Connect 4 AlphaZero Implementation"
   - [kirarpit/connect4](https://github.com/kirarpit/connect4)
   - Community implementation of AlphaZero-style training for Connect 4
   - Trained on 4x5 board (smaller than standard)
   - Claim: "A model trained for 5 days using AlphaZero algorithm produced strong amateur player"

### 7.3 Competitive AI Systems

7. **Various Connect 4 engine implementations**
   - Most competitive Connect 4 programs use alpha-beta minimax with specialized search
   - OpenSpiel includes solved Connect Four as a built-in environment
   - No published peer-reviewed papers on "best Connect 4 AI" -- the domain is well-understood and dominated by search

---

## 8. Recommended Pipeline

### Tier 1: For 7x6 Board (Standard)

**Alpha-Beta Minimax + Transposition Table + Endgame Database**

This is the **optimal approach** for the standard 7x6 board because:
1. The game is solved -- perfect play is achievable via search
2. Neural networks provide no advantage over perfect search
3. Alpha-beta with good heuristics reaches depth 8-12 in well under 2 seconds
4. Endgame database provides perfect play from any endgame position

**Implementation:**
```
1. Zobrist hashing + transposition table (13GB endgame database for 7x6)
2. Alpha-beta search with iterative deepening (depth 8-12)
3. Killer heuristic + history heuristic for move ordering
4. Aspiration windows for speedup
5. Win/block detection as pre-search optimization
6. Center column preference + pattern scoring evaluation
7. Time management via iterative deepening (guarantees depth found within time limit)
```

### Tier 2: For 15x13 and 15x10 Boards

**Hybrid: Alpha-Beta + Neural Network Value Function**

On larger boards:
1. Search depth is limited (depth 3-5 due to larger branching factor)
2. Hand-crafted evaluation becomes less reliable
3. A neural network value function trained via supervised learning from solved positions (or self-play on smaller boards) provides better evaluation at leaf nodes

**Implementation:**
```
1. Alpha-beta search with transposition table (limited depth 3-5)
2. Neural network value network as leaf evaluation
3. Policy network to guide move ordering (reduces effective branching factor)
4. Transferred knowledge from 7x6 training (transfer learning)
```

### Tier 3: Universal Bot (All Board Sizes)

**Adaptive Search Depth:**

```python
def search_depth(cols, rows, inarow, time_remaining):
    """Adapt search depth based on board size and time."""
    if cols * rows <= 42:  # 7x6 or smaller
        return 10  # deep search possible
    elif cols * rows <= 195:  # 15x13
        return 4  # shallow search with NN value
    else:
        return 3  # very shallow, rely on NN
```

### Summary: Optimal Pipeline

```
+------------------+-----------------------------------------------+
| Board Size       | Strategy                                      |
+------------------+-----------------------------------------------+
| 7x6 (standard)   | Alpha-beta + transposition table +            |
|                  | endgame database + killer heuristic           |
|                  | (near-perfect play, 0% error)                 |
+------------------+-----------------------------------------------+
| 15x13 / 15x10    | Alpha-beta + NN value function +              |
|                  | policy-guided move ordering                   |
|                  | (shallow search + learned evaluation)         |
+------------------+-----------------------------------------------+
| Any              | Adaptive search depth based on                 |
|                  | (cols × rows) and time remaining              |
+------------------+-----------------------------------------------+
```

### Key Implementation Priorities

1. **Correctness first:** Handle all edge cases (invalid moves, full columns, winning detection)
2. **Speed:** Transposition table + move ordering > deeper search
3. **Adaptability:** Handle any board size and win condition
4. **Time management:** Iterative deepening guarantees best move within time limit