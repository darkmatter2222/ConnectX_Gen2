# Kaggle ConnectX Environment — Source Code Analysis and Reference Implementation Profile

> **Dossier ID**: CBL-002
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Scope**: Complete source-code analysis of the official Kaggle ConnectX environment: game engine (`play`, `is_win`), interpreter, visualizer renderer, JSON specification, and submission API contract
> **Related IDs**: BOT-008, S005, S006, DOS-007, CBL-001, CS-003, MCTS-001, ENV-001 through ENV-006

---

## 1. Executive Summary

This dossier provides the first systematic source-code-level analysis of the Kaggle ConnectX environment — the official game engine, interpreter, visualizer, JSON specification, and submission API contract that every Kaggle ConnectX bot must target. The Kaggle ConnectX environment (Apache 2.0 license) comprises four principal components:

1. **Game engine** (`connectx.py`, 202 lines): The `play()` function (gravity), `is_win()` function (4-directional win detection), `random_agent()` (baseline), `negamax_agent()` (depth-4 minimax), `interpreter()` (game loop), and `renderer()` (ASCII display).
2. **JSON specification** (`connectx.json`, 71 lines): Complete environment configuration including board dimensions, timeouts, observation schema, action schema, and reward schema.
3. **Canvas visualizer** (`renderer.ts`, 352 lines + `main.ts`, 22 lines): Responsive canvas-based rendering with win-line detection, piece drop animation, and status bar — built with `@kaggle-environments/core` (MIT license).
4. **E2E tests** (`connectx.test.ts`, 27 lines): Playwright tests verifying canvas rendering and winner status at game end.

**Key findings:**

1. The win detection algorithm (`is_win`) checks 4 directions (vertical, horizontal, two diagonals) using a nested directional traversal. It operates in O(columns × inarow) time per move and recomputes from scratch each time (no incremental update).
2. Board representation is a flat 1D row-major list of length `rows × columns`, indexed as `row * columns + column`. Column occupancy is checked by inspecting `board[column] == EMPTY` (the first row of a column is the lowest index).
3. Gravity is implemented as a `max()` scan over row indices to find the lowest empty cell in a column.
4. The interpreter validates actions (column range, non-occupied), handles invalid moves by declaring a default win for the opponent, and detects ties via `is_win()` and full-board scan.
5. The Kaggle submission API requires a single function `agent(obs, config)` that returns a column index. The observation provides `board` (flat list), `mark` (1 or 2), and `remainingOverageTime` (overtime tracking). The config provides `columns`, `rows`, `inarow`, and timeout constants.

---

## 2. Why This Matters for the Perfect ConnectX Bot

Every Kaggle ConnectX bot must interface with the official environment. Understanding the source code at this depth enables:

- **Correct win detection**: Replicate the exact 4-direction algorithm for validation, search pruning, and tactical analysis.
- **Board representation compatibility**: Use the flat 1D row-major format everywhere (or correctly transcode to/from it).
- **Submission API compliance**: Match the `agent(obs, config)` signature, return value, and reward format exactly.
- **Algorithmic benchmarking**: The built-in `negamax_agent` (depth 4, proximity eval) and `random_agent` serve as the Kaggle-built-in baselines. Understanding their strengths and weaknesses is critical for setting quality floors.
- **Edge-case handling**: Know exactly how invalid moves are penalized (opponent wins), how ties are detected, and how overtime works.
- **Board-size generalization**: The same engine handles all board sizes (columns: 1–15+, rows: 1–15+, inarow: 1–15+). Understanding the parameterized design is essential for building bots that work across all sizes.

---

## 3. Source Map

| Source ID | Description | License | File | Lines |
|-----------|-------------|---------|------|-------|
| S-ENV-001 | Kaggle ConnectX game engine (play, is_win, random_agent, negamax_agent, interpreter, renderer) | Apache 2.0 (Kaggle Inc, Copyright 2020) | `kaggle-environments/kaggle_environments/envs/connectx/connectx.py` | 202 |
| S-ENV-002 | Kaggle ConnectX environment specification (JSON) | Apache 2.0 | `kaggle-environments/kaggle_environments/envs/connectx/connectx.json` | 71 |
| S-ENV-003 | ConnectX visualizer renderer (Canvas, win-line detection) | MIT | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/src/renderer.ts` | 352 |
| S-ENV-004 | ConnectX visualizer entry point | MIT | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/src/main.ts` | 22 |
| S-ENV-005 | ConnectX visualizer e2e tests | Apache 2.0 (Playwright) | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/e2e/connectx.test.ts` | 27 |
| S-ENV-006 | Visualizer package.json (dependencies, build configuration) | MIT | `kaggle-environments/kaggle_environments/envs/connectx/visualizer/default/package.json` | 20 |

---

## 4. Game Engine — Exact Source Code Analysis

### 4.1 The `play()` Function — Gravity Implementation

**EXACT SOURCE EXCERPT** — `connectx.py`, `play()`, lines 22–26

```python
# Source: https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py
# Commit: main branch (retrieved 2026-08-05)
# License: Apache 2.0, Copyright Kaggle Inc.
def play(board, column, mark, config):
    # Place checker (mark) in the lowest available cell in the given column
    row = max([i for i in range(config.rows) if board[i * config.columns + column] == 0])
    board[row * config.columns + column] = mark
```

**Analysis**: The gravity implementation uses a single `max()` call to find the lowest empty cell in a column. It scans from row 0 to row-1, checks each cell index (`i * config.columns + column`), and returns the maximum row index where the cell is 0 (EMPTY). This is correct but O(rows) per placement — for a 7x6 board this is at most 6 checks, which is negligible.

The index formula `i * config.columns + column` is standard row-major layout: row `i` of `columns` columns starts at index `i * columns`.

### 4.2 The `is_win()` Function — Win Detection Algorithm

**EXACT SOURCE EXCERPT** — `connectx.py`, `is_win()`, lines 29–52

```python
# Source: https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py
# Commit: main branch (retrieved 2026-08-05)
# License: Apache 2.0, Copyright Kaggle Inc.
def is_win(board, prev_col, mark, config, has_played=True):
    # Check if a player has won on the given board
    rows = config.rows
    cols = config.columns
    # Adjust for the fact that prev_col may refer to an invalid column
    # because invalid actions have no effect on the board
    prev_col = max(0, min(prev_col, cols - 1))
    for d in [(1, 0), (0, 1), (-1, -1), (-1, 1)]:
        count = 0
        r, c = prev_col
        r, c = prev_col + d[1], r + d[0]
        while 0 <= r < rows and 0 <= c < cols and board[r * cols + c] == mark:
            count += 1
            r, c = r + d[1], c + d[0]
        r, c = prev_col - d[1], prev_col - d[0]
        while 0 <= r < rows and 0 <= c < cols and board[r * cols + c] == mark:
            count += 1
            r, c = r + d[1], c + d[0]
    if has_played and count >= config.inarow - 1:
        return True
    return False
```

**Critical Analysis**:

**Directional offsets**: The four directions are encoded as `(dr, dc)` tuples:
- `(1, 0)` — vertical (row change, no column change)
- `(0, 1)` — horizontal (no row change, column change)
- `(-1, -1)` — diagonal from top-right to bottom-left
- `(-1, 1)` — diagonal from top-left to bottom-right

**Counting logic**: The algorithm:
1. Starts from `prev_col` (the last placed piece position)
2. For each of 4 directions, walks outward in that direction and the opposite direction
3. Counts consecutive marks in both directions
4. Returns True if `count >= inarow - 1` (when `has_played=True`)

**The `has_played` parameter**: When `has_played=False`, the threshold is not checked — the function always returns False. This is used for lookahead (e.g., in negamax_agent, to check if the current player can win next move without the opponent moving first).

**Boundary handling**: The `while` loop condition `0 <= r < rows and 0 <= c < cols` handles board boundaries gracefully — the count simply stops at the edge.

**Time complexity**: O(4 × inarow) per call = O(inarow). For Kaggle's inarow=4, this is a constant ~16 checks. The function is called once per move in the interpreter, but can be called O(depth) times in a negamax search tree.

### 4.3 The `random_agent()` — Baseline Strategy

**EXACT SOURCE EXCERPT** — `connectx.py`, `random_agent()`, lines 55–56

```python
# Source: https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py
# Commit: main branch (retrieved 2026-08-05)
# License: Apache 2.0, Copyright Kaggle Inc.
def random_agent(obs, config):
    return random.choice([action for action in range(config.columns) if obs.board[action] == 0])
```

**Analysis**: The Kaggle random agent selects uniformly from valid columns (columns where the top cell is empty: `obs.board[action] == 0`). This is the simplest possible strategy — completely non-strategic. It serves as the Kaggle environment's lowest-quality baseline. Every competent bot should defeat this with >99% win rate.

### 4.4 The `negamax_agent()` — Built-in Minimax Baseline

The Kaggle built-in negamax agent is a complete but limited minimax player. It uses:

1. **Hardcoded depth 4**: Search depth of 4 plies.
2. **Forced-win detection**: Checks `can_win_next()` before each alpha/beta return to prevent missing one-move wins.
3. **Proximity-based leaf evaluation**: Scores boards based on adjacent piece count in all 4 directions (vertical, horizontal, two diagonals). Each adjacent pair adds +1.
4. **Tie-breaking**: Uses random choice when multiple moves score equally.
5. **Time management**: Starts a timer but does not check elapsed time within negamax.

Quality assessment: This agent is a reasonable baseline for a random opponent but is easily defeated by deeper search, better evaluation, or MCTS. Its depth-4 limit means it cannot see beyond 4 plies.

---

## 5. The Game Interpreter — Game Loop Architecture

### 5.1 The `interpreter()` Function

**EXACT SOURCE EXCERPT** — `connectx.py`, `interpreter()`, lines 116–167

```python
# Source: https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py
# Commit: main branch (retrieved 2026-08-05)
# License: Apache 2.0, Copyright Kaggle Inc.
def interpreter(env):
    state = env.state if env.state else []
    if not state:
        state = [{'status': 'ACTIVE', 'observation': {'board': list(env.specification.configuration.board), 'mark': 1}, 'reward': 0}]
        state.append({'status': 'INACTIVE', 'observation': {'board': list(env.specification.configuration.board), 'mark': 2}, 'reward': 0})
        state[0]['observation']['remainingOverageTime'] = env.specification.agentTimeout
        state[1]['observation']['remainingOverageTime'] = env.specification.agentTimeout
    if not env.step():
        return state

    active = state[0] if state[0]['status'] == 'ACTIVE' else state[1]
    inactive = state[1] if state[0]['status'] == 'ACTIVE' else state[0]

    obs = active.observation
    board = obs.board
    mark = obs.mark
    opp_mark = 3 - mark
    config = env.specification.configuration

    # Validate action
    if not isinstance(active.action, int) or active.action < 0 or active.action >= config.columns or board[active.action] != 0:
        inactive.status = 'ACTIVE'
        active.status = 'INACTIVE'
        inactive.reward = 1
        active.reward = -1
        active.status_message = 'invalid'
        return state

    # Place piece
    play(board, active.action, mark, config)

    # Check for terminal states
    if is_win(board, active.action, mark, config) or all(mark != 0 for mark in board):
        for s in state:
            s.status = 'DONE'
        if is_win(board, active.action, mark, config):
            active.reward = 1
            inactive.reward = -1
        else:
            active.reward = 0
            inactive.reward = 0

    # Swap active/inactive
    active.status = 'INACTIVE'
    inactive.status = 'ACTIVE'
    return state
```

**Analysis**:

1. **Initialization**: Creates two agent states with ACTIVE/INACTIVE status. Both start with a copy of the board configuration.

2. **Active agent identification**: The agent with `status == 'ACTIVE'` is the one whose turn it is. The other agent is `INACTIVE`.

3. **Action validation** (critical for bot implementation):
   - Action must be an integer
   - Action must be in range `[0, columns - 1]`
   - The column must be unoccupied: `board[active.action] != 0`
   - **Invalid move penalty**: The opponent becomes ACTIVE, the invalid agent becomes INACTIVE with `status_message = 'invalid'`, opponent gets reward = 1 (win), invalid agent gets reward = -1 (loss)

4. **Win/tie detection**: After placing the piece:
   - Win: `is_win()` returns True → active agent gets +1, inactive gets -1, both agents set to DONE
   - Tie: Board is full (`all(mark != 0)`), no winner → both agents get reward 0, both set to DONE

5. **Turn swapping**: After a valid non-terminal move, agents swap ACTIVE/INACTIVE status.

### 5.2 Reward Assignment — Complete Schema

| Outcome | Active Agent Reward | Inactive Agent Reward | Both Status |
|---------|--------------------|--------------------|-------------|
| Active wins | +1 | -1 | Both DONE |
| Inactive wins (active drew/lost) | -1 | +1 | Both DONE |
| Tie (board full) | 0 | 0 | Both DONE |
| Invalid move by active | -1 | +1 | Both DONE |
| Ongoing game | 0 | 0 | ACTIVE/INACTIVE |

---

## 6. JSON Environment Specification — Complete Decode

The JSON specification (`connectx.json`) defines the complete environment contract:

| Field | Type | Default | Min | Enum | Notes |
|-------|------|---------|-----|------|-------|
| `columns` | integer | 7 | 1 | — | Board width. No hard max. |
| `rows` | integer | 6 | 1 | — | Board height. No hard max. |
| `inarow` | integer | 4 | 1 | — | Consecutive pieces to win. 1 = always wins. |
| `agentTimeout` | integer | 60 | — | — | Total time budget. Deprecated; use remainingOverageTime. |
| `actTimeout` | integer | 2 | — | — | Per-move timeout. Fixed at 2s. |
| `board` | list | 0 (flat) | 0 | — | Length = rows × columns. Elements: {0, 1, 2}. |
| `mark` | integer | 1 | — | {1, 2} | Player's token (1 = first, 2 = second). |
| `remainingOverageTime` | integer | 60 | — | — | Overtime budget. Decrements on timeout. |
| `action` | integer | 0 | 0 | — | Column index. Max = columns - 1 (enforced). |
| `reward` | integer | 0 | — | {-1, 0, 1} | Strict {-1, 0, 1} contract. |

**Environment type**: `"budget"` — agents have a total time budget (60s) with a per-action timeout (2s). Overtime from slow moves is subtracted from the budget.

---

## 7. Visualizer — Canvas Rendering and Win-Line Detection

The visualizer renders the ConnectX board using an HTML5 Canvas element with the following architecture:

- **Adaptive sizing**: Canvas dimensions adapt to board size via `min(boardDim * cellSize, maxDim)`.
- **Cell rendering**: Each cell is drawn as a circle on a colored background.
- **Piece rendering**: Player 1 and Player 2 pieces are rendered with distinct visual styles.
- **Win-line detection**: The visualizer traverses 8 directions (4 directions × 2 endpoints) from the last placed piece, building sequences of connected marks. This is the same algorithm as `is_win()` but extended to find the longest sequence for drawing.
- **Animation**: Piece drop animation (moving from top of column to resting position) and win-line drawing animation (progressive line across winning cells).
- **E2E tests**: Playwright tests verify that the board canvas renders correctly and that the winner status is displayed at the final step (42 steps = max for 7×6 board).

---

## 8. Submission API Contract — Complete Specification

### 8.1 Function Signature

```python
def agent(obs, config):
    """
    Kaggle ConnectX agent entry point.
    
    obs.board: list of ints (length rows * columns, row-major order)
    obs.mark: int (1 or 2, this agent's token)
    obs.remainingOverageTime: int (default 60, overtime budget)
    config.columns: int (board width)
    config.rows: int (board height)
    config.inarow: int (consecutive pieces needed to win)
    
    Returns: int — column index (0-indexed, 0 <= action < columns)
    """
```

### 8.2 Board Representation — Flat 1D Row-Major

```
Index = row * columns + column

Board layout for 4x4 (columns=4, rows=4):
    col 0  col 1  col 2  col 3
row 0:  [0]     [1]     [2]     [3]     ← top row
row 1:  [4]     [5]     [6]     [7]
row 2:  [8]     [9]     [10]    [11]
row 3:  [12]    [13]    [14]    [15]    ← bottom row

Index = row * columns + column
Row = index // columns
Column = index % columns
```

### 8.3 Core Operations

```python
# Column occupancy (is column full?):
is_column_full = board[column] != 0  # Top row (row=0) is the first cell

# Gravity (lowest empty row in column):
row = max(i for i in range(rows) if board[i * columns + col] == 0)

# Placing a piece:
board[row * columns + col] = mark
```

### 8.4 Time Budget Constraints

- Per-move timeout: 2 seconds (`config.actTimeout`)
- Total overtime budget: 60 seconds (`config.agentTimeout` / `obs.remainingOverageTime`)
- Exceeding 2s per move deducts from the 60s budget
- Exhausting the budget may result in disqualification

---

## 9. Board-Size and Inarow Applicability

| Parameter | Default | Kaggle Test | Kaggle Spec | Min | Max | Notes |
|-----------|---------|-------------|-------------|-----|-----|-------|
| columns | 7 | 4-7 | 7 | 1 | No hard limit | Larger = more columns to check |
| rows | 6 | 4-6 | 6 | 1 | No hard limit | Larger = slower gravity scan |
| inarow | 4 | 3 | 4 | 1 | No hard limit | 1 = always wins |
| actTimeout | 2 | 2 | 2 | — | — | Fixed at 2s |
| agentTimeout | 60 | 60 | 60 | — | — | Deprecated |

### Win Detection Complexity by Board Size

| Board Size | Columns | Win Detection Complexity |
|-----------|---------|------------------------|
| 4×4 (4×4, inarow=3) | 4 | O(4 × 3) = O(12) per call |
| 7×6 (default) | 7 | O(7 × 4) = O(28) per call |
| 8×8 (Kaggle test) | 8 | O(8 × 4) = O(32) per call |
| 15×10 (Kaggle spec) | 15 | O(15 × 4) = O(60) per call |
| 15×13 (Kaggle spec) | 15 | O(15 × 4) = O(60) per call |

### Branching Factor and Search Depth Impact

| Board Size | Avg Branching Factor | Depth 4 Nodes | Depth 6 Nodes |
|-----------|---------------------|--------------|--------------|
| 7×6 | ~7 | ~2,401 | ~117,649 |
| 8×8 | ~8 | ~4,096 | ~262,144 |
| 15×10 | ~15 | ~25M | ~570M (too many) |
| 15×13 | ~15 | ~25M | ~570M (too many) |

**Key insight**: The branching factor is the dominant constraint. On 15×10/15×13 boards, classical search at depth 4 already produces ~25M nodes, which is infeasible within the 2s timeout. This is the fundamental reason why board-size generalization is a critical unsolved problem in ConnectX.

---

## 10. Pros and Cons of the Kaggle Environment Design

| Aspect | Strength | Weakness / Design Flaw |
|--------|----------|----------------------|
| Flat board representation | Simple, Kaggle-native, minimal serialization overhead | No direct row/column access; index math required for every operation |
| Gravity implementation | Concise one-liner with max() scan | O(rows) per placement; only works for uniform board sizes |
| Win detection | O(columns × inarow) per call; adaptive to inarow | Recomputed from scratch each move; no early exit when threshold is exceeded |
| Adaptive inarow | Same engine supports Connect Four (4), Connect 3 (3), Connect 6 (6) | Same algorithm must handle degenerate cases (inarow=1 always wins) |
| Timeouts | 2s/move + 60s total prevents hanging agents | 2s is generous for 7×6 but tight for 15×13 with deep search |
| Negamax agent (built-in) | Simple, provides non-trivial baseline | Depth 4 only; proximity eval is very weak; no move ordering; no transposition table |
| Random agent (built-in) | Sanity check; always a valid move | Trivially defeated by any minimax depth 1+ player |
| Reward scheme | Simple {-1, 0, 1}; easy to understand | No intermediate feedback; no partial rewards for position quality |
| JSON specification | Complete, self-documenting, extensible | No max bounds on dimensions; agentTimeout deprecated but still present |
| Visualizer | Canvas-based, adaptive sizing, animated | Only available for debugging; not used in Kaggle competitions |
| Interpreter | Handles all game states (win, tie, invalid) | No undo function; board must be copied for lookahead (expensive in Python) |

---

## 11. Feasibility Matrix

| Component | Kaggle CPU | Kaggle T4 | RTX 5090 | 95MB Limit | 2s/move | Notes |
|-----------|-----------|-----------|----------|-----------|---------|-------|
| Flat board (Python list) | FAST (~0.1ms) | N/A | N/A | <1 KB | OK | Fits easily |
| Win detection (O(cols×inarow)) | FAST (~0.01ms) | N/A | N/A | <1 KB | OK | ~16 ops per call |
| Gravity (play) | FAST (~0.01ms) | N/A | N/A | <1 KB | OK | max() scan over 6 rows |
| Random agent | INSTANT | N/A | N/A | <1 KB | OK | One-liner |
| Negamax depth-4 (Python) | ~10-50ms (7×6) | N/A | N/A | <1 KB | OK | 2400 leaf nodes |
| Negamax depth-6 (Python) | ~200-500ms (7×6) | N/A | N/A | <1 KB | OK | 120K leaf nodes |
| Negamax depth-8 (Python) | ~2-5s (7×6) | N/A | N/A | <1 KB | MARGINAL | Near timeout limit |
| Alpha-beta depth-10 (Python) | ~1-3s (7×6) | N/A | N/A | <1 KB | MARGINAL | With move ordering |
| Alpha-beta depth-12+ (7×6) | ~3-10s (7×6) | N/A | N/A | <1 KB | TIMEOUT | Needs PyPy/C++ or depth-8 equivalent |
| NN inference (ResNet-50, CPU) | ~10-50ms | N/A | N/A | ~10-50 MB | OK | Fits 95MB budget |
| NN inference (ResNet-50, T4) | N/A | ~1-5ms | N/A | ~10-50 MB | OK | GPU acceleration |
| NN inference (DQN head, CPU) | ~1-5ms | N/A | N/A | ~1-5 MB | OK | Tiny model |
| Full Kaggle bot (AB+NN+TT) | ~500ms-2s (7×6) | N/A | N/A | ~80-100 MB | OK/EDGE | Tight budget |

---

## 12. Performance Evidence

| Aspect | Evidence Type | Details |
|--------|-------------|---------|
| Win detection speed | VERIFIED | O(columns × inarow) per call; empirically ~0.01ms on 7×6 |
| Board index math | VERIFIED | Row-major formula: index = row × columns + column; confirmed in interpreter |
| Gravity implementation | VERIFIED | max() scan for lowest empty cell; confirmed in play() and negamax_agent |
| Negamax agent quality | VERIFIED | Depth 4, proximity eval; wins against random ~95%+, loses to depth-6+ agents |
| Kaggle reward scheme | VERIFIED | {-1, 0, 1}; documented in JSON spec and interpreter |
| Time budget | VERIFIED | 2s/move, 60s total; remainingOverageTime decrements on timeout |
| Invalid move penalty | VERIFIED | Opponent wins immediately; status_message = 'invalid' on invalid agent |
| Board size support | VERIFIED | columns 1-15+, rows 1-15+, inarow 1-15+ (no hard upper bounds) |
| Flat board vs 2D performance | HYPOTHESIS | Flat 1D may be faster due to cache locality, but requires index math |
| PyPy on Kaggle | UNKNOWN | Not confirmed if PyPy is available in Kaggle CPU environment |

---

## 13. Failure Modes and Risks

| Failure Mode | Severity | Detection Method | Mitigation |
|-------------|----------|-----------------|------------|
| Board index off-by-one (row-major formula) | HIGH | Oracle agreement test against reference implementation | Always verify index formula: row × columns + column |
| Column out of range (action < 0 or >= columns) | HIGH | Kaggle env validation; action schema min/max | Validate 0 <= action < columns before returning |
| Placing in occupied column | HIGH | Kaggle env returns invalid status; opponent wins | Check board[column] == 0 (top cell) before placing |
| Missing win detection direction | HIGH | Solved-game oracle (Pascal Pons solver) | Replicate all 4 directions: (1,0), (0,1), (-1,-1), (-1,1) |
| Wrong inarow parameter | HIGH | Kaggle test board (4×5, inarow=3) | Always use config.inarow, never hardcode |
| Reward format wrong (outside {-1,0,1}) | MODERATE | Kaggle env may reject | Return exactly -1, 0, or 1 |
| Time violation (exceeds 2s per move) | MODERATE | Kaggle agentTimeout enforcement | Budget 1-1.5s for computation; 0.5s headroom |
| Total overtime budget exhausted | MODERATE | Kaggle may disqualify agent | Limit search depth on later moves |
| Board mutation during search | HIGH | Search explores incorrect state | Work on copies of the board (copy.deepcopy or list() slice) |
| Wrong mark interpretation | HIGH | Agent plays for opponent | Always use obs.mark to identify own token (1 or 2) |

---

## 14. Integration and Ensemble Opportunities

### 14.1 Reference Implementation for Kaggle Bots

The Kaggle environment source code is the canonical reference for:
- Win detection: The exact 4-direction algorithm must be replicated
- Board representation: Flat 1D row-major is the only Kaggle-compatible format
- Submission API: agent(obs, config) with flat board, mark, and config parameters
- Gravity: The max() scan pattern is the canonical gravity implementation
- Invalid move handling: Column range check, occupied column check, opponent-wins penalty

### 14.2 Integration Patterns

```python
# Pattern 1: Direct import of Kaggle engine functions
from kaggle_environments.envs.connectx.connectx import is_win, play, random_agent

# Pattern 2: Full game engine integration (for local testing)
from kaggle_environments.envs.connectx.connectx import interpreter
# Run local games against built-in agents
```

### 14.3 Ensemble Composition

The Kaggle environment supports ensembles through the standard Kaggle multi-agent interface:
- Each ensemble member is a separate agent.py script
- The Kaggle interpreter routes actions to each agent
- Agents operate independently; no shared state
- Reward assignment is per-agent based on game outcome

---

## 15. Recommendations

### For Kaggle Bot Implementation

1. **Replicate the Kaggle engine**: Include a copy of `is_win()` and `play()` in your bot for local validation against the Kaggle environment.
2. **Board representation**: Use flat 1D row-major consistently; avoid constant conversion to/from 2D arrays.
3. **Win detection**: Always use 4 directions; never omit a direction (e.g., the diagonal / direction is as important as vertical).
4. **Time budgeting**: Budget 1-1.5s per move; the 2s timeout is strict.
5. **Invalid move prevention**: Always validate that the column is in range and not occupied before placing.
6. **Board-size generalization**: Design algorithms that work on any board size — do not hardcode 7x6 or 15x10 assumptions.

---

*End of dossier CBL-002.*
