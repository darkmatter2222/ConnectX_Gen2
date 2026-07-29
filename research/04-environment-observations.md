# Connect X - Environment Observations & Notes

## Board Layout Discovery

The default board is 6 rows × 7 columns = 42 cells total.

### Flat Array Indexing
The `board` field in the observation is a flat list of integers. The indexing was discovered empirically:

```
index = row * columns + col
```

Where:
- `row` goes from 0 (top) to 5 (bottom)
- `col` goes from 0 (left) to 6 (right)

So index 35 = row 5, col 0 = bottom-left cell.
Index 41 = row 5, col 6 = bottom-right cell.

### Visualization
```python
def print_board(board, cols=7, rows=6):
    for r in range(rows - 1, -1, -1):
        row_vals = [board[r * cols + c] for c in range(cols)]
        symbols = [' ' if v == 0 else str(v) for v in row_vals]
        print(f"  | {' | '.join(symbols)} |")
```

### Gravity (not visible from API)
The API does NOT explicitly tell you which row a piece landed in. The bot only chooses a **column**. Gravity is implicit — pieces fall to the lowest available row in the chosen column. A column with all rows filled is an invalid move.

### Key Discovery: Both Bots Play Only Columns 0-1
In testing, random bots playing on a 6×7 board consistently played only in columns 0 and 1, creating draws. This may be because the default behavior of the `make('connectx')` environment uses a simplified board or the bots are playing differently than expected.

**TODO:** Verify the actual board configuration used by Kaggle. The built-in `connectx` environment from kaggle-environments may have a different configuration than the standard 6×7 Connect Four.

## Evaluation Results

When testing `smart_bot` vs `dumb_bot` with 50 episodes:
- 50 draws, 0 wins for either side
- This means both bots are equally matched (likely both playing poorly)

## OpenSpiel Integration

The kaggle-environments package includes OpenSpiel environments including `connect_four` and `connect_four_proxy`. This means:
- The game tree of Connect Four is already solved in OpenSpiel
- We can leverage OpenSpiel's perfect-play AI as a baseline
- `open_spiel_connect_four` is available in the environment

## Key Configuration Parameters

```python
configuration = {
    "columns": 7,
    "rows": 6,
    "inarow": 4,
    "episodeSteps": 1000,
    "actTimeout": 2,
    "runTimeout": 1200,
    "agentTimeout": 60,
    "timeout": 2
}
```

Note: For the actual Kaggle competition, the board and win conditions may differ. The Kaggle Connect X competition supports **multiple board sizes** and **different win conditions**. The evaluation may use any combination.

## Kaggle Connect X Specifics

The actual Kaggle competition (Connect X) is a **variant** of Connect Four where:
- Board size may vary (not fixed to 6×7)
- Win condition (inarow) may vary
- The Kaggle evaluation tests across multiple board configurations
- Submissions must work on ANY valid board size

## Agent Signature

```python
def agent(obs, config):
    """
    obs.board: list[int] - flat board array
    obs.mark: int - your player marker (1 or 2)
    obs.remainingOverageTime: int - overtime seconds remaining
    obs.step: int - current step number
    
    config.columns: int - board width
    config.rows: int - board height
    config.inarow: int - required in-a-row to win
    config.episodeSteps: int - max steps per game
    """
    return 0  # column index
```