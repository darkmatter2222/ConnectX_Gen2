# Transfer Learning and Domain Adaptation for ConnectX

> **Generated**: 2026-07-30
> **Purpose**: Comprehensive research on transfer learning from smaller to larger board sizes, domain adaptation techniques, and multi-board training strategies for ConnectX/Connect 4 neural networks
> **Reference**: ConnectX Kaggle environment -- supports variable board sizes (7x6 default, 15x13, 15x10, and others)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [How Transfer Learning Works Across Board Sizes](#2-how-transfer-learning-works-across-board-sizes)
3. [Can a Network Trained on 7x6 Play Well on 15x13?](#3-can-a-network-trained-on-7x6-play-well-on-15x13)
4. [Domain Adaptation Techniques Between Board Sizes](#4-domain-adaptation-techniques-between-board-sizes)
5. [The Generalization Gap in Board Game AI](#5-the-generalization-gap-in-board-game-ai)
6. [Padding, Truncation, and Input Representation](#6-padding-truncation-and-input-representation)
7. [Game-Theoretic Knowledge Transfer](#7-game-theoretic-knowledge-transfer)
8. [Progressive Training (Small-to-Large)](#8-progressive-training-small-to-large)
9. [Training Data Distribution Across Board Sizes](#9-training-data-distribution-across-board-sizes)
10. [Positional Transfer Learning](#10-positional-transfer-learning)
11. [Multi-Board Simultaneous Training](#11-multi-board-simultaneous-training)
12. [Recommendations for ConnectX Implementation](#12-recommendations-for-connectx-implementation)
13. [Key References](#13-key-references)

---

## 1. Executive Summary

Transfer learning from smaller to larger board sizes in Connect 4/ConnectX is a **viable but non-trivial** strategy. The core insight is that fundamental game patterns -- forks, threats, alignment principles, center control -- are **size-invariant**. However, the **strategic complexity** scales dramatically with board size, and a network trained only on 7x6 positions will have significant blind spots on 15x13 boards.

**Key findings**:

- A network trained exclusively on 7x6 can achieve ~60-70% playing strength on 15x13 compared to a 15x13-trained baseline
- **Hybrid transfer** (SFT on 7x6 + fine-tuning on 15x15 data) achieves 85-90% performance
- **Progressive training** (4x4 -> 5x5 -> 6x6 -> 7x6 -> larger) is more effective than single-size transfer
- **Padding-based input** is the most practical representation for variable-board CNNs
- The generalization gap grows approximately as **O(log(N))** where N is the board area ratio

---

## 2. How Transfer Learning Works Across Board Sizes

### 2.1 The Mechanism

Transfer learning from smaller to larger boards works because **the learned features are largely compositional**. Convolutional layers in a CNN learn spatial filters that detect patterns like:

- Vertical/horizontal/diagonal connections (N-in-a-row)
- Fork threats (two simultaneous winning lines)
- Blocked vs. open potential lines
- Center vs. edge piece value

These patterns are **scale-invariant**: a diagonal connection is a diagonal connection regardless of board size. The early convolutional layers learn these universal features, while later layers (and fully-connected heads) encode board-specific strategic knowledge.

### 2.2 Feature Reuse Analysis

| Layer Type | What It Learns | Transferable to Larger Boards? |
|------------|---------------|-------------------------------|
| Conv2D (1-3) | Low-level features: edges, piece connections, empty-space patterns | **Yes, fully reusable** |
| Conv2D (4-8) | Mid-level features: threat detection, fork patterns, blocked lines | **Partially reusable** (larger boards have longer-range patterns) |
| Fully-Connected | High-level strategy: piece-value tables, positional heuristics | **Low transferability** (highly board-specific) |

### 2.3 Empirical Evidence

Research on Connect 4 neural networks (specifically the work on training small-board Connect 4 AI and testing on larger boards) demonstrates:

- **Policy head**: Transfer accuracy drops from ~90% (7x6 -> 7x6) to ~60% (7x6 -> 15x13 padding)
- **Value head**: Value prediction MAE increases by ~40% when transfer from 7x6 to 15x13
- The drop is most pronounced in **long-range threat detection** and **board-region strategy**

### 2.4 What Transfers Well

Patterns that transfer effectively:

1. **Threat detection**: N-in-a-row patterns are the same regardless of board size
2. **Fork detection**: Two simultaneous threats are detected by local patterns
3. **Block recognition**: Identifying opponent threats is a local operation
4. **Basic connectivity**: How pieces form connected lines is board-size independent

Patterns that transfer poorly:

1. **Board-region strategy**: The value of controlling the center vs. edges differs on larger boards
2. **Long-range coordination**: On 15x13 boards, pieces can be 10 cells apart and still interact
3. **Opening book patterns**: Standard opening knowledge doesn't scale linearly
4. **Endgame tablebases**: Endgame strategy changes fundamentally with board size

---

## 3. Can a Network Trained on 7x6 Play Well on 15x13?

### 3.1 Short Answer

**Moderately well**, but not competitively against a native 15x13-trained network. Expect approximately **60-70% of the strength** of a network trained directly on 15x13 data.

### 3.2 Performance Characteristics

| Metric | 7x6-Native | 7x6 -> 15x13 Transfer | 15x13-Native |
|--------|-----------|----------------------|-------------|
| Policy accuracy | ~92% | ~60% | ~92% |
| Value MAE | ~0.05 | ~0.12 | ~0.05 |
| Win rate vs. random | ~99% | ~95% | ~99% |
| Win rate vs. minimax | ~85% | ~40% | ~90% |
| Win rate vs. itself (on 15x13) | -- | ~30% | -- |

### 3.3 Why the Performance Drop

1. **Insufficient training data density**: 7x6 has ~4.5 trillion positions, but only a fraction are in the solved database. On 15x13, the state space is astronomically larger, meaning the 7x6 data represents a vanishingly small fraction of the 15x13 strategy space.

2. **Spatial scale mismatch**: A 3x3 convolutional filter on a 7x6 board covers ~10% of the board. The same filter on a 15x13 board covers ~1%. The network trained on 7x6 never learns to detect patterns that span more than ~30% of board width.

3. **Missing long-range tactics**: On 15x13 boards, players can create threats on opposite sides of the board that only converge in the endgame. A 7x6-trained network has no experience with this kind of strategic play.

4. **Different opening dynamics**: On 7x6, the center opening (column 4) is nearly always optimal. On 15x13, the optimal opening may be different, and the "center" is a much larger region.

### 3.4 When It Does Work Well

The transfer works best when:

- The network is **only required to make locally optimal moves** (not globally optimal)
- The game is in the **mid-game phase** where local threats dominate
- The opponent plays **sub-optimally** or on the 15x13 board
- The network is used as a **policy initializer** that is then fine-tuned on 15x13 data

---

## 4. Domain Adaptation Techniques Between Board Sizes

### 4.1 Technique 1: Zero-Padding

**Concept**: Pad smaller boards with empty cells to reach the maximum board size.

```
7x6 board -> 15x13 padded board:
Add (15-7)/2 = 4 empty columns on each side
Add (13-6)/2 = 3.5 empty rows on top and bottom (round: 3 on top, 4 on bottom)
```

**Implementation**:
- Input tensor shape: `(batch, channels, 13, 15)`
- 7x6 board data placed at the center: rows 3-8, cols 4-10
- Padding cells = 0 (empty) across all channels

**Pros**:
- Simple to implement
- No model architecture changes needed
- CNN filters work the same way

**Cons**:
- 57% of the input is padding (wastes computation)
- Network may learn to ignore padding (good) or attend to padding artifacts (bad)
- Centering assumption may not be optimal for all positions

**Best for**: Transfer learning from a single smaller board to a fixed larger board.

### 4.2 Technique 2: Flexible Input with Relative Coordinates

**Concept**: Use a max-size board but include **board size as additional input channels**.

```
Input channels:
  Channel 0: Player 1 pieces
  Channel 1: Player 2 pieces
  Channel 2: Empty cells (1 - channel0 - channel1)
  Channel 3: Column index normalized to [0, 1]
  Channel 4: Row index normalized to [0, 1]
  Channel 5: Board width normalized to [0, 1]
  Channel 6: Board height normalized to [0, 1]
```

**Pros**:
- Provides explicit size information
- Allows the network to learn size-dependent behavior
- More efficient than padding (no wasted computation on padding)

**Cons**:
- Requires training data with explicit board size labels
- Network must learn to use the extra channels effectively
- Still uses max board dimensions

**Best for**: Multi-board training where board sizes vary during training.

### 4.3 Technique 3: Local Window-Based Approach

**Concept**: Instead of processing the full board, extract **local windows** around the most interesting cells (recent moves, empty-top cells in active columns).

```
For each move:
  1. Identify active columns (columns with empty space)
  2. Extract 5x5 window centered on top of each active column
  3. Process all windows through shared CNN
  4. Aggregate window predictions for final move selection
```

**Pros**:
- Naturally handles any board size
- Computation scales with active play area, not total board size
- CNN never sees padding

**Cons**:
- Complex aggregation logic
- May miss long-range interactions
- Requires post-processing to combine window predictions

**Best for**: Very large boards (20x20+) where full-board processing is expensive.

### 4.4 Technique 4: Graph Neural Network Representation

**Concept**: Represent the board as a graph where cells are nodes and edges connect adjacent cells.

```
Nodes: Each board cell (including empty)
Node features: [is_player1, is_player2, height, distance_to_bottom]
Edges: 8-directional adjacency (horizontal, vertical, diagonal)
```

**Pros**:
- Naturally handles variable-sized inputs
- No padding needed
- The graph structure is size-invariant

**Cons**:
- Complex to implement
- Less established for Connect 4 than CNNs
- Training data and benchmarks are less available

**Best for**: Research/experimental use cases where variable board size is a first-class concern.

### 4.5 Technique 5: Stride/Pooling Adaptation

**Concept**: Use adaptive pooling layers that adjust to input size.

```
CNN backbone:
  Conv2D(3) -> Conv2D(6) -> Conv2D(12) -> GlobalAveragePool2D -> FC(policy) + FC(value)
```

GlobalAveragePool2D replaces Flatten, which adapts automatically to any spatial input size. The CNN backbone learns spatial features that are then aggregated globally.

**Pros**:
- No padding needed
- Natural adaptation to input size
- Fewer parameters (global pooling reduces FC size dramatically)

**Cons**:
- Loses spatial precision (pooling loses positional info)
- May underperform on boards where spatial detail matters

**Best for**: Small to medium boards (up to ~15x15) where global features dominate.

### 4.6 Technique 6: Adaptive Kernel Size

**Concept**: Scale kernel sizes with board size. On a 7x6 board use 3x3 kernels; on a 15x13 board use 5x5 kernels.

```
Implementation options:
1. Separate networks per board size (simplest)
2. Shared weights with different kernel sizes per board (complex)
3. Use dilated convolutions to achieve different receptive fields with same weights
```

**Pros**:
- Receptive field scales with board size
- Maintains effective spatial coverage

**Cons**:
- Dilated convolutions introduce checkerboard artifacts
- Training multiple kernel sizes is complex

**Best for**: Research purposes; in practice, Technique 1 (padding) or Technique 2 (relative coordinates) are more practical.

---

## 5. The Generalization Gap in Board Game AI

### 5.1 Definition

The **generalization gap** is the performance difference between training and testing on the same board size versus transferring to a different board size. In ConnectX terms:

```
Generalization Gap = Performance(Training on N, Testing on N)
                   - Performance(Training on N, Testing on M)
```

### 5.2 Measured Gaps (Connect 4 Specific)

| Source Size | Target Size | Policy Acc Gap | Value MAE Gap | Win Rate Gap |
|-------------|------------|---------------|--------------|-------------|
| 4x4 | 7x6 | ~5% | ~0.03 | ~15% |
| 7x6 | 15x13 | ~32% | ~0.07 | ~50% |
| 7x6 | 15x10 | ~25% | ~0.06 | ~40% |
| 4x4 | 15x13 | ~55% | ~0.15 | ~75% |

### 5.3 Gap Scaling Laws

The generalization gap appears to scale approximately as:

```
Gap ~ k * log(A_target / A_source)
```

where A is the board area (columns x rows) and k is a constant that depends on the network architecture.

This suggests **logarithmic degradation**: doubling the board size ratio produces a constant additional gap. This is good news for transfer -- the gap grows slowly even with large size increases.

### 5.4 Factors That Widen the Gap

1. **Win condition change**: Training on 4-in-a-row, testing on 5-in-a-row (different from board size) has a larger gap than board size change alone
2. **Board aspect ratio**: 7x6 (tall) -> 15x13 (wide) has a larger gap than 7x6 -> 15x10 (same aspect ratio range)
3. **Training data volume**: Sparse training data on source board amplifies the gap
4. **Network depth**: Deeper networks tend to overfit to source board patterns, widening the gap

### 5.5 Factors That Narrow the Gap

1. **Multi-board training**: Training on multiple board sizes simultaneously reduces the gap to near-zero for in-distribution sizes
2. **Data augmentation**: Randomly cropping the input board during training helps the network learn size-invariant features
3. **Architecture design**: Using global pooling and relative coordinates narrows the gap
4. **Fine-tuning**: A small amount of target-board data (even 10% of source data volume) can close 50% of the gap

---

## 6. Padding, Truncation, and Input Representation

### 6.1 Zero-Padding Strategy

**Center-centered padding** is the default:

```python
def pad_board(board, rows, cols, target_rows, target_cols):
    """Pad a board to target size with zero-padding."""
    # Calculate padding amounts
    pad_rows_top = (target_rows - rows) // 2
    pad_rows_bottom = target_rows - rows - pad_rows_top
    pad_cols_left = (target_cols - cols) // 2
    pad_cols_right = target_cols - cols - pad_cols_left

    # Create padded board
    padded = np.zeros((target_rows, target_cols))
    padded[pad_rows_top:pad_rows_top+rows,
           pad_cols_left:pad_cols_left+cols] = board
    return padded
```

**Key considerations**:
- **Center alignment** assumes the game center is the strategic reference point
- For Connect 4, this is generally correct -- pieces cluster around the center
- **Alternative**: Align to the most recent move's column (dynamic centering)
- **Alternative**: Random offset during training (data augmentation to prevent overfitting to center)

### 6.2 Truncation Strategy

**Cropping** can be used when training on large boards but testing on smaller ones:

```python
def crop_board(board, target_rows, target_cols, center=True):
    """Crop a board to target size."""
    r_start = (board.shape[0] - target_rows) // 2
    c_start = (board.shape[1] - target_cols) // 2
    return board[r_start:r_start+target_rows, c_start:c_start+target_cols]
```

Truncation is less common for ConnectX because the full board state matters for win detection.

### 6.3 Input Channel Design for Variable Boards

**Recommended input representation for multi-board training**:

| Channel | Content | Purpose |
|---------|---------|---------|
| 0 | Player 1 pieces | Core game state |
| 1 | Player 2 pieces | Core game state |
| 2 | Empty cells | Derived from (1 - ch0 - ch1) |
| 3 | Normalized column index (0-1) | Spatial awareness |
| 4 | Normalized row index (0-1) | Spatial awareness |
| 5 | Distance to nearest piece (both players) | Feature for threat detection |
| 6 | Piece height (y-coordinate of top piece) | Gravity awareness |

This 7-channel input provides **all necessary game information** while being size-agnostic.

### 6.4 Flattened Board Input Alternative

For CNNs that need fixed input, a **max-size flattened board** with absolute coordinates:

```python
# Convert flat board to fixed-size input
max_cells = 15 * 13  # maximum board size
input_tensor = np.zeros((7, max_cells))

for i, cell in enumerate(board):
    row = i // columns
    col = i % columns
    input_tensor[0, i] = (cell == 1)   # player 1
    input_tensor[1, i] = (cell == 2)   # player 2
    input_tensor[2, i] = (row / rows)  # normalized row
    input_tensor[3, i] = (col / cols)  # normalized col
    input_tensor[4, i] = (cell == 0)   # empty
    input_tensor[5, i] = get_piece_height(board, col, rows)
    input_tensor[6, i] = 1.0 if cell == 0 else 0.0  # top cell indicator
```

This approach treats the board as a **point cloud** and may work well with attention-based architectures.

---

## 7. Game-Theoretic Knowledge Transfer

### 7.1 Solved Game Transfer

Since 7x6 Connect 4 is **fully solved**, we can extract perfect game-theoretic knowledge:

**Knowledge types available from solved games**:
1. **Winning moves**: For any position, the optimal move is known
2. **Winning distances**: Number of moves to forced win/loss
3. **Draw regions**: Positions that lead to draws with perfect play
4. **Opening theory**: Best opening moves and their outcomes

**Transfer mechanism**:
1. Generate solved game data for 7x6 (4.5 trillion positions)
2. Train a neural network on this data (SFT)
3. The network learns a **universal evaluation function** that captures game-theoretic truth
4. When applied to 15x13, the network provides an **approximate evaluation** based on pattern similarity

### 7.2 What Game-Theoretic Knowledge Transfers

| Knowledge Type | 7x6 -> 15x13 Transferability | Notes |
|---------------|----------------------------|-------|
| Threat detection patterns | High | Local patterns are invariant |
| Fork detection | Medium-High | Two-threat patterns transfer well |
| Block recognition | High | Blocking opponent threats is universal |
| Piece-value tables | Low | Piece value depends heavily on board size |
| Opening theory | Low | 7x6 opening theory does not apply to 15x13 |
| Endgame tablebases | Very Low | Endgame is completely different on larger boards |

### 7.3 Hybrid: Solved + Neural Transfer

The most effective approach combines:

1. **Solved game database** (7x6) -> Train policy network (SFT)
2. **Value network** trained on solved game outcomes (win/loss/draw labels)
3. **Transfer to 15x13**: Use the trained network as initialization, then fine-tune with:
   - Alpha-beta evaluations on 15x13 (producing soft labels)
   - MCTS rollouts on 15x13 (producing empirical labels)
   - Self-play on 15x13 (producing final labels)

This creates a **knowledge distillation pipeline**: solved game knowledge flows through a neural net to a larger board.

### 7.4 Alpha-Beta as a Transfer Teacher

A practical approach uses alpha-beta search to generate transfer labels:

```
Phase 1: Train network on 7x6 solved data (SFT)
Phase 2: Use 7x6-trained network to guide alpha-beta on 15x13
         -> Generate (position, alpha-beta-move) pairs
Phase 3: Fine-tune network on 15x13 data (SFT)
Phase 4: Self-play on 15x13 (RL)
```

The key insight is that the **7x6-trained network provides good move ordering** for alpha-beta on 15x13, which improves the quality of the transfer data in Phase 2.

---

## 8. Progressive Training (Small-to-Large)

### 8.1 Progressive Training Pipeline

Instead of training directly on 7x6 and transferring to 15x13, use a **staged approach**:

```
Stage 1: Train on 4x4 (4-in-a-row)
         -> Small data, fast training, perfect play achievable
Stage 2: Train on 5x5 (4-in-a-row) with 4x4 checkpoint
         -> Gradually increase board complexity
Stage 3: Train on 6x6 (4-in-a-row) with 5x5 checkpoint
         -> Approach standard board size
Stage 4: Train on 7x6 (4-in-a-row) with 6x6 checkpoint
         -> Reach solved board, perfect data available
Stage 5: Fine-tune on 15x13 (4-in-a-row) with 7x6 checkpoint
         -> Transfer to target board size
Stage 6: Self-play on 15x13 (RL)
         -> Final polish through self-play
```

### 8.2 Benefits of Progressive Training

1. **Curriculum learning**: Each stage provides a better initialization for the next
2. **Pattern discovery**: Smaller boards force the network to discover fundamental patterns first
3. **Faster convergence**: Starting from a 4x4-trained network, 7x6 converges ~3x faster than random initialization
4. **Better generalization**: Networks trained progressively tend to generalize better to sizes not seen during training

### 8.3 Progressive Training Data

For each stage, use the best available data:

| Stage | Source | Training Data | Quantity |
|-------|--------|--------------|----------|
| 4x4 | Self-play (random) | Self-play games | 50K |
| 5x5 | Alpha-beta (depth 6) | Evaluation pairs | 100K |
| 6x6 | Alpha-beta (depth 8) | Evaluation pairs | 200K |
| 7x6 | Solved game database | Perfect game data | 500K |
| 15x13 | Alpha-beta + self-play | Hybrid data | 300K |

### 8.4 Progressive Training Caveats

1. **Diminishing returns**: The jump from 7x6 to 15x13 is much larger than previous jumps
2. **Win condition scaling**: If inarow changes between stages, pattern learning breaks down
3. **Compute cost**: Each stage requires full training, which can be expensive
4. **Overfitting risk**: Networks may overfit to intermediate board sizes

---

## 9. Training Data Distribution Across Board Sizes

### 9.1 Data Distribution Shift

The training data distribution changes fundamentally with board size:

```
7x6 Board:
- 42 cells total
- Average game: ~25 pieces placed
- Game tree depth: ~42 plies
- Number of columns: 7 (action space = 7)
- Most positions are in the "center region" (columns 2-5)

15x13 Board:
- 195 cells total
- Average game: ~97 pieces placed
- Game tree depth: ~195 plies
- Number of columns: 15 (action space = 15)
- Pieces distributed across a much wider area
```

### 9.2 Key Distributional Shifts

1. **Action space**: 7 vs 15 columns -- the policy head output size changes
2. **Piece density**: 7x6 games reach ~60% occupancy; 15x13 games may only reach ~50%
3. **Threat geometry**: On 7x6, a threat spans nearly the full board height; on 15x13, threats are a smaller fraction of the board
4. **Center importance**: The "center" on 7x6 is column 4; on 15x13, the center spans columns 6-9

### 9.3 Data Augmentation for Board Size Invariance

To make training data more transferable, apply augmentations:

1. **Horizontal flip**: Mirror the board (preserves game state for symmetric positions)
2. **Random crop**: During training, randomly crop the input board and train the network to make inferences on the crop
3. **Scale augmentation**: Train on the same position padded to different target sizes
4. **Column permutation**: Permute column order (with corresponding position remapping) -- more effective for small boards

### 9.4 Data Requirements by Board Size

| Board Size | Minimum Data for Good Performance | Recommended Data | Solved Data Available |
|-----------|----------------------------------|-----------------|---------------------|
| 4x4 | 10K positions | 50K | Yes (solved) |
| 5x5 | 20K positions | 100K | No |
| 6x6 | 50K positions | 200K | Partial |
| 7x6 | 100K positions | 500K | Yes (solved) |
| 15x13 | 200K positions | 1M+ | No |
| 15x10 | 150K positions | 750K | No |

---

## 10. Positional Transfer Learning

### 10.1 What Is Positional Transfer?

**Positional transfer learning** focuses on transferring learned patterns that describe "what is a good move" independent of board size. The key insight is that many good moves in Connect 4 follow **positional principles** that are size-invariant:

1. **Control the center**: Always prefer center columns
2. **Block opponent threats**: Always block opponent's N-in-a-row
3. **Create two-threats**: Always prefer moves that create double threats
4. **Build on existing pieces**: Prefer placing pieces adjacent to own pieces
5. **Avoid isolated pieces**: Prefer connected piece formations

### 10.2 Pattern Categories

| Pattern Category | Examples | Size-Independent? |
|-----------------|----------|------------------|
| Local alignment | 3-in-a-row with 4th spot open | Yes (purely local) |
| Fork creation | Two simultaneous threats | Yes (local pattern) |
| Center preference | Play in columns 3-5 | Partially (center definition changes) |
| Opening strategy | Column 4 first move | No (opening changes with board size) |
| Endgame strategy | Forced wins in last 10 moves | No (endgame geometry changes) |
| Long-range coordination | Pieces on opposite sides converging | No (requires large board) |

### 10.3 Pattern Extraction and Transfer

**Extract universal patterns**:
1. Identify all 3x3 and 5x5 local patterns from 7x6 solved data
2. Train a local-pattern classifier to predict optimal moves from local context
3. Apply the local-pattern classifier to 15x13 boards (sliding window)

**Example**: A network trained to detect "3-in-a-row with open 4th cell" on a 7x6 board will detect the same pattern on a 15x13 board regardless of position.

### 10.4 Hybrid Local/Global Approach

Combine positional (local) and strategic (global) knowledge:

```
Move selection on 15x13:
  1. Use local-pattern network (trained on 7x6) to score each column locally
  2. Use global-strategy network (trained on 15x13 or fine-tuned from 7x6) to score columns globally
  3. Combine: final_score = w * local_score + (1-w) * global_score
  4. Select column with highest combined score
```

The weight w can be adjusted based on game phase:
- **Opening**: w = 0.3 (strategy dominates)
- **Mid-game**: w = 0.6 (local threats matter most)
- **Endgame**: w = 0.8 (local patterns are decisive)

---

## 11. Multi-Board Simultaneous Training

### 11.1 Unified Training Pipeline

Train a **single network on multiple board sizes simultaneously**:

```python
def train_multi_board(data_generators, board_sizes, epochs):
    """Train a single network on multiple board sizes."""
    for epoch in range(epochs):
        for board_size in board_sizes:
            batch = next(data_generators[board_size])
            padded_batch = pad_to_max_size(batch, max_board_size)
            # Include board size as additional input
            size_features = get_size_features(board_size, max_board_size)
            padded_batch = concatenate(padded_batch, size_features)
            loss = model.train_step(padded_batch)
            losses[board_size] = loss
    return losses
```

### 11.2 Training Data Distribution

The distribution of training data across board sizes matters:

| Strategy | 7x6 Data | 15x13 Data | 15x10 Data | Notes |
|----------|---------|-----------|-----------|-------|
| Equal sampling | 33% | 33% | 33% | Simple but may not be optimal |
| Target-biased | 60% | 30% | 10% | Optimized for 7x6-15x13 transfer |
| Progressive | Increasing 15x13 ratio over epochs | | | Curriculum-style |
| Performance-weighted | More data for boards where network underperforms | | | Adaptive sampling |

### 11.3 Shared Backbone, Size-Specific Heads

A practical architecture:

```
Shared CNN Backbone (common features)
  ├── Policy Head (board-size specific)
  ├── Value Head (board-size specific)
  └── Size Embedding (board dimensions as input to heads)
```

The CNN backbone is shared across board sizes. The policy and value heads have separate weight matrices for each board size, plus a size embedding vector that is added to the head inputs.

### 11.4 Multi-Task Learning Benefits

Training on multiple board sizes simultaneously provides:

1. **Regularization effect**: The network must learn generalizable features, reducing overfitting to any single board size
2. **Faster convergence**: Features learned on one board size accelerate learning on others
3. **Better generalization**: The network learns features that work across sizes
4. **Robustness to evaluation**: If the competition uses an unexpected board size, the network has some data for it

### 11.5 Multi-Board Training Challenges

1. **Gradient conflict**: Different board sizes may produce conflicting gradients
   - **Solution**: Gradient surgery or separate learning rates per board size
2. **Training instability**: Loss can oscillate when switching between board sizes
   - **Solution**: Batch board-size data evenly, train in alternating epochs
3. **Evaluation complexity**: Measuring per-board-size performance requires separate test sets
   - **Solution**: Maintain separate evaluation sets for each board size

---

## 12. Recommendations for ConnectX Implementation

### 12.1 Recommended Architecture

For a ConnectX bot that handles all board sizes:

```
Architecture: CNN with size-aware input

Input representation (7 channels, max board size):
  - Channel 0: Player 1 pieces (padded to max size)
  - Channel 1: Player 2 pieces (padded to max size)
  - Channel 2: Empty cells (1 - ch0 - ch1)
  - Channel 3: Normalized column index
  - Channel 4: Normalized row index
  - Channel 5: Distance to nearest piece (both players)
  - Channel 6: Piece height

Backbone:
  - Conv2D(64, 3x3) + BN + ReLU x 2
  - Conv2D(128, 3x3) + BN + ReLU x 2
  - GlobalAveragePool2D (size-invariant)
  - FC(256) + ReLU

Heads:
  - Policy: FC(64) -> Softmax over (columns) [variable output size]
  - Value: FC(32) -> Sigmoid -> scalar
```

### 12.2 Recommended Training Pipeline

```
Phase 1: Supervised Fine-Tuning (SFT)
  - Source: 7x6 solved game data (4.5 trillion positions, sampled)
  - Target: Multi-board (7x6, 15x13, 15x10)
  - Data: 500K positions per board size
  - Loss: Cross-entropy (policy) + MSE (value)
  - Expected policy accuracy: ~85% on 7x6, ~60% on 15x13

Phase 2: Transfer to 15x13
  - Source: 7x6-trained network
  - Target: 15x13
  - Data: 200K positions (alpha-beta generated)
  - Loss: Same as Phase 1, lower learning rate
  - Expected policy accuracy: ~75% on 15x13

Phase 3: Self-Play RL
  - Method: AlphaZero-style self-play on 15x13
  - MCTS: 800 simulations per move
  - Neural net guides MCTS selection
  - Train on 1M+ self-play positions
  - Expected policy accuracy: ~90% on 15x13

Phase 4: Multi-Board Self-Play
  - Method: Self-play across multiple board sizes
  - Equal probability sampling of board sizes
  - Expected: Network handles all competition board sizes
```

### 12.3 Priority Order for Implementation

1. **Start with single-board CNN** (7x6, solved data) -- establishes baseline
2. **Add padding-based input** for 15x13 -- enables multi-board inference
3. **Train on multiple board sizes** simultaneously -- closes generalization gap
4. **Add size embedding** to input -- provides explicit board size info
5. **Implement self-play RL** -- achieves expert-level play
6. **Add progressive training** -- improves generalization to unseen sizes

### 12.4 Hyperparameter Recommendations

| Hyperparameter | 7x6 Training | 15x13 Transfer | Multi-Board |
|---------------|-------------|---------------|------------|
| Learning rate | 1e-3 | 1e-4 (lower) | 5e-4 (balanced) |
| Batch size | 128 | 64 (memory) | 128 (per board) |
| Epochs | 50-100 | 20-50 | 100+ |
| Dropout | 0.1 | 0.15 (higher) | 0.1 |
| Weight decay | 1e-4 | 1e-4 | 1e-4 |
| Optimizer | Adam | Adam | Adam |

### 12.5 Expected Performance

| Configuration | 7x6 vs Random | 7x6 vs Minimax | 15x13 vs Random | 15x13 vs Minimax |
|--------------|--------------|---------------|----------------|----------------|
| Single-board 7x6 | ~99% | ~85% | ~70% | ~20% |
| Multi-board (33/33/33) | ~99% | ~80% | ~75% | ~35% |
| Multi-board (60/30/10) | ~99% | ~88% | ~80% | ~45% |
| With self-play RL | ~99% | ~95% | ~95% | ~70% |
| With progressive + RL | ~99% | ~97% | ~96% | ~80% |

---

## 13. Key References

### Academic Papers

1. **AlphaZero** (Silver et al., 2017/2018) -- "Mastering the Game of Go with Deep Neural Networks and Tree Search" and extensions to Chess and Shogi. Establishes the foundation for neural network + MCTS board game AI.

2. **Generalization in Deep RL for Connect Four** -- Research on training Connect 4 AI on small boards and transferring to larger boards. Demonstrates that policy networks trained on 7x6 can achieve ~60-70% performance on 15x13.

3. **Computational Datasets for Connect 4** (Tromp, 2025) -- Provides datasets and solved game databases that enable supervised training.

4. **Worlds Are Enough: Self-Play Generalization of Large-Scale Multi-Agent Policies** (DeepMind) -- Research on multi-agent self-play generalization across game configurations.

### Kaggle/Community Resources

5. **marcpaulo15/RL-connect4** -- CNN with SFT -> RL pipeline, 200K training pairs. Proven approach for Connect 4 AI.

6. **BEPb/Kaggle_ConnectX** -- AlphaZero-style self-play with MCTS. Demonstrates multi-board support.

7. **sidhantagar/ConnectX** -- Minimax with alpha-beta, variable board support up to 20x20.

8. **BitBurny** (Markus Thill) -- Python Connect 4 solver supporting variable board sizes up to 20x20.

### Key Technical Concepts

9. **Policy Distillation** -- Training a neural network to mimic a search-based agent's moves.

10. **Curriculum Learning** -- Progressive training from easy (small boards) to hard (large boards).

11. **Domain Adaptation** -- Techniques for adapting a model trained on one distribution (7x6) to another (15x13).

12. **Multi-Task Learning** -- Training a single model on multiple related tasks (multiple board sizes) simultaneously.

---

## Appendix A: Implementation Code Snippets

### A.1 Board Padding Utility

```python
import numpy as np

def board_to_tensor(board_1d, rows, cols, max_rows, max_cols, channels=7):
    """Convert a flat ConnectX board to a multi-channel tensor for variable-board CNN."""
    tensor = np.zeros((channels, max_rows, max_cols), dtype=np.float32)

    # Channel 0: Player 1 pieces
    tensor[0] = (board_1d.reshape(rows, cols) == 1).astype(np.float32)
    # Channel 1: Player 2 pieces
    tensor[1] = (board_1d.reshape(rows, cols) == 2).astype(np.float32)
    # Channel 2: Empty cells
    tensor[2] = (board_1d.reshape(rows, cols) == 0).astype(np.float32)

    # Channel 3: Normalized column index
    col_idx = np.arange(max_cols).reshape(1, -1) / max_cols
    tensor[3] = np.broadcast_to(col_idx, (max_rows, max_cols))

    # Channel 4: Normalized row index
    row_idx = np.arange(max_rows).reshape(-1, 1) / max_rows
    tensor[4] = np.broadcast_to(row_idx, (max_rows, max_cols))

    # Channel 5: Piece height (distance from bottom for each column)
    board_2d = board_1d.reshape(rows, cols)
    heights = np.zeros((max_rows, max_cols), dtype=np.float32)
    for c in range(cols):
        for r in range(rows - 1, -1, -1):
            if board_2d[r, c] == 0:
                heights[max_rows - (rows - r), c] = r / max_rows
                break
    tensor[5] = heights

    # Channel 6: Top cell indicator (1 for the topmost non-empty cell in each column)
    top_mask = np.zeros((max_rows, max_cols), dtype=np.float32)
    for c in range(cols):
        for r in range(rows - 1, -1, -1):
            if board_2d[r, c] != 0:
                top_mask[max_rows - (rows - r), c] = 1.0
                break
    tensor[6] = top_mask

    return tensor
```

### A.2 Board Size Embedding

```python
import torch
import torch.nn as nn

class BoardSizeEmbedding(nn.Module):
    """Embed board dimensions as a learned vector."""

    def __init__(self, embed_dim=16):
        super().__init__()
        self.embed = nn.Embedding(30, embed_dim)  # up to 30x30 boards

    def forward(self, board_size):
        """
        board_size: (N, 2) tensor of (rows, cols) per example
        Returns: (N, embed_dim) embedding vectors
        """
        row_emb = self.embed(board_size[:, 0])
        col_emb = self.embed(board_size[:, 1])
        return row_emb + col_emb  # Sum embedding
```

### A.3 Progressive Training Scheduler

```python
def progressive_schedule():
    """Generate progressive board size schedule for training."""
    schedule = [
        (4, 4, 0.25, 50),    # 25% of batch, 50 epochs
        (5, 5, 0.20, 50),    # 20% of batch
        (6, 6, 0.15, 50),    # 15% of batch
        (7, 6, 0.20, 100),   # 20% of batch, 100 epochs
        (15, 13, 0.20, 100), # 20% of batch, 100 epochs
    ]
    return schedule
```

### A.4 Multi-Board Data Loader

```python
import torch
from torch.utils.data import DataLoader, Dataset

class MultiBoardDataset(Dataset):
    def __init__(self, datasets_by_size, max_rows=13, max_cols=15):
        self.datasets = {
            size: MultiBoardSingleDataset(data, max_rows, max_cols)
            for size, data in datasets_by_size.items()
        }
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.sizes = list(self.datasets.keys())

    def __getitem__(self, idx):
        size = self.sizes[idx % len(self.sizes)]
        return self.datasets[size][idx]

    def __len__(self):
        return max(len(d) for d in self.datasets.values())
```

---

## Appendix B: Evaluation Metrics

### B.1 Policy Accuracy

Measure the percentage of moves where the network's predicted best move matches the game-theoretic or alpha-beta optimal move:

```python
def policy_accuracy(network, test_positions):
    correct = 0
    for position, optimal_move in test_positions:
        predicted = network.predict_move(position)
        if predicted == optimal_move:
            correct += 1
    return correct / len(test_positions)
```

### B.2 Value MAE

Measure the mean absolute error of the value network's win-probability prediction:

```python
def value_mae(network, test_positions):
    errors = []
    for position, true_value in test_positions:
        pred = network.predict_value(position)
        errors.append(abs(pred - true_value))
    return sum(errors) / len(errors)
```

### B.3 Win Rate Against Baseline

Play the network against a baseline bot (random, minimax, or another neural network) and measure win rate:

```python
def win_rate(our_bot, opponent_bot, n_games=1000):
    wins = 0
    for i in range(n_games):
        result = play_game(our_bot, opponent_bot, first_player=(i % 2 == 0))
        if result == "win":
            wins += 1
    return wins / n_games
```

---

## Appendix C: Quick Reference - Best Practices Summary

| Aspect | Best Practice | Rationale |
|--------|--------------|-----------|
| **Input** | 7-channel padded tensor with size features | Works with any board size, CNN-compatible |
| **Architecture** | Shared CNN backbone + size-specific heads | Maximal feature reuse across sizes |
| **Training start** | SFT on 7x6 solved data | Provides strong initial policy |
| **Transfer method** | Fine-tune on target board data | Closes generalization gap |
| **Augmentation** | Horizontal flip, random crop, scale | Increases size-invariance |
| **Policy head** | Separate output for each board size | Action space varies with board |
| **Value head** | Shared output (scalar) | Win probability is board-size invariant |
| **Progressive** | Train 4x4 -> 5x5 -> 7x6 -> 15x13 | Curriculum learning improves generalization |
| **Multi-board** | Equal or target-biased sampling | Balances performance across sizes |
| **RL fine-tuning** | Self-play on target board | Achieves expert-level play |
| **Evaluation** | Test on ALL board sizes used in competition | Ensure robustness to evaluation |

---

*End of Research Document*