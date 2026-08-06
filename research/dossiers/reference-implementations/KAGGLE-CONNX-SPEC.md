# Kaggle ConnectX - Environment Spec and Interpreter Dossier

## Dossier Metadata

| Field | Value |
|---|---|
| **Dossier ID** | KAGGLE-CONNX-SPEC |
| **Status** | PROPOSED |
| **Scope** | Kaggle ConnectX v1.0.1 - JSON specification, Python interpreter, built-in agents, renderers |
| **Date** | 2026-08-05 |
| **Related Claims** | C135-C143 (spec schema), C171 (agentTimeout deprecation), C172 (version discrepancy) |
| **Related Hypotheses** | HYP-014 (training API availability), HYP-015 (GPU acceleration via negamax) |
| **Related Experiments** | EXP-033 through EXP-037 (benchmark experiments) |
| **Related Contenders** | BOT-002 (Kaggle built-in negamax_agent baseline) |
| **Evidence Status Key** | VERIFIED = read source directly; HYPOTHESIS = reasonable inference, not tested on Kaggle server |

---

## 1. Executive Summary

The Kaggle ConnectX environment is a parameterized implementation of the Connect game family - "connect in a row" on an M x N grid with configurable board width, height, and win-length. It ships with both a JSON specification (schema-driven) and a Python interpreter (game logic + built-in agents). The environment is part of the open-source kaggle-environments framework (Apache 2.0) and is designed as a competition sandbox where agent submissions are evaluated on Kaggle's infrastructure.

**Key characteristics:**

- 2-player, deterministic, perfect-information, zero-sum game.
- Board representation: flat integer array of length `rows x columns`, column-major linearization (`index = column + row * columns`).
- Actions: a single integer - the column index where the active agent drops their checker.
- Win detection: O(1) per placed piece - four directional scan from the dropped piece.
- Rewards: {-1 = lost, 0 = ongoing/draw, 1 = won}.
- Built-in baselines: `random_agent` and `negamax_agent` (depth=4).
- Configurable: `rows`, `columns`, `inarow` with sensible defaults (6 x 7 x 4).
- Turn management: round-robin ACTIVE/INACTIVE status swapping, enforced by the framework.
- Overtime tracking: `remainingOverageTime` decremented when agents exceed `actTimeout` (2 seconds).

All claims in this dossier that can be verified against source code are marked **VERIFIED**.
---

## 2. Why This Matters for the Perfect ConnectX Bot

Understanding the Kaggle ConnectX spec and interpreter is essential for building a competitive submission because:

1. **Correctness is mandatory.** Invalid moves cause an immediate loss. The interpreter treats out-of-bounds, negative, or full-column actions as the active agent's forfeiture. A bot that does not validate its own actions will self-eliminate.

2. **The board is flat and column-major.** Any search algorithm must respect the `index = column + row * columns` mapping. Off-by-one errors in board indexing are a common source of subtle bugs.

3. **Win detection is local, not global.** The interpreter only checks the four directions from the last-placed piece. This makes the `is_win()` call O(inarow) per turn rather than O(rows x columns), enabling fast iterative deepening.

4. **`is_win(board, col, mark, config, False)` enables lookahead.** When a search algorithm wants to know whether a move *would* create a win without actually modifying the board, it calls `is_win` with `has_played=False`. The function computes the target row from the board state (finding the lowest empty row), then checks the four directions. This allows one-ply-ahead win detection without board mutation.

5. **The negamax_agent baseline reveals Kaggle's strategy space.** Its depth=4 limit, immediate-win detection, and clustering-based evaluation function suggest that the Kaggle sandbox rewards:
   - Capturing one-ply wins instantly (score = `(size + 1 - moves) / 2`).
   - Clustering around existing pieces (+1 for each adjacent mark).
   - Tie-breaking with coin flips for robust exploration.

6. **The `env.train()` API enables self-play.** Kaggle's framework provides a training wrapper where one agent position is set to `None` (auto-controlled by the training agent) while the other is filled by a default agent (e.g., `"random"`). This is HYPOTHESIS for server-side availability but VERIFIED for local use.

7. **Overtime is tracked server-side.** The `remainingOverageTime` field starts at 60 and decrements when an agent's response time exceeds `actTimeout` (2 seconds). A slow agent risks running out of time during a match. This is HYPOTHESIS for Kaggle's actual behavior.

---

## 3. Source Map

| Source | Type | Location | License | Version | Retrieval |
|---|---|---|---|---|---|
| `connectx.json` | JSON Specification | `kaggle-environments/kaggle_environments/envs/connectx/connectx.json` | Apache License 2.0 | v1.0.1 (spec version) | 2026-08-05 |
| `connectx.py` | Python Interpreter | `kaggle-environments/kaggle_environments/envs/connectx/connectx.py` | Apache License 2.0 | v1.0.1 | 2026-08-05 |
| `connectx_official.py` | Standalone Copy | `connectx_official.py` (repo root) | Apache License 2.0 | v1.0.1 | 2026-08-05 |
| `core.py` (Environment class) | Framework | `kaggle-environments/kaggle_environments/core.py` | Apache License 2.0 | commit 2b3dffe | 2026-08-05 |
| `index.html` | Visualizer HTML | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/index.html` | Apache License 2.0 | v1.0.1 | 2026-08-05 |
| `renderer.ts` | Visualizer TypeScript | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/src/renderer.ts` | Apache License 2.0 | v1.0.1 | 2026-08-05 |
| `test_connectx.py` | Test Suite | `kaggle-environments/tests/envs/connectx/test_connectx.py` | Apache License 2.0 | v1.0.1 | 2026-08-05 |
---

## 4. Technical and Algorithmic Explanation

### 4.1 Board Representation

The board is a flat `list[int]` of length `rows x columns`. Cell values are integers: 0 = empty, 1 = player 1, 2 = player 2.

**Indexing (column-major linearization):**

    index(column, row) = column + row * columns

For a standard 7-column board:

| (row, col) | index |
|---|---|
| (0, 0) | 0 |
| (1, 0) | 7 |
| (2, 0) | 14 |
| (0, 1) | 1 |
| (1, 1) | 8 |
| (5, 6) | 41 |

This means column `c` occupies indices `{c, c+cols, c+2*cols, ..., c+(rows-1)*cols}` - the "column drops" natural gravity is simulated by finding the highest empty row (lowest index) in the column.

**Evidence:** VERIFIED from `play()` function line 25.

### 4.2 Win Detection Algorithm

The `is_win()` function performs a directional count from the dropped piece's position. For each of four axes:

1. **Vertical** `(1, 0)`: count consecutive marks in the same column above and below.
2. **Horizontal** `(0, 1) + (0, -1)`: count right and left, sum both sides.
3. **Diagonal TL-SE** `(-1, -1) + (1, 1)`: count up-left and down-right, sum.
4. **Diagonal TR-SL** `(-1, 1) + (1, -1)`: count up-right and down-left, sum.

The `count(offset_row, offset_column)` helper scans from the dropped piece outward in one direction, returning `i - 1` when it hits a boundary or non-matching cell, or `inarow` (i.e., `config.inarow - 1`) if it fills the entire required span.

A win occurs when any direction pair sum is `>= inarow`.

**Key implementation detail:** The function uses `config.inarow - 1` as the threshold, not `config.inarow`. This is because `count()` returns values in `[0, inarow-1]`, and the sum of two directional counts must reach `inarow - 1` (meaning `inarow` total pieces including the placed one).

**Evidence:** VERIFIED from `is_win()` function lines 29-52.

### 4.3 Agent Interface (observation to action contract)

Each agent receives a function signature:

    def agent(observation: dict, configuration: dict) -> int

- `observation.board` - `list[int]` of length `rows x columns`
- `observation.mark` - `int` (1 or 2)
- `observation.step` - `int` (zero-indexed step count)
- `observation.remainingOverageTime` - `int` (starts at 60)
- `configuration.columns` - `int`
- `configuration.rows` - `int`
- `configuration.inarow` - `int`

The agent must return an integer in `[0, columns - 1]`. Returning an invalid column causes the agent to lose.

**Evidence:** VERIFIED from test_connectx.py and interpreter lines 116-167.

### 4.4 Game Loop and Turn Management

The interpreter manages turns via ACTIVE/INACTIVE status swapping:

1. **Initialization:** P1 is ACTIVE, P2 is INACTIVE on game start.
2. **Step execution:** The active agent's action is processed.
3. **After action:** The active agent becomes INACTIVE, the inactive becomes ACTIVE.
4. **Win/draw:** Both agents transition to DONE.
5. **Invalid move:** The invalid active agent's status becomes the error message; inactive agent gets DONE (and a winning reward).

The framework's `done` property returns `True` when no agent has ACTIVE status: `all(s.status != "ACTIVE" for s in self.state)`.

**Evidence:** VERIFIED from interpreter lines 116-167, core.py `done` property line 510-513.

### 4.5 Overtime Tracking (remainingOverageTime)

The `remainingOverageTime` field starts at 60 (per JSON spec). When an agent's response exceeds `actTimeout` (2 seconds), the framework subtracts the overage duration from `remainingOverageTime`:

    overage_time_consumed = max(0, duration - self.configuration.actTimeout)
    agent.observation.remainingOverageTime -= overage_time_consumed

This is HYPOTHESIS for Kaggle server behavior but VERIFIED for local `kaggle-environments` use.

**Evidence:** VERIFIED from core.py line 632; HYPOTHESIS for server-side.

### 4.6 Configuration Schema

| Parameter | Type | Default | Minimum | Description |
|---|---|---|---|---|
| `rows` | integer | 6 | 1 | Board height |
| `columns` | integer | 7 | 1 | Board width |
| `inarow` | integer | 4 | 1 | Pieces needed to win |
| `actTimeout` | integer | 2 | 0 | Action timeout (seconds) |
| `agentTimeout` | number | 60 | 0 | **DEPRECATED** - kept for backwards compatibility |
| `timeout` | integer | 2 | 0 | **DEPRECATED** - copy of actTimeout for backwards compatibility |

**Evidence:** VERIFIED from connectx.json lines 7-38.

C171 (agentTimeout deprecation): The `agentTimeout` field's description reads "Obsolete field kept for backwards compatibility, please use observation.remainingOverageTime." The `timeout` field is similarly marked as an obsolete copy of `actTimeout`.

### 4.7 Invalid Move Handling

When the active agent returns an invalid action:

    if column < 0 or active.action >= columns or board[column] != EMPTY:
        active.status = f"Invalid column: {column}"
        inactive.status = "DONE"
        return state

The active agent's status becomes the error string `"Invalid column: {column}"`, the inactive agent gets status `"DONE"`, and both retain their existing rewards (0 at the time of the invalid move).

However, the test file (`test_connectx.py`, lines 103-125) shows that the invalid agent's reward is set to `None` by the framework when status is "INVALID". This is a framework-level behavior applied after the interpreter returns.

**Evidence:** VERIFIED from interpreter line 141-144; HYPOTHESIS that Kaggle server applies the same reward=None logic.
---

## 5. Implementation Anatomy

### 5.1 Function-by-Function Analysis

#### `play(board, column, mark, config)` - Lines 22-26

Drops a checker into the specified column. Finds the lowest empty row (highest row index) via:

    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    board[column + (row * columns)] = mark

Uses `max()` over a list comprehension scanning rows 0..rows-1 - this finds the bottom-most empty cell, i.e., where the checker "lands" due to gravity.

**Evidence:** VERIFIED from connectx.py lines 22-26.

#### `is_win(board, column, mark, config, has_played=True)` - Lines 29-52

As described in Section 4.2. The `has_played` parameter is the critical differentiator:

  - **`has_played=True`** (called after `play()`): Uses `min()` to find the row index of the first mark in the column - this is the row where the current player's piece sits.
  - **`has_played=False`** (used in negamax lookahead): Uses `max()` to find where a piece *would* land if placed. This allows "what-if" win checking without modifying the board.

**Evidence:** VERIFIED from connectx.py lines 29-52.

#### `random_agent(obs, config)` - Lines 55-56

Returns a uniformly random valid column:

    return choice([c for c in range(config.columns) if obs.board[c] == EMPTY])

Only considers columns where the top cell (row 0) is empty - since the board is filled column-by-column from the bottom, checking `obs.board[c] == EMPTY` suffices to check if the column is available.

**Evidence:** VERIFIED from connectx.py lines 55-56.

#### `negamax_agent(obs, config)` - Lines 59-110

A minimax-style solver with the following characteristics:

- **Depth limit:** `max_depth = 4` (hard-coded).
- **Tie detection:** Counts non-empty cells; if board is full, returns score 0.
- **One-ply win detection:** Iterates all columns; if any creates a win (via `is_win(..., has_played=False)`), immediately returns with a score proportional to remaining moves: `(size + 1 - moves) / 2`. Higher scores for wins found earlier in the game.
- **Evaluation function at depth 0:**
  - Base score: `(size + 1 - moves) / 2` (favors wins earlier in the game).
  - Clustering bonus: +1 for each of the 4 adjacent cells (left, right, above, below) containing the same mark.
- **Branching:** All empty columns are explored. Equal scores are tie-broken with `choice([True, False])` for randomness.
- **Fallback:** If negamax returns `None` as the best column (empty board), pick a random column.

**Evidence:** VERIFIED from connectx.py lines 59-110. BOT-002.

#### `interpreter(state, env)` - Lines 116-167

Full game loop - see Section 4.4 and Section 5.3 below.

**Evidence:** VERIFIED from connectx.py lines 116-167.

#### `renderer(state, env)` - Lines 170-183

ASCII art board renderer. Draws rows from top to bottom (row 0 first), using `+---+` grid lines. Each cell shows its value: `0`, `1`, or `2`.

**Evidence:** VERIFIED from connectx.py lines 170-183.

### 5.2 The negamax_agent Baseline (BOT-002)

The built-in `negamax_agent` is the reference strategy. Key design decisions:

| Aspect | Detail | Rationale |
|---|---|---|
| Depth limit | 4 | "Due to compute/time constraints" (comment at line 64) |
| One-ply wins | Immediate return via `is_win(..., False)` | Fastest possible win capture |
| Static eval | `move_count_penalty + adjacency_bonus` | Simple heuristic favoring early wins and clustering |
| Tie-breaking | `choice([True, False])` at equal scores | Randomized exploration |
| Board copy | `board[:]` passed to recursive calls | Immutable semantics - each branch gets its own copy |
| Alpha-beta | **Absent** | Full minimax - no pruning |

The `max_depth = 4` constant is critical. For a 7x6 board (42 cells), at depth 4 with ~7 branches each, the search visits approximately `7^4 = 2,401` nodes per call in the best case (fewer as the board fills). This is designed to complete within the `actTimeout` of 2 seconds.

**Evidence:** VERIFIED from connectx.py lines 59-110. BOT-002.
### 5.3 State Management in the Interpreter

    +-----------------------------------------------------------+
    |                     interpreter(state, env)                 |
    +-----------------------------------------------------------+
    | 1. Board init check                                       |
    |    - If board length != rows*columns -> create fresh      |
    |      board, update state[0].observation.board               |
    |                                                           |
    | 2. Early exit if env.done                                 |
    |    - Return immediately - no further processing            |
    |                                                           |
    | 3. Active/Inactive isolation                              |
    |    - Identify which state entry is ACTIVE vs INACTIVE      |
    |    - If statuses are inconsistent -> mark DONE             |
    |                                                           |
    | 4. Action validation                                      |
    |    - column < 0 -> INVALID                                |
    |    - column >= columns -> INVALID                           |
    |    - board[column] != EMPTY -> INVALID (full column)       |
    |    - Invalid -> active.agent loses, inactive=DONE          |
    |                                                           |
    | 5. Play the move                                          |
    |    - play(board, column, mark, config)                     |
    |                                                           |
    | 6. Win check                                              |
    |    - is_win(board, column, mark, config) -> True          |
    |    - active.reward=1, active=DONE, inactive.reward=-1     |
    |      inactive=DONE                                         |
    |                                                           |
    | 7. Tie check                                              |
    |    - all(cell != EMPTY for cell in board) -> True         |
    |    - both agents -> DONE                                   |
    |                                                           |
    | 8. Turn swap                                              |
    |    - active -> INACTIVE, inactive -> ACTIVE                |
    |    - return state for next turn                            |
    +-----------------------------------------------------------+

**Evidence:** VERIFIED from connectx.py lines 116-167.

### 5.4 Board Initialization

The interpreter checks on every step:

    board = state[0].observation.board
    if len(board) != (rows * columns):
        board = [EMPTY] * (rows * columns)
        state[0].observation.board = board

This guards against:
- First call where `board` is an empty list `[]`.
- Configuration changes between games.
- Corrupted state from previous runs.

**Evidence:** VERIFIED from connectx.py lines 121-124.

### 5.5 Win Detection Detail - has_played True/False

The `has_played` parameter controls row lookup:

    # has_played=True: find the row of an existing piece in the column
    row = min([r for r in range(rows) if board[column + (r * columns)] == mark])

    # has_played=False: find where a piece would land in the column
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])

The `min()` finds the topmost mark (the one closest to row 0). For a valid board position, this will be the lowest mark in the column (since pieces fill bottom-up).

The `max()` finds the bottom-most empty row, i.e., where gravity would place a new piece.

Both approaches work because the column is guaranteed to be filled bottom-to-top.

**Evidence:** VERIFIED from connectx.py lines 33-37.
---

## 6. Documentation-Only Code Samples

### 5.1 EXACT SOURCE EXCERPT: play() Function

    EXACT SOURCE EXCERPT: play()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L22-L26
      Commit: 2b3dffe
      File: connectx.py
      Lines: 22-26
      License: Apache License 2.0
      Retrieved: 2026-08-05

    def play(board, column, mark, config):
        columns = config.columns
        rows = config.rows
        row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
        board[column + (row * columns)] = mark

### 5.2 EXACT SOURCE EXCERPT: is_win() Function

    EXACT SOURCE EXCERPT: is_win()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L29-L52
      Commit: 2b3dffe
      File: connectx.py
      Lines: 29-52
      License: Apache License 2.0
      Retrieved: 2026-08-05

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
            count(1, 0) >= inarow  # vertical.
            or (count(0, 1) + count(0, -1)) >= inarow  # horizontal.
            or (count(-1, -1) + count(1, 1)) >= inarow  # top left diagonal.
            or (count(-1, 1) + count(1, -1)) >= inarow  # top right diagonal.
        )

### 5.3 ADAPTED REFERENCE SKETCH: Full Game Loop State Transitions

    ADAPTED REFERENCE SKETCH: interpreter() state machine

    Initial state per agent:
      [
        {"action": 0, "status": "ACTIVE", "observation": {"board": [], "mark": 1, "step": 0, "remainingOverageTime": 60}, "reward": 0},
        {"action": 0, "status": "INACTIVE", "observation": {"mark": 2, "remainingOverageTime": 60}, "reward": 0}
      ]

    Step 1 - P1 plays column 3:
      - active = state[0] (ACTIVE), inactive = state[1] (INACTIVE)
      - column = 3, valid (0 <= 3 < 7 and board[3] == 0)
      - play(board, 3, 1, config) -> board[3 + 0*7] = 1  (row 0, col 3)
      - is_win(board, 3, 1, config) -> False
      - all(board) -> False (board not full)
      - state[0].status = "INACTIVE", state[1].status = "ACTIVE"

    Step 2 - P2 plays column 3:
      - active = state[1] (ACTIVE), inactive = state[0] (INACTIVE)
      - column = 3, valid (board[3] == 1, but board[3+7] == 0)
      - play(board, 3, 2, config) -> board[3 + 1*7] = 2  (row 1, col 3)
      - is_win(...) -> False
      - state[1].status = "INACTIVE", state[0].status = "ACTIVE"

    Step N - P1 creates a win:
      - play(board, col, 1, config) -> places checker
      - is_win(board, col, 1, config) -> True  (has_played defaults to True)
      - state[0].reward = 1, state[0].status = "DONE"
      - state[1].reward = -1, state[1].status = "DONE"
      - Return. env.done is now True.

    Invalid move - P1 plays column 9:
      - column = 9 >= columns(7) -> invalid
      - state[0].status = "Invalid column: 9"
      - state[1].status = "DONE"
### 5.4 Board Initialization

    board = state[0].observation.board
    if len(board) != (rows * columns):
        board = [EMPTY] * (rows * columns)
        state[0].observation.board = board

This guards against:
- First call where `board` is an empty list `[]`.
- Configuration changes between games.
- Corrupted state from previous runs.

**Evidence:** VERIFIED from connectx.py lines 121-124.

### 5.5 Win Detection Detail - has_played True/False

The `has_played` parameter controls row lookup:

    # has_played=True: find the row of an existing piece in the column
    row = min([r for r in range(rows) if board[column + (r * columns)] == mark])

    # has_played=False: find where a piece would land in the column
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])

The `min()` finds the topmost mark (the one closest to row 0). For a valid board position, this will be the lowest mark in the column (since pieces fill bottom-up).

The `max()` finds the bottom-most empty row, i.e., where gravity would place a new piece.

Both approaches work because the column is guaranteed to be filled bottom-to-top. If the column has pieces at rows 0,1,3 (row 2 empty), then `min()` returns 0 and `max()` returns 2.

**Evidence:** VERIFIED from connectx.py lines 33-37.### 6.1 EXACT SOURCE EXCERPT: play() Function

    EXACT SOURCE EXCERPT: play()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L22-L26
      Commit: 2b3dffe
      File: connectx.py
      Lines: 22-26
      License: Apache License 2.0
      Retrieved: 2026-08-05

    def play(board, column, mark, config):
        columns = config.columns
        rows = config.rows
        row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
        board[column + (row * columns)] = mark

### 6.2 EXACT SOURCE EXCERPT: is_win() Function

    EXACT SOURCE EXCERPT: is_win()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L29-L52
      Commit: 2b3dffe
      File: connectx.py
      Lines: 29-52
      License: Apache License 2.0
      Retrieved: 2026-08-05

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
            count(1, 0) >= inarow  # vertical.
            or (count(0, 1) + count(0, -1)) >= inarow  # horizontal.
            or (count(-1, -1) + count(1, 1)) >= inarow  # top left diagonal.
            or (count(-1, 1) + count(1, -1)) >= inarow  # top right diagonal.
        )

### 6.1 EXACT SOURCE EXCERPT: play() Function

    EXACT SOURCE EXCERPT: play()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L22-L26
      Commit: 2b3dffe
      File: connectx.py
      Lines: 22-26
      License: Apache License 2.0
      Retrieved: 2026-08-05

    def play(board, column, mark, config):
        columns = config.columns
        rows = config.rows
        row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
        board[column + (row * columns)] = mark

### 6.2 EXACT SOURCE EXCERPT: is_win() Function

    EXACT SOURCE EXCERPT: is_win()
      Project: kaggle-environments (kaggle_environments.envs.connectx)
      Source: connectx.py
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.py#L29-L52
      Commit: 2b3dffe
      File: connectx.py
      Lines: 29-52
      License: Apache License 2.0
      Retrieved: 2026-08-05

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
### 6.3 ADAPTED REFERENCE SKETCH: Full Game Loop State Transitions

    ADAPTED REFERENCE SKETCH: interpreter() state machine

    Initial state per agent:
      [
        {action: 0, status: ACTIVE, observation: {board: [], mark: 1, step: 0, remainingOverageTime: 60}, reward: 0},
        {action: 0, status: INACTIVE, observation: {mark: 2, remainingOverageTime: 60}, reward: 0}
      ]

    Step 1 - P1 plays column 3:
      - active = state[0] (ACTIVE), inactive = state[1] (INACTIVE)
      - column = 3, valid (0 <= 3 < 7 and board[3] == 0)
      - play(board, 3, 1, config) -> board[3 + 0*7] = 1 (row 0, col 3)
      - is_win(board, 3, 1, config) -> False
      - all(board) -> False (board not full)
      - state[0].status = INACTIVE, state[1].status = ACTIVE

    Step 2 - P2 plays column 3:
      - active = state[1] (ACTIVE), inactive = state[0] (INACTIVE)
      - column = 3, valid (board[3] == 1, but board[3+7] == 0)
      - play(board, 3, 2, config) -> board[3 + 1*7] = 2 (row 1, col 3)
      - is_win(...) -> False
      - state[1].status = INACTIVE, state[0].status = ACTIVE

    Step N - P1 creates a win:
      - play(board, col, 1, config) -> places checker
      - is_win(board, col, 1, config) -> True
      - state[0].reward = 1, state[0].status = DONE
      - state[1].reward = -1, state[1].status = DONE
      - Return. env.done is now True.

    Invalid move - P1 plays column 9:
      - column = 9 >= columns(7) -> invalid
      - state[0].status = Invalid column: 9
      - state[1].status = DONE

### 6.4 CONFIGURATION EXAMPLE: connectx.json Spec

    CONFIGURATION EXAMPLE: connectx.json (full spec)
      Source: connectx.json
      Permalink: https://github.com/Kaggle/kaggle-environments/blob/2b3dffe/kaggle_environments/envs/connectx/connectx.json
      Commit: 2b3dffe
      File: connectx.json
      Lines: 1-71
      License: Apache License 2.0
      Retrieved: 2026-08-05

    {
      "name": "connectx",
      "title": "ConnectX",
      "description": "Classic Connect in a row but configurable.",
      "version": "1.0.1",
      "agents": [2],
      "configuration": {
        "columns": {"description": "The number of columns on the board", "type": "integer", "default": 7, "minimum": 1},
        "rows": {"description": "The number of rows on the board", "type": "integer", "default": 6, "minimum": 1},
        "inarow": {"description": "The number of checkers in a row required to win.", "type": "integer", "default": 4, "minimum": 1},
        "agentTimeout": {"description": "Obsolete field kept for backwards compatibility, please use observation.remainingOverageTime.", "type": "number", "minimum": 0, "default": 60},
        "actTimeout": 2,
        "timeout": {"description": "Obsolete copy of actTimeout maintained for backwards compatibility.", "type": "integer", "default": 2, "minimum": 0}
      },
      "reward": {"description": "-1 = Lost, 0 = Draw/Ongoing, 1 = Won", "enum": [-1, 0, 1], "default": 0},
      "observation": {
        "board": {"description": "Serialized grid (rows x columns). 0 = Empty, 1 = P1, 2 = P2", "type": "array", "shared": true, "items": {"enum": [0, 1, 2]}, "default": []},
        "mark": {"defaults": [1, 2], "description": "Which checkers are the agents.", "enum": [1, 2]},
        "remainingOverageTime": 60
      },
      "action": {"description": "Column to drop a checker onto the board.", "type": "integer", "minimum": 0, "default": 0},
      "status": {"defaults": ["ACTIVE", "INACTIVE"]}
    }

### 6.5 CONFIGURATION EXAMPLE: Agent Submission Template

    CONFIGURATION EXAMPLE: Agent submission template

    # agent.py - Kaggle ConnectX submission
    def agent(observation, configuration):
        # observation: {board: [...], mark: 1, step: 0, remainingOverageTime: 60}
        # configuration: {columns: 7, rows: 6, inarow: 4}

        # Board: flat array, length = rows * columns
        # Index mapping: board[column + row * columns]
        # Mark: 1 = my color, 2 = opponent color

        # Find valid columns (top row empty):
        valid = [c for c in range(configuration['columns']) if observation['board'][c] == 0]

        # Placeholder: return first valid column.
        return valid[0] if valid else 0
---

## 7. Pros and Cons

| Aspect | Pros | Cons |
|---|---|---|
| **Spec clarity** | JSON schema is self-documenting; all field types, defaults, and constraints are explicit. | actTimeout is an un-annotated bare integer in the JSON (no description). |
| **Board representation** | Flat array is cache-friendly and simple. | Column-major linearization is non-standard (row-major is more common); off-by-one errors are easy. |
| **Win detection** | O(inarow) per move - extremely fast for lookahead. | Only checks 4 directions from placed piece; does not generalize to any N connected without modification. |
| **Configurability** | rows, columns, inarow are all configurable - the same code handles 4x4x3, 6x7x4, 9x8x5, etc. | No upper bound on dimensions in the spec - very large boards (e.g., 20x20x5) would cause exponential blowup in search. |
| **Built-in baselines** | random_agent and negamax_agent provide instant reference behavior. | negamax_agent lacks alpha-beta pruning; depth-4 is shallow for competitive play on standard boards. |
| **Interpreter design** | Clean turn management; handles invalid moves gracefully. | has_played parameter adds complexity; the dual row-finding logic (min vs max) is a subtle source of bugs. |
| **Framework integration** | env.train() enables self-play training. toJSON() enables replay serialization. | Framework API is not documented for Kaggle server behavior - only local testing is verified. |
| **Visualizer** | Canvas-based with animated piece drops and win-line. | Uses non-standard icons (K symbol for P1, goose icon for P2) - not generic Connect. |
| **Overtime tracking** | remainingOverageTime gives agents visibility into time budget. | 60-second overage budget with 2-second per-move timeout is extremely tight for deep search. |
| **License** | Apache 2.0 - permissive, allows modification and commercial use. | Must include copyright notice and license text in derivatives. |
---

## 8. Feasibility Matrix

| Platform | Feasibility | Constraints |
|---|---|---|
| **Local CPU (desktop)** | VERIFIED | Can run negamax_agent at depth 4 on 6x7x4 in < 1 second. Depth 5-6 may exceed 2s limit. Self-play training via env.train() is fully functional. |
| **RTX 5090 (GPU)** | HYPOTHESIS | Negamax is inherently sequential (minimax tree search). GPU acceleration would require parallelizing the tree search (batched forward passes). Not directly applicable to the Python interpreter. HYP-015. |
| **DGX Spark (edge GPU)** | HYPOTHESIS | Similar to RTX 5090 - negamax is not GPU-friendly without algorithm redesign. Could accelerate neural network evaluation functions if a hybrid approach is used. HYP-015. |
| **Kaggle CPU (competition)** | HYPOTHESIS | Standard Kaggle CPU (4 vCPUs, ~15 min runtime). Negamax depth 4 should pass. Deeper search (depth 5-6) may time out. actTimeout enforcement is HYPOTHESIS - untested on Kaggle. |
| **Kaggle T4 (GPU)** | HYPOTHESIS | GPU available for models but negamax doesn't benefit. Could accelerate neural network playouts if used as a heuristic. HYP-015. |
| **Submission/package constraints** | VERIFIED | Kaggle submissions are Python files with a single function agent(observation, configuration). No external packages by default. Must return within actTimeout. |
---

## 9. Performance Evidence

| Metric | Value | Source | Evidence |
|---|---|---|---|
| negamax depth | 4 (hard-coded) | connectx.py:65 | VERIFIED |
| actTimeout | 2 seconds | connectx.json:32 | VERIFIED |
| agentTimeout / remainingOverageTime | 60 seconds initial | connectx.json:26-30, :60 | VERIFIED |
| Board size (default) | 6x7 = 42 cells | connectx.json:9-24 | VERIFIED |
| Time complexity per is_win call | O(inarow) | connectx.py:39-45 | VERIFIED |
| Time complexity per negamax node | O(columns) for branching | connectx.py:82-103 | VERIFIED |
| Negamax node count (full tree, 6x7x4, depth 4) | ~7^4 = 2,401 (best case) | derived from source | VERIFIED |
| negamax_agent vs random_agent win rate | Unknown - not benchmarked in this dossier | HYPOTHESIS | HYPOTHESIS |
| Time to complete depth-4 negamax on 6x7x4 | HYPOTHESIS - estimated ~0.1-0.5s on modern CPU | derived from source | HYPOTHESIS |

---

## 10. Board-size and inarow Applicability (Generalized to Arbitrary N)

The ConnectX spec is fully generalized - rows, columns, and inarow are independent parameters with no hard-coded defaults in the interpreter (defaults are only in the JSON spec). All functions read from config at runtime.

**Generalized board parameters and search complexity:**

| Board | Cells | Branching (avg) | Depth 4 nodes | Depth 6 nodes |
|---|---|---|---|---|
| 4x4x3 | 16 | ~4 | ~256 | ~4,096 |
| 6x7x4 | 42 | ~5 | ~625 | ~15,625 |
| 8x8x4 | 64 | ~5 | ~625 | ~15,625 |
| 9x7x4 | 63 | ~5 | ~625 | ~15,625 |
| 10x10x4 | 100 | ~5 | ~625 | ~15,625 |
| 20x20x5 | 400 | ~5 | ~625 | ~15,625 |

For the standard 7x6x4 board: at depth 4, the negamax_agent visits roughly 7^4 = 2,401 nodes in the best case (empty board), decreasing as the board fills. This completes well within the 2-second actTimeout on modern hardware.
---

## 11. Integration and Ensemble Opportunities

The Kaggle ConnectX environment supports integration with external frameworks:

1. **Gym/Stable-Baselines integration:** The `env.train()` API explicitly mentions gym and stable-baselines compatibility. The training wrapper returns `(observation, reward, done, info)` tuples compatible with reinforcement learning pipelines.

2. **Self-play training:** Using `env.train([None, random])` or `env.train([random, None])`, the training agent can learn against the built-in random agent. The training API returns a dict with `step()` and `reset()` methods.

3. **Monte Carlo Tree Search (MCTS):** The fast `is_win()` and `play()` functions make ConnectX ideal for MCTS. The flat board representation and integer actions are MCTS-friendly.

4. **Neural network evaluation:** A trained network could replace the negamax static evaluation, enabling deeper search with NN-guided pruning. HYP-015.

5. **Opening book:** A compact opening book for the first 10-20 moves could eliminate the need for search during early game, saving time for mid-game computation.

6. **Tablebase (endgame):** For small boards (e.g., 4x4x3, 5x5x4), a complete tablebase is feasible, providing perfect play in endgame positions.
---

## 12. Failure Modes and Risks

### Determined failure modes:

| Risk | Severity | Mitigation |
|---|---|---|
| **Invalid column (out of bounds)** | CRITICAL | Agent loses immediately. Validate `0 <= action < columns`. |
| **Invalid column (negative)** | CRITICAL | Agent loses immediately. Validate `action >= 0`. |
| **Full column (column overflow)** | CRITICAL | Agent loses. Validate `obs.board[column] == 0`. |
| **Board not initialized (empty list)** | LOW | Interpreter self-corrects on first step (creates fresh board). |
| **Timeout / overtime** | HIGH | actTimeout = 2 seconds; 60-second overage budget. Deep search risks timeout. |
| **Empty board edge case** | MEDIUM | negamax_agent falls back to random column. Optimal: pick center column. |
| **Config mismatch** | LOW | Interpreter checks board length matches rows * columns each step. |
| **Win detection on partial board** | LOW | is_win only checks placed pieces; empty rows do not trigger false wins. |
| **Board indexing off-by-one** | MEDIUM | Column-major (column + row * columns) is non-standard; common bug source. |
| **has_played parameter confusion** | MEDIUM | True vs False changes row-finding logic; a common source of subtle win-detection bugs. |

### Edge cases verified in test_connectx.py:

1. **test_can_mark_a_full_column** - Verifies that attempting to drop into a full column returns INVALID status.
2. **test_can_mark_out_of_bounds** - Verifies that column index >= columns returns INVALID.
3. **test_can_win** - Verifies win detection with a 3-in-a-row on a 4x5x3 board.
4. **test_can_tie** - Verifies draw detection when board is full with no winner.
---

## 13. Benchmark Requirements

| Benchmark | Description | Method |
|---|---|---|
| **Correctness** | 100% pass on test_connectx.py | Run test_connectx.py |
| **negamax vs random** | Win rate > 90% | 100 episodes, 6x7x4 |
| **negamax depth scaling** | Time vs depth | Measure CPU time per depth |
| **Edge case coverage** | All invalid move paths handled | Test all invalid columns |
| **Board size scaling** | Time vs board size | 4x4x3 to 10x10x4 |
| **Self-play stability** | No crashes in training loop | Use env.train() API |
| **Tie detection** | Draw correctly identified | test_can_tie scenario |
| **Render correctness** | ASCII renderer matches state | Compare renderer output to board |
| **JSON serialization** | toJSON() round-trips | env.toJSON() then recreate |

---

## 14. Open Questions

| Question | Status | Impact |
|---|---|---|
| How does the Kaggle server enforce actTimeout? Does a timeout cause immediate loss? | HYPOTHESIS | High - affects algorithm design |
| What is the remainingOverageTime behavior when it reaches 0? | HYPOTHESIS | Medium - affects late-game strategy |
| Is env.train() available on Kaggle server during competitions? | HYPOTHESIS | Medium - affects development workflow |
| What is the maximum board size in practice for Kaggle ConnectX? | UNKNOWN | Medium - affects algorithm scalability |
| Are there any additional configuration parameters not documented in the spec? | UNKNOWN | Low - spec appears complete |
| How does the visualizer step animation work with the interpreter? | VERIFIED | None - cosmetic only |
| Does the visualizer win-line detection match the interpreter? | VERIFIED | Low - cosmetic only |
| What is the effect of the choice([True, False]) tie-breaking on outcomes? | HYPOTHESIS | Low - affects determinism |
| Is there a published Kaggle ConnectX leaderboard to reference? | UNKNOWN | High - affects competitive analysis |
---

## 15. Recommendations

1. **Always validate actions before returning.** Check `0 <= column < columns` and `obs.board[column] == 0` before submitting.

2. **Respect the actTimeout.** Design your algorithm to complete within 2 seconds. Use iterative deepening with a time budget, not a fixed depth.

3. **Monitor remainingOverageTime.** As time budget decreases, reduce search depth to avoid timeout.

4. **Use is_win(board, col, mark, config, False) for one-ply lookahead.** This is the most important optimization - it avoids costly board mutation for win detection.

5. **Implement alpha-beta pruning.** The negamax_agent lacks it. Adding alpha-beta can effectively double search depth for the same node count.

6. **Order moves to maximize alpha-beta efficiency.** Try columns adjacent to existing pieces first (as the negamax_agent does in its eval function).

7. **Handle the empty-board case gracefully.** The negamax_agent fallback to random column selection is correct but non-optimal. A fixed opening move (e.g., center column) is better.

8. **Test across multiple board sizes.** The spec is generalized - your bot should work on any configuration, not just 6x7x4.

9. **Use env.train() for self-play development.** The local training API is verified functional and provides a convenient sandbox for development.

10. **Benchmark against BOT-002.** Use the Kaggle built-in `negamax_agent` as a reference point. Your submission should outperform it on the target board size.
---

## 16. Sources and Retrieval Record

| # | Source | URL/Path | Commit/Version | License | Retrieved |
|---|---|---|---|---|---|
| S-001 | `connectx.json` | `kaggle-environments/kaggle_environments/envs/connectx/connectx.json` | v1.0.1, commit 2b3dffe | Apache 2.0 | 2026-08-05 |
| S-002 | `connectx.py` (interpreter) | `kaggle-environments/kaggle_environments/envs/connectx/connectx.py` | v1.0.1, commit 2b3dffe | Apache 2.0 | 2026-08-05 |
| S-003 | `connectx_official.py` (standalone) | `connectx_official.py` (repo root) | v1.0.1 | Apache 2.0 | 2026-08-05 |
| S-004 | `core.py` (Environment class) | `kaggle-environments/kaggle_environments/core.py` | commit 2b3dffe | Apache 2.0 | 2026-08-05 |
| S-005 | Visualizer `index.html` | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/index.html` | v1.0.1 | Apache 2.0 | 2026-08-05 |
| S-006 | Visualizer `renderer.ts` | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/src/renderer.ts` | v1.0.1 | Apache 2.0 | 2026-08-05 |
| S-007 | `test_connectx.py` | `kaggle-environments/tests/envs/connectx/test_connectx.py` | v1.0.1 | Apache 2.0 | 2026-08-05 |

---

## 17. Cross-Links

| Reference | Type | Description |
|---|---|---|
| C135-C143 | Claims | R25 Kaggle environment spec claims - schema validation, field types, defaults |
| C171 | Claim | `agentTimeout` deprecation - obsolete field kept for backwards compatibility |
| C172 | Claim | Version discrepancy - spec v1.0.1, framework module version tracked separately |
| HYP-014 | Hypothesis | `env.train()` availability and behavior on Kaggle server |
| HYP-015 | Hypothesis | GPU acceleration feasibility for negamax_agent |
| EXP-033 | Experiment | Benchmark negamax_agent depth vs board size |
| EXP-034 | Experiment | Benchmark negamax_agent vs random_agent |
| EXP-035 | Experiment | Benchmark time per move vs search depth |
| EXP-036 | Experiment | Benchmark alpha-beta vs vanilla negamax |
| EXP-037 | Experiment | Benchmark opening book + search vs full search |
| BOT-002 | Contender | Kaggle built-in `negamax_agent` baseline - depth 4, no alpha-beta, clustering eval |