# Evaluation Function Design for ConnectX

> **Generated**: 2026-07-30 (Iteration 2)
> **Purpose**: Optimal evaluation function features and weights for ConnectX
> **Status**: Based on web research, known implementations, and game theory

---

## Core Evaluation Features

### 1. Window Scoring (Primary Feature)

Count 4-in-a-row windows and score based on pieces present:

```
def evaluate_window(window, piece):
    count = window.count(piece)
    opp_count = window.count(3 - piece)  # opponent
    
    if count == 4:
        return 100  # Win
    elif count == 3 and opp_count == 0:
        return 5    # Threat (3-in-a-row, open)
    elif count == 2 and opp_count == 0:
        return 2    # Potential (2-in-a-row, open)
    else:
        return 0
```

### 2. Center Control

```
def center_control(board, col):
    center_idx = len(board) // 2
    dist = abs(col - center_idx)
    return max(0, 3 - dist)  # Closer to center = higher score
```

### 3. Threat Detection

```
def count_threats(board, piece, inarow):
    threats = 0
    for each 4-in-a-row window:
        if window.count(piece) == 3 and window.count(opponent) == 0:
            threats += 1
    return threats
```

**Weight**: Threats are critical — a position with 2 threats is often winning.

### 4. Fork Detection (Two Simultaneous Threats)

```
def count_forks(board, piece, inarow):
    """A fork = two or more winning threats simultaneously."""
    winning_moves = []
    for col in range(columns):
        if is_valid(board, col) and creates_win(board, col, piece):
            winning_moves.append(col)
    return len(winning_moves) >= 2
```

**Weight**: Fork = instant win (opponent can only block one).

### 5. Space Control (Territory)

```
def space_control(board, piece):
    """Score based on how many rows each player controls."""
    my_rows = sum(1 for r in range(rows) if board[row_has_piece(r, piece)])
    return my_rows - opponent_rows
```

### 6. Connectivity

```
def connectivity(board, piece):
    """Measure how connected pieces are."""
    score = 0
    for each pair of adjacent pieces:
        score += 1
    return score
```

---

## Comprehensive Evaluation Function

```python
def evaluate_board(board, config, piece):
    """Comprehensive evaluation function for ConnectX."""
    score = 0
    
    # 1. Window scoring (4× board)
    for axis in ['horizontal', 'vertical', 'diagonal1', 'diagonal2']:
        for window in sliding_windows(board, config.inarow, axis):
            score += score_window(window, piece)
    
    # 2. Center control
    score += center_control_score(board, config.columns)
    
    # 3. Threat detection
    score += 10 * count_threats(board, piece, config.inarow)
    score -= 10 * count_threats(board, 3-piece, config.inarow)
    
    # 4. Fork detection
    score += 100 * count_forks(board, piece, config.inarow)
    score -= 100 * count_forks(board, 3-piece, config.inarow)
    
    # 5. Space control
    score += space_control_score(board, piece)
    
    # 6. Connectivity
    score += connectivity_score(board, piece)
    
    # 7. Mobility (number of good moves)
    score += mobility_score(board, config)
    
    return score
```

---

## Feature Weights (Initial)

| Feature | Weight | Notes |
|---------|--------|-------|
| Win (4-in-a-row) | 100 | Instant win |
| Threat (3-in-a-row, open) | 5-10 | One move from winning |
| Potential (2-in-a-row, open) | 2 | Building towards threat |
| Center control | 3 | Per piece, per column distance |
| Fork | 100 | Two threats = instant win |
| Space control | 1 | Per row |
| Connectivity | 1 | Per connected pair |
| Mobility | 0.5 | Per good move available |

### Weight Tuning

**Initial weights are a starting point**. Optimal weights depend on:
1. Board size
2. inarow parameter
3. Search depth
4. Play phase (opening vs midgame vs endgame)

**Recommendation**: Use heuristic weights initially, then tune with self-play or gradient descent.

---

## Advanced Evaluation Techniques

### 1. Temporal Evaluation (Ply-Adjusted)

```
def ply_adjusted_score(score, depth):
    """Adjust score based on how fast we can win/lose."""
    if is_win(board, piece):
        return 10000 - depth  # Prefer faster wins
    elif is_losing(board):
        return -(10000 - depth)  # Prefer slower losses
    return score
```

### 2. Potential Evaluation

```
def potential(board, piece, inarow):
    """How many 4-in-a-row lines are we close to completing?"""
    count = 0
    for each line:
        my_pieces = line.count(piece)
        if my_pieces > 0 and line.count(opponent) == 0:
            count += my_pieces
    return count
```

### 3. Opposition Quality

```
def opposition_quality(board, piece, inarow):
    """How good are our blocking moves?"""
    opp_threats = count_threats(board, 3-piece, inarow)
    # Count how many of our moves can block them
    blocks = sum(1 for col in range(columns) 
                 if is_valid(board, col) and blocks_opp_threat(board, col))
    return blocks - opp_threats  # Positive = good defense
```

### 4. "Near-Miss" Evaluation

```
def near_miss(board, piece, inarow):
    """Score positions where we almost had a win but got blocked."""
    count = 0
    for each line of length inarow+1:
        if line.count(piece) == inarow and line.count(opponent) == 1:
            count += 1
    return count  # We were one piece away, now blocked
```

---

## Evaluation for Different Board Sizes

### 7×6 (Standard)

- **Window scoring**: Primary feature (4-in-a-row detection)
- **Threat detection**: Critical (3-in-a-row threats are common)
- **Center control**: Important (center columns have more influence)

### 15×13 (Large)

- **Window scoring**: Less effective (rarer to get 4-in-a-row)
- **Space control**: More important (territory matters more)
- **Connectivity**: More important (pieces are spread out)
- **Potential**: More important (long-term building)

### Key Insight

> The evaluation function must be **adaptive** — different features dominate on different board sizes.
> A unified function should weight features differently based on board size.

### Adaptive Weights

```python
def get_weights(board_size):
    if board_size == (7, 6):
        return {
            'window': 1.0,
            'threat': 1.0,
            'center': 1.0,
            'space': 0.5,
            'connectivity': 0.5,
            'potential': 0.3,
        }
    elif board_size == (15, 13):
        return {
            'window': 0.3,
            'threat': 0.5,
            'center': 0.3,
            'space': 1.5,
            'connectivity': 1.5,
            'potential': 1.0,
        }
```

---

## Open Questions

1. What are the optimal weights for each feature?
2. How to weight features adaptively based on game phase?
3. Does "potential" (number of near-wins) matter more than threat count?
4. Is mobility (number of good moves) a good evaluation feature?
5. How does the evaluation function change with inarow parameter?
6. Can we learn optimal weights from solved positions?

---

## References

- mra1991/connect-four-negamax: Board control, contiguous sequences, threats
- sidhantagar/ConnectX: Heuristic evaluation for variable boards
- BitBully/BitBurny: Threat detection, board control, move prioritization