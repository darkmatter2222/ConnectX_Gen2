# Kaggle ConnectX — Package & API Deep Dive

> **Based on:** Live inspection of `kaggle-environments` v1.30.2
> Source: `C:\Users\ryans\AppData\Roaming\Python\Python313\site-packages\kaggle_environments\`

---

## 1. How to Install

```bash
pip install kaggle-environments
```

**Important:** There is **no standalone** `pip install connectx`. The game logic lives inside `kaggle-environments` at:
- `kaggle_environments/envs/connectx/connectx.py` — game rules (play, is_win, agents)
- `kaggle_environments/envs/connectx/connectx.json` — game specification
- `kaggle_environments/core.py` — Environment class (run, step, reset, render)

---

## 2. Game Specification (connectx.json)

| Field | Type | Default | Min | Description |
|-------|------|---------|-----|-------------|
| `columns` | int | 7 | 1 | Board width |
| `rows` | int | 6 | 1 | Board height |
| `inarow` | int | 4 | 1 | Consecutive pieces to win |
| `actTimeout` | number | 2 | 0 | Seconds per action |
| `agentTimeout` | number | 60 | 0 | Obsolete — use `remainingOverageTime` |
| `timeout` | int | 2 | 0 | Obsolete copy of actTimeout |
| `reward` | enum [-1,0,1] | 0 | — | -1=lost, 0=draw/ongoing, 1=won |

**Action space:** `int` column index, min 0, no maximum (bounded by columns at runtime).

**Observation fields:**
- `board` — flat list of rows×columns integers (0=empty, 1=player 1, 2=player 2)
- `mark` — 1 or 2 (your piece)
- `remainingOverageTime` — starts at 60, decrements over match

**Status enum:** `ACTIVE` | `INACTIVE`

---

## 3. Environment API (core.py)

### 3.1 Creating an Environment

```python
from kaggle_environments import make

env = make("connectx", configuration={"columns": 7, "rows": 6, "inarow": 4})
```

The `make()` function:
1. Looks up the environment name in the global `environments` registry
2. Loads the JSON specification
3. Validates configuration against spec
4. Calls the interpreter to initialize the board
5. Returns an `Environment` instance

### 3.2 Environment Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `run()` | `run(agents: list[Callable]) -> list[list[State]]` | Run to completion, returns all steps |
| `step()` | `step(actions: list) -> list[State]` | Execute one step with given actions |
| `reset()` | `reset(num_agents: int = None) -> list[State]` | Reinitialize board and agent states |
| `render()` | `render(mode="human") -> str or None` | Visualize board (ansi, html, ipython, json) |

### 3.3 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `env.configuration` | Struct | columns, rows, inarow, actTimeout, runTimeout, episodeSteps |
| `env.specification` | Struct | JSON spec (agents count, reward schema, etc.) |
| `env.steps` | list[list[State]] | All steps executed so far |
| `env.done` | bool | True when episode is finished |
| `env.state` | list[State] | Current agent states |

### 3.4 Configuration Details (from spec + runtime)

| Field | Default | Description |
|-------|---------|-------------|
| `configuration.columns` | 7 | Board width |
| `configuration.rows` | 6 | Board height |
| `configuration.inarow` | 4 | Win condition |
| `configuration.actTimeout` | 2.0 | Seconds per move |
| `configuration.runTimeout` | ~1200 | Total episode timeout |
| `configuration.episodeSteps` | rows×columns | Max steps before forced end |
| `configuration.agentTimeout` | 60 | Obsolete (keep for compat) |

---

## 4. Game Rules (connectx.py)

### 4.1 `play(board, column, mark, config)`

Places a piece using gravity:

```python
def play(board, column, mark, config):
    columns = config.columns
    rows = config.rows
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    board[column + (row * columns)] = mark
```

**Board layout:** Flat row-major array.
- Index = `row * columns + col`
- Row 0 = top (indices 0 to columns-1)
- Row rows-1 = bottom (last `columns` indices)

**Gravity:** Find the highest row index `r` where the cell is EMPTY, then place there.

**Valid moves:** `board[column] == EMPTY` — i.e., the top cell (row 0) of a column is empty.

### 4.2 `is_win(board, column, mark, config, has_played=True)`

Checks 4 directions from the placed piece:

```python
def is_win(board, column, mark, config, has_played=True):
    columns = config.columns
    rows = config.rows
    inarow = config.inarow - 1  # <-- threshold: need inarow-1 MORE pieces
    
    # Find which row the piece landed in
    row = (
        min([r for r in range(rows) if board[column + (r * columns)] == mark])  # has_played
        else max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])  # first move
    )
    
    def count(offset_row, offset_column):
        """Count consecutive pieces of `mark` in direction (offset_row, offset_column)."""
        for i in range(1, inarow + 1):
            r = row + offset_row * i
            c = column + offset_column * i
            if r < 0 or r >= rows or c < 0 or c >= columns or board[c + (r * columns)] != mark:
                return i - 1
        return inarow
    
    return (
        count(1, 0) >= inarow                    # vertical down
        or (count(0, 1) + count(0, -1)) >= inarow   # horizontal
        or (count(-1, -1) + count(1, 1)) >= inarow  # diagonal \
        or (count(-1, 1) + count(1, -1)) >= inarow  # diagonal /
    )
```

**Key insight:** `count()` sweeps in ONE direction from the placed piece, counting consecutive matching pieces. Multi-direction calls (horizontal, both diagonals) sum BOTH directions from the placed piece.

**Threshold:** `config.inarow - 1` (e.g., 3 for Connect 4). The count returns how many *additional* pieces beyond the current one are in that direction. So if `count(1,0)` returns 3 and we need 3 more, that's 4 total including the placed piece → WIN.

**Direction vectors:**
- `(1, 0)` → vertical down
- `(0, 1)` + `(0, -1)` → horizontal right + left
- `(-1, -1)` + `(1, 1)` → top-left diagonal + bottom-right
- `(-1, 1)` + `(1, -1)` → top-right diagonal + bottom-left

**`has_played` flag:**
- `True` (normal): `min()` finds the row where the mark was placed
- `False` (first move): `max()` finds the row where the piece would land

### 4.3 Built-in Agents

```python
random_agent(obs, config)   # Picks random valid column
negamax_agent(obs, config)  # Depth-4 negamax with heuristic scoring
```

### 4.4 Interpreter (game loop)

```python
def interpreter(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows
    
    # 1. Validate/initialize board
    board = state[0].observation.board
    if len(board) != (rows * columns):
        board = [0] * (rows * columns)
        state[0].observation.board = board
    
    # 2. If done, no-op
    if env.done:
        return state
    
    # 3. Isolate ACTIVE/INACTIVE agents
    active = state[0] if state[0].status == "ACTIVE" else state[1]
    inactive = state[0] if state[0].status == "INACTIVE" else state[1]
    
    # 4. If invalid status, mark DONE
    if active.status != "ACTIVE" or inactive.status != "INACTIVE":
        active.status = "DONE" if active.status == "ACTIVE" else active.status
        inactive.status = "DONE" if inactive.status == "INACTIVE" else inactive.status
        return state
    
    # 5. Execute active agent's action
    column = active.action
    
    # 6. Invalid move → active loses
    if column < 0 or column >= columns or board[column] != 0:
        active.status = f"Invalid column: {column}"
        inactive.status = "DONE"
        return state
    
    # 7. Place piece
    play(board, column, active.observation.mark, env.configuration)
    
    # 8. Check win
    if is_win(board, column, active.observation.mark, env.configuration):
        active.reward = 1
        inactive.reward = -1
        active.status = "DONE"
        inactive.status = "DONE"
        return state
    
    # 9. Check tie (board full)
    if all(mark != 0 for mark in board):
        active.status = "DONE"
        inactive.status = "DONE"
        return state
    
    # 10. Swap turns
    active.status = "INACTIVE"
    inactive.status = "ACTIVE"
    
    return state
```

---

## 5. Agent Interface (agent.py)

### 5.1 Required Signature

Your bot must define a function with this signature:

```python
def agent(obs, config):
    """
    Args:
        obs: Struct with attributes:
            obs.board       — list[int], flat row-major board (0=empty, 1=you, 2=opponent)
            obs.mark        — int, 1 or 2 (your piece)
            obs.step        — int, current step number
            obs.remainingOverageTime — int, overtime seconds remaining (starts at 60)
        
        config: Struct with attributes:
            config.columns    — int, board width
            config.rows       — int, board height
            config.inarow     — int, pieces needed to win
            config.episodeSteps — int, max steps
            config.actTimeout — float, seconds per move (2.0)
            config.runTimeout — float, total episode timeout
            config.agentTimeout — int, obsolete (60)
    
    Returns:
        int: Column index to drop a piece into (0-based)
    """
    return 3  # Example: drop in center column
```

### 5.2 Key Details

1. **Both `obs` and `config` use dot notation** (wrapped in `structify()` from utils.py)
2. **`config` is NOT on `obs`** — `obs.configuration` raises `AttributeError`
3. **`obs.board` is a flat list**, NOT nested
4. **Your piece = `obs.mark`** (1 or 2, determined randomly at game start)
5. **Board is mutable** — don't modify it; create copies if needed

### 5.3 Timeout Mechanism

```python
# agent.py line 220
if duration - self.configuration.actTimeout > observation.remainingOverageTime:
    action = DeadlineExceeded()
```

**How it works:**
- Each action call starts a timer (`perf_counter()`)
- If `duration - actTimeout > remainingOverageTime`, the agent is killed
- `actTimeout` = 2.0 seconds (per-move budget)
- `remainingOverageTime` starts at 60 and decrements
- Total budget per move = `actTimeout + remainingOverageTime`
- So you effectively have up to **62 seconds total across the entire match** for overage
- The normal per-move budget is **2 seconds**
- Overtime is a one-time 60-second reserve that can be used for burst spending

### 5.4 Error Handling

| Error Type | Agent Status | Reward |
|------------|-------------|--------|
| Invalid column (< 0 or >= columns or full) | `"Invalid column: X"` | -1 (loss) |
| Timeout | `"TIMEOUT"` | -1 (loss) |
| Python exception | `"ERROR"` | -1 (loss) |
| Invalid action schema | `"INVALID"` | -1 (loss) |

---

## 6. Running Games

### 6.1 Run Full Episode

```python
from kaggle_environments import make

env = make("connectx", configuration={"columns": 7, "rows": 6})

# Run two agents against each other
result = env.run([my_agent, opponent_agent])

# result is list[list[State]], one list per step
# Final board:
final_state = result[-1]
print(final_state[0].observation.board)
print(final_state[0].reward)       # 1 = win, -1 = loss, 0 = draw
print(final_state[1].reward)       # opponent's reward
print(final_state[0].status)        # "DONE" when finished
```

### 6.2 Run with Built-in Agents

```python
env = make("connectx", configuration={"columns": 7, "rows": 6})
result = env.run(["random", "negamax"])

# Or evaluate multiple episodes:
from kaggle_environments import evaluate
rewards = evaluate("connectx", agents=["random", "negamax"], configuration={"columns": 7, "rows": 6}, num_episodes=10)
# rewards = [[reward1, reward2], ...] per episode
```

### 6.3 Render Board

```python
# ANSI text board
print(env.render())

# HTML
html = env.render(mode="html")

# JSON state
json_str = env.render(mode="json")
```

The renderer renders bottom-to-top visually:
```
+---+---+---+---+---+---+---+
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+
... (rows go from top (0) to bottom (rows-1))
+---+---+---+---+---+---+---+
  0   1   2   3   4   5   6
```

### 6.4 Step-by-Step

```python
env = make("connectx", configuration={"columns": 7, "rows": 6})
env.reset()  # empty board

# Step manually
step1 = env.step([3, 3])  # Both pick column 3
step2 = env.step([4, 2])  # Next pair
# ...
```

---

## 7. Kaggle Submission Format

### 7.1 Notebook Format

Submit as a **Jupyter Notebook (`.ipynb`)** with these cells:

**Cell 1 — Install:**
```python
!pip install kaggle-environments
```

**Cell 2 — Agent function:**
```python
from kaggle_environments.envs.connectx.connectx import play, is_win

def agent(obs, config):
    # Your implementation
    return 3  # column index
```

**Optional — Testing cells:**
```python
from kaggle_environments import make

env = make("connectx", configuration={"columns": 7, "rows": 6})
result = env.run([agent, agent])  # self-play
print(env.render())
```

### 7.2 Rules

1. Agent **must** be named exactly `agent`
2. Must accept exactly `(obs, config)` — no more, no less
3. Must return an `int` column index
4. No network calls allowed (except via UrlAgent which Kaggle handles)
5. No file I/O beyond the notebook itself

### 7.3 Evaluation

Kaggle runs your agent against all other submissions on:
- **7×6** boards (standard)
- **15×13** boards (large)
- **15×10** boards (wide)

Each pair plays multiple episodes. Score = average of (+1=win, 0=draw, -1=loss) across all opponents and board sizes.

---

## 8. Practical Helper Code

### 8.1 Board Utilities

```python
# Convert flat index to (row, col)
def idx_to_rc(idx, columns):
    return divmod(idx, columns)  # (row, col)

# Convert (row, col) to flat index
def rc_to_idx(row, col, columns):
    return row * columns + col

# Check if column has space
def has_space(board, col, columns):
    return board[col] == 0  # top cell (row 0) empty

# Get landing row
def get_landing_row(board, col, rows, columns):
    for r in range(rows - 1, -1, -1):
        if board[rc_to_idx(r, col, columns)] == 0:
            return r
    return -1  # column full

# Copy board
def copy_board(board):
    return board[:]
```

### 8.2 Quick Testing Loop

```python
from kaggle_environments import make, evaluate

def my_agent(obs, config):
    # Implementation
    return 3

# Test self-play on default board
env = make("connectx")
result = env.run([my_agent, my_agent])
print("P1 reward:", result[-1][0].reward)
print("P2 reward:", result[-1][1].reward)
print(env.render())

# Test against built-in agents
for board_config in [
    {"columns": 7, "rows": 6},
    {"columns": 15, "rows": 13},
    {"columns": 15, "rows": 10},
]:
    env = make("connectx", configuration=board_config)
    result = env.run([my_agent, "negamax"])
    print(f"\nBoard {board_config['columns']}x{board_config['rows']}:")
    print(f"  P1: {result[-1][0].reward}, P2: {result[-1][1].reward}")
```

---

## 9. Summary — Agent Checklist

When building your bot, ensure:

- [ ] Function named `agent(obs, config)` returns `int`
- [ ] `obs.board` is a flat list (use `row * columns + col` for indexing)
- [ ] `obs.mark` tells you if you're 1 (first player) or 2
- [ ] Valid moves: `board[c] == 0` for any column `c`
- [ ] Win check: call `is_win(board, col, obs.mark, config)` after placing
- [ ] Time limit: ~2 seconds per call, 60 seconds total overage
- [ ] Board configs: 7×6, 15×13, 15×10
- [ ] Don't modify `obs.board` — make copies for search
- [ ] `config` is separate from `obs` — don't access `obs.configuration`