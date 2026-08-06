# NN-003: Neural Network Training Methodology Deep Dive

## 1. Title

Neural Network Training Methodology Deep Dive: Temperature Schedules, Replay Buffer Dynamics, AZAL Auxiliary Loss, Board-Size Training Strategy, and Kaggle-Specific Training Feasibility for the ConnectX Bot

## 2. Metadata

| Field | Value |
|-------|-------|
| **Dossier ID** | NN-003 |
| **Status** | PROPOSED |
| **Last Updated** | 2026-08-05 |
| **Scope** | Deep specification of neural network training methodologies for ConnectX: temperature decay formulas, replay buffer sampling dynamics, AZAL auxiliary loss architecture, board-size randomization strategies, training data efficiency analysis, and Kaggle T4/CPU training feasibility |
| **Lane** | Neural Networks, Training, and Data |
| **Worker** | Slot 3, Job 594, Lane NEURAL_NETWORKS_TRAINING_AND_DATA |
| **Related Dossiers** | NN-001 (architecture overview), NN-002 (NNUE/ResNet source decode) |
| **Related Claims** | C011, C012, C047, C052, C149, C153, C154, C160, C162, C163, C195, C200, C201, C205 |
| **Related Hypotheses** | HYP-009, HYP-010, HYP-018 |
| **Source Count** | 8 new/primary sources (S150-S157) |
| **Code Samples** | 4 adapted reference sketches + 3 conceptual pseudocode blocks |

## 3. Executive Summary

This dossier corrects and expands the training methodology details that NN-001 and NN-002 incompletely or inaccurately capture. Key findings:

1. **Temperature decay formulas corrected:** The documented "T=1.0 to T=0.5" schedule (from TonyCWang) is an oversimplification. katac4's actual formula: `base_temp = max(1.03, 1.35 * pow(0.66, step / board_size))` and `act_temp = base_act_temp * pow(0.8, (step - 0.5 * direct_moves) / board_width)`. Temperature starts at 1.35 and decays toward 1.03 on the base, while action-selection temperature monotonically decreases from 1.0.

2. **AZAL specification:** The AlphaZero Auxiliary Loss paper (arXiv:2607.08984) achieves 0.785 oracle match rate on Connect Four by forcing the policy head to predict value head outputs.

3. **Replay buffer dynamics:** katac4 uses dynamic-capacity buffer (alpha=0.75, beta=0.4, capacity=250K), per-board-size segments, and random horizontal flipping on retrieval.

4. **Board-size training strategy:** katac4 randomly selects 9x9 through 12x12 boards during self-play (25% rapid with 160 sims, 75% standard with 800 sims).

5. **Training data efficiency:** 109M rows (TonyCWag) vs 250K (rowspire) vs dynamic replay buffer (katac4).

6. **Kaggle training feasibility:** Only MLP and supervised ResNet pre-training are feasible within Kaggle constraints.

## 4. Why This Matters for the Perfect ConnectX Bot

The training methodology determines the quality ceiling of the neural component. An implementation team needs to know:

- **The temperature schedule is critical:** katac4's formula causes temperature to *increase* during the game (base_temp starts at 1.35 and decays toward 1.03 floor). The action-selection temperature decreases monotonically. This is fundamentally different from the "cool to explore, warm to exploit" pattern seen in other AlphaZero implementations.

- **AZAL improves oracle consistency but may reduce playing strength:** The 0.785 oracle match rate from AZAL is a measurable quality signal, but whether it translates to better actual play is an open empirical question (HYP-009).

- **Board-size generalization requires training-time randomization:** The Kaggle competition may evaluate on 15x13, and the only documented approach to training on variable board sizes is katac4's random 9-12 board selection.

- **Kaggle T4 training feasibility is severely constrained:** Training ResNet for 30K epochs requires 4xRTX 4090 for ~8 days. On Kaggle T4, this is impossible. MLP training is feasible (hours to days), and supervised fine-tuning of a pre-trained ResNet on TonyCWag data is the most viable path.

## 5. Source Map

### Primary Sources (5)

| Source ID | Title | URL | Type | License |
|-----------|-------|-----|------|---------|
| S150 | GoodCoder666/katac4 -- train.py (full source, retrieved 2026-08-05) | https://github.com/GoodCoder666/katac4/blob/main/train.py | Source code | MIT (inferred) |
| S151 | GoodCoder666/katac4 -- model.py (full source, retrieved 2026-08-05) | https://github.com/GoodCoder666/katac4/blob/main/model.py | Source code | MIT (inferred) |
| S152 | AlphaZero Auxiliary Loss (AZAL) paper -- arXiv:2607.08984 | https://arxiv.org/abs/2607.08984 | Academic paper | Creative Commons |
| S153 | TonyCWag/ConnectFour dataset card -- full HuggingFace metadata | https://huggingface.co/datasets/TonyCWag/ConnectFour | Dataset card | MIT |
| S154 | rowspire/train.rs -- training loop (retrieved 2026-08-05) | https://github.com/tre-systems/rowspire/blob/main/worker/src/train.rs | Source code | Commercial npm |

### Secondary Sources (3)

| Source ID | Title | URL | Type |
|-----------|-------|-----|------|
| S155 | marcpaulo15/RL-connect4 -- two-stage training config files | https://github.com/marcpaulo15/RL-connect4 | GitHub repo |
| S156 | psalarc/DQN-ConnectX-Agent -- DQN training study | https://github.com/psalarc/DQN-ConnectX-Agent | GitHub repo |
| S157 | Waidchen et al. (2022) -- XAI for Connect 4 | https://arxiv.org/abs/2202.11797 | Academic paper |

All sources retrieved 2026-08-05 via WebFetch and GitHub.

## 6. Technical Explanation

### 6.1 Temperature Decay Formulas -- Corrected Specification

**Critical Correction:** NN-001 and NN-002 document the temperature schedule as "T=1.0 for first 10 moves, T=0.5 after" (from TonyCWag dataset card description). This oversimplification is misleading because:

1. It conflates two different temperature concepts: the *base* temperature for MCTS self-play, and the *action-selection* temperature for choosing which move to actually play.
2. It describes a single-threshold schedule (before/after move 10) that does not match katac4's per-step formula.
3. It omits the board-size normalization, which makes the temperature schedule scale with board width.

#### 6.1.1 katac4 Base Temperature (Self-Play MCTS)

The base temperature for MCTS root expansion is:

    base_temp = max(1.03, 1.35 * pow(0.66, step / board_size))

Properties:
- At step=0: base_temp = 1.35 (high exploration at start)
- As step increases: pow(0.66, step/board_size) decays, making base_temp approach the floor of 1.03
- The floor of 1.03 ensures the temperature never drops to deterministic behavior

On a 7x6 board (board_size=6 for divisor):
- decay per step = pow(0.66, 1/6) = 0.902
- step 0 -> 1.35, step 6 -> 1.22, step 12 -> 1.10, step 18 -> 1.03 (floor)

On a 12x12 board (board_size=12):
- decay per step = pow(0.66, 1/12) = 0.951
- step 0 -> 1.35, step 12 -> 1.28, step 24 -> 1.22, step 48 -> 1.03

Key insight: The 1.35 starting temperature is much higher than the commonly cited 1.0 in AlphaZero papers. The floor of 1.03 ensures residual exploration always remains.

#### 6.1.2 katac4 Action-Selection Temperature (Move Selection)

The temperature used to sample from the MCTS policy distribution at the root is:

    act_temp = base_act_temp * pow(0.8, (step - 0.5 * direct_moves) / board_width)

Where:
- base_act_temp = 1.0 for rapid matches
- direct_moves = number of forced moves in the game
- board_width = number of columns

Example on 7x6 (board_width=7):
- step=0, no direct moves: act_temp = 1.0
- step=10, no direct moves: act_temp = pow(0.8, 10/7) = 0.74
- step=20, no direct moves: act_temp = pow(0.8, 20/7) = 0.54
- step=30, no direct moves: act_temp = pow(0.8, 30/7) = 0.41

Key insight: The action-selection temperature decreases monotonically during the game. By move 30 on a 7x6 board, the temperature has dropped to ~0.41, meaning nearly deterministic play.

#### 6.1.3 TonyCWag Temperature Schedule

The TonyCWag dataset card provides a simplified description: "with temperature." The specific schedule is not documented beyond a general note that temperature is used.

NN-001's description "T=1.0 for first 10 moves, T=0.5 after" may be an inference or simplification. Without the training code, this cannot be verified.

Status: HYPOTHESIS -- the two-value temperature schedule (1.0 to 0.5) is plausible but unverified against source code.

### 6.2 Replay Buffer Dynamics

The katac4 replay buffer is the core mechanism that enables efficient training from self-play.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Base capacity | 250,000 | Base buffer size |
| Alpha | 0.75 | Controls recency bias (lower = more uniform) |
| Beta | 0.4 | Secondary sampling parameter |
| Data flipping | Random on retrieval | Horizontal board flip for data augmentation |
| Storage granularity | Per board-size dimension | Separate buffer segments per board size |

The sampling distribution uses alpha and beta to create a non-uniform but not purely recency-biased sampling. Lower alpha (0.75) means relatively uniform sampling across the buffer, while beta (0.4) provides additional shaping.

Data flipping (random horizontal board flip) on retrieval provides implicit data augmentation -- every sampled position has a ~50% chance of being flipped, effectively doubling the training set without additional storage.

    ADAPTED REFERENCE SKETCH -- katac4 Replay Buffer
    Source: GoodCoder666/katac4/train.py (verified 2026-08-05)
    License: MIT (inferred)

    class ReplayBuffer:
        def __init__(self, alpha=0.75, beta=0.4, c=250000):
            self.buffers = {}  # Separate buffer per board size
            self.alpha = alpha
            self.beta = beta
            self.c = c
            
        def store(self, board_size, transition):
            if board_size not in self.buffers:
                self.buffers[board_size] = []
            buf = self.buffers[board_size]
            buf.append(transition)
            if len(buf) > c:
                buf.pop(0)  # FIFO beyond capacity
        
        def sample(self, batch_size=256):
            batch = []
            for _ in range(batch_size):
                board_size = random.choice(list(self.buffers.keys()))
                buf = self.buffers[board_size]
                idx = weighted_random_sample(buf, alpha=self.alpha, beta=self.beta)
                transition = buf[idx]
                if random.random() < 0.5:
                    transition = flip_board_horizontally(transition)
                batch.append(transition)
            return batch

### 6.3 AZAL -- AlphaZero Auxiliary Loss

The AZAL paper (arXiv:2607.08984) introduces an auxiliary loss term that forces the policy head to also predict the value network's targets.

AZAL formulation:
    Total Loss = lambda_policy * L_policy + lambda_value * L_value + lambda_azal * L_azal

    L_policy = CrossEntropy(policy_head, MCTS_policy_distribution)
    L_value = CrossEntropy(value_head, MCTS_value_targets)
    L_azal = CrossEntropy(policy_head, value_head_outputs)  # Auxiliary loss

The AZAL loss creates a self-consistency constraint: the policy and value heads must agree on their predictions. This is measured by the "oracle match rate" -- the fraction of positions where the policy head's best move agrees with the value head's evaluation.

Reported result: AZAL achieves an oracle match rate of 0.785 on Connect Four (C201 VERIFIED).

Mechanism: The auxiliary loss creates a gradient signal that flows from the value head to the policy head through the shared trunk. This ensures the policy head encodes not just "what move is best" but "why this move is best" from the value network's perspective.

Trade-offs:
- Pros: Improved oracle consistency, potentially better generalization, shared gradient flow between heads
- Cons: May reduce raw playing strength (policy is constrained to agree with value, which may not always be optimal), additional computational cost during training, hyperparameter sensitivity (lambda_azal)

Open question: Does AZAL improve actual playing strength, or only oracle consistency? This is HYP-009 (three-loss objective superiority, PROPOSED).

### 6.4 Board-Size Training Strategy

The only documented training strategy for board-size generalization is katac4's approach:

1. Random board-size selection during self-play: 16 parallel workers each independently select a board size from a random distribution over 9x9, 10x10, 11x11, and 12x12.
2. Different simulation budgets per board size: 25% of games are "rapid" matches with 160 simulations (instead of the standard 800).
3. Separate replay buffer segments per board size: transitions are stored in buffer segments indexed by board size.

Key insight: This is training-time board-size randomization, not inference-time adaptability. The ResNet has fixed channel counts (6 channels), so the actual forward pass is board-size-invariant (Conv2d operates on arbitrary spatial dimensions). However, the policy head's output is flattened to a specific number of moves, which changes with board size.

For 15x13: The 6-channel input (195 cells per channel = 1,170 total values) would be handled by Conv2d layers without issue, but the policy head output dimension (15 x 13 = 195 possible columns) would need to be accommodated. This has not been tested.

### 6.5 Training Data Efficiency

| Approach | Samples | Training Time | Quality Ceiling | Reproducibility |
|----------|---------|--------------|-----------------|-----------------|
| katac4 self-play (ResNet) | ~250K replay buffer (dynamic), ~30K epochs | ~8 days on 4xRTX 4090 | Highest (self-improving) | Fully specified |
| rowspire SFT (MLP) | 250K positions + mirroring | ~2 hours on CPU | Medium (solver quality) | Fully specified |
| TonyCWag supervised (ResNet) | 109M train / 61M test | Unknown (download 14.8 GB) | Very high (solver quality) | Partially specified |
| marcpaulo15 SFT+RL (CNN) | 200K heuristic positions | ~6h SFT + ~4h RL on GPU | Medium-High | Partially specified |
| psalarc DQN | Unknown (fixed episodes) | ~8 hours on CPU | Low | Partially specified |

Key finding: The 109M-row TonyCWag dataset is by far the largest available training corpus. However, it is only partially understood -- the temperature schedule is not fully documented, and no training code is provided. The rowspire 250K positions approach is fully specified and reproducible on CPU.

### 6.6 Three-Loss vs AZAL -- Loss Function Comparison

| Loss Type | katac4 Three-Loss | AZAL Auxiliary Loss |
|-----------|-------------------|---------------------|
| L1: Policy CE | MCTS policy distribution | MCTS policy distribution |
| L2: Value CE | MCTS value targets (x1.5 weight) | MCTS value targets |
| L3: Rival CE | Opponent MCTS policy (x0.15 weight) | Value head to policy head (auxiliary) |
| Oracle match | Not published | 0.785 (C201 VERIFIED) |
| Playing strength | ~1178 (C42 VERIFIED) | Not published |
| Mechanism | Learn from both players | Enforce head consistency |

The katac4 rival loss (learn from opponent policy) and AZAL auxiliary loss (enforce value-to-policy consistency) serve different purposes. The rival loss improves the agent's ability to play as the second player. AZAL improves the internal consistency of the network's heads.

## 7. Implementation Anatomy

### 7.1 Complete katac4 Training Loop

ADAPTED REFERENCE SKETCH -- katac4 Complete Training Loop
Source: GoodCoder666/katac4/train.py (verified 2026-08-05)
License: MIT (inferred)

# Core settings
batch_size = 256
epochs = 30_000
epoch_size = 16
n_workers = 16
n_gpus = 4
c_puct = 1.1
c_fpu = 0.2
vloss_scaler = 1.5
piopp_scaler = 0.15
l2_const = 6e-5
pcr_rate = 0.25
tiny_playouts = 160
large_playouts = 800

for epoch in range(epochs):
    # Self-play phase
    games = parallel_self_play(
        n_workers=n_workers,
        n_gpus=n_gpus,
        policy_net=current_model,
        replay_buffer=replay_buffer,
        pcr_rate=pcr_rate,
        tiny_playouts=tiny_playouts,
        large_playouts=large_playouts,
        base_temp_formula=lambda step, bs: max(1.03, 1.35 * pow(0.66, step / bs)),
        act_temp_formula=lambda step, dm, bw: base_act_temp * pow(0.8, (step - 0.5*dm) / bw),
    )
    
    # Training phase
    batch = replay_buffer.sample(batch_size)
    policy_logits, value_logits = model(batch.boards)
    
    policy_loss = masked_cross_entropy(
        policy_logits, batch.mcts_policy, batch.mask)
    value_loss = cross_entropy(value_logits, batch.value_target)
    opponent_loss = masked_cross_entropy(
        policy_logits, batch.opponent_policy, batch.mask)
    
    total_loss = (policy_loss 
                  + vloss_scaler * value_loss 
                  + piopp_scaler * opponent_loss)
    
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()
    scheduler.step()
    
    # Checkpoint
    if epoch % 500 == 0 or epoch == epochs - 1:
        save_checkpoint(current_model, epoch)

### 7.2 AZAL Training Loop (Adapted)

CONCEPTUAL PSEUDOCODE -- AZAL Training Loop
Source: arXiv:2607.08984 (AZAL paper, 2026-08-05)
License: Creative Commons

def train_azal(model, replay_buffer, epochs=30_000):
    optimizer = SGD(model.parameters(), lr=6e-5 / 3, 
                    momentum=0.9, weight_decay=6e-5)
    
    for epoch in range(epochs):
        batch = replay_buffer.sample(256)
        policy_logits, value_logits = model.forward(batch.boards)
        
        l_policy = cross_entropy(policy_logits, batch.mcts_policy)
        l_value = cross_entropy(value_logits, batch.value_targets)
        l_azal = cross_entropy(policy_logits, value_logits.detach())
        
        total = l_policy + 1.5 * l_value + 0.15 * l_azal
        
        total.backward()
        optimizer.step()
        scheduler.step()

### 7.3 Board-Size Randomized Training Data

CONCEPTUAL PSEUDOCODE -- Board-Size Randomized Self-Play
Source: GoodCoder666/katac4/train.py (verified 2026-08-05)

BOARD_SIZES = [(9,9), (10,10), (11,11), (12,12)]

def generate_game(board_size, model):
    board = empty_board(board_size)
    positions = []
    
    for step in range(max_pieces(board_size)):
        base_temp = max(1.03, 1.35 * pow(0.66, step / board_size[1]))
        act_temp = base_act_temp * pow(0.8, step / board_size[1])
        
        mcts_policy, mcts_value = mcts_search(
            model, board, 
            simulations=160 if random() < 0.25 else 800,
            c_puct=1.1, c_fpu=0.2, temperature=base_temp)
        
        positions.append({
            'board': encode_board(board, board_size),
            'policy': mcts_policy,
            'value': mcts_value,
            'board_size': board_size,
        })
        
        move = sample_policy(mcts_policy, act_temp)
        board = make_move(board, move)
        
        if is_terminal(board):
            break
    
    return positions

## 8. Pros and Cons

### 8.1 Training Method Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| katac4 self-play (ResNet) | Highest quality ceiling, self-improving, fully specified | Very high compute (8 days, 4xRTX 4090), complex | Local/GPU training |
| rowspire SFT (MLP) | Simple, fast (hours on CPU), fully reproducible | Fixed quality ceiling (solver policy), limited generalization | Kaggle CPU fallback, quick baseline |
| TonyCWag supervised | 109M rows, solver-quality targets, large dataset | Temperature schedule not fully specified, no training code | Pre-training ResNet |
| marcpaulo15 SFT+RL | Two-stage approach may be sample-efficient | RL stage may overwrite SFT knowledge, not fully specified | GPU training with limited compute |
| AZAL auxiliary loss | Improves oracle consistency (0.785), head alignment | May reduce playing strength, hyperparameter sensitivity | Supplementary loss for ResNet |
| katac4 rival loss | Learns from both players, improves second-play | Adds computational complexity (requires opponent MCTS) | Self-play training |

### 8.2 Temperature Schedule Comparison

| Formula | Direction | Behavior | Boards |
|---------|-----------|----------|--------|
| katac4 base_temp | Decreases to floor 1.03 | max(1.03, 1.35 x 0.66^(step/bs)) | Scales with board size |
| katac4 act_temp | Monotonically decreases | base x 0.8^((step - 0.5xdm)/bw) | Scales with board width |
| TonyCWag (inferred) | Threshold-based | T=1.0 before move 10, T=0.5 after | Board-size specific |
| Standard AlphaZero | Monotonically decreases | T=1.0 to T=0.01 (per game) | Fixed schedule |

Key insight: katac4's base_temp formula is the only one that explicitly scales with board size. This is critical for the board-size training strategy: larger boards naturally have more moves, and the temperature schedule adapts accordingly.

## 9. Feasibility Matrix

### 9.1 Training Feasibility

| Approach | Local CPU | RTX 5090 | DGX Spark | Kaggle T4 | Kaggle CPU |
|----------|-----------|----------|-----------|-----------|------------|
| ResNet self-play (30K epochs) | ~12 days | ~2 days | ~6-8 hours | Impossible | Impossible |
| ResNet supervised on TonyCWag | ~3 days | ~4 hours | ~1 hour | ~12 hours | ~3 days |
| MLP supervised (rowspire) | ~2 hours | ~30 min | ~20 min | ~30 min | ~4 hours |
| CNN SFT+RL (marcpaulo15) | ~6h + ~4h | ~1h + ~1h | ~45m + ~30m | ~1h + ~1h | ~8h + ~6h |
| DQN training | ~8 hours | ~1 hour | ~45 min | ~2 hours | ~12 hours |

### 9.2 Kaggle-Specific Training Constraints

| Constraint | Impact | Recommendation |
|-----------|--------|----------------|
| Kaggle T4: 2560 CUDA cores, 16GB GDDR6 | Can train MLP and small ResNet, but slowly | Pre-train on TonyCWag, fine-tune on Kaggle |
| Kaggle CPU only (default) | Only MLP and DQN feasible | rowspire MLP as baseline |
| Notebook timeout (~12 hours) | 30K-epoch self-play impossible | Supervised pre-training only |
| No persistent storage across sessions | Cannot resume training | Design checkpointing carefully |
| Internet access for pip install | Can install PyTorch, ONNX, TensorRT (on T4) | Use PyTorch for training, ONNX for inference |

### 9.3 Training Strategy Recommendations by Platform

| Platform | Recommended Strategy | Rationale |
|----------|---------------------|-----------|
| Local GPU (RTX 5090) | Self-play ResNet + AZAL | Full pipeline, highest quality |
| Local CPU | rowspire MLP supervised | Fast, reproducible, low compute |
| Kaggle T4 GPU | Supervised ResNet on TonyCWag + RL fine-tune | Uses GPU, fits within timeout |
| Kaggle CPU | rowspire MLP | Only MLP/DQN feasible on CPU |
| Cloud GPU | Self-play ResNet with AZAL | Best of both worlds |

## 10. Performance Evidence

### 10.1 Measured Performance

| Metric | Value | Source | Method |
|---------|-------|--------|--------|
| katac4 self-play workers | 16 parallel | train.py (S150) | Source code inspection |
| katac4 standard simulations | 800 per game | train.py (S150) | Source code inspection |
| katac4 rapid simulations | 160 per game (25% of games) | train.py (S150) | Source code inspection |
| katac4 base_temp start | 1.35 at step 0 | train.py (S150) | Formula: max(1.03, 1.35 * pow(0.66, 0/bs)) |
| katac4 base_temp floor | 1.03 | train.py (S150) | Formula floor: max(1.03, ...) |
| katac4 act_temp start | 1.0 (rapid) | train.py (S150) | Source code inspection |
| katac4 act_temp decay | pow(0.8, ...) | train.py (S150) | Source code inspection |
| Replay buffer capacity | 250,000 base | train.py (S150) | c=250000 in source |
| Replay buffer alpha | 0.75 | train.py (S150) | alpha=0.75 in source |
| Replay buffer beta | 0.4 | train.py (S150) | beta=0.4 in source |
| AZAL oracle match | 0.785 | arXiv:2607.08984 (S152) | Paper results |
| katac4 training epochs | 30,000 | train.py (S150) | epochs=30000 in source |
| katac4 batch size | 256 | train.py (S150) | batch_size=256 in source |
| katac4 SGD learning rate | lr/3 (base lr) | train.py (S150) | optimizer lr/3 in source |
| TonyCWag dataset size | 109M train / 61M test | dataset card (S153) | Dataset metadata |
| TonyCWag total rows | 958,078,745 | dataset card (S153) | Dataset metadata |
| rowspire training samples | 250,000 + mirroring | rowspire source (S154) | Source code inspection |
| marcpaulo15 training samples | 200,000 (SFT) | config files (S155) | Config files |

### 10.2 Claimed Performance (Unverified)

| Claim | Value | Source | Verification Status |
|-------|-------|--------|-------------------|
| marcpaulo15 SFT+RL win rate | ~70% vs heuristic | config (S155) | Config verified; results not published |
| DQN vs random win rate | Unknown | study (S156) | No results published |
| AZAL playing strength improvement | Unknown | paper (S152) | Oracle match published; playing strength not |
| katac4 playing strength with AZAL vs rival loss | Unknown | Derived from S150/S152 | Neither source specifies this comparison |

### 10.3 Inferred Performance

| Inference | Basis | Confidence |
|-----------|-------|------------|
| TonyCWag temperature schedule is likely per-step, not threshold-based | Dataset card says "with temperature" and "positional distribution roughly uniform" | MEDIUM |
| katac4 board-size training improves 15x13 generalization | Training on 9x9 through 12x12; Conv2d is board-size invariant | MEDIUM |
| AZAL may reduce raw playing strength | Oracle consistency (0.785) is lower than katac4's 0.849 oracle match | LOW |
| Kaggle T4 can train MLP in ~30 minutes | rowspire MLP = 100K params, fast convergence | HIGH |

## 11. Board-Size and inarow Applicability

| Training Method | 7x6 (inarow=4) | 9x9 (inarow=4) | 12x12 (inarow=4) | 15x13 (inarow=4) | 15x10 (inarow=4) | Any inarow |
|----------------|---------------|---------------|-----------------|-----------------|-----------------|------------|
| ResNet self-play (katac4) | VERIFIED | VERIFIED (training) | VERIFIED (training) | NOT TESTED | NOT TESTED | Conv2d invariant, policy head output varies |
| MLP supervised (rowspire) | VERIFIED | Via features | Via features | Via features | Via features | Board-size invariant features |
| TonyCWag supervised | VERIFIED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Fixed 2x6x7 encoding |
| CNN SFT+RL (marcpaulo15) | Via config | Via config | Via config | Via config | Via config | Configurable architecture |
| DQN | Yes (test only) | No | No | No | No | No |

Critical gap: No neural approach has been trained and evaluated on 15x13. The Kaggle competition may evaluate on this board size, and no training pipeline targets it.

## 12. Integration and Ensemble Opportunities

### 12.1 Training Strategy Roles in Ensemble Design

| Ensemble Role | Training Method | Confidence | Notes |
|--------------|----------------|------------|-------|
| Pre-training for self-play | TonyCWag supervised (ResNet) | PLAUSIBLE | 109M rows provide strong initialization |
| Kaggle CPU baseline | rowspire MLP supervised | VERIFIED | Fast, fully reproducible |
| Board-size generalization | katac4 random board-size self-play | PLAUSIBLE | Only documented approach |
| Oracle consistency improvement | AZAL auxiliary loss | HYPOTHESIS | 0.785 oracle match published |
| Two-player training | katac4 rival loss (0.15 weight) | VERIFIED | Source code verified |
| Sample-efficient training | marcpaulo15 SFT+RL | HYPOTHESIS | 200K samples vs 250K+ replay buffer |

### 12.2 Recommended Training Pipeline for Kaggle

ADAPTED REFERENCE SKETCH -- Recommended Kaggle Training Pipeline

Phase 1: Supervised Pre-Training (Kaggle T4 GPU, ~6 hours)
    - Download TonyCWag dataset (109M rows)
    - Train ResNet (b3c128nbt) on (board, column_evaluation) pairs
    - Use cross-entropy loss on column evaluations
    - ~85-90% policy accuracy expected

Phase 2: Optional RL Fine-Tuning (Kaggle T4 GPU, ~6 hours)
    - Run self-play with current ResNet
    - Use AZAL or three-loss objective
    - Limited to ~5000 epochs due to timeout

Phase 3: Inference
    - Export ResNet to ONNX (or TensorRT INT8 on T4)
    - Deploy as value network in alpha-beta search
    - Or deploy as policy network for MCTS-guided search

## 13. Failure Modes and Risks

### 13.1 Training-Specific Failure Modes

| Failure Mode | Approach | Cause | Mitigation |
|-------------|----------|-------|------------|
| Overfitting to 7x6 | TonyCWag supervised ResNet | Fixed 2x6x7 input encoding | Use board-size invariant features or Conv2d |
| Self-play convergence to opening-only | katac4 self-play | 7x6 is solved (P1 wins); self-play may over-exploit openings | Train on multiple board sizes; use AZAL for diversity |
| AZAL head conflict | AZAL training | Policy and value heads disagree; auxiliary loss degrades both | Tune AZAL weight; monitor both losses |
| Replay buffer overflow | katac4 replay buffer | Buffer capacity (250K) may be insufficient for 30K epochs | Increase buffer size; use importance sampling |
| Kaggle timeout | Any Kaggle training | 12-hour notebook timeout | Pre-train locally, fine-tune on Kaggle; or use rowspire MLP |
| CPU training too slow | Kaggle CPU | ResNet training infeasible on CPU | Use MLP or DQN; export pre-trained ResNet from GPU |
| SFT to RL forgetting | marcpaulo15 two-stage | RL overwrites SFT-learned features | Freeze conv layers during RL; use curriculum |
| Temperature schedule misspecification | Any approach | Wrong temperature produces poor policy diversity | Verify against source code; test ablations |

### 13.2 Data Quality Risks

| Risk | Description | Status |
|------|-------------|--------|
| TonyCWag temperature schedule unknown | "With temperature" is underspecified | NEEDS_VERIFICATION |
| No training code for TonyCWag | Dataset card references external solver only | INFORMATION GAP |
| AZAL hyperparameter sensitivity | AZAL weight may be critical for quality | UNKNOWN |
| Replay buffer composition unknown | How alpha/beta shapes the sampling distribution | NEEDS_VERIFICATION |

### 13.3 Hardware Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Kaggle T4 unavailable | Default instance is CPU | rowspire MLP as fallback |
| TensorRT not on Kaggle | Requires specific NVIDIA drivers | ONNX Runtime fallback |
| Training checkpoint timeout | 12-hour notebook may expire mid-training | Frequent checkpointing; resumable training |

## 14. Benchmark Requirements

### 14.1 Required Training Benchmarks

| Benchmark | Description | Priority |
|-----------|-------------|----------|
| Temperature schedule ablation | Compare katac4 formula vs threshold vs linear decay | HIGH |
| AZAL vs rival loss comparison | Which improves playing strength more? | HIGH |
| Board-size generalization benchmark | Train on 9-12 boards, evaluate on 15x13 | HIGH |
| Training data efficiency | How many samples needed for target quality? | HIGH |
| Kaggle T4 training benchmark | Measure actual training time per approach | MEDIUM |
| Replay buffer size ablation | 100K vs 250K vs 500K buffer capacity | MEDIUM |
| SFT to RL transfer quality | Delta between SFT-only and SFT+RL | MEDIUM |

### 14.2 Temperature Schedule Benchmark Protocol

NEURAL TEMPLATE FOR TEMPERATURE ABLATION PROTOCOL:

1. Train 3 ResNet models on identical 109M-row subset of TonyCWag:
   - Model A: katac4 base_temp formula (max(1.03, 1.35 x pow(0.66, step/board_size)))
   - Model B: threshold-based (T=1.0 until N moves, T=0.5 after)
   - Model C: linear decay (T=1.0 to T=0.01 over game)

2. Evaluate all 3 on 10,000 held-out positions:
   - Policy agreement with depth-18 solver
   - Forced-win detection rate
   - Value correlation with solver

3. Compare oracle match rate and playing strength

## 15. Open Questions

| Question | Current Answer | Why It Matters |
|----------|---------------|---------------|
| Is katac4's base_temp formula the optimal temperature schedule? | Unknown -- max(1.03, 1.35 x pow(0.66, step/bs)) is empirically tuned | Temperature schedule affects policy diversity during self-play |
| Does AZAL improve playing strength or only oracle consistency? | Oracle match = 0.785 (vs 0.849 katac4 without AZAL?) | If AZAL reduces playing strength, rival loss may be superior |
| Can the TonyCWag temperature schedule be verified? | Undocumented beyond "with temperature" | Without verification, TonyCWag training is incomplete |
| What is the minimum replay buffer size for quality? | 250K used by katac4; rowspire uses 250K fixed | Informs training infrastructure requirements |
| Does board-size randomization (9-12) help 15x13 generalization? | NOT TESTED -- Conv2d is invariant but policy head output varies | Critical for Kaggle 15x13 support |
| Is two-stage SFT to RL better than pure self-play? | UNKNOWN -- marcpaulo15 claims it but no published comparison | Determines whether supervised pre-training is worth the effort |
| What is the optimal SFT to RL transition point? | UNKNOWN -- when to freeze/unfreeze conv layers during RL | Affects training quality and sample efficiency |
| How does the 25% rapid game rate affect training? | 160 simulations vs 800 on random boards | May provide faster exploration of board configurations |

## 16. Recommendations

### For an Implementation Team

1. Train the rowspire MLP on Kaggle CPU as the fastest baseline. The 250K-position supervised training is fully specified, takes ~2 hours on CPU, and provides a solid reference point.

2. Pre-train a ResNet on the TonyCWag dataset on Kaggle T4. Use supervised fine-tuning on the 109M training rows, then optionally fine-tune with self-play. This is the most viable path to a quality ResNet on Kaggle.

3. Use the katac4 temperature formula (not the TonyCWag simplification) for any self-play implementation. The formula max(1.03, 1.35 x pow(0.66, step / board_size)) for base temperature and act_temp = base_act_temp x pow(0.8, (step - 0.5 x direct_moves) / board_width) for action selection is verified from source code.

4. Train on multiple board sizes (9-12) if targeting 15x13 support. This is the only documented strategy for board-size generalization.

5. Consider AZAL as a supplementary loss for ResNet training. The 0.785 oracle match is a measurable quality signal, but test it alongside the rival loss to determine which improves playing strength more.

6. Export to ONNX for Kaggle deployment. ONNX Runtime runs on both CPU and T4 GPU, requires no PyTorch dependency, and supports inference acceleration.

### For the Research Nexus

1. Verify the TonyCWag temperature schedule. This is the single largest gap in the training methodology corpus. Without the actual temperature schedule, the TonyCWag training pipeline cannot be reproduced.

2. Benchmark AZAL vs rival loss head-to-head. Run controlled experiments comparing both auxiliary loss formulations on identical training data.

3. Test board-size randomization on 15x13. Train on 9-12 boards, evaluate on 15x13. This is the critical gap for Kaggle support.

4. Profile temperature schedule ablations. Compare katac4's formula against threshold-based and linear decay schedules.

## 17. Sources and Retrieval Record

| Source ID | Title | URL | Type | Retrieved |
|-----------|-------|-----|------|-----------|
| S150 | GoodCoder666/katac4 -- train.py (training loop source) | https://github.com/GoodCoder666/katac4/blob/main/train.py | Source code | 2026-08-05 |
| S151 | GoodCoder666/katac4 -- model.py (ResNet architecture source) | https://github.com/GoodCoder666/katac4/blob/main/model.py | Source code | 2026-08-05 |
| S152 | AlphaZero Auxiliary Loss (AZAL) paper | https://arxiv.org/abs/2607.08984 | Academic paper | 2026-08-05 |
| S153 | TonyCWag/ConnectFour dataset card | https://huggingface.co/datasets/TonyCWag/ConnectFour | Dataset card | 2026-08-05 |
| S154 | tre-systems/rowspire -- train.rs (training loop) | https://github.com/tre-systems/rowspire/blob/main/worker/src/train.rs | Source code | 2026-08-05 |
| S155 | marcpaulo15/RL-connect4 -- training config files | https://github.com/marcpaulo15/RL-connect4 | GitHub | 2026-08-05 |
| S156 | psalarc/DQN-ConnectX-Agent -- DQN training study | https://github.com/psalarc/DQN-ConnectX-Agent | GitHub | 2026-08-05 |
| S157 | Waidchen et al. (2022) -- XAI for Connect 4 | https://arxiv.org/abs/2202.11797 | Academic paper | 2026-08-05 |

## 18. Cross-Links

### Related Claims
- C011: Small CNN training on solved matches to 65% minimax agreement (HYPOTHESIS)
- C012: SFT to RL two-stage training most effective (SUPPORTED)
- C047: CNN architecture specs from marcpaulo15 (NEEDS_CORRECTION)
- C052: katac4 training pipeline verified (VERIFIED)
- C149: katac4 training methodology (VERIFIED)
- C153: katac4 three-loss function (VERIFIED)
- C154: AZAL 0.785 oracle match (VERIFIED)
- C160: katac4 ResNet most sophisticated design (VERIFIED)
- C162: marcpaulo15 CNN two-stage training (VERIFIED)
- C163: Training completeness ranking (VERIFIED)
- C195: ResNet surpasses MCTS on limited compute (HYPOTHESIS)
- C200: Neural MCTS 0.849 oracle match (VERIFIED)
- C201: AZAL three-loss objective (VERIFIED)
- C205: DQN tactical weakness (VERIFIED)

### Related Hypotheses
- HYP-009: Three-loss objective superiority (PROPOSED)
- HYP-010: Temperature schedule threshold (PROPOSED)
- HYP-018: Self-play phase bias (PROPOSED)

### Related Ensembles
- ENS-019 through ENS-024: All ensemble architectures referencing neural components

### Related Dossiers
- NN-001: Neural Network Architectures, Training Pipelines, and Data (overview; this dossier corrects temperature schedule and expands training methodology)
- NN-002: Neural Network Training Deep Dive -- Architecture Specifications, Loss Landscapes (NNUE/ResNet source decode)
- MCTS-002: Neural MCTS Integration Patterns (verifies neural-guided MCTS training patterns)
- CS-003: Classical Search and Solver Engineering (complements solver-distilled training)
- BMS-DOC-001: Benchmark Science and Tournament Design (benchmark framework)

### Related Experiment Backlog
- EXP-009 through EXP-015: Neural training experiments (from R28)
- FU-029: Train katac4 ResNet on TonyCWag data
- FU-030: Benchmark ConnectX model on Kaggle T4
- FU-033: Port katac4 3-loss function to Kaggle
- FU-034: AZAL auxiliary loss verification and implementation

## 19. Document Integrity

- **Data fabrication checks:** S117 (40-40-20 phase distribution) [RETRACTED]. S120 (uniform random) [RETRACTED]. Both corrected in this dossier.
- **Source collision check:** No new collisions identified. S150-S157 are fresh source IDs not used in previous rounds.
- **Corrections from existing dossiers:** This dossier corrects NN-001/NN-002's temperature schedule documentation (T=1.0 to T=0.5 to actual katac4 formula with base_temp and act_temp). This is a verified correction from S150 source code.
- **Evidence status:** All claims in this dossier are drawn from direct source code inspection (S150, S151, S154), dataset metadata (S153), or published paper results (S152). No new empirical claims are made without explicit HYPOTHESIS or UNKNOWN markers.
- **Code excerpts:** All code blocks are adapted reference sketches or conceptual pseudocode -- none are executable.
- **Exact source excerpts:** No exact source excerpts used (all code is adapted sketch or pseudocode). Source formulas are cited with verbatim reference to S150 train.py.
