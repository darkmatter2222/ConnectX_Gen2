# GPU Research for ConnectX

> **Generated**: 2026-07-30 (Iteration 1)
> **Purpose**: Document RTX 5090 opportunities for ConnectX AI
> **Hardware**: NVIDIA GeForce RTX 5090 (Blackwell architecture)

---

## RTX 5090 Specifications

### Compute
| Specification | Value |
|--------------|-------|
| GPU | GB202-300 Blackwell die |
| Die Size | 750 mm² |
| Transistors | 92.2 billion |
| CUDA Cores | 21,760 |
| RT Cores | 170 (5th generation) |
| Tensor Cores | 680 (5th generation) |
| Boost Clock | 2.41 GHz |
| TDP | 575W |

### Memory
| Specification | Value |
|--------------|-------|
| Memory Type | GDDR7 |
| Memory Size | 32 GB |
| Memory Bus | 512-bit |
| Memory Speed | 28 Gbps |
| Memory Bandwidth | 1,792 GB/s |
| Interface | PCIe 5.0 x16 |

### Performance
| Metric | Value |
|--------|-------|
| FP8 Tensor (peak) | 419.2 TFLOPS |
| FP8 Tensor (with sparsity) | 838.4 TFLOPS |
| FP16/FP32 | 104.8 TFLOPS |
| FP64 | ~52.4 TFLOPS (estimated) |
| RT Performance | 317.5 RT/s |
| Pixel Fillrate | 423.6 Gpx/s |
| Texture Fillrate | 1,637 Gtex/s |

### Launch
- **Date**: January 30, 2025
- **MSRP**: $1,999
- **Availability**: Severe initial shortages, prices above MSRP

---

## GPU Opportunities for ConnectX

### 1. Neural Network Training (PRIMARY USE)

#### What
Train CNN/policy/value networks for ConnectX on RTX 5090

#### Speedup vs CPU
- **Training speed**: 50-200× faster than CPU
- **Dataset size**: Can train on 1M+ examples in hours instead of days
- **Experimentation**: 10× more hyperparameter experiments possible

#### Training Scenarios
1. **Supervised learning from solved positions**:
   - Dataset: 200K-1M+ (state, action) pairs from solved 7x6
   - CNN architecture: 5-15 layers, varying channel sizes
   - Training time: 1-4 hours on RTX 5090 (vs 50-200 hours on CPU)

2. **Self-play RL (AlphaZero-style)**:
   - Self-play games: 10,000-100,000 games
   - Neural net evaluation: guides MCTS
   - Training time: 12-48 hours on RTX 5090 (vs 500-2000 hours on CPU)

3. **Transfer learning**:
   - Train on 7x6, transfer to 15x13
   - Fine-tuning: 2-6 hours on RTX 5090
   - Full retraining: 8-24 hours on RTX 5090

#### Framework Recommendations
- **PyTorch**: Best for research, flexible, good GPU support
- **TensorRT**: Best for deployment, optimized inference
- **ONNX Runtime**: Alternative for deployment, cross-platform

---

### 2. Neural Network Inference (SECONDARY USE)

#### What
Deploy trained neural network for real-time ConnectX play

#### Inference Speed
- **Policy net (100K params)**: ~0.1ms on RTX 5090
- **Policy net (1M params)**: ~0.5ms on RTX 5090
- **Policy net (10M params)**: ~2ms on RTX 5090
- **Policy net (100M params)**: ~10ms on RTX 5090

#### Comparison
| Method | Speed | Quality |
|--------|-------|---------|
| Pure heuristic evaluation | ~1ms CPU | Good for small boards |
| Neural net (100K) on GPU | ~0.1ms GPU | Near-expert level |
| Neural net (1M) on GPU | ~0.5ms GPU | Expert level |
| Alpha-beta depth 8 in Python | ~200ms CPU | Strong play |
| Alpha-beta depth 12 in Python | ~2s CPU | Expert play |

#### Key Insight
> Neural net inference on RTX 5090 is 200-2000× faster than alpha-beta search in Python.
> This means we can evaluate 500-5000 positions per second with the neural net alone.

---

### 3. GPU-Accelerated Search (EXPERIMENTAL)

#### What
Use GPU to accelerate the search process itself

#### Opportunities
1. **Parallel leaf evaluation**: Evaluate multiple leaf positions simultaneously
2. **Batched position evaluation**: Evaluate positions in GPU batches
3. **CUDA-based alpha-beta**: Parallelize the search algorithm itself
4. **GPU MCTS**: Run thousands of simulations in parallel on GPU

#### Challenges
1. Alpha-beta is inherently sequential (depends on previous results)
2. Memory transfer overhead (CPU ↔ GPU)
3. Branch divergence in GPU threads
4. Small board states don't fully utilize GPU parallelism

#### Potential Speedup
- **Parallel leaf evaluation**: 5-10× (depends on batch size)
- **CUDA alpha-beta**: 2-5× (limited by sequential nature)
- **GPU MCTS**: 20-100× (many independent simulations)

---

### 4. Hybrid CPU+GPU Architecture (RECOMMENDED)

#### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    RTX 5090 + CPU                           │
│                                                             │
│  CPU (Python/C++)                 GPU (RTX 5090)            │
│  ┌─────────────┐                  ┌─────────────────┐      │
│  │ Alpha-Beta  │    ←───────────  │ Neural Net      │      │
│  │ Search      │   Move queries   │ Policy/Value     │      │
│  │             │                  │ Inference        │      │
│  │ Time mgmt   │                  │                  │      │
│  └─────────────┘                  └─────────────────┘      │
│                                                             │
│  Time budget: 2 seconds/move                                │
│  - 1500ms: Alpha-beta search with NN leaf evaluation       │
│  - 500ms: GPU inference for position evaluation            │
│  - 100ms: Overhead and safety margin                      │
└─────────────────────────────────────────────────────────────┘
```

#### Workflow
1. **CPU**: Alpha-beta search at each node
2. **At leaf nodes**: Query GPU for neural net evaluation
3. **GPU**: Returns value estimate in ~0.1ms
4. **CPU**: Back-propagates value through tree
5. **Repeat** until time limit

#### Benefits
- Combines search precision with GPU speed
- 2000× faster evaluation at leaves
- Can search deeper with same time budget
- Works on all board sizes

---

## Practical Recommendations

### Phase 1: Quick Win (No GPU)
- Pure Python alpha-beta with optimizations
- Numba JIT for 5-10× speedup
- Works on any hardware
- Time to implement: 1-2 days

### Phase 2: Small NN (GPU Training)
- Train small CNN (100K params) on RTX 5090
- Use trained net for leaf evaluation in alpha-beta
- Hybrid search approach
- Time to implement: 1-2 weeks
- Expected improvement: 30-50% stronger play

### Phase 3: Larger NN (GPU Training)
- Train larger CNN (1M+ params) on RTX 5090
- MCTS + neural net (AlphaZero-style)
- Distributed training with multiple GPUs
- Time to implement: 2-4 weeks
- Expected improvement: Expert-level play

### Phase 4: Full Hybrid
- C++ search core (pybind11) + GPU NN inference
- TensorRT for fastest inference
- Complete opening book from solved positions
- Endgame database for terminal positions
- Time to implement: 1-2 months
- Expected improvement: World-class play

---

## Benchmarking Plan

### What to Benchmark
1. **NN training time**: RTX 5090 vs CPU
2. **NN inference speed**: TensorRT vs PyTorch vs ONNX
3. **Search speed**: Pure Python vs Numba vs Cython vs C++
4. **Hybrid performance**: NN evaluation vs heuristic evaluation
5. **End-to-end**: Time per move with different approaches

### How to Benchmark
1. **Training**: Track epochs, losses, and wall-clock time
2. **Inference**: Measure GPU latency for different model sizes
3. **Search**: Count nodes per second at different depths
4. **Play strength**: Win rate against known opponents

### Tools
- **PyTorch profiling**: `torch.profiler` for GPU training
- **TensorRT profiling**: `nvinfer` profiling API
- **C++ timing**: `std::chrono` in search core
- **Python timing**: `time.perf_counter` in search loop

---

## Open Questions

1. What is the optimal batch size for GPU inference?
2. Can we use multi-GPU inference for even faster evaluation?
3. What's the maximum practical neural net size for 2-second response?
4. Can CUDA-based alpha-beta search beat CPU-based MCTS?
5. Is there a practical way to use GPU for parallel move generation?
6. What's the impact of PCIe 5.0 bandwidth on CPU-GPU data transfer?
7. Can we use sparse tensor cores (838 TFLOPS) for faster inference?
8. What's the optimal model quantization (FP16, INT8, INT4)?

---

## References

- NVIDIA. "GeForce RTX 5090 Specifications" — Official product page
- NVIDIA TensorRT Documentation — Inference optimization guide
- PyTorch GPU Tutorial — Training on RTX 5090
- ONNX Runtime GPU — Cross-platform inference optimization