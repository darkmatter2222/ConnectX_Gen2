# Iteration 4 Findings — ConnectX Bot Research

> **Generated**: 2026-07-31
> **Purpose**: Document findings from web research and agent execution

---

## Web Research Findings

### BitBully (Markus Thill) — Refined Details

- **Search Algorithm**: MTD(f) with null-window negamax
- **Bitboard Representation**: Optimized bitwise operations for efficient processing
- **Evaluation**: Integer values (win/loss from current player's perspective)
- **Opening DB**: Precomputed databases for early positions
- **Performance**: 197.5 seconds on 2012-era hardware for initial position
- **Optimizations**: 
  - Transposition table with 1 million entries
  - Threat detection
  - Center-first move ordering
  - Huffman-encoded lookup tables
- **Core**: C++ with Python wrappers
- **Claim**: "Fast perfect-play Connect Four solver"

### mra1991/connect-four-negamax — Refined Details

- **Minimax/Negamax**: Single symmetric negamax loop (score(parent) = -score(child))
- **Alpha-Beta**: Bounds eliminate branches that cannot affect final decision
- **Bitboards**: Two Python integers (one per player) for rapid bitwise checks
- **Transposition Table**: Stores depth, score, exact/lower-bound/upper-bound, best move, search generation
- **Move Ordering**: 
  1. Transposition table move
  2. Immediate winning moves
  3. Immediate defensive blocks
  4. Killer moves
  5. Positional and historical heuristics
- **Evaluation**: Nonterminal boards analyzed (not just zero)
  - Central dominance
  - Open sequences
  - Threat density
  - Ply-adjusted scores (faster wins preferred, losses delayed)

### GitHub Repos Found

| Repository | Stars | Language | Approach | Details |
|-----------|-------|----------|----------|---------|
| MarkusThill/BitBully | ~68 | C++ | MTD(f) + bitboards | Perfect-play solver, 197.5s on 2012 hardware |
| mra1991/connect-four-negamax | ~7 | Python | Symmetric negamax | Bitboards, TT, killer heuristic, evaluation |
| danielspottiswood/ML_Connect_4 | 0 | Python | NN + minimax | Hybrid approach |
| Axelredx/ConnectX_AI | 1 | Java | 8-move lookahead | Targets L0/L1 opponents |
| ayeennp/ConnectFour-bot | 0 | C | 8-move lookahead | Claims "(almost) perfect" play |
| darkatwi/Connect-4 | 0 | C | Minimax + AB | Console game with difficulty tiers |
| Amir-rfz/Connect-4-Game-Bot | 0 | HTML | Minimax | Adaptive gameplay logic |

---

## Key Patterns Observed

1. **Compiled languages dominate**: C++ (BitBully), C (ayeennp, darkatwi) achieve deeper lookahead than Python
2. **Bitboards are critical**: Both top engines use bitboard representation for constant-time operations
3. **MTD(f) over alpha-beta**: BitBully uses MTD(f) which is more efficient for exact values
4. **Hybrid approaches emerging**: NN + minimax (danielspottiswood) shows the trend
5. **Open source is sparse**: Most implementations have 0-1 stars; no MCTS-based public repos

---

## Hypotheses to Track

| ID | Hypothesis | Confidence | Status |
|----|-----------|------------|--------|
| H19 | C/C++ minimax with 8-move lookahead outperforms Python at depth 3 | High | PENDING |
| H20 | Hybrid NN + minimax is the best approach for Kaggle ConnectX | Medium | PENDING |
| H21 | 8-move lookahead is achievable in compiled languages but not Python | High | PENDING |

---

## Next Steps

1. Wait for 5 agent results (GPU, MCTS, game theory, open-source bots, advanced search)
2. Create comprehensive research documents from agent findings
3. Update research trajectory and final conclusion
4. Commit and push to origin