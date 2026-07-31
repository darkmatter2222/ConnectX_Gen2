# Iteration 3 Findings — ConnectX Bot Research

> **Generated**: 2026-07-30
> **Purpose**: Document findings from web research and agent execution

---

## Web Research Findings

### New Repositories Identified (Iteration 3)

| Repository | Stars | Approach | Key Details |
|-----------|-------|----------|-------------|
| Mikesteinberg/ConnectX | 1 | RL | "Reinforcement Learning Model for Connect 4, Connect 5, etc" |
| Axelredx/ConnectX_AI | 1 | Java, 8-move lookahead | "AxelBrain" - targets L0/L1 opponents, CXPlayerTester utility |
| danielspottiswood/ML_Connect_4 | 0 | NN + Minimax hybrid | "Neural network + minimax recursive algorithm" |
| ayeennp/ConnectFour-bot | 0 | C, 8-move lookahead | "Almost perfect" game via minimax checking 8 moves ahead |
| darkatwi/Connect-4 | 0 | C, minimax+AB | Console game with difficulty tiers (Easy/Medium/Hard) |
| Amir-rfz/Connect-4-Game-Bot | 0 | HTML, minimax | Adaptive gameplay logic |
| GabrielBatavia/Connect4-for-ConnectX | 0 | Jupyter | Rule adaptation for Kaggle |
| Midkemma/ConnectX | 0 | C# | Flexible board rules |
| BobMorane22/ConnectX-deprecated | 0 | C++ | Configurable AI training |

### Key Findings

1. **Axelredx/ConnectX_AI**: Java-based "AxelBrain" AI with **8-move lookahead** targeting Kaggle L0/L1. Has testing utility (CXPlayerTester) with repetition and timeout controls.

2. **ayeennp/ConnectFour-bot**: C implementation claiming **"(almost) perfect" play** via minimax checking **8 moves ahead**. Notably, 8 moves = 16 plies is quite deep for a pure Python approach.

3. **danielspottiswood/ML_Connect_4**: Hybrid approach (NN + minimax) - confirms the hybrid trend is common across implementations.

4. **Mikesteinberg/ConnectX**: RL model supporting multiple win conditions (Connect 4, Connect 5, etc) - similar to sidhantagar's approach.

5. **BobMorane22/ConnectX-deprecated**: C++ with configurable training - shows C++ implementations exist.

### Notable Pattern

Most GitHub repos use **minimax with alpha-beta pruning** as the core algorithm. Only a few use neural networks. No one seems to be using MCTS for ConnectX.

---

## Research Agents Running

| Agent | Topic | Status |
|-------|-------|--------|
| af6e4ba8... | Kaggle leaderboard/competition | Running |
| a45b3b2b... | GPU game AI | Completed (output empty) |
| ada35f63... | MCTS for ConnectX | Completed (output empty) |
| ad881d76... | Game theory | Completed (output empty) |
| a5654603... | Open-source bots | Completed (output empty) |

---

## Hypotheses to Track

| ID | Hypothesis | Confidence | Status |
|----|-----------|------------|--------|
| H19 | C/C++ minimax with 8-move lookahead outperforms Python at depth 3 | High | PENDING |
| H20 | Hybrid NN + minimax is the best approach for Kaggle ConnectX | Medium | PENDING |
| H21 | 8-move lookahead is achievable in compiled languages but not Python | High | PENDING |

---

## Next Steps

1. Wait for Kaggle agent to complete
2. Create comprehensive research documents from agent findings
3. Update research trajectory and final conclusion
4. Commit and push to origin