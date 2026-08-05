# ConnectX Component Catalog

Reusable components extracted from the research corpus. Components are atomic, composable, and independently verifiable.

---

## Component Summary Table

| ID | Name | Function | Board-size Support | Compute Profile |
|----|------|----------|-------------------|-----------------|
| CMP-001 | Solved-Game Tablebook | Lookup optimal move from pre-computed database | 7x6 (solved), 9x6 | O(1) lookup, negligible memory |
| CMP-002 | Alpha-Beta Search | Depth-limited minimax with pruning + move ordering | All (4x4-15x13) | O(b^d) worst, O(b^(d/2)) best |
| CMP-003 | Transposition Table | Cache evaluated positions with LRU eviction | All (~10M entries max) | O(1) lookup, O(n) eviction |
| CMP-004 | Fork Detection | Identify positions with two simultaneous threats | All ConnectX variants | O(7) per position |
| CMP-005 | MCTS with PUCT | Monte Carlo tree search with UCB selection | All (7x6 ~1-2K sims/2s) | ~50-400 sim/s (Python) |
| CMP-006 | NN Policy Prior (ResNet) | Generate policy prior over legal moves | 7x6 (trained on) | Sub-1ms on T4 (FP16) |
| CMP-007 | TensorRT FP16 Inference | Accelerated NN inference on GPU | All (GPU-independent) | 1.10ms ResNet-18 on T4 |
| CMP-008 | Game-Phase Routing | Select algorithm by game phase | All | O(1) phase detection |
| CMP-009 | MCTS Warm-Start | Seed MCTS with classical search results | All | AB depth-4 (~50-100ms) + MCTS |
| CMP-010 | Asymmetric Evaluation | Bias toward proactive defense via scoring weights | All | O(1) formula |
| CMP-011 | NNUE Evaluation Function | Neural network updated efficiently — incremental position eval | 7x6 | O(1) incremental update |
| CMP-012 | Phase Detection | Classify position as opening/midgame/endgame | All | O(1) piece-count check |
| CMP-013 | Midgame Tactical Search | Depth-6+ alpha-beta for tactical positions | 7x6 | O(b^6) with pruning |
| CMP-014 | Endgame Tablebook Lookup | Lookup pre-computed endgame results | 7x6+ | O(1) lookup |
| CMP-015 | TensorRT INT8 Inference | Quantized NN inference for ResNet value networks | All (GPU) | 3-5x speedup over FP32 |
| CMP-016 | Quantization Calibration | Generate representative calibration dataset for INT8 | All | O(1000) positions |
| CMP-017 | Board-Size Router | Select classical search vs neural MCTS by board dimensions | All | O(1) dimension check |
| CMP-018 | NNUE Incremental Update | Delta-based NNUE feature update for move application | 7x6 | O(1) feature delta |

---

## Detailed Component Entries

### CMP-001 — Solved-Game Tablebook

| Attribute | Value |
|-----------|-------|
| **Function** | Lookup optimal move from pre-computed solved-game database for opening phase |
| **Evidence** | C001 (VERIFIED — 7x6 solved, first player wins from center column) |
| **Board-size Support** | 7x6 only (solved); potentially 9x6 |
| **Compute Profile** | O(1) lookup per position; negligible memory for cached subset |
| **Compatibility** | Compatible with all search algorithms; incompatible with pure random play |
| **Known Interactions** | Eliminates opening-phase MCTS inconsistency; pairs well with alpha-beta mid-game |
| **Risks** | Tablebook size grows exponentially with piece count; transitions at boundaries may be exploitable |
| **Contenders** | tromp book88 (8x8, ~500MB), Pascal Pons solver (depth-14), H-ENSEMBLE-001 |
| **Source IDs** | S028 |
| **Claim IDs** | C001, C002, C135 |

### CMP-002 — Alpha-Beta Search with Move Ordering

| Attribute | Value |
|-----------|-------|
| **Function** | Depth-limited minimax with alpha-beta pruning and heuristic move ordering |
| **Evidence** | C008 (VERIFIED — center-first ordering 3-5x speedup); C097 (VERIFIED — 8-heuristic move ordering hierarchy) |
| **Board-size Support** | All (4x4 to 15x13); practical on 7x6, 9x6, 10x8 |
| **Compute Profile** | O(b^d) worst-case; O(b^(d/2)) with perfect ordering; practical depth ~8-12 on 7x6 in Python |
| **Compatibility** | Works with all board representations; pairs well with TT and fork detection |
| **Known Interactions** | TT probe is the most impactful ordering heuristic; center-first ordering universal across all engines |
| **Risks** | Shallow depth (d3) easily defeated by MCTS; depth >=8 needed for near-optimal 7x6 play |
| **Contenders** | ariaborin (TT + history + threat-map), QveenCoder (minimax + alpha-beta), tromp/fhourstones88 |
| **Source IDs** | S050, S051 |
| **Claim IDs** | C008, C097 |

### CMP-003 — Transposition Table

| Attribute | Value |
|-----------|-------|
| **Function** | Store evaluated positions to avoid re-computation, with LRU eviction |
| **Evidence** | C071 (NEEDS_CORRECTION — ariaborin TT source code needs re-verification) |
| **Board-size Support** | All; practical up to ~10M entries |
| **Compute Profile** | O(1) lookup; O(n) eviction where n = table size |
| **Compatibility** | Compatible with all search algorithms; standard in classical engines |
| **Known Interactions** | Amplifies alpha-beta effectiveness; pairs with move ordering for maximum pruning |
| **Risks** | Memory usage scales linearly with table size; stale entries may mislead search |
| **Contenders** | ariaborin (10M-entry TT with LRU), QveenCoder, tromp/fhourstones88 |
| **Source IDs** | S045 |
| **Claim IDs** | C071 |

### CMP-004 — Fork Detection (Tactical Guard)

| Attribute | Value |
|-----------|-------|
| **Function** | Identify positions with two simultaneous threats (forks) — highest-value tactical pattern |
| **Evidence** | C094 (VERIFIED — Tromp inline fork detection O(7)) |
| **Board-size Support** | All ConnectX variants (4x5 to 15x13) |
| **Compute Profile** | O(7) per position; negligible overhead |
| **Compatibility** | Works with all search algorithms; independent of board representation |
| **Known Interactions** | Critical for alpha-beta; MCTS must discover forks through random playouts |
| **Risks** | O(7) formula is board-size dependent; larger boards may have more fork patterns |
| **Contenders** | tromp/fhourstones88 (Search.cpp ab()), H-ENSEMBLE-001, H-ENSEMBLE-003 |
| **Source IDs** | S075 |
| **Claim IDs** | C094 |

### CMP-005 — MCTS with PUCT Selection

| Attribute | Value |
|-----------|-------|
| **Function** | Monte Carlo tree search with upper confidence bound for action selection |
| **Evidence** | C137 (VERIFIED — connectpuct PUCT 11/20 vs minimax d3); C138 (VERIFIED — katac4 LCB effective) |
| **Board-size Support** | All; practical on 7x6 with ~1000-2000 simulations in 2s |
| **Compute Profile** | ~50-400 simulations/second in Python; ~1M simulations in 2s on Kaggle T4 |
| **Compatibility** | Works with any evaluation function; pairs with NN policy priors |
| **Known Interactions** | Asymptotically consistent (C142) but finite-sample bounds unknown for Connect 4 |
| **Risks** | Cannot identify long forced-draw sequences (C135 — consistency problem); no solved-game integration |
| **Contenders** | connectpuct (PUCT), rowspire (neural-guided MCTS), katac4 (ResNet + PUCT) |
| **Source IDs** | S029, S039, S091 |
| **Claim IDs** | C135, C137, C142 |

### CMP-006 — Neural Network Policy Prior (ResNet)

| Attribute | Value |
|-----------|-------|
| **Function** | Generate policy prior pi_NN over legal moves to guide MCTS root expansion |
| **Evidence** | C148 (VERIFIED — katac4 ResNet: b3c128nbt, 3 bottleneck blocks, 128 channels, ~530K params) |
| **Board-size Support** | 7x6 (trained on); unverified on larger boards (C014 HYPOTHESIS) |
| **Compute Profile** | Sub-1ms on T4 with TensorRT FP16 (1.10ms for ResNet-18, target sizes smaller) |
| **Compatibility** | Replaces Dirichlet noise in MCTS root; feeds into NN-guided leaf evaluation |
| **Known Interactions** | 80% pi_NN + 20% uniform exploration recommended; NN value replaces random playouts at leaves |
| **Risks** | NN overfit to 7x6; training pipeline partially specified (C163 HYPOTHESIS); generalization unverified |
| **Contenders** | katac4 (ResNet), rowspire (MLP), marcpaulo15 (CNN) |
| **Source IDs** | S091, S092, S101 |
| **Claim IDs** | C148, C163 |

### CMP-007 — TensorRT FP16 Inference

| Attribute | Value |
|-----------|-------|
| **Function** | Accelerated neural network inference on Kaggle T4 GPU using TensorRT FP16 |
| **Evidence** | C150 (NEEDS_CORRECTION — source ID mismatch); C146 (SUPPORTED — TensorRT FP16 benchmarks) |
| **Board-size Support** | All (independent of board size — runs on GPU) |
| **Compute Profile** | 1.10ms ResNet-18 on T4; sub-0.5ms for target sizes (50-530K params) |
| **Compatibility** | Any ONNX-compatible NN; requires GPU (T4 on Kaggle, RTX on local) |
| **Known Interactions** | Enables NN-guided MCTS within 2s budget; pairs with NN policy prior |
| **Risks** | Source attribution for specific benchmarks is broken; RTX 5090 benchmarks unverified |
| **Contenders** | katac4 (TensorRT FP16 deployment), DEEP-GAP, Francesco Pochetti |
| **Source IDs** | S093 |
| **Claim IDs** | C146, C150 |

### CMP-008 — Game-Phase Routing

| Attribute | Value |
|-----------|-------|
| **Function** | Select different search algorithms based on game phase (piece count, board state) |
| **Evidence** | C102 (VERIFIED — opening theory); H-ENSEMBLE-001 (proposed routing mechanism) |
| **Board-size Support** | All |
| **Compute Profile** | Minimal overhead (phase detection is O(1)) |
| **Compatibility** | Universal — can route between any combination of components |
| **Known Interactions** | Opening → solved-game; mid-game → alpha-beta or MCTS; endgame → deep search |
| **Risks** | Phase boundary transitions may be exploitable; phase boundaries not empirically determined |
| **Contenders** | H-ENSEMBLE-001 (proposed), H-ENSEMBLE-002 (proposed) |
| **Source IDs** | S028 |
| **Claim IDs** | C102, C139 |

### CMP-009 — MCTS Warm-Start

| Attribute | Value |
|-----------|-------|
| **Function** | Use classical search to seed MCTS children with informed move ordering |
| **Evidence** | C137 (VERIFIED — connectpuct PUCT benchmark) |
| **Board-size Support** | All |
| **Compute Profile** | Alpha-beta depth-4 (~50-100ms) + MCTS with remaining budget |
| **Compatibility** | MCTS-compatible only; requires alpha-beta integration |
| **Known Interactions** | Reduces MCTS waste on bad moves; alpha-beta depth choice affects quality |
| **Risks** | Alpha-beta may mis-order in complex positions; MCTS may override warm-start benefit |
| **Contenders** | H-ENSEMBLE-004 (proposed) |
| **Source IDs** | S091 |
| **Claim IDs** | C137 |

### CMP-010 — Asymmetric Evaluation Function

| Attribute | Value |
|-----------|-------|
| **Function** | Weighted evaluation that biases toward proactive defense (opponent-threat amplification) |
| **Evidence** | C005 (VERIFIED — QveenCoder and nguyenthequang both implement 100K/100/-120 scoring) |
| **Board-size Support** | All |
| **Compute Profile** | O(1) — simple formula, negligible overhead |
| **Compatibility** | Works with any search algorithm; standard in classical engines |
| **Known Interactions** | 1.2x opponent-threat amplification creates proactive defense bias |
| **Risks** | Values are implementation-specific; may not generalize across board sizes |
| **Contenders** | QveenCoder, nguyenthequang, H-ENSEMBLE-003 |
| **Source IDs** | S050, S051 |
| **Claim IDs** | C005, C059 |

---

## Component Compatibility Matrix

Legend: **V** = Compatible, **X** = Incompatible, **N/A** = Self.

Cells record the **row component's compatibility with the column component**. Each cell notes the integration assumption or incompatibility.

```
         | CMP-001 | CMP-002 | CMP-003 | CMP-004 | CMP-005 | CMP-006 | CMP-007 | CMP-008 | CMP-009 | CMP-010
---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+--------
CMP-001  |   N/A   |    V    |    V    |    V    |    X    |   N/A   |   N/A   |    V    |    X    |   N/A
CMP-002  |    V    |   N/A   |    V    |    V    |    V    |   N/A   |   N/A   |    V    |    V    |    V
CMP-003  |    V    |    V    |   N/A   |    V    |    V    |   N/A   |   N/A   |    V    |    V    |    V
CMP-004  |    V    |    V    |    V    |   N/A   |    V    |   N/A   |   N/A   |    V    |    V    |    V
CMP-005  |    X    |    V    |    V    |    V    |   N/A   |    V    |    V    |    V    |    V    |   N/A
CMP-006  |   N/A   |   N/A   |   N/A   |   N/A   |    V    |   N/A   |    V    |   N/A   |   N/A   |   N/A
CMP-007  |   N/A   |   N/A   |   N/A   |   N/A   |    V    |    V    |   N/A   |   N/A   |   N/A   |   N/A
CMP-008  |    V    |    V    |    V    |    V    |    V    |   N/A   |   N/A   |   N/A   |    V    |   N/A
CMP-009  |    X    |    V    |    V    |    V    |    V    |   N/A   |   N/A   |    V    |   N/A   |   N/A
CMP-010  |   N/A   |    V    |    V    |    V    |   N/A   |   N/A   |   N/A   |   N/A   |   N/A   |   N/A
```

### Compatibility Notes

#### Confirmed Compatible Pairs

| Pair | Interaction | Assumption |
|------|-------------|------------|
| CMP-001 + CMP-002 | Tablebook feeds into alpha-beta as opening solver | Routing via CMP-008 recommended at phase boundary |
| CMP-001 + CMP-003 | TT cache can include tablebook positions | Same game-state representation required |
| CMP-001 + CMP-004 | Tablebook does not conflict with fork detection | Fork detection applies only outside tablebook range |
| CMP-002 + CMP-003 | TT accelerates alpha-beta search via position reuse | Standard classical-engine pattern; 10M-entry tables practical on 7x6 |
| CMP-002 + CMP-004 | Fork detection serves as move-ordering heuristic for AB | Priority: fork > TT > center-first > history heuristic |
| CMP-002 + CMP-005 | Alpha-beta can seed or bound MCTS search | Warm-start (CMP-009) formalizes this interaction |
| CMP-002 + CMP-008 | Phase routing uses alpha-beta as mid-game engine | Depth selection depends on time budget and phase |
| CMP-002 + CMP-009 | Alpha-beta depth choice determines warm-start quality | Depth-4 to depth-8 recommended for warm-start; deeper increases latency |
| CMP-002 + CMP-010 | Asymmetric evaluation weights alpha-beta leaf scores | Values 100K/100/-120 are empirically validated on 7x6 |
| CMP-003 + CMP-004 | TT stores fork-detected positions | No conflict; both independent of board representation |
| CMP-003 + CMP-005 | TT is shared across MCTS sub-trees | LRU eviction key must be hashable across MCTS visits |
| CMP-003 + CMP-008 | Phase-specific TT sub-tables avoid cross-phase contamination | Separate TT namespaces recommended per phase |
| CMP-003 + CMP-010 | Asymmetric scores stored in TT entries | Same evaluation function required for consistent re-lookup |
| CMP-004 + CMP-005 | Fork detection biases MCTS playout selection | Independent of board representation; O(7) per position |
| CMP-004 + CMP-008 | Fork detection applicable in all phases | Phase routing uses fork detection in mid-game and endgame |
| CMP-004 + CMP-010 | Proactive defense amplifies fork-threat evaluation | 1.2x threat amplification compounds fork-value scoring |
| CMP-005 + CMP-006 | NN policy prior guides MCTS root expansion | 80/20 mix of pi_NN and uniform exploration recommended |
| CMP-005 + CMP-007 | TensorRT acceleration enables deep MCTS within budget | 1.10ms per forward pass enables thousands of NN-guided playouts |
| CMP-005 + CMP-008 | Phase routing selects MCTS for mid-game exploration | NN prior (CMP-006) active only in phases using NN inference |
| CMP-005 + CMP-010 | NN value head or leaf evaluation uses asymmetric scoring | Default NN training on random play may not capture proactive bias |
| CMP-006 + CMP-007 | TensorRT runs the ResNet model at inference time | ONNX export required; FP16 precision targets sub-1ms |
| CMP-007 + CMP-008 | Phase routing activates NN inference only in selected phases | GPU context switching overhead must be amortized across phases |
| CMP-008 + CMP-009 | Phase routing triggers warm-start before MCTS activation | Routing decision must complete before warm-start latency cost |
| CMP-009 + CMP-010 | Warm-start leaf evaluation uses asymmetric scoring | Same evaluation parameters as AB search for consistency |

#### Incompatible Pairs

| Pair | Reason for Incompatibility |
|------|---------------------------|
| CMP-001 + CMP-005 | Solved-game tablebook overrides MCTS randomness; MCTS cannot integrate with pre-solved positions without breaking asymptotic consistency guarantees. Tablebook provides exact answers; MCTS converges to optimal via sampling — these are contradictory epistemologies for the opening phase. |
| CMP-001 + CMP-009 | Warm-start uses alpha-beta to seed MCTS; alpha-beta with tablebook bypass is not a warm-start signal, it is a direct answer. The seed would always be the tablebook move, collapsing MCTS exploration entropy to zero. |
| CMP-006 + non-NN components | NN policy prior is only meaningful for MCTS root expansion (CMP-005) and NN-guided leaf evaluation (CMP-005 leaves). Alpha-beta search does not use a policy prior — it uses move ordering heuristics (CMP-002) and evaluation functions (CMP-010). |
| CMP-007 + CPU-only runtime | TensorRT requires GPU (T4 on Kaggle, RTX on local). Cannot run on CPU-only environments. |
| CMP-008 + phase-boundary exploits | Phase routing transitions are inherently exploitable if an opponent can detect phase boundaries. This is not a strict incompatibility but a known risk that constrains the component's use in competitive settings. |
| CMP-010 + NN training without bias injection | The asymmetric evaluation function (CMP-010) is a hand-crafted heuristic. If the NN is trained on random play data (no bias injection), the NN value head will not reflect the proactive-defense bias. Either train the NN with biased self-play, or blend CMP-010 scores with NN value at inference time. |

#### Integration Assumptions

The following assumptions are required for multi-component integration:

1. **State representation uniformity**: All components must agree on a canonical board encoding (bitboard, array, or hash) to enable TT sharing and phase routing.

2. **Phase boundary calibration**: Game-phase routing (CMP-008) requires empirically determined piece-count thresholds for opening/mid-game/endgame transitions. These thresholds are board-size dependent and must be tuned per board.

3. **Evaluation function consistency**: When CMP-010 (asymmetric evaluation) is used alongside CMP-003 (TT), the same evaluation parameters must be active at write and read time to prevent stale/misleading cache entries.

4. **NN alignment with heuristics**: When CMP-006 (NN policy prior) and CMP-002 (alpha-beta) are both active in a hybrid engine (via CMP-008 or CMP-009), the NN's learned priors should align with the heuristic move ordering to avoid conflicting signals.

5. **Resource budget allocation**: Game-phase routing (CMP-008) distributes the time budget across phases. Warm-start (CMP-009) and NN inference (CMP-007) have fixed latency costs that must be accounted for in the per-phase allocation.

6. **Board-size parameterization**: Fork detection (CMP-004), asymmetric evaluation (CMP-010), and solved-game tablebooks (CMP-001) are board-size dependent. The O(7) fork formula, the 100K/100/-120 scoring values, and the tablebook itself must be re-parameterized for non-7x6 boards.

7. **GPU context lifecycle**: CMP-007 (TensorRT) requires GPU context initialization and model loading. For phase routing (CMP-008), the GPU context should be maintained across phases rather than destroyed/recreated, to amortize the initialization overhead.