# Training Data Generation for ConnectX Neural Networks

> **Generated**: 2026-07-30 (Iteration 2)
> **Purpose**: How to generate training data for ConnectX neural networks
> **Status**: Based on web research and known implementations

---

## Data Generation Methods

### 1. From Solved Game Database (Primary Method)

**Source**: Böck (2025) complete win-draw-loss lookup table for 7x6
**Method**:
1. For each position in the solved database with ≤8 pieces
2. Extract the optimal move (game-theoretic best)
3. Create (board_state, best_move) pair

**Dataset size**: Estimated 100K-500K unique positions (reachable from start)
**Accuracy**: 100% (optimal moves from solved game)

```python
def generate_from_solved_db(solved_db, max_pieces=8):
    training_data = []
    for position, (best_move, win_status, depth) in solved_db.items():
        if count_pieces(position.board) <= max_pieces:
            training_data.append((position, best_move))
    return training_data
```

### 2. From Alpha-Beta Search (Secondary Method)

**Method**: Run alpha-beta search, collect (board_state, best_move) pairs
**Dataset size**: Limited by search time (can generate 10K-50K per hour)
**Accuracy**: Dependent on search depth (depth-8 = ~90% accuracy)

```python
def generate_from_ab_search(board, config, depth=10, samples=50000):
    training_data = []
    for _ in range(samples):
        # Random starting position
        state = random_position(board, config)
        # Search to find best move
        result = alpha_beta_search(state, config, depth)
        training_data.append((state, result.best_move))
    return training_data
```

### 3. From Self-Play (Reinforcement Learning Data)

**Method**: Run games between two AI agents, collect (state, action) pairs
**Dataset size**: Limited by game count (10K-100K games per day)
**Accuracy**: Dependent on agent strength (self-play quality matters)

```python
def generate_selfplay_games(agent, num_games=10000):
    training_data = []
    for _ in range(num_games):
        game = simulate_game(agent, agent)
        for state, move, winner in game:
            training_data.append((state, move, winner))
    return training_data
```

### 4. From MCTS Simulation

**Method**: Run MCTS, use most-visited move as "teacher signal"
**Dataset size**: Proportional to simulation count
**Accuracy**: Improves with more simulations

```python
def generate_from_mcts(board, config, simulations=10000):
    training_data = []
    root = mcts_root(board, config, simulations)
    # Collect top-k most visited moves as teacher signal
    for child in root.children:
        if child.visits > 100:  # Only confident predictions
            training_data.append((board, child.move, child.visits / root.total_visits))
    return training_data
```

---

## Training Data Pipeline

### Recommended Pipeline

```
Phase 1: Generate 200K+ positions from solved DB
   ↓
Phase 2: Train SFT model (supervised fine-tuning)
   ↓
Phase 3: Self-play with SFT model to generate new data
   ↓
Phase 4: Train RL model (reinforcement learning)
   ↓
Phase 5: Generate more self-play data with improved model
   ↓
Phase 6: Fine-tune with combined data (SFT + self-play)
```

### Data Distribution

| Phase | Source | Size | Purpose |
|-------|--------|------|---------|
| Phase 1 | Solved DB | 200K | SFT training |
| Phase 3 | Self-play | 50K | RL fine-tuning |
| Phase 5 | Self-play (improved) | 100K | Further RL fine-tuning |

### Data Augmentation

To increase effective dataset size:
1. **Board rotations**: Reflect board horizontally (8 symmetric positions)
2. **Color swaps**: Swap player colors (2 variations)
3. **Total augmentation**: 8 × 2 = 16× more training data
4. **Effective size**: 200K → 3.2M training examples

---

## Training Data Characteristics

### Optimal Data Properties

| Property | Recommended | Notes |
|----------|-------------|-------|
| **Total size** | 200K-1M | Enough for effective training |
| **Board coverage** | All reachable 7x6 positions | Comprehensive coverage |
| **Piece count range** | 2-15 pieces | Most positions in this range |
| **Augmentation** | 16× (rotation + color) | Standard for board games |

### Data Imbalance Issues

**Problem**: More draw positions than wins or losses in some configurations.
**Solution**: Weight samples by game outcome (more emphasis on wins/losses).

### Position Quality Filter

```python
def filter_training_data(positions):
    """Filter out low-quality training positions."""
    filtered = []
    for pos in positions:
        if is_winning(pos, 1):
            filtered.append((pos, optimal_move, 1.0))  # Win signal
        elif is_losing(pos, 1):
            filtered.append((pos, optimal_move, 0.0))  # Loss signal
        else:
            filtered.append((pos, optimal_move, 0.5))  # Draw signal
    
    # Filter out terminal positions (already decided)
    return [d for d in filtered if not is_terminal(d[0])]
```

---

## Transfer Learning from Solved to Unsolved

### Strategy

1. **Train on solved 7x6 data** (200K+ positions, optimal moves)
2. **Fine-tune on 15x13 self-play** (limited data, but practical)
3. **Transfer learned features** (CNN layers) to larger board

### What Transfers Well

| Feature | 7x6 → 15x13 | Notes |
|---------|-------------|-------|
| CNN early layers | ✅ | Spatial pattern detection |
| Threat detection | ✅ | 3-in-a-row detection transfers |
| Fork detection | ⚠️ | Rare on 15x13, may need adaptation |
| Center control | ✅ | Center column advantage transfers |
| Endgame patterns | ⚠️ | Different for different board sizes |

### Training Schedule for Transfer

| Step | Data | Purpose | Expected Accuracy |
|------|------|---------|-------------------|
| 1 | Solved 7x6 (200K) | Train CNN from scratch | ~95% vs optimal |
| 2 | 15x13 self-play (10K) | Fine-tune FC layers | ~70% vs optimal |
| 3 | 15x13 self-play (50K) | Full fine-tune | ~80% vs optimal |

---

## Evaluation of Generated Data

### Accuracy Metrics

| Metric | Method |
|--------|--------|
| **Policy accuracy** | % of moves matching optimal move |
| **Value accuracy** | Correlation with true win probability |
| **Play strength** | Win rate against known opponents |

### Self-Consistency Check

```python
# Check if NN predictions are consistent with itself
def self_consistency(model, test_set):
    correct = 0
    for state, _ in test_set:
        prediction = model.predict(state)
        # Run MCTS and see if prediction agrees
        mcts_result = mcts_search(state, 1000)
        if prediction == mcts_result:
            correct += 1
    return correct / len(test_set)
```

---

## Open Questions

1. What is the minimum dataset size for effective training?
2. How much does augmentation actually help?
3. Can we generate data from partial solutions?
4. How to handle the "curriculum learning" problem (easy → hard)?
5. What's the optimal balance between SFT and self-play data?

---

## References

- marcpaulo15: 200K state-action pairs from heuristic
- BEPb/Kaggle_ConnectX: 1000 random game baseline → self-play
- AlphaZero: Self-play from scratch