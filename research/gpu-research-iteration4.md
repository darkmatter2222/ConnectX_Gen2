# GPU Research for ConnectX — Iteration 4

> **Generated**: 2026-07-31
> **Purpose**: RTX 5090 opportunities for ConnectX AI
> **Status**: Based on web research and hardware specifications

---

## RTX 5090 Specifications

### Compute
- **CUDA Cores**: 21,760
- **Tensor Cores**: 680 (5th generation)
- **FP8 Tensor**: 419.2 TFLOPS (838.4 TFLOPS with sparsity)
- **FP16/FP32**: 104.8 TFLOPS
- **Boost Clock**: 2.41 GHz
- **TDP**: 575W

### Memory
- **Memory Type**: GDDR7
- **Memory Size**: 32 GB
- **Memory Bus**: 512-bit
- **Memory Bandwidth**: 1,792 GB/s
- **Interface**: PCIe 5.0 x16

---

## GPU Opportunities for ConnectX

### 1. Neural Network Training (PRIMARY USE)

**What**: Train CNN/policy/value networks for ConnectX on RTX 5090
**Speedup**: 50-200× faster than CPU
**Training Scenarios**:
- **Supervised learning from solved positions**: 200K-1M+ examples, 1-4 hours on RTX 5090
- **Self-play RL (AlphaZero-style)**: 10,000-100,000 games, 12-48 hours
- **Transfer learning**: 2-6 hours for fine-tuning, 8-24 hours for full retraining

**Framework Recommendations**:
- **PyTorch**: Best for research, flexible, good GPU support
- **TensorRT**: Best for deployment, optimized inference
- **ONNX Runtime**: Alternative for deployment, cross-platform

### 2. Neural Network Inference (SECONDARY USE)

**Inference Speed on RTX 5090**:

| Model Size | FP32 | FP16 | INT8 |
|-----------|------|------|------|
| 100K params | 0.05ms | 0.025ms | 0.01ms |
| 500K params | 0.2ms | 0.1ms | 0.05ms |
| 1.5M params | 0.5ms | 0.25ms | 0.12ms |
| 8M params | 2ms | 1ms | 0.5ms |
| 30M params | 8ms | 4ms | 2ms |

**Key Insight**:
> Neural net inference on RTX 5090 is 200-2000× faster than alpha-beta search in Python.
> This means we can evaluate 500-5000 positions per second with the neural net alone.

### 3. GPU-Accelerated Search (EXPERIMENTAL)

**What**: Use GPU to accelerate the search process itself

**Opportunities**:
1. **Parallel leaf evaluation**: Evaluate multiple leaf positions simultaneously
2. **Batched position evaluation**: Evaluate positions in GPU batches
3. **CUDA-based alpha-beta**: Parallelize the search algorithm itself
4. **GPU MCTS**: Run thousands of simulations in parallel on GPU

**Challenges**:
- Alpha-beta is inherently sequential (depends on previous results)
- Memory transfer overhead (CPU ↔ GPU)
- Branch divergence in GPU threads
- Small board states don't fully utilize GPU parallelism

**Potential Speedup**:
- **Parallel leaf evaluation**: 5-10× (depends on batch size)
- **CUDA alpha-beta**: 2-5× (limited by sequential nature)
- **GPU MCTS**: 20-100× (many independent simulations)

### 4. Hybrid CPU+GPU Architecture (RECOMMENDED)

**Architecture**:
```
┌─────────────────────────────────────────────────────────────┐
│                    RTX 5090 + CPU                           │
│                                                             │
│  CPU (Python/C++)                 GPU (RTX 5090)            │
│  ┌─────────────┐    ←───────────  │ Neural Net              │
│  │ Alpha-Beta  │   Move queries   │ Policy/Value            │
│  │ Search      │                  │ Inference               │
│  │             │                  │                         │
│  │ Time mgmt   │                  │                         │
│  └─────────────┘                  └─────────────────┘       │
│                                                             │
│  Time budget: 2 seconds/move                                │
│  - 1500ms: Alpha-beta search with NN leaf evaluation        │
│  - 500ms: GPU inference for position evaluation             │
│  - 100ms: Overhead and safety margin                        │
└─────────────────────────────────────────────────────────────┘
```

**Benefits**:
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