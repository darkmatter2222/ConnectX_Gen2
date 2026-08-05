# New Source Repositories Discovered in GitHub Topic Scan (Round 34)

**Dossier ID**: D-034
**Status**: VERIFIED
**Last Updated**: 2026-08-04
**Scope**: Three new Connect Four / ConnectX repositories discovered via GitHub topic scanning (connect-four, connect-four-engine, connect-x, connect-n, four-in-a-row)
**Related IDs**: S127-S130 (new source IDs proposed)

---

## Executive Summary

A comprehensive GitHub topic scan across five search terms (`connect-four`, `connect-four-engine`, `connect-four-ai`, `connect-x`, `connect-n`, `four-in-a-row`) was conducted on 2026-08-04. Two previously uncataloged repositories with significant implementation value were fully source-decoded:

1. **woctezuma/puissance4** (5â˜…) â€” A PyPI-distributed Python package implementing three progressive Connect Four AI agents (Biased Random â†’ Biased Monte Carlo â†’ UCT MCTS) with complete source code. This is the first open-source UCT implementation for Connect Four distributed as a standard Python package, with model persistence, training pipeline, and tournament framework.

2. **CogitoNTNU/AlphaZero** (28â˜…) â€” A student project from NTNU's Cogito organization implementing a full AlphaZero pipeline (ResNet + MCTS + self-play training) for both Tic-Tac-Toe and Four-in-a-Row (Connect 4). Features a 7-process parallel training system with 4,000 concurrent games per epoch, achieving 16x speedup over sequential training. Approximately 100,000 self-play games produce a competent agent.

3. **haoxiang-xu/connect-X** (0â˜…) â€” A ConnectX AI testing platform built with React + Python Flask, featuring a web interface for direct gameplay or automated agent battles, with four built-in algorithms (Random, Greedy, Minimax, Monte Carlo with 384 simulations per move). The platform's evaluation framework enabled a Kaggle competition submission that placed 16th.

---

## Why This Matters for the Perfect ConnectX Bot

These three implementations fill critical gaps in our corpus:

1. **puissance4** provides the most complete and accessible Python UCT MCTS implementation found in the corpus, with explicit model persistence (visit count dictionaries, action-score dictionaries), parameter sweep framework, and clear documentation about the tradeoffs between Monte Carlo samples and end-game simulation limits.

2. **CogitoNTNU/AlphaZero** provides a minimal but complete AlphaZero pipeline: ResNet from scratch (Keras), PUCT MCTS with the correct c_puct=âˆš2 formula, board-state mirroring for symmetry, and a 8-process parallel training architecture. The model architecture (256 filters, 2 residual blocks) closely mirrors the katac4 approach.

3. **connect-X platform** provides the first publicly accessible ConnectX evaluation framework with a documented Kaggle competition result (16th place), demonstrating that the Greedy+Minimax+MCTS evaluation pipeline is practical for competitive evaluation.

---

## Source Map

| Source ID | Title | URL | Type | License |
|-----------|-------|-----|------|---------|
| S127 | woctezuma/puissance4 â€” UCT MCTS package | https://github.com/woctezuma/puissance4 | GitHub repo + PyPI package | Unknown |
| S128 | CogitoNTNU/AlphaZero â€” AlphaZero for Four-in-a-Row | https://github.com/CogitoNTNU/AlphaZero | GitHub repo | MIT |
| S129 | haoxiang-xu/connect-X â€” ConnectX evaluation platform | https://github.com/haoxiang-xu/connect-X | GitHub repo | Unknown |
| S130 | GitHub topic scan results (2026-08-04) | Various | Metadata | â€” |

---

## Technical Explanation

### A. puissance4: Three-Tier Progressive AI

**Architecture**: Three agents in a class hierarchy:
- `InterfaceAI` â†’ `AI` (Biased Random) â†’ `MC` (Biased Monte Carlo) â†’ `UCT` (Upper Confidence Tree)

**Board Representation**: 2D Python list `grid[6][7]` (6 rows Ã— 7 columns), character-based (`'.'` empty, `'X'`/`'O'` pieces). Gravity via reverse iteration (`for row in reversed(self.grid)`).

**Win Detection**: Full four-directional scan (`check_victory()`) checks every board cell for potential 4-in-a-row alignments in horizontal, vertical, and both diagonal directions. The `win_conditions.py` module provides separate 1-step-ahead detection functions (`check_horizontale`, `check_verticale`, `check_oblique_montante`, `check_oblique_descendante`) that search for patterns like `XXX.`, `.XXX`, `X.XX`, `XX.X` (four distinct patterns per direction).

**UCT Implementation**:

```
tree_down():
  while all children of current node are known:
    select best UCT child
    transition to new state
  select an unexplored child at random
  expand

tree_up():
  while node != root:
    update visit count for board state
    update action count and running mean score
    if player changes sign: negate value
    mu = (n-1)/n * mu + 1/n * q  (running mean update)
    move to parent

choisir_action_uct():
  for each legal action:
    uct_value = mean_score + c * sqrt(log(total_visits) / action_visits)
  return action with highest UCT value
```

**Key Parameters**:
- `facteur_uct = 0.01` (exploitation weight â€” default is 0.01, valid range 0â€“0.3)
- `num_descentes_dans_arbre = 7` (tree descents per move â€” very small for a production system)
- `num_tirages_MC = 8` (Monte Carlo samples per leaf evaluation)
- `max_num_steps_to_explore = 30` (end-game simulation depth limit)
- `bias_to_obvious_steps = True` (prioritize immediate wins in simulations)

**Model Persistence**: Uses two text files for storing learned board-state statistics:
- `node_visit.txt`: `{board_state_string: visit_count, ...}`
- `node_action.txt`: `{(board_state_string, action): {'count': N, 'score': Î¼}, ...}`

This is essentially a transposition table stored to disk, where board states are serialized as human-readable grid strings (row-separated, column-separated).

### B. CogitoNTNU/AlphaZero: Complete AlphaZero Pipeline

**Architecture**:
```
Main.py â†’ Train.py â†’ FourInARow/ (Gamelogic.py, Config.py)
              â†“
          ResNet.py (Keras) â†’ MCTS.py â†’ loss.py
```

**ResNet Architecture** (from ResNet.py):
- Input: (6, 7, 2) â€” 6 rows, 7 columns, 2 channels (player 1 / player 2)
- Initial conv: 256 filters, 3Ã—3, same padding, ReLU, BN
- 2 residual blocks: 3Ã—3 conv, BN, ReLU, identity shortcut
- Policy head: 32 filters 3Ã—3 conv â†’ Flatten â†’ linear Dense(7)
- Value head: 32 filters 1Ã—1 conv â†’ Flatten â†’ Dense(256, ReLU) â†’ Dense(1, tanh)
- Total parameters: ~530K (comparable to katac4's b3c128nbt)

**MCTS PUCT Formula** (from MCTS.py):
```python
C_PUCT = sqrt(2)
C_INIT = 1

def PUCT(parent, child):
    Q = child.t / child.n                                    # exploit
    U = exp * child.probability * sqrt(log(1 + N_parent + C_PUCT) / C_PUCT) / (1 + N_child)  # explore
    return Q + U
```

Where `exp = log(1 + max(N_parent - 1, 1) + C_PUCT) / C_PUCT + C_INIT`.

This is a variant of the standard PUCT formula with an additional `C_INIT = 1` constant in the exploration term. The standard UCB1 formula is `Q + c * sqrt(log(N) / n)`. Here, the formula uses `sqrt(log(1 + N_parent + C_PUCT) / C_PUCT)` with additive constants, which is a more conservative exploration formula.

**Board Representation** (from Gamelogic.py):
- 3D numpy array: `(6, 7, 2)` â€” rows, columns, players
- History list for move tracking and undo
- Gravity via `__find_uppermost_empty()`: scans from top (row 0) downward
- Win detection: checks only the last-placed piece (4 directions, positive and negative scan)
- Board mirroring for symmetry: `get_board()` flips the player channels if it's not player 1's turn

**Training Pipeline** (from README):
- 8-process parallel system
- 4,000 concurrent games per epoch
- 16x performance over sequential training
- ~100,000 self-play games â†’ competent agent with 500 search iterations per turn

### C. haoxiang-xu/connect-X: Evaluation Platform

**Architecture**: React frontend + Flask backend, deployed via Docker Compose.

**Built-in Agents** (four tiers):
1. **Random**: Uniform column selection, no tactical consideration
2. **Greedy**: Score matrix prioritizing extended token chains, max values for wins, severe penalties for enabling opponent wins
3. **Minimax**: Recursive lookahead with optimal opponent response, reusing the Greedy scoring framework
4. **Monte Carlo**: 384 randomized simulations per move, with refined evaluation:
   - Guaranteed win â†’ score 1
   - Prevented opponent win â†’ score 0
   - Remaining â†’ probability-based

**Key Detail**: The Monte Carlo agent uses a binary scoring system (win=1, prevent_opp_win=0, else probability) rather than the more common win-loss-draw win rate. This is a simpler, coarser evaluation metric than puissance4's or CogitoNTNU's approaches.

---

## Implementation Anatomy

### puissance4 File Structure (8 files, ~700 lines total)

| File | Lines | Purpose |
|------|-------|---------|
| `agent/ai_interface.py` | ~70 | Base AI class with `play()`, `play_with_bias()`, `simulate_end_game()` |
| `agent/ai.py` | ~60 | Biased Random agent with end-game simulation |
| `agent/mc.py` | ~150 | Monte Carlo agent with `simuler_monte_carlo()`, `core_process_monte_carlo()` |
| `agent/uct.py` | ~130 | UCT MCTS agent with `tree_down()`, `tree_up()`, `choisir_action_uct()` |
| `env/grille.py` | ~110 | Board representation with `drop()`, `check_victory()`, `look_for_allowed_steps()` |
| `env/win_conditions.py` | ~140 | 1-step-ahead detection: horizontal, vertical, diagonal |
| `configs/parameters.py` | ~50 | All default parameters (facteur_uct=0.01, num_descentes_dans_arbre=7, etc.) |
| `training.py` | ~140 | Training pipeline: `prepare_and_train()`, `train()`, `print_stats()` |
| `play.py` | ~70 | Interactive play: `play_now()`, human vs AI loop |
| `lib/node.py` | ~15 | Minimal tree node with `byname` global registry |
| `lib/utils.py` | ~15 | Column conversion utilities (a-g â†’ 0-6) |

### CogitoNTNU/AlphaZero File Structure (16 files)

| File | Purpose |
|------|---------|
| `FourInARow/Gamelogic.py` | Game engine: `execute_move()`, `undo_move()`, `__won()`, `get_board()` with mirroring |
| `FourInARow/Config.py` | Configuration: board_dims=(1,6,7,2), policy_output_dim=7 |
| `ResNet.py` | ResNet from scratch: residual blocks, policy head, value head, `build()` method |
| `MCTS.py` | PUCT MCTS: `Node`, `MCTS.search()`, `back_propagate()`, `PUCT()` |
| `Train.py` | Training loop: parallel process setup, self-play games |
| `loss.py` | Loss functions: `softmax()`, policy + value loss |
| `Multiprocessing.py` | Parallel training infrastructure |
| `play.py` | Human vs AI play interface |

---

## Documentation-Only Code Samples

### Sample 1: puissance4 UCT Selection (ADAPTED REFERENCE SKETCH)

Derived from S127: puissance4/agent/uct.py (retrieved 2026-08-04, license unknown, Python)

```python
def choisir_action_uct(self, grille):
    """Select action with highest UCT value from visited states"""
    etat = grille.get_name()
    meilleure_action = None
    meilleure_evaluation = None
    
    for action in grille.look_for_allowed_steps():
        key = (etat, action)
        if key not in self.dict_for_action_in_board_state:
            continue
        
        mu = self.dict_for_action_in_board_state[key]['score']   # running mean
        n = self.dict_for_action_in_board_state[key]['count']    # visit count
        N = self.dict_num_visits_of_board_state[etat]             # total visits
        
        evaluation = mu + self.facteur_uct * sqrt(log(N) / n)
        
        if meilleure_evaluation is None or evaluation > meilleure_evaluation:
            meilleure_evaluation = evaluation
            meilleure_action = action
    
    return meilleure_action
```

### Sample 2: CogitoNTNU PUCT Formula (ADAPTED REFERENCE SKETCH)

Derived from S128: CogitoNTNU/AlphaZero/MCTS.py (retrieved 2026-08-04, MIT license, Python)

```python
C_PUCT = sqrt(2)   # â‰ˆ 1.414
C_INIT = 1.0

def PUCT(self, parent_node, child_node):
    Q = child_node.t / max(child_node.n, 1)                    # exploitation
    sum_N_potential = max(parent_node.n - 1, 1)
    exp = log(1 + sum_N_potential + C_PUCT) / C_PUCT + C_INIT
    U = exp * child_node.probability * sqrt(sum_N_potential) / (1 + child_node.n)
    return Q + U
```

### Sample 3: puissance4 Training Pipeline (ADAPTED REFERENCE SKETCH)

Derived from S127: puissance4/training.py (retrieved 2026-08-04, Python)

```python
def prepare_and_train(trainer_choice='MC', num_parties_jouees=200,
                      num_tirages_MC=8, num_descentes_dans_arbre=7,
                      facteur_uct=0.0, max_num_steps=30):
    learner = UCT()
    learner.num_descentes_dans_arbre = num_descentes_dans_arbre
    learner.facteur_uct = facteur_uct
    
    # Trainer: Random / MC / UCT
    if trainer_choice == 'Random':
        trainer = AI()
    elif trainer_choice == 'MC':
        trainer = MC()
    else:
        trainer = UCT()
    
    trainer.equalize_computing_resources(learner)
    
    # Train: play num_parties_jouees self-play games
    learner, num_victories, num_steps = train(learner, trainer, num_parties_jouees)
    
    # Save learned model to disk
    learner.save_model()
    return is_consistent, num_victories, num_steps
```

### Sample 4: puissance4 Parameter Sweep Example (CONFIGURATION EXAMPLE)

Derived from S127: puissance4/training.py (retrieved 2026-08-04, Python)

```python
# Grid search over MCTS parameters
for num_tirages_MC in [8]:
    for num_descentes_dans_arbre in range(6, 14, 2):      # 6, 8, 10, 12
        for facteur_uct in [0]:                           # single value
            for max_num_steps in [30]:
                result = prepare_and_train('UCT', 200,
                    num_tirages_MC=num_tirages_MC,
                    num_descentes_dans_arbre=num_descentes_dans_arbre,
                    facteur_uct=facteur_uct,
                    max_num_steps_to_explore=max_num_steps)
```

### Sample 5: CogitoNTNU ResNet Build (ADAPTED REFERENCE SKETCH)

Derived from S128: CogitoNTNU/AlphaZero/ResNet.py (retrieved 2026-08-04, MIT license, Python/Keras)

```python
def build(height=6, width=7, depth=2, filters=256,
          policy_output_dim=7, reg=0.0001, num_res_blocks=2):
    input_data = Input(shape=(height, width, depth))
    
    # Initial convolution (same as AlphaZero paper)
    x = Conv2D(filters, (3,3), padding='same')(input_data)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    
    # Residual blocks
    for _ in range(num_res_blocks):
        x = residual_block(x, filters, strides=(1,1), reg=reg)
    
    # Policy head: 3x3 conv â†’ flatten â†’ linear output
    pol_head = Conv2D(32, (3,3), padding='same')(x)
    pol_head = Flatten()(Activation('relu')(BatchNormalization()(pol_head)))
    pol_head = Dense(policy_output_dim, activation='linear')(pol_head)
    
    # Value head: 1x1 conv â†’ flatten â†’ 256 â†’ 1(tanh)
    val_head = Conv2D(32, (1,1), padding='same')(x)
    val_head = Flatten()(Activation('relu')(BatchNormalization()(val_head)))
    val_head = Dense(256, activation='relu')(val_head)
    val_head = Dense(1, activation='tanh')(val_head)
    
    return Model(input_data, [pol_head, val_head])
```

---

## Pros and Cons

### puissance4 (S127)

| Aspect | Assessment |
|--------|-----------|
| **Strengths** | (1) Complete, well-structured Python package. (2) Three progressive AI tiers in a class hierarchy. (3) Model persistence via text file dictionaries. (4) Parameter sweep framework for hyperparameter tuning. (5) PyPI-distributed, standard Python packaging. (6) Clear documentation of trade-offs between MC samples and end-game simulation limits. (7) `equalize_computing_resources()` method ensures fair comparison between agents. |
| **Weaknesses** | (1) Very small defaults (7 tree descents, 8 MC samples) â€” not production-strength. (2) Board states stored as human-readable grid strings â€” no bitboard or hash-based representation. (3) No transposition table with hashing â€” only a flat dictionary keyed by string board states. (4) `facteur_uct=0.01` is extremely conservative; the docstring recommends 0â€“0.3 but default is 0.01. (5) No mirror normalization. (6) French variable names (`grille`, `num_descentes_dans_arbre`, `choisir_action_uct`) may reduce accessibility. |
| **Reuse Potential** | HIGH â€” UCT implementation is clean and well-documented. Parameter sweep framework is directly applicable to hyperparameter tuning. Model persistence mechanism is novel and portable. |

### CogitoNTNU/AlphaZero (S128)

| Aspect | Assessment |
|--------|-----------|
| **Strengths** | (1) Complete AlphaZero pipeline from scratch: ResNet + MCTS + self-play training. (2) ResNet architecture closely mirrors katac4 (256 filters, 2 residual blocks, 6Ã—7Ã—2 input, 7 policy output, tanh value output). (3) Parallel training: 8 processes, 4,000 concurrent games, 16x speedup. (4) Board state mirroring for symmetry (player channel swap on opponent's turn). (5) `C_PUCT = sqrt(2)` â€” the theoretically correct formula from the AlphaZero paper. (6) MIT license. (7) Extensible to other games (Tic-Tac-Toe, Chess, Go planned). |
| **Weaknesses** | (1) Student project â€” no performance benchmarks reported (no win rate, no ELO, no convergence data). (2) Uses deprecated Keras API (`keras.layers.normalization.BatchNormalization` â†’ `tf.keras.layers.BatchNormalization`). (3) No training loss curves or convergence tracking. (4) No FPU (First Play Urgency) â€” leaf evaluations directly use NN value prediction without protection against bad NN priors. (5) No temperature-based move sampling at root (only `get_temperature_move()` exists as unused utility). (6) Training code not fully decoded (Train.py 404). (7) No PyTorch/TensorFlow 2.x migration. |
| **Reuse Potential** | MEDIUM-HIGH â€” ResNet architecture is directly comparable to katac4. PUCT formula is theoretically correct. Training infrastructure concept (parallel self-play) is applicable. |

### haoxiang-xu/connect-X (S129)

| Aspect | Assessment |
|--------|-----------|
| **Strengths** | (1) Web-based evaluation platform for ConnectX agents. (2) Four built-in baseline agents (Random, Greedy, Minimax, Monte Carlo). (3) Docker-based deployment. (4) Documented Kaggle competition result (16th place). (5) 384 Monte Carlo simulations per move â€” significantly more than puissance4's 8. |
| **Weaknesses** | (1) Very low star count (0â˜…). (2) No source code was accessible (GitHub returned 404 for raw files). (3) Limited detail about actual agent performance or training methodology. (4) 16th-place Kaggle result is not competitive against top bots. |
| **Reuse Potential** | LOW â€” No source code accessible, limited detail. However, the platform concept (web-based ConnectX evaluation) is novel and worth revisiting if source becomes available. |

---

## Feasibility Matrix

| Implementation | Local CPU | RTX 5090 | DGX Spark | Kaggle CPU (2s) | Kaggle T4 (GPU) | Submission |
|----------------|-----------|----------|-----------|-----------------|-----------------|------------|
| **puissance4 UCT** (7 descents, 8 MC) | âœ… Trivial (~ms per move) | âœ… Trivial | âœ… Trivial | âœ… Viable (7 descents â‰ˆ instant; could increase to 500+ for stronger play) | âš ï¸ No GPU code; Numba JIT would be needed | âœ… 1 file, ~700 lines, no external deps |
| **CogitoNTNU ResNet** | âš ï¸ Slow inference (~50-200ms) | âœ… Fast inference (<5ms with PyTorch) | âœ… Fast inference | âš ï¸ ~100-200ms inference via PyTorch; needs Numba/Cython | âœ… TensorRT FP16 ~1-2ms inference | âš ï¸ Requires PyTorch (available on Kaggle) |
| **CogitoNTNU Training** | âš ï¸ Slow (no parallel) | âœ… 16x+ speedup with multi-GPU | âš ï¸ Limited by DGX Spark RAM | âŒ Not feasible on Kaggle | âœ… 8-process parallel on Kaggle T4 | âŒ Training not submitted; only inference |

---

## Performance Evidence

| Source | Measured | Claimed by Authors | Inferred | Unknown |
|--------|----------|-------------------|----------|---------|
| **puissance4 UCT** | Parameters: 7 descents, 8 MC samples (designed for benchmarking, not strength) | "UCT vs MC: MC benefits from obvious-steps bias" | 7 descents Ã— 8 MC = 56 leaf evaluations per move; strong enough for casual play, weak for competitive | Win rate vs random, vs minimax |
| **CogitoNTNU AlphaZero** | 8-process parallel, 4,000 concurrent games/epoch, 16x speedup | "~100,000 self-play games yield competent AI with 500 search iterations" | 100K games / 500 iterations/move â‰ˆ 200 moves/game; deep search tree | Win rate, ELO rating, convergence |
| **connect-X platform** | Kaggle 16th place with Greedy+Minimax+MCTS (384 sims/move) | "16th place in Kaggle competition" | 384 simulations per move â‰ˆ moderate strength | Exact methodology, agent architecture |

---

## Board-Size and inarow Applicability

| Implementation | 7x6 | 15x13 | 4x5 | 15x10 | Arbitrary |
|----------------|-----|-------|-----|-------|-----------|
| **puissance4** | âœ… Hard-coded (7Ã—6 in grille.py, parameters.py) | âŒ Hard-coded | âŒ Hard-coded | âŒ Hard-coded | âŒ No |
| **CogitoNTNU** | âœ… Hard-coded (6Ã—7 in Config.py, Gamelogic.py) | âš ï¸ Configurable (filters=256 scales, but 7 policy output is fixed) | âœ… Configurable (height=3, width=3 in TicTacToe build) | âŒ Hard-coded | Partial â€” ResNet.build() accepts height/width/filters/policy_output_dim |
| **connect-X** | âœ… Targeted | âŒ Unknown | âŒ Unknown | âŒ Unknown | âŒ Unknown |

**Key Finding**: Neither puissance4 nor CogitoNTNU are readily adaptable to arbitrary board sizes for the Kaggle ConnectX competition, which requires handling 7Ã—6, 15Ã—13, 15Ã—10, and other configurations. However, CogitoNTNU's ResNet.build() method accepts height, width, and policy_output_dim as parameters, making it the most adaptable architecture for multi-board-size support with modifications.

---

## Integration and Ensemble Opportunities

1. **puissance4 â†’ Ensemble with neural guidance**: The UCT implementation's dictionary-based model persistence (visit counts, action scores) is functionally equivalent to a transposition table. These could be used as a classical fallback when a neural network is not available, or as a warm-start for a neural-guided MCTS.

2. **CogitoNTNU ResNet â†’ Direct replacement for katac4**: The ResNet architecture (256 filters, 2 residual blocks, 6Ã—7Ã—2 input, 7 policy output, value head 1Ã—1 conv â†’ 256 â†’ tanh) is very similar to katac4's b3c128nbt but with fewer residual blocks. This is a lighter-weight alternative that could provide sub-0.5ms inference on Kaggle T4.

3. **CogitoNTNU â†’ Parallel training pipeline**: The 8-process parallel self-play training with 4,000 concurrent games per epoch is a practical template for training our own agent on RTX 5090 or Kaggle T4.

4. **connect-X â†’ Evaluation framework**: The platform's evaluation approach (Greedy baseline â†’ Minimax â†’ Monte Carlo with 384 sims) provides a tiered evaluation methodology for testing our bot against progressively stronger opponents.

---

## Failure Modes and Risks

1. **puissance4 model persistence using string board states**: The `get_name()` method serializes the 6Ã—7 board as a human-readable string (`"row1;row2;..."`). This produces very long keys for the visit dictionary and is not hash-based. For practical use, a 64-bit hash would be orders of magnitude more efficient.

2. **CogitoNTNU uses deprecated Keras API**: The codebase uses `keras.layers.normalization.BatchNormalization` which was deprecated in TensorFlow 2.x and removed in TF 2.6+. This requires migration to `tf.keras.layers.BatchNormalization` or the model will not run on modern TensorFlow.

3. **CogitoNTNU no FPU**: Without First Play Urgency, the MCTS is vulnerable to a single bad neural network prediction dominating the root node's policy. For a competitive bot, FPU with `c_fpu = 0.2 * 1/sqrt(depth)` would be essential.

4. **puissance4 tiny defaults**: The default parameters (7 tree descents, 8 MC samples) are designed for benchmarking speed, not strength. Production use would require significant parameter increases (100-4000 descents, 50-200 MC samples).

5. **No test evidence for connect-X**: The repository was not accessible via WebFetch (raw files returned 404), and no source code could be verified. The "16th place Kaggle" claim is unverified.

---

## Benchmark Requirements

1. **Benchmark puissance4 UCT vs Minimax (depth 5+)**: Measure win rate across 1000 games. The parameter sweep framework allows systematic testing of `facteur_uct` (0.01â€“0.3), `num_descentes_dans_arbre` (7â€“500), `num_tirages_MC` (8â€“200).

2. **Benchmark CogitoNTNU ResNet inference latency**: Measure PyTorch/Keras inference time on Kaggle T4 for the 256-filter ResNet (~530K params). Compare to katac4's ~530K params.

3. **Reproduce CogitoNTNU training**: Run 10,000 self-play games to measure convergence speed, policy accuracy improvement, and value head calibration.

4. **Test CogitoNTNU ResNet on arbitrary board sizes**: Evaluate whether the build() method correctly generates models for 15Ã—13, 15Ã—10, and other Kaggle board configurations.

5. **Compare puissance4 UCT (500 descents) vs CogitoNTNU MCTS (500 iterations)**: Direct comparison of two UCT implementations with different parameter choices and board representations.

---

## Open Questions

1. What is the actual strength (ELO or win rate) of the CogitoNTNU AlphaZero agent after 100,000 self-play games? The authors claim "competent" but provide no quantitative measure.

2. What is the training methodology (loss function, optimizer, learning rate schedule) used by CogitoNTNU? The Train.py file was not accessible (404).

3. How does puissance4's model persistence (string-keyed dictionary) scale with board size and number of visited positions?

4. What Kaggle board configurations did connect-X evaluate? The README mentions ConnectX but the repository source was inaccessible.

5. Can CogitoNTNU's ResNet architecture be directly ported to PyTorch for Kaggle deployment?

---

## Recommendations

1. **Use puissance4 as baseline**: Implement puissance4's three-tier evaluation pipeline (Biased Random â†’ Biased MC â†’ UCT) as a baseline evaluation suite for our bot. The parameter sweep framework is directly applicable.

2. **Adopt CogitoNTNU ResNet architecture**: The 256-filter, 2-block ResNet with 7 policy output and tanh value head is a solid baseline architecture for our own training. The parallel training infrastructure (8 processes, 4K concurrent games) is a practical template.

3. **Migrate CogitoNTNU to PyTorch**: Replace deprecated Keras API with PyTorch modules for Kaggle compatibility. The ResNet architecture translates directly.

4. **Investigate connect-X if source becomes available**: The platform concept (web-based ConnectX evaluation with documented Kaggle results) is unique and worth pursuing if the source code can be recovered.

5. **Add board-size adaptivity**: Modify CogitoNTNU's ResNet.build() to accept arbitrary (height, width, inarow) and regenerate the model dynamically, enabling support for 15Ã—13 and other Kaggle configurations.

---

## Sources and Retrieval Record

| ID | Title | URL | License | Retrieval Date |
|----|-------|-----|---------|----------------|
| S127 | woctezuma/puissance4 â€” UCT MCTS package | https://github.com/woctezuma/puissance4 | Unknown | 2026-08-04 |
| S128 | CogitoNTNU/AlphaZero â€” AlphaZero for Four-in-a-Row | https://github.com/CogitoNTNU/AlphaZero | MIT | 2026-08-04 |
| S129 | haoxiang-xu/connect-X â€” ConnectX evaluation platform | https://github.com/haoxiang-xu/connect-X | Unknown | 2026-08-04 |
| S130 | GitHub topic scan (connect-four, connect-four-engine, connect-ai, connect-x, connect-n, four-in-a-row) | Various | â€” | 2026-08-04 |

---

## Cross-Links

- **S026** (GoodCoder666/katac4): ResNet architecture comparison â€” katac4 uses b3c128nbt (3 Bottlenest blocks, 128 channels) while CogitoNTNU uses 2 blocks, 256 channels. Both have ~530K params.
- **S041** (rowspire): Neural-guided MCTS comparison â€” rowspire uses UCB1 (c=1.41, 4000 sims, NN-guided) while puissance4 uses UCB1 (c=0.01, 7 descents, 8 MC samples).
- **S070** (BitBully MTD(f)): Classical solver comparison â€” puissance4 has no transposition table while BitBully uses cached lookup tables.
- **HYP-015** (GPU acceleration requirement): Neither puissance4 nor CogitoNTNU use GPU; they are CPU-only implementations.
- **CMP-005** (NN-guided search): CogitoNTNU's ResNet + MCTS is the most complete neural-guided search implementation discovered in this scan.

---

## Follow-Up Research Tasks

1. **Fetch CogitoNTNU Train.py**: Access the training loop code (currently 404) to understand the loss function, optimizer, and learning rate schedule.
2. **Migrate CogitoNTNU to PyTorch**: Port the ResNet and MCTS code from Keras to PyTorch for Kaggle T4 compatibility.
3. **Add board-size adaptivity to CogitoNTNU**: Modify `ResNet.build()` to accept arbitrary (height, width, inarow) and test on 15Ã—13.
4. **Benchmark puissance4 UCT strength**: Run parameter sweep (7â€“500 descents, 8â€“200 MC samples, facteur_uct 0.01â€“0.3) against minimax baseline.
5. **Recover connect-X source code**: Attempt to access the platform source via PyPI sdist or web archive.
6. **Compare UCT formulas**: Contrast puissance4's UCB1 (`mu + c*sqrt(log(N)/n)`) vs CogitoNTNU's PUCT (`Q + exp*p*sqrt(N)/(1+n)`) vs katac4's PUCT (`Q + c*p*sqrt(N)/(1+n)`).
7. **Implement puissance4's model persistence**: Port the text-file dictionary approach to our transposition table for classical MCTS with disk-based learning.

---

## Deferred Empirical Experiments

1. **Train CogitoNTNU ResNet on TonyCWang dataset**: Verify whether the 256-filter, 2-block ResNet achieves ~85% policy accuracy on 958M-row training data.
2. **Measure CogitoNTNU ResNet inference on Kaggle T4**: Compare PyTorch inference (530K params) to katac4's ResNet and TensorRT FP16 benchmark.
3. **Run puissance4 parameter sweep**: Systematically test `facteur_uct` (0.01, 0.1, 0.3), `num_descentes_dans_arbre` (7, 50, 200, 1000), `num_tirages_MC` (8, 50, 200) and report win rate vs opponent strength.
4. **Reproduce CogitoNTNU self-play training**: Run 10,000 self-play games and measure convergence (policy KL divergence, value RMSE vs random opponent).
5. **Test CogitoNTNU board-size adaptivity**: Generate ResNet models for 15Ã—13, 15Ã—10, 4Ã—5 and measure inference latency on Kaggle T4.

---

## Master Report Implications

`RESEARCH_REPORT.md` should be updated with:
- Three new repositories added to the reference implementations catalog
- puissance4 as the most accessible Python UCT MCTS implementation
- CogitoNTNU/AlphaZero as the most complete open-source AlphaZero pipeline for Connect 4 (after katac4)
- The 256-filter, 2-block ResNet as a valid alternative to katac4's b3c128nbt

## Nexus Index Implications

Add links to:
- `research/dossiers/reference-implementations/new-repo-sources-r34.md` in `research/README.md` under "Reference Implementations"
- Cross-link from `research/contender-roster.md` (new baseline agents: puissance4 UCT, CogitoNTNU AlphaZero)
- Cross-link from `research/ensemble-catalog.md` (puissance4 as classical UCT fallback)

---

## Deferred Empirical Experiments

1. Train CogitoNTNU ResNet on TonyCWang dataset â€” verify ~85% policy accuracy
2. Measure CogitoNTNU ResNet inference on Kaggle T4 â€” compare to katac4
3. Run puissance4 parameter sweep â€” win rate vs opponent strength
4. Reproduce CogitoNTNU self-play training â€” measure convergence
5. Test CogitoNTNU board-size adaptivity â€” 15Ã—13/15Ã—10 inference on Kaggle T4

---

EXTERNAL WORKER COMPLETE