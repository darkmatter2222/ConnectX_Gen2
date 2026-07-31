# Iteration 2 Findings — ConnectX Bot Research

> **Generated**: 2026-07-30
> **Purpose**: Document findings from web research and parallel agent execution

---

## Web Research Findings

### New Repositories Identified

| Repository | Stars | Approach | Key Details |
|-----------|-------|----------|-------------|
| sidhantagar/ConnectX | Unknown | Minimax + alpha-beta | Variable board sizes (up to 20×20), configurable win (3-10), Pygame |
| VSZM/ConnectX | Unknown | DQN + minimax | 2-step lookahead, Cython acceleration |
| BEPb/Kaggle_ConnectX | Unknown | AlphaZero MCTS | Self-play RL, PARL framework, xparl cluster |
| marcpaulo15/RL-connect4 | Unknown | SFT → RL CNN | 200K state-action pairs, transfer learning |
| mra1991/connect-four-negamax | Unknown | Symmetric negamax | Bitboards, iterative deepening, symmetry reduction |
| dillonloh/connectx | 0 | Minimax depth-3 | No pruning, wins >60% vs negamax, top 100 Kaggle |
| omarfsosa/connectx | 0 | RL + Kaggle env | Exploring RL with kaggle environment |
| athulshibu/Connect4_look_ahead | 0 | 4 lookahead models | 1-4 moves ahead simulation |

### Key Findings from Web Data

1. **dillonloh/connectx**: Simple minimax (depth-3, no pruning) wins >60% against negamax, reaches top 100 on Kaggle. **Insight**: Simple approaches can be competitive.

2. **athulshibu/Connect4_look_ahead**: Multiple models with different lookahead depths (1-4 moves). **Insight**: Lookahead depth is a tunable parameter.

3. **sidhantagar/ConnectX**: Supports variable board sizes (0-20) and win conditions (3-10). **Insight**: Generalization across configurations is feasible and valuable.

4. **marce1e1e/connectx_mcts**: MCTS implementation exists for ConnectX (details not fully extracted).

5. **BEPb/Kaggle_ConnectX**: AlphaZero-style with PARL framework and distributed training (xparl cluster). **Insight**: Self-play RL is the most sophisticated approach.

---

## Research Areas Being Investigated (Agents Running)

| Agent | Topic | Expected Output |
|-------|-------|-----------------|
| a9ec81c4... | Neural net architectures | Optimal CNN architecture, parameter counts |
| a6929911... | Transfer learning | Generalization from 7x6 to 15x13 |
| af99bdd6... | Time management | Optimal 2-second-per-move strategy |
| a7ae01c7... | Evaluation functions | Best features and weights |
| ac9f6f41... | Training data generation | Data generation strategies from solved positions |
| a2292f98... | Kaggle top bots | Current leaderboard and top strategies |

---

## Additional Data Points from Web Fetches

### BitBully / BitBurny (Markus Thill) — Refined Details

- **Architecture**: C++ core with Python bindings (pybind11)
- **Search**: MTD(f), negamax, null-window algorithms
- **Performance**: ~197.5 seconds on 2012-era hardware
- **Speedup**: 1.5× over baseline at six plies
- **Bitboards**: Dual integer bitboards for constant-time moves
- **Opening DB**: Precomputed victory distances
- **Evaluation**: Game-theoretic values (win/loss/draw)

### Key GitHub Resources

| Repository | Description |
|-----------|-------------|
| MarkusThill/bitburny | High-performance Connect Four solver (C++ core, pybind11) |
| mra1991/connect-four-negamax | Symmetric negamax with bitboards |
| sidhantagar/ConnectX | Minimax with alpha-beta, variable board sizes |

### Known Kaggle Approaches

1. **Minimax-based**: sidhantagar, dillonloh
2. **Hybrid DQN+Minimax**: VSZM
3. **AlphaZero MCTS**: BEPb
4. **SFT→RL**: marcpaulo15
5. **Symmetric negamax**: mra1991

---

## Open Questions from Web Research

1. Why does simple minimax depth-3 (dillonloh) achieve 60%+ win rate against negamax?
2. What is the actual performance difference between depth-3 and depth-8 minimax on Kaggle?
3. How does the "20 board sizes" and "win conditions 3-10" in sidhantagar's repo affect evaluation?
4. Can the 4-model lookahead approach (athulshibu) be combined with a single-model approach?

---

## Hypotheses Generated from This Round

| ID | Hypothesis | Confidence | Status |
|----|-----------|------------|--------|
| H15 | Simple minimax (depth-3) can beat negamax on Kaggle due to negamax's shallow search | Medium | PENDING |
| H16 | Variable board size support is more important than board-specific optimization | Medium | PENDING |
| H17 | Cython acceleration provides 5-10× speedup on evaluation function | Medium | PENDING |
| H18 | 4-model lookahead (multiple depths) outperforms single-depth search | Low | PENDING |

---

## Next Steps

1. Wait for 6 agent results (neural nets, transfer learning, time management, evaluation, training data, Kaggle)
2. Integrate findings into existing research documents
3. Update final conclusion if evidence changes
4. Commit all changes