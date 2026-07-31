# Neural Network Architecture Research for ConnectX

> **Generated**: 2026-07-30 (Iteration 2)
> **Purpose**: Optimal neural network architecture for ConnectX/Connect 4
> **Status**: Based on web research, known implementations, and game AI literature

---

## Optimal CNN Architecture for Connect 4

### Recommended Architecture (Proven by marcpaulo15)

```
Input: Board state (multiple channels)
        ↓
Conv2D + BatchNorm + ReLU × N (N=8-15 layers)
        ↓
Flatten
        ↓
FC Head 1: Policy (7 nodes → softmax → move probability)
        ↓
FC Head 2: Value (1 node → sigmoid → win probability)
```

### Architecture Specifications

| Parameter | Recommended | Alternative |
|-----------|-------------|-------------|
| **Input channels** | 3 (player 1, player 2, empty) | 2 (just player 1) + board size features |
| **Conv filter size** | 3×3 | 5×5 (larger receptive field) |
| **Number of layers** | 8-15 | 5 (small) / 20+ (large) |
| **Channels per layer** | 64-256 (increasing) | 32 (small) / 512 (large) |
| **Activation** | ReLU | Tanh / LeakyReLU |
| **Batch norm** | Yes | No (simpler) |
| **Policy head** | FC → 7 → softmax | FC → 14 → softmax (with board rotation) |
| **Value head** | FC → 128 → FC → 1 | FC → 64 → FC → 1 |

### Parameter Counts

| Model Size | Layers | Channels | Parameters | Training Data Needed | Expected Strength |
|-----------|--------|----------|------------|---------------------|-------------------|
| Tiny | 5 | 32 | ~100K | 10K positions | Weak (below random) |
| Small | 8 | 64 | ~500K | 50K positions | Below minimax |
| Medium | 10 | 128 | ~1.5M | 200K positions | Near minimax |
| Large | 15 | 256 | ~8M | 500K+ positions | Expert |
| XL | 20 | 512 | ~30M | 1M+ positions | Superhuman |

### Key Insight from marcpaulo15

- **CNN layers frozen as feature extractor**: Train CNN on SFT data, then freeze early layers and only train FC layers for RL
- **200K (state, action) pairs**: Sufficient for effective SFT
- **Transfer learning**: After SFT, apply RL (PPO, DQN, REINFORCE, Dueling DQN)

### Why This Architecture Works

1. **Convolutional layers** capture spatial patterns (connected pieces, threats)
2. **Multiple channels** provide richer input (separate player, opponent, empty)
3. **Policy head** outputs move probability distribution (soft, not hard)
4. **Value head** outputs win probability (scalar, useful for MCTS)
5. **Frozen features**: Early layers learn generic board patterns; FC layers adapt to specific tasks

---

## Alternative Architectures

### 1. Transformer Architecture

```
Input: Piece positions as tokens
        ↓
Positional encoding
        ↓
Transformer encoder × N layers
        ↓
Pool (mean/max)
        ↓
Policy/Value heads
```

**Pros**: Captures long-range dependencies better than CNN
**Cons**: More parameters, slower training, less data-efficient

### 2. ResNet Architecture

```
Input → Conv → Residual Block × N → Flatten → Policy/Value
```

**Pros**: Residual connections enable very deep networks
**Cons**: Overkill for Connect 4's relatively simple patterns

### 3. Graph Neural Network

```
Input: Board as graph (cells as nodes)
        ↓
Graph convolution × N layers
        ↓
Readout (global pooling)
        ↓
Policy/Value heads
```

**Pros**: Naturally handles variable board sizes
**Cons**: Complex to implement, less established for board games

### Recommendation

**Start with CNN (proven, effective)** → **If results plateau, try Transformer**

---

## Training Strategies

### 1. Supervised Fine-Tuning (SFT)

**Dataset**: (state, action) pairs from solved game database
**Method**: Train policy head to predict optimal moves
**Loss**: Cross-entropy loss
**Expected accuracy**: 80-95% on solved positions

### 2. Reinforcement Learning (RL)

**Algorithm**: PPO (recommended), DQN, REINFORCE, Dueling DQN
**Method**: Self-play, update network from MCTS results
**Loss**: Combination of policy + value loss

### 3. Hybrid (Recommended)

```
SFT → RL → SFT → RL → ... (alternating)
```

**Why**: SFT provides strong initialization, RL fine-tunes beyond heuristic limits

---

## Input Representation

### Standard (3 Channels)

```
Channel 0: Current player's pieces (1 for piece, 0 for empty)
Channel 1: Opponent's pieces (1 for piece, 0 for empty)
Channel 2: Empty cells (1 for empty, 0 for occupied)
```

### Expanded (7 Channels)

```
Channel 0: Current player's pieces
Channel 1: Opponent's pieces
Channel 2: Empty cells
Channel 3: Piece height (y-coordinate)
Channel 4: Distance to nearest player piece
Channel 5: Distance to nearest opponent piece
Channel 6: Board edge mask (1 near edge, 0 otherwise)
```

### Recommended for 7x6

**Start with 3-channel** (simplest, effective) → **If performance plateaus, try 7-channel**

### Recommended for Larger Boards

**Expanded representation** (7+ channels) to capture spatial information

---

## Optimization for Inference

### TensorRT Optimization

1. **FP16 precision**: ~2× speedup vs FP32
2. **INT8 precision**: ~4× speedup vs FP32 (with calibration)
3. **Layer fusion**: Combine Conv + BN + ReLU into single layer
4. **Dynamic batching**: Batch multiple inferences for throughput

### Expected Inference Speed (RTX 5090)

| Model Size | FP32 | FP16 | INT8 |
|-----------|------|------|------|
| 100K params | 0.05ms | 0.025ms | 0.01ms |
| 500K params | 0.2ms | 0.1ms | 0.05ms |
| 1.5M params | 0.5ms | 0.25ms | 0.12ms |
| 8M params | 2ms | 1ms | 0.5ms |
| 30M params | 8ms | 4ms | 2ms |

### Key Insight

> For 2-second-per-move constraint:
> - Up to 8M param model is feasible (1ms inference = 2000 evaluations)
> - Up to 30M param model is feasible with batching (4ms inference = 500 evaluations)
> - For MCTS (800 simulations): Need sub-1ms inference → use small model (100K-500K params)

---

## Open Questions

1. What is the smallest effective network for Connect 4?
2. How does board size affect optimal architecture?
3. Is a single network for all board sizes feasible?
4. What about attention-based architectures?
5. How much does batch norm help for Connect 4?
6. Is there an optimal filter size for Connect 4? (3×3 vs 5×5?)
7. Can we use graph neural networks effectively for variable board sizes?

---

## References

- marcpaulo15/RL-connect4: CNN with SFT → RL, 200K training pairs
- BEPb/Kaggle_ConnectX: CNN + MCTS with PARL framework
- AlphaZero paper: ConvNet with MCTS for Go/Chess/Shogi
- Silver et al. (2017): Mastering the Game of Go with Deep Neural Networks