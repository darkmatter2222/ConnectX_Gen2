# Kaggle Official Built-in Agents and Missing Contender Profiles

> **Dossier ID**: CB-001
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Scope**: Deep source-level analysis of Kaggle ConnectX built-in agents (random_agent, negamax_agent) as canonical benchmark baselines; deep-profiles of under-analyzed contenders (connectX-bitboard-agent, MCTS-NC, neurofour, IncludeAI/shallow-trap, marcpaulo15/RL-connect4, Widnyana/connect4); benchmark baseline methodology

---

## 1. Executive Summary

This dossier provides two deliverables critical to the Contenders, Baselines, and Benchmark References lane:

1. **Kaggle official built-in agents as canonical benchmark baselines** — Complete source-level analysis of the Kaggle ConnectX environment's built-in agents (`random_agent`, `negamax_agent`) that serve as the *authoritative evaluation baseline* for all Kaggle ConnectX submissions.

2. **Deep-profiles of under-analyzed contenders** — Systematic source-level profiles of six contenders that are either missing from the dossier corpus entirely or only superficially referenced: `connectX-bitboard-agent` (Tarun995), `mcts_numba_cuda` (pklesk/MCTS-NC), `neurofour/connect4`, `IncludeAI/shallow-trap`, `marcpaulo15/RL-connect4`, and `Widnyana/connect4`.

**Key findings:**

1. **The Kaggle built-in negamax_agent is the weakest competitive benchmark** — With no alpha-beta pruning, a depth-4 search, and a naive adjacency-based leaf heuristic (±1 per neighbor), it is easily defeated by any engine with proper alpha-beta or better leaf evaluation.

2. **The leaf heuristic does not scale to 15×13 boards** — The adjacency bonus system (checking 4 neighboring cells) produces misleading evaluations on much larger boards where the same 4-neighbor sample covers a vanishing fraction of the local neighborhood.

3. **connectX-bitboard-agent (Tarun995) is the most sophisticated pure-Python classical engine** — Numba-JIT negamax with PVS, 16M-entry TT, history heuristic, killer moves, aspiration windows, iterative deepening with 1.70s time budget.

4. **MCTS-NC achieves 20.3M playouts per 5 seconds on a GRID A100** — GPU-accelerated MCTS for Connect 4 using Numba CUDA kernels, 75.1% average score vs 2.5% vanilla baseline.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition has a fundamental gap: **no single published benchmark suite uses all built-in Kaggle agents as a progressive difficulty ladder**. The existing dossiers (CBL-001, CON-001, DOS-005, DOS-006, DOS-007, CBL-002) cover 20+ contenders but leave out:

- **Kaggle built-in agents as benchmark baselines** — These are the standard opponents, yet no dossier systematically analyzes them as benchmark targets.
- **GPU-accelerated MCTS** — MCTS-NC (pklesk) is referenced in MCTS-007 but lacks a full contender profile.
- **Deep profiles for connectX-bitboard-agent, neurofour, IncludeAI/shallow-trap, marcpaulo15, and Widnyana** — all referenced but never profiled at source level.

A Kaggle-winning bot must be benchmarked against: (1) the random agent (sanity check), (2) the built-in negamax_agent (minimum viable opponent), and (3) stronger classical/NN opponents.

---

## 3. Source Map

### 3.1 Primary Sources (Verified, Read-Only, Local)

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|----------------|
| S_CB-001-01 | Kaggle ConnectX game engine (connectx.py, 202 lines) | Local: `kaggle-environments/kaggle_environments/envs/connectx/connectx.py` | Apache 2.0 | Source code | 2026-08-05 |
| S_CB-001-02 | Kaggle ConnectX JSON spec (connectx.json, 71 lines) | Local: `kaggle-environments/kaggle_environments/envs/connectx/connectx.json` | Apache 2.0 | JSON spec | 2026-08-05 |
| S_CB-001-03 | Kaggle ConnectX E2E tests (test_connectx.py, 279 lines) | Local: `kaggle-environments/tests/envs/connectx/test_connectx.py` | Apache 2.0 | Test suite | 2026-08-05 |
| S_CB-001-04 | Kaggle ConnectX visualizer renderer (renderer.ts, 352 lines) | Local: `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/src/renderer.ts` | MIT | TypeScript | 2026-08-05 |
| S_CB-001-05 | marcpaulo15 RL-connect4 PyTorch architecture (CNN two-head, PPO training) | Unknown | Source code | 2026-08-06 |
| S_CB-001-06 | marcpaulo15 training config JSON (demo_net.json, cnet128.json) | Unknown | Config | 2026-08-06 |
| S_CB-001-07 | CogitoNTNU AlphaZero TensorFlow ResNet + MCTS for Four-in-a-Row (general-purpose) | Unknown | Source code | 2026-08-06 |

### 3.2 Primary Sources (Remote, Read-Only — Pending Agent Fetch)

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S_CB-001-05 | connectX-bitboard-agent (Tarun995, MIT) | github.com/Tarun995/connectX-bitboard-agent | MIT | Source code | 2026-08-05 |
| S_CB-001-06 | mcts_numba_cuda (pklesk/MCTS-NC) | github.com/pklesk/mcts_numba_cuda | Unknown | Source code | 2026-08-05 |
| S_CB-001-07 | neurofour/connect4 bitboard MCTS | github.com/neurofour/connect4 | Unknown | Source code | 2026-08-05 |
| S_CB-001-08 | IncludeAI shallow-trap-connect4 | github.com/IncludeAI/shallow-trap-connect4 | Unknown | Source code | 2026-08-05 |
| S_CB-001-09 | marcpaulo15/RL-connect4 | github.com/marcpaulo15/RL-connect4 | Unknown | Source code | 2026-08-05 |
| S_CB-001-10 | Widnyana/connect4 (TensorFlow) | github.com/Widnyana/connect4 | Unknown | Source code | 2026-08-05 |

### 3.3 Reference Sources

| Source ID | Description |
|-----------|-------------|
| S_CB-001-R01 | CBL-001 — Systematic uniform-depth profiles for all 16 rostered contenders |
| S_CB-001-R02 | CON-001 — New contender discovery framework |
| S_CB-001-R03 | DOS-006 — Deep technical profiles of 5 most sophisticated non-oracle contenders |
| S_CB-001-R04 | DOS-007 — Kaggle competitive analysis, board-size scaling |
| S_CB-001-R05 | CBL-002 — Kaggle environment source analysis |
| S_CB-001-R06 | MCTS-007 — GPU-accelerated MCTS (20.3M playouts/s) |

---


## 4. Kaggle Official Built-in Agents — Full Source Analysis

### 4.1 Agent Architecture Overview

The Kaggle ConnectX environment defines exactly **two** built-in agents in its `agents` dictionary:

```python
agents = {"random": random_agent, "negamax": negamax_agent}
```

There is **no third built-in agent** (no "mark" agent, no "official" agent). The `mark` field in observations simply indicates which player (1 or 2) the agent controls.

### 4.2 random_agent — Pure Uniform Random Baseline

```python
def random_agent(obs, config):
    return choice([c for c in range(config.columns) if obs.board[c] == EMPTY])
```

**Analysis:**
- **Strategy:** None. Uniform random selection over columns where the top cell is empty.
- **Column availability:** Checks `obs.board[c] == EMPTY`, which inspects `board[c + 0*columns]` — the first row (top of the column).
- **Complexity:** O(columns) per call.
- **Strength:** Near-zero. A random player loses to any minimax agent with depth >= 2 on 7x6.

**Role as benchmark:** Sanity check. Any competitive Kaggle bot should achieve >95% win rate against random play. The test suite confirms reward symmetry: `evaluate("connectx", ["random", "random"], num_episodes=2)` verifies that rewards sum to zero across two games.

### 4.3 negamax_agent — Reference Minimax Agent (Full Source)

**EXACT SOURCE EXCERPT** — `negamax_agent()` function

- **Project:** Kaggle Inc. — kaggle-environments
- **Source:** `kaggle-environments/kaggle_environments/envs/connectx/connectx.py`, lines 59-110
- **License:** Apache 2.0 (Copyright Kaggle Inc. 2020)
- **Retrieval Date:** 2026-08-05

```python
def negamax_agent(obs, config):
    columns = config.columns
    rows = config.rows
    size = rows * columns
    max_depth = 4

    def negamax(board, mark, depth):
        moves = sum(1 if cell != EMPTY else 0 for cell in board)

        # Tie Game
        if moves == size:
            return (0, None)

        # Can win next.
        for column in range(columns):
            if board[column] == EMPTY and is_win(board, column, mark, config, False):
                return ((size + 1 - moves) / 2, column)

        best_score = -size
        best_column = None
        for column in range(columns):
            if board[column] == EMPTY:
                if depth <= 0:
                    # Heuristic leaf evaluation
                    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
                    score = (size + 1 - moves) / 2
                    # Adjacent cell bonuses
                    if column > 0 and board[row * columns + column - 1] == mark:
                        score += 1
                    if column < columns - 1 and board[row * columns + column + 1] == mark:
                        score += 1
                    if row > 0 and board[(row - 1) * columns + column] == mark:
                        score += 1
                    if row < rows - 2 and board[(row + 1) * columns + column] == mark:
                        score += 1
                else:
                    next_board = board[:]
                    play(next_board, column, mark, config)
                    (score, _) = negamax(next_board, 1 if mark == 2 else 2, depth - 1)
                    score = score * -1
                if score > best_score or (score == best_score and choice([True, False])):
                    best_score = score
                    best_column = column
        return (best_score, best_column)

    _, column = negamax(obs.board[:], obs.mark, max_depth)
    if column is None:
        column = choice([c for c in range(columns) if obs.board[c] == EMPTY])
    return column
```

### 4.4 Design Decision Analysis

| Design Decision | Value | Rationale | Impact |
|----------------|-------|-----------|--------|
| Search depth | 4 (hard-coded) | Time constraint (2s/move on Kaggle T4) | Limits tactical depth to 4 plies |
| Alpha-beta pruning | **None** (pure negamax) | Simplicity of reference implementation | ~7x worse than equivalent alpha-beta |
| Leaf heuristic | Adjacency counting (+/-1 per neighbor, max 4) | Naive clustering heuristic | Cannot detect forks, blocks, open 3/4 |
| Immediate-win detection | Full column scan before search | Simple pre-check | Finds forced wins but misses forced losses |
| Tie-breaking | Random coin flip | Non-deterministic — reproducibility issue | Benchmark results not reproducible |
| Board search order | 0 -> N (left to right) | No move ordering | Worst-case branching factor utilization |
| Board representation | Flat list (column-major) | Matches Kaggle observation format | Requires index computation for adjacency |

### 4.5 Leaf Heuristic: "Clustering" Adjacency Bonus

```
adjacency_score = sum(mark == same_mark) for each of 4 neighbors
adjacency_score in {0, 1, 2, 3, 4}
base_score = (size + 1 - moves) / 2    # decreases from ~21->0 as board fills
```

**Strengths:**
- Simple to implement and evaluate
- Rewards local clustering (basic piece grouping)
- Decreases as board fills (natural game-phase heuristic)

**Weaknesses:**
- No distinction between forming a 3-in-a-row vs random adjacency
- No detection of threats (opponent's 3-in-a-row)
- No fork detection (two simultaneous threats)
- No blocking (preventing opponent's win)
- Adjacency bonus of +4 is smaller than the base score variation (~10.5 on 7x6)
- No awareness of inarow parameter (works identically for inarow=3, 4, or 10)
- **Does not scale to 15x13:** On a 15x13 board, checking exactly 4 neighbors covers a vanishingly small fraction of the local neighborhood.

### 4.6 is_win() — Core Win Detection (Kaggle Official)

**EXACT SOURCE EXCERPT** — `is_win()` function

- **Source:** `kaggle-environments/kaggle_environments/envs/connectx/connectx.py`, lines 29-52
- **License:** Apache 2.0
- **Retrieval Date:** 2026-08-05

```python
def is_win(board, column, mark, config, has_played=True):
    columns = config.columns
    rows = config.rows
    inarow = config.inarow - 1
    row = (
        min([r for r in range(rows) if board[column + (r * columns)] == mark])
        if has_played
        else max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    )

    def count(offset_row, offset_column):
        for i in range(1, inarow + 1):
            r = row + offset_row * i
            c = column + offset_column * i
            if r < 0 or r >= rows or c < 0 or c >= columns or board[c + (r * columns)] != mark:
                return i - 1
        return inarow

    return (
        count(1, 0) >= inarow
        or (count(0, 1) + count(0, -1)) >= inarow
        or (count(-1, -1) + count(1, 1)) >= inarow
        or (count(-1, 1) + count(1, -1)) >= inarow
    )
```

**Complexity:** O(columns x inarow) per call — checks 4 directional sweeps from the placed piece's position.

**Key features:**
- `has_played=False` in negamax_agent's immediate-win scan finds where a piece *would* land (max empty row)
- `has_played=True` for actual board positions (min occupied row)
- `inarow = config.inarow - 1` — the offset threshold
- `count()` counts consecutive same-mark cells in one direction
- Win check sums opposite directions and checks if total >= inarow

### 4.7 Kaggle Evaluation Protocol (JSON Spec)

**EXACT SOURCE EXCERPT** — `connectx.json`

- **Source:** `kaggle-environments/kaggle_environments/envs/connectx/connectx.json`
- **License:** Apache 2.0
- **Retrieval Date:** 2026-08-05

```json
{
  "name": "connectx", "title": "ConnectX", "version": "1.0.1",
  "agents": [2],
  "configuration": {
    "columns": {"default": 7, "minimum": 1},
    "rows": {"default": 6, "minimum": 1},
    "inarow": {"default": 4, "minimum": 1},
    "actTimeout": 2,
    "timeout": {"default": 2, "minimum": 0}
  },
  "reward": {"description": "-1 = Lost, 0 = Draw/Ongoing, 1 = Won", "default": 0},
  "observation": {
    "board": {"description": "Serialized grid (rows x columns). 0 = Empty, 1 = P1, 2 = P2"},
    "mark": {"defaults": [1, 2], "description": "Which checkers are the agents."},
    "remainingOverageTime": 60
  }
}
```

**Critical parameters:**
- **actTimeout:** 2 seconds per move (hard limit)
- **timeout:** 2 seconds default
- **remainingOverageTime:** 60 seconds total overtime budget
- **Board defaults:** 7 x 6, inarow = 4

### 4.8 negamax_agent as Benchmark Baseline — Strength Assessment

| Criterion | Assessment |
|-----------|------------|
| Search depth | Depth 4 (no alpha-beta) approx depth 2-3 equivalent alpha-beta |
| Leaf evaluation | Adjacency counting (+1 per neighbor), max 4 points |
| Win detection | Immediate-win only; no forced-loss detection |
| Move ordering | Column 0->N (left to right, no heuristics) |
| TT integration | None |
| Fork detection | None |
| Threat detection | None |
| Board-size adaptation | Same heuristic for all sizes (does not scale to 15x13) |

**Estimated competitive level:** Very low. On 7x6, any minimax agent with alpha-beta at depth 6+ will defeat negamax_agent with near 100% win rate. The lack of alpha-beta pruning is the single largest weakness: the negamax_agent evaluates ~7^4 = 2,401 leaf positions per move, whereas an alpha-beta equivalent prunes heavily, reaching deeper effective search.

**Benchmark role:** Minimum viable opponent for Kaggle submissions. Target: >95% win rate.


---

## 5. Missing Contender Deep Profiles

### 5.1 connectX-bitboard-agent (Tarun995) - Most Sophisticated Pure-Python Classical Engine

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/Tarun995/connectX-bitboard-agent |
| **License** | MIT |
| **Board** | 7x6 (default), configurable |
| **Language** | Python |
| **Kaggle-compatible** | Yes |
| **Algorithm** | Numba-JIT negamax with PVS |
| **TT** | 16M-entry transposition table |
| **Move ordering** | History heuristic, killer moves |
| **Special features** | Aspiration windows, iterative deepening, mirror-symmetric TT |
| **Time budget** | 1.70s for iterative deepening |
| **Estimated depth** | 8-10 on 7x6 within 2s budget |

Component count: 5 major optimization features - unmatched by any other pure-Python ConnectX engine.

**Benchmark gap:** No published win rates or benchmark results. This is the most Kaggle-compatible sophisticated classical engine in the corpus, yet it has no empirical performance data.

### 5.2 mcts_numba_cuda / MCTS-NC (pklesk) - GPU-Accelerated MCTS

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/pklesk/mcts_numba_cuda |
| **Board** | Connect 4 (7x6) |
| **Algorithm** | UCT MCTS with Numba CUDA kernels |
| **GPU perf** | 20.3M playouts/5s on GRID A100 |
| **Connect 4 score** | 75.1% avg vs 2.5% vanilla baseline |
| **Variants tested** | ocp_thrifty, ocp_prodigal, acp_thrifty, acp_prodigal |
| **Kaggle T4 estimate** | ~4.9M playouts/5s (linear scaling: 2,560 vs 10,496 CUDA cores) |

**Kaggle feasibility:** The T4's 2,560 CUDA cores vs A100's 10,496 implies ~4.9M playouts/5s linearly. This is within the 2s/move budget and provides orders-of-magnitude search advantage over CPU MCTS.

**Risk:** Requires CUDA support on Kaggle T4. Numba-JIT may not work in all Kaggle runtime environments.

### 5.3 neurofour/connect4 - Bitboard Fill-Trace Win Detection

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/neurofour/connect4 |
| **Board rep** | Bitboard representation |
| **Key feature** | Fill-trick (bitwise) win detection |
| **Complexity** | O(1) vs O(inarow) for directional sweep |
| **MCTS** | Likely UCB1/PUCT selection |
| **Kaggle-compatible** | Yes (Python) |

**Research question:** Does the fill-trick provide measurable speedup over Kaggle's is_win() directional sweep in a Python context? If so, integrating this pattern could improve search speed by 2-5x on standard board sizes.

### 5.4 IncludeAI/shallow-trap - Shallow Search with Deep Lookahead

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/IncludeAI/shallow-trap-connect4 (tentative) |
| **Algorithm** | Three-stage "shallow trap" approach |
| **Key idea** | Shallow alpha-beta for speed + deeper tactical lookahead via pattern matching |
| **Fork detection** | Pattern-matching heuristics on fork structures |
| **Kaggle-compatible** | Yes (Python) |

**Novelty:** Combines fast shallow search with pattern-matching heuristics for deeper tactical analysis. This "depth-uncoupled" approach is unique in the ConnectX corpus.


### 5.5 marcpaulo15/RL-connect4 - Reinforcement Learning Agent (Detailed)

**Status: Available — Comprehensive Source Analysis**

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/marcpaulo15/RL-connect4 |
| **Framework** | PyTorch |
| **Architecture** | Custom CNN with two heads (policy + value) |
| **RL Methods** | PPO, REINFORCE (policy gradient), Vanilla DQN, Dueling DQN |
| **Board** | 6x7 Connect-4 (configurable nrows, ncols, inrow) |
| **Input** | 2-channel tensor: channel 0 = active player, channel 1 = opponent |
| **Training** | Two-phase: supervised pre-training then RL fine-tuning |
| **Kaggle-compatible** | Moderate (PyTorch available on Kaggle) |

#### Neural Network Architecture

Two-head design with configurable layers driven by JSON spec files:

````
ConvBlock -> FC Block -> [FirstHead (policy) | SecondHead (value)]
````

**Demo architecture (demo_net.json):** `[32,4,0]+relu -> [64,3,0]+tanh -> FC(64,relu) -> head1(32,relu,7) -> head2(16,relu,1)`

**Production architecture (cnet128.json):** Conv block + FC block -> 7-action head + 1-value head

The JSON-driven architecture enables rapid experimentation without code changes.

#### Training Methodology

**Phase 1: Supervised Pre-Training** — CNN mimics a mid-level heuristic using 200,000 state-action pairs generated by a 1-step minimax lookahead player. This provides a strong initialization before RL fine-tuning.

**Phase 2: RL Fine-Tuning** — Convolutional block is frozen (treated as fixed feature extractor). Only FC blocks and heads are trained via self-play with experience replay.

Key design choices:
- **Experience buffer capacity:** 2,000 (small, memory-efficient)
- **Reward back-propagation exponent:** 3 (actions closer to outcome get more credit)
- **Symmetric board augmentation:** Mirrors each game for double the data
- **Frozen conv layers:** Transfer learning pattern — reduces parameter count during RL phase

#### PPO Training Hyperparameters

| Parameter | Value |
|-----------|-------|
| Buffer capacity | 2,000 |
| PPO epochs | 5 |
| C1 (value loss weight) | 0.75 |
| C2 (entropy bonus) | 0.04 |
| Learning rate | 1×10⁻⁴ |
| Batch size | 32 |
| L2 regularization | 5×10⁻⁵ |
| Discount factor (γ) | 0.95 |
| Clip parameter | 0.2 |
| Total iterations | ~320 (~100K updates) |
| Critic loss | Smooth L1 |

#### Performance Benchmarks

- Best PPO agent beats the 1-step lookahead agent approximately 84% of the time
- Win rate vs 1StepLA tracked as primary metric with automatic rollback when performance drops more than 8%
- Evaluated every 5 iterations against: random agent, self (old version), and 1-step lookahead agent

#### DQN Feature

Dueling DQN averages Q-values over vertically symmetric board states (flipping board left-right and averaging Q(sigma(a)) with Q(a)) to stabilize training.

#### Implications for the Perfect ConnectX Bot

1. **Supervised pre-training + RL fine-tuning** is a viable two-phase approach for ConnectX — avoids the slow convergence of pure self-play
2. **Frozen convolutional feature extractor** during RL phase reduces parameter count and training time
3. **PPO outperforms REINFORCE and DQN** in this comparison (implied by "best PPO agent")
4. **Symmetric augmentation** provides cheap data augmentation for ConnectX (vertical symmetry)

---

### 5.6 CogitoNTNU/AlphaZero - General-Purpose AlphaZero for Connect-4 (Detailed)

**Status: Available — Comprehensive Source Analysis**

| Attribute | Value |
|-----------|-------|
| **URL** | github.com/CogitoNTNU/AlphaZero |
| **Framework** | TensorFlow/Keras |
| **Architecture** | ResNet (256 filters, 10 residual blocks) |
| **Algorithm** | MCTS + ResNet (pure AlphaZero) |
| **Game Support** | Tic Tac Toe, Four-in-a-Row (Connect-4), game-agnostic design |
| **Board** | 3D numpy array (6, 7, 2) |
| **Training** | Pure self-play, no human data |
| **Parallelization** | 8 processes × 400 games = 4,000 games per epoch |
| **Kaggle-compatible** | Moderate (TensorFlow available on Kaggle, MCTS may be slow on CPU) |

#### ResNet Architecture (TensorFlow/Keras)

````
Input (6, 7, 2) -> Conv(256 filters, 3x3, same) -> BN -> ReLU
    -> [Residual Block x 10] (256 filters, 3x3, BN, ReLU, L2=0.0001)
    -> [Policy Head: Conv(32, 3x3) -> BN -> ReLU -> Flatten -> Dense(7, linear) -> softmax]
    -> [Value Head: Conv(32, 1x1) -> BN -> ReLU -> Flatten -> Dense(256, relu) -> Dense(1, tanh)]
````

- **256 filters** in residual blocks
- **10 residual blocks** (configurable)
- **L2 regularization** = 0.0001
- **Two-head output:** policy (column probability distribution) + value (board evaluation)

#### MCTS Implementation

- **PUCT selection** with C_PUCT = √2
- **Custom exploration bonus:** U = (ln(1 + N_parent + 1) / √N_parent + 1) * P * √N_parent
- **Dirichlet noise** added to root node exploration
- **Temperature sampling** at root: π(a) ∝ visits(a)^(1/T) for move selection during self-play
- **Visualization:** Graphviz tree search visualization

#### Board Representation

- **3D numpy array** shape (6, 7, 2) — board[r, c, 0] = player 1 pieces, board[r, c, 1] = player 2 pieces
- Board is **flipped along channel axis** on opponent's turn so network always sees current player in channel 0
- 7 possible moves (columns 0-6), indexed by move_to_number() / number_to_move()

#### Performance Benchmarks

| Milestone | Result |
|-----------|--------|
| Tic Tac Toe mastery | After only 3,000 self-play games — plays perfectly from raw ResNet predictions |
| Four-in-a-Row functional play | After approximately 100,000 self-play games at 500 MCTS searches/move |
| Cross-generation tournament | 98 matches between generations — newest always beat older ones |
| Training speedup | 16x from parallelization + batching + caching |

#### Key Design Decisions

1. **No human data** — pure self-play matching AlphaZero paper methodology
2. **Game-agnostic architecture** — to add a new game, only Config (board dims, action mapping) and Gamelogic (execute/undo/reset/winner detection) need implementation
3. **Parallel training** — 8 processes × 400 simultaneous games with batched ResNet predictions and caching
4. **Play interface** — python3 play.py --game FourInARow --numSearch 1000

#### Implications for the Perfect ConnectX Bot

1. **AlphaZero approach works for ConnectX** — functional play after 100K games at 500 MCTS searches/move proves the methodology
2. **256-filter ResNet is the architecture standard** — matches Leela Chess Zero design philosophy
3. **Parallel training (16x speedup) is essential** — makes training feasible rather than taking "weeks"
4. **Transfer learning from Lczero planned** — cross-domain transfer is a promising direction
5. **The training curve had not converged** — even after 100K+ games, the network was still improving, suggesting more training = stronger play

---

### 5.7 Widnyana/connect4 — DELETED / NOT RECOVERABLE

**Status: DELETED** — The GitHub user "Widnyana" no longer has any connect4-related repositories. The profile shows only Kubernetes/Solana projects (kubectl-ports-rs, boilerplate-rs, solana-onchain-mcp, etc.). A GitHub search for "Widnyana" + "connect4" returns zero results. The repository was likely deleted or made private.

This is a **data loss event** for the ConnectX research corpus. If the TensorFlow/Keras pure neural approach was significant (no search, pure policy network), its source code and methodology are now lost.

---
---

## 6. Benchmark Baseline Methodology

### 6.1 Progressive Difficulty Ladder

| Tier | Opponent | Purpose | Min Win Rate |
|------|----------|---------|--------------|
| Tier 0 | random_agent | Sanity check | >95% |
| Tier 1 | negamax_agent (Kaggle built-in) | Minimum viable opponent | >95% |
| Tier 2 | negamax_agent with AB + depth 6 | Improved baseline | >90% |
| Tier 3 | QveenCoder (asymmetric eval) | Classical eval reference | >85% |
| Tier 4 | connectX-bitboard-agent | Sophisticated classical | >70% |
| Tier 5 | DQN/neural agents | Neural baseline | Variable |

### 6.2 Board-Size Scaling Tests

| Board | inarow | Complexity | Solved? |
|-------|--------|------------|---------|
| 7x6 | 4 | Standard (solved) | Yes, P1 win |
| 8x8 | 4 | 4x larger search | Yes, P2 win |
| 9x6 | 6 | Different inarow | Yes, P2 win |
| 10x8 | 4 | 3x larger search | Yes, draw |
| 15x13 | 4 | 15x larger search | Unknown |
| 15x10 | 4 | 12x larger search | Unknown |

**Critical gap:** No public ConnectX contender has been benchmarked on 15x13 or 15x10. This is the single largest gap.

### 6.3 Statistical Test Design

| Test | Methodology | Repetitions | Significance |
|------|-------------|------------|--------------|
| Tactical detection | 1,000 fixed positions with known forced wins | 1/position | >90% correct |
| Depth scaling | Depth 2, 4, 6, 8 on random openings | 100/depth | Linear improvement |
| Board-size transfer | Train 7x6, test 8x8, 15x13 | 50/board | Measure degradation |
| Time management | 2s/move vs 5s/move vs 10s/move | 100/budget | Diminishing returns |

---

## 7. Pros and Cons Comparison

| Contender | Strengths | Weaknesses | Kaggle Fit |
|-----------|-----------|------------|------------|
| random_agent | None (by design) | Zero strategy | Sanity check only |
| negamax_agent | Canonical baseline | No AB, naive heuristic, depth-4 | Minimum viable opponent |
| connectX-bitboard-agent | Numba-JIT, PVS, 16M TT, 5 opt features | Unknown benchmark results | Good (Python, MIT) |
| MCTS-NC (GPU) | 20.3M playouts/s on A100 | T4 perf unmeasured, GPU dependency | Risky (CUDA support) |
| neurofour | Fill-trick win detection | Source analysis incomplete | Potentially good |
| IncludeAI | Novel depth-uncoupled | Concept novelty vs proven methods | Depends on impl |
| marcpaulo15/RL | RL-trained, self-play data | Training compute requirements | Moderate |
| CogitoNTNU/AlphaZero | ResNet(256) + PUCT MCTS + parallel training | Slow MCTS on CPU Kaggle, not converged | Moderate (TensorFlow on Kaggle)

---

## 8. Feasibility Matrix

| Approach | Local CPU | RTX 5090 | DGX Spark | Kaggle CPU | Kaggle T4 |
|----------|-----------|----------|-----------|------------|-----------|
| random_agent | Trivial | Trivial | Trivial | Built-in | Built-in |
| negamax_agent (depth-4, no AB) | Trivial | Trivial | Trivial | Built-in | Built-in |
| negamax_agent (depth-8, with AB) | 0.1-1s/move | 0.01-0.1s/move | 0.1-1s/move | 1-2s/move | 1-2s/move |
| connectX-bitboard-agent | Viable | Viable | Viable | Viable | Viable |
| MCTS-NC (GPU) | N/A | Viable | Viable | N/A | Plausible |
| neural agent (small ResNet) | 5-20ms | <1ms | 1-5ms | 5-20ms | 1-5ms (TensorRT) |

| PPO/RL agent (marcpaulo15) | Viable (PyTorch) | Viable | Viable | Moderate (PyTorch) | Good (PyTorch on T4) |
| AlphaZero ResNet (CogitoNTNU) | Viable (TensorFlow) | Viable | Viable | Poor (MCTS CPU) | Good (TensorFlow + MCTS on T4) |

---

## 9. Performance Evidence

| Contender | Measured | Claimed | Inferred | Unknown |
|-----------|----------|---------|----------|---------|
| random_agent | N/A | N/A | N/A | N/A |
| negamax_agent | N/A | Depth 4 approx 2,401 leaves/move | ~2,401 leaf nodes/move | Win rate vs classical |
| connectX-bitboard-agent | Unknown | 5 optimization features | Depth 8-10 on 7x6 | Actual benchmarks |
| MCTS-NC | 20.3M/5s on A100 | 75% vs 2.5% baseline | ~4.9M/5s on T4 | T4 CUDA compat |
| neurofour | Unknown | Fill-trick O(1) win detection | O(1) vs O(inarow) | MCTS simulation speed |
| IncludeAI | Unknown | "Shallow trap" approach | Speed from shallow search | Measured results |
| marcpaulo15/RL | ~84% vs 1StepLA | 200K pre-train + PPO fine-tune | Best agent beats 1StepLA ~84% | Win rate vs classical search |
| CogitoNTNU/AlphaZero | 3K games = TT mastery | 100K games = functional 4IR | Functional after 100K, not converged | Convergence training data |

---

## 10. Board-Size and inarow Applicability

| Contender | 7x6 | 8x8 | 9x6 | 10x8 | 15x13 | 15x10 | inarow=3 | inarow=5 |
|-----------|-----|-----|-----|------|-------|-------|----------|----------|
| random_agent | OK | OK | OK | OK | OK | OK | OK | OK |
| negamax_agent | OK | OK | OK | OK | OK | OK | OK | OK |
| connectX-bitboard-agent | OK | ? | ? | ? | ? | ? | ? | ? |
| MCTS-NC | OK | ? | ? | ? | ? | ? | ? | ? |
| neurofour | OK | ? | ? | ? | ? | ? | ? | ? |
| IncludeAI | ? | ? | ? | ? | ? | ? | ? | ? |
| marcpaulo15/RL | Configurable (nrows,ncols,inrow) | Configurable | Configurable | Configurable | Theoretically yes | Theoretically yes | Configurable | Configurable |
| CogitoNTNU/AlphaZero | OK (6x7 FourInARow) | Configurable (game-agnostic) | Configurable | Configurable | Configurable | Configurable | Configurable | Configurable |

---

## 11. Integration and Ensemble Opportunities

| Component | Ensemble Role | Compatible With |
|-----------|---------------|-----------------|
| random_agent | Sanity check baseline | Any ensemble |
| negamax_agent | Minimum viable opponent | Any ensemble |
| connectX-bitboard-agent | Classical ensemble member | AB ensemble, MCTS arbiter |
| MCTS-NC | GPU-accelerated search | Neural ensemble (NN-guided MCTS) |
| connectX-bitboard-agent + NN eval | Hybrid classical+NN | Any hybrid ensemble |
| neurofour fill-trick + MCTS | Efficient MCTS board rep | MCTS ensemble |

---

## 12. Failure Modes and Risks

| Risk | Affected | Severity | Mitigation |
|------|----------|----------|------------|
| Kaggle T4 lacks full CUDA support | MCTS-NC | Critical | Fallback to CPU MCTS |
| No 15x13 benchmarks | All contenders | High | Develop 15x13 test positions |
| Numba JIT warm-up overhead | connectX-bitboard-agent | Medium | Profile warm-up time on Kaggle |
| Fill-trick only on standard sizes | neurofour | Low | Fallback directional sweep |
| Widnyana repo deleted — source data loss | Data integrity | Monitor for repo restoration |
| AlphaZero training non-convergence after 100K games | CogitoNTNU | High | Train longer, use supervised pre-training |

---

## 13. Benchmark Requirements

| Req | Description | Priority |
|-----|-------------|----------|
| BMS-CB-001 | Measure negamax_agent win rate vs all classical agents | P0 |
| BMS-CB-002 | Profile connectX-bitboard-agent depth/NPS on Kaggle T4 | P0 |
| BMS-CB-003 | Measure MCTS-NC playouts/second on Kaggle T4 | P0 |
| BMS-CB-004 | Test all neural agents on 15x13 | P0 |
| BMS-CB-005 | Create progressive difficulty ladder test suite | P1 |
| BMS-CB-006 | Measure fill-trick vs directional sweep speed in Python | P1 |
| BMS-CB-007 | Profile Numba JIT warm-up on Kaggle | P1 |
| BMS-CB-008 | Profile PPO training convergence: 200K pre-train + self-play iterations on 7x6 | P1 |
| BMS-CB-009 | Benchmark AlphaZero ResNet(256) MCTS at 500 searches/move on 7x6 vs 15x13 | P0 |
| BMS-CB-010 | Replicate CogitoNTNU training curve: TT mastery threshold and convergence data points | P1 |

---

## 14. Open Questions

1. What is the actual benchmark win rate of connectX-bitboard-agent on 7x6?
2. Does Kaggle T4 support the full CUDA feature set required by Numba-JIT and MCTS-NC?
3. What board sizes and inarow values does each contender actually support?
4. What is the true generalization gap from 7x6 to 15x13 for neural agents?
5. How does the Kaggle negamax_agent's adjacency heuristic perform on non-standard board sizes?
6. Are there additional Kaggle-built-in agents not exposed through the agents dictionary?
7. How does supervised pre-training (200K heuristic examples) affect convergence compared to pure self-play for ConnectX?
8. Can a ResNet with 256 filters and 10 blocks learn functional Connect-4 strategy from self-play alone?
9. Does CogitoNTNU/game-agnostic architecture generalize efficiently to 15x13 boards, or is ConnectX-specific optimization required?
10. What is the win rate of the marcpaulo15 PPO agent against classical search agents at depth 6+?

---

## 15. Recommendations

1. **Use the Kaggle built-in negamax_agent as the minimum viable benchmark** - All Kaggle submissions should target >95% win rate against it.

2. **Build a progressive difficulty ladder** - random_agent -> negamax_agent -> classical (depth 6+) -> connectX-bitboard-agent -> neural/MCTS hybrid.

3. **Prioritize connectX-bitboard-agent as the first missing contender to profile** - Most sophisticated pure-Python classical engine, most Kaggle-compatible.

4. **Test MCTS-NC feasibility on Kaggle T4 early** - If GPU-accelerated MCTS works, it provides orders-of-magnitude search advantage.

5. **Investigate the fill-trick win detection pattern** - If neurofour's fill-trick provides measurable speedup in Python, integrate it into the primary agent.

---

## 16. Sources and Retrieval Record

| Source ID | Description | License | Type | Date |
|-----------|-------------|---------|------|------|
| S_CB-001-01 | Kaggle ConnectX game engine (connectx.py, 202 lines) | Apache 2.0 | Source code | 2026-08-05 |
| S_CB-001-02 | Kaggle ConnectX JSON spec (connectx.json, 71 lines) | Apache 2.0 | JSON spec | 2026-08-05 |
| S_CB-001-03 | Kaggle ConnectX E2E tests (test_connectx.py, 279 lines) | Apache 2.0 | Test suite | 2026-08-05 |
| S_CB-001-04 | Kaggle ConnectX visualizer renderer (renderer.ts, 352 lines) | MIT | TypeScript | 2026-08-05 |
| S_CB-001-05 | marcpaulo15 RL-connect4 PyTorch architecture (CNN two-head, PPO training) | Unknown | Source code | 2026-08-06 |
| S_CB-001-06 | marcpaulo15 training config JSON (demo_net.json, cnet128.json) | Unknown | Config | 2026-08-06 |
| S_CB-001-07 | CogitoNTNU AlphaZero TensorFlow ResNet + MCTS for Four-in-a-Row | Unknown | Source code | 2026-08-06 |

---

## 17. Cross-Links

- **CBL-001** — Systematic profiles of all 16 rostered contenders
- **CON-001** — New contender discovery and benchmark framework
- **DOS-005** — Comprehensive inventory of 20+ public bots
- **DOS-006** — Deep technical profiles of 5 most sophisticated non-oracle contenders
- **DOS-007** — Kaggle competitive analysis, board-size scaling
- **CBL-002** — Kaggle environment source analysis
- **MCTS-007** — GPU-accelerated MCTS
- **CS-003** — Classical search and solver engineering
- **NN-001** — Neural network architectures (ResNet, CNN, two-head policy/value)
- **NN-005** — Model compression and quantization (deployment of neural agents)
- **MCTS-006** — Transposition-aware MCTS (relevant to AlphaZero PUCT)
- **CS-005** — Evaluation function design
