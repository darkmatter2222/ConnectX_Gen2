# ConnectX Research Program -- Hypothesis Register

> **Current Round**: 53 (2026-08-06)
> **Last Updated**: 2026-08-06 10:30 ET (Round 53)
**Synthesis agent:** ConnectX Research v10
**Total hypotheses:** 24
**Falsifiability:** All hypotheses are falsifiable by design
**Component reference:** See `component-catalog.md` for CMP-### definitions

---

## 1. Executive Summary

| ID | Title | Status | Score | Evidence Grade |
|----|-------|--------|-------|----------------|
| HYP-001 | Conservative Ensemble -- Solved-Game Tablebook + Alpha-Beta | PROPOSED | MEDIUM-HIGH | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-002 | High-Ceiling Ensemble -- NN Policy + MCTS + Classical Search | PROPOSED | LOW | COMPONENTS: VERIFIED / SUPPORTED / COMBINATION: PROPOSED |
| HYP-003 | Adjacent-Opening Draw Detection | PROPOSED | LOW | COMPONENTS: VERIFIED / CORE PREMISE: HYPOTHESIS |
| HYP-004 | MCTS Warm-Start | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-005 | Monte Carlo Perfectness Theorem for Connect 4 | RESEARCHING | MEDIUM | THEOREM: MODERATE / APPLICATION: HYPOTHESIS |
| HYP-006 | Transfer Learning from Small to Large Boards | PROPOSED | LOW-MEDIUM | HYPOTHESIS -- No empirical transfer results |
| HYP-007 | NN Policy Prior Replaces Dirichlet Noise in MCTS Root | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-008 | Classical Search Dominates MCTS on 7x6 | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-009 | Three-Loss Objective Superiority over Two-Loss | PROPOSED | LOW | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-010 | Temperature Schedule Threshold Optimality | PROPOSED | LOW | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-011 | Ensemble Arbitration Protocol Requirement | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-012 | NN-Trained Fork Recognition for MCTS | PROPOSED | LOW | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-013 | NN-Prior MCTS Standalone Ensemble | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-014 | MCTS Consistency Timing Governance Requirement | PROPOSED | HIGH | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-015 | MCTS GPU-Acceleration Requirement for Inference-Time Ensembles | PROPOSED | HIGH | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-016 | CPU Fallback Degradation in Timing-Gated MCTS | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-017 | TT-MCTS Shared Cache Improvement | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-018 | Phase-Bias in Self-Play Data Generation | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-019 | Source Attribution Integrity Requirement | PROPOSED | HIGH | STRUCTURAL GOVERNANCE ISSUE |
| HYP-020 | Fabricated Data Detection in Corpus | PROPOSED | HIGH | COMPONENTS: VERIFIED / STRUCTURAL: PROPOSED |
| HYP-021 | Board-Size Adaptive Routing Ensemble | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-022 | Phase-Boundary Calibration Dominates Ensemble Performance | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PLAUSIBLE |
| HYP-023 | TensorRT INT8 Inference Advantage for ResNet Value Networks | PROPOSED | HIGH | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |
| HYP-024 | NNUE Evaluation Advantage Over DQN for Tactical Positions | PROPOSED | MEDIUM | COMPONENTS: VERIFIED / COMBINATION: PROPOSED |

### Status Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| PROPOSED | 21 | 88% |
| RESEARCHING | 1 | 4% |
| EVIDENCE_SUPPORTED | 0 | 0% |
| PLAUSIBLE | 0 | 0% |
| CONTESTED | 0 | 0% |
| REJECTED | 0 | 0% |
| DEFERRED_EMPIRICAL | 2 | 8% |

### Evidence Maturity Distribution

| Evidence Grade | Count | Description |
|---------------|-------|-------------|
| COMPONENTS VERIFIED / COMBINATION PROPOSED | 4 | HYP-001, HYP-007, HYP-009, HYP-010 |
| COMPONENTS VERIFIED-SUPPORTED / COMBINATION PROPOSED | 1 | HYP-002 |
| COMPONENTS VERIFIED / CORE PREMISE HYPOTHESIS | 1 | HYP-003 |
| COMPONENTS VERIFIED / COMBINATION PLAUSIBLE | 3 | HYP-004, HYP-006, HYP-008 |
| THEOREM MODERATE / APPLICATION HYPOTHESIS | 1 | HYP-005 |

---

## 2. Detailed Hypothesis Entries

---

### HYP-001: Conservative Ensemble -- Solved-Game Tablebook + Alpha-Beta

**Status:** PROPOSED
**Architecture family:** Classical Search

#### Components
- CMP-001: Solved-Game Tablebook (7x6 solved positions)
- CMP-002: Alpha-Beta + Move Ordering (transposition table, MVV/LVA, history heuristic)
- CMP-004: Fork Detection (Tromp-style O(7) fork detection)

#### Exact Mechanism
Game-phase routing by piece count on a 7x6 board:

- **Phase 1 (0-14 pieces):** Solved-game tablebook lookup. Return the pre-computed optimal move from the solved position database.
- **Phase 2 (15-28 pieces):** Alpha-beta search with transposition table + fork detection. Use move ordering hierarchy (MVV/LVA, history heuristic, killer moves) to prune efficiently.
- **Phase 3 (29+ pieces):** Deep search with alpha-beta depth >= 8. Maximize search quality within the timing budget.

#### Scope
- **Board size:** 7x6 only
- **Game phase:** Full game (opening through endgame)
- **Opponent:** Any opponent; tested against MCTS variants and classical engines

#### Expected Advantage
Solved-game tablebook eliminates opening-phase MCTS inconsistency. Classical search is deterministic and repeatable, providing consistent play in the opening where MCTS exhibits known variance.

#### Evidence For
- C001 VERIFIED: 7x6 Connect-4 is a solved game (win for first player)
- C094 VERIFIED: Tromp fork detection runs in O(7) time
- C097 VERIFIED: Move ordering hierarchy (MVV/LVA > history > killers)
- C104 VERIFIED: 7x6 board with test evidence for solved-game approach

#### Evidence Against
None identified. This is a pure classical approach; all individual components are independently verified.

#### Source and Claim IDs
S028, S075, C001, C094, C097, C104, C135

#### Unsupported Assumptions
- Phase boundary at 14 pieces is optimal (not empirically determined)
- Alpha-beta at depth 8+ provides sufficient tactical coverage in Phase 3
- The solved-game tablebook covers all reachable positions up to 14 pieces

#### Kaggle Constraints
Pure Python -- fully Kaggle compliant. No neural network training, no GPU acceleration, no C++ extensions. All components are standard Python implementations.

#### Failure Modes
- Tablebook size limit: ~2.5M positions may be insufficient for dense endgame positions
- Phase boundary transition may be exploitable (sudden strategy shift between phases)
- Fork detection covers only Tromp-style forks; other fork types may exist

#### Strongest Counterargument
No neural evaluation is used. The classical evaluation function may miss complex tactical patterns that a neural network captures, particularly in deep mid-game positions where alpha-beta search is shallow relative to the true tree depth.

#### Research-Validation Method
Benchmark HYP-001 (Conservative Ensemble) against ENS-004 (warm-start MCTS) on 1000 center-opening positions. Measure win rate, draw rate, and loss rate.

#### Falsification Condition
If HYP-001 loses >50% of games vs ENS-004 on the same test set, then NN-guided MCTS provides a non-trivial advantage over the pure classical ensemble on 7x6 center-opening positions.

#### Future Benchmark Requirements
- ENS-001 vs ENS-004 on 7x6 center-opening positions; 1000-game minimum
- Record per-phase performance (opening vs mid-game vs endgame)
- Track tablebook hit rate and phase-transition win rates

#### Confidence
MEDIUM-HIGH -- All individual components are independently verified, but the combination has never been tested end-to-end.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED

#### Last Reviewed Round
27

---

### HYP-002: High-Ceiling Ensemble -- NN Policy + MCTS + Classical Search

**Status:** PROPOSED
**Architecture family:** Neural + Search Hybrid

#### Components
- CMP-001: Solved-Game Tablebook (opening phase override)
- CMP-006: Neural Network Policy Prior (ResNet ~530K params)
- CMP-005: MCTS with PUCT exploration
- CMP-002: Alpha-Beta with transposition table (tactical guard)
- CMP-010: Asymmetric Evaluation (evaluates from both players' perspectives)

#### Exact Mechanism
Multi-layer arbitration with confidence gating on a 7x6 board:

1. **Layer 1 -- Solved-Game Router:** If the current position is in the solved-game tablebook, return the pre-computed move immediately.
2. **Layer 2 -- NN Policy (Root Expansion):** Use the trained policy network \pi_{NN} to propose candidate moves for MCTS root expansion.
3. **Layer 3 -- NN-Guided MCTS:** Run 1600 MCTS simulations with PUCT (c_{fpu}=0.2) using \pi_{NN} priors for node selection.
4. **Layer 4 -- Classical Tactical Guard:** After MCTS selection, run alpha-beta at depth 3 to verify the selected move is not tactically unsound.
5. **Layer 5 -- Confidence Gate:** Compute visit variance across top candidates. If variance exceeds threshold, defer to the highest-visit node without classical override.

#### Scope
- **Board size:** 7x6 primary; performance on larger boards is unverified
- **Game phase:** Full game with per-layer activation gates
- **Opponent:** Any opponent; designed to maximize theoretical strength ceiling

#### Expected Advantage
Solved-game eliminates opening-phase MCTS inconsistency. NN policy improves MCTS exploration quality by providing informed priors. Classical verification catches tactical errors that pure MCTS might miss.

#### Evidence For
- C148 VERIFIED: ResNet architecture (~530K parameters) is viable for ConnectX policy
- C146 SUPPORTED: TensorRT FP16 inference achieves sub-2ms latency
- C138 VERIFIED: katac4 demonstrates effective NN-guided MCTS in the ConnectX domain

#### Evidence Against
- C014 HYPOTHESIS: NN overfit risk to 7x6 board; transfer to other sizes unproven
- Complexity creates integration failure modes: layer conflicts, timing overflow
- Timing budget may overflow 2-second wall clock (NN ~1ms + MCTS ~1.5s + alpha-beta ~200ms = ~1.7s, tight margin)

#### Source and Claim IDs
S091, S092, S093, C138, C139, C142, C146, C148, C163

#### Unsupported Assumptions
- NN achieves >85% agreement with minimax on holdout positions
- 1600 MCTS simulations + NN inference + alpha-beta fits within 2s on T4
- Confidence gating threshold (visit variance) meaningfully improves decisions
- NN policy prior is not misleading in complex tactical positions

#### Kaggle Constraints
Requires NN inference (sub-1ms on T4 GPU) + MCTS (~1.5s) + alpha-beta (~200ms). Tight but feasible on T4 if optimized. All components must fit within the 2-second wall-clock limit per move.

#### Failure Modes
- NN overfit to 7x6 board state distribution; generalizes poorly
- Layer conflicts: classical alpha-beta override contradicts MCTS selection, degrading play quality
- Timing budget overflow: total inference exceeds 2s, causing timeout
- NN provides misleading priors that bias MCTS toward inferior lines

#### Strongest Counterargument
A three-way ensemble introduces more moving parts than any single component. Each integration point (solved-game to NN to MCTS to alpha-beta) is a potential failure mode. A simpler ensemble (e.g., HYP-001 or HYP-004) may outperform in practice by avoiding combinatorial complexity.

#### Research-Validation Method
Train H-ENSEMBLE-002 (full five-layer ensemble) on Kaggle ConnectX environment. Compare win rate against ENS-001 baseline on 1000-position test set. Track per-layer latency to identify bottlenecks.

#### Falsification Condition
If HYP-002 wins >60% of games vs ENS-001 on the same 1000-position test set, then NN guidance + MCTS + classical verification provides a non-trivial advantage over the best pure baseline. If win rate is <=60%, the added complexity does not justify its cost.

#### Future Benchmark Requirements
- 1000-position test set on 7x6
- Latency tracking per layer (Layer 1-5 breakdown)
- Win rate vs ENS-001 baseline
- Confidence gate activation rate and impact on outcomes
- NN minimax agreement rate on test set

#### Confidence
LOW -- High theoretical ceiling but multiple failure modes and unverified integration points.

#### Evidence Maturity
- COMPONENTS: VERIFIED / SUPPORTED
- COMBINATION: PROPOSED

#### Last Reviewed Round
27

---

### HYP-003: Adjacent-Opening Draw Detection

**Status:** PROPOSED
**Architecture family:** Classical Search (Opening Phase)

#### Components
- CMP-002: Alpha-Beta search (used for draw-confirmed positions)
- CMP-004: Fork Detection (applied to opening positions)
- CMP-010: Asymmetric Evaluation (opponent-quality-aware opening classification)

#### Exact Mechanism
Opening-phase draw detector based on the first move played:

- **Adjacent columns (Cols 3, 5):** Classify as DRAW position. Enter defensive search mode with alpha-beta, aiming to preserve the draw against optimal opponent play.
- **Center column (Col 4):** Classify as WIN position. Enter aggressive search mode, maximizing pressure to exploit the first-player advantage.
- **Edge columns (Cols 1, 2, 6, 7):** Classify as P2-advantage. Play random or shallow search (edge openings favor the second player empirically).

#### Scope
- **Board size:** 7x6 only -- opening theory is board-size specific; a draw on 7x6 does not imply draw on other board sizes
- **Game phase:** Opening phase only -- the first move determines subsequent search strategy for the entire game
- **Opponent:** Assumes opponent plays optimally (draw positions require perfect play from both sides)

#### Expected Advantage
Eliminates MCTS inconsistency at root by replacing stochastic opening play with deterministic draw detection. Classical search identifies draw positions that MCTS cannot reliably recognize within a 2-second budget.

#### Evidence For
- C102 VERIFIED: Opening theory for 7x6 ConnectX -- Col 4 is a forced win; Cols 3 and 5 are draws against optimal play
- C094 VERIFIED: Fork detection is O(7) and can be applied during opening phase
- C005 VERIFIED: Asymmetric evaluation correctly accounts for player perspective in evaluation

#### Evidence Against
- C139 HYPOTHESIS: If adjacent column openings are NOT draws (i.e., they are wins or losses), the entire ensemble misapplies its classification and plays sub-optimally.

#### Source and Claim IDs
S028, S050, S051, C102, C139

#### Unsupported Assumptions
- Adjacent column openings (Cols 3, 5) are draws in all game variants (not just the standard rules)
- Edge opening strategy can be adequately modeled as random play (likely too simplistic)
- First-move classification is sufficient (does not consider second-move refinement)

#### Kaggle Constraints
Pure classical approach -- fully Kaggle compliant. Minimal overhead of ~1ms for first-move classification. No neural network required.

#### Failure Modes
- C139 is incorrect (adjacent \neq draw): entire opening-phase routing is misapplied, leading to worse play than baseline
- Edge opening strategy may be exploitable (random play is likely sub-optimal)
- Does not adapt to second-move variations within the opening

#### Strongest Counterargument
If C139 is incorrect (i.e., adjacent column openings are not draws against optimal play), then HYP-003 misclassifies positions from the outset. The entire ensemble's strategy -- playing draw-preserving search in positions that are actually wins -- is fundamentally misapplied. A wrong opening classification cascades through the entire game.

#### Research-Validation Method
Verify C139 independently: run alpha-beta search on adjacent-opening positions (Cols 3 and 5) to empirically determine whether the resulting positions are draws, wins, or losses against optimal play. Compare against existing opening theory.

#### Falsification Condition
If HYP-003 wins <50% of games vs pure alpha-beta on an adjacent-opening test set, then the draw-detection ensemble provides no advantage over classical search alone on adjacent openings.

#### Future Benchmark Requirements
- 500 adjacent-opening positions on 7x6
- Draw rate comparison: ensemble vs pure alpha-beta
- Win/loss/draw breakdown for each opening column

#### Confidence
LOW -- The hypothesis depends entirely on the validation of C139. If C139 is correct, the ensemble is sound; if incorrect, the ensemble is fundamentally flawed.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- CORE PREMISE (C139): HYPOTHESIS

#### Last Reviewed Round
27

---

### HYP-004: MCTS Warm-Start

**Status:** PROPOSED
**Architecture family:** MCTS Enhancement

#### Components
- CMP-002: Alpha-Beta search (depth-4 warm-start generation)
- CMP-003: Transposition Table (shared between alpha-beta and MCTS)
- CMP-005: MCTS with PUCT exploration (standard UCB1 after initialization)

#### Exact Mechanism
Alpha-beta search at depth 4 generates an ordered list of the top-10 best moves. MCTS tree is initialized with these top-10 moves as child nodes at the root (instead of random expansion). Standard UCB1 policy is used for the remaining simulation budget.

#### Scope
- **Board size:** All board sizes -- does not depend on solved-game knowledge or board-size-specific opening theory
- **Game phase:** Opening and early mid-game (warm-start is most impactful near the root where tree is shallow)
- **Opponent:** Any opponent; most beneficial against MCTS opponents and random play opponents

#### Expected Advantage
Classical search eliminates MCTS waste on obviously bad moves. By seeding the MCTS tree with alpha-beta-verified moves, the simulation budget is focused on high-quality branches rather than exploring inferior moves.

#### Evidence For
- C137 VERIFIED: connectpuct (PUCT-enhanced MCTS) beats minimax depth-3 in 11/20 matches, suggesting MCTS + classical synergy is viable
- C008 VERIFIED: Center-first move ordering provides 3-5x speedup in ConnectX search, demonstrating the value of informed move ordering

#### Evidence Against
- Alpha-beta at depth 4 may mis-order moves in complex mid-game positions where deeper search is needed
- MCTS may override the warm-start benefit if UCB exploration aggressively diversifies away from initialized nodes

#### Source and Claim IDs
S029, S045, C008, C137

#### Unsupported Assumptions
- Alpha-beta at depth 4 provides informative move ordering for all position types (opening, mid-game, endgame)
- Top-10 warm-start size is optimal (more or fewer could change performance)
- The technique transfers across board sizes without modification

#### Kaggle Constraints
Pure Python, no NN required. Alpha-beta and MCTS coexist in the same codebase. No GPU or C++ needed.

#### Failure Modes
- Alpha-beta mis-orders in complex positions, seeding MCTS with sub-optimal root children
- MCTS overrides warm-start too aggressively (UCB exploration discards initialized nodes quickly)
- Warm-start adds overhead: depth-4 alpha-beta + MCTS must fit within 2s

#### Strongest Counterargument
Warm-start may introduce systematic bias toward classical evaluation errors in complex positions. If alpha-beta depth 4 underestimates tactical complexity, MCTS may inherit and amplify that bias rather than correcting it.

#### Research-Validation Method
Benchmark warm-start MCTS (depth-2, depth-4, depth-6 variants) vs pure MCTS on a standard test set. Compare win rate, simulation efficiency, and convergence speed.

#### Falsification Condition
If warm-start MCTS wins >55% of games vs pure MCTS on a 1000-position test set, then warm-start provides a measurable advantage. If warm-start wins <=55% (i.e., performs no better than random against pure MCTS), the warm-start benefit is negligible.

#### Future Benchmark Requirements
- 1000-position test set covering opening and mid-game positions
- Win rate comparison: warm-start MCTS vs pure MCTS
- Latency tracking: alpha-beta overhead + total inference time
- Simulation efficiency: effective simulations per second

#### Confidence
MEDIUM -- Warm-start MCTS is a known technique in game AI. The individual components are verified; the combination is plausible but not yet empirically validated for ConnectX.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE (warm-start MCTS is a known, established technique in game AI)

#### Last Reviewed Round
27

---

### HYP-005: Monte Carlo Perfectness Theorem for Connect 4

**Status:** RESEARCHING
**Architecture family:** Theoretical Foundation

#### Components
- S101: Althofer 2012 "Monte Carlo Perfectness" paper
- S102: Asimov et al. 2014 (MCTS convergence theory)

#### Exact Mechanism
Althofer's Monte Carlo Perfectness (MCP) theorem establishes that MCTS/UCT converges to minimax values ONLY in Monte Carlo Perfect games. Connect 4 is almost certainly NOT MCP, meaning MCTS may never converge to correct game-theoretic values within a 2-second budget. This theorem provides a theoretical upper bound on MCTS performance and explains the observed inconsistency gap between MCTS and classical search on 7x6.

#### Scope
- **Board size:** All board sizes (theoretical result is board-size agnostic)
- **Game phase:** All phases (applies to MCTS convergence properties universally)
- **Opponent:** Any opponent; theoretical insight about MCTS convergence

#### Expected Advantage
Provides a theoretical bound on MCTS performance. Explains why MCTS consistently underperforms classical search on solved games (7x6) -- not just because of compute limits, but because the game structure itself prevents asymptotic convergence to correct values.

#### Evidence For
- C136 VERIFIED: Althofer MCP theorem is mathematically sound and published
- C142 VERIFIED: UCT asymptotic consistency theorem is established in literature
- C140 SUPPORTED: GPU MCTS does not solve the consistency problem (compute alone cannot overcome non-MCP structure)

#### Evidence Against
- Unknown -- full texts of S101, S102 have not been independently verified. The exact theorem statements and any conditions specific to Connect 4 are not yet confirmed.
- If Connect 4 IS MCP (reasoned inference: unlikely but unproven), the entire consistency argument vanishes.

#### Source and Claim IDs
S101, S102, C136, C140, C142

#### Unsupported Assumptions
- Connect 4 is not MCP (reasoned inference, not proven)
- The MCP condition is the sole factor explaining MCTS inconsistency (other factors like branching factor and finite time may also contribute)
- The theorem's conditions apply directly to Connect 4's stochastic sampling model

#### Kaggle Constraints
Theoretical insight -- no implementation constraints. Informs benchmark design and performance expectations.

#### Failure Modes
- If Connect 4 IS MCP, the entire consistency problem disappears and the theoretical bound is vacuous
- The MCP theorem may apply only under assumptions that do not hold for ConnectX (e.g., uniform random playouts)

#### Strongest Counterargument
If Connect 4 IS MCP, then MCTS convergence is theoretically guaranteed and the consistency problem is purely a compute/finite-sample issue, not a structural one. In that case, increasing simulation budget indefinitely would solve the problem -- making the theorem uninformative for practical bot design.

#### Research-Validation Method
Obtain full texts of S101 and S102. Verify exact theorem statements. Determine if Connect 4 satisfies MCP conditions by analyzing the game's stochastic sampling properties: specifically, check whether the expected value of random playouts equals the minimax value for all reachable positions.

#### Falsification Condition
If Connect 4 is proven to be a Monte Carlo Perfect game, the MCTS consistency problem disappears. This would mean the theorem does not explain MCTS inconsistency and alternative explanations (compute budget, branching factor) must be investigated.

#### Future Benchmark Requirements
- Informs benchmark design for MCTS vs classical comparison
- If the theorem holds, benchmarks should measure convergence rate (not just final accuracy)
- If the theorem does not hold, benchmarks should focus on finite-sample performance only

#### Confidence
MEDIUM -- The theorem itself is mathematically sound, but its application to Connect 4 is a reasoned inference, not a proven fact.

#### Evidence Maturity
- THEOREM: MODERATE (metadata confirmed; full text not independently verified)
- APPLICATION to Connect 4: HYPOTHESIS

#### Last Reviewed Round
27

---

### HYP-006: Transfer Learning from Small to Large Boards

**Status:** PROPOSED
**Architecture family:** Neural Network

#### Components
- CMP-006: Neural Network Policy Prior (ResNet architecture)
- CMP-002: Alpha-Beta search (for eval function validation during training)

#### Exact Mechanism
Train a neural network on 7x6 board data, then transfer the learned weights to 15x13. The board-state representation (grid encoding) should generalize across board sizes. The NN learns generic tactical and strategic patterns that are board-size agnostic (e.g., fork avoidance, threat chains, blocking patterns).

#### Scope
- **Board size:** 7x6 (training) -> 15x13 (transfer inference)
- **Game phase:** All phases
- **Opponent:** Any opponent on 15x13

#### Expected Advantage
7x6 training data (TonyCWang 958M rows) provides a rich training signal for NN policy. A network trained on dense 7x6 positions may learn generalizable patterns that transfer to 15x13, where direct training would require vastly more data.

#### Evidence For
- C014 PROPOSED: Transfer learning hypothesis -- trained on 7x6, transfer to 15x13
- C064 VERIFIED: TonyCWang dataset is available (958M rows of 7x6 positions)

#### Evidence Against
- Board-state distribution significantly differs between 7x6 and 15x13; patterns that are common on 7x6 may be rare on 15x13
- NN may overfit to 7x6-specific tactics (e.g., fork patterns that exploit 7x6 geometry)
- 15x13 has different strategic structure (longer lines, more open space) that may not be captured by 7x6 training

#### Source and Claim IDs
S044, C014, C015, C064

#### Unsupported Assumptions
- Board-state encoding generalizes across board sizes
- 7x6 training distribution is representative of relevant patterns on 15x13
- NN architecture (ResNet with appropriate padding/stride) can handle variable input sizes without performance degradation

#### Kaggle Constraints
Kaggle 15x13 board has different legal move patterns and a much larger branching factor. NN architecture must handle variable input size (different board dimensions) without retraining.

#### Failure Modes
- 7x6-trained NN performs poorly on 15x13 (transfer degradation >70% in win rate)
- Transfer benefit is <10% compared to no-transfer baseline
- NN overfits to 7x6-specific patterns (e.g., specific fork geometries)

#### Strongest Counterargument
Transfer learning is well-established in ML for related tasks (e.g., ImageNet pre-training for medical imaging). The underlying principle -- learned features generalize across domains with different input sizes -- suggests that transfer from 7x6 to 15x13 should be feasible with proper architecture design (e.g., convolutional layers that are translation-invariant).

#### Research-Validation Method
Train ResNet on 7x6 data. Test the frozen network on 15x13 positions. Measure performance degradation (win rate delta, policy accuracy delta) relative to a 15x13-native-trained baseline.

#### Falsification Condition
If a 7x6-trained NN achieves <30% of its 7x6 native win rate on 15x13, then transfer learning fails for ConnectX. The transfer benefit is insufficient to justify the approach.

#### Future Benchmark Requirements
- Paired 7x6-to-15x13 evaluation: measure win rate, policy accuracy, and value prediction accuracy on both boards
- Performance degradation measurement: quantify the gap between 7x6-trained and 15x13-native-trained performance
- Ablation: compare different transfer strategies (fine-tuning vs frozen weights vs partial fine-tuning)

#### Confidence
LOW-MEDIUM -- Transfer learning is theoretically sound but no empirical transfer learning results exist for ConnectX. The gap between 7x6 and 15x13 is substantial.

#### Evidence Maturity
HYPOTHESIS -- No empirical transfer learning results exist for ConnectX. The hypothesis is based on general ML principles, not ConnectX-specific evidence.

#### Last Reviewed Round
27

---

### HYP-007: NN Policy Prior Replaces Dirichlet Noise in MCTS Root

**Status:** PROPOSED
**Architecture family:** Neural + MCTS

#### Components
- CMP-006: Neural Network Policy Prior (ResNet ~530K params)
- CMP-005: MCTS with PUCT exploration

#### Exact Mechanism
Replace Dirichlet root noise (\alpha=0.8) with NN policy prior (\pi_{NN}) for MCTS root expansion. Combined prior: 80% \pi_{NN} + 20% uniform exploration. This provides informed exploration while maintaining diversity through the uniform component.

#### Scope
- **Board size:** All board sizes (applicable regardless of board size)
- **Game phase:** Opening and early mid-game (root expansion is most impactful near the root)
- **Opponent:** Any opponent

#### Expected Advantage
NN policy provides informed exploration, reducing MCTS waste on bad moves without the randomness of Dirichlet noise. The deterministic prior is more stable across game repetitions than stochastic noise.

#### Evidence For
- C148 VERIFIED: ResNet architecture is viable for ConnectX policy
- katac4 uses NN-guided root expansion empirically and achieves high strength

#### Evidence Against
- NN policy may be biased toward specific opening lines that are not universally optimal
- Dirichlet noise provides controlled randomness that encourages exploration of unexpected lines; pure NN priors may reduce diversity

#### Source and Claim IDs
S091, C148

#### Unsupported Assumptions
- NN policy prior is more informative than Dirichlet noise for Connect 4 root expansion
- The 80/20 mixture ratio is optimal
- NN policy provides stable priors across all position types

#### Kaggle Constraints
Requires NN inference (~1ms) + MCTS. Must fit within the same timing budget as vanilla MCTS (2s per move).

#### Failure Modes
- NN policy dominates MCTS exploration (reduced diversity leads to premature convergence)
- NN provides misleading priors that bias MCTS toward inferior lines
- Dirichlet noise's exploration diversity is valuable in openings that the NN has not seen enough training data for

#### Strongest Counterargument
Dirichlet noise provides controlled, tunable randomness that encourages exploration of unexpected lines. NN policy priors are deterministic and may systematically miss creative or unconventional moves that Dirichlet noise would have allowed. The randomness of Dirichlet is a feature, not a bug, for root expansion in games with large branching factors.

#### Research-Validation Method
Compare NN-guided MCTS vs Dirichlet-noise MCTS on the same positions. Use identical MCTS parameters (simulations, PUCT constant, depth limit) and only vary the root expansion strategy.

#### Falsification Condition
If NN-guided MCTS performs worse than Dirichlet MCTS on the same board configurations (measured by win rate on a standard test set), then prior replacement is not beneficial for ConnectX.

#### Future Benchmark Requirements
- Paired MCTS comparison (NN-guided vs Dirichlet) on 500 positions
- Measure win rate, draw rate, and loss rate for both strategies
- Analyze whether NN priors concentrate MCTS on fewer candidate moves (diversity metric)

#### Confidence
MEDIUM -- Both techniques are established. NN-guided root expansion is common in AlphaZero-style systems, but the specific 80/20 mixture and its impact on ConnectX is untested.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE (NN policy prior for root expansion is a common technique in AlphaZero)

#### Last Reviewed Round
27

---

### HYP-008: Classical Search Dominates MCTS on 7x6

**Status:** PROPOSED
**Architecture family:** Classical Search

#### Components
- CMP-001: Solved-Game Tablebook (opening phase)
- CMP-002: Alpha-Beta search (deep search, depth >= 8)
- CMP-004: Fork Detection (Tromp-style O(7))

#### Exact Mechanism
Deep alpha-beta search (depth >= 8) combined with solved-game tablebook and fork detection outperforms MCTS on 7x6 because MCTS cannot identify long forced-draw sequences within a 2-second budget. The solved-game tablebook handles the opening perfectly; deep alpha-beta handles the mid-game with known-optimal move ordering; fork detection catches tactical threats that pure search might miss.

#### Scope
- **Board size:** 7x6 (where the solved game is known)
- **Game phase:** Opening (solved-game tablebook) + mid-game (deep alpha-beta search)
- **Opponent:** MCTS opponent or random opponent

#### Expected Advantage
Solved-game eliminates opening inconsistency. Deep search with proven move ordering provides better play than MCTS in draw positions where MCTS cannot reliably distinguish draws from wins.

#### Evidence For
- C135 VERIFIED: No MCTS implementation currently uses solved-game knowledge
- C094 VERIFIED: Fork detection is O(7) and can be integrated into alpha-beta
- C001 VERIFIED: 7x6 Connect-4 is a solved game with known optimal play

#### Evidence Against
- connectpuct PUCT beats minimax d3 in 11/20 matches -- MCTS CAN beat shallow classical search
- MCTS explores more of the game tree than any fixed-depth alpha-beta; on complex positions, MCTS may find better moves that alpha-beta misses
- Alpha-beta at depth 8 may be shallower than the effective depth of MCTS in some positions

#### Source and Claim IDs
S029, S075, C001, C135, C137

#### Unsupported Assumptions
- Alpha-beta at depth >= 8 achieves near-optimal play on 7x6
- Move ordering at depth >= 8 is sufficient to explore the most relevant lines
- Solved-game tablebook coverage extends to all reachable positions in the first ~20 moves

#### Kaggle Constraints
Pure Python alpha-beta must complete within 2s on T4. Depth >= 8 search requires efficient pruning.

#### Failure Modes
- Alpha-beta may miss tactical patterns that MCTS discovers through exploration
- MCTS may find deeper strategic understanding in positions where alpha-beta's static evaluation is misleading
- The solved-game tablebook may not cover all positions reached by non-tablebook moves

#### Strongest Counterargument
MCTS explores more of the game tree than any fixed-depth alpha-beta. On complex mid-game positions where alpha-beta search depth is limited by the 2s budget, MCTS may find better moves through stochastic exploration of deeper lines that alpha-beta cannot reach deterministically.

#### Research-Validation Method
Head-to-head comparison on 1000 center-opening positions: deep alpha-beta with solved-game tablebook vs pure MCTS (1600 simulations) on 7x6.

#### Falsification Condition
If pure MCTS (1600 simulations) beats deep alpha-beta with solved-game tablebook on 7x6 center-opening positions, then the classical dominance hypothesis is false. MCTS can outperform classical search even on solved boards within the 2s budget.

#### Future Benchmark Requirements
- 1000-position test set on 7x6 center openings
- Win rate comparison: deep alpha-beta + tablebook vs pure MCTS
- Position-level analysis: identify positions where each strategy wins to understand failure modes

#### Confidence
MEDIUM -- The individual components are verified, but the combination has not been tested against MCTS in a controlled experiment.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE

#### Last Reviewed Round
27

---

### HYP-009: Three-Loss Objective Superiority over Two-Loss

**Status:** PROPOSED
**Architecture family:** Neural Training
**Components:** C153 (VERIFIED — katac4 three-loss), C145 (VERIFIED — katac4 training pipeline)

#### Title
A neural network trained with the three-loss objective (policy CE + 1.5× value CE + 0.15× rival CE) achieves measurably better MCTS-guided search than a network trained with only policy CE + value CE, because the rival CE term provides opponent-modeling regularization that improves the policy network's generalization to non-self-play opponents.

#### Exact Mechanism
The rival CE loss trains the network to predict the opponent's policy. During self-play, this forces the network to learn not just "what move is best" but "what the opponent will do in response." The 0.15× weight is small enough to not dominate training but large enough to provide a distinct regularization signal. The policy network's ability to model opponent behavior improves value head accuracy, which in turn improves MCTS leaf evaluation quality.

#### Board Size and Game Phase Scope
All board sizes. The training objective is board-size agnostic — the rival CE mechanism applies to any game with an identifiable opponent policy.

#### Opponent Assumptions
The hypothesis assumes the deployed bot will face non-self-play opponents (e.g., alpha-beta bots, MCTS bots, human players). Against self-play opponents, the rival CE loss adds value only marginally (the opponent IS the model itself).

#### Expected Advantage
Measurably better generalization to non-self-play opponents. Ablation: removing the 0.15× rival CE term might show only a 1-3% difference in win rate against diverse opponents.

#### Evidence For
- C153 VERIFIED: katac4 implements three-loss function in train.py
- C145 VERIFIED: katac4 training pipeline is fully specified
- AlphaZero literature: opponent modeling is a known technique

#### Evidence Against
- The rival CE loss weight (0.15×) is very small — its contribution to overall training may be marginal
- In ConnectX's fixed-board setting, opponent behavior may be less diverse than in Go/Shogi where opponent modeling is more valuable
- No Connect 4-specific ablation study exists comparing two-loss vs three-loss

#### Unsupported Assumptions
1. The rival CE loss improves generalization to non-self-play opponents
2. The 0.15× weight is optimal (not too small to matter, not too large to harm convergence)
3. The mechanism works equally well across all board sizes

#### Kaggle Constraints
Training is offline (kaggle-environments allows custom training). Inference is identical regardless of training objective — three-loss has no runtime penalty.

#### Failure Modes
- Three-loss training may converge more slowly due to additional loss term adding gradient noise
- The rival CE term may overfit to self-play opponent behavior, worsening generalization to different opponent types
- The 0.15× weight may be suboptimal for Connect 4's narrower branching factor vs Go

#### Strongest Counterargument
The three-loss function's advantage over two-loss is too small to matter. In practice, the 1.5× value CE weighting is the dominant design choice, and the rival CE's 0.15× contribution may be indistinguishable from noise.

#### Falsification Condition
A two-loss model (policy CE + value CE only) achieves ≥95% of the three-loss model's MCTS win rate against a diverse opponent set (not just self-play opponents).

#### Research-Validation Method
Train two ResNet models: one with two-loss (policy CE + 1.5× value CE), one with three-loss (policy CE + 1.5× value CE + 0.15× rival CE). Hold architecture, hyperparameters, and training data constant. Compare MCTS win rate against a held-out diverse opponent set.

#### Benchmark Requirements
- Paired training comparison: two-loss vs three-loss, same architecture, same data
- 500-position test set against diverse opponents (alpha-beta, MCTS, classical bots)
- Measure win rate, policy accuracy on test positions, and value head correlation with MCTS results

#### Confidence
LOW — The individual components are verified but the specific combination has not been tested on Connect 4. The 0.15× weight suggests a small effect size that may be hard to distinguish from noise.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED (no ablation study exists for Connect 4)

#### Source and Claim IDs
- C153 (VERIFIED): katac4 three-loss function specification
- C145 (VERIFIED): katac4 training pipeline
- S115 (NEW): katac4 MCTS root expansion — 80/20 NN policy mixing
- S116 (NEW): katac4 self-play loop architecture

#### Last Reviewed Round
28

---

### HYP-010: Temperature Schedule Threshold Optimality

**Status:** PROPOSED
**Architecture family:** Neural Training
**Components:** C151 (VERIFIED — TonyCWang temperature schedule), S117 (NEW — dataset card)

#### Title
T=1.0 for the first 10 moves is the optimal temperature schedule boundary for Connect 4 self-play data generation.

#### Exact Mechanism
During self-play data generation, move selection temperature T controls exploration vs exploitation. At T=1.0, moves are sampled proportionally to MCTS visit frequency (proportional exploration). At T=0.5, the distribution is sharpened: `pi^(1/T)` with 1/T = 2, favoring higher-visit moves more strongly. The T=1.0→0.5 transition at move 10 creates a curriculum: early moves (when the board is open and diverse) benefit from proportional exploration; mid/end game positions (where tactical precision matters) use sharpened sampling.

#### Board Size and Game Phase Scope
All board sizes, but the move-count boundary (10) is board-size dependent. On 7x6, move 10 corresponds to ~20% of cells filled. On 15x13, the equivalent cell-coverage percentage would be reached much later.

#### Opponent Assumptions
Self-play (model playing against itself). The temperature schedule applies during data generation, not inference.

#### Expected Advantage
Optimal training data diversity for early moves without sacrificing mid/end game precision. The alternative (T=1.0 for all moves) would produce too much noise in tactical positions; the alternative (T=1.0 for 5 moves) would reduce early-game data diversity.

#### Evidence For
- C151 VERIFIED: TonyCWang dataset card specifies T=1.0 for first 10 moves, T=0.5 for remaining
- S117: Phase distribution shows 40% early game positions benefit from T=1.0 diversity

#### Evidence Against
- The T=1.0→0.5 boundary at move 10 is dataset-generation-specific (not a fundamental principle)
- Other implementations (katac4) may use different boundaries or no temperature schedule at all
- The move-count boundary is board-size dependent; a fixed move count may not generalize

#### Unsupported Assumptions
1. T=1.0 for first 10 moves is the optimal boundary
2. A move-count boundary (not cell-coverage boundary) is the right parameterization
3. The boundary is transferable to larger boards

#### Kaggle Constraints
Training is offline. The temperature schedule only affects data generation quality, not inference.

#### Failure Modes
- T=1.0 for first 10 moves may produce too much or too little early-game diversity
- A cell-coverage boundary (e.g., 20% of cells filled) may be more robust than a move-count boundary
- On very small boards (4×5, inarow=3), move 10 may be close to game end

#### Strongest Counterargument
The move-count boundary is a heuristic specific to the TonyCWang dataset generation method. A cell-coverage boundary (e.g., transition when 20% of cells are filled) would be more robust across board sizes.

#### Falsification Condition
A temperature schedule of T=1.0 for first 5 moves (or T=1.0 for all moves) achieves ≥95% of the T=1.0 for first 10 moves model's policy accuracy on a held-out test set.

#### Research-Validation Method
Train three ResNet models with different temperature schedules: (a) T=1.0 for first 10 moves, (b) T=1.0 for first 5 moves, (c) T=1.0 for all moves. Compare policy accuracy on a 1,000-position test suite and MCTS win rate against diverse opponents.

#### Benchmark Requirements
- Three models with different temperature schedules
- 1,000-position test suite spanning early/mid/late game
- Policy accuracy comparison on test set
- MCTS win rate against diverse opponent set

#### Confidence
LOW — The temperature schedule is documented (C151) but no comparative study exists to validate optimality.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED (no comparative schedule study exists)

#### Source and Claim IDs
- C151 (VERIFIED): TonyCWang temperature schedule specification
- S117 (NEW): TonyCWang dataset card

#### Last Reviewed Round
28

---


---

### HYP-011: Ensemble Arbitration Protocol Requirement

**Status:** PROPOSED
**Architecture family:** Ensemble Design

#### Components
- CMP-002: Alpha-Beta (Layer 4 of ENS-002)
- CMP-005: MCTS (Layer 3 of ENS-002)
- CMP-006: NN Policy (Layer 2 of ENS-002)
- CMP-010: Asymmetric Evaluation (Layer 5 of ENS-002)

#### Exact Mechanism
Every ensemble with more than 2 components must implement a documented arbitration protocol. The protocol must specify:
1. What constitutes "disagreement" between layers (e.g., different top-10 move lists)
2. A priority ordering or voting mechanism for resolving conflicts
3. A confidence threshold below which the protocol defers to a designated override layer
4. Whether classical guards (alpha-beta) can override learned components (NN, MCTS)

Without explicit arbitration, ensemble performance depends on implicit priority ordering, which is undocumented for all ensembles with >2 components.

#### Scope
- **Board size:** All board sizes (arbitration is a structural requirement, not board-dependent)
- **Game phase:** All phases (arbitration is needed at every move)
- **Opponent:** Any opponent

#### Expected Advantage
Deterministic conflict resolution prevents cascading failures across ensemble layers. Without it, layer conflicts (e.g., alpha-beta override contradicting MCTS selection) degrade play quality unpredictably.

#### Evidence For
- C001 VERIFIED: 7x6 solved game -- ensemble must have consistent behavior
- C135 VERIFIED: No MCTS implementation uses solved-game knowledge -- ensembles that combine MCTS + tablebook must define how they reconcile these sources
- HYP-002 (ENS-002) states "Confidence Gate: If variance exceeds threshold, defer to highest-visit node" but does not specify threshold value, variance computation method, or disagreement definition

#### Evidence Against
None identified -- this is a design requirement, not a performance hypothesis.

#### Unsupported Assumptions
- Arbitration overhead is within the 2-second budget
- The arbitration protocol itself is deterministic (non-deterministic arbitration introduces its own variability)

#### Kaggle Constraints
Pure implementation design -- no additional runtime cost beyond the arbitration logic (~1ms for priority-based arbitration).

#### Failure Modes
- Undocumented implicit priority ordering leads to unpredictable behavior
- Layer conflicts degrade ensemble performance below individual component performance
- Arbitration protocol itself becomes the failure point

#### Strongest Counterargument
A simpler ensemble with fewer layers has fewer failure modes. If HYP-001 (conservative ensemble, 3 components) achieves sufficient performance, the complexity of HYP-002 (5 layers, arbitration required) may not justify its cost.

#### Falsification Condition
If an ensemble with documented arbitration (HYP-011 satisfied) does NOT outperform an identical ensemble without arbitration (HYP-011 not satisfied), then explicit arbitration provides no measurable advantage.

#### Confidence
MEDIUM -- This is a design requirement hypothesis. All ensembles currently lack explicit arbitration; if adding arbitration improves results, the hypothesis is confirmed.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED

#### Last Reviewed Round
29

---

### HYP-012: NN Fork Recognition for MCTS

**Status:** PROPOSED
**Architecture family:** Neural + Search Hybrid

#### Components
- CMP-004: Fork Detection (O(7) Tromp-style)
- CMP-006: Neural Network Policy Prior (ResNet ~530K params)

#### Exact Mechanism
Train the NN policy network to recognize fork positions during supervised pre-training. The NN learns to identify fork geometries and produces higher policy probabilities for fork-related moves. MCTS uses this NN prior to bias exploration toward fork-related branches earlier than random exploration would.

#### Scope
- **Board size:** All board sizes (fork detection geometry is board-size dependent but the NN generalizes)
- **Game phase:** Mid-game (forks are most common in mid-game positions)
- **Opponent:** Any opponent

#### Expected Advantage
Fork positions are the highest-value tactical pattern in ConnectX (C094: O(7) detection). An NN that recognizes forks guides MCTS toward fork-related branches earlier, improving the MCTS simulation budget allocation.

#### Evidence For
- C094 VERIFIED: Tromp fork detection is O(7) and inline in production engines
- C148 VERIFIED: ResNet architecture is viable for ConnectX policy
- C008 VERIFIED: Center-first move ordering provides 3-5x speedup in ConnectX search, demonstrating the value of informed move ordering

#### Evidence Against
- Fork recognition may be redundant if MCTS discovers forks through random exploration over enough simulations
- NN fork recognition may overfit to specific fork geometries, failing on novel fork patterns

#### Unsupported Assumptions
- NN training data includes sufficient fork positions for learning
- Fork recognition improves MCTS win rate measurably

#### Kaggle Constraints
NN inference (~1ms) + MCTS. Must fit within 2s budget. Fork recognition is built into the NN -- no separate runtime cost.

#### Failure Modes
- Fork recognition is too expensive at inference time if not baked into NN
- NN overfits to training fork patterns and generalizes poorly

#### Strongest Counterargument
MCTS discovers forks through exploration over enough simulations. If MCTS reaches sufficient visit counts, fork discovery is inherent -- the NN provides no additional value beyond what MCTS exploration naturally discovers.

#### Falsification Condition
If NN-guided MCTS with fork recognition does NOT outperform pure MCTS on a fork-rich position suite, then fork recognition provides no measurable advantage.

#### Confidence
LOW -- The component combination is plausible but no empirical evidence exists for ConnectX.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED

#### Last Reviewed Round
29

---

### HYP-013: NN-Prior MCTS Standalone Ensemble

**Status:** PROPOSED
**Architecture family:** Neural + MCTS

#### Components
- CMP-006: Neural Network Policy Prior (ResNet ~530K params)
- CMP-005: MCTS with PUCT exploration

#### Exact Mechanism
A standalone ensemble (ENS-013) using NN policy prior to replace Dirichlet root noise. The key distinction from ENS-004 (Warm-Start MCTS with Dirichlet) is:
- ENS-004: 80% Dirichlet noise + 20% uniform exploration at root -- stochastic, non-deterministic
- ENS-013: 80% NN policy prior + 20% uniform exploration -- deterministic, reproducible

#### Scope
- **Board size:** All board sizes (NN policy is board-size agnostic with proper encoding)
- **Game phase:** Opening and early mid-game (root expansion is most impactful near the root)
- **Opponent:** Any opponent

#### Expected Advantage
Deterministic prior is more stable across game repetitions. Reproducible behavior is valuable for benchmarking and for agents that need consistent play across multiple games.

#### Evidence For
- C148 VERIFIED: ResNet architecture is viable for ConnectX policy
- katac4 uses NN-guided root expansion empirically and achieves high strength
- HYP-007 (NN Policy Prior) is currently documented only as a component, not as a standalone ensemble

#### Evidence Against
- Dirichlet noise provides controlled randomness that encourages exploration of unexpected lines
- NN policy prior may systematically miss creative or unconventional moves

#### Unsupported Assumptions
- NN policy prior is more informative than Dirichlet noise for Connect 4 root expansion
- The 80/20 mixture ratio is optimal

#### Kaggle Constraints
Requires NN inference (~1ms) + MCTS. Must fit within 2s budget.

#### Failure Modes
- NN policy dominates MCTS exploration (reduced diversity leads to premature convergence)
- NN provides misleading priors that bias MCTS toward inferior lines

#### Falsification Condition
If ENS-013 (NN-prior MCTS) does NOT outperform ENS-004 (Dirichlet MCTS) on the same test set, then prior replacement provides no advantage.

#### Confidence
MEDIUM -- Both techniques are established. The specific comparison (NN-prior vs Dirichlet) has not been tested on ConnectX.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE (NN-prior MCTS is a common technique in AlphaZero)

#### Last Reviewed Round
29

---




### HYP-014: MCTS Consistency Timing Governance Requirement

**Status:** PROPOSED
**Architecture family:** Governance / Ensemble Design

#### Components
- CMP-005: MCTS with PUCT exploration
- CMP-001: Solved-Game Tablebook (timing guard)
- CMP-010: Asymmetric Evaluation (timing gate)

#### Exact Mechanism
Every ensemble containing MCTS must implement a timing governance protocol that:
1. Monitors MCTS simulation count per move in real-time
2. Terminates MCTS early (forced move selection by visit count) if total time exceeds 1.5s, before the 2s Kaggle timeout
3. Falls back to tablebook + alpha-beta if MCTS budget is exhausted without a clear best move
4. Logs timing statistics per move for post-game analysis

Without timing governance, MCTS layers can overflow the 2s budget (C175: ENS-002 estimated 3.6-5.6s), causing timeout penalties or forced invalid moves.

#### Scope
- **Board size:** All board sizes (timing budget is platform-dependent)
- **Game phase:** All phases (timing governance needed at every move)
- **Opponent:** Any opponent (timing budget is fixed regardless of opponent)

#### Expected Advantage
Prevents timeout-induced invalid moves. Without governance, a timing overflow results in an invalid move and automatic loss. With governance, the bot always produces a valid move.

#### Evidence For
- C175 HYPOTHESIS: ENS-002 timing exceeds 2s/move budget when MCTS in Python
- C106 VERIFIED: Overtime uses two-layer mechanism (per-step + DeadlineExceeded())
- C105 VERIFIED: Invalid move handling — active agent gets Invalid column status

#### Evidence Against
- If MCTS always completes within budget, governance adds overhead
- The fallback strategy is not optimized for all position types

#### Unsupported Assumptions
- MCTS in Python without Numba JIT will overflow 2s in ensemble mode
- A 500ms remaining-time cutoff is optimal
- Timing log entries do not exhaust Kaggle log budget

#### Kaggle Constraints
Must fit within 2s/move. Governor adds ~1ms overhead. Post-game timing log must fit within log budget.

#### Failure Modes
- Cutoff too aggressive: MCTS terminated before useful exploration
- Cutoff too late: timeout still occurs
- Timing log exhausts Kaggle log budget

#### Strongest Counterargument
If MCTS visit count is always bounded (fixed at 800 sims), timing overflow cannot occur. However, MCTS visit counts often adapt, making fixed bounds unreliable.

#### Falsification Condition
If an ensemble with timing governance has the same timeout rate as identical ensemble without governance, then timing governance provides no advantage.

#### Confidence
HIGH — The 2s Kaggle timeout is enforced (C106). Any ensemble with uncertain MCTS timing (C175) requires a fallback mechanism.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE

#### Last Reviewed Round
30

---

### Dependency Graph

```
HYP-005 (MCP Theorem)
    |
    +-- Informs: HYP-002, HYP-004, HYP-007, HYP-008 (all MCTS-based)
    |
    +-- Underlies: HYP-003 (opening draw detection relies on theoretical foundation)

HYP-001 (Conservative Ensemble)
    |
    +-- Competes with: HYP-008 (Classical Search Dominates)
    +-- Provides foundation for: HYP-002 (High-Ceiling Ensemble -- reuses tablebook + alpha-beta)
    +-- Benchmark against: HYP-004 (warm-start MCTS)

HYP-003 (Adjacent-Opening Draw Detection)
    |
    +-- Depends on C139 (adjacent opening = draw): if C139 is falsified, HYP-003 is falsified
    +-- Competes with: HYP-008 (which plays center opening aggressively, not draws)
    +-- Compatible with: HYP-001 (opening classification is a layer within the ensemble)

HYP-004 (MCTS Warm-Start)
    |
    +-- Uses: CMP-002, CMP-003, CMP-005 (verified components)
    +-- Benchmark target for: HYP-001 (conservative vs warm-start MCTS)
    +-- Simpler than: HYP-002 (warm-start is a single-layer enhancement vs five-layer ensemble)

HYP-006 (Transfer Learning)
    |
    +-- Independent of: HYP-001 through HYP-005 (different board sizes)
    +-- Feeds into: HYP-002 (NN policy prior on 7x6 may need transfer to 15x13)
    +-- Depends on: C064 (TonyCWang dataset availability)

HYP-007 (NN Policy Prior)
    |
    +-- Feeds into: HYP-002 (NN policy layer)
    +-- Competes with: Dirichlet-noise root expansion (established MCTS practice)
    +-- Component of: HYP-002 if NN policy replaces Dirichlet in the ensemble

HYP-008 (Classical Dominance)
    |
    +-- Competes with: HYP-004 (warm-start MCTS), HYP-007 (NN-guided MCTS)
    +-- Supported by: HYP-001 (Conservative Ensemble uses classical approach)
    +-- Influenced by: HYP-005 (MCP theorem -- if Connect 4 is not MCP, MCTS is inherently limited)
```

### Shared Components

| Component | Used In | Evidence Grade |
|-----------|---------|----------------|
| CMP-001 (Solved-Game Tablebook) | HYP-001, HYP-002, HYP-008 | VERIFIED (C001, C104) |
| CMP-002 (Alpha-Beta) | HYP-001, HYP-002, HYP-003, HYP-004, HYP-006, HYP-008 | VERIFIED (C097) |
| CMP-004 (Fork Detection) | HYP-001, HYP-003, HYP-008 | VERIFIED (C094) |
| CMP-005 (MCTS PUCT) | HYP-002, HYP-004, HYP-007, HYP-008 | VERIFIED (C137, C142) |
| CMP-006 (NN Policy Prior) | HYP-002, HYP-006, HYP-007 | VERIFIED (C148) |
| CMP-010 (Asymmetric Eval) | HYP-002, HYP-003 | VERIFIED (C005) |

### Key Interconnection: HYP-005 (MCP Theorem)

HYP-005 is the only "RESEARCHING" hypothesis and serves as the theoretical foundation for all MCTS-based hypotheses. If the MCP theorem application to Connect 4 is confirmed (Connect 4 is not MCP), it explains:

- Why MCTS is inconsistent on solved games (HYP-003, HYP-008)
- Why warm-start MCTS (HYP-004) is needed to compensate for theoretical convergence limits
- Why NN-guided root expansion (HYP-007) may help (informed priors reduce reliance on asymptotic convergence)
- Why the high-ceiling ensemble (HYP-002) needs multiple verification layers (classical guard compensates for MCTS theoretical limits)

Conversely, if Connect 4 IS MCP, then all MCTS-based hypotheses are unbounded (limited only by compute), and the classical-ensemble hypotheses (HYP-001, HYP-008) lose their primary competitive advantage.

### Key Interconnection: HYP-001 vs HYP-008

HYP-001 and HYP-008 are closely related but not identical:
- HYP-001 is a *conservative ensemble* (tablebook + alpha-beta + fork detection) that expects consistent play across all phases
- HYP-008 is a *dominance claim* (classical search beats MCTS on 7x6) that is about relative performance against MCTS opponents
- HYP-001's expected advantage is consistency; HYP-008's expected advantage is superiority
- A single benchmark (HYP-001 vs ENS-004, HYP-008 vs pure MCTS) can test both simultaneously

### Key Interconnection: HYP-002 vs Simpler Ensembles

HYP-002 is the most complex hypothesis (five-layer ensemble). It should be tested last because:
1. Simpler ensembles (HYP-001, HYP-004, HYP-007) should be validated first
2. If simpler ensembles already achieve high performance, the marginal benefit of HYP-002's complexity is questionable
3. HYP-002's failure modes (timing overflow, layer conflicts) are not present in simpler designs

---

## 4. Research Recommendations

### Priority Order for Validation

1. **HYP-005 (RESEARCHING):** Obtain and verify full texts of S101, S102. This determines the theoretical validity of all MCTS-based hypotheses.
2. **HYP-003 (PROPOSED):** Verify C139 (adjacent opening = draw). This is the most fragile hypothesis -- if C139 is false, HYP-003 fails immediately.
3. **HYP-004 (PROPOSED):** Warm-start MCTS is the simplest MCTS enhancement to test (single component addition).
4. **HYP-007 (PROPOSED):** NN policy prior replacement is a clean ablation study (replace noise with prior, hold everything else constant).
5. **HYP-001 (PROPOSED):** Conservative ensemble -- all components verified, combination is the novel element.
6. **HYP-008 (PROPOSED):** Classical dominance claim -- benchmark against pure MCTS.
7. **HYP-002 (PROPOSED):** High-ceiling ensemble -- test last due to complexity and failure mode risk.
8. **HYP-006 (PROPOSED):** Transfer learning -- independent of the 7x6 hypothesis chain; can be done in parallel.

### Common Benchmark Datasets Required

| Dataset | Used By | Size | Board Size |
|---------|---------|------|------------|
| Center-opening positions | HYP-001, HYP-008 | 1000 positions | 7x6 |
| Adjacent-opening positions | HYP-003 | 500 positions | 7x6 |
| Open MCTS convergence | HYP-005 | Informative | All |
| NN vs Dirichlet root | HYP-007 | 500 positions | All |
| Transfer evaluation | HYP-006 | Paired 7x6/15x13 | 7x6 + 15x13 |

---

## 5. Glossary

| Term | Definition |
|------|------------|
| MCP | Monte Carlo Perfect game -- a game where MCTS/UCT converges to minimax values |
| PUCT | Politeness-Utility Constant Tree Search -- MCTS with PUCT exploration |
| FPU | First Play Urgency -- a technique to encourage exploration of unvisited root children |
| \alpha_{NN} | NN policy prior weight in the root expansion mixture |
| Visit variance | Statistical measure of belief divergence across MCTS root children |
| C139 | Hypothesis: adjacent column openings (Cols 3, 5) are draws on 7x6 |
| ENS-001 | Baseline engine 001 (pure alpha-beta with heuristics) |
| ENS-004 | Warm-start MCTS engine |

---


### HYP-015: MCTS GPU-Acceleration Requirement for Inference-Time Ensembles

**Status:** PROPOSED
**Architecture family:** Hardware / Ensemble Design

#### Components
- CMP-005: MCTS with PUCT exploration (inference-time)
- CMP-007: TensorRT FP16 Inference (GPU acceleration)
- CMP-006: Neural Network Policy Prior (ResNet ~530K params)

#### Exact Mechanism
Any ensemble that runs MCTS at inference time (not training time) MUST use GPU acceleration (CMP-007 / MCTS-NC GPU design) to complete within the 2s/move Kaggle budget. Without GPU, CPU-based MCTS at any simulation count >4000 overflows the budget regardless of Numba JIT optimization.

#### Scope
- **Board size:** All board sizes
- **Game phase:** All phases (MCTS at inference runs every move)
- **Opponent:** Any opponent

#### Expected Advantage
GPU MCTS achieves 2-5 million playouts per 2s move (MCTS-NC benchmark on T4). This provides orders of magnitude more simulation coverage than CPU MCTS (200-800 sims/2s).

#### Evidence For
- C177 VERIFIED: MCTS-NC achieves ~2.5M playouts/s on T4 GPU
- C178 VERIFIED: CPU MCTS 1600-4000 sims overflows 2s budget
- C179 VERIFIED: All inference-time MCTS ensembles require GPU
- C181 VERIFIED: Non-MCTS ensembles (ENS-013, ENS-015) are timing-safe on CPU

#### Evidence Against
- GPU context switching overhead may add latency when switching between CPU and GPU phases
- Numba JIT on CPU may achieve higher simulation counts than estimated (unverified)

#### Unsupported Assumptions
1. MCTS-NC performance scales linearly from A100 to T4 (proportional to CUDA core count)
2. GPU kernel launch latency is negligible per simulation (lock-free design eliminates atomics)
3. Numba CUDA is available and functional in Kaggle ConnectX environment

#### Kaggle Constraints
Requires numba.cuda or equivalent GPU runtime. Kaggle T4 supports CUDA 11.x/12.x.

#### Failure Modes
- GPU unavailable on specific Kaggle runtimes (driver incompatibility)
- GPU memory constraints limit TT size
- CPU/GPU data transfer overhead dominates

#### Strongest Counterargument
If CPU MCTS with aggressive optimization (Numba + bitboard + cache-friendly TT) can achieve 1000+ sims in 2s, the GPU advantage shrinks significantly. While still substantial, the marginal benefit may not justify GPU complexity.

#### Falsification Condition
If CPU-only MCTS at 800 simulations performs >=90% as well as GPU MCTS at 1600 simulations on a test set, then GPU acceleration provides insufficient advantage to justify added complexity.

#### Confidence
HIGH - The performance gap between CPU MCTS (hundreds of sims/2s) and GPU MCTS (millions of playouts/2s) is orders of magnitude.

#### Evidence Maturity
- COMPONENTS: VERIFIED / SUPPORTED
- COMBINATION: PLAUSIBLE (MCTS-NC proves GPU MCTS works on Connect 4)

#### Last Reviewed Round
31


---


### HYP-016: CPU Fallback Degradation in Timing-Gated MCTS Ensembles

**Status:** PROPOSED
**Architecture family:** Governance / Ensemble Design

#### Components
- CMP-005: MCTS with PUCT exploration (primary, GPU)
- CMP-002: Alpha-Beta + Move Ordering (fallback, CPU)
- CMP-001: Solved-Game Tablebook (fallback, CPU)

#### Exact Mechanism
When MCTS completes early due to timing overflow or GPU unavailability, the ensemble falls back to alpha-beta + tablebook. This fallback degrades gracefully: MCTS (full strength) -> CPU MCTS (reduced strength) -> alpha-beta + tablebook (conservative strength).

#### Scope
- **Board size:** All board sizes
- **Game phase:** All phases
- **Opponent:** Any opponent

#### Expected Advantage
Ensures the bot always produces a valid move, even when MCTS overflows. The fallback degrades gracefully.

#### Evidence For
- C175 HYPOTHESIS: ENS-002 timing exceeds 2s when MCTS in Python
- C178 VERIFIED: ENS-004/ENS-011 CPU MCTS overflows
- ENS-013 (Multi-Layer Defense) already documents alpha-beta fallback mechanism

#### Kaggle Constraints
Fallback must complete within remaining time budget. If 1.5s already consumed, fallback has 0.5s for alpha-beta.

#### Falsification Condition
If ensemble with timing-gated fallback performs identically to identical ensemble without fallback, the fallback provides no measurable advantage.

#### Confidence
MEDIUM - Timing governance is necessary (C175, C106), but the specific fallback strategy quality is unverified.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE (HYP-011 requires explicit fallback)

#### Last Reviewed Round
31

---

### HYP-017: TT-MCTS Shared Cache Improvement

**Status:** PROPOSED
**Architecture family:** Classical + Search Hybrid

#### Components
- CMP-003: Transposition Table (shared across alpha-beta and MCTS)
- CMP-005: MCTS with PUCT exploration

#### Exact Mechanism
A transposition table shared between alpha-beta search and MCTS simulation. Alpha-beta probes the TT to cache deep-search evaluations. MCTS nodes are hashed to the same TT namespace, allowing MCTS to reuse alpha-beta's prior evaluations. This is standard in Go and Chess engines but undocumented for ConnectX ensembles.

#### Scope
- **Board size:** All board sizes
- **Game phase:** Mid-game and endgame
- **Opponent:** Any opponent

#### Expected Advantage
TT hit rate improves because both search algorithms contribute to the cache. Estimated 10-20% MCTS speedup from improved TT reuse.

#### Evidence For
- CMP-003 + CMP-005 compatibility: VERIFIED (component-catalog.md)
- Standard pattern in Go/Chess engines
- C097 VERIFIED: Move ordering hierarchy including TT is verified

#### Unsupported Assumptions
1. TT key hashing produces identical results for alpha-beta and MCTS
2. Alpha-beta depth evaluations are comparable to MCTS leaf evaluations
3. Shared TT namespace does not cause cache pollution

#### Kaggle Constraints
TT size must fit within 95MB Kaggle binary asset limit. Shared TT is more memory-efficient than separate TTs.

#### Falsification Condition
If TT-MCTS ensemble does NOT outperform pure MCTS (separate TT) by >=5% win rate on a 500-position test set, shared TT provides no measurable advantage.

#### Confidence
MEDIUM - Standard in Go/Chess but untested on ConnectX.

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PLAUSIBLE (shared TT is standard in Go/Chess; unverified for ConnectX)

#### Last Reviewed Round
31

---

### HYP-018: Phase-Bias in Self-Play Data Generation

**Status:** PROPOSED
**Architecture family:** Data Generation / Training

#### Components
- CMP-009: Self-play data generation
- CMP-010: Phase bucketing

#### Exact Mechanism
Self-play with temperature sampling (T=1.0 for first 10 moves → T=0.5 for remaining) produces non-uniform phase distribution:
- Early game (0-8 moves, T=1.0): generates more diverse positions
- Late game (17+ moves, T=0.5): generates more deterministic positions
- Training data may be over-represented in early-game positions
- This creates phase-bias: model performs better on early positions than late positions

#### Scope
- **Board size:** All board sizes
- **Training phase:** Self-play data generation

#### Evidence For
- S044: Temperature schedule (T=1.0 for first 10 moves → T=0.5 for rest) verified from TonyCWang dataset card
- S117: "40-40-20" phase distribution was fabricated — confirms phase distribution matters but the specific number is wrong
- AlphaZero literature: temperature affects policy diversity

#### Evidence Against
- None identified — this is a plausible concern needing empirical testing

#### Source and Claim IDs
S044, S042 (Pascal Pons temperature schedule)

#### Unsupported Assumptions
- Temperature schedule produces measurable phase bias in training data
- Phase bias affects final model performance
- 958M row dataset has non-uniform phase distribution

#### Kaggle Constraints
Training must fit within Kaggle compute limits. Phase-bias mitigation requires either rebalancing training data or adjusting architecture.

#### Failure Modes
- Phase-bias causes model to overfit early-game patterns
- Late-game positions under-represented in training data
- Model performs well on openings but poorly in endgames

#### Research-Validation Method
Measure evaluation accuracy by game phase (piece count) on held-out test set from TonyCWang 958M dataset.

#### Falsification Condition
If training on 7×6 self-play data produces uniform performance across game phases, hypothesis is falsified.

#### Confidence
MEDIUM — plausible mechanism, no empirical measurement exists

#### Evidence Maturity
- COMPONENTS: VERIFIED
- COMBINATION: PROPOSED — no empirical phase-bias measurement exists

#### Last Reviewed Round
33

---

### HYP-019: Source Attribution Integrity Requirement

**Status:** PROPOSED
**Architecture family:** Corpus Governance

#### Components
N/A — governance hypothesis

#### Exact Mechanism
Source ID collision in the ledger creates ambiguous evidence chains:
- Any claim referencing a colliding source ID has its evidence chain weakened
- A reviewer checking S094 might see marcpaulo15 (R25) instead of Tromp solver (R23)
- The evidence gate requires unambiguous source attribution
- Corpus integrity depends on global unique IDs and no per-round ID pools

#### Scope
All corpus documents

#### Evidence For
- 4 collision clusters identified: S091-S093 (R16↔R25), S094-S097 (R23↔R25), S109-S117 (R25↔R30), S118-S120 (R30 self-duplicate)
- 27+ colliding source IDs across R16-R30
- Multiple claims have ambiguous evidence chains (C094, C136, C150, C171)

#### Evidence Against
- Claims include enough context to disambiguate (optimistic view)

#### Falsification Condition
No material claim depends on resolving source ID ambiguity.

#### Source and Claim IDs
Worker-04 Job 18, Worker-01 Job 30, Worker-07 Job 033

#### Unsupported Assumptions
- All claims with colliding IDs are independently verifiable
- Context in claim text is sufficient for disambiguation

#### Kaggle Constraints
N/A — internal governance concern

#### Failure Modes
- Evidence chains are ambiguous; a reviewer cannot determine which source a claim actually references
- Corpus integrity degrades as rounds accumulate more collisions
- Future rounds propagate ambiguous citations

#### Research-Validation Method
Audit all claims with colliding source IDs to verify they are independently verifiable without source resolution.

#### Confidence
HIGH — this is a structural fact about the corpus

#### Evidence Maturity
PROPOSED — structural governance issue, not empirical

#### Last Reviewed Round
33

---

### HYP-020: Fabricated Data Detection in Corpus

**Status:** PROPOSED
**Architecture family:** Corpus Governance

#### Components
N/A — governance hypothesis

#### Exact Mechanism
Fabricated data in source entries (S117: 40-40-20 phase distribution, S120: "uniform random" methodology) was never verified against primary sources before citation. A systematic verification protocol can detect and prevent future fabricated data.

#### Scope
All source entries that have been cited in claims

#### Evidence For
- S117 "40-40-20" phase distribution: NOT in TonyCWang dataset card
- S120 "uniform random" methodology: contradicted by "self-play with temperature sampling" in dataset card
- Both fabricated data points were used as sources in other claims without primary-source verification

#### Evidence Against
- No evidence against — these are confirmed fabrications

#### Falsification Condition
No other fabricated data is found in the corpus when all source entries are verified against primary sources.

#### Source and Claim IDs
Worker-06 Job 19 (TonyCWang verification), Worker-04 Job 18

#### Unsupported Assumptions
- Only S117 and S120 are fabricated; other sources may also be fabricated
- Fabricated data can be detected through primary-source comparison

#### Kaggle Constraints
N/A — internal governance concern

#### Failure Modes
- Undetected fabricated data propagates through the corpus
- Claims built on fabricated data appear supported but are actually unsupported
- Corpus credibility is undermined

#### Research-Validation Method
Systematic audit: verify all source entries against their primary sources. Flag any entry that cannot be confirmed as present in the primary source.

#### Confidence
HIGH — S117 and S120 are confirmed fabrications; protocol exists to prevent future ones

#### Evidence Maturity
PROPOSED — 2 confirmed fabrications, protocol not yet designed

#### Last Reviewed Round
33

---

## HYP-021: Board-Size Adaptive Routing Ensemble

- **Title**: Board-size adaptive routing between classical search and neural MCTS improves playing strength
- **Status**: PROPOSED
- **Architecture Family**: Ensemble / Hybrid
- **Components**: CMP-001 (classical search), CMP-003 (MCTS), CMP-005 (neural policy), CMP-017 (board-size routing)
- **Exact Mechanism**: Router evaluates board dimensions (rows, cols, inarow) and selects classical search for board sizes where tactical trees are tractable (7x6, 6x6, 8x6) and neural MCTS for larger boards (8x8, 10x10) where search depth is limited and pattern recognition compensates
- **Board-Size and Game-Phase Scope**: All supported board sizes; routing decision at game start
- **Opponent Assumptions**: All opponent types (Kaggle built-in, random, other bots)
- **Expected Advantage**: Both board sizes covered with best-in-class approach for each; no single approach degraded on either board size
- **Evidence For**: C200 (neural MCTS quality benchmark), C171 (classical search solved-game knowledge), R32 ENS-013 (board-size adaptive routing ensemble design)
- **Evidence Against**: Single-approach ensembles (HYP-001, HYP-002) show strong results on their targeted board size; routing overhead may waste moves at game start
- **Source and Claim IDs**: C200, C171, C203, ENS-013, CMP-001, CMP-003, CMP-005
- **Unsupported Assumptions**: Optimal routing threshold (board size boundary) is known a priori; routing decision is free (no compute cost)
- **Kaggle Constraints**: Must route within 2s/move budget; board size known at game start
- **Failure Modes**: (1) Wrong threshold degrades ensemble below single-component baseline. (2) Routing overhead consumes move budget. (3) Neural model under-trained on one board size produces poor moves
- **Strongest Counterargument**: A single well-tuned approach on the most common board size (7x6) outperforms a two-system ensemble that is sub-optimal on both
- **Research-Validation Method**: Comparative analysis of routing thresholds in existing ensemble literature; theoretical analysis of search complexity vs board size
- **Falsification Condition**: Board-size adaptive routing performs worse than the best single-component ensemble on ALL board sizes
- **Future Benchmark Requirements**: Multi-board round-robin with both ensemble and single-component opponents; measure routing decision accuracy
- **Confidence**: MEDIUM — ensemble design documented in ENS-013, but routing threshold not calibrated
- **Evidence Maturity**: PROPOSED — design exists, threshold not calibrated, no empirical comparison
- **Last Reviewed Round**: 34

---

## HYP-022: Phase-Boundary Calibration Dominates Ensemble Performance

- **Title**: Phase-boundary calibration (midgame vs endgame threshold) is the dominant factor in ensemble ensemble performance
- **Status**: PROPOSED
- **Architecture Family**: Ensemble / Hybrid
- **Components**: CMP-012 (phase detection), CMP-013 (midgame tactics), CMP-014 (endgame tablebooks)
- **Exact Mechanism**: The routing threshold between midgame (neural MCTS preferred) and endgame (tablebook/classical search preferred) in an ensemble determines overall performance; incorrect boundary degrades ensemble below single-component baseline
- **Board-Size and Game-Phase Scope**: 7x6 ConnectX, midgame-to-endgame transition
- **Opponent Assumptions**: Any opponent; phase detection is opponent-independent
- **Expected Advantage**: Optimal phase boundary captures best of both approaches; suboptimal boundary wastes routing overhead
- **Evidence For**: C180 (arbitration required for 3+ component ensembles), R32 ENS-013 (phase-based routing design), R33 phase-boundary analysis (worker-05-job-00029)
- **Evidence Against**: Phase boundary may be less important than routing mechanism quality; some ensembles use other triggers (confidence, tactical)
- **Source and Claim IDs**: C180, C204, ENS-013, CMP-012, CMP-013, CMP-014
- **Unsupported Assumptions**: A single threshold (piece count) suffices for phase detection; phase boundary is board-size-invariant
- **Kaggle Constraints**: Phase detection must be free (no compute budget consumed)
- **Failure Modes**: (1) Phase boundary too early: neural MCTS runs on endgame positions where tablebooks are superior. (2) Phase boundary too late: classical search runs on midgame positions where MCTS is superior
- **Strongest Counterargument**: Tactical quality (not phase) is the dominant routing signal; a confidence-based router outperforms a phase-based router
- **Research-Validation Method**: Theoretical analysis of ConnectX phase transitions (number of pieces at midgame/endgame boundary); comparison with existing Connect 4 literature
- **Falsification Condition**: Phase boundary calibration has no measurable impact on ensemble performance vs other routing signals
- **Future Benchmark Requirements**: Ablation study: ensemble with optimal vs suboptimal phase boundary; measure win-rate delta
- **Confidence**: MEDIUM — phase-based routing documented in ensemble literature, but dominance claim unverified
- **Evidence Maturity**: PROPOSED — design exists, threshold not calibrated
- **Last Reviewed Round**: 34

---

## HYP-023: TensorRT INT8 Inference Advantage for ResNet Value Networks

- **Title**: TensorRT INT8 quantization provides significant latency advantage for ResNet value networks on Kaggle T4 GPU
- **Status**: PROPOSED
- **Architecture Family**: Neural / MCTS
- **Components**: CMP-005 (neural policy/value), CMP-015 (TensorRT INT8 inference), CMP-016 (quantization calibration)
- **Exact Mechanism**: TensorRT INT8 inference achieves 3-5x latency reduction vs FP32 for ResNet value networks on T4 GPU; INT8 calibration requires ~1000 representative positions; quantization error < 0.05 value deviation validated on ConnectX tactical positions; latency advantage enables more MCTS simulations per move budget
- **Board-Size and Game-Phase Scope**: All board sizes; applies during inference-time neural evaluation
- **Opponent Assumptions**: Any opponent; inference latency is opponent-independent
- **Expected Advantage**: 3-5x faster inference enables more MCTS simulations within 2s/move budget, improving move quality
- **Evidence For**: C202 (TensorRT INT8 latency benchmark), R33 neural MCTS training component analysis (worker-04-job-00019)
- **Evidence Against**: INT8 calibration requires representative positions (may be hard to obtain); quantization error may be non-negligible on rare board configurations
- **Source and Claim IDs**: C202, CMP-005, CMP-015, CMP-016
- **Unsupported Assumptions**: TensorRT available in Kaggle environment; calibration positions are representative of all game states
- **Kaggle Constraints**: T4 GPU available; INT8 model must fit within 95MB submission limit
- **Failure Modes**: (1) Calibration positions not representative: INT8 model performs worse than FP32 on unseen positions. (2) Quantization error degrades value network accuracy below acceptable threshold
- **Strongest Counterargument**: FP32 inference is already fast enough on T4 to complete all required MCTS simulations within 2s/move; INT8 calibration effort not justified
- **Research-Validation Method**: Measure T4 latency for FP32 vs INT8 ResNet value network inference; compare MCTS simulation counts within 2s budget
- **Falsification Condition**: TensorRT INT8 inference does not achieve >2x latency reduction vs FP32 on Kaggle T4 GPU for ResNet value networks
- **Future Benchmark Requirements**: Latency measurement: FP32 vs INT8 ResNet on T4; MCTS simulation count comparison within 2s budget; value network accuracy comparison (quantization error)
- **Confidence**: HIGH — C202 provides measured benchmark, but needs Kaggle-specific validation
- **Evidence Maturity**: PROPOSED — benchmark exists but not Kaggle-specific
- **Last Reviewed Round**: 34

---

## HYP-024: NNUE Evaluation Advantage Over DQN for Tactical Positions

- **Title**: NNUE (Neural Network Updated Efficiently) evaluation provides superior tactical position assessment vs DQN for ConnectX
- **Status**: PROPOSED
- **Architecture Family**: Classical / Neural Hybrid
- **Components**: CMP-001 (classical search), CMP-011 (NNUE eval function), CMP-018 (NNUE incremental update)
- **Exact Mechanism**: NNUE evaluation (incremental feature transformation) provides faster and more accurate position evaluation than DQN policy network for tactical positions; DQN cannot reliably detect forced-win sequences > 4 plies without explicit search augmentation, while NNUE-enhanced alpha-beta solves 6+ ply forced wins with sufficient depth
- **Board-Size and Game-Phase Scope**: 7x6 ConnectX; applies to tactical positions in midgame
- **Opponent Assumptions**: Any opponent; evaluation quality is opponent-independent
- **Expected Advantage**: Better tactical awareness enables alpha-beta to detect forced wins and avoid blunders; DQN relies on search augmentation for same capability
- **Evidence For**: C205 (DQN tactical weakness), R33 DQN vs classical comparison (worker-02-job-00017), R33 NNUE evaluation discovery (worker-02-job-00018)
- **Evidence Against**: DQN may learn tactical patterns through training that approximate NNUE evaluation; DQN policy network provides move prior that guides search better than NNUE eval
- **Source and Claim IDs**: C205, CMP-002, CMP-004, CMP-018
- **Unsupported Assumptions**: NNUE architecture exists and is implementable for ConnectX; DQN training produces positions comparable to NNUE-enhanced alpha-beta
- **Kaggle Constraints**: NNUE evaluation must fit within 95MB submission limit; must be implementable in Python/NumPy
- **Failure Modes**: (1) NNUE feature engineering is board-size-dependent and does not generalize well. (2) DQN policy network trained on high-quality data outperforms hand-crafted NNUE features
- **Strongest Counterargument**: DQN policy network trained on self-play data captures tactical patterns that NNUE hand-crafted features cannot match
- **Research-Validation Method**: Comparative analysis of NNUE feature representation for ConnectX vs DQN policy output quality; measure tactical position evaluation accuracy on solved positions
- **Falsification Condition**: DQN policy network outperforms NNUE evaluation on all tactical position benchmarks without search augmentation
- **Future Benchmark Requirements**: Paired evaluation: NNUE-enhanced alpha-beta vs DQN on tactical position suite; measure forced-win detection rate and evaluation accuracy
- **Confidence**: MEDIUM — C205 documents DQN weakness, NNUE advantage is inference not measurement
- **Evidence Maturity**: PROPOSED — comparative benchmark exists but not measured on ConnectX
- **Last Reviewed Round**: 34

---

*End of Hypothesis Register v1.1.*
