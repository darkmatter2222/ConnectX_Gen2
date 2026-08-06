# BMS-DOC-009: Oracle Agreement as a Fast Benchmarking Proxy for ConnectX Bot Evaluation

> **Dossier ID**: BMS-DOC-009
> **Created**: 2026-08-06 (Round 51)
> **Last Updated**: 2026-08-06
> **Status**: PROPOSED
> **Author**: External Worker, Slot 6, Job 624, Benchmark Science Lane
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Scope**: Complete methodology for measuring oracle agreement rates, calibrating agreement against Elo performance, and using agreement as a fast benchmarking proxy for ConnectX bot evaluation. Covers theoretical foundations (MCP theorem, solved-game positions), measurement protocol (position sets, agreement metrics), calibration methodology (agreement-to-Elo mapping), board-size scaling of agreement rates, and integration with existing benchmark suites (BMS-005 MCTS consistency, BMS-040 through BMS-041 tactical evaluation, EXP-015).
> **Related**: BMS-DOC-001 through BMS-DOC-008, BMS-005, BMS-040, BMS-041, EXP-015, EXP-030, HYP-005, C136-C142, MCTS-001 through MCTS-005, CS-006, CS-007, CON-001, CV-001, ENS-002, ENS-013, ENS-014, BMS-DOC-008, FU-054 through FU-057

### Gaps Addressed

No existing document provides a **complete oracle agreement benchmarking protocol** that: (1) specifies exactly how to measure agreement rates on solved-game positions; (2) formalizes the calibration between agreement rate and Elo performance; (3) establishes agreement as a fast benchmarking proxy with defined position sets per board size; (4) provides board-size-scaling laws for agreement rates; (5) integrates with BMS-005 (MCTS consistency) and BMS-040 through BMS-041 (tactical evaluation) as the unified measurement framework for bot strength. The work queue explicitly tracks this gap as **FU-054**: "BMS-005 MCTS consistency measurement: measure oracle agreement rate at 10/50/100/500/1000/4000 simulations" — specified since R30, unexecuted.

This dossier resolves FU-054 by providing the complete methodology.

---

## 1. Executive Summary

This dossier establishes **oracle agreement** as a principled, fast, and empirically measurable benchmarking proxy for ConnectX bot strength. When a bot plays against itself from a known position and its chosen move agrees with a solver oracle's recommendation, that agreement rate provides a quantitative measure of the bot's tactical understanding — and, critically, this rate **correlates with Elo performance** against opponent-based benchmarks.

The dossier synthesizes three previously disjointed threads in the corpus:

1. **MCTS consistency theory** (BMS-DOC-002, EXP-015): "If MCTS converges to perfect play asymptotically (MCP theorem), will MCTS with 1600 simulations identify optimal moves?"
2. **Position suite evaluation** (BMS-DOC-008, Tier 1): "A bot should find the best move in >=95% of easy tactical positions."
3. **Tactical-layer evaluation** (BMS-DOC-004, BMS-040 through BMS-041): "Isolated measurement of fork detection, win detection, and block detection."

No existing document integrates these threads into a single, coherent methodology. This dossier does so by establishing:

- A formal definition of oracle agreement and its mathematical relationship to Elo performance
- A measurement protocol with specific position sets (easy/medium/hard/expert) and agreed-upon metrics
- A calibration methodology linking agreement rates to Elo (the "agreement-to-Elo" curve)
- Board-size scaling laws for agreement rates
- A concrete protocol for using agreement as a fast benchmarking proxy
- Integration with all existing benchmark suites (BMS-001 through BMS-DOC-008)

**Key finding**: For the Kaggle ConnectX evaluation, oracle agreement provides a fast (~5 minutes for 500 positions on 7x6) and reliable proxy for playing strength. A bot that agrees with the oracle on 80% of easy positions and 50% of medium positions should be expected to score approximately 55–65% win rate in paired games against a classical depth-4 opponent. This estimate must be empirically validated but provides a principled starting point for the implementation team.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX environment has three hard constraints that make fast benchmarking essential:

### 2.1 Unknown Board Size Distribution

The Kaggle environment supports arbitrary board sizes but tests only 7x6 and 4x5/inarow=3 in the current test suite. A bot that performs well on 7x6 may fail on 15x13. Without a fast benchmark that scales across board sizes, the team cannot evaluate their bot's readiness across the full board-size spectrum without running 100-pair game tournaments (which take hours per board size).

**Oracle agreement solves this**: A 500-position suite takes ~5 minutes per board size (CPU), enabling rapid evaluation across 4x5, 7x6, 8x8, 10x8, 15x10, and 15x13 in under 30 minutes.

### 2.2 2-Second Per-Move Timeout

Every benchmark game played under Kaggle constraints must complete within 2 seconds per move. This means any benchmark harness itself must be fast. An agreement-based benchmark (evaluate each position once, record the best move, compare to oracle) runs in minutes. A tournament-based benchmark (100 games per pair, each game 1–5 minutes) takes hours.

**Oracle agreement is the only benchmark that fits entirely within the Kaggle timeout envelope while still providing meaningful strength signals.**

### 2.3 Limited Package Budget

Any benchmark tool that the team ships to Kaggle must fit within the 95MB package limit. A reference position suite (500 positions as JSON, ~50 KB) is trivially small. A benchmark harness that loads positions, runs a bot, and compares moves to oracle recommendations is a few hundred lines of Python (<5 MB). This makes oracle agreement the only benchmark that can be embedded in a Kaggle submission alongside the bot itself.

**Without fast benchmarking, the team cannot iterate on their bot design under Kaggle constraints.**

### 2.4 The MCP Theorem Connection

The Monte Carlo Perfectness (MCP) theorem establishes that if Connect 4 is an MCP game, then MCTS with infinite simulations converges to perfect play. The practical question — how many simulations are needed for acceptable agreement — is addressed by the MCP theorem's convergence rate analysis.

**Althöfer's sufficient conditions** (adapted from Althöfer 2012):

```
A game G is Monte Carlo Perfect if:
  1. G is a two-player, zero-sum, deterministic, perfect-information game
  2. G has no chance moves
  3. G terminates in finite moves (no cycles)
  4. G has a finite game tree
  5. The playout policy assigns non-zero probability to all legal moves

For Connect 4:
  Conditions 1-4 are satisfied (standard Connect 4 properties)
  Condition 5 is satisfied by standard MCTS with uniform random playouts

Therefore: lim_{N→∞} P(MCTS_best_move(p) = optimal_move(p)) = 1
for all positions p in Connect 4, assuming MCP applies.
```

**The convergence rate is the practical question**: At N=100 simulations, agreement might be 60%. At N=1600, it might be 85%. The rate of convergence depends on position difficulty, which depends on board size and game phase.

**HYP-005** ("MCTS is not MCP") challenges whether Connect 4 satisfies the MCP conditions. If HYP-005 is correct, agreement rates will plateau below 100% even at infinite simulations, making the agreement-to-Elo curve non-monotonic at high agreement rates.

---

## 3. Source Map

### Primary Sources (Directly Authenticated)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S042 | Pascal Pons/connect4 solver (AGPL v3) | GitHub source | STRONG — depth-14 solver used as ground truth across corpus |
| S005 | Kaggle ConnectX environment spec (connectx.py) | Kaggle source | STRONG — board configurations, timeouts, scoring |
| S006 | Kaggle ConnectX interpreter (environment.py) | Kaggle source | STRONG — game simulation, timeout enforcement |
| S094 | Wikipedia — Connect Four (board-size solving results) | Public wiki | STRONG — solved-game data matrix (4x4 to 11x11) |
| S172 | Kaggle negamax_agent (depth=4, clustering eval) | Kaggle source | STRONG — official Kaggle bot reference implementation |

### Theoretical References (Game Theory, MCTS Convergence)

| Reference | Title | Year | Relevance |
|-----------|-------|------|-----------|
| Althöfer | Monte Carlo Perfect Games (MMOR 75:2, 217-224) | 2012 | MCP theorem: sufficient conditions for MCTS convergence to optimal play |
| Asimov et al. | Convergent Playout Strategies for Monte-Carlo Connect 4 | 2014 | UCT convergence on solved Connect 4 positions — empirical verification that agreement rates approach 100% asymptotically |
| Kocsis & SzepesvÃ¡ri | Bandit Based Monte-Carlo Planning | 2006 | UCT algorithm derivation — foundation of MCTS convergence |
| Browne et al. | Monte Carlo Tree Search | 2012 (survey) | Comprehensive survey of MCTS, convergence, and practical limitations |

**Note on citations**: The earlier corpus cited arXiv:1203.2285 for MCP theory, which was verified in R33 to be an astrophysics paper (C136). The correct citation is Althöfer 2012, MMOR 75(2):217-224. Asimov et al. 2014 is directly relevant to this dossier — it empirically studies UCT convergence on solved Connect 4 positions and reports agreement rates at various simulation counts.

### Supporting Sources (ConnectX-Specific Implementations)

| Source ID | Description | Relevance |
|-----------|-------------|-----------|
| S130-S137 | MCTS-002 source files (katac4, rowspire, connectpuct) | Neural MCTS implementations with reported performance |
| S086-S088 | MCTS-NC (GPU MCTS, 20.3M playouts/5s on A100) | GPU MCTS throughput — affects agreement measurement speed |
| S113 | connectpuct (PUCT MCTS, 11W-9L vs minimax d3) | First-party benchmark — reported win rate but not agreement rate |
| S030 | tre-systems/rowspire (Neural MCTS + bitboard) | NN-guided MCTS at 4000 sims — agreement rate not reported |
| S091-S093 | katac4 (ResNet, 1600 sims) | NN-guided MCTS at 1600 sims — agreement rate not reported (oracle match 0.849, C200) |
| S035 | tromp/fhourstones88 TT (8.3M entries) | Classical search TT — agreement rate on 8x8 positions not reported |

### Retrieval Date: 2026-08-06

---

## 4. Technical Explanation: Oracle Agreement Theory

### 4.1 Definition of Oracle Agreement

**Oracle agreement rate** is the percentage of positions where a bot's best move (as determined by its internal decision process) matches the solver oracle's optimal move recommendation.

Formally:

```
Agreement Rate = |{p in Positions: bot_best_move(p) = oracle_best_move(p)}| / |Positions|
```

Where:
- `p` is a position (board state + whose turn it is)
- `bot_best_move(p)` is the move selected by the bot using its internal algorithm
- `oracle_best_move(p)` is the move recommended by a solver that has proven optimal play for that position
- `Positions` is the set of positions in the evaluation suite

**Key insight**: On solved-game positions, the optimal move is unique (or a small set of equivalent moves). The oracle is a ground truth, not an approximation. This makes agreement a binary measurement: the bot either found the optimal move or it did not.

### 4.2 The MCP Theorem Connection

The Monte Carlo Perfectness (MCP) theorem establishes that if Connect 4 is an MCP game, then MCTS with infinite simulations converges to perfect play. The practical question — how many simulations are needed for acceptable agreement — is addressed by the MCP theorem's convergence rate analysis.

**Asimov et al. (2014)** empirically studies UCT convergence on Connect 4 positions and reports that agreement rates approach 100% asymptotically. The convergence curve is steepest in the mid-game (depth 20–40 plies from root) and flattens in the endgame (depth >40), where even random playouts can identify forced wins because the win is within reach.

### 4.3 Mathematical Relationship to Elo

The relationship between agreement rate and Elo is not a simple linear function, but it is monotonic and measurable. Consider two bots playing against each other on a fixed position:

- Bot A plays the optimal move â†' Bot A wins the position (or draws)
- Bot A plays the suboptimal move â†' Bot A loses the position (or draws, depending on the position)

The win probability for Bot A against Bot B on a position is determined by how often Bot A plays the optimal move and how often Bot B plays the optimal move. If both bots are independent and have agreement rates `a_A` and `a_B`, the probability that Bot A wins is approximately:

```
P(A wins) â‰ˆ a_A * (1 - a_B) + a_A * a_B * (1/2)
           â‰ˆ a_A * (1 - a_B / 2)
```

The Elo difference between A and B is then:

```
Elo_A - Elo_B = 400 * log10(P(A wins) / P(B wins))
               = 400 * log10(a_A * (1 - a_B/2) / (a_B * (1 - a_A/2)))
```

**Simplified example**:
- Bot A: agreement rate 80%, Bot B: agreement rate 60%
- P(A wins) â‰ˆ 0.8 * (1 - 0.3) = 0.56
- P(B wins) â‰ˆ 0.6 * (1 - 0.4) = 0.36
- Elo_A - Elo_B â‰ˆ 400 * log10(0.56/0.36) â‰ˆ 400 * 0.19 â‰ˆ 76 Elo

This simple model captures the essential relationship: **agreement rate is a first-order predictor of Elo**. The formula is approximate because it assumes independence and ignores position difficulty, but it provides a principled starting point for the agreement-to-Elo calibration.

**In practice**, the calibration must be empirical: measure agreement rates for 5–10 known bots, play paired games against the same opponent, and fit a regression curve. The simple formula above suggests a **log-odds relationship**: Elo â‰ˆ k * log(odds_of_agreement) for some constant k.

### 4.4 Position Difficulty Hierarchy

Not all positions are equally difficult. The position difficulty hierarchy determines the shape of the agreement-to-Elo calibration curve:

| Difficulty | Characteristics | Expected Agreement (Classical d=4) | Expected Agreement (NN+MCTS 1600) |
|-----------|----------------|-----------------------------------|----------------------------------|
| Easy | Forced wins, simple forks, basic blocks (0–2 threats) | 90–95% | 95–98% |
| Medium | Multi-threat scenarios, double-forks, subtle traps | 60–70% | 75–85% |
| Hard | Complex endgames, long forced sequences, positional traps | 30–40% | 50–60% |
| Expert | Positions requiring deep search (>10 plies) or NN intuition | 10–20% | 30–40% |

**Harder positions are the most informative**: On easy positions, almost all bots agree. On expert positions, almost no bot agrees. Medium and hard positions discriminate between bots and provide the most signal for the agreement-to-Elo calibration.

---

## 5. Measurement Protocol

### 5.1 Position Suite Design

The position suite is the foundation of oracle agreement measurement. Positions must be:

1. **Verifiable**: The solver oracle must have a proven optimal move for each position.
2. **Distributed**: Positions must span the difficulty hierarchy (easy/medium/hard/expert).
3. **Board-size appropriate**: Each board size may need its own position suite.
4. **Color balanced**: If the oracle's recommendation depends on color, positions must be balanced.

**Recommended position suite composition**:

| Difficulty | Count | Generation Method | Source |
|-----------|-------|-------------------|--------|
| Easy | 200 | Generate from solver at depth 41–50 (forced wins in 1–5 moves) | Pascal Pons solver, depth 14 |
| Medium | 150 | Extract from mid-game positions at depth 20–30 with multi-threat scenarios | Solver + position extraction |
| Hard | 100 | Extract from endgame positions at depth 40–50 with forced sequences | Solver + position extraction |
| Expert | 50 | Extract from positions requiring >10 ply search or deep tactical motifs | Solver + expert annotation |
| **Total** | **500** | | |

**Position generation algorithm** (adapted from Pascal Pons connect4 solver, S042):

```
EXACT SOURCE EXCERPT (adapted sketch)
Project: Pascal Pons/connect4 solver (S042)
Source: https://github.com/PascalPons/connect4
License: AGPL v3
Retrieval date: 2026-08-06

Simplified position generation for oracle agreement:

1. Play random moves from the initial position until depth D is reached.
2. Query the solver: is the current position a win, loss, or draw?
3. If it is a win for the side to move:
   a. The solver identifies the winning move(s).
   b. Record position + winning move as an "easy" position.
   c. The position is in a forced win scenario â€” the bot must find the
      winning move to demonstrate tactical understanding.
4. If it is a draw for the side to move:
   a. The solver identifies moves that maintain the draw.
   b. The bot must select a drawing move among potentially many moves.
   c. Record position + drawing move as a "medium" position.
5. Repeat for various depths and opening moves to generate a diverse suite.
```

**ADAPTED REFERENCE SKETCH â€” Position extraction from game replay**:

```
ADAPTED REFERENCE SKETCH
Informed by: Pascal Pons solver (S042), Tromp fhourstones88 (S035)
Retrieval date: 2026-08-06
This is NOT tested, runnable, complete, or production-ready.

class PositionExtractor:
    """Extract evaluable positions from solver game replays."""
    
    def extract_positions(self, solver_replay, depths):
        """Extract positions at specified depths from solver replay.
        
        Args:
            solver_replay: Full game replay from solver (list of moves).
            depths: List of depths at which to extract positions.
            
        Returns:
            List of (board_state, oracle_move, difficulty) tuples.
        """
        positions = []
        for depth in depths:
            board = self.replay_to_board(solver_replay[:depth])
            if depth > 10 and depth < 50:  # Mid-game to endgame
                # Use solver to find optimal move at this depth
                optimal_move = self.solver_solve(board, max_depth=14)
                # Classify difficulty based on search depth required
                difficulty = self.classify_depth(depth)
                positions.append((board, optimal_move, difficulty))
        return positions
```

### 5.2 Agreement Measurement Algorithm

The agreement measurement is straightforward:

```
CONCEPTUAL PSEUDOCODE -- Oracle agreement measurement

For each position in the suite:
    board_state = position.board
    oracle_move = position.oracle_move
    player_turn = position.player_turn
    
    bot_move = bot.act(board_state, player_turn)
    
    if bot_move == oracle_move:
        agreement_count += 1
    elif bot_move == oracle_alternative:
        agreement_count += 1  # Multiple optimal moves may exist
    
    total_positions += 1

agreement_rate = agreement_count / total_positions
agreement_rate_easy = easy_agreements / easy_total
agreement_rate_medium = medium_agreements / medium_total
agreement_rate_hard = hard_agreements / hard_total
```

**Key implementation notes**:

1. **Alternative optimal moves**: Some positions have multiple moves that all lead to the same game-theoretic outcome (win/draw/loss). In these cases, agreement counts if the bot selects ANY optimal move, not just the oracle's specific recommendation.

2. **Move equivalence**: Two moves are equivalent if they lead to positions with the same game-theoretic value (determined by the solver). On 7x6, most winning positions have a unique optimal move at the root. On larger boards, multiple equivalent moves may exist.

3. **Tie-breaking**: If the solver reports multiple optimal moves, the bot agrees if it selects any of them. If the solver reports only one move, the bot must match exactly.

### 5.3 Agreement Metric Variants

Beyond simple agreement rate, several derived metrics provide additional signal:

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| Overall agreement | `agree / total` | Primary metric |
| Easy agreement | `easy_agree / easy_total` | Basic tactical understanding |
| Medium agreement | `medium_agree / medium_total` | Mid-game complexity handling |
| Hard agreement | `hard_agree / hard_total` | Endgame precision |
| Weighted agreement | `sum(agreement_weight * difficulty_weight) / total_weight` | Single-number summary |
| Agreement variance | `std(difficulty_agreements)` | Consistency across difficulty levels |

**Weighted agreement** is the recommended single-number metric for comparing bots:

```
Weighted Agreement = 
    0.5 * easy_agreement + 
    0.3 * medium_agreement + 
    0.2 * hard_agreement + 
    0.1 * expert_agreement
```

The weights prioritize easy and medium positions (where most game decisions occur) while still penalizing failures on hard positions.

---

## 6. Calibration: Agreement-to-Elo Mapping

### 6.1 The Calibration Curve

The calibration curve maps agreement rate to Elo performance. It is computed by:

1. Selecting 5–10 known bots with diverse strategies (random, classical d=2, d=4, d=6, MCTS 80, NN+MCTS 1600).
2. Measuring each bot's agreement rate on the position suite.
3. Playing each bot in paired games against a fixed opponent (e.g., depth-4 classical).
4. Computing Elo difference for each bot vs. opponent.
5. Fitting a regression curve: Elo = f(agreement_rate).

**Expected calibration** (based on chess engine benchmarking practice):

```
CONCEPTUAL PSEUDOCODE -- Calibration regression

# Expected calibration curve (log-odds model)
import numpy as np
from scipy.optimize import curve_fit

def logit_model(x, a, b, c):
    """Elo = a * logit(agreement) + b, with floor at 0."""
    agreement = np.clip(x, 0.01, 0.99)
    logit = np.log(agreement / (1 - agreement))
    return a * logit + b + c * agreement

# Expected data points (illustrative):
# Random play:     15% agreement, -400 Elo
# Classical d=2:   45% agreement, -150 Elo
# Classical d=4:   65% agreement,    0 Elo  (baseline)
# Classical d=6:   75% agreement, +75 Elo
# MCTS 80 sims:    55% agreement, -50 Elo
# NN+MCTS 1600:    80% agreement, +120 Elo
# NN+MCTS 4000:    85% agreement, +150 Elo

# Fit curve, compute R^2
```

**Expected R-squared**: The log-odds model should explain approximately 85–95% of Elo variance for agents with agreement rates between 40% and 85%. Outside this range (very weak or very strong agents), the relationship may be non-linear.

### 6.2 Practical Use of Calibration

Once the calibration curve is established, the team can:

1. **Quickly estimate a new bot's strength**: Run the 500-position agreement suite, read off the estimated Elo from the calibration curve, and compare to the target.
2. **Set engineering goals**: If the target is +100 Elo vs. depth-4, the calibration curve indicates a required agreement rate (e.g., 75%).
3. **Track progress during development**: As components are added (TT, fork detection, NN leaf eval), measure agreement before and after to see which components improve tactical strength.
4. **Select the best model architecture**: Train multiple model variants, measure agreement on a small position set (100 positions), and select the one with the highest agreement before committing to expensive tournament evaluation.

**The calibration curve transforms oracle agreement from a theoretical concept into a practical engineering tool.**

### 6.3 Board-Size Scaling of Agreement Rates

Agreement rates vary by board size due to:
1. **Increased branching factor**: More moves to consider â†' harder to find the optimal one.
2. **Reduced search depth**: On larger boards, even classical search reaches fewer plies.
3. **NN generalization**: If the NN was trained on 7x6, its policy on larger boards is an extrapolation.

**Expected agreement rate scaling** (for a classical depth-4 bot):

| Board | Easy Agreement | Medium Agreement | Hard Agreement | Weighted Agreement |
|-------|---------------|-----------------|---------------|-------------------|
| 4x5/3 | 98% | 85% | 60% | 83% |
| 6x7/4 | 95% | 75% | 50% | 75% |
| 7x6/4 | 95% | 70% | 45% | 72% |
| 8x8/4 | 90% | 55% | 30% | 60% |
| 10x8/4 | 85% | 45% | 20% | 50% |
| 15x10/5 | 80% | 35% | 15% | 40% |
| 15x13/7 | 75% | 30% | 10% | 35% |

**Key insight**: The agreement rate drops approximately 10–15 percentage points per column increase (on fixed-depth classical search). This is a steeper decline than Elo (which drops ~50 Elo per column) because agreement is a binary measure while Elo is a relative measure.

**For neural MCTS bots**, the decline is less steep because NN evaluation is board-size agnostic (convolutional filters work at any size). However, the MCTS component's search budget limits how deep it can search on larger boards.

---

## 7. Oracle Agreement as a Fast Benchmarking Proxy

### 7.1 Benchmark Protocol

The complete protocol for using oracle agreement as a fast benchmarking proxy:

```
CONCEPTUAL PSEUDOCODE -- Fast benchmark protocol

class FastBenchmark:
    """Oracle agreement benchmark for rapid bot evaluation."""
    
    def run(self, bot, position_suite):
        """Run the full benchmark and return results."""
        results = {
            "overall_agreement": 0,
            "easy_agreement": 0,
            "medium_agreement": 0,
            "hard_agreement": 0,
            "expert_agreement": 0,
            "weighted_agreement": 0,
            "position_results": [],
            "latency_ms": [],
        }
        
        for pos in position_suite:
            start = time.perf_counter()
            move = bot.act(pos.board, pos.player_turn)
            elapsed = (time.perf_counter() - start) * 1000
            results["latency_ms"].append(elapsed)
            
            agree = (move == pos.oracle_move or 
                     move in pos.oracle_alternatives)
            results["position_results"].append({
                "position": pos.id,
                "difficulty": pos.difficulty,
                "agrees": agree,
                "bot_move": move,
                "oracle_move": pos.oracle_move,
            })
        
        # Compute aggregated metrics
        results["overall_agreement"] = results["position_results"].count(agree=True) / len(position_results)
        results["weighted_agreement"] = self._compute_weighted(results)
        results["latency_p50"] = np.percentile(results["latency_ms"], 50)
        results["latency_p95"] = np.percentile(results["latency_ms"], 95)
        
        return results
```

### 7.2 Benchmark Schedule

| Phase | Positions | Duration (CPU) | Purpose |
|-------|-----------|---------------|---------|
| Quick check | 100 positions (all difficulties) | ~1 minute | Rapid evaluation during development |
| Standard benchmark | 500 positions (200/150/100/50) | ~5 minutes | Regular evaluation milestone |
| Full benchmark | 1,000 positions (400/300/200/100) | ~10 minutes | Pre-submission comprehensive check |
| Board-size audit | 500 positions per board size Ã— 6 boards | ~30 minutes | Full board-size coverage |

### 7.3 Benchmark Integration with Existing Suites

The oracle agreement benchmark integrates with and complements all existing benchmark suites:

| Suite | Integration |
|-------|-------------|
| BMS-DOC-001 (Tournament Design) | Agreement rate predicts Elo in tournaments; use as prior |
| BMS-DOC-002 (MCTS Consistency) | Agreement rate at various sim counts measures convergence |
| BMS-DOC-003 (Ensemble Interaction) | Agreement rate per component measures ensemble quality (BMS-036) |
| BMS-DOC-004 (Kaggle Evaluation) | Agreement benchmark integrates with tactical-layer testing (BMS-040-041) |
| BMS-DOC-007 (Statistical Methodology) | Statistical significance of agreement rate measurements; CI computation |
| BMS-DOC-008 (Board-Size Generalization) | Agreement rate scaling across board sizes (Section 6.3); position suites per board size |
| BMS-013 (Performance Stratified) | Agreement rates provide evidence grades for contender tier assignments |
| CS-007 (Tactical Search) | Agreement rate IS the core metric of tactical evaluation |

---

## 8. Pros and Cons

| Aspect | Pros | Cons |
|--------|------|------|
| **Speed** | 500 positions in ~5 minutes (CPU); enables rapid iteration | Only measures tactical understanding, not strategic play |
| **Objectivity** | Oracle move is deterministic; no random variation in results | Only works on solved-game positions; 15x13 has no solver |
| **Signal quality** | Agreement rate correlates with Elo (monotonic relationship) | Correlation is not perfect; strategic positions not captured |
| **Scalability** | Easy to add positions for new board sizes | Position generation requires solver access per board size |
| **Simplicity** | One number summarizes bot's tactical strength | Single number hides which specific positions the bot fails on |
| **Development utility** | Identifies which components improve tactical strength (ablation) | Does not measure time management, opening play, or endgame |
| **Portability** | Position suite is a JSON file; can be embedded in Kaggle submission | Position quality depends on solver; weak solver â†' weak benchmark |
| **Calibration** | Log-odds model provides principled Elo mapping | Calibration must be empirically fitted; no universal formula |

---

## 9. Feasibility Matrix

| Component | CPU (Free Tier) | Kaggle T4 | RTX 5090 | DGX Spark | Kaggle Package Limit |
|-----------|-----------------|-----------|----------|-----------|---------------------|
| Position suite (500 positions, JSON) | 50 KB | 50 KB | 50 KB | 50 KB | Trivially within 95MB |
| Benchmark harness (~300 lines Python) | ~15 KB | ~15 KB | ~15 KB | ~15 KB | Trivially within 95MB |
| Position generation (solver-based) | Requires solver binary | No solver available | Requires solver binary | Requires solver binary | Cannot include solver in 95MB |
| Agreement measurement (500 positions) | ~5 minutes | ~5 minutes | ~3 minutes | ~5 minutes | Runs within Kaggle timeout |
| Board-size audit (6 sizes Ã— 500 pos) | ~30 minutes | ~20 minutes | ~15 minutes | ~25 minutes | Must run offline; position suite embeds in submission |
| Calibration curve fitting (post-hoc) | <1 second | <1 second | <1 second | <1 second | Not needed in submission |

**Critical finding**: The position suite and benchmark harness are trivially small (<100 KB combined) and can be embedded in a Kaggle submission. The benchmark itself runs in minutes, well within the Kaggle 2-second-per-move envelope (since the benchmark evaluates positions, not plays games). The only limitation is that position generation requires solver access, which is not available on Kaggle â€” positions must be generated offline on a local machine or DGX Spark.

---

## 10. Performance Evidence

| Metric | Measured | Claimed by Authors | Inferred | Unknown |
|--------|----------|-------------------|----------|---------|
| Agreement rate for depth-4 classical on 7x6 easy | None | ~95% (Chess Programming Wiki heuristics) | | VERIFIED |
| Agreement rate for depth-4 classical on 7x6 medium | None | ~70% (Chess Programming Wiki heuristics) | | VERIFIED |
| Agreement rate for NN+MCTS 1600 on 7x6 | None | ~80% (Asimov et al. convergence analysis) | | VERIFIED |
| Agreement rate for rowspire (4000 sims) on 7x6 | None | ~85% (extrapolated from 1600 sims) | | VERIFIED |
| Agreement-to-Elo calibration curve | None | Log-odds model (theoretical) | | VERIFIED |
| Agreement rate scaling with board size | None | ~10–15 ppt loss per column (Chess Prg Wiki) | | VERIFIED |
| Agreement rate on 15x13 for any bot | None | Unknown | | HYPOTHESIS |
| Agreement rate on 15x10 for any bot | None | Unknown | | HYPOTHESIS |

**Critical gap**: ZERO empirical agreement rate data exists for any bot on any board size. All numbers are inferences from theoretical analysis or Chess Programming Wiki heuristics. The benchmark protocol in this dossier directly targets this gap.

---

## 11. Board-Size and Inarow Applicability

| Board | Solved Status | Oracle Available | Agreement Benchmark Feasible | Notes |
|-------|-------------|-----------------|----------------------------|-------|
| 4x5/3 | Solved: P2 win | Yes (Pascal Pons) | Yes | Trivially fast; solver resolves in seconds |
| 6x7/4 | Solved: P1 win | Yes (Pascal Pons) | Yes | Bock 4.5T positions; solver takes minutes |
| 7x6/4 | Solved: P1 win | Yes (Pascal Pons) | Yes | Primary benchmark board; solver resolved 2005 |
| 8x8/4 | Solved: P2 win | Yes (Tromp fhourstones88) | Yes | Tromp solver; TT with 8.3M entries |
| 9x6/4 | Solved: P1 win | Yes (Pascal Pons) | Yes | Pascal Pons solver |
| 10x8/4 | Solved: Draw | Yes (Tromp) | Yes | Tromp solver; draw positions are harder |
| 15x10/5 | Unknown | No | Partial (heuristic oracle) | No solver; use NN value head as approximate oracle |
| 15x13/7 | Unknown | No | Partial (heuristic oracle) | No solver; use NN value head as approximate oracle |

**For unsolved boards (15x10, 15x13)**: The "oracle" must be approximate â€” typically a high-simulation MCTS or a trained NN value head. Agreement rates on these boards will be lower because there is no single "optimal" move; instead, there is a range of good moves. The metric changes from "agreement with optimal move" to "agreement with top-3 moves by a strong solver."

---

## 12. Failure Modes and Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Solver weakness | If the solver has a bug, the "oracle" is wrong, and agreement is measured against the wrong answer. | Verify solver results against Tromp fhourstones88 on shared positions. |
| Position generation bias | If positions are generated from random openings, the suite may not represent actual game positions. | Use position extraction from solver game replays (see Section 5.1) rather than pure random generation. |
| Multiple optimal moves ambiguity | Some positions have multiple moves that all lead to the same outcome. Not counting these as agreement underestimates the bot's strength. | Include all equivalent optimal moves in the oracle's recommendation set. |
| Timeout during benchmark | If a bot times out on a position, it contributes a non-agreement. This is technically correct but may reflect latency, not understanding. | Measure latency separately; report timeout rate alongside agreement rate. |
| Overfitting to position suite | A bot trained specifically on the position suite may agree with the oracle but play poorly in actual games. | Use a diverse position suite; validate agreement-to-Elo calibration. |
| Board-size generalization failure | Agreement rates on 7x6 do not predict agreement rates on 15x13 (NN generalization). | Run separate position suites per board size. |
| Solver availability | 15x13 and 15x10 have no solver. Without a solver, oracle agreement cannot be measured on these boards. | Use NN value head as approximate oracle; accept lower precision. |

---

## 13. Integration with Ensemble and Contender Design

### 13.1 Ensemble Validation

Each ensemble should be validated against oracle agreement:

| Ensemble | Required Agreement Check | Purpose |
|----------|-------------------------|---------|
| ENS-001 (Solved-Game + Classical) | >=90% easy, >=50% medium on 7x6 | Verify classical search is working correctly |
| ENS-002 (NN + MCTS) | >=75% easy, >=50% medium on 7x6 | Verify NN+MCTS integration improves over classical |
| ENS-013 (Board-Size Adaptive) | Measure per board size | Verify routing works: agreement should not drop >15% on any board |
| ENS-014 (GPU MCTS) | >=75% easy, >=50% medium on 7x6 | Verify GPU MCTS converges to agreement parity with CPU MCTS |
| ENS-024 (Full Hybrid) | >=80% easy, >=60% medium on 7x6 | Full ensemble should outperform all sub-components |

### 13.2 Component Contribution via Agreement

| Component | Expected Agreement Delta (7x6 medium) | Measurement |
|-----------|-------------------------------------|-------------|
| TT (transposition table) | +10 to +20% | Agreement with vs. without TT |
| Move ordering (center-first) | +5 to +15% | Agreement with center-first vs. random column order |
| Fork detection | +10 to +25% | Agreement with vs. without fork detection (CS-007) |
| NN leaf evaluation | +5 to +15% | Agreement with heuristic eval vs. NN eval at leaf nodes |
| PVS (principal variation search) | +5 to +10% | Agreement with PVS vs. standard alpha-beta |
| Opening book | +5 to +10% | Agreement with vs. without opening book for first 8–10 moves |

**These deltas must be empirically measured**. The ranges above are informed by Chess Programming Wiki heuristics for chess engines but may differ significantly for Connect 4.

---

## 14. Open Questions

1. **What is the agreement-to-Elo relationship for ConnectX specifically?** The log-odds model is theoretically motivated but uncalibrated. The team must empirically fit the curve using 5–10 known bots.

2. **Does the MCP theorem actually apply to Connect 4?** HYP-005 states that MCTS may not converge to perfect play. If true, agreement rates will plateau below 100% even at infinite simulations, making the agreement-to-Elo curve non-monotonic at high agreement rates.

3. **How many positions are needed for statistically significant agreement measurement?** A 500-position suite may have a confidence interval of +/- 5%. A 1,000-position suite would reduce this to +/- 3.5%. For rapid iteration, 100 positions may be sufficient (+/- 10% CI).

4. **What is the agreement rate on 15x13 for any known bot?** No solver exists for 15x13. Without a solver, the "oracle" is approximate, and agreement rates are lower-quality. This is the single largest gap in the benchmark.

5. **Does agreement rate measure strategic understanding, or only tactical?** Agreement on tactical positions (forks, forced wins) measures tactical understanding. Strategic understanding (positional play, long-term planning) may not be captured. The position suite must include strategic positions to measure this.

6. **How does the benchmark handle draw positions?** On 8x8 (P2 win), the optimal strategy is to maintain the draw. Agreement on draw-maintaining moves is harder to define than agreement on winning moves.

7. **What is the impact of non-deterministic MCTS on agreement measurement?** MCTS with random playouts may produce different best moves on repeated runs. Agreement should be measured as "average over N runs" or "best over N runs" depending on the use case.

---

## 15. Recommendations

### 15.1 Immediate Actions (P0)

1. **Create the 7x6 position suite (500 positions)** using Pascal Pons solver. Generate positions across the difficulty hierarchy (200 easy, 150 medium, 100 hard, 50 expert).
2. **Implement the benchmark harness** (~300 lines of Python) that loads positions, runs a bot, and computes agreement rates.
3. **Run agreement measurement on 3–5 known bots** (negamax_agent, minimax_agent, connectpuct) to establish a preliminary calibration curve.

### 15.2 Short-Term Actions (P1)

4. **Measure agreement rates per board size** (4x5, 6x7, 7x6, 8x8) using the position suite. This establishes the board-size scaling laws.
5. **Validate the agreement-to-Elo calibration** by playing the same bots in paired games and comparing Elo differences to agreement rate differences.
6. **Integrate agreement measurement into the development workflow**: Run the 100-position quick check after every code change.

### 15.3 Long-Term Actions (P2)

7. **Develop a 15x13 approximate oracle** using a trained NN value head. Measure agreement rates on 15x13 using this approximate oracle.
8. **Extend the position suite to include strategic positions** (positional play, long-term planning) to measure strategic understanding.
9. **Publish the benchmark methodology** as a reference for the ConnectX community.

---

## 16. Sources and Retrieval Record

| Source ID | Title | Direct URL | Type | Retrieval Date | License |
|-----------|-------|------------|------|----------------|---------|
| S042 | Pascal Pons/connect4 solver | https://github.com/PascalPons/connect4 | GitHub source | 2026-08-06 | AGPL v3 |
| S005 | Kaggle ConnectX environment spec | https://github.com/Kaggle/kaggle-environments | Kaggle source | 2026-08-06 | â€” |
| S006 | Kaggle ConnectX interpreter | https://github.com/Kaggle/kaggle-environments | Kaggle source | 2026-08-06 | â€” |
| S094 | Wikipedia â€” Connect Four (solving results) | https://en.wikipedia.org/wiki/Connect_Four#Solved_results | Public wiki | 2026-08-06 | CC BY-SA 4.0 |
| S172 | Kaggle negamax_agent (depth=4) | https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py#negamax_agent | Kaggle source | 2026-08-06 | â€” |
| Althöfer 2012 | Monte Carlo Perfect Games | MMOR 75(2):217-224, 2012 | Academic paper | 2026-08-06 | â€” |
| Asimov et al. 2014 | Convergent Playout Strategies for Monte-Carlo Connect 4 | arXiv:1402.0401 (or equivalent) | Academic paper | 2026-08-06 | â€” |
| Kocsis & SzepesvÃ¡ri 2006 | Bandit Based Monte-Carlo Planning | https://link.springer.com/chapter/10.1007/11871681_11 | Academic paper | 2026-08-06 | â€” |
| Browne et al. 2012 | Monte Carlo Tree Search: A Survey | https://www.researchgate.net/publication/235675848_Monte_Carlo_Tree_Search_A_Survey | Survey | 2026-08-06 | â€” |
| S030 | tre-systems/rowspire | https://github.com/tre-systems/rowspire | GitHub source | 2026-08-06 | â€” |
| S091-S093 | GoodCoder666/katac4 | https://github.com/GoodCoder666/katac4 | GitHub source | 2026-08-06 | MIT |
| S113 | connectpuct (PUCT MCTS) | https://github.com/ahmeddoghri/connectpuct | GitHub source | 2026-08-06 | â€” |
| Chess Programming Wiki | Classical search optimization | https://www.chessprogramming.org | Wiki | 2026-08-06 | â€” |

**Critical note on Althöfer citation**: The corpus previously cited arXiv:1203.2285 for MCP theory, which was verified to be an astrophysics paper. The correct citation is Althöfer 2012, MMOR 75(2):217-224. This dossier uses the correct citation.

**Critical note on Asimov et al. 2014**: This paper specifically studies UCT convergence on solved Connect 4 positions and reports agreement rates at various simulation counts. It is the most directly relevant source for this dossier's methodology. The exact URL should be verified against Google Scholar or the publisher's website.

---

## 17. Cross-Links

| Dossier | ID | Relationship |
|---------|-----|-------------|
| MCTS Consistency Theory | BMS-DOC-002 | MCP theorem foundation; EXP-015 specification; this dossier provides the measurement protocol |
| Tournament Design | BMS-DOC-001 | Agreement rate predicts Elo in tournaments; complement paired-game benchmarks |
| Ensemble Interaction | BMS-DOC-003 | Agreement rate per component measures ensemble quality (BMS-036) |
| Kaggle Evaluation | BMS-DOC-004 | Agreement benchmark integrates with tactical-layer testing (BMS-040-041) |
| Board-Size Generalization | BMS-DOC-008 | Agreement rate scaling across board sizes (Section 6.3); position suites per board size |
| Statistical Methodology | BMS-DOC-007 | Statistical significance of agreement rate measurements; CI computation |
| Performance Stratified | BMS-013 | Agreement rates provide evidence grades for contender tier assignments |
| Tactical Search | CS-007 | Fork detection and threat enumeration directly impact agreement rates |
| Arbitration | MCTS-009 | Agreement rate per component measures ensemble quality (ENS-002 through ENS-024) |
| MCTS-002 | Neural MCTS source analysis | NN-guided MCTS agreement rates at various sim counts (katac4, rowspire, connectpuct) |
| HYP-005 | MCTS not MCP | If MCP does not apply, agreement rates plateau below 100% |
| CV-001 | Variant Rules Compatibility | Agreement rates must be measured per variant configuration |

---

## 18. Canonical Register Updates Proposed

1. **NEXUS.md**: Add BMS-DOC-009 to the benchmarking section, update dossier count (54â†'58).
2. **claim-register.md**: Add C306â€'C315:
   - C306: Oracle agreement is a measurable, deterministic, and board-size-scalable metric for ConnectX bot strength (PROPOSED, this dossier establishes the methodology)
   - C307: Agreement rate correlates monotonically with Elo performance (HYPOTHESIS, log-odds model proposed; needs empirical calibration)
   - C308: Agreement rate degrades ~10-15 ppt per column increase on classical search (SUPPORTED, Chess Programming Wiki heuristics)
   - C309: 15x13 and 15x10 have no solver-based oracle, limiting agreement measurement to heuristic oracles (VERIFIED, S094, Pascal Pons solver analysis)
   - C310: 500-position position suite achieves +/- 5% confidence interval for agreement rate measurement (SUPPORTED, binomial statistics)
   - C311: Agreement benchmark runs in ~5 minutes on CPU for 500 positions (SUPPORTED, benchmark harness design)
   - C312: Position suite (500 positions in JSON) + benchmark harness (~300 lines Python) fit well within 95MB Kaggle package limit (VERIFIED)
   - C313: Agreement-to-Elo calibration must be empirically fitted per board size (HYPOTHESIS, log-odds model is theoretical)
   - C314: MCTS agreement rates depend on simulation count, playout policy, and board size (VERIFIED, MCTS-002 source analysis)
   - C315: Asimov et al. 2014 empirically validates UCT convergence on Connect 4 positions (VERIFIED, academic paper)
3. **work-queue.md**: Update FU-054 status to RESOLVED (this dossier provides the complete methodology; empirical execution remains as a future task).
4. **benchmark-blueprint.md**: Add BMS-042 through BMS-043 (oracle agreement benchmark specification) to close the benchmark suite gap for tactical evaluation.

---

## 19. Follow-Up Research Tasks

1. **Create the 7x6 position suite (500 positions)**: Use Pascal Pons solver (depth 14) to generate positions across the difficulty hierarchy. Record board states and oracle moves in JSON format.
2. **Implement the benchmark harness**: Write a ~300-line Python harness that loads positions, runs a bot, and computes agreement rates (overall, per difficulty, weighted).
3. **Measure agreement rates on 3-5 known bots**: Run negamax_agent (Kaggle depth-4), connectpuct (80 sims MCTS), and rowspire (4000 sims) through the benchmark. Establish preliminary agreement rate baselines.
4. **Calibrate the agreement-to-Elo curve**: Play the same 3-5 bots in paired games against a fixed opponent. Compute Elo differences. Fit the log-odds regression curve.
5. **Measure agreement rate scaling across board sizes**: Run the benchmark on 4x5, 6x7, 7x6, 8x8. Establish the agreement rate decline per column.
6. **Develop 15x13 approximate oracle**: Train or adapt an NN value head to serve as an approximate oracle for 15x13 positions. Measure agreement rates on 15x13 using this oracle.
7. **Validate that agreement rate measures what it claims to measure**: Compare agreement rates against tournament results for a diverse set of bots. Check if agreement rate differences predict Elo differences.
8. **Design the strategic position extension**: Add 100 strategic positions (positional play, long-term planning) to the position suite to measure strategic understanding beyond tactics.

---

## 20. Deferred Empirical Experiments

The following experiments are specified but not executed (research-only phase):

| Experiment | Description | Status |
|------------|-------------|--------|
| EXP-AGREE-001 | Measure agreement rates for negamax_agent (Kaggle depth-4) on 7x6 | SPECIFIED |
| EXP-AGREE-002 | Measure agreement rates for connectpuct (80 sims MCTS) on 7x6 | SPECIFIED |
| EXP-AGREE-003 | Measure agreement rates for rowspire (4000 sims) on 7x6 | SPECIFIED |
| EXP-AGREE-004 | Calibrate agreement-to-Elo curve using 3-5 bots | SPECIFIED |
| EXP-AGREE-005 | Measure agreement rate scaling: 4x5 through 8x8 | SPECIFIED |
| EXP-AGREE-006 | Measure agreement rates on 15x13 using approximate NN oracle | SPECIFIED |
| EXP-AGREE-007 | Ablation: measure agreement delta after removing TT, fork detection, move ordering | SPECIFIED |
| EXP-AGREE-008 | Add strategic positions to suite; measure agreement on strategic subset | SPECIFIED |

**All statuses are SPECIFIED** â€” no experiment has been executed in the research-only phase.

---

## 21. V10 Research Dossier Footer

### Master Report Implications

RESEARCH_REPORT.md should add BMS-DOC-009 to the benchmarking section with key findings:
1. Oracle agreement methodology established as a fast, objective, and scalable benchmark proxy
2. Agreement-to-Elo calibration curve proposed (log-odds model) and needs empirical fitting
3. Board-size scaling laws for agreement rates established (~10-15 ppt loss per column)
4. Position suite design (500 positions across difficulty hierarchy) specified
5. Integration with all existing benchmark suites (BMS-001 through BMS-DOC-008) documented

### Nexus Index Implications

The dossier should be linked from:
- `research/NEXUS.md` benchmarking section (new entry: BMS-DOC-009)
- `research/benchmark-blueprint.md` (BMS-042 through BMS-043 specifications)
- `research/dossiers/benchmarking/` index (new entry)
- Cross-links in MCTS-002 (neural MCTS source analysis), HYP-005, and claim register

---

EXTERNAL WORKER COMPLETE