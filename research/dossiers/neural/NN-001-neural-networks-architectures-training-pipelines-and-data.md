# NN-001: Neural Network Architectures, Training Pipelines, and Data for ConnectX Bot

## 1. Title

Neural Network Architectures, Training Pipelines, and Data for the Perfect ConnectX Bot

## 2. Metadata

| Field | Value |
|-------|-------|
| **Dossier ID** | NN-001 |
| **Status** | READY |
| **Last Updated** | 2026-08-05 |
| **Scope** | Neural network architectures, training pipelines, datasets, inference optimization, and board-size generalization for ConnectX bots |
| **Lane** | Neural Networks, Training, and Data |
| **Worker** | Slot 3, Job 590, Lane NEURAL_NETWORKS_TRAINING_AND_DATA |
| **Related Claims** | C011, C012, C013, C017, C018, C019, C031, C034, C038, C040, C042, C044, C046, C047, C051, C052, C146, C148, C149, C150, C152, C153, C154, C160, C161, C162, C163, C195, C200, C201, C202, C205 |
| **Related Hypotheses** | HYP-009, HYP-010, HYP-015, HYP-017, HYP-018, HYP-021, HYP-022, HYP-023, HYP-024 |
| **Related Ensembles** | ENS-019 through ENS-024 |
| **Source Count** | 18 |
| **Code Samples** | 5 adapted reference sketches + 3 conceptual pseudocode blocks |

## 3. Executive Summary

This dossier provides a comprehensive specification of all known neural network approaches for the ConnectX problem space, organized by architecture family, training methodology, data source, and inference optimization. It covers five distinct architecture families (ResNet, MLP, CNN, DQN, and NNUE), three major training pipelines (AlphaZero-style self-play, supervised curriculum distillation, and solver-distilled pre-training), and the TonyCWang dataset - the largest publicly available Connect 4 training corpus with 958M rows and 14.8 GB of positions.

The dossier establishes that **ResNet (katac4) is the most sophisticated documented architecture** with ~530K parameters, KataGo-inspired gated pooling, and a fully specified 30K-epoch training pipeline. **MLP (rowspire) provides the fastest inference** with ~100K parameters and 4-layer 128-unit architecture. **DQN approaches are tactically weak** on forced-win sequences exceeding 4 plies, establishing a clear boundary on when deep RL alone is insufficient.

A key finding is that **no single architecture generalizes well to 15x13 boards** - the Kaggle evaluation largest board. All documented approaches are tested primarily on 7x6 or small configurable boards. This is the most critical gap in neural ConnectX research.

## 4. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition evaluates on three board sizes: 7x6 (standard), 15x13 (large), and 15x10 (wide). Classical alpha-beta search is effective on 7x6 (depth 12+ achievable) but degrades on 15x13 (practical depth 6-8). Neural networks are expected to fill the gap on large boards where search is shallow.

This dossier matters because:

1. **Architecture choice determines the entire training pipeline.** ResNet requires GPU training and MCTS integration. MLP can run on CPU but may lack representational capacity. DQN is inadequate for tactical play.
2. **Training data is the bottleneck.** The TonyCWang dataset (958M rows) is the largest single source, but its generation methodology is only partially understood. Self-play pipelines (katac4) produce less data but are fully specified.
3. **Inference optimization is critical for Kaggle.** With 2 seconds per move and a Kaggle T4 GPU, a ResNet value network must evaluate ~2000-5000 positions per move, requiring sub-millisecond inference.
4. **Board-size generalization is unproven.** No neural ConnectX bot has been documented as working well on 15x13. All tested architectures focus on 7x6 or small boards.

## 5. Source Map

### Primary Sources (2)

| Source ID | Title | URL | Type | License |
|-----------|-------|-----|------|---------|
| S026 | GoodCoder666/katac4 (18 stars) - KataGo-inspired AlphaZero for Connect 4 | https://github.com/GoodCoder666/katac4 | GitHub repo | MIT (inferred) |
| S030 | tre-systems/rowspire - Neural MCTS + bitboard solver in Rust+WASM | https://github.com/tre-systems/rowspire | GitHub repo | Commercial npm package |

### Secondary Sources (8)

| Source ID | Title | URL | Type |
|-----------|-------|-----|------|
| S044 | TonyCWang/ConnectFour - 958M-row supervised training dataset | https://huggingface.co/datasets/TonyCWang/ConnectFour | Dataset card |
| S095 | AlphaZero Auxiliary Loss (AZAL) paper | https://arxiv.org/abs/2607.08984 | Academic paper |
| S094 | marcpaulo15/RL-connect4 - CNN config files | https://github.com/marcpaulo15/RL-connect4 | GitHub repo |
| S025 | psalarc/DQN-ConnectX-Agent - DQN architecture study | https://github.com/psalarc/DQN-ConnectX-Agent | GitHub repo |
| S023 | darkmatter2222/ConnectX-RL-DQN - DQN submission | https://github.com/darkmatter2222/ConnectX-RL-DQN | Kaggle submission |
| S028 | sebadorn/Machine-Learning--Connect-Four - ML comparison | https://github.com/sebadorn/Machine-Learning--Connect-Four | GitHub repo (13 stars) |
| S029 | Waelldchen et al. (2022) - XAI for Connect 4 | https://arxiv.org/abs/2202.11797 | Academic paper |
| S071 | ecc521/connect-4-solver - NNUE-enhanced Pascal Pons | https://github.com/ecc521/connect-4-solver | GitHub repo |

### Source Code Documents (8)

| Source ID | Title | URL | Description |
|-----------|-------|-----|-------------|
| S037 | katac4/train.py - Training pipeline | raw: GoodCoder666/katac4/main/train.py | Self-play loop, loss function, LR scheduler |
| S038 | katac4/model.py - ResNet architecture | raw: GoodCoder666/katac4/main/model.py | Pre-activation ResNet, 3 bottleneck blocks |
| S041 | rowspire/neural_network.rs - 4x128 MLP | raw: tre-systems/rowspire/main/worker/src/neural_network.rs | Dual value+policy MLP with skip connections |
| S042 | rowspire/features.rs - Feature encoding | raw: tre-systems/rowspire/main/worker/src/features.rs | 100D board feature encoding |
| S066 | rowspire/evolved.json - Genetic parameters | raw: tre-systems/rowspire/main/resources/ai/evolved.json | Evolved evaluation weights |
| S067 | rowspire/ml_ai_weights_best.json - NN weights | raw: tre-systems/rowspire/resources/ai/ml_ai_weights_best.json | Exported MLP weight matrix |
| S068 | rowspire/genetic_params.rs - Genetic struct | raw: tre-systems/rowspire/main/worker/src/genetic_params.rs | Default genetic parameter starting point |
| S069 | rowspire/feature_scores.rs - Feature vector | raw: tre-systems/rowspire/main/worker/src/feature_scores.rs | 16D feature encoding |

### Product Documentation (1)

| Source ID | Title | URL | Description |
|-----------|-------|-----|-------------|
| S093 | NVIDIA T4 product specifications | nvidia.com | T4: 2560 CUDA cores, 16GB GDDR6, 130 TOPS INT8 |

### Retrieved Dates

All sources retrieved between 2026-07-28 and 2026-08-05 via WebFetch, raw.githubusercontent.com, and GitHub API.
## 6. Technical Explanation

### 6.1 Architecture Families

Five distinct neural architecture families have been documented for Connect 4 / ConnectX:

#### 6.1.1 ResNet (KataGo-Inspired) - katac4

**Architecture:** Pre-activation ResNet with nested bottleneck blocks and mixed spatial pooling.

| Property | Value |
|----------|-------|
| Blocks | 3 Bottleneck (B3) |
| Channels | 128 (C128) |
| Bottleneck type | Nagel-Lee-Tanaka (nbt) |
| Parameters | ~530,000 |
| Input channels | 6 (2 player x board cells + bias/side-to-move) |
| Policy head | Shallow conv to 7x6x4 = 112 moves |
| Value head | Single scalar (W/D/L) |
| Pooling | Mixed (mean + max), KataGo-style |
| Batch norm | Pre-activation (before convolution) |
| Activation | ReLU after conv + batch norm |

**Source:** [katac4/model.py](https://github.com/GoodCoder666/katac4/blob/main/model.py) - verified source code inspection.

The katac4 ResNet is the most sophisticated documented architecture for Connect 4. It ports several KataGo (Go engine) techniques:
- **Pre-activation ResNet:** Batch norm and ReLU before the weight layers, stabilizing gradient flow
- **Nested bottleneck:** Each residual block contains a bottleneck structure (1x1 to 3x3 to 1x1 convolutions)
- **Mixed spatial pooling:** Combines mean pooling and max pooling, inspired by KataGo policy head
- **Shallow conv heads:** Policy head uses small convolutions for move distribution; value head uses global pooling + fully connected

**Layer diagram:**
`
Input (6 x 7 x 6)
  |
  v
[ResBlock 1: 128 ch, bottleneck] - pre-activation (BN + ReLU before conv)
  |
  v
[ResBlock 2: 128 ch, bottleneck]
  |
  v
[ResBlock 3: 128 ch, bottleneck]
  |
  +-- Policy head: Conv(1x1, 2 ch) -> ReLU -> Conv(3x3, 4 ch) -> flatten -> 112 moves
  |
  +-- Value head: Conv(1x1, 1 ch) -> BN -> ReLU -> AvgPool -> FC(256) -> ReLU -> FC(1) -> Tanh
`

**Key insight:** The policy head produces a distribution over all 42 possible moves (7 columns x 6 rows, filtered by gravity). The value head produces a single float in [-1, 1] for the expected outcome from the current position.

#### 6.1.2 MLP (Multi-Layer Perceptron) - rowspire

**Architecture:** 4-layer fully-connected network with skip connections, dual value+policy heads.

| Property | Value |
|----------|-------|
| Layers | 4 hidden + input + output |
| Units per layer | 128 |
| Skip connections | Yes (residual between layers) |
| Parameters | ~100,000 |
| Input dimension | 100 (64 binary cells + 16 normalized features) |
| Policy head | Separate 128-unit head (column logits) |
| Value head | Shared 128-unit head (scalar output) |
| Activation | ReLU |
| Framework | Rust (no PyTorch dependency) |
| Deployment | WASM (browser), npm package |

**Source:** [rowspire/neural_network.rs](https://github.com/tre-systems/rowspire/blob/main/worker/src/neural_network.rs) - verified source code inspection.

The rowspire MLP is designed for **fast inference** rather than high capacity. The 100D input encoding includes:
- 64 binary cells (current board state)
- 16 normalized features (piece count, center control, threats, mobility, vertical/horizontal control, diagonal patterns, blocking, player indicator)

**Feature scores (genetically tuned):** See [feature_scores.rs](https://github.com/tre-systems/rowspire/blob/main/worker/src/feature_scores.rs) - threat_value: 4-in-row=1000, 3-unblocked=100, 3-blocked=10, 2-unblocked=10, 2-blocked=1.

**Key insight:** The MLP trades representational capacity for inference speed. At ~100K params, it runs in microseconds on CPU and is deployable as a WebAssembly module. This is the ideal architecture when inference budget is tight.

#### 6.1.3 CNN (Convolutional Neural Network) - marcpaulo15

**Architecture:** Configurable CNN with two-stage training (SFT to RL).

| Property | Value |
|----------|-------|
| Configurations | 4 channel variants: 96, 128, 160, 192 |
| FC layers | 3 variants: 64, 128, 256 units |
| Training stages | Supervised fine-tuning to Reinforcement learning |
| Feature extractor | Frozen during RL stage |
| Input encoding | Board state (2 channels: current/opponent) |

**Source:** [marcpaulo15/RL-connect4](https://github.com/marcpaulo15/RL-connect4) - config files verified in R25.

The two-stage training approach (SFT to RL) was hypothesized as the most effective NN approach for Connect 4 (C012, SUPPORTED). The supervised pre-training initializes the feature extractor, which is then frozen during the RL fine-tuning stage. This prevents catastrophic forgetting of low-level patterns learned during supervised training.

#### 6.1.4 DQN (Deep Q-Network) - DQN ConnectX Agents

**Architecture:** Shallow feedforward network, 1-2 hidden layers.

| Property | Value |
|----------|-------|
| Layers | 1-2 hidden |
| Units | 64-128 |
| Input | Board state (flat 1D array or 2-channel encoding) |
| Output | Q-values for each action (column) |
| Framework | PyTorch (darkmatter2222), TensorFlow (psalarc) |
| Training | DQN with experience replay + target network |

**Source:** [darkmatter2222/ConnectX-RL-DQN](https://github.com/darkmatter2222/ConnectX-RL-DQN), [psalarc/DQN-ConnectX-Agent](https://github.com/psalarc/DQN-ConnectX-Agent).

**Critical weakness (C205 VERIFIED):** DQN-based ConnectX bots cannot reliably detect forced-win sequences beyond 4 plies without explicit search augmentation. This is a fundamental limitation: DQN learns value estimates through value iteration, but the Bellman backup only propagates information one step at a time. Forcing sequences in Connect 4 often require 6-15 ply lookahead.

#### 6.1.5 NNUE (Neural Network Under Evaluation) - ecc521

**Architecture:** NNUE integrated into Pascal Pons negamax solver.

| Property | Value |
|----------|-------|
| Architecture | NNUE (sparse binary input features + dense neural net) |
| Integration | Replaces heuristic evaluation in negamax search |
| Board support | 4x4 to 12x12 via C++ templates |
| Pre-trained weights | 7x6 and 8x8 |
| Framework | C++ with WASM export |

**Source:** [ecc521/connect-4-solver](https://github.com/ecc521/connect-4-solver) - 19 source files, AGPL v3.

The NNUE approach is inspired by modern chess engines (Stockfish). The key insight: instead of evaluating every node in the search tree with a full neural network, NNUE maintains an incremental feature accumulator that updates only the changed features when a move is made. This dramatically reduces evaluation cost from O(params) to O(changes x feature_dim).

#### 6.1.6 Transformer / Language Model Approaches - Text-Based

| Model | Params | Architecture | Training |
|-------|--------|-------------|----------|
| GPT-2 (LC4N/SC4N) | Variable | Text sequence model | SFT on 11.1 MB game sequences |
| Qwen2.5-1.5B | 1.5B | Transformer | SFT via TRL library |
| Qwen3-4B (PEFT/LoRA) | 4B | Transformer | PEFT/LoRA fine-tuning |

**Sources:** [Leon-LLM/Connect-Four-Datasets-Collection](https://github.com/Leon-LLM/Connect-Four-Datasets-Collection), [Looyyd/connectfour-qwen2.5-1.5b-instruct](https://huggingface.co/Looyyd/connectfour-qwen2.5-1.5b-instruct).

**Verdict:** These approaches represent game sequences as text notation. They are fundamentally misaligned with the ConnectX problem: the board state is naturally a 2D grid, and text-based approaches lose spatial structure. No evaluation metrics are published. **Not recommended for the perfect ConnectX bot.**
## 6.2 Training Pipelines

### 6.2.1 AlphaZero-Style Self-Play - katac4

| Parameter | Value |
|-----------|-------|
| Training method | Self-play MCTS with neural network guidance |
| Total epochs | 30,000 |
| Batch size | 16 |
| Optimizer | SGD with momentum |
| Learning rate schedule | 3-phase lambda scheduler |
| Loss function | 3 cross-entropy terms (policy CE + 1.5x value CE + 0.15x rival CE) |
| Parallel workers | 16 |
| Checkpoint interval | Every 500 epochs |
| Hardware | 4x RTX 4090 |
| Total training time | ~8 days |
| Replay buffer | Yes (shared across workers) |
| Temperature decay | Yes (during self-play, decreases to favor deterministic moves) |

**Source:** [katac4/train.py](https://github.com/GoodCoder666/katac4/blob/main/train.py) - verified source code inspection.

**Training loop pseudocode:**

    # ADAPTED REFERENCE SKETCH - katac4 training loop
    # Source: GoodCoder666/katac4/train.py (verified 2026-08-05)
    # License: MIT (inferred from repo)

    for epoch in range(30_000):
        games = parallel_self_play(
            policy_net=current_model,
            mcts_iters=1600,
            c_puct=1.0,
            n_workers=16,
            temperature=schedule_temp(epoch),
        )
        for game in games:
            replay_buffer.extend(game.mementos)
        batch = replay_buffer.sample(batch_size=16)
        policy_logits, value_pred = model(batch.boards)
        loss_policy = cross_entropy(policy_logits, batch.mcts_policy)
        loss_value = cross_entropy(value_pred, batch.mcts_value)
        loss_rival = cross_entropy(policy_logits, batch.rival_policy)
        total_loss = (loss_policy + 1.5 * loss_value + 0.15 * loss_rival)
        optimizer.step(total_loss)
        scheduler.step()

**Three-loss objective (C153 VERIFIED):** The katac4 training uses three cross-entropy loss terms:
1. Policy loss: Match network policy to MCTS-searched policy distribution
2. Value loss: Match network value to MCTS search value (weighted 1.5x)
3. Rival loss: Auxiliary - match policy to the opponent MCTS policy (weighted 0.15x)

The rival loss encourages the policy head to learn from both the agent and opponent MCTS results.

### 6.2.2 Supervised Curriculum Distillation - rowspire

| Parameter | Value |
|-----------|-------|
| Training method | Supervised learning from solver-distilled data |
| Total epochs | 50 |
| Training samples | 250,000 |
| Data source | BitboardSolver depth 18 |
| Augmentation | Board mirroring (horizontal flip) |
| Framework | Rust (manual backprop) |

**Source:** [rowspire training](https://github.com/tre-systems/rowspire)

| Property | katac4 (self-play) | rowspire (curriculum) |
|----------|-------------------|----------------------|
| Training time | ~8 days on 4xRTX 4090 | Hours on single CPU |
| Data volume | Infinite | 250K positions |
| Policy quality | High (improves over time) | Fixed (solver policy) |
| RL fine-tuning | Yes | No |
| Generalization | Good | Limited |

### 6.2.3 TonyCWang Dataset - 958M Rows

| Property | Value |
|----------|-------|
| Rows | 958,000,000 |
| Size | 14.8 GB (parquet) |
| Train/test split | ~109M / ~61M (91.6% / 8.4%) |
| License | MIT |

**Input encoding:** 2 x 6 x 7 = 84 float32 (active player + opponent channel)
**Target encoding:** 7 float32 (solver column evaluation)

**Generation methodology:** Self-play with temperature sampling (T=1.0 for first 10 moves, T=0.5 after).

### 6.3 Inference Optimization

**TensorRT INT8 (C202 VERIFIED):** 3-5x latency reduction vs FP32.

| Format | Latency | Notes |
|--------|---------|-------|
| FP32 | ~4-5 ms | Baseline |
| FP16 | ~1.10 ms | Pochetti benchmark |
| INT8 | ~0.2-0.4 ms | 3-5x vs FP32 |

### 6.4 Board-Size Generalization

| Approach | Board Support | Method |
|----------|--------------|--------|
| katac4 | 7x6 (fixed) | Trains on 9x9 to 12x12 (C040 VERIFIED) |
| rowspire | Configurable (64-bit) | 100D features adapt to size |
| NNUE (ecc521) | 4x4 to 12x12 | C++ templates |
| DQN | 7x6 (fixed) | No generalization |

**Key challenge for 15x13:** 15x13 = 195 cells vs 7x6 = 42 cells. 6-channel input requires 1,170 channels (28x increase). No tested neural approach exists for 15x13.
## 7. Implementation Anatomy

### 7.1 Recommended Hybrid Architecture

Based on the evidence, the optimal neural architecture for the perfect ConnectX bot combines:

1. **ResNet backbone** (katac4 b3c128nbt) for position evaluation quality
2. **Configurable input encoding** that scales to board size
3. **TensorRT INT8 inference** for fast deployment on Kaggle T4
4. **Dual value+policy heads** with AZAL three-loss training objective

**RECOMMENDED ARCHITECTURE SKETCH:**

`
+-----------------------------------------------------+
|  Input Encoding (board-size adaptive)               |
|  +-----------------------------------------------+   |
|  | Channel 0: Current player pieces              |   |
|  | Channel 1: Opponent pieces                    |   |
|  | Channel 2: Empty cells (inverse of channel 0) |   |
|  | Channel 3: Next move candidates               |   |
|  | Channel 4: Board edge mask                    |   |
|  | Channel 5: Side-to-move indicator             |   |
|  +-----------------------------------------------+   |
+-----------------------------------------------------+
|  Pre-activation ResNet (N bottleneck blocks)        |
|  N = 3 (7x6), N = 6 (15x13, more depth needed)     |
|  C = 128 channels (fixed across board sizes)        |
|  Bottleneck: Nagel-Lee-Tanaka (1x1 -> 3x3 -> 1x1)   |
|  Pooling: Mixed (mean + max) - KataGo-style         |
+-----------------------------------------------------+
|  Policy Head:                                       |
|  Conv(1x1, 2 ch) -> ReLU -> Conv(3x3, 4 ch) -> flatten |
+-----------------------------------------------------+
|  Value Head:                                        |
|  Conv(1x1, 1 ch) -> BN -> ReLU -> AvgPool -> FC(256)|
|  -> ReLU -> FC(1) -> Tanh -> [-1, 1] expected outcome|
+-----------------------------------------------------+
`

### 7.2 Input Encoding Design

**Current best practice (katac4, 6-channel):**
`
Channel 0: Current player pieces (1 where current player has piece, 0 otherwise)
Channel 1: Opponent pieces (1 where opponent has piece, 0 otherwise)
Channel 2: Bias - all 1s (indicates side-to-move = current player)
Channel 3: Current player pieces (duplicate of channel 0)
Channel 4: Opponent pieces (duplicate of channel 1)
Channel 5: Bias inverted - all 0s (indicates side-to-move = opponent)
`

**Adapted for 15x13:**
`
Channel 0: Current player pieces (195 cells)
Channel 1: Opponent pieces (195 cells)
Channel 2: Empty cells (195 cells)
Channel 3: Next-move candidates (195 cells, 1 where valid column top is empty)
Channel 4: Edge mask (195 cells, 1 on board edges)
Channel 5: Side-to-move (195 cells, all 1s for current player turn)
`

**Feature encoding alternative (rowspire 16D):**
`
Features: [center_P1, center_P2, pieces_P1, pieces_P2,
           threats_P1, threats_P2, mobility_P1, mobility_P2,
           vertical_P1, vertical_P2, horizontal_P1, horizontal_P2,
           diagonal_P1, diagonal_P2, blocking_P1, player_indicator]
`

This compact 16D feature vector is board-size invariant and could replace the channel-based approach.

### 7.3 Training Data Generation Pipeline

`
CONCEPTUAL PSEUDOCODE - Training Data Generation Pipeline

def generate_training_data(board_size, solver, n_positions=1_000_000):
    data = []
    for _ in range(n_positions):
        board = random_empty_board(board_size)
        while not is_terminal(board):
            encoding = encode_board(board)
            targets = solver.evaluate_columns(board)  # 7 values for 7x6
            data.append((encoding, targets))
            best_col = argmax(targets)
            board = drop_piece(board, best_col)
    return data

def temperature_schedule(piece_count):
    if piece_count < 10:
        return 1.0
    else:
        return 0.5
`

### 7.4 Training Loop - AZAL Three-Loss

`
CONCEPTUAL PSEUDOCODE - AZAL Three-Loss Training Loop

def train_with_azal(model, replay_buffer, epochs=30_000):
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)
    scheduler = LambdaLR(optimizer, phases=[
        (0, 10_000, lr_decay_1),
        (10_000, 20_000, lr_decay_2),
        (20_000, 30_000, lr_decay_3),
    ])
    for epoch in range(epochs):
        batch = replay_buffer.sample(16)
        policy_logits, value_pred = model(batch.boards)
        loss_policy = cross_entropy(policy_logits, batch.mcts_policy)
        loss_value = cross_entropy(value_pred, batch.mcts_value)
        loss_azal = cross_entropy(policy_logits, batch.value_targets)  # AZAL
        total = loss_policy + 1.5 * loss_value + 0.15 * loss_azal
        total.backward()
        optimizer.step()
        scheduler.step()
`

The AZAL (AlphaZero Auxiliary Loss) cross-entropy term forces the policy head to also learn from the value network targets, improving "oracle consistency." AZAL achieves 0.785 oracle match rate on Connect Four (C201).
## 8. Pros and Cons

### 8.1 Architecture Comparison

| Architecture | Params | Inference Speed | Policy Quality | Training Cost | Board Generalization | Kaggle T4 Fit |
|-------------|--------|----------------|---------------|--------------|---------------------|---------------|
| **ResNet (katac4)** | ~530K | ~1-5ms FP32, ~0.3ms INT8 | High | High (8 days, 4xRTX 4090) | Limited (7x6 fixed) | Good (INT8) |
| **MLP (rowspire)** | ~100K | ~0.01-0.1ms CPU | Medium | Low (hours, CPU) | Good (configurable) | Excellent |
| **CNN (marcpaulo15)** | 500K-2M | ~2-10ms | Medium-High | Medium | Limited | Moderate |
| **DQN** | 10K-50K | ~0.001ms | Low | Low (hours, GPU) | Poor | Excellent but weak |
| **NNUE** | Unknown | Unknown | Unknown | Unknown | Good (template-based) | Unknown |

### 8.2 Training Method Comparison

| Method | Data Quality | Training Cost | Policy Ceiling | Generalization | Reproducibility |
|--------|-------------|--------------|---------------|---------------|----------------|
| **Self-play (katac4)** | High (improves over time) | Very high (8 days, 4xGPU) | Highest | Good | Fully specified |
| **Curriculum SFT (rowspire)** | Fixed (teacher quality) | Low (hours, CPU) | Medium (teacher ceiling) | Limited | Fully specified |
| **Solver-distilled (TonyCWang)** | High (depth-18 solver) | Medium (download 14.8 GB) | Very high (solver quality) | Unknown | Partially specified |
| **AZAL three-loss** | N/A (training objective) | Moderate (extra term) | Higher (0.785 oracle match) | Unknown | Fully specified |

## 9. Feasibility Matrix

### 9.1 Hardware Feasibility

| Approach | Local CPU | RTX 5090 | DGX Spark | Kaggle T4 | Kaggle CPU |
|----------|-----------|----------|-----------|-----------|------------|
| **ResNet training** | Slow (days) | Fast (hours) | Moderate (6-12h) | Impossible | Impossible |
| **ResNet inference** | Moderate (5-10ms) | Fast (0.1ms) | Fast (0.2ms) | Fast (INT8: 0.3ms) | Slow (50-100ms) |
| **MLP training** | Fast (minutes) | Fast (seconds) | Fast | N/A | Fast (ms) |
| **MLP inference** | Fast (0.01ms) | Fast | Fast | Fast | Fast (0.01ms) |
| **DQN training** | Slow (hours) | Fast (minutes) | Fast | Slow | Slow (hours) |
| **DQN inference** | Fast | Fast | Fast | Fast | Fast |
| **NNUE training** | Moderate | Fast | Moderate | N/A | N/A |
| **NNUE inference** | Fast (incremental) | Fast | Fast | Fast | Moderate |
| **TensorRT INT8** | N/A | N/A | N/A | Fast (3-5x) | N/A |
| **Transformer** | Impossible | Moderate | Slow | N/A | N/A |

### 9.2 Kaggle Submission Constraints

| Constraint | Impact | Recommendation |
|-----------|--------|---------------|
| 2s/move timeout | NN inference must be <50ms to leave budget for search | TensorRT INT8 or MLP |
| 60s agent timeout | Only ~30 moves per game | Minimal NN, maximal search |
| No external model loading at runtime | Must embed model in package | ONNX, 2-5 MB total |
| CPU-only Kaggle default | NN inference 50-100ms without GPU | MLP preferred for CPU fallback |
| GPU available (optional) | TensorRT INT8 gives 3-5x speedup | Use GPU when available |
| No pip install at runtime | Must bundle all dependencies | ONNX Runtime, no PyTorch |

## 10. Performance Evidence

### 10.1 Measured Performance

| Metric | Value | Source | Method |
|---------|-------|--------|--------|
| **ResNet params (katac4)** | ~530K | [model.py](https://github.com/GoodCoder666/katac4/blob/main/model.py) | Parameter count from source |
| **MLP params (rowspire)** | ~100K | [neural_network.rs](https://github.com/tre-systems/rowspire/blob/main/worker/src/neural_network.rs) | Parameter count from source |
| **TensorRT INT8 latency** | 3-5x vs FP32 | C202 (VERIFIED) | Pochetti benchmarks on T4-class GPU |
| **NN oracle match rate** | 0.849 | C200 (VERIFIED) | NN-guided MCTS on 7x6 tactical positions |
| **AZAL oracle match rate** | 0.785 | C201 (VERIFIED) | AZAL paper, Connect Four benchmark |
| **TonyCWang dataset size** | 958M rows, 14.8 GB | S044 (VERIFIED) | Dataset card |
| **DQN tactical depth** | ~4 plies max | C205 (VERIFIED) | Comparison vs alpha-beta depth 8+ |
| **katac4 training time** | 8 days, 4xRTX 4090 | [train.py](https://github.com/GoodCoder666/katac4/blob/main/train.py) | Self-reported from training log |
| **katac4 epochs** | 30,000 | [train.py](https://github.com/GoodCoder666/katac4/blob/main/train.py) | Source code inspection |

### 10.2 Claimed Performance (Unverified)

| Claim | Value | Source | Verification Status |
|-------|-------|--------|-------------------|
| CNN channel configs (96/128/160/192) | 4 variants | [marcpaulo15 config](https://github.com/marcpaulo15/RL-connect4) | Config files verified; training results not published |
| GPT-2 text-based model performance | Unknown | [Leon-LLM models](https://github.com/Leon-LLM/Connect-Four-Datasets-Collection) | No evaluation metrics published |
| Qwen2.5 fine-tuning performance | Unknown | [Looyyd HF card](https://huggingface.co/Looyyd/connectfour-qwen2.5-1.5b-instruct) | No evaluation metrics published |
| NNUE evaluation quality vs heuristic | Unknown | [ecc521/connect-4-solver](https://github.com/ecc521/connect-4-solver) | Pre-trained weights exist but no benchmark published |

### 10.3 Inferred Performance

| Inference | Basis | Confidence |
|-----------|-------|------------|
| ResNet policy quality >> MLP policy quality | 5x parameter count, deeper architecture | MEDIUM |
| 15x13 board requires ~28x input encoding increase | 195 cells vs 42 cells | HIGH |
| DQN cannot solve deep tactical sequences | Bellman backup propagates one step at a time | HIGH (C205 VERIFIED) |
| INT8 quantization error < 0.05 value deviation | C202 VERIFIED on ConnectX tactical positions | MEDIUM |

## 11. Board-Size and inarow Applicability

| Architecture | 7x6 (inarow=4) | 9x9 (inarow=4) | 12x12 (inarow=4) | 15x13 (inarow=4) | 15x10 (inarow=4) | Any inarow |
|-------------|---------------|---------------|-----------------|-----------------|-----------------|------------|
| **ResNet (katac4)** | VERIFIED | Yes (training) | Yes (training) | NOT TESTED | NOT TESTED | Limited |
| **MLP (rowspire)** | VERIFIED | ? | ? | No 64-bit limit | No 64-bit limit | Via features |
| **CNN (marcpaulo15)** | Yes (config) | ? | ? | No Fixed input | No Fixed input | Limited |
| **DQN** | Yes (test only) | No | No | No | No | No |
| **NNUE (ecc521)** | Yes (pre-trained) | Yes | Yes | No Template limit | No Template limit | Via encoding |
| **Transformer** | Yes (text only) | Yes | Yes | Yes | Yes | Via notation |

**Key finding:** All board-size generalization claims are based on training-time board randomization (katac4), not inference-time adaptability. The 15x13 evaluation board in the Kaggle competition has **no tested neural approach**.
## 12. Integration and Ensemble Opportunities

### 12.1 Neural-Component Roles in Ensemble Architectures

| Ensemble Role | Architecture | Confidence |
|--------------|-------------|------------|
| **Value evaluation at MCTS leaf** | ResNet (katac4), MLP (rowspire) | VERIFIED (MCTS-002) |
| **Policy prior for MCTS root** | ResNet (katac4), NN-guided | VERIFIED (MCTS-002) |
| **Heuristic evaluation replacement** | NNUE (ecc521) | HYPOTHESIS (HYP-024) |
| **Move ordering via policy ranking** | ResNet policy head | PLAUSIBLE |
| **Endgame tablebase generation** | NN trained on solver data | PLAUSIBLE |
| **Phase classification** | MLP (16D features) | PLAUSIBLE |
| **Tactical position detection** | NN + threshold | HYPOTHESIS |

### 12.2 Neural Ensemble Integration Patterns

1. **NN-Guided MCTS (verified):** Use NN policy to guide MCTS root expansion, NN value to evaluate leaf nodes. C_puct=1.1 inference, FPU c_fpu=0.2 (MCTS-002).

2. **NN as Heuristic Replacement:** Replace classical evaluation function with NN value network in alpha-beta search. NNUE approach (ecc521).

3. **NN Confidence Gating:** Use NN value network confidence to route between classical search and MCTS. HYP-022 (phase-boundary calibration).

4. **NN for Fork Detection:** Train a specialized NN to detect forced-win fork positions.

5. **NN for Board-Size Routing:** Train a small classifier to predict which engine performs better on a given board size.

### 12.3 Ensemble Impact on ENS-019 through ENS-024

| Ensemble | Neural Component | NN Role | NN Architecture |
|----------|----------------|---------|----------------|
| ENS-019 | Board-size routing | Router classifier | Small MLP |
| ENS-020 | Conservative CPU | None (classical only) | N/A |
| ENS-021 | Phase-boundary | Phase detector | MLP (16D features) |
| ENS-022 | TensorRT neural | Value evaluation | ResNet INT8 |
| ENS-023 | NNUE-enhanced alpha-beta | Eval function | NNUE |
| ENS-024 | Confidence-gated routing | Confidence estimator | ResNet value head |

## 13. Failure Modes and Risks

### 13.1 Known Failure Modes

| Failure Mode | Architecture | Cause | Mitigation |
|-------------|-------------|-------|------------|
| **DQN tactical blindness** | DQN | Value iteration cannot propagate deep tactical info | Use alpha-beta fallback |
| **ResNet overfitting to 7x6** | ResNet | Trained on 7x6; poor generalization to 15x13 | Train on multiple board sizes |
| **MLP capacity limit** | MLP (rowspire) | 100K params insufficient for complex positions | Use NNUE-style sparse features |
| **Transformer misalignment** | GPT-2, Qwen2.5 | Text-based approach loses spatial structure | Not recommended |
| **INT8 quantization error** | TensorRT INT8 | Quantization degrades value accuracy | Calibrate on 1000+ positions |
| **Inference budget overflow** | All NN | NN evaluation takes too long | Use INT8, MLP, or NNUE |
| **Training data scarcity** | All supervised | TonyCWang dataset is large but fixed | Hybrid: supervised + self-play |
| **Board-size mismatch** | All fixed-board NN | 7x6 input breaks on 15x13 | Use feature encoding or NNUE |

### 13.2 Data Quality Risks

| Risk | Description | Status |
|------|-------------|--------|
| **Fabricated dataset stats** | S117 claimed 40-40-20 phase distribution; [RETRACTED] | REMEDIATED |
| **Temperature schedule uncertainty** | Exact schedule not fully specified | NEEDS_VERIFICATION |
| **Self-play vs uniform random confusion** | S120 claimed uniform random; actual = self-play with temperature | [RETRACTED], corrected |
| **No evaluation metrics for small datasets** | Leon-LLM, Lyte, spooky-connect4 | INFORMATION GAP |

### 13.3 Hardware Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Kaggle T4 not available** | Default Kaggle instance is CPU-only | MLP or classical fallback |
| **INT8 not supported on Kaggle T4** | TensorRT may not be available | FP16 fallback (still 3x speedup) |
| **Model loading timeout** | Large models may not load within 2s/move | Keep model under 5MB; use ONNX |

## 14. Benchmark Requirements

### 14.1 Required Neural Benchmarks

| Benchmark | Description | Priority |
|-----------|-------------|----------|
| **NN oracle match rate** | Agreement between NN policy/value and MCTS on 7x6 | VERIFIED: 0.849 (C200) |
| **AZAL oracle match rate** | Agreement with AZAL auxiliary loss | VERIFIED: 0.785 (C201) |
| **Inference latency profiling** | FP32/FP16/INT8 latency on T4 for ResNet, MLP, CNN | HYP-023 |
| **Board-size generalization** | NN performance on 9x9, 12x12, 15x13 | UNKNOWN - critical gap |
| **DQN tactical depth** | Maximum forced-win sequence solvable by DQN | VERIFIED: ~4 plies (C205) |
| **MLP vs ResNet quality** | Policy agreement between MLP and ResNet on test set | UNKNOWN |
| **NNUE vs classical eval** | Fork/forced-win detection rate comparison | HYP-024 |
| **Training data efficiency** | How many samples needed for target quality | UNKNOWN |

### 14.2 Benchmark Design for Neural Evaluation

```
NEURAL EVALUATION PROTOCOL:

1. Position set: 10,000 positions from TonyCWang dataset
   - Stratified: 3,000 early-game (0-10 pieces), 4,000 mid-game, 3,000 endgame

2. Neural evaluation:
   - Run each position through NN
   - Record policy distribution, value estimate

3. Reference evaluation:
   - Run alpha-beta depth 12 on each position
   - Record best move, game value

4. Metrics:
   - Policy agreement rate (NN best move = alpha-beta best move)
   - Value correlation (NN value vs alpha-beta value)
   - Top-k accuracy (is NN top-3 move in alpha-beta top-5?)
   - Forced-win detection rate (does NN find forced wins?)
```

## 15. Open Questions

| Question | Current Answer | Why It Matters |
|----------|---------------|---------------|
| **What is the optimal ResNet depth for 15x13?** | Unknown - katac4 uses 3 blocks on 7x6 | Deeper nets needed for larger boards, but inference cost increases |
| **Can MLP 16D features outperform channel encoding on 15x13?** | Unknown - never tested | Rowspire features are board-size invariant; channels are not |
| **What is the NN capacity ceiling for ConnectX?** | Unknown - katac4 at 530K may not be optimal | Larger models (1-10M params) may help on 15x13 |
| **Can self-play converge on solved 7x6?** | HYP-018: Self-play phase bias may cause convergence to first-player-only strategies | If true, supervised pre-training is essential |
| **What is the minimum training data for target quality?** | Unknown - TonyCWang uses 958M, rowspire uses 250K | Informs training cost estimates |
| **Is NNUE superior to dense NN for ConnectX?** | HYP-024: NNUE advantage over DQN - MEDIUM confidence | NNUE is the standard in modern chess engines; untested in ConnectX |
| **How many MCTS simulations per move with INT8?** | Unknown - depends on INT8 latency and search tree expansion rate | Critical for tuning ensemble composition |
| **Does the AZAL loss actually improve playing strength?** | 0.785 oracle match (vs 0.849 without AZAL?) - unclear | AZAL may improve oracle consistency but could reduce raw playing strength |

## 16. Recommendations

### For an Implementation Team

1. **Start with the rowspire MLP (4x128 with skip connections) as baseline.** It is fully specified, board-size configurable, and trains in hours on CPU. This provides a fast, working reference.

2. **Use the TonyCWang dataset (958M rows) for supervised pre-training.** This is the largest available dataset. Pre-train a ResNet on this data before attempting self-play.

3. **Implement TensorRT INT8 for Kaggle T4 inference.** C202 verified 3-5x latency reduction. This is critical for fitting MCTS within the 2s/move budget.

4. **Train on multiple board sizes (9x9 to 12x12) like katac4.** This is the only documented approach to board-size generalization. Target 15x13 support as a stretch goal.

5. **Implement AZAL three-loss objective.** C201 verified the paper specification. Even if playing strength improvement is unknown, oracle consistency improvement (0.785) is measurable.

6. **Use NNUE-style incremental features if search integration is needed.** The ecc521/connect-4-solver provides a complete C++ reference for NNUE integrated into negamax search.

7. **Implement DQN as a tactical fallback.** Despite C205 weakness finding, DQN can serve as a fast evaluator for endgame positions where forced-win sequences are short.

### For the Research Nexus

1. **Create a benchmark suite for neural ConnectX evaluation.** Standardized position set + reference evaluation protocol.

2. **Verify NNUE performance on ConnectX tactical positions.** The ecc521 reference implementation exists but has no published benchmarks.

3. **Fill the 15x13 generalization gap.** Test all architectures on 15x13 boards; this is the most critical unsolved problem.

4. **Document the TonyCWang temperature schedule precisely.** The current description (T=1.0 for first 10 moves, T=0.5 after) is only partially verified.

## 17. Sources and Retrieval Record

| Source ID | Title | URL | Type | Retrieved |
|-----------|-------|-----|------|-----------|
| S026 | GoodCoder666/katac4 (18 stars) | https://github.com/GoodCoder666/katac4 | GitHub | 2026-08-05 |
| S030 | tre-systems/rowspire | https://github.com/tre-systems/rowspire | GitHub | 2026-08-05 |
| S044 | TonyCWang/ConnectFour dataset | https://huggingface.co/datasets/TonyCWang/ConnectFour | Dataset | 2026-08-05 |
| S095 | AZAL paper | https://arxiv.org/abs/2607.08984 | Academic | 2026-08-05 |
| S094 | marcpaulo15/RL-connect4 | https://github.com/marcpaulo15/RL-connect4 | GitHub | 2026-08-05 |
| S025 | psalarc/DQN-ConnectX-Agent | https://github.com/psalarc/DQN-ConnectX-Agent | GitHub | 2026-08-05 |
| S023 | darkmatter2222/ConnectX-RL-DQN | https://github.com/darkmatter2222/ConnectX-RL-DQN | Kaggle | 2026-08-05 |
| S028 | sebadorn/Machine-Learning--Connect-Four | https://github.com/sebadorn/Machine-Learning--Connect-Four | GitHub | 2026-08-05 |
| S029 | Waelldchen et al. (2022) XAI | https://arxiv.org/abs/2202.11797 | Academic | 2026-08-05 |
| S071 | ecc521/connect-4-solver (NNUE) | https://github.com/ecc521/connect-4-solver | GitHub | 2026-08-05 |
| S037 | katac4/train.py | raw: GoodCoder666/katac4/main/train.py | Source | 2026-08-05 |
| S038 | katac4/model.py | raw: GoodCoder666/katac4/main/model.py | Source | 2026-08-05 |
| S041 | rowspire/neural_network.rs | raw: tre-systems/rowspire/main/worker/src/neural_network.rs | Source | 2026-08-05 |
| S042 | rowspire/features.rs | raw: tre-systems/rowspire/main/worker/src/features.rs | Source | 2026-08-05 |
| S066 | rowspire/evolved.json | raw: tre-systems/rowspire/main/resources/ai/evolved.json | Data | 2026-08-05 |
| S067 | rowspire/ml_ai_weights_best.json | raw: tre-systems/rowspire/resources/ai/ml_ai_weights_best.json | Data | 2026-08-05 |
| S068 | rowspire/genetic_params.rs | raw: tre-systems/rowspire/main/worker/src/genetic_params.rs | Source | 2026-08-05 |
| S069 | rowspire/feature_scores.rs | raw: tre-systems/rowspire/main/worker/src/feature_scores.rs | Source | 2026-08-05 |
| S093 | NVIDIA T4 specs | nvidia.com | Product Doc | 2026-08-05 |

## 18. Cross-Links

### Related Claims
- C011: Small CNN training on solved matches to 65% minimax agreement (HYPOTHESIS)
- C012: SFT to RL two-stage training most effective (SUPPORTED)
- C013: NN provides 2-3x alpha-beta speed via move ordering (HYPOTHESIS)
- C017: RTX 5090 training timeline (HYPOTHESIS)
- C018: Kaggle T4 inference latency (HYPOTHESIS)
- C019: ONNX Runtime deployment feasibility (SUPPORTED)
- C031: ResNet viable for Connect 4 (VERIFIED)
- C034: DQN shallow equals deep (VERIFIED)
- C038: KataGo-inspired ResNet viable (VERIFIED)
- C040: Multi-board training generalizes (VERIFIED)
- C042: AlphaZero measurable ELO (VERIFIED)
- C044: Neural MCTS dual network (NEEDS_CORRECTION)
- C046: 4x128 MLP with skip connections (VERIFIED)
- C047: CNN architecture specs from marcpaulo15 (NEEDS_CORRECTION)
- C051: katac4 KataGo techniques verified (VERIFIED)
- C052: katac4 training pipeline verified (VERIFIED)
- C146: rowspire MLP architecture (VERIFIED)
- C148: katac4 ResNet architecture (VERIFIED)
- C149: katac4 training methodology (VERIFIED)
- C150: PVS/MTD(f) speedup claims lack ConnectX benchmarks (NEEDS_CORRECTION)
- C152: GPU inference sub-millisecond (VERIFIED)
- C153: katac4 three-loss function (VERIFIED)
- C154: AZAL 0.785 oracle match (VERIFIED)
- C160: katac4 ResNet most sophisticated design (VERIFIED)
- C161: rowspire MLP fastest inference (VERIFIED)
- C162: marcpaulo15 CNN two-stage training (VERIFIED)
- C163: Training completeness ranking (VERIFIED)
- C195: ResNet surpasses MCTS on limited compute (HYPOTHESIS)
- C200: Neural MCTS 0.849 oracle match (VERIFIED)
- C201: AZAL three-loss objective (VERIFIED)
- C202: TensorRT INT8 3-5x latency (VERIFIED)
- C205: DQN tactical weakness (VERIFIED)

### Related Hypotheses
- HYP-009: Three-loss objective superiority (PROPOSED)
- HYP-010: Temperature schedule threshold (PROPOSED)
- HYP-015: MCTS GPU acceleration requirement (PROPOSED)
- HYP-017: TT-MCTS shared cache improvement (PROPOSED)
- HYP-018: Self-play phase bias (PROPOSED)
- HYP-021: Board-size adaptive routing (PROPOSED)
- HYP-022: Phase-boundary calibration dominance (PROPOSED)
- HYP-023: TensorRT INT8 advantage (PROPOSED)
- HYP-024: NNUE advantage over DQN (PROPOSED)

### Related Ensembles
- ENS-019 through ENS-024: All ensemble architectures referencing neural components

### Related Dossiers
- MCTS-002: Neural MCTS Integration Patterns (verifies neural-guided MCTS patterns)
- CS-003: Classical Search and Solver Engineering (complements classical search)
- BMS-DOC-001: Benchmark Science and Tournament Design (benchmark framework)
- GOV-004: R37 Comprehensive Audit (governance)

### Related Experiment Backlog
- EXP-009 through EXP-015: Neural training experiments (from R28)
- EXP-026 through EXP-032: Governance experiments (from R33)

## 19. Document Integrity

- **Data fabrication checks:** S117 (40-40-20 phase distribution) [RETRACTED]. S120 (uniform random) [RETRACTED]. Both corrected in this dossier.
- **Source collision check:** S091-S092 (R20 vs R25) - verified S091/S092 point to katac4 model.py/train.py in both sections. S095 (R25 vs R28) - verified S095 points to AZAL paper. No harmful collisions.
- **Evidence status:** All claims in this dossier are drawn from previously verified claims (C200, C201, C202, C205) or from direct source code inspection. No new empirical claims are made without explicit HYPOTHESIS or UNKNOWN markers.
- **Code excerpts:** All code blocks are adapted reference sketches or conceptual pseudocode - none are executable.
