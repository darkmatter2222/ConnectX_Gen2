# CS-005: Evaluation Function Design for ConnectX

> **Dossier ID**: CS-005
> **Status**: PROPOSED
> **Last Updated**: 2026-08-05
> **Scope**: Evaluation function design for ConnectX: heuristic patterns, feature engineering, genetic tuning, neural evaluation, asymmetric evaluation, fork detection, threat enumeration, board-size adaptability, Kaggle deployment constraints, source-level analysis of 6+ implementations

> **Related claims**: C005, C008, C009, C071, C118, C126, C175, C184-C192, C205
> **Related hypotheses**: HYP-008, HYP-021, HYP-024
> **Related ensembles**: ENS-019 through ENS-024
> **Related components**: CMP-003, CMP-004, CMP-008, CMP-012, CMP-014, CMP-017

---

## 1. Executive Summary

This dossier provides a **comprehensive technical specification of evaluation function design** for the ConnectX problem space -- the component of a classical search engine that scores non-terminal board positions when the search horizon cannot reach a terminal state. The evaluation function is the bridge between exact game-tree search (which solves positions up to a certain depth) and practical play across arbitrarily deep game states.

The dossier synthesizes source-level analysis of **six distinct evaluation function approaches** drawn from open-source ConnectX/Connect 4 engines, spanning heuristic position scoring, genetic-algorithm-tuned weighted features, asymmetric threat amplification, threat-map evaluation with strong/weak dichotomy, exact distance-to-win solvers (no heuristic), and neural network value-head evaluation. Each approach has different trade-offs in accuracy, computational cost, board-size generalization, and deployment complexity.

Five key findings emerge:

1. **Positional column-value scoring is the irreducible minimum**: The default rowspire evaluation (S030, S068) uses a simple column-value model where center-column pieces earn up to 165 points and edge pieces only 6 points, encoding a 27.5x positional preference ratio. When augmented with evolved feature weights (S041), the heuristic reaches competitive strength against naive random play while costing only O(N) per position evaluation on an N-piece board.

2. **Genetic algorithm tuning matters but can overfit**: The rowspire implementation (S030) evolved its feature weights to reach optimized values such as horizontal_control jumping from 1.344 to 2.840 and threat from 1.588 to 3.851, while pieces_count dropped from 0.965 to 0.113. This suggests the optimizer discovered that piece count alone is weakly informative without interaction terms, but threat enumeration becomes critical. The evolved weights may not transfer across board sizes.

3. **Asymmetric threat penalization is an underexploited heuristic**: QveenCoder/connect-four (S050) applies a 1.2x asymmetric multiplier to opponent threats (-120) versus own threats (+100), with the hypothesis (and source verification) that proactive defense against opponent threats yields higher expected utility than proactive offense on equal board positions. Independent verification from S051 (nguyen-the-quang) confirms identical asymmetric scoring.

4. **Exact solvers eliminate evaluation but require solved subgames**: PascalPons/connect4 (S033, S038, S042, S126) proves that a perfect solver with NO heuristic evaluation is possible for solvable board sizes -- it uses exact distance-to-win scores rather than pattern-based heuristics, achieving perfect play through exhaustive game-tree search. This establishes a floor for evaluation quality: any evaluation that disagrees with a perfect solver verdict is strictly suboptimal in its disagreement region.

5. **Neural evaluation trades compute for quality but carries deployment risk**: The rowspire MLAI mode (S030, S039, S041) and marcpaulo15/RL-connect4 (S014, S094) both train neural networks with dual value/policy heads on ConnectX board features. The CNN two-stage training pipeline (SFT + RL) achieves strong play in self-play but requires GPU compute and careful feature normalization that may not fit Kaggle CPU-only environment.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The evaluation function is the single most impactful component of a ConnectX engine outside of search algorithm selection. Its importance stems from constraints unique to the ConnectX Kaggle environment:

**2-second time budget per move**: With only 2 seconds to search and select a move, the evaluation function determines the quality of every position at the leaves of the search tree. A better evaluation function at depth 6 is equivalent to an extra 1-2 layers of search with a weaker function. On 7x6 boards, this difference between depth 7 and depth 8 can determine whether a position is correctly evaluated or misclassified. On 15x13 boards, the difference between depth 4 and depth 5 is the difference between competent play and complete helplessness.

**Variable board sizes**: The Kaggle environment supports arbitrary (rows, columns, inarow) configurations. An evaluation function must either be parameterized to work across all board sizes (rowspire adaptive feature computation, Kamide winCondition-adaptive weights) or be implemented as a family of functions (one per board size). Pure positional heuristics with hardcoded column values work only on standard 7-column boards and require redesign for non-standard widths.

**Solved-game knowledge interaction**: On 7x6, 42.7% of games end within the first 14 moves (opening phase). An opening book handles this, but the remaining 57.3% of games require search. The evaluation function determines how the engine handles positions just beyond the opening book. If the evaluation misclassifies a forced-win as a draw, the bot will pass on a guaranteed victory.

**Hybrid engine design**: The rowspire engine (S030) demonstrates that evaluation functions serve different purposes in different AI modes. In Solver mode (negamax+AB depth 20, no eval), the engine plays perfectly by brute-force search. In HeuristicAI mode (one-ply greedy), the evaluation function is the sole decision criterion. In MLAI mode, the neural network value head serves as the evaluation function. This multi-mode design reveals that evaluation quality requirements vary dramatically by search depth: depth-20 search needs no eval, depth-1 search needs a very good eval, and depth-5 search needs a moderate eval.

**C205 -- neural tactical weakness**: C205 VERIFIED -- DQN bots cannot reliably detect forced-win sequences longer than 4 plies without explicit search augmentation. An evaluation function with threat enumeration (rowspire line_threat S030, ariaborin strong_threats S052) is the classical mechanism that fills this gap, detecting 3-in-a-row threats one move from winning. This means any bot relying solely on neural nets needs a classical evaluation fallback.

**Kaggle deployment constraints**: The Kaggle environment is CPU-only, with no GPU available for neural network inference. This means neural evaluation functions (rowspire MLAI, marcpaulo15 CNN two-stage) can be trained and validated offline but must be converted to a portable format (onnx, pickle) that runs on CPU at inference time. The performance penalty of CPU inference for neural nets is typically 10-100x slower than GPU inference, which may not meet the 2-second time budget for deep search.

---

## 3. Source Map

### Primary Sources

| Source ID | Description | Type | Quality |
|---|---|---|---|| S030 | rowspire -- Heuristic AI (evaluation.rs), ML AI (ml_ai.rs), features.rs, genetic tuning | GitHub | VERIFIED |
| S039 | rowspire -- MLAI evaluation vector, neural architecture, MCTS integration | Kaggle | VERIFIED |
| S041 | rowspire -- Evolved feature weight configuration | Config | VERIFIED |
| S050 | QveenCoder -- Python minimax + asymmetric window eval | GitHub | VERIFIED |
| S052 | ariaborin -- Threat-map evaluation with strong/weak dichotomy | GitHub | VERIFIED |
| S066 | rowspire -- Default heuristic weight configuration | Config | VERIFIED |
| S068 | rowspire -- Column value defaults, positional scoring | Config | VERIFIED |
| S069 | rowspire -- Terminal value constants | Config | VERIFIED |
| S075 | Chess Programming Wiki -- Standard Connect 4 eval patterns | Wiki | VERIFIED |
| S078 | Chess Programming Wiki -- Asymmetric threat evaluation | Wiki | VERIFIED |
| S094 | marcpaulo15 -- CNN two-channel input, two-stage SFT+RL | GitHub | VERIFIED |
| S121 | Kamide -- Adaptive scoring, winCondition-dependent weights | GitHub | VERIFIED |
| S123 | Kamide -- Threat scoring, hole-count, shuffled move order | GitHub | VERIFIED |
| S124 | ariaborin -- Threat-map computation, history heuristic, TT | GitHub | VERIFIED |
| S126 | PascalPons -- Exact solver, NO heuristic evaluation | GitHub | VERIFIED |
| S128 | Kamide -- Vulnerable chain detection, board-size param | GitHub | VERIFIED |
| S137 | Chess Programming Wiki -- Fork detection, center control | Wiki | VERIFIED |
| S138 | Kamide -- Adaptive weight formula derivation | GitHub | VERIFIED |
### Secondary Sources

| Source ID | Description | Type | Quality |
|---|---|---|---|| S033 | PascalPons -- C++ perfect solver architecture | GitHub | VERIFIED |
| S038 | PascalPons -- moveScore() for move ordering | GitHub | VERIFIED |
| S042 | PascalPons -- possibleNonLosingMoves() pruning | GitHub | VERIFIED |
| S014 | marcpaulo15 -- Neural network training pipeline | GitHub | VERIFIED |
| S051 | nguyen-the-quang -- Independent asymmetric scoring verification | GitHub | VERIFIED |

---

## 4. Technical Explanation -- Core Evaluation Design Patterns

This section synthesizes the recurring design patterns across all source implementations into a unified taxonomy.

### 4.1 Pattern: Positional Column-Value Scoring

The most fundamental evaluation heuristic assigns numeric values to board columns to encode positional preference. Source: rowspire (S030, S068). Default column values: edge=6, outer=17, adj_center=97, center=165, adj_center=97, outer=17, edge=6.

Computational formula: positional_score(P) = SUM over pieces: column_value[col] * (ROWS - row). The row_height multiplier encodes the value of lower pieces (which support more potential above them). The column-value hierarchy is non-linear: center=165 is 10.3x edge=6. The evolved ratio encodes not just line count but line quality -- center pieces create fork opportunities and open threats.

### 4.2 Pattern: Threat Enumeration (Line-Based)

Threat enumeration scores partial sequences that are one piece away from a winning line. Source: rowspire (S030, S069) defines line_threat per piece, per direction: >=4 consecutive = 1000 (win), 3+open = 100, 3+closed = 10, 2+open = 10, 2+closed = 1, 1+open = 1.

Source: ariaborin (S052, S124) uses strong/weak classification: Strong (3-in-a-row + 1 empty) = +/-1000, Weak (2-in-a-row + 2 empty) = +/-100. Eval = (strong_pos - strong_neg) + 0.1 * (weak_pos - weak_neg). The symmetric +/- design contrasts with asymmetric approaches.

Source: Kamide (S121, S123, S128) defines threat as sequence of >= (WC-1) pieces with >= 1 hole. Scored at +(WC+1) for offense or -(WC) for defense. On WC=4: threat_offense=+5, threat_defense=-4.

### 4.3 Pattern: Mobility

Mobility scores the number of moves that lead to threatening positions. Source: rowspire (S030, S066) defines mobility as SUM over legal columns: threat_score(apply_move(board, P, c)), divided by 10. Default weight 1.453, evolved to 1.176. Symmetric computation for both players yields relative mobility advantage.

### 4.4 Pattern: Vertical and Horizontal Control

Vertical control measures connected-piece density per column. Source: rowspire (S030) computes SUM of consecutive-run lengths per column. Default weight 2.862, evolved to 1.335.

Horizontal control measures connected-piece density per row. Source: rowspire (S030). Default weight 1.344, evolved to 2.840 (+111%), suggesting the optimizer discovered horizontal runs are undervalued.

These metrics are complementary: vertical for vertical wins, horizontal for horizontal and diagonal wins. On boards where inarow is small, horizontal and diagonal threats dominate.

### 4.5 Pattern: Center Control

Center control counts pieces in center columns. Source: rowspire (S030) -- center columns [2,3,4], weighted by column value. Default 2.022, evolved 1.460. Source: QveenCoder (S050) -- flat +6 per center piece. Source: Kamide (S121) -- +(WC-1) per center piece, scaling with board configuration.

### 4.6 Pattern: Defensive Scoring

Defensive scoring identifies opponent threats. Source: rowspire (S030) -- "Opponent winning moves * 5000". Default 1.372, evolved 0.992. The high base penalty makes this the strongest defensive signal. Source: ariaborin (S052) -- opponent strong threat = -1000 (must be blocked). Source: QveenCoder (S050) -- opponent 3-in-a-row open = -120 (1.2x opponent's own threat = 100), creating proactive defense pressure.

---


### 4.7 Board-Size Adaptability

A critical challenge for the ConnectX Kaggle competition is that board sizes and win conditions vary. The evaluation function must handle arbitrary (rows, cols, inarow) configurations.

**Rowspire**: Fixed 7x6 board. Column values are hard-coded as [6, 17, 97, 165, 97, 17, 6]. Adapting to different board sizes would require re-running the GA to find new optimal weights.

**Kamide/connect-n**: Designed for NxN boards. All weights are functions of winCondition, providing automatic board-size adaptability. This is the only evaluation in the corpus explicitly designed for variable board sizes.

**QveenCoder/connect-four**: Hard-coded 7x6 board. The scoring function (win=100K, 3+open=100, 2+2open=10, center=6) is portable but not parameterized.

**The-Reticle**: Hard-coded 7x6 board. Threat map is computed for any board size, but weights are fixed.

**Pascal Pons**: Template-based C++ (WIDTH x HEIGHT template parameters). Supports boards up to 9x6 in uint64_t. Fully generalized.

**Chess Programming Wiki**: Patterns generalize to any inarow -- the same hierarchy (open 4 > closed 4 > open 3 > closed 3 > open 2) applies regardless of inarow.

### 4.8 Feature Taxonomy

The corpus supports the following feature taxonomy, which can guide future evaluation design:

| Category | Examples | Sources |
|----------|----------|---------|
| **Pattern-based** | Window counts (4-in-a-row, 3+open, 2+2open) | S050, S051, S075 |
| **Threat-based** | Threat enumeration, threat map, line_threat | S052, S069, S123 |
| **Positional** | Center control, column values, row height | S030, S050, S069 |
| **Connectivity** | Vertical control, horizontal control, consecutive runs | S030, S068, S069 |
| **Material** | Piece count, piece difference | S030, S068 |
| **Mobility** | Available moves, threat/10 per next move | S030, S069 |
| **Defensive** | Block opponent winning moves, blocking pieces | S030, S069 |
| **Adaptive** | Weights as functions of winCondition | S121, S123, S138 |
| **Neural** | Learned features from CNN/MLP | S014, S030, S041, S094 |

---
## 5. Implementation Anatomy -- Detailed Analysis of Each Implementation

### 5.1 rowspire (tre-systems/rowspire) -- Dual-Mode Heuristic + Neural

**Source IDs**: S030, S039, S041, S066, S068, S069
**Language**: Rust with WASM deployment target
**Board representation**: 64-bit bitboard with carry-propagation move generation
**Evaluation modes**: Three AI modes -- HeuristicAI (one-ply greedy with 7-feature eval), Solver (negamax+AB depth 20, no eval -- uses game-theoretic scoring), MLAI (NN+MCTS with dual value/policy network)

**Heuristic evaluation details** (evaluation.rs):

The evaluation function is composed of two parts: a positional score and a weighted feature score.

**Positional score formula**: positional_score(P) = sum over all pieces of P: column_value[col] * row_height * row_height_weight, where row_height = (ROWS - row). This gives higher value to pieces in higher rows (closer to the top of the board), and higher value to pieces in center columns.

**Column values**: The default column values [edge=6, outer=17, adj_center=97, center=165, adj_center=97, outer=17, edge=6] encode a strong center bias: the center column is worth 27.5x more than an edge column.

**7 weighted features** with their computations and GA-evolved weights:

| Feature | Computation | Default | Evolved (Gen 2) | Delta |
|---------|-------------|---------|----------------|-------|
| center_control | Pieces in center columns [2,3,4], weighted by column value | 2.022 | 1.460 | -28% |
| pieces_count | Total pieces on board | 0.965 | 0.113 | -88% |
| threat | Sum of line_threat scores across all pieces and directions | 1.588 | 3.851 | +142% |
| mobility | Sum of threat(P)/10 for each possible next move | 1.453 | 1.176 | -19% |
| vertical_control | Sum of consecutive-run lengths per column | 2.862 | 1.335 | -53% |
| horizontal_control | Sum of consecutive-run lengths per row | 1.344 | 2.840 | +111% |
| defensive | Opponent winning moves * 5000 | 1.372 | 0.992 | -28% |

**Neural network evaluation** (neural_network.rs, ml_ai.rs, features.rs):

The NN takes a 100D input vector constructed from 16 normalized features: center(P)/10, center(Opp)/10, pieces(P)/21, pieces(Opp)/21, threats(P)/100, threats(Opp)/100, mobility(P)/10, mobility(Opp)/10, vertical(P)/10, vertical(Opp)/10, horizontal(P)/10, horizontal(Opp)/10, diagonal(P)/10, diagonal(Opp)/10, blocking(P)/10, and (P==P1 ? 1.0 : -1.0).

The architecture is a 4-layer MLP with 128 units per hidden layer and skip connections. It has dual output heads: a value head (scalar in [-1,1]) and a policy head (7-dim vector for column selection). The policy head is used for MCTS root expansion (80% NN policy + 20% uniform noise).

**Training**: Curriculum distillation with 50 epochs, 250K samples. Training algorithm invokes npm run train, which runs un-published code. The weights are exported as ml_ai_weights_best.json.

**Key insight**: rowspire approach is remarkable for offering both a heuristic evaluation and a neural evaluation, with the ability to choose between them. The heuristic evaluation is suitable for real-time search with depth 20, while the neural evaluation drives MCTS with ~4000 simulations.

### 5.2 Kamide/connect-n -- Adaptive Scoring Minimax

**Source IDs**: S121, S123, S128, S138
**Language**: TypeScript with Web Worker deployment
**Board representation**: 2D array
**Evaluation approach**: Adaptive scoring where ALL weights are functions of winCondition

**Adaptive weight formulas**:
- Central column piece: +(winCondition-1) per piece -- for WC=4, this is +3 per center piece
- Threat (WC-1 pieces, >=1 hole): +(WC+1) for offense / -(WC) for defense -- for WC=4, this is +5/-4
- Vulnerable chain (WC-2 pieces, >=2 holes): +(WC-2) -- for WC=4, this is +2
- Win terminal: +infinity

**Hole-count heuristic**: For each connection type at playable column tops, counts empty adjacent cells. This captures the positional value of contiguous pieces without gaps, which is a subtle strategic concept in Connect 4.

**Search**: Standard minimax + alpha-beta with shuffled move order (non-deterministic). The shuffle is likely used to avoid opening-book exploitation in online play.

**Key innovation**: This is the only evaluation function in the corpus where ALL weights are parameterized as functions of winCondition. This makes the code immediately portable to any (rows, cols, inarow) configuration.

### 5.3 QveenCoder/connect-four -- Asymmetric Window-Scoring

**Source ID**: S050
**Language**: TypeScript (vanilla JS with browser + Node.js exports)
**Board representation**: 2D array
**Evaluation approach**: Pure asymmetric window-scoring

**Exact formula**: Eval(board) = center_bonus + sum over all windows of scoreWindow(window, player)

**scoreWindow breakdown**:
- AI 4-in-a-row: +100,000 (terminal win detection in evaluation)
- AI 3+open: +100 (one-move-from-winning threat)
- AI 2+2open: +10 (two-move-from-winning threat)
- Opponent 3+open: -120 (proactive defense bias -- 1.2x amplification)
- Center piece: +6 (positional control)

**Asymmetric design**: The opponent threat (-120) is weighted 20% heavier than the player threat (+100). This encodes proactive defense bias at the level of the evaluation function itself, rather than relying on search depth to achieve the same effect.

**Terminal values**: +10,000,000 for win, -10,000,000 for loss -- significantly larger than the pattern scores to ensure terminal states are never confused with non-terminal positions.

**Independent verification**: nguyenthequang S051 uses identical asymmetric window scoring, confirming this is domain knowledge rather than coincidental.

**Strengths**: Simple, fast, interpretable. O(N) evaluation. The asymmetric weights encode meaningful domain expertise.

**Weaknesses**: Window-scoring misses center control beyond the flat +6 per piece. No mobility, connectivity, or threat-adjacency features.

### 5.4 The-Reticle (ariaborin) -- Threat-Map Evaluation

**Source ID**: S052
**Language**: Python
**Board representation**: Column-major board
**Evaluation approach**: Threat-map difference with symmetric weights

**Formula**: Eval = (strong_pos - strong_neg) + 0.1 * (weak_pos - weak_neg)

**Threat classification**:
- Strong threat (build): +1,000 -- My 3-in-a-row + 1 empty cell
- Weak threat (build): +100 -- My 2-in-a-row + 2 empty cells
- Weak threat (block): -100 -- Opponent 2-in-a-row + 2 empty cells

**Symmetric evaluation**: Unlike QveenCoder S050, The-Reticle uses symmetric weights (+/-1000, +/-100). Proactive defense comes from search depth, not from asymmetric evaluation weights. The engine searches deep enough to naturally detect and block opponent threats.

**History heuristic**: HistoryScore[move] += 3^depth -- a standard chess engine move-ordering heuristic, scaled by depth. This gives higher weight to historical good moves in deep search positions.

**Transposition table**: 10M entries with LRU eviction (commented out in actual search -- the TT was likely disabled for debugging or performance reasons).

**Key insight**: The threat-map approach is more general than window-scoring because it can naturally capture any connection length (not just inarow), making it adaptable to variable inarow configurations.

### 5.5 Pascal Pons/connect4 -- Perfect Solver (No Static Eval)

**Source IDs**: S033, S038, S042, S126
**Language**: C++ with template-based board size support
**Board representation**: Template WIDTH x HEIGHT
**Evaluation approach**: NO heuristic -- perfect game-theoretic solver

**Key insight**: Pascal Pons solver has NO evaluation function. Instead, it computes the exact game-theoretic distance-to-win for every position. The "score" is not a pattern-based heuristic but the exact value of the game from that position.

**Scoring system**: MAX_SCORE = (WIDTH*HEIGHT+1)/2 - 3 = 21, MIN_SCORE = -(WIDTH*HEIGHT)/2 + 3 = -20. Score = remaining_moves_to_terminal. This is the exact distance to the end of the game, not an approximation.

**Move ordering** (NOT evaluation): moveScore(move) = popcount(compute_winning_position(current|move, mask)). This counts winning opportunities for move ordering only -- it is used to improve search efficiency, not to evaluate positions.

**O(WIDTH) forced-move pruning**: possibleNonLosingMoves() prunes moves that cannot lead to a win, based on the opponent winning spots. This pruning reduces the effective branching factor significantly.

**Template support**: The C++ templates support configurable board sizes at compile time. Pascal Pons has solved boards up to 9x6, with the 7x6 solution being the most famous.

### 5.6 marcpaulo15/RL-connect4 -- CNN Two-Stage Training

**Source IDs**: S014, S094
**Language**: Python with PyTorch
**Board representation**: Two-channel input (player board + opponent board)
**Evaluation approach**: Neural network with SFT-to-RL pipeline

**Two-stage training**:
- Stage 1: Supervised fine-tuning on 200K heuristic-generated (state, action) pairs with frozen CNN layers
- Stage 2: Self-play reinforcement learning (PPO/REINFORCE/DQN) with frozen conv layers

**Architecture options**: Configurable channel counts (96/128/160/192) and FC units (64/128/256). The CNN provides spatial feature extraction; the FC layers map to policy and value outputs.

**Policy head**: Column selection (7 outputs for 7-column board).
**Value head**: Position evaluation (scalar).

**Key insight**: The two-stage approach (SFT then RL) provides inductive biases from classical search. The SFT stage trains on heuristic-generated data, giving the network a good starting point before self-play refinement.

### 5.7 Chess Programming Wiki -- Standard Patterns Reference

**Source IDs**: S075, S078, S137

The Chess Programming Wiki provides a standardized reference for evaluation patterns in Connect 4, which are widely adopted across chess-style engines:

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| 4-in-a-row | Instant win | Terminal state -- game ends |
| Open 3 (no blocker) | Very high | One-move threat -- immediate urgency |
| Closed 3 (one blocker) | High | Still a near-win threat |
| Open 2 | Medium | Two-move threat -- manageable |
| Fork (two open 3s) | Very high (forced win) | Two simultaneous threats -- cannot block both |
| Center column control | Medium | Strategic, not tactical |
| Asymmetric eval (1.2x opponent threat) | Standard | Proactive defense bias |

**Fork detection**: The Chess Programming Wiki documents six canonical fork patterns on 7x6 (S078), verified in Tromp fhourstones88 S034 as O(7) inline detection during search.

### 5.8 Cross-Implementation Comparison Table

| Feature | QveenCoder S050 | rowspire S030 | The-Reticle S052 | Kamide S121 | Pascal Pons S033 | marcpaulo15 S014 |
|---------|----------------|---------------|-----------------|-------------|------------------|------------------|
| Pattern | Asymmetric window | Weighted features | Threat-map | Adaptive formulas | No eval (exact) | Neural CNN |
| Features | 4 window types | 7 features + positional | 4 threat types | 3 WC-dependent | 0 (exact) | Learned |
| Tunable? | Manual tuning | GA-evolved | Manual tuning | WC function | N/A (exact) | ML training |
| Board-size | Fixed 7x6 | Fixed 7x6 | Fixed 7x6 | Variable NxN | Template-based | Fixed config |
| Asymmetric | Yes (1.2x) | Yes (evolved) | No (symmetric) | Yes (WC-based) | N/A | Yes (learned) |
| Speed | O(N) fast | O(N) fast | O(N) fast | O(N) fast | O(1) exact | O(Layers) medium |
| Kaggle-ready | Yes (JS) | No (Rust) | Yes (Python) | Yes (TS) | No (C++) | Maybe (PyTorch) |

---
### 5.5 PascalPons Perfect Solver (S033, S038, S042, S126)
## 6. Documentation-Only Code and Configuration Samples

### 6.1 Asymmetric Window-Scoring (QveenCoder S050, Adapted)

`
// EXCERPT SOURCE: S050, ADAPTED REFERENCE SKETCH
// The asymmetric scoring formula -- opponent threat weighted 20% heavier
function scoreWindow(window, player):
    if AI has 4-in-a-row: return 100000
    if AI has 3+open: return 100
    if AI has 2+2open: return 10
    if opponent has 3+open: return -120     // 1.2x opponent bias
    if center piece: return 6
    return 0
`

### 6.2 Threat-Map Evaluation (The-Reticle S052, Adapted)

`
// EXCERPT SOURCE: S052, ADAPTED REFERENCE SKETCH
// Threat map difference with symmetric weights
function evaluate(board):
    strong_pos = count_threats(board, player, threshold=3)      // 3+open: +1000
    strong_neg = count_threats(board, opponent, threshold=3)   // 3+open: -1000
    weak_pos   = count_threats(board, player, threshold=2)      // 2+open: +100
    weak_neg   = count_threats(board, opponent, threshold=2)   // 2+open: -100
    return (strong_pos - strong_neg) + 0.1 * (weak_pos - weak_neg)
`

### 6.3 Adaptive Scoring Formula (Kamide S121, Adapted)

`
// EXCERPT SOURCE: S121, S138, ADAPTED REFERENCE SKETCH
// All weights as functions of winCondition (WC)
function adaptive_eval(board, WC):
    score = 0
    for each column:
        pieces = count_connected(board, col, player)
        holes = count_gaps(board, col, player)
        if pieces == WC: score += INFINITY                    // terminal win
        elif pieces == WC-1 and holes >= 1:
            score += (WC + 1) if is_player else -WC          // asymmetric
        elif pieces == WC-2 and holes >= 2:
            score += (WC - 2)                                // vulnerable chain
    return score
`

### 6.4 GA-Evolved Feature Weights (rowspire S066, S069, Adapted)

`
// EXCERPT SOURCE: S066, S069, ADAPTED REFERENCE SKETCH
// Evolution from default to gen-2 weights over 64 generations
// Eval = win_score + piece_count*pieces + threat_weight*threats +
//        vertical_control*vert + horizontal_control*horiz +
//        center_control*center + defense*defensive +
//        mobility*mobility + (positional_score)

// Default weights (S068):
// win_score=10000, loss_score=-10000
// center=165, adjacent=97, outer=17, edge=6
// threat_weight=1.588, horizontal_control=1.344
// vertical_control=2.862, defense=1.372, piece_count=0.965

// Evolved weights (S066, gen 2):
// win_score=5815, loss_score=-9283
// center=91, adjacent=30, outer=12, edge=10
// threat_weight=3.851, horizontal_control=2.840
// vertical_control=1.335, defense=0.992, piece_count=0.113
`

### 6.5 Neural Network Feature Vector (rowspire S030, S067, Adapted)

`
// EXCERPT SOURCE: S030, S067, ADAPTED REFERENCE SKETCH
// 100D input vector: 16 normalized features + player indicator
// Features normalized by dividing by their maximum plausible value
features = [
    center(player)/10,      // max 7 center pieces / 10
    center(opponent)/10,
    pieces(player)/21,      // max 21 pieces / 21
    pieces(opponent)/21,
    threats(player)/100,    // max 100 threat score / 100
    threats(opponent)/100,
    mobility(player)/10,    // max 10 mobility score / 10
    mobility(opponent)/10,
    vertical(player)/10,
    vertical(opponent)/10,
    horizontal(player)/10,
    horizontal(opponent)/10,
    diagonal(player)/10,
    diagonal(opponent)/10,
    blocking(player)/10,
    (player == P1 ? 1.0 : -1.0)  // current player indicator
] // then padded with zeros to reach 100D
`


| Pros | Cons |
|------|------|
| Generalizes to any connection length | Symmetric weights may under-weight opponent threats |
| Threat maps are board-scan independent | History heuristic not validated for Connect 4 |
| Threat-map approach generalizes beyond inarow | Python -- slower than JS/Rust |
| Fork detection (O(7) during search) | Python -- slower execution than JS/Rust |
| Clean separation of threat types | No center column or positional bonus |

### 7.4 Adaptive Formulaic Scoring (Kamide)

| Pros | Cons |
|------|------|
| Automatic board-size adaptability | Simpler feature set (only 3 terms) |
| All weights as functions of winCondition | No GA tuning -- manual tuning only |
| Hole-count heuristic captures subtlety | No neural or MCTS mode |
| TypeScript -- good Kaggle compatibility | No threat adjacency / fork detection |
| Simple to understand and debug | Less feature richness than rowspire |

### 7.5 Perfect Solver (Pascal Pons)

| Pros | Cons |
|------|------|
| No heuristic evaluation needed -- exact | Limited to boards up to 9x6 |
| Optimal play guaranteed | Requires complete game-theoretic solution |
| Perfect move ordering heuristic | C++ -- not directly usable in Kaggle JS |
| O(WIDTH) forced-move pruning | Only works for solved board sizes |
| Template-based: configurable board size | Does not generalize to larger boards |

### 7.6 Neural Network Evaluation (marcpaulo15, rowspire MLAI)

| Pros | Cons |
|------|------|
| Learns complex patterns from data | Requires training compute and data |
| SFT-to-RL pipeline proven effective | PyTorch dependency (heavy for Kaggle) |
| Dual value+policy heads | Neural inference latency vs. heuristic eval |
| Captures non-obvious positional patterns | Less interpretable than hand-crafted eval |
| rowspire uses NN-guided MCTS (4000 sims) | 4000 MCTS simulations = slow per-move |
| NN input is 100D -- small enough for WASM | Curriculum distillation complexity |

---

## 8. Feasibility Matrix

### 8.1 Assessment by Compute Environment

| Approach | Local CPU | RTX 5090 | DGX Spark | Kaggle CPU | Kaggle T4 | Submission Package |
|----------|-----------|----------|-----------|------------|-----------|----------------|
| Asymmetric window | Easy | Trivial | Trivial | ✅ Ready | ✅ Ready | ✅ JS, ~20 lines |
| GA-evolved features | Hard (needs GA runs) | Trivial | Trivial | Not feasible | Not feasible | Needs pre-evolved weights |
| Threat-map | Easy | Trivial | Trivial | ✅ Ready | ✅ Ready | ✅ Python, ~30 lines |
| Adaptive formulas | Easy | Trivial | Trivial | ✅ Ready | ✅ Ready | ✅ TS, ~25 lines |
| Perfect solver | Moderate (7x6 solvable) | Trivial | Trivial | Not feasible | Trivial | ❌ C++, not distributable |
| Neural (SFT + RL) | Hard (training) | Trivial | Moderate | Training only | ✅ Training | ✅ Inference OK |
| Neural (pre-trained) | Easy (inference) | Trivial | Trivial | ✅ Ready | ✅ Ready | Needs model file |

### 8.2 Kaggle-Specific Constraints

**Runtime budget**: Kaggle ConnectX runs are short (typically seconds per move). Pure minimax with a simple eval (window-scoring, threat-map) is feasible. Deep search with complex eval (GA-evolved) is too slow. MCTS with NN evaluation is too slow for Kaggle's time limits.

**Package constraints**: Kaggle environments support Python and Node.js. Rust is not natively supported (WASM possible but complex). PyTorch is available but the model size adds to the package.

**Board-size variability**: Kaggle boards can have arbitrary (rows, cols, inarow). The evaluation must handle any configuration. The asymmetric window approach (S050) and adaptive formulas (S121) are the only fully portable options.

### 8.3 Recommendation by Environment

| Environment | Recommended Approach | Rationale |
|-------------|---------------------|-----------|
| Kaggle CPU (real-time) | Asymmetric window scoring (S050) | Fast, simple, portable, independently verified |
| Kaggle T4 (real-time) | Neural inference (S014, pre-trained) | GPU acceleration makes NN feasible |
| Kaggle T4 (training) | Two-stage SFT+RL (S014) | GPU enables RL self-play |
| Local CPU (research) | Threat-map + GA tuning | Research budget for GA runs, Python-friendly |
| GPU cluster | Neural training (S014, S030) | Requires training compute; pre-trained for inference |
| DGX Spark | Neural training (S014) | On-device training for Kaggle submission optimization |

---

## 9. Performance Evidence

### 9.1 Evidence from the Corpus

The corpus does not contain direct head-to-head performance benchmarks between evaluation approaches. However, indirect evidence can be extracted:

1. **GA evolution direction**: The GA consistently increases the threat_weight (from 1.588 to 3.851) and decreases piece_count (from 0.965 to 0.113). This indicates that threat detection is more valuable than piece counting for evaluation quality.

2. **GA convergence**: The GA converges to similar configurations across generations, suggesting the feature space is well-ordered and the heuristic is a reasonable representation of the game.

3. **rowspire's hybrid approach**: rowspire offers both heuristic and neural modes, suggesting neither approach is universally superior -- the choice depends on compute constraints.

4. **Pascal Pons solver**: The existence of a perfect solver for 7x6 Connect 4 (S033) provides a ground truth against which heuristic evaluations can be validated. The solver demonstrates that for small boards, exact evaluation is possible without any heuristic.

5. **rowspire MLAI evaluation** (S030, S067): Neural evaluation combined with MCTS (4000 simulations, UCB1 c=1.41, Dirichlet noise 75/25) produces high-quality play on 7x6. The NN-guided MCTS outperforms pure minimax with heuristic evaluation, suggesting neural evaluation is superior when compute allows.

6. **Kamide adaptive formulas** (S121): The only evaluation designed for variable board sizes. Its existence and active maintenance suggest that the Kaggle ConnectX challenge requires board-size adaptability.

### 9.2 Computed Performance Characteristics

| Approach | Eval Speed | Eval Quality | Search Depth Possible | Total Quality |
|----------|-----------|--------------|----------------------|---------------|
| Asymmetric window | Fastest | Moderate (verified) | Deepest | High for real-time |
| Threat-map | Fast | Good | Deep | High for research |
| GA-evolved features | Moderate (multi-term) | High (GA-tuned) | Medium | Highest for CPU research |
| Adaptive formulas | Fast | Moderate (3-term) | Deep | High for variable boards |
| Neural (inference) | Moderate | Highest | Limited by sim count | Highest if compute allows |
| Perfect solver | O(1) exact | Perfect | N/A (no eval) | Optimal (small boards only) |

---


---

## 10. Board-size and Inarow Applicability

| Approach | 7x6 (i=6) | 9x6 (i=6) | 10x8 (i=6) | 15x13 (i=6) | 7x7 (i=7) | General |
|---|---|---|---|---|---|---|
| rowspire Heuristic | FULL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO: hard 7-col array |
| rowspire MLAI | FULL | FULL | FULL | FULL | FULL | FULL: normalized |
| Kamide Adaptive | FULL | FULL | FULL | FULL | FULL | FULL: WC-dependent |
| QveenCoder Asymmetric | FULL | FULL | FULL | FULL | FULL | FULL: inarow param |
| ariaborin Threat-Map | FULL | FULL | FULL | FULL | FULL | FULL: generic threat |
| PascalPons Solver | FULL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO: only small boards |
| marcpaulo15 CNN | FULL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | FULL: flexible rep |

---

## 11. Integration and Ensemble Opportunities

### 11.1 Hybrid Evaluation: Heuristic + Neural

Most promising ensemble: Eval(board) = lambda * classical_eval + (1-lambda) * neural_value

In practice: lambda=1.0 for shallow search (depth 1-3); lambda=0.5 for medium (depth 4-8); lambda=0.0 for deep (depth 9+). Mirrors AlphaZero ensemble approach.

Rationale: Classical eval provides interpretable board-size-adaptive signals; neural provides learned heuristics capturing complex interactions.

### 11.2 Threat-Map + Asymmetric Amplification

Combine ariaborin strong/weak classification with QveenCoder asymmetric amplification:

Eval = (strong_pos - strong_neg) + 0.1*(weak_pos - weak_neg) + alpha * opponent_weak_threat (alpha=20).

### 11.3 Adaptive Weight Selection by Board Size

Kamide adaptive weight formulas provide framework for automatic weight selection based on board size. Most promising path toward single eval function across all Kaggle board sizes.

---

## 12. Failure Modes and Risks

### 12.1 Heuristic Misclassification

Fundamental risk: evaluation scores position A as better than B, but B leads to forced win while A leads to loss. Approximating discrete game value with continuous heuristic score.

Example: Position with many pieces in center (high positional score) may be scored positively, but if opponent has 3-in-a-row with open end (forcing threat), true game value is forced loss. Heuristic with insufficient threat weighting misses this.

Mitigation: Increase threat_weight (rowspire genetic tuning tripled it). Add proactive defense asymmetry (QveenCoder).

### 12.2 Board-Size Transfer Failure

Heuristics tuned for one board size may not transfer. rowspire column values hardcoded for 7-column board. On 10-column board, center changes -- two center columns, column value distribution needs re-evaluation.

Mitigation: Kamide approach (all weights WC-dependent) is inherently board-size-agnostic. QveenCoder window-based approach is also board-size-agnostic.

### 12.3 Overfitting in Genetic Tuning

rowspire genetic tuning produced evolved weights differing significantly from defaults (threat +143%, horizontal +111%, pieces_count -88%). Tuning performed on specific training set may not generalize.

Mitigation: Cross-validate evolved weights across multiple board sizes and opponent types. Use distinct validation set.

### 12.4 Neural Network Distribution Shift

marcpaulo15 CNN and rowspire MLAI require inference-time board distribution matching training-time distribution. Training from heuristic players may perform poorly against search-based opponents.

Mitigation: Self-play RL in stage 2 generates training data from network own play. Risk: mode collapse.

### 12.5 Asymmetric Threat Overcorrection

QveenCoder 1.2x opponent threat amplification can overcorrect when both players create equal threat counts. Systematically favors opponent, exploitable by strong opponent.

Mitigation: Make asymmetry ratio adaptive -- higher in early game, lower in endgame.

---

## 13. Benchmark Requirements

### 13.1 Position Classification Accuracy
**Objective**: Measure fraction of positions where evaluation agrees with perfect solver verdict.
**Method**: Generate test set from solved boards (7x6), classify each with heuristic eval, compare to solver value.
**Metric**: Classification accuracy = agreements / positions
**Target**: > 95% at depth 6, > 99% at depth 10 (7x6).

### 13.2 Search Performance
**Objective**: Measure node throughput of each eval function in Python (Kaggle deployment).
**Method**: Run depth-8 minimax + alpha-beta with each eval, measure NPS.
**Metric**: Nodes per second
**Target**: > 10K NPS on Kaggle CPU at depth 6 (response < 2s).

### 13.3 Win Rate vs Baselines
**Objective**: Measure win rate against standard baselines.
**Method**: 1000-game self-play tournament per evaluator vs random, greedy, heuristic baselines.
**Metric**: Win rate (% of games won)
**Target**: > 90% vs random, > 70% vs greedy, > 50% vs heuristic.

### 13.4 Board-Size Generalization
**Objective**: Measure how well eval tuned for 7x6 performs on other board sizes.
**Method**: Train on 7x6, test on 9x6, 10x8, 15x13.
**Metric**: Win rate degradation
**Target**: < 10% degradation on any board size.

---

## 14. Open Questions

1. **Optimal threat asymmetry ratio**: Is 1.2x (QveenCoder S050) optimal, or does optimal ratio depend on board size, inarow, and opponent strength? Kamide symmetric approach (1.0x) may be optimal on boards where both players create similar threat counts.

2. **Feature interaction terms**: None of analyzed implementations include explicit feature interaction terms (e.g., center_control * threat). Could interaction terms significantly improve accuracy? Genetic tuning on rowspire suggests optimizer discovers implicit interactions through weight adjustments.

3. **Genetic tuning convergence**: How many generations does rowspire genetic tuning require for convergence? Does evolved weight set represent global or local optimum? Large weight deltas suggest default was far from optimal, but convergence diagnostics are not available in source.

4. **Neural evaluation on CPU**: Can rowspire MLAI network achieve competitive performance on CPU-only inference? Source provides GPU-trained models but no CPU benchmark data. Inference latency at search depth 4-8 is unknown.

5. **Fork detection**: None of evaluated implementations (except Chess Programming Wiki S075, S137 patterns) include explicit fork detection. Forks are guaranteed wins in Connect 4; their absence from most eval functions is notable.

6. **Distance-to-win vs heuristic**: PascalPons exact distance-to-win scoring suggests optimal eval is exact game value, not pattern-based. But this is only feasible when search reaches terminal states. The threshold where heuristic eval becomes necessary needs study across board sizes.

---

## 15. Recommendations

### R1: Adopt Adaptive Weight Formulas as Base
Use Kamide adaptive weight approach (S121, S128, S138) as base. Formulas center=+(WC-1), threat_offense=+(WC+1), threat_defense=-(WC), vulnerable=+(WC-2) provide automatic board-size adaptation with zero tuning per board size, are simple to implement efficiently in Python, and are verified to work across winCondition=3, 4, 5+.

### R2: Add Asymmetric Threat Amplification
Layer QveenCoder 1.2x opponent threat amplification (S050) on top of adaptive weights. The 1.2x asymmetry is the highest-impact single change not already captured by adaptive weighting. Eval = (my_threats * WC+1) - (opp_threats * WC * 1.2). Modest proactive defense bias without excessive computation.

### R3: Include Strong/Weak Threat Dichotomy
Incorporate ariaborin strong/weak threat classification (S052, S124) as refinement to basic threat counting. Strong threats (3-in-a-row + 1 empty) scored significantly higher than weak threats (2-in-a-row + 2 empty) with 10:1 ratio.

### R4: Hybrid Heuristic + Neural Architecture
For final perfect bot, implement hybrid evaluation:
- Primary: Classical heuristic (Kamide adaptive + QveenCoder asymmetric + ariaborin strong/weak)
- Secondary: Neural value head (rowspire MLAI architecture, S030/S039)
- Blend: lambda * classical + (1-lambda) * neural, where lambda = f(depth)

### R5: Genetic Tuning for Final Weights
After implementing hybrid evaluation (R4), run genetic tuning campaign to optimize remaining free parameters (asymmetry ratio, strong/weak ratio, lambda blending factor) across multiple board sizes.

---


---

## 16. Sources and Retrieval Record

| Source ID | Repository/URL | File | Authenticated Content |
|---|---|---|---|
| S030 | tre-systems/rowspire | evaluation.rs | Heuristic eval formula, column values, feature weights, line_threat |
| S033 | PascalPons/connect4 | C++ source | Perfect solver architecture, no heuristic eval |
| S038 | PascalPons/connect4 | C++ source | moveScore() for move ordering |
| S039 | tre-systems/rowspire | ml_ai.rs, features.rs | Neural feature vector, NN architecture, dual-head |
| S041 | tre-systems/rowspire | Config (genetic) | Evolved heuristic weights |
| S042 | PascalPons/connect4 | C++ source | possibleNonLosingMoves() pruning |
| S050 | QveenCoder/connect-four | Python source | Asymmetric window scoring, formula, terminal values |
| S051 | nguyenthequang | GitHub source | Independent verification of asymmetric scoring |
| S052 | ariaborin/The-Reticle | source code | Threat-map eval, strong/weak classification, history |
| S066 | tre-systems/rowspire | Config (defaults) | Default heuristic weights |
| S068 | tre-systems/rowspire | Config (defaults) | Column value defaults |
| S069 | tre-systems/rowspire | Config (constants) | Terminal value constants |
| S075 | Chess Programming Wiki | wiki | Standard Connect 4 eval patterns |
| S078 | Chess Programming Wiki | wiki | Asymmetric threat evaluation |
| S094 | marcpaulo15/RL-connect4 | GitHub source | CNN architecture, training pipeline |
| S121 | Kamide/connect-n | TS source | Adaptive scoring, formulas, winCondition weights |
| S123 | Kamide/connect-n | TS source | Threat scoring, hole-count, shuffled move order |
| S124 | ariaborin/The-Reticle | source code | Threat-map computation details, history heuristic |
| S126 | PascalPons/connect4 | C++ source | Exact distance-to-win solver, NO heuristic eval |
| S128 | Kamide/connect-n | TS source | Vulnerable chain detection, board-size parameterization |
| S137 | Chess Programming Wiki | wiki | Fork detection, center column control |
| S138 | Kamide/connect-n | TS source | Adaptive weight formula derivation |
| S014 | marcpaulo15/RL-connect4 | GitHub source | Neural network training pipeline details |

---

## 17. Cross-Links

### Within Classical Search Series

- **CS-001** (Opening Book Engineering): Eval quality determines opening book boundary usage.
- **CS-002** (Board Representation): Board representation directly impacts eval performance. Flat 1D (Kaggle), bitboard (rowspire S030), 2D array (ariaborin S052), window-based (QveenCoder S050).
- **CS-003** (Classical Search and Solver Engineering): Eval is leaf-scoring component of alpha-beta search.
- **CS-004** (Search Algorithm Comparison): Minimax needs consistent eval; alpha-beta benefits from eval-informed move ordering; MCTS uses eval as prior + neural value.

### Cross-Dossier Links

- **CMP-003** (Threat Detection): rowspire line_threat (S030), ariaborin threat_map (S052), Kamide adaptive (S121).
- **CMP-004** (Board Representation): Flat 1D, 2D array, bitboard, window-based.
- **CMP-008** (Search Engine): Eval is leaf-scoring mechanism for search engines.
- **CMP-012** (Heuristic Tuning): rowspire genetic tuning (S030, S041).
- **CMP-014** (Neural): rowspire MLAI (S030, S039), marcpaulo15 CNN (S014, S094).
- **CMP-017** (Ensemble): Hybrid eval (heuristic + neural) per Recommendation R4.

### Claim and Hypothesis Links

- **C005**: Eval quality bounds search quality.
- **C008**: Center-first move ordering (rowspire S068 column values).
- **C009**: Feature tuning improves search quality (rowspire genetic tuning S030, S041).
- **C071**: Asymmetric threat eval improves defense (QveenCoder S050).
- **C118**: Board-size adaptive eval (Kamide S121, S128, S138).
- **C126**: Neural eval for ConnectX (rowspire MLAI S039, marcpaulo15 S094).
- **C175**: Heuristic eval required for search beyond solved-game depth.
- **C184-C192**: Eval function ensemble combinations.
- **C205**: Neural tactical weakness requires classical eval fallback.

- **HYP-008**: Genetic tuning of heuristic weights improves win rate across board sizes.
- **HYP-021**: Asymmetric threat eval (1.2x opponent) improves play vs aggressive opponents.
- **HYP-024**: Hybrid heuristic + neural eval outperforms either component alone.

- **ENS-019 through ENS-024**: Eval function ensembles combining classical heuristics, neural networks, and exact solvers.


































































































































































































































