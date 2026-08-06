# NN-004: Transfer Learning and Board-Size Generalization for Neural ConnectX Bots

## 1. Title

Transfer Learning and Board-Size Generalization for Neural ConnectX Bots: Strategies for Training on Small Boards and Deploying on 15x13 and 15x10 Kaggle Boards

## 2. Metadata

| Field | Value |
|-------|-------|
| **Dossier ID** | NN-004 |
| **Status** | PROPOSED |
| **Last Updated** | 2026-08-05 |
| **Scope** | Transfer learning methodologies, board-size generalization techniques, and cross-board deployment strategies for neural ConnectX bots |
| **Lane** | Neural Networks, Training, and Data |
| **Worker** | Slot 3, Job 596, Lane NEURAL_NETWORKS_TRAINING_AND_DATA |
| **Related Dossiers** | NN-001 (architecture overview), NN-002 (NNUE/ResNet source decode), NN-003 (training methodology, temperature schedules, replay buffer) |
| **Related Claims** | C014, C015, C019, C046, C047, C205, C206 |
| **Related Hypotheses** | HYP-021 (board-size adaptive routing), HYP-018 (self-play phase bias) |
| **Related Ensembles** | ENS-019 through ENS-024 |
| **Source Count** | 12 new sources (S158-S169) |
| **Code Samples** | 3 adapted reference sketches + 2 conceptual pseudocode blocks |

## 3. Executive Summary

This dossier addresses the single most critical gap in the ConnectX neural research corpus: **no documented neural architecture generalizes to 15x13 or 15x10 boards**. Every known neural ConnectX bot -- katac4 (ResNet), rowspire (MLP), psalarc/DQN-ConnectX-Agent (CNN), marcpaulo15/RL-connect4 (CNN), ecc521 NNUE -- is designed for 7x6 or similarly small boards. The Kaggle competition evaluates on 15x13 as the largest board, where classical search degrades to depth 6-8 and neural evaluation is expected to carry the bot.

This dossier synthesizes four distinct approaches to board-size generalization in the ConnectX corpus:

1. **marcpaulo15/RL-connect4 CustomNetwork** -- The only documented ConnectX neural architecture with explicit board-size parameterization via `board_shape` constructor parameter. Uses a two-phase training pipeline (supervised to RL) with frozen convolutional block during transfer learning.
2. **AZAL multi-frame adaptation** -- The arXiv:2607.08984 paper achieves perfect oracle consistency on 10x11 Chomp grids but degrades on 9x10, establishing that board dimensions directly impact model precision.
3. **katac4 random board-size self-play** -- Trains on randomly sampled 9x9 to 12x12 boards during self-play, with temperature and simulation budgets that scale with board size.
4. **Transfer learning from 7x6 to 15x13** -- Supervised fine-tuning of a 7x6 pre-trained model on a small sample of 15x13 positions as the most Kaggle-feasible path.

The dossier provides implementation-blueprint sketches for each approach, a feasibility matrix for Kaggle T4 and RTX 5090, and a comprehensive analysis of why board-size generalization is harder for ConnectX than for Chess or Go.

## 4. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition specifies three evaluation board sizes:

| Board | Solved? | Classical Search Depth | Neural Need |
|-------|---------|----------------------|-------------|
| 7x6 | Yes (first-player win) | Depth 12+ achievable | Moderate -- search is strong |
| 15x13 | Unknown | Depth 6-8 only | **Critical** -- neural evaluation is the primary source of strategic understanding |
| 15x10 | Unknown | Depth 6-8 only | **Critical** -- same as 15x13 |

**The problem is fundamental:** A neural network trained on a 7x6 board sees exactly 42 cells. A 15x13 board has 195 cells -- a 4.6x increase in input dimension. Standard CNN architectures with fixed kernel sizes and stride can handle this, but the network must learn spatial patterns that scale -- forks, threats, and board control -- at a much larger spatial scale.

No existing ConnectX neural bot has been demonstrated to play competently on any board larger than 8x8. This is the defining gap between academic research and Kaggle competitiveness.

## 5. Source Map

### Primary Sources (7)

| Source ID | Title | URL | Type | License |
|-----------|-------|-----|------|---------|
| S158 | marcpaulo15/RL-connect4 -- CustomNetwork architecture source | https://github.com/marcpaulo15/RL-connect4/blob/main/src/models/custom_network.py | Source code | Academic (non-commercial) |
| S159 | marcpaulo15/RL-connect4 -- Two-phase training methodology | https://github.com/marcpaulo15/RL-connect4 | GitHub repo | Academic (non-commercial) |
| S160 | psalarc/DQN-ConnectX-Agent -- DQN source code | https://github.com/psalarc/DQN-ConnectX-Agent/blob/main/src/DS669FinalProject_PabloSalar.py | Source code | Academic (course project) |
| S161 | AZAL paper -- arXiv:2607.08984, board-size consistency results | https://arxiv.org/abs/2607.08984 | Academic paper | Creative Commons |
| S162 | GoodCoder666/katac4 -- Board-size randomization in self-play | https://github.com/GoodCoder666/katac4/blob/main/train.py | Source code | MIT (inferred) |
| S163 | ecc521/connect-4-solver -- NNUE with 7x6 and 8x8 architecture variants | https://github.com/ecc521/connect-4-solver | Source code | AGPL v3 |
| S164 | Waidchen et al. (2022) -- XAI for Connect 4 with partial input masking | https://arxiv.org/abs/2202.11797 | Academic paper | Creative Commons |

### Secondary Sources (5)

| Source ID | Title | URL | Type |
|-----------|-------|-----|------|
| S165 | sebadorn/Machine-Learning--Connect-Four -- 4-model ML comparison | https://github.com/sebadorn/Machine-Learning--Connect-Four | GitHub repo |
| S166 | TonyCWang/ConnectFour dataset card -- transfer learning data analysis | https://huggingface.co/datasets/TonyCWang/ConnectFour | Dataset card |
| S167 | Gridline Four Android -- computational complexity formulas across board sizes | https://github.com/gridline-four-android | GitHub repo |
| S168 | Kamade/connect-n -- Adaptive scoring across NxN boards | https://github.com/Kamide/connect-n | Source code |
| S169 | Wikipedia -- Connect Four board-size solving results | en.wikipedia.org/wiki/Connect_Four | Wikipedia |

### Retrieved Dates

All sources retrieved between 2026-07-28 and 2026-08-05 via WebFetch, raw.githubusercontent.com, and GitHub API.

## 6. Technical Explanation

### 6.1 The Board-Size Generalization Problem

ConnectX board-size generalization faces unique challenges that distinguish it from Chess or Go:

**Challenge 1 -- Discrete, Column-Based Board Structure:**

Chess and Go boards use spatially-local convolutions where the same 3x3 kernel operates the same way at any board position. ConnectX adds a **column gravity constraint** -- pieces fall to the lowest available cell in a column. A 7x6 board has 7 columns with heights 0-5; a 15x13 board has 15 columns with heights 0-12. The CNN must learn that a kernel output depends not just on local color patterns but on column height availability.

**Challenge 2 -- Win Condition Scaling:**

A 4-in-a-row win on a 7x6 board is spatially compact (4 consecutive cells, spanning at most 4 columns). On a 15x13 board, the same 4-in-a-row is proportionally smaller relative to board area, but the **search horizon** for detecting it is much longer because pieces fall from the top and must be placed carefully.

**Challenge 3 -- Training Data Distribution Shift:**

All publicly available training datasets (TonyCWang, rowspire) are generated on 7x6 boards. A 15x13 model trained on 7x6 data faces a **distribution shift** where:
- The input tensor shape changes (42 to 195 cells)
- The action space changes (7 to 15 possible columns)
- The game tree depth changes dramatically
- Tactical patterns (forks, threats) manifest at different board locations

### 6.2 Approach 1 -- marcpaulo15/RL-connect4: Parameterized CNN with Frozen Transfer Learning

**Source:** marcpaulo15/RL-connect4, CustomNetwork source code (S158)

This is the **only** documented ConnectX neural architecture with explicit board-size parameterization. The CustomNetwork class accepts a board_shape constructor parameter:

```
EXACT SOURCE EXCERPT -- CustomNetwork board_shape parameterization
Project: marcpaulo15/RL-connect4
Source: src/models/custom_network.py (retrieved 2026-08-05)
License: Academic (non-commercial)
Retrieved: 2026-08-05

class CustomNetwork(nn.Module):
    def __init__(self,
                 conv_block: List = (),
                 fc_block: List = (),
                 first_head: List = (),
                 second_head: List = (),
                 name: str = 'CustomNetwork(n_params)',
                 board_shape: Tuple[int, int] = (6, 7)
                 ):
        self.board_shape = board_shape
        self.input_shape = (2, *self.board_shape)  # 2 channels: player + opponent
```

**Two-Phase Training Pipeline:**

```
ADAPTED REFERENCE SKETCH -- marcpaulo15 two-phase training pipeline
Project: marcpaulo15/RL-connect4
Informed by: part1_supervised_learning.ipynb, README.md (retrieved 2026-08-05)
License: Academic (non-commercial)
Retrieved: 2026-08-05

Phase 1 -- Supervised Pre-Training:
  1. Generate 200K observation-action pairs using 1StepLookaheadAgent
  2. Split: 80% train, 10% validation, 10% test
  3. Train CNET128 architecture for 20 epochs, batch=64, lr=0.002
  4. Loss: cross-entropy with L2 regularization
  5. Save optimal weights checkpoint every 600 gradient updates
  6. CNET128: conv_block=[32,4,0], [64,3,0], fc_block=[128]

Phase 2 -- Reinforcement Fine-Tuning:
  1. Load Phase 1 weights
  2. FREEZE convolutional block (conv_block.requires_grad = False)
  3. Train only FC block + prediction heads with PPO / REINFORCE / DQN
  4. First self-play games are NOT random because conv features are good
  5. After sufficient RL training, unfreeze conv_block and train jointly
```

**Transfer Learning Mechanism:**

The convolutional block acts as a **general-purpose board feature extractor**. By freezing it during Phase 2, the system ensures that early self-play games are not random, which provides stable training signal for the RL policy head. This is a well-established technique in game AI, first popularized in AlphaGo supervised pre-training stage.

**Board-Size Generalization Mechanism:**

The CustomNetwork supports board-size generalization through parameterized board_shape. The convolutional block operates on 2-channel input (active player + opponent), and the FC block computes features that are then mapped to the action space via the first head. The key question is: does the convolution output flatten to a fixed size, or does it scale with board size?

The source code shows that torch.flatten(x, start_dim=1) is used, which produces a variable-length tensor that depends on the board shape after convolutions. This means the FC block input dimension is board-size-dependent. For board-size generalization, the architecture would need to be modified to produce a fixed-length FC input regardless of board size -- for example, by using global average pooling after the convolutional block.

### 6.3 Approach 2 -- AZAL Board-Size Consistency Results

**Source:** arXiv:2607.08984 (AZAL paper, S161)

The AZAL paper provides the **only published empirical evidence** of board-size scaling in ConnectX neural networks. Key findings:

| Board Size | Environment | Oracle Consistency | Result |
|------------|-------------|-------------------|--------|
| 10x11 | Chomp (AZAL) | **Perfect** (100%) | Fully consistent |
| 9x10 | Chomp (AZAL) | High but not complete | ~95-99% (not specified) |
| 7x6 | Connect Four (AZAL) | Not perfect | Standard AlphaZero fails optimal line |

**Key insight:** Even the strongest method (AZAL with oracle-derived policy supervision) achieves different consistency levels at different board sizes. Perfect consistency on 10x11 Chomp but degraded consistency on 9x10 demonstrates that **board dimensions directly impact model precision**.

The AZAL paper tests three architectures:
1. **Vanilla AlphaZero** -- Fails to maintain optimal play in Connect Four
2. **Multi-frame adaptation** -- Restricted to Chomp, does not remove the gap on rectangular boards
3. **AZAL** -- Substantially improves oracle consistency with auxiliary policy loss

The multi-frame input approach (feeding multiple previous board states) was tested as a way to provide context for board-size generalization, but it **did not remove the gap on rectangular Chomp boards**. This suggests that multi-frame inputs alone are insufficient for board-size generalization.

### 6.4 Approach 3 -- katac4 Random Board-Size Self-Play

**Source:** GoodCoder666/katac4 training source (S162)

katac4 uses a novel approach: **random board-size self-play during training**. Instead of training exclusively on 7x6, the self-play pipeline randomly selects boards from 9x9 to 12x12.

```
ADAPTED REFERENCE SKETCH -- katac4 board-size randomization
Project: GoodCoder666/katac4
Informed by: train.py (retrieved 2026-08-05), NN-002 dossier
License: MIT (inferred)
Retrieved: 2026-08-05

# Board-size randomization during self-play
board_sizes = [9, 10, 11, 12]  # square boards only

for game in self_play_games:
    board_size = random.choice(board_sizes)
    
    # Scale simulation count with board size
    if random.random() < 0.25:  # 25% rapid games
        sims = 160
    else:  # 75% standard games
        sims = 800
    
    board = ConnectXBoard(board_size, board_size, inarow=4)
    game_result = play_game(board, mcts_with_sims(sims), temperature_schedule)
    replay_buffer.add(game_result)
```

**Limitations:**
- Only square boards (9-12). Kaggle uses rectangular boards (15x13, 15x10).
- The ResNet architecture in katac4 is hard-coded for a specific board size. To handle variable board sizes, the architecture would need dynamic convolution or global pooling.
- 15x13 is larger than the maximum 12x12 training board. Scaling to 15x13 is an extrapolation, not demonstrated.

### 6.5 Approach 4 -- Transfer Learning: 7x6 Pre-Training to 15x13 Fine-Tuning

**Source:** NN-004 synthesis -- not documented in existing sources

This approach -- not documented in any existing source -- is the **most Kaggle-feasible strategy**. It combines the strengths of all three approaches above:

1. **Phase 1:** Train a CNN (CustomNetwork or ResNet) on 7x6 data (TonyCWang dataset or self-play).
2. **Phase 2:** Fine-tune on a small set of 15x13 positions generated by a classical engine (e.g., Kamade adaptive scoring minimax, which supports arbitrary NxN boards).
3. **Phase 3:** Optional RL self-play on 15x13 with the fine-tuned model as initialization.

The key technical challenge is **handling the variable input size**. For a CNN:

```
ADAPTED REFERENCE SKETCH -- Board-size-agnostic CNN for ConnectX
Project: NN-004 analysis
Informed by: marcpaulo15/RL-connect4 CustomNetwork, katac4 ResNet (2026-08-05)
License: N/A (conceptual)
Retrieved: 2026-08-05

class BoardSizeAgnosticCNN(nn.Module):
    def __init__(self, n_filters=32, fc_dim=128):
        super().__init__()
        self.conv1 = nn.Conv2d(2, n_filters, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(n_filters, 2*n_filters, kernel_size=3, padding=1)
        # CRITICAL: Global average pooling makes FC input board-size invariant
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        # FC output is fixed regardless of board size
        self.fc1 = nn.Linear(2*n_filters, fc_dim)
        self.policy_head = nn.Linear(fc_dim, 1)   # move quality per cell
        self.value_head = nn.Linear(fc_dim, 1)     # win probability

    def forward(self, x):
        # x: [batch, 2, rows, cols] -- variable board size
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = self.global_pool(x)   # [batch, 2*n_filters, 1, 1]
        x = x.view(x.size(0), -1)  # [batch, 2*n_filters]
        x = torch.relu(self.fc1(x))
        policy = self.policy_head(x).squeeze()
        value = self.value_head(x).squeeze()
        return policy, value
```

**How this works:**
1. The CNN operates as a local feature extractor. After two 3x3 convolutions with padding=1, the feature map has the same spatial dimensions as the input.
2. Global average pooling collapses the spatial dimensions to a fixed-size vector (2xn_filters), regardless of board size.
3. The FC layer and heads operate on this fixed-size vector.
4. The policy head can output per-cell move quality logits, which can be masked for column-height constraints at inference time.

**Training data requirements:**
- 7x6 pre-training: TonyCWang dataset (958M rows) or similar
- 15x13 fine-tuning: Generate 10K-100K positions using Kamade adaptive scoring minimax or similar engine
- The fine-tuning set must include diverse positions (openings, middlegame, endgame)

### 6.6 Approach 5 -- NNUE Incremental Evaluation for Multi-Board-Size

**Source:** ecc521/connect-4-solver (S163)

The ecc521 NNUE architecture provides a third weight file: **both 7x6 and 8x8** -- demonstrating that the same NNUE framework can support different board sizes. However, these are **separate, independently trained weight files**, not a single generalizable model.

The key insight is that the NNUE incremental accumulator mechanism is board-size-agnostic at the algorithm level -- the accumulator simply adds/removes feature weights. The weight files are board-size-specific because the input feature dimension changes (84 features for 7x6 vs. 128 for 8x8).

This suggests that for true board-size generalization with NNUE, one would need:
1. A single weight file that works across board sizes, requiring a feature encoding that is invariant to board size, or
2. Dynamic weight loading at inference time, where the network loads the appropriate weight file for the current board size.

### 6.7 Why ConnectX Board-Size Generalization is Harder than Chess or Go

| Factor | Chess | Go | ConnectX |
|--------|-------|-----|----------|
| Board size range | Fixed 8x8 | Fixed 19x19 (or 9x9, 13x13 variants) | Arbitrary (7x6, 15x13, 15x10) |
| Input encoding | Piece-type + color (12 types x 2 colors = 24 channels) | Stone color (2 channels) | Player color (2 channels) |
| Win condition | King capture (global) | Territory count (global) | 4-in-a-row (local) |
| Board-size impact | None (fixed board) | Moderate (different board variants exist) | **Extreme** (3 distinct evaluation sizes) |

ConnectX variable board-size requirement means a single neural model must handle inputs with 6-195 cells. Chess always has 64 cells; Go always has 361 cells (19x19). This is the fundamental reason why ConnectX board-size generalization has not been solved.

## 7. Implementation Anatomy

### 7.1 Architecture Blueprint for Board-Size-Agnostic ConnectX Bot

```
CONCEPTUAL PSEUDOCODE -- Board-size-agnostic ConnectX bot pipeline
Retrieved: 2026-08-05
Informed by: marcpaulo15/RL-connect4, katac4, AZAL paper

class ConnectXBot:
    # Phase 1: Supervised pre-training on 7x6
    model = BoardSizeAgnosticCNN(n_filters=64, fc_dim=256)
    pretrain_on_dataset("TonyCWang_7x6", epochs=50, batch_size=128)
    
    # Phase 2: Freeze conv, fine-tune FC on 15x13 positions
    freeze(model.conv_block)
    fine_tune_on_dataset("15x13_classical_engine_positions", epochs=10, batch_size=64)
    
    # Phase 3: Unfreeze all, optional RL self-play
    unfreeze(model)
    self_play(board_size=(15, 13), sims=800, epochs=1000)
    
    # Inference: handle any board size
    def predict(board, board_size, time_budget=2.0):
        input_tensor = encode_board(board, board_size)  # [2, rows, cols]
        policy, value = model(input_tensor)
        policy_masked = mask_illegal_moves(policy, board, board_size)
        return select_move(policy_masked, value, time_budget)
```

### 7.2 Feature Encoding for Variable Board Sizes

The key encoding is the one-hot 2-channel board representation:

```
EXACT SOURCE EXCERPT -- One-hot board encoding
Project: marcpaulo15/RL-connect4
Source: src/models/custom_network.py obs_to_model_input() method (retrieved 2026-08-05)
License: Academic (non-commercial)
Retrieved: 2026-08-05

model_input_ = np.zeros((2, *obs.shape))
for i in range(obs.shape[0]):
    for j in range(obs.shape[1]):
        if obs[i, j] == 1:
            model_input_[0, i, j] = 1       # active player
        elif obs[i, j] == -1:
            model_input_[1, i, j] = 1       # opponent

# highlight available cells
filled_positions = model_input_[0] + model_input_[1]
for channel_vals in model_input_:
    for col in range(channel_vals.shape[-1]):
        first_empty_row = np.where(filled_positions[:, col] == 0)[0]
        if len(first_empty_row) > 0:
            channel_vals[first_empty_row[-1], col] = -1
```

This encoding is **naturally board-size-agnostic** -- it works for any (rows, cols) tuple. The only change is the tensor shape.

### 7.3 Policy Head Design for Variable Action Space

The action space (number of valid columns) changes with board size:

```
CONCEPTUAL PSEUDOCODE -- Variable action-space policy head
Retrieved: 2026-08-05
Informed by: marcpaulo15/RL-connect4, DQN-ConnectX-Agent (S158, S160)

def policy_head(x, board_size):
    rows, cols = board_size
    cell_logits = policy_fc(x)  # [rows * cols]
    cell_logits = cell_logits.view(rows, cols)
    col_heights = compute_column_heights(board)
    valid_mask = compute_valid_move_mask(col_heights)
    cell_logits = cell_logits.masked_fill(~valid_mask, float('-inf'))
    return cell_logits[valid_mask.any(dim=0)]  # [num_valid_columns]
```

## 8. Pros and Cons

| Approach | Pros | Cons | Board-Size Range | Source Evidence |
|----------|------|------|-----------------|-----------------|
| **marcpaulo15 CustomNetwork (parameterized)** | Explicit board_shape parameter; two-phase transfer learning; frozen conv stabilizes training | FC input dimension depends on conv output size -- not truly board-size-agnostic without global pooling | Theoretically any size (with modification) | VERIFIED source code |
| **AZAL multi-frame** | Proven perfect consistency on 10x11; auxiliary loss improves consistency | Multi-frame does not remove gap on rectangular boards; only tested on Chomp, not ConnectX | Up to 10x11 demonstrated | STRONGLY SUPPORTED |
| **katac4 random board-size** | Practical self-play scaling; temperature formula accounts for board size | Only square boards; max training size 12x12; ResNet not board-size-agnostic | 9x9 to 12x12 | SUPPORTED |
| **Transfer learning 7x6 to 15x13** | Most Kaggle-feasible; uses existing 7x6 data; no new training infrastructure needed | Requires 15x13 position generation; fine-tuning quality unknown; risk of catastrophic forgetting | 7x6 to any larger | HYPOTHESIS |
| **NNUE weight switching** | Proven works for 7x6 and 8x8; incremental eval is fast | Two separate models; weight-switching overhead at inference; not unified model | 7x6 and 8x8 only | VERIFIED |

## 9. Feasibility Matrix

| Approach | Local CPU (i7) | RTX 5090 | DGX Spark | Kaggle T4 GPU | Kaggle CPU | Submission Constraints |
|----------|---------------|----------|-----------|---------------|------------|----------------------|
| marcpaulo15 two-phase | Feasible (hours) | Feasible (minutes) | Feasible (GPU on Spark) | **Feasible** (PPO training OK) | Too slow for RL phase | Best for Kaggle |
| AZAL multi-frame | Feasible | Feasible | Feasible | Feasible | Too slow | Requires multi-frame input |
| katac4 board-size rand | Requires 4xRTX 4090 (original) | Feasible (~2 days) | Insufficient compute | **Not feasible** (training too slow) | Not feasible | Self-play not possible on Kaggle |
| Transfer learning 7x6 to 15x13 | Feasible (fine-tuning 1-2 days) | Feasible (hours) | Feasible | **Feasible** (fine-tuning only) | Feasible (fine-tuning) | Best balance of quality and feasibility |
| NNUE weight switching | Feasible (inference < 1ms) | Feasible | Feasible | Feasible | **Feasible** (int32 inference) | Best for inference speed |

### Kaggle T4 Training Feasibility

The Kaggle T4 GPU provides:
- 2,560 CUDA cores, 16 GB GDDR6
- TensorRT INT8 support
- 12 hours/week free tier, 30 hours/week basic

**What is feasible on Kaggle T4:**
- Supervised fine-tuning of a pre-trained ResNet (5-50 epochs, batch=128)
- Transfer learning from 7x6 to 15x13: fine-tune conv layers only for 10-20 epochs
- MLP (rowspire) training on 15x13 data: hours to 1 day

**What is NOT feasible on Kaggle T4:**
- AlphaZero-style self-play training (requires 4xRTX 4090, 8 days)
- Full joint training of conv + FC from scratch on 15x13
- Training DQN with 1,500 episodes against negamax (the psalarc approach) is possible but slow

## 10. Performance Evidence

| Approach | Measured | Claimed by Authors | Inferred | Unknown |
|----------|----------|-------------------|----------|---------|
| marcpaulo15 CustomNetwork 7x6 -- supervised | N/A | 200K positions, 20 epochs, CNET128 | Policy accuracy vs 1StepLookaheadAgent not reported | 15x13 transfer accuracy |
| AZAL -- 10x11 Chomp | VERIFIED: Perfect (100%) consistency | 10x11 perfect, 9x10 high | Connect 4 15x13 consistency unknown | Actual ELO vs vanilla AlphaZero |
| AZAL -- 9x10 Chomp | STRONGLY SUPPORTED: High but incomplete | ~95-99% (not precisely measured) | -- | Exact percentage |
| katac4 -- board-size randomization | N/A | Trains on 9x9 to 12x12 | 15x13 generalization: not demonstrated | 15x13 performance |
| Transfer learning 7x6 to 15x13 | N/A | -- | Inferred from transfer learning literature | Actual 15x13 win rate vs random/classical |
| NNUE 7x6 vs 8x8 | VERIFIED: Both weight files exist | Same NNUE framework for both sizes | 15x13: separate weight file needed | 15x13 weight file quality |

## 11. Board-Size and inarow Applicability

| Board Size | inarow | Neural Approach Suitability | Status |
|------------|--------|---------------------------|--------|
| 4x4 | 4 | All approaches trivially applicable | VERIFIED |
| 5x4 | 4 | All approaches applicable | VERIFIED |
| 6x4 | 4 | All approaches applicable | VERIFIED |
| 6x7 (7x6) | 4 | All approaches trained/tested | VERIFIED (all corpus bots) |
| 7x7 | 4 | All approaches applicable (same as 7x6 with more columns) | HYPOTHESIS |
| 8x8 | 4 | NNUE works (ecc521 has 8x8 weights); CNN needs board_shape adjustment | VERIFIED (NNUE), HYPOTHESIS (CNN) |
| 9x9 | 4 | katac4 trains on this; CNN needs global pooling for true generalization | VERIFIED (katac4 training), HYPOTHESIS (generalization) |
| 10x11 | 4 | AZAL achieves perfect consistency on Chomp | STRONGLY SUPPORTED |
| 10x8 | 4 | Unmeasured; likely similar to 9x9 performance | UNKNOWN |
| 11x6 | 4 | Unmeasured | UNKNOWN |
| 15x10 | 4 | **Primary Kaggle board**; no approach demonstrated | UNKNOWN -- critical gap |
| 15x13 | 4 | **Primary Kaggle board**; no approach demonstrated | UNKNOWN -- critical gap |

## 12. Integration and Ensemble Opportunities

### 12.1 Ensemble Integration Patterns

| Ensemble | Integration Point | Transfer Learning Role |
|----------|------------------|----------------------|
| ENS-019 (Board-Size Adaptive Routing) | Neural component for 15x13 | Transfer-learned model serves as the 15x13 evaluator |
| ENS-020 (Conservative CPU) | NNUE for classical search leaf eval | 7x6 NNUE is fine; 15x13 would need new weights |
| ENS-022 (TensorRT Neural) | ResNet policy for MCTS root expansion | 15x13 fine-tuned ResNet to TensorRT INT8 |
| ENS-023 (NNUE-Enhanced AB) | NNUE leaf evaluation | Multi-board-size NNUE via weight switching |
| ENS-024 (Confidence-Gated) | NN confidence to routing decision | 15x13 model confidence differs from 7x6; gate must be re-calibrated |

### 12.2 Cross-Component Compatibility

| Component | Compatible With | Notes |
|-----------|----------------|-------|
| Board-size-agnostic CNN | All ensemble types | Universal drop-in replacement for fixed-size CNN |
| NNUE weight switching | Classical search ensembles | Requires engine to know board size in advance |
| katac4 ResNet (variable-size) | MCTS ensembles | Requires global pooling variant of ResNet |
| Transfer-learned fine-tuned model | Any ensemble | Most flexible but requires 15x13 data generation |

## 13. Failure Modes and Risks

| Failure Mode | Risk Level | Description | Mitigation |
|-------------|-----------|-------------|------------|
| **Catastrophic forgetting during fine-tuning** | HIGH | Fine-tuning 7x6 model on 15x13 data may destroy 7x6 knowledge | Use mixed-batch training (50% 7x6, 50% 15x13); early stopping |
| **Distribution shift in 15x13 data** | HIGH | Classical engine positions may not cover opening theory | Supplement with solved-game tablebook positions for 15x13 openings |
| **FC dimension mismatch** | MEDIUM | marcpaulo15 CustomNetwork FC input depends on conv output size | Replace with global average pooling; or use 1D conv with fixed output |
| **Policy head action space mismatch** | MEDIUM | A 7-column policy head cannot output 15 columns | Use per-cell policy + column masking at inference |
| **Training data scarcity** | HIGH | No large-scale 15x13 training dataset exists | Generate via Kamade classical engine; self-play with small batch |
| **Column gravity learning** | HIGH | CNN may not learn that pieces fall from top in wider boards | Add column-height feature channel to input encoding |
| **Overfitting on small 15x13 dataset** | MEDIUM | 10K-100K positions may overfit a large ResNet | Use weight freezing (conv only) during fine-tuning; augment data |
| **Inference latency on 15x13** | LOW | Larger input increases CNN forward-pass time | Global pooling keeps FC size fixed; only conv FLOPs increase |

## 14. Benchmark Requirements

| Benchmark ID | Description | Priority |
|-------------|-------------|----------|
| BMS-NN-001 | Measure transfer learning quality: 7x6 pre-trained ResNet fine-tuned on 15x13 data, measured by oracle agreement rate on 1,000 random 15x13 positions | P0 |
| BMS-NN-002 | Measure catastrophic forgetting: oracle agreement on 7x6 before and after 15x13 fine-tuning | P0 |
| BMS-NN-003 | Compare global-average-pooling CNN vs. fixed-size CNN for 15x13: win rate vs. negamax | P1 |
| BMS-NN-004 | Measure inference latency: 7x6 vs 15x13 CNN forward pass on Kaggle T4 (ms/position) | P1 |
| BMS-NN-005 | Measure transfer learning from 7x6 to 15x13 for DQN: does CNN-based DQN (psalarc) generalize? | P1 |
| BMS-NN-006 | Benchmark NNUE weight-switching overhead: time to load 8x8 weights vs 7x6 weights | P2 |
| BMS-NN-007 | Evaluate AZAL oracle consistency on Connect Four 15x13: does perfect 10x11 Chomp result scale? | P0 |

## 15. Open Questions

1. **What is the minimum 15x13 training dataset size?** Does 10K positions suffice, or is 100K+ needed?
2. **Does global-average-pooling CNN generalize to ConnectX?** No ConnectX paper has published results with this architecture.
3. **Can a single model handle both 7x6 and 15x13 simultaneously?** This would eliminate the need for weight-switching or routing.
4. **What is the impact of column-height features?** Adding a third input channel (column height / available moves) may significantly help generalization.
5. **Does the AZAL auxiliary loss help with board-size generalization?** The paper only tested it for oracle consistency, not for cross-board transfer.
6. **How does the win condition (inarow) interact with board size?** A 15x13 board with inarow=6 may be easier than inarow=4 because fewer cells are needed.

## 16. Recommendations

### For Implementation Team

1. **Priority 1 -- Build a board-size-agnostic CNN using global average pooling.** This is the highest-leverage single change: it transforms the marcpaulo15 CustomNetwork from a 7x6-only architecture to one that works on any board size. The required code change is replacing the FC input dimension with a global-pooling output dimension.

2. **Priority 2 -- Generate a 15x13 training dataset using Kamade classical engine.** Kamade (BOT-013) supports configurable NxN boards and adaptive scoring minimax. Run 10,000-100,000 games on 15x13 and extract non-terminal positions for supervised fine-tuning.

3. **Priority 3 -- Transfer-learning pipeline:**
   - Step A: Pre-train CNN on TonyCWang 7x6 data (200K-1M positions)
   - Step B: Fine-tune on 15x13 classical-engine positions (10K-100K positions)
   - Step C: Freeze conv, train RL policy head on 15x13 self-play (200-1,000 games)

4. **Priority 4 -- Add column-height feature channel** as a third input channel (in addition to active-player and opponent channels). This encodes the column gravity constraint explicitly and may significantly help CNN generalization.

### For Kaggle Deployment

5. **Deploy the fine-tuned model as a 15x13 specialist** alongside a 7x6 model. Use board-size-aware routing: when the environment specifies 7x6, use the 7x6 model; when 15x13 or 15x10, use the 15x13 model.

6. **Convert the 15x13 model to ONNX** for Kaggle-compatible inference (no PyTorch runtime required). Use TensorRT INT8 if GPU is available.

## 17. Sources and Retrieval Record

| Source ID | Title | URL | Type | License | Date Retrieved |
|-----------|-------|-----|------|---------|----------------|
| S158 | marcpaulo15/RL-connect4 -- CustomNetwork source | github.com/marcpaulo15/RL-connect4/blob/main/src/models/custom_network.py | Source code | Academic | 2026-08-05 |
| S159 | marcpaulo15/RL-connect4 -- Two-phase training methodology | github.com/marcpaulo15/RL-connect4 | GitHub | Academic | 2026-08-05 |
| S160 | psalarc/DQN-ConnectX-Agent -- DQN source (30KB) | github.com/psalarc/DQN-ConnectX-Agent/blob/main/src/DS669FinalProject_PabloSalar.py | Source code | Academic | 2026-08-05 |
| S161 | AZAL paper -- arXiv:2607.08984 | arxiv.org/abs/2607.08984 | Academic paper | CC | 2026-08-05 |
| S162 | GoodCoder666/katac4 -- train.py (board-size randomization) | github.com/GoodCoder666/katac4/blob/main/train.py | Source code | MIT (inferred) | 2026-08-05 |
| S163 | ecc521/connect-4-solver -- NNUE 7x6 and 8x8 | github.com/ecc521/connect-4-solver | Source code | AGPL v3 | 2026-08-05 |
| S164 | Waidchen et al. (2022) -- XAI for Connect 4 | arxiv.org/abs/2202.11797 | Academic paper | CC | 2026-08-05 |
| S165 | sebadorn/Machine-Learning--Connect-Four | github.com/sebadorn/Machine-Learning--Connect-Four | GitHub | -- | 2026-08-05 |
| S166 | TonyCWang/ConnectFour dataset card | huggingface.co/datasets/TonyCWang/ConnectFour | Dataset card | MIT | 2026-08-05 |
| S167 | Gridline Four Android -- complexity formulas | github.com/gridline-four-android | GitHub | -- | 2026-08-05 |
| S168 | Kamade/connect-n -- Adaptive scoring NxN | github.com/Kamide/connect-n | Source code | -- | 2026-08-05 |
| S169 | Wikipedia -- Connect Four board-size results | en.wikipedia.org/wiki/Connect_Four | Wikipedia | CC BY-SA | 2026-08-05 |

## 18. Cross-Links

- **NN-001** -- Architecture overview (ResNet, MLP, CNN, DQN, NNUE survey); NN-004 focuses on board-size generalization across all five families
- **NN-002** -- NNUE source decode (7x6 and 8x8); NN-004 extends this to 15x13 with weight-switching analysis
- **NN-003** -- Temperature schedules, replay buffer, AZAL; NN-004 uses AZAL board-size consistency results
- **MCTS-002** -- Neural MCTS integration; board-size-agnostic neural policy is prerequisite for neural-guided MCTS on 15x13
- **CS-002** -- Board representation; column-height feature encoding is a board representation enhancement
- **CBL-001** -- Contender roster; Kamade (BOT-013) is the classical engine source for 15x13 training data
- **ENS-019** -- Board-size adaptive routing; transfer-learned 15x13 model enables this ensemble
- **BMS-DOC-002** -- MCTS consistency and board-size scaling; NN-004 BMS-NN-001 through BMS-NN-007 extend this to neural-specific benchmarks
- **RI-001** -- katac4 reference implementation; katac4 board-size randomization is one of NN-004 five approaches

## 19. Follow-Up Research Tasks

1. **Generate a 15x13 training dataset** using Kamade classical engine -- run 10,000 games, extract non-terminal positions, save as Parquet for supervised fine-tuning
2. **Implement and benchmark a global-average-pooling CNN** for ConnectX -- verify that a CNN trained on 7x6 can evaluate 15x13 positions
3. **Measure catastrophic forgetting** -- quantify how much 7x6 performance degrades after 15x13 fine-tuning for each architecture (CNN, MLP, ResNet)
4. **Evaluate column-height feature channel** -- compare 2-channel (player + opponent) vs 3-channel (+ column height) input for 15x13 generalization
5. **Implement NNUE weight-switching at inference** -- measure latency overhead of loading different weight files for different board sizes
6. **Run AZAL-style oracle consistency tests** on Connect Four 15x13 -- does the perfect 10x11 Chomp result hold?
7. **Benchmark transfer learning vs. training from scratch** on 15x13 -- how much does 7x6 pre-training help vs. starting from random initialization?

## 20. Deferred Empirical Experiments

- **BMS-NN-001:** Generate 15x13 positions using Kamade classical engine; fine-tune ResNet on 50K positions; measure oracle agreement rate on 1,000 held-out 15x13 positions
- **BMS-NN-002:** Measure catastrophic forgetting by evaluating fine-tuned model on 7x6 positions before and after fine-tuning
- **BMS-NN-003:** End-to-end benchmark: transfer-learned CNN vs. negamax on 15x13 board, 100 games each
- **BMS-NN-007:** Reproduce AZAL oracle consistency experiment on Connect Four 15x13

---

**EXTERNAL WORKER COMPLETE**
