# Opening Book Research for ConnectX

> **Generated**: 2026-07-30 (Iteration 1)
> **Purpose**: Research opening book design for ConnectX bot
> **Status**: Research based on solved game database and known approaches

---

## What is an Opening Book?

An opening book is a database of precomputed optimal moves for common opening positions. Instead of searching the game tree at each move, the bot looks up the precomputed best move.

### Benefits
- **Instant response**: No search needed (0ms)
- **Guaranteed optimal**: For covered positions
- **Saves computation**: Reduces time spent on early game

### Drawbacks
- **Storage**: Can be large (MBs to GBs)
- **Limited coverage**: Only covers common positions
- **Not generalizable**: 7x6 opening book doesn't work for 15x13

---

## BitBully Opening Database

### Overview
- **Size**: Precomputed opening database for early-game positions
- **Performance**: Constant-time lookups in milliseconds
- **Method**: MTD(f) search of all positions up to ~10-12 moves deep
- **Storage**: Column-row matrix representation (compact)

### Method
1. Search all positions from the starting position to ~10-12 moves
2. For each position, record the best move and its game-theoretic value
3. Store as a hash table: position hash → (best move, value, depth)
4. At runtime: hash the board, lookup the entry, return the move

### Performance
- **Initial position**: ~197 seconds to solve (on 2012 hardware)
- **After 10 moves**: Milliseconds (solved sub-positions)
- **After 14 moves**: Both engines resolve in milliseconds

---

## Building an Opening Book for ConnectX

### Approach 1: From Solved Game Database

**Source**: Böck (2025) complete win-draw-loss table for 7x6
**Method**:
1. For each position with ≤8 pieces, lookup the win/draw/loss
2. Extract the optimal move from the winning line
3. Store position → best move mapping

**Storage**:
- ~4.5 trillion positions total, but only positions reachable from start matter
- Estimated opening book size: 10K-100K positions (common positions)
- Storage per entry: ~20 bytes (hash + move + value)
- Total: ~2MB-20MB

### Approach 2: From Searched Positions

**Method**:
1. Run MTD(f) from the starting position
2. For each position encountered, record the best move
3. Store as a hash table

**Performance**:
- 7x6 board: ~200 seconds per initial position
- After solving, can generate full opening book
- Each search produces ~1,000-10,000 opening book entries

### Approach 3: Neural Network as "Soft Opening Book"

**Method**:
1. Train neural net on opening positions
2. At runtime: neural net predicts best opening move
3. Faster than lookup, no storage cost

**Trade-off**:
- NN is approximate (not guaranteed optimal)
- But works for ALL opening positions (including rare ones)
- And generalizes to larger board sizes

---

## Opening Book Design Patterns

### Hash Table Design

```python
class OpeningBook:
    def __init__(self, max_size=100000):
        self.book = {}  # hash → (move, value, depth)
        self.max_size = max_size
    
    def add(self, board_hash, move, value, depth=0):
        if len(self.book) >= self.max_size:
            self.evict_old_entries()
        self.book[board_hash] = (move, value, depth)
    
    def lookup(self, board_hash):
        return self.book.get(board_hash)
    
    def evict_old_entries(self):
        """Evict entries with lowest depth (least useful)."""
        min_depth = min(v[2] for v in self.book.values())
        keys_to_remove = [k for k, v in self.book.items() if v[2] == min_depth]
        for k in keys_to_remove:
            del self.book[k]
```

### Hash Function
- **Zobrist hashing**: Standard approach
- **Position + move count**: Include turn number for disambiguation
- **Size**: 64-bit hash for reasonable collision avoidance

### Move Encoding
- **Column index**: 0-6 (for 7x6) or 0-14 (for 15x13)
- **Encoding**: 4 bits per move
- **Compact**: ~20 bytes per entry (hash + move + value + depth)

### Entry Value
- **Value**: Win/draw/loss or move count to win
- **Depth**: How deep the search went for this position
- **Score**: Evaluation score (for heuristic opening books)

---

## Opening Book for Different Board Sizes

### 7×6 (Solved)

- **Status**: Known from Böck (2025) complete solution
- **Opening moves**: Column 4 (center) is optimal
- **Coverage**: All reachable positions with ≤8 pieces
- **Size**: ~500K entries (estimated)
- **Storage**: ~10MB

### 15×13 (Unsolved)

- **Status**: Not solved — cannot have perfect opening book
- **Approach**: Use SFT-trained neural net as "soft opening book"
- **Alternative**: Run MTD(f) search at game start, build book during self-play
- **Coverage**: Limited (only positions from self-play games)

### 15×10 (Unsolved)

- **Status**: Not solved — cannot have perfect opening book
- **Approach**: Same as 15x13 (NN-based soft opening book)

### Unified Approach

For multi-board-size support:
1. **7x6**: Use solved game database (hard lookup)
2. **Larger boards**: Use neural net policy (soft lookup)
3. **Transition**: Switch from NN to search when board has <8 pieces

---

## Neural Net as Opening Book

### Concept

Instead of a traditional opening book (hash table), use a neural network to predict opening moves:

1. **Input**: Board state (flat or 2D array)
2. **Output**: Probability distribution over columns
3. **Selection**: Take highest probability move
4. **Fallback**: If NN confidence low, use search

### Advantages

| Feature | Opening Book | Neural Net |
|---------|-------------|------------|
| 7x6 perfect play | ✅ Yes | ⚠️ Depends on training |
| Larger boards | ❌ No | ✅ Generalizes |
| Storage | MBs | KBs |
| Response time | ~0ms | ~0.1ms (GPU) |
| Rare positions | ⚠️ May miss | ✅ Handles all |
| Training required | ❌ No | ✅ Yes |

### Training Neural Net as Opening Book

**Dataset**: Solved 7x6 positions (up to 10 moves from start)
**Architecture**: Simple CNN or MLP
**Training**: Supervised learning on optimal moves from solved positions
**Accuracy**: Expected >95% on solved positions

---

## Open Questions

1. What is the optimal size for a ConnectX opening book?
2. Can we generate an opening book for 15x13 through self-play?
3. Is a neural net opening book better than a traditional hash-based book?
4. What hash function is best for ConnectX positions?
5. How do we handle transposition table entries that overlap with opening book?
6. Can we use GPU to accelerate opening book generation?
7. What's the trade-off between book size and play strength?

---

## References

- BitBully (Markus Thill): Opening database implementation
- Böck (2025): Complete win-draw-loss lookup table for 7x6
- Allis (1988): Knowledge-based approach with opening book
- Allen (1988): Connect Four Proved