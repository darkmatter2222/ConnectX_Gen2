# MCTS Research for ConnectX — Iteration 4

> **Generated**: 2026-07-31
> **Purpose**: Monte Carlo Tree Search algorithms for ConnectX
> **Status**: Based on web research and known implementations

---

## What is MCTS?

Monte Carlo Tree Search (MCTS) is a heuristic search algorithm that builds a search tree by simulating random plays from the current position. Unlike alpha-beta minimax (which evaluates positions with a heuristic function), MCTS uses statistical sampling to estimate the value of each position.

### The Four Phases of MCTS

1. **Selection**: Traverse the existing tree from root to a leaf node, using the UCT formula
2. **Expansion**: Add a new child node to the leaf
3. **Simulation (Play-out)**: Play random moves from the new position until terminal
4. **Backpropagation**: Update statistics along the path from new node to root

### The UCT Formula

```
UCT = (value / visits) + C * sqrt(ln(parent_visits) / visits)
```

- **value / visits**: Exploitation (favor moves with high win rate)
- **C * sqrt(ln(parent_visits) / visits)**: Exploration (favor moves with few visits)
- **C**: Exploration constant (typical values: 1.0-2.0)
- **C = √2 ≈ 1.414**: Default for balanced exploration/exploitation

### Key Parameters

| Parameter | Typical Range | Effect |
|-----------|--------------|--------|
| C (exploration) | 1.0 - 2.0 | Higher = more exploration |
| Simulations per move | 1000 - 100,000 | More = stronger play, slower |
| Time per move | 1-2 seconds | Budget constraint |
| Rollout policy | Random / Heuristic / NN | Quality of play-outs |

---

## MCTS Variants for Connect 4

### 1. Standard UCT (Kocsis & Szepesvári, 2006)

The original UCT algorithm:
```python
def uct(node, parent):
    return (node.value / node.visits) + C * sqrt(log(parent.visits) / node.visits)
```

- **Simple**: Easy to implement
- **Baseline**: Standard against which to compare variants
- **C = √2**: Good default

### 2. Progressive Delays (Gelly et al., 2006)

Adjusts exploration based on tree depth:
- More exploration in early search phases
- Less exploration as tree grows
- Improves convergence speed

### 3. RAVE (Rapid Action Value Estimation)

- Tracks per-action statistics across the entire tree
- Uses these statistics to guide selection earlier in tree traversal
- Particularly effective when tree is small

### 4. Neural MCTS (AlphaZero-style)

Combines MCTS with neural network:
- **Policy network P(s,a)**: Biases move selection toward promising moves
- **Value network V(s)**: Evaluates position without full rollout
- **Warm start**: Policy network initializes the root's children

```python
# AlphaZero-style selection
def select_move(state, policy_net, value_net, simulations=800):
    root = MCTSNode(state)
    policy = policy_net.predict(state)  # Policy prior
    
    for _ in range(simulations):
        node = root
        while node.isFullyExpanded():
            node = node.select_uct(policy)  # Use policy prior
        expansion = node.expand()
        value = value_net.predict(expansion.board)  # NN evaluation
        expansion.backpropagate(value)
    
    return root.best_child().move  # Most visited child
```

### 5. RAVE-MCTS

Combines RAVE with standard UCT:
- RAVE provides early guidance when tree is small
- UCT provides stable estimates when tree is large
- Weighted combination: `UCT + λ * RAVE`

### 6. Win-rate MCTS

Optimizes for win-rate rather than expected score:
- More appropriate for game playing
- Handles ties and draws properly

---

## MCTS vs Alpha-Beta for Connect 4

### Alpha-Beta Advantages
- **Deterministic**: Same result every time
- **Pruning**: Can eliminate entire branches
- **Heuristic evaluation**: Can assess non-terminal positions
- **Shallow board**: Near-optimal at depth 8-12 on 7x6
- **Time-bounded**: Guaranteed to return a move

### Alpha-Beta Disadvantages
- **Evaluation function quality**: Limited by heuristic accuracy
- **Branching factor**: ~7 branches at each node (one per column)
- **Large boards**: Search space explodes (15x13 = ~195 cells)
- **Python overhead**: Slow node evaluation in Python
- **Fixed depth**: Limited lookahead capability

### MCTS Advantages
- **No heuristic needed**: Learns value through simulation
- **Adaptable**: Focuses search on promising branches
- **Large boards**: Handles sparse search spaces well
- **Parallelizable**: Many independent simulations
- **Neural net integration**: Can use NN for move selection and evaluation

### MCTS Disadvantages
- **Non-deterministic**: Different simulations give different results
- **Slow convergence**: Needs many simulations for accuracy
- **Random rollouts**: Wastes computation on bad moves
- **No time guarantee**: May not find good move if under time pressure
- **Small boards**: Overkill for 7x6 where alpha-beta works well

### Comparison Summary

| Factor | Alpha-Beta | MCTS |
|--------|-----------|------|
| Small boards (7x6) | ✅ Excellent | ⚠️ Overkill |
| Large boards (15x13) | ❌ Too slow | ✅ Good |
| Heuristic quality needed | ✅ Critical | ❌ Not needed |
| Parallelization | ⚠️ Limited | ✅ Easy |
| Time guarantee | ✅ Yes | ⚠️ Best effort |
| Learning from data | ❌ No | ✅ Yes (with NN) |
| Deterministic | ✅ Yes | ❌ No |

---

## MCTS Implementation for ConnectX

### Basic Implementation

```python
class MCTSNode:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move  # Move that led to this state
        self.parent = parent
        self.children = {}  # move → MCTSNode
        self.wins = 0
        self.visits = 0
        self.untried_moves = get_valid_moves(board)
    
    def isFullyExpanded(self):
        return len(self.untried_moves) == 0
    
    def isTerminal(self):
        return is_win(self.board, 1) or is_win(self.board, 2) or is_draw(self.board)
    
    def uct(self, C=1.414):
        if self.visits == 0:
            return float('inf')  # Unvisited nodes are always preferred
        return (self.wins / self.visits) + C * sqrt(log(self.parent.visits) / self.visits)
    
    def best_child(self, explore=0.0):
        """Select child with highest win rate (or UCT if explore > 0)"""
        if explore == 0:
            return max(self.children.values(), key=lambda n: n.wins / max(n.visits, 1))
        return max(self.children.values(), key=lambda n: n.uct(explore))
    
    def expand(self):
        move = self.untried_moves.pop()
        new_board = make_move(self.board, move)
        child = MCTSNode(new_board, move=move, parent=self)
        self.children[move] = child
        return child
    
    def backpropagate(self, value):
        self.visits += 1
        self.wins += value  # 1 for win, 0 for loss/draw
        if self.parent:
            self.parent.backpropagate(1 - value)  # Opponent's perspective


def mcts_search(board, config, time_limit=2.0):
    """Run MCTS for time_limit seconds."""
    root = MCTSNode(board)
    end_time = time.time() + time_limit
    
    while time.time() < end_time:
        # Selection
        node = root
        while node.isFullyExpanded() and not node.isTerminal():
            node = node.select_uct()
        
        # Expansion
        if not node.isTerminal() and not node.isFullyExpanded():
            node = node.expand()
        
        # Simulation
        if not node.isTerminal():
            value = random_rollout(node.board, config)
        
        # Backpropagation
        node.backpropagate(value)
    
    # Return best move (most visited)
    best = root.best_child(explore=0.0)
    return best.move
```

### Optimized Implementation

```python
def optimized_mcts(board, config, time_limit=2.0, C=2.0):
    """Optimized MCTS with smart rollouts and move ordering."""
    root = MCTSNode(board)
    end_time = time.time() + time_limit
    
    while time.time() < end_time:
        # Selection — use UCT with C=2.0 for Connect 4
        node = root
        while node.isFullyExpanded() and not node.isTerminal():
            node = node.best_uct_child(C=C)
        
        # Expansion
        if not node.isTerminal() and not node.isFullyExpanded():
            node = node.expand()
        
        # Simulation — use heuristic rollout (not random)
        if not node.isTerminal():
            value = smart_rollout(node.board, config)  # Heuristic-based
        else:
            value = evaluate_terminal(node.board)
        
        # Backpropagation
        node.backpropagate(value)
    
    return root.best_move()


def smart_rollout(board, config):
    """Heuristic-based rollout (not random)."""
    board_copy = board.copy()
    player = 1
    while not is_win(board_copy, 1) and not is_win(board_copy, 2):
        valid = get_valid_moves(board_copy)
        # Prefer moves that create threats
        best_move = max(valid, key=lambda m: threat_score(board_copy, m))
        board_copy = make_move(board_copy, best_move)
        player = 3 - player  # Switch player
    return 1.0 if is_win(board_copy, 1) else 0.0
```

---

## MCTS with Neural Network (AlphaZero Style)

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                    MCTS Search                       │
│                                                      │
│  Selection: UCT with Policy Prior                    │
│    - Policy network biases move selection            │
│    - Value network replaces rollouts                 │
│                                                      │
│  ┌─────────────┐    ┌──────────────────┐            │
│  │ Policy Net   │───→│ UCT Selection    │            │
│  │ (moves)     │    │ (biased by P(s,a))│            │
│  └─────────────┘    └──────────────────┘            │
│                                                      │
│  ┌─────────────┐    ┌──────────────────┐            │
│  │ Value Net    │───→│ Leaf Evaluation  │            │
│  │ (win prob)  │    │ (no rollout!)     │            │
│  └─────────────┘    └──────────────────┘            │
│                                                      │
│  Backpropagation:                                    │
│    - Update statistics along path                    │
│    - No random simulation needed                     │
└──────────────────────────────────────────────────────┘
```

### Key Features

1. **Policy prior P(s,a)**: Neural network suggests promising moves for UCT selection
2. **Value estimate V(s)**: Neural network evaluates positions, replacing random rollouts
3. **Better move ordering**: NN focuses search on promising branches
4. **Faster convergence**: NN evaluation is more accurate than random rollouts
5. **Self-improvement**: NN is updated from MCTS search results

### Training Loop

```python
# AlphaZero training loop
def train_mcts_bot(env, policy_net, value_net, iterations=10000):
    for i in range(iterations):
        # Self-play with MCTS
        game = self_play_with_mcts(env, policy_net, value_net)
        
        # Collect training data
        states, mcts_probs, rewards = game.to_training_data()
        
        # Update networks
        policy_net.update(states, mcts_probs)
        value_net.update(states, rewards)
    
    return policy_net, value_net
```

### Performance

- **BEPb/Kaggle_ConnectX**: Uses this exact approach
- **Training**: 1,000 random-game baseline → self-play with MCTS
- **Infrastructure**: xparl cluster for parallel self-play
- **Framework**: PyTorch + PARL

---

## MCTS for Different Board Sizes

### 7×6 (Standard)
- **Simulations needed**: ~1,000-10,000 per move
- **Best approach**: Alpha-beta (simpler, faster, stronger)
- **MCTS role**: Supplement for opening book generation

### 10×7 (Medium)
- **Simulations needed**: ~10,000-50,000 per move
- **Best approach**: MCTS with neural net evaluation
- **Rationale**: Alpha-beta too slow, MCTS concentrates search

### 13×15 (Large)
- **Simulations needed**: ~50,000-200,000 per move
- **Best approach**: MCTS + neural net + GPU acceleration
- **Rationale**: Alpha-beta completely infeasible, MCTS is only viable search

### Key Insight

> MCTS scales better to larger boards than alpha-beta. On 15x13, alpha-beta achieves depth 2-3 at best, while MCTS with NN can achieve much better practical play.

---

## Tuning Parameters

### Exploration Constant C

| C Value | Behavior | Recommended For |
|---------|----------|-----------------|
| 0.5 | Aggressive exploitation | NN-guided MCTS (NN provides exploration signal) |
| 1.0 | Balanced | Standard MCTS with random rollouts |
| 1.414 (√2) | Balanced default | Universal default |
| 2.0 | Aggressive exploration | Early training, small boards |
| 3.0 | Maximum exploration | Very sparse boards (15x13) |

### Number of Simulations

| Board Size | Simulations | Time (Python) |
|-----------|-------------|---------------|
| 7×6 | 1,000-10,000 | 0.5-2s |
| 10×7 | 10,000-50,000 | 1-2s |
| 13×15 | 50,000-200,000 | Requires optimization |

### Rollout Policy

| Policy | Quality | Speed | Recommendation |
|--------|---------|-------|----------------|
| Random | Low | Fast | Baseline only |
| Heuristic | Medium | Medium | Good for standard MCTS |
| NN-guided | High | Fast | Best for AlphaZero-style |

---

## Open Questions

1. What is the optimal C value for ConnectX?
2. Can RAVE improve MCTS convergence speed?
3. How many simulations per move are needed for expert play?
4. Does neural-guided MCTS outperform NN-only evaluation?
5. Can we parallelize MCTS across CPU cores?
6. Is there a way to combine MCTS and alpha-beta (hybrid)?
7. What's the impact of rollout policy quality on MCTS strength?

---

## References

- Kocsis, S. & Szepesvári, C. (2006). "Bandit based Monte-Carlo Planning"
- Gelly, S. et al. (2006). "Modification and Analysis of Local Search for Go"
- Silver, D. et al. (2016). "Mastering Chess and Shogi by Self-Play" (AlphaZero)
- Silver, D. et al. (2017). "Mastering the Game of Go with Deep Neural Networks and Tree Search"
- BEPb/Kaggle_ConnectX: AlphaZero-style MCTS with self-play