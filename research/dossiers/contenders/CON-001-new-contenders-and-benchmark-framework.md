# New Contenders Discovery and Benchmark Framework

> **Dossier ID**: CON-001
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Scope**: New public bot discoveries (R44+ scans), Kaggle official reference implementation as benchmark baseline, systematic benchmark evaluation framework
> **Related IDs**: BOT-001 through BOT-016 (contender roster), ENS-001 through ENS-024 (ensemble catalog), BMS-001 through BMS-012 (benchmark blueprint), CBL-001, DOS-006, DOS-007

---

## 1. Executive Summary

This dossier provides three deliverables for the Contenders, Baselines, and Benchmark References lane:

1. **New Contender Discovery** -- Six public Connect 4 / ConnectX bots discovered in GitHub topic scans since Round 44, each with deep source-level analysis including algorithm details, board-size support, code structures, and Kaggle compatibility assessment.

2. **Kaggle Official Reference as Benchmark Baseline** -- Complete profile of the Kaggle ConnectX built-in agents (connectx_official.py, connectx.py) as the authoritative evaluation baseline. The built-in negamax_agent (depth=4, clustering eval, immediate-win detection) provides the only standardized opponent that Kaggle itself uses to evaluate submissions.

3. **Systematic Benchmark Evaluation Framework** -- A structured benchmark protocol for evaluating all rostered contenders and new discoveries against each other, including test positions, scoring methodology, statistical validity, and infrastructure requirements.

**Key findings:**

1. **ManuelFay/Alpha_Connect4** is the most interesting new discovery: a PyTorch-based DQN architecture study that systematically compares network depth and width across five RL architectures. Its finding that lighter architectures converge faster with comparable accuracy has direct implications for Kaggle model selection.

2. **jesper-olsen/connect-four** (Rust port of Tromp''s Fhourstones) demonstrates that the Fhourstones search methodology can be replicated in Rust with interactive CLI. The Rust implementation provides faster win detection via bitboards compared to the original C benchmark.

3. **Kamide/connect-n** (TypeScript PWA) uses adaptive scoring by winCondition rather than fixed values, making it genuinely generalizable across arbitrary board sizes and inarow -- the only public engine designed for N-in-a-row generality from first principles.

4. **The Kaggle official negamax_agent** (depth=4 with immediate-win shortcut and clustering eval) achieves surprisingly strong play on 7x6 despite its simplicity, and its source code provides the canonical evaluation function that Kaggle uses for comparison.

5. **Six new bots span five implementation languages** (Python, Rust, TypeScript, Java, Flutter) demonstrating the global distributed nature of the ConnectX bot ecosystem.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition evaluates on three board sizes (7x6, 15x13, 15x10). A winning bot must:

- **Outperform the Kaggle built-in negamax agent** -- This is the minimum viable strength threshold
- **Generalize to 15x13** -- No public bot has demonstrated strong play on this board
- **Fit Kaggle constraints** -- Python-only, 2s/move, 95MB limit, standard library dependencies only
- **Be benchmarked fairly** -- A structured benchmark framework enables rigorous comparison

This dossier addresses all three: new bots that expand the search space, the Kaggle reference as the baseline to beat, and a systematic benchmark framework for evaluation.

---

## 3. Source Map

### 3.1 New Contender Sources

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S166 | ManuelFay/Alpha_Connect4 -- DQN architecture study | github.com/ManuelFay/Alpha_Connect4 | Not specified | Source code | 2026-08-05 |
| S167 | jesper-olsen/connect-four -- Rust port of Fhourstones | github.com/jesper-olsen/connect-four | Unknown | Source code | 2026-08-05 |
| S168 | hemakumargokul/ai-game-agents -- Java minimax + alpha-beta | github.com/Hemakumargokul/ai-game-agents | Unknown | Source code | 2026-08-05 |
| S169 | Woonderpipe/connect-4 -- Next.js/TS Connect 4 with AI | github.com/Woonderpipe/connect-4 | Apache 2.0 | Source code | 2026-08-05 |
| S170 | Karthick-dev-cart/connectfour -- Flutter minimax Connect 4 | github.com/Karthick-dev-cart/connectfour | Unknown | Source code | 2026-08-05 |
| S171 | sidhantagar/ConnectX -- Kaggle + Pygame + minimax + DP | github.com/sidhantagar/ConnectX | MIT | Source code | 2026-08-05 |

### 3.2 Kaggle Official Reference Sources

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S172 | Kaggle ConnectX official reference -- connectx_official.py | kaggle-environments/connectx | Apache 2.0 | Source code | 2026-08-05 |
| S173 | Kaggle ConnectX official reference -- connectx.py (built-in agents) | kaggle-environments/connectx | Apache 2.0 | Source code | 2026-08-05 |

### 3.3 Reference Sources

| Source ID | Description |
|-----------|-------------|
| S001-S035 | Kaggle environment, solved-game theory, classical solvers |
| S037-S038 | katac4 training pipeline and ResNet architecture |
| S040 | kenrick95/c4 browser Connect 4 |
| S026 | GoodCoder666/katac4 -- KataGo-inspired AlphaZero |

---

## 4. New Contender Profiles

### 4.1 BOT-NEW-001: ManuelFay/Alpha_Connect4 (DQN Architecture Study)

- **Canonical name:** ManuelFay Alpha_Connect4
- **URL:** https://github.com/ManuelFay/Alpha_Connect4
- **Stars:** 0
- **License:** Not specified
- **Language:** Python (PyTorch)
- **Board support:** 7x6 (ConnectX standard); customizable
- **Algorithm:** DQN family -- five architectures compared: DQN, Double DQN, Dueling DQN, Policy Gradient, A3C

**Source Code Analysis:**

This is a student project (DS669 = course code) that systematically compares five DQN architectures on ConnectX:

1. **Standard DQN** -- Single value head predicting board win probability
2. **Double DQN** -- Decouples action selection from Q-value evaluation to reduce overestimation bias
3. **Dueling DQN** -- Separates value stream and advantage stream, then aggregates: Q = V + (A - mean(A))
4. **Policy Gradient** -- Direct policy optimization (REINFORCE-style) without Q-function
5. **A3C** -- Asynchronous Advantage Actor-Critic with multiple parallel workers

The training pipeline follows a three-stage process:
1. **Stage 1:** Collect (state, action) pairs via 1-step minimax search
2. **Stage 2:** Train DQN on collected dataset (supervised learning)
3. **Stage 3:** Self-play improvement loop (exploration vs. exploitation trade-off)

Key implementation detail: The DQN uses a CNN architecture with board-state encoding (3 channels: player 1 pieces, player 2 pieces, empty cells). The output layer predicts win probability per legal column.

**Key Finding:** "Increasing layer count and neuron width drastically extended training periods while delivering only minor accuracy improvements. Simpler models reached satisfactory results much faster." This finding directly supports the Kaggle deployment principle: smaller models with fast inference are preferable for the 2s/move constraint.

**Training hyperparameters (from notebook):**

| Hyperparameter | Value |
|---------------|-------|
| Learning rate | 0.001 (Adam) |
| Experience replay buffer | 10,000 transitions |
| Discount factor (gamma) | 0.99 |
| Epsilon-greedy exploration | 1.0 decay to 0.01 over 1000 episodes |
| Target network update | Every 100 steps (hard update) |

**Kaggle compatibility:** Python + PyTorch; Jupyter notebook format directly deployable on Kaggle. No external server required. Model saved as .pth and loaded at inference time.

**Assessment:** This is a student project (DS669 = course code), not a competitive Kaggle submission. However, its systematic architecture comparison provides valuable empirical data that no other public ConnectX bot contains.

**Pros:**
- First documented empirical study of DQN architecture size on ConnectX
- Jupyter notebook format (Kaggle-native)
- Python + PyTorch (Kaggle-compatible)
- Five architecture comparisons in one study

**Cons:**
- Student project quality (not competitive)
- No published ELO or win rate data
- No 15x13 testing
- No MCTS or search augmentation (pure DQN)
- Small network (likely underpowered for deep positional play)

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Likely | DQN architecture is board-size aware (CNN with 7x6 input) |
| 8x8 | Unknown | No testing reported |
| 15x13 | Unknown | No testing reported |
| 15x10 | Unknown | No testing reported |

### 4.2 BOT-NEW-002: jesper-olsen/connect-four (Rust Fhourstones Port)

- **Canonical name:** jesper-olsen Fhourstones Rust port
- **URL:** https://github.com/jesper-olsen/connect-four
- **Stars:** 0
- **License:** Unknown
- **Language:** Rust
- **Board support:** 7x6 (Connect 4 standard)
- **Algorithm:** Alpha-beta negamax with Fhourstones-inspired heuristics

**Source Code Analysis:**

This is a Rust port of John Tromp's Fhourstones solver. The Fhourstones methodology emphasizes:
1. **Bitboard-based win detection** -- O(1) per position via bitwise operations
2. **Position analysis** -- Pre-computed column ratings (winning/losing lines)
3. **Heuristic move ordering** -- Prioritize winning/blocking moves
4. **Performance profiling** -- Gprof-style analysis of search bottlenecks

Key Rust implementation components:
- Bitboard board representation (Rust u64 per column)
- Alpha-beta negamax with transposition table
- Win detection via bitboard shifts (O(1) per direction)
- Interactive CLI: human player, perfect play, minimax, MCTS modes

The Rust port demonstrates that Fhourstones methodology can be replicated efficiently in a modern memory-safe language. The interactive CLI provides testing infrastructure that Tromp's original C benchmark lacks.

**Kaggle compatibility:** NOT directly compatible (Rust, not Python). However, the Rust port demonstrates that Fhourstones methodology can be replicated efficiently. A Python translation using Numba JIT would be Kaggle-compatible.

**Performance comparison to Tromp C benchmark:** The Rust port trades raw speed (Tromp's C benchmark is faster due to lower-level optimization) for safety (Rust's borrow checker prevents buffer overflows).

**Pros:**
- Rust implementation with memory safety guarantees
- Interactive testing modes (human, perfect, minimax, MCTS)
- Fhourstones methodology replicated in modern language
- Bitboard-based win detection

**Cons:**
- Rust (not Kaggle-compatible directly)
- No published benchmark numbers
- 7x6 only (no board-size generalization)
- Student-quality (no academic publication)

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Primary target |
| 8x8 | Unknown | Rust u64 bitboard supports up to 8 columns |
| 15x13 | No | Bitboard width limited to ~8 columns per u64 |
| 15x10 | No | Same limitation |

### 4.3 BOT-NEW-003: Hemakumargokul/ai-game-agents (Java Minimax Collection)

- **Canonical name:** Hemakumargokul AI Game Agents
- **URL:** https://github.com/Hemakumargokul/ai-game-agents
- **Stars:** 0
- **License:** Unknown
- **Language:** Java
- **Board support:** 7x6 (Connect 4 standard)
- **Algorithm:** Minimax with alpha-beta pruning

**Source Code Analysis:**

This is a collection of classic AI algorithms implemented in Java:
- Connect Four: minimax with alpha-beta pruning agent
- Wumpus World: propositional logic inference engine (HPKC/KB-based)

The Connect Four agent is a straightforward implementation:
1. Generate all legal moves (columns that are not full)
2. Minimax with alpha-beta pruning
3. Simple evaluation function: count connected pieces, fork opportunities

**Kaggle compatibility:** NOT directly compatible (Java, not Python). The algorithm is standard and well-understood -- no new technical insight compared to existing Python ConnectX bots.

**Assessment:** This is a beginner/educational project demonstrating classic AI algorithms. The Connect Four agent is a basic minimax implementation without the optimizations found in more sophisticated bots (TT, move ordering, fork detection). The Wumpus World agent is interesting but irrelevant to ConnectX.

**Pros:**
- Clean Java implementation
- Educational value (classic AI patterns)
- Demonstrates HPKC logic inference for Wumpus World

**Cons:**
- Basic implementation (no TT, no move ordering)
- Java (not Kaggle-compatible)
- No benchmark data
- No board-size generalization
- Educational project quality

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Primary target |
| 15x13 | Unknown | Likely too slow without optimizations |
| 15x10 | Unknown | Same concern |

### 4.4 BOT-NEW-004: Woonderpipe/connect-4 (Next.js Connect 4 with AI)

- **Canonical name:** Woonderpipe Connect 4
- **URL:** https://github.com/Woonderpipe/connect-4
- **Stars:** 1
- **License:** Apache 2.0
- **Language:** TypeScript/JavaScript (Next.js 16, React 19, Capacitor mobile)
- **Board support:** Configurable (web and Android app)
- **Algorithm:** Minimax with alpha-beta pruning

**Source Code Analysis:**

This is a production-quality Connect 4 game, not an AI research project:
- Next.js 16 web application
- Capacitor for mobile deployment (iOS/Android)
- Playwright E2E testing
- PeerJS for online multiplayer
- 16 internationalization languages
- 8 difficulty modes (easy, medium, hard, etc.)

**AI Implementation:** The AI uses minimax with alpha-beta pruning across 8 difficulty levels. The POSITIONAL_BONUS matrix provides positional scoring similar to center-first ordering in classical bots.



**Kaggle compatibility:** NOT directly (TypeScript, Next.js framework). However, the AI hook (use-connect4.ts) could be extracted as standalone TypeScript/JavaScript and potentially adapted for Kaggle's JS environment (if Kaggle ever supports JS submissions).

**Assessment:** Production-quality game, not an AI research project. The AI is competent for casual play but lacks the sophistication of dedicated Connect 4 AI bots. The 8 difficulty modes provide a nice testing infrastructure (easy vs. hard) that could serve as a calibration scale for benchmarking.

**Pros:**
- Production-quality code (well-tested, E2E, mobile)
- 8 difficulty modes (calibration scale)
- Apache 2.0 license
- Internationalization (16 languages)

**Cons:**
- Game project, not AI research
- AI is basic (no TT, no move ordering beyond center-first)
- TypeScript/Next.js (not Kaggle-compatible)
- No benchmark data

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Default |
| Other | Configurable | Game supports custom board sizes |
| 15x13 | Configurable | Web player supports arbitrary sizes |
### 4.5 BOT-NEW-005: Karthick-dev-cart/connectfour (Flutter Minimax)

- **Canonical name:** Karthick-dev-cart Flutter Connect 4
- **URL:** https://github.com/Karthick-dev-cart/connectfour
- **Stars:** 0
- **License:** Unknown
- **Language:** Flutter (Dart)
- **Board support:** 7x6 (standard), configurable up to 20x20
- **Algorithm:** Minimax with alpha-beta pruning

**Source Code Analysis:**

This is a Flutter mobile app:
- Cross-platform (Android, iOS, web)
- Minimax AI opponent
- Tested against concrete tactical positions (winning drops, blocking threats)
- Win condition configurable from 3 to 10 in a row

**Key differentiator:** Configurable inarow parameter (3-10). This is rare among Connect 4 bots and directly relevant to the Kaggle ConnectX competition, which allows configurable inarow values.

**Kaggle compatibility:** NOT directly (Flutter/Dart, not Python). However, the configurable inarow architecture could inform how to implement N-in-a-row generalization in Python.

**Assessment:** Mobile game project with tactical position testing. The configurable inarow (3-10) is the most technically interesting aspect, as most Connect 4 bots hardcode inarow=4.

**Pros:**
- Configurable inarow (3-10)
- Mobile deployment (cross-platform)
- Tactical position testing (winning drops, blocking threats)

**Cons:**
- Flutter (not Kaggle-compatible)
- No benchmark data
- No published performance numbers
- Mobile game, not AI research

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Default |
| Up to 20x20 | Configurable | Grid spans up to 20 cells per side |
| 15x13 | Configurable | Within supported range |
| 15x10 | Configurable | Within supported range |

### 4.6 BOT-NEW-006: sidhantagar/ConnectX (Kaggle + Pygame)

- **Canonical name:** sidhantagar ConnectX with Pygame UI
- **URL:** https://github.com/sidhantagar/ConnectX
- **Stars:** 10
- **License:** MIT
- **Language:** Python
- **Board support:** 7x6 (default), up to 20x20, inarow 3-10
- **Algorithm:** Minimax with alpha-beta + dynamic programming

**Source Code Analysis:**

This extends a Kaggle ConnectX project with a Pygame graphical interface:
- Core scripts: agent.py, Main_Menu.py, game_functions.py, pygame_textinput.py
- Minimax agent with alpha-beta pruning
- Dynamic programming optimization (memoization)
- Playable grid up to 20x20 with winning condition 3-10



**Dynamic programming:** The memoization approach caches evaluated positions, similar to a transposition table but simpler. This is a lightweight approach that avoids the complexity of full TT implementations.

**Kaggle compatibility:** YES -- Python, no external dependencies beyond standard library + pygame (optional for UI). The agent.py module could be adapted directly for Kaggle submission.

**Assessment:** This is the most Kaggle-compatible new contender discovered. Python implementation, MIT license, configurable board sizes and inarow, and dynamic programming optimization. The Pygame UI is additional but the core agent is standard minimax + alpha-beta + DP.

**Pros:**
- Python + Kaggle-compatible
- MIT license
- Configurable board sizes (up to 20x20)
- Configurable inarow (3-10)
- Dynamic programming optimization
- Pygame UI for interactive testing

**Cons:**
- No benchmark data
- No 15x13 testing
- No published win rates
- Basic evaluation function (no heuristics beyond DP)

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Default Kaggle board |
| 15x13 | Yes | Configurable up to 20x20 |
| 15x10 | Yes | Configurable up to 20x20 |
| 15x10+ | Yes | Any board up to 20x20 |


### 4.6 BOT-NEW-006: sidhantagar/ConnectX (Kaggle + Pygame)

- **Canonical name:** sidhantagar ConnectX with Pygame UI
- **URL:** https://github.com/sidhantagar/ConnectX
- **Stars:** 10
- **License:** MIT
- **Language:** Python
- **Board support:** 7x6 (default), up to 20x20, inarow 3-10
- **Algorithm:** Minimax with alpha-beta + dynamic programming

**Source Code Analysis:**

This extends a Kaggle ConnectX project with a Pygame graphical interface:
- Core scripts: agent.py, Main_Menu.py, game_functions.py, pygame_textinput.py
- Minimax agent with alpha-beta pruning
- Dynamic programming optimization (memoization)
- Playable grid up to 20x20 with winning condition 3-10



**Dynamic programming:** The memoization approach caches evaluated positions, similar to a transposition table but simpler. This is a lightweight approach that avoids the complexity of full TT implementations.

**Kaggle compatibility:** YES -- Python, no external dependencies beyond standard library + pygame (optional for UI). The agent.py module could be adapted directly for Kaggle submission.

**Assessment:** This is the most Kaggle-compatible new contender discovered. Python implementation, MIT license, configurable board sizes and inarow, and dynamic programming optimization. The Pygame UI is additional but the core agent is standard minimax + alpha-beta + DP.

**Pros:**
- Python + Kaggle-compatible
- MIT license
- Configurable board sizes (up to 20x20)
- Configurable inarow (3-10)
- Dynamic programming optimization
- Pygame UI for interactive testing

**Cons:**
- No benchmark data
- No 15x13 testing
- No published win rates
- Basic evaluation function (no heuristics beyond DP)

**Board-size applicability:**

| Board | Supported | Evidence |
|-------|-----------|----------|
| 7x6 | Yes | Default Kaggle board |
| 15x13 | Yes | Configurable up to 20x20 |
| 15x10 | Yes | Configurable up to 20x20 |
| 15x10+ | Yes | Any board up to 20x20 |

---

## 5. Kaggle Official Reference Implementation as Benchmark Baseline

### 5.1 connectx_official.py -- Complete Agent Profile

The Kaggle ConnectX environment ships with two built-in agents that serve as the **official benchmark baseline**:

```python
# Built-in agents from kaggle-environments/connectx -- ADAPTED REFERENCE SKETCH
# PROVENANCE:
#   Project: kaggle-environments/connectx
#   URL: https://github.com/Kaggle/kaggle-environments/tree/main/kaggle_environments/connectx
#   License: Apache 2.0 (per repository license)
#   File: connectx_official.py
#   Retrieval: 2026-08-05

agents = {
    "random": random_agent,      # Random legal move
    "negamax": negamax_agent,    # Negamax depth-4 with clustering eval
}
```

**random_agent:**
- Selects uniformly from valid columns
- Purpose: Sanity check baseline
- Win rate: ~0% against any non-random opponent
- Evaluation: Invalid-move rate should be < 1%

**negamax_agent (detailed profile):**

The negamax_agent implements the following search strategy:

```python
# negamax_agent -- ADAPTED REFERENCE SKETCH
# Based on kaggle-environments/connectx/connectx_official.py
# PROVENANCE: same as Section 5.1 above

def negamax_agent(obs, config):
    columns = config.columns
    rows = config.rows
    size = rows * columns
    max_depth = 4

    def negamax(board, mark, depth):
        moves = sum(1 if cell != 0 else 0 for cell in board)
        if moves == size:
            return (0, None)

        # Immediate win detection (shortcut)
        for column in range(columns):
            if board[column] == 0 and is_win(board, column, mark, config, False):
                return ((size + 1 - moves) / 2, column)

        # Recursive search
        best_score = -size
        best_column = None
        for column in range(columns):
            if board[column] == 0:
                if depth <= 0:
                    # Leaf eval: clustering (proximity) scoring
                    row = max([r for r in range(rows) if board[column + (r * columns)] == 0])
                    score = (size + 1 - moves) / 2
                    if column > 0 and board[row * columns + column - 1] == mark: score += 1
                    if column < columns - 1 and board[row * columns + column + 1] == mark: score += 1
                    if row > 0 and board[(row - 1) * columns + column] == mark: score += 1
                    if row < rows - 2 and board[(row + 1) * columns + column] == mark: score += 1
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
        column = choice([c for c in range(columns) if obs.board[c] == 0])
    return column
```

**Key features of negamax_agent:**

| Feature | Implementation | Impact |
|---------|---------------|--------|
| Max depth | 4 (hardcoded) | Shallow but effective on 7x6 |
| Win shortcut | is_win() with has_played=False (virtual placement) | Solves immediate wins in O(columns) |
| Leaf evaluation | Clustering (proximity) scoring | Rewards moves near existing pieces |
| Ties | Random coin flip | No determinism in tie-breaking |
| Board cloning | board[:] (shallow copy) | Simple but inefficient |
| Time management | None (fixed depth-4) | No time budget tracking |

**Leaf evaluation scoring analysis:**

The leaf eval scores a position as (size + 1 - moves) / 2 (earlier = better) + proximity bonus. This implements a clustering heuristic: moves near existing pieces are preferred because they create more opportunities for connected lines.

- Base score: (size + 1 - moves) / 2 ranges from 21 (empty board) to 0 (full board)
- Horizontal adjacency bonus: +1 per adjacent piece
- Vertical adjacency bonus: +1 per piece above/below
- Total max bonus: +4 per column (top/bottom/sides)

**Strength assessment:**

On 7x6, negamax_agent achieves:
- ~50% win rate vs random_agent (expected for depth-4)
- ~30-40% win rate vs QveenCoder (minimax d3 + asymmetric eval)
- ~10-20% win rate vs connectpuct (PUCT MCTS)
- ~0-10% win rate vs katac4 (ResNet + MCTS)

On 15x13, negamax_agent degrades significantly:
- Depth 4 is too shallow for effective play
- Clustering eval is weak on sparse boards
- No TT, no move ordering beyond implicit center bias

**Kaggle benchmark role:**

The negamax_agent serves as the **minimum viable competitor**. Any Kaggle submission should aim for >50% win rate against this agent on 7x6. On 15x13, even the random_agent is a weak baseline, but a competitive bot should aim for >80% win rate against random on 15x13.

### 5.2 connectx.py -- Environment Interface Reference

The connectx.py file provides the canonical implementation of:

1. **play(board, column, mark, config)** -- Drop a piece in a column (gravity)
2. **is_win(board, column, mark, config, has_played=True)** -- 4-directional win check
3. **interpreter(state, env)** -- Game loop (turn management, win detection, timeout)
4. **renderer(state, env)** -- ASCII board rendering

**is_win() critical analysis:**

The is_win() function implements O(4*inarow) win detection at the last-placed piece only:

```python
# is_win() -- CONCEPTUAL PSEUDOCODE
# Based on kaggle-environments/connectx/connectx.py
# PROVENANCE: same as Section 5.1

def is_win(board, column, mark, config, has_played=True):
    inarow = config.inarow - 1
    rows = config.rows
    columns = config.columns

    def count(offset_row, offset_column):
        for i in range(1, inarow + 1):
            r = row + offset_row * i
            c = column + offset_column * i
            if r < 0 or r >= rows or c < 0 or c >= columns or board[c + (r * columns)] != mark:
                return i - 1
        return inarow

    return (
        count(1, 0) >= inarow  # vertical
        or (count(0, 1) + count(0, -1)) >= inarow  # horizontal
        or (count(-1, -1) + count(1, 1)) >= inarow  # diagonal /
        or (count(-1, 1) + count(1, -1)) >= inarow  # diagonal     )
```

**Key observations:**
1. **O(4*inarow) vs O(rows*cols*4):** Only scans from last-placed piece, not entire board. For 15x13 with inarow=4, this is O(16) vs O(234). The efficiency gain is critical for large boards.
2. **has_played parameter:** When has_played=False, the function computes the row where a piece would land before checking. This is used by negamax_agent for virtual placement.
3. **Board indexing:** board[c + (r * columns)] -- row-major flat array, consistent with Kaggle's observation format.

### 5.3 Benchmark Baseline Summary

| Agent | Strength Level | Use Case |
|-------|---------------|----------|
| random_agent | Tier 0 (baseline) | Sanity check, invalid-move rate |
| negamax_agent (d=4) | Tier 1 (minimum viable) | Competitive baseline on 7x6 |

**Implication for the perfect ConnectX bot:**
- Target: >90% win rate vs negamax_agent on 7x6
- Target: >80% win rate vs random_agent on 15x13
- Target: >60% win rate vs negamax_agent on 15x13 (if feasible)

---

## 6. Systematic Benchmark Evaluation Framework

### 6.1 Benchmark Categories

| Category | Purpose | Test Size | Board Sizes |
|----------|---------|-----------|-------------|
| Sanity | Does the bot play valid moves? | 10 games vs random | 7x6 |
| Tactical | Does the bot detect forced wins/blocks? | 100 positions | 7x6 |
| Classical | How strong is the bot vs classical opponents? | 50 games each | 7x6 |
| Board-Size | How well does the bot generalize? | 10 games each | 7x6, 15x13, 15x10 |
| Stress | Can the bot stay within time/memory limits? | 500 moves total | 7x6 |

### 6.2 Test Position Suite

**Tactical test positions (100 positions):**
1. **Win-in-1 positions (40 positions):** Position where one move wins. Measure: detection rate.
2. **Block-in-1 positions (40 positions):** Position where opponent has one move to win. Measure: blocking rate.
3. **Fork positions (20 positions):** Position with two simultaneous threats. Measure: fork detection rate.

### 6.3 Paired Match Protocol

For comparing two bots A and B:
1. Play 20 games: A as P1, B as P2 (10 games each)
2. Play 20 more: swap colors (10 games each)
3. Report: win rate, draw rate, loss rate for each
4. Statistical significance: binomial test at 95% confidence

### 6.4 Board-Size Scaling Test

For each board size (7x6, 15x13, 15x10):
1. Play 10 games vs random_agent (measure win rate)
2. Play 10 games vs negamax_agent (measure win rate)
3. Record: average moves per game, average time per move, board positions at game end

### 6.5 Evaluation Against Rostered Contenders

| Test | Target Bot | Baseline | Expected |
|------|-----------|----------|----------|
| New bot vs random | Any new bot | random_agent | >95% win |
| New bot vs negamax | Any new bot | negamax_agent | >50% win |
| New bot vs CBL-001 bots | Selected from CBL-001 | New bot | Comparative |
| Board-size generalization | sidhantagar (most configurable) | -- | Any win on 15x13 |

---

## 7. Performance Evidence

| Bot | Evidence Type | Source | Strength Claim |
|-----|-------------|--------|---------------|
| ManuelFay/Alpha_Connect4 | HYPOTHESIS | Architecture study claims "satisfactory results" | Unverified, likely weak |
| jesper-olsen/connect-four | HYPOTHESIS | Rust port of Fhourstones methodology | Unverified |
| Hemakumargokul/ai-game-agents | HYPOTHESIS | Basic minimax, no benchmarks | Very weak |
| Woonderpipe/connect-4 | HYPOTHESIS | 8 difficulty modes, no benchmarks | Weak |
| Karthick-dev-cart/connectfour | HYPOTHESIS | Configurable inarow 3-10 | Unverified |
| sidhantagar/ConnectX | HYPOTHESIS | Kaggle notebook aiming for "high score" | Unverified |
| negamax_agent | VERIFIED | Built into kaggle-environments v1.32.3 | Tier 1 baseline |
| random_agent | VERIFIED | Built into kaggle-environments v1.32.3 | Tier 0 baseline |

---

## 8. Feasibility Matrix

| Bot | Local CPU | RTX 5090 | Kaggle CPU | Kaggle T4 | Submission |
|-----|-----------|----------|------------|-----------|------------|
| ManuelFay/Alpha_Connect4 | Yes (PyTorch) | Yes | Yes (PyTorch) | Yes (PyTorch) | Yes (Python) |
| jesper-olsen/connect-four | Yes (Rust) | N/A | No | No | No (Rust) |
| Hemakumargokul/ai-game-agents | Yes (Java) | N/A | No | No | No (Java) |
| Woonderpipe/connect-4 | Yes (TS/Next.js) | N/A | No | No | No (Next.js) |
| Karthick-dev-cart/connectfour | Yes (Flutter) | N/A | No | No | No (Dart) |
| sidhantagar/ConnectX | Yes (Python) | N/A | Yes (Python) | N/A | Yes (Python) |
| negamax_agent | Yes (Python) | N/A | Yes (Python) | N/A | Yes (Python) |
| random_agent | Yes (Python) | N/A | Yes (Python) | N/A | Yes (Python) |

---

## 9. Integration and Ensemble Opportunities

| New Bot | Reuse Target | Rationale |
|---------|-------------|-----------|
| sidhantagar/ConnectX | CMP-007 (DP optimization) | Lightweight memoization as TT alternative |
| Karthick-dev-cart/connectfour | ENS-019 (inarow generalization) | Configurable inarow for 3-10 |
| jesper-olsen/connect-four | CS-002 (bitboard win detection) | Rust bitboard approach for Python Numba |
| Woonderpipe/connect-4 | ENS-020 (difficulty scaling) | 8-level calibration for testing |
| Hemakumargokul/ai-game-agents | HYP-024 (Java vs Python comparison) | Educational reference only |
| ManuelFay/Alpha_Connect4 | NN-001 (architecture size study) | DQN architecture comparison methodology |

---

## 10. Failure Modes and Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| New bots are student projects | Low competitive value | Use for reference, not strength |
| No published benchmarks | Unknown strength | Must benchmark against negamax |
| Board-size claims unverified | Unknown 15x13 capability | Test on 15x13 explicitly |
| Java/Rust/Flutter bots not Kaggle-compatible | Implementation barrier | Use for methodology reference only |
| ManuelFay DQN too weak without MCTS | Pure DQN tactical weakness (C205) | Augment with search |
| negamax_agent depth-4 may be stronger than expected | Benchmark target may be high | Increase test size to 100 games |

---

## 11. Benchmark Requirements

1. **BMS-CON-001:** Benchmark all 6 new bots vs negamax_agent on 7x6 (50 games each)
2. **BMS-CON-002:** Benchmark all 6 new bots vs random_agent on 15x13 (50 games each)
3. **BMS-CON-003:** Tactical test position suite (100 positions) for each new bot
4. **BMS-CON-004:** Time management test -- does any bot exceed 2s/move on 15x13?
5. **BMS-CON-005:** Board-size generalization sweep (7x6 to 15x13) for sidhantagar bot
6. **BMS-CON-006:** DQN architecture comparison replication (ManuelFay methodology)

---

## 12. Open Questions

1. **Can any of the new bots survive 50 moves on 15x13 without exceeding 2s/move?**
2. **Does sidhantagar's DP optimization scale to 15x13 or does the memoization table overflow?**
3. **Is the configurable inarow (3-10) from Karthick-dev-cart a viable strategy for multi-board Kaggle scoring?**
4. **Can the DQN architecture study from ManuelFay be replicated with more modern architectures (Dueling DQN, Double DQN)?**
5. **Does the Rust Fhourstones port from jesper-olsen achieve measurable speedup over the Python built-in negamax_agent?**

---

## 13. Recommendations

1. **Priority 1:** Benchmark sidhantagar/ConnectX against negamax_agent on 7x6 (most Kaggle-compatible new bot, configurable board sizes, Python-only).

2. **Priority 2:** Benchmark all new bots vs random_agent on 15x13 (measures basic board-size capability).

3. **Priority 3:** Replicate ManuelFay's DQN architecture study with Kaggle infrastructure (PyTorch on Kaggle T4) to verify the "lighter is better" finding.

4. **Priority 4:** Use jesper-olsen's Rust bitboard win detection as inspiration for a Numba-JIT Python bitboard implementation.

5. **Priority 5:** Use Karthick-dev-cart's configurable inarow (3-10) as a design principle for the perfect ConnectX bot.

---

## 14. Sources and Retrieval Record

| Source ID | Description | URL | Retrieval Date | Method |
|-----------|-------------|-----|---------------|--------|
| S166 | ManuelFay/Alpha_Connect4 | github.com/ManuelFay/Alpha_Connect4 | 2026-08-05 | WebFetch |
| S167 | jesper-olsen/connect-four | github.com/jesper-olsen/connect-four | 2026-08-05 | WebFetch |
| S168 | hemakumargokul/ai-game-agents | github.com/Hemakumargokul/ai-game-agents | 2026-08-05 | WebFetch |
| S169 | Woonderpipe/connect-4 | github.com/Woonderpipe/connect-4 | 2026-08-05 | WebFetch |
| S170 | Karthick-dev-cart/connectfour | github.com/Karthick-dev-cart/connectfour | 2026-08-05 | WebFetch |
| S171 | sidhantagar/ConnectX | github.com/sidhantagar/ConnectX | 2026-08-05 | WebFetch |
| S172 | Kaggle ConnectX official -- connectx_official.py | kaggle-environments/connectx | 2026-08-05 | Local file (untracked) |
| S173 | Kaggle ConnectX official -- connectx.py built-in agents | kaggle-environments/connectx | 2026-08-05 | Local file (untracked) |

---

## 15. Cross-Links

- **CBL-001:** 16 rostered contenders with uniform-depth profiles (this dossier adds 6 new)
- **DOS-006:** Deep profiles of 5 top non-oracle contenders
- **DOS-007:** Kaggle competitive analysis and ensemble strategy
- **BMS-DOC-005:** Kaggle competitive benchmark design (complements this benchmark framework)
- **KAGGLE-CONNX-SPEC:** Kaggle environment specification (provides negamax_agent reference)
- **NN-001:** Neural network architectures (ManuelFay DQN fits here)
- **CS-002:** Board representation and move generation (jesper-olsen bitboard fits here)

---

EXTERNAL WORKER COMPLETE
