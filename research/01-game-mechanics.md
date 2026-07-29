# Connect X Game Mechanics & Rules

## Competition Overview

**Kaggle URL:** https://www.kaggle.com/competitions/connectx

This is a Kaggle competition for building AI bots to play Connect X — a variant of Connect Four where the board size and win conditions are configurable.

## Core Game Rules

### Board Configuration (default)
- **Columns:** 7
- **Rows:** 6
- **Win condition:** 4 in a row (horizontal, vertical, or diagonal)
- **Total cells:** 42 (7 × 6)
- **Max episode steps:** 1000

### Play Rules
1. Players alternate turns (Player 1 / mark 1 goes first)
2. On each turn, a player picks a column (0-indexed: 0 through columns-1)
3. The piece falls to the lowest available row in that column (gravity)
4. If a column is full, that action is INVALID
5. The game ends when:
   - A player gets 4 (configurable `inarow`) in a row → that player WINS (reward +1, opponent -1)
   - The board is full with no winner → DRAW (both get 0)
   - A timeout occurs → timeout player LOSES

### Scoring
- **Win:** +1 for winner, -1 for loser
- **Draw:** 0 for both players

## Kaggle Environment API

### Environment Creation
```python
from kaggle_environments import make

# Default config (7x6 board, 4 in a row)
env = make('connectx')

# Custom board size and win condition
env = make('connectx', configuration={"columns": 7, "rows": 6, "inarow": 4})
```

### Bot Interface — Step Function
Each bot must implement a `step` function:

```python
def agent(obs, config):
    """
    Args:
        obs (dict):
            - board: list of ints (flat array, row-major order, size = rows * columns)
              0 = empty, 1 = player 1's mark, 2 = player 2's mark
            - mark: int (your player mark: 1 or 2)
            - step: int (current game step)
            - remainingOverageTime: int (seconds of overtime remaining, starts at 60)
        config (dict):
            - columns: int
            - rows: int
            - inarow: int (required in-a-row to win)
            - episodeSteps: int (max steps per episode)
            - actTimeout: float (per-action timeout)
            - runTimeout: float (total run timeout)
    Returns:
        int: column index (0 to columns-1)
    """
    # Your logic here
    return 0  # default: play column 0
```

### Board Layout
The board is a **flat list** in **row-major order**. For a 7-column board:
- Row 0 (top): indices 0-6
- Row 1: indices 7-13
- Row 2: indices 14-20
- Row 3: indices 21-27
- Row 4: indices 28-34
- Row 5 (bottom): indices 35-41

Row index = index // columns, Column index = index % columns

### Available Board Configurations
The competition supports various board sizes. The Kaggle evaluation uses the default 7×6 board with 4-in-a-row.

### Agent Timeout
- **agentTimeout:** 60 seconds (overtime)
- **actTimeout:** 2 seconds per action (during evaluation)
- Bots that exceed the timeout lose the game

### Evaluation System
- Episodes are run between submitted bots
- The evaluation system runs multiple episodes to reduce randomness
- Bot performance is ranked by win rate across many episodes

## Configuration Parameters
```
columns: 7          # Board width
rows: 6             # Board height
inarow: 4           # Required in-a-row to win
episodeSteps: 1000  # Max steps per game
actTimeout: 2       # Per-action timeout (seconds)
runTimeout: 1200    # Total episode timeout (seconds)
agentTimeout: 60    # OverTime limit (seconds)
timeout: 2          # General timeout
```

## Key Observations

1. **Board is flat row-major** — must convert to 2D for strategy (row = idx // cols, col = idx % cols)
2. **Action space is small** — only 7 possible columns, making search feasible
3. **Gravity mechanic** — can only play in columns that aren't full
4. **Deterministic game** — no randomness in gameplay, making perfect play possible
5. **Time limit** — 2 seconds per move during evaluation, 60 seconds overtime
6. **Configurable board** — the environment supports different board sizes and win conditions

## Sources
- Kaggle Connect X competition page: https://www.kaggle.com/competitions/connectx
- kaggle-environments Python package (built-in ConnectX implementation)