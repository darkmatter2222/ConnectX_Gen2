# Time Management for ConnectX

> **Generated**: 2026-07-30 (Iteration 2)
> **Purpose**: Optimal time allocation for 2-second per move limit
> **Status**: Research based on web data and known implementations

---

## Time Budget Breakdown

### Kaggle Constraints
- **actTimeout**: 2 seconds per move
- **agentTimeout**: 60 seconds total for the game
- **runTimeout**: 1200 seconds total for the episode

### Recommended Allocation

| Game Phase | Time per Move | Total Time | Strategy |
|-----------|---------------|------------|----------|
| Opening (0-10 moves) | 0.3-0.5s | 3-5s | Shallow search or opening book |
| Midgame (10-40 moves) | 1.0-1.5s | 30-50s | Deep search with optimizations |
| Endgame (40+ moves) | 1.5-2.0s | 15-20s | Full search or endgame DB |
| Overtime (>60s agentTimeout) | 0.5-1.0s | - | Reduced search to conserve time |

### Time Remaining Awareness

```python
def time_aware_search(time_left, moves_left, total_time=60):
    """Adjust search strategy based on remaining time and moves."""
    if time_left > 30:
        # Early game: conservative search
        return search_depth_for_time(1.0)
    elif time_left > 10:
        # Mid game: normal search
        return search_depth_for_time(1.5)
    else:
        # Late game / overtime: aggressive time management
        return search_depth_for_time(min(2.0, time_left * 0.8))

def search_depth_for_time(time_budget):
    """Find maximum depth achievable within time budget."""
    for depth in range(1, 20):
        nodes = estimate_nodes(depth)
        time = nodes / nodes_per_second
        if time > time_budget:
            return depth - 1
    return 19
```

---

## Progressive Deepening

### How It Works

1. Search depth 1 → record best move
2. Search depth 2 → update best move
3. Search depth 3 → update best move
4. ... continue until time runs out
5. Return best move found at deepest depth

### Implementation

```python
def progressive_deepening(board, config, time_limit=2.0):
    """Iterative deepening with progressive depth."""
    best_move = None
    depth = 0
    start_time = time.time()
    
    while time.time() - start_time < time_limit:
        depth += 1
        move = alpha_beta_search(board, config, depth, 
                                  alpha=-float('inf'), beta=float('inf'))
        best_move = move['move']
        # If move's score changed significantly, continue deeper
        if depth > 4 and abs(move['score'] - prev_score) < 1:
            break  # Score stable, no need to go deeper
        prev_score = move['score']
    
    return best_move
```

### Benefits
- **Guaranteed move**: Always return a move within time limit
- **Best depth**: Automatically find optimal depth
- **TT reuse**: Transposition table from lower depths helps higher depths
- **Time efficiency**: No wasted computation on unnecessary depth

### Drawbacks
- **Overhead**: Re-searching lower depths
- **Solutions**: Store TT between iterations, skip known moves

---

## Dynamic Time Allocation

### Game-Phase-Based Strategy

| Phase | Characteristics | Strategy |
|-------|----------------|----------|
| **Opening** | Many moves, low complexity | Shallow search (depth 4-6) |
| **Transition** | Board filling, threats emerging | Medium search (depth 8-10) |
| **Midgame** | Complex position, many threats | Deep search (depth 10-12) |
| **Late midgame** | Fewer pieces, simpler | Deeper search (depth 12+) |
| **Endgame** | < 8 pieces, often solved | Endgame DB lookup or full search |

### Piece Count Heuristic

```python
def estimate_complexity(board):
    """Estimate board complexity by piece count."""
    pieces = sum(1 for cell in board if cell != 0)
    max_pieces = len(board)
    ratio = pieces / max_pieces
    
    if ratio < 0.3:
        return "opening"  # Few pieces, many branches
    elif ratio < 0.7:
        return "midgame"  # Complex position
    elif ratio < 0.9:
        return "endgame"  # Few pieces, simple
    else:
        return "terminal"  # Near game over
```

### Overtime Management

When agentTimeout (60s) is exceeded, switch to conservative strategy:
1. Reduce search depth by 50%
2. Use opening book more aggressively
3. Prioritize time-critical moves
4. If time runs out, return random valid move (avoid timeout failure)

---

## Per-Move Budget Optimization

### What to Optimize Per Move

| Factor | Impact | Optimization |
|--------|--------|-------------|
| Move ordering | High (2-3× speedup) | TT → threats → center |
| TT size | High (affects hit rate) | Large TT, depth-based eviction |
| Algorithm choice | Medium (MTD(f) vs AB) | Profile and benchmark |
| JIT compilation | High (5-10×) | Numba for pure Python |
| Bitboard representation | Medium | Use bit operations |

### Time-Per-Node Analysis

```python
# If we need 2 seconds per move, and alpha-beta at depth 10 visits 100K nodes:
nodes_per_second = 100_000 / 2.0  # 50K nodes/sec
# To achieve depth 12 (visiting 10M nodes), we need:
time_needed = 10_000_000 / 50_000  # 200 seconds! Too slow.

# Solution: Optimize move ordering to get 1M nodes/sec
time_needed = 10_000_000 / 1_000_000  # 10 seconds at depth 12
# Still too slow. Need to reduce depth or optimize further.
```

### Key Insight

> **The optimal per-move strategy depends on the game phase:**
> - Early game: Don't waste time — use opening book
> - Midgame: Spend most time — position is complex
> - Endgame: Use endgame DB or shallow search

---

## Benchmark Reference

### Expected Nodes/Second (Python, 7x6)

| Optimization | Depth 8 | Depth 10 | Depth 12 |
|-------------|---------|----------|----------|
| Pure Python | ~30K | ~3K | ~100 |
| +TT | ~50K | ~5K | ~200 |
| +TT + MO | ~100K | ~10K | ~500 |
| +TT + MO + PVS | ~150K | ~15K | ~1K |
| +Numba | ~500K | ~50K | ~3K |
| +Numba + all opt | ~1M | ~100K | ~8K |

### Time per Move (Python)

| Depth | Pure + TT + MO | +Numba | Notes |
|-------|---------------|--------|-------|
| 6 | ~0.1s | ~0.01s | Fast, good for opening |
| 8 | ~0.5s | ~0.05s | Good balance |
| 10 | ~5s | ~0.5s | Edge of time limit |
| 12 | ~50s | ~5s | Exceeds limit without optimization |

### Key Takeaway

> **Without Numba/JIT, depth 8-10 is the practical limit for 2-second moves.**
> **With Numba/JIT, depth 10-12 is achievable.**
> **With C++ binding, depth 14+ is possible.**

---

## Open Questions

1. What's the optimal time allocation per move across a full game?
2. How to predict time needed for a given depth?
3. Can we use early moves to "warm up" later searches?
4. What's the impact of "time left" vs "moves left" on strategy?
5. How to handle the 60-second agentTimeout gracefully?

---

## References

- BitBully: Dynamic depth based on board complexity
- mra1991: Iterative deepening with time limits
- dillonloh: Simple depth-3 minimax (no need for deep search?)