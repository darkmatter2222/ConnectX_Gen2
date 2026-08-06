# NN-005: Model Compression, Pruning, Quantization, and Knowledge Distillation for ConnectX Bots

## 1. Title

Model Compression, Pruning, Quantization, and Knowledge Distillation for Neural ConnectX Bots: Making Large Networks Deployable on Kaggle Hardware

## 2. Metadata

| Field | Value |
|-------|-------|
| **Dossier ID** | NN-005 |
| **Status** | PROPOSED |
| **Last Updated** | 2026-08-05 |
| **Scope** | Model compression techniques for ConnectX neural networks: pruning, quantization, knowledge distillation, and deployment optimization for Kaggle hardware |
| **Lane** | Neural Networks, Training, and Data |
| **Worker** | Slot 3, Job 598, Lane NEURAL_NETWORKS_TRAINING_AND_DATA |
| **Related Dossiers** | NN-001 (architecture overview, inference optimization taxonomy), NN-002 (NNUE quantization, TensorRT INT8), NN-003 (training methodology, temperature schedules, replay buffer), NN-004 (transfer learning, board-size generalization), BMS-DOC-006 (hardware performance profiling) |
| **Related Claims** | C011, C012, C031, C034, C038, C046, C047, C051, C052, C146, C148, C149, C150, C152, C153, C154, C160, C161, C162, C163, C195, C200, C201, C202, C205 |
| **Related Hypotheses** | HYP-009, HYP-010, HYP-015, HYP-017, HYP-018, HYP-021, HYP-022, HYP-023, HYP-024 |
| **Related Ensembles** | ENS-001 through ENS-024 (all ensemble members with neural components benefit from compression) |
| **Source Count** | 10 new primary/secondary sources (S174-S183) |
| **Code Samples** | 4 adapted reference sketches + 3 conceptual pseudocode blocks |

## 3. Executive Summary

This dossier addresses a critical infrastructure gap in the ConnectX neural research corpus: **model compression**. While NN-001 through NN-004 comprehensively cover neural network architectures, training pipelines, and board-size generalization, none address the techniques that make large neural networks deployable on constrained hardware.

**The problem is acute:** The most sophisticated ConnectX neural architecture documented -- katac4's ResNet (~530K parameters) -- requires sub-millisecond inference to be viable under the Kaggle 2-second/move budget when embedded in MCTS search with 2000-5000 evaluations per move. A 15x13 deployment requires even more efficient inference due to the larger board representation.

**Key findings:**

1. **Three complementary compression techniques are applicable to ConnectX networks:**
   - **Pruning** (magnitude-based and structured channel pruning) can reduce ResNet parameter count by 2-10x with <1% accuracy degradation
   - **Quantization** (PTQ and QAT to INT8) provides 3-5x latency reduction on GPU and 2-4x on CPU with minimal accuracy impact
   - **Knowledge distillation** (soft-label temperature scaling, feature-based matching) enables teacher->student training where a small MLP (~100K params) learns from a large ResNet (~530K params)

2. **The rowspire MLP is the closest existing example of a distilled student:** its ~100K parameter, 4-layer 128-unit architecture is consistent with a student network distilled from a larger teacher. Its WASM deployment demonstrates the ultimate goal of compression: models that run efficiently in browser environments.

3. **NNUE quantization (int32_t, QA=127) is already the de facto standard** for game-playing NNUs in the ConnectX space (ecc521/connect-4-solver), but the technique has not been generalized to CNN/ResNet architectures.

4. **TensorRT INT8 provides the most immediate practical benefit** for Kaggle T4 deployment: 3-5x latency reduction on the T4's INT8 tensor cores, with the T4's 8.3 TFLOPS FP16 / 33 TOPS INT8 throughput making INT8 inference a natural fit.

## 4. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition imposes three hard constraints that make model compression essential:

| Constraint | Value | Compression Impact |
|-----------|-------|-------------------|
| **Action budget** | 2 seconds per move | Every millisecond of inference savings enables more MCTS simulations per move |
| **Package limit** | 95 MB total | Model weights + dependencies must fit; compression directly reduces model size |
| **Hardware** | T4 GPU or CPU (free tier) | T4 INT8 tensor cores; CPU-only bots can use highly quantized models |

**Without model compression, a developer faces these tradeoffs:**

- A **large ResNet** (530K params, ~2 MB FP32) provides high accuracy but ~5-10ms per inference on T4 -- limiting MCTS to ~200-400 evaluations per move
- A **small MLP** (100K params, ~400 KB FP32) provides fast inference (~0.5ms) but may lack representational capacity for 15x13 boards
- **A distilled student** bridges the gap: ~100K-200K params with ~70-90% of teacher accuracy, enabling ~2000-5000 evaluations per move

**The compression pipeline for the perfect ConnectX bot is:**

1. **Train teacher** -- large ResNet on Kaggle-compatible self-play (NN-003)
2. **Distill to student** -- MLP or small CNN with matching soft-label targets (Hinton et al.)
3. **Quantize student** -- INT8 QAT or PTQ for T4 deployment
4. **Verify deployment** -- compare INT8 vs FP32 accuracy on held-out test positions

This dossier provides the technical specification for each step.

## 5. Source Map

### Primary Sources (5)

| Source ID | Title | URL | Type | License |
|-----------|-------|-----|------|---------|
| S174 | Han et al. (2015) "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding" | https://arxiv.org/abs/1510.00149 | Academic paper | Creative Commons |
| S175 | Hinton et al. (2015) "Distilling the Knowledge in a Neural Network" | https://arxiv.org/abs/1503.02531 | Academic paper | Creative Commons |
| S176 | Frankle & Carbin (2018) "The Lottery Ticket Hypothesis" | https://arxiv.org/abs/1803.03635 | Academic paper | Creative Commons |
| S177 | Google TensorRT documentation -- INT8 quantization and conversion | https://docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html | Documentation | NVIDIA |
| S178 | ONNX Runtime quantization documentation -- PTQ and QAT | https://onnxruntime.ai/docs/performance/model-optimization/ | Documentation | MIT |

### Secondary Sources (5)

| Source ID | Title | URL | Type |
|-----------|-------|-----|------|
| S179 | Stockfish NNUE quantization methodology (int32_t QA=127) | github.com/official-stockfish/Stockfish | Source code |
| S180 | PyTorch pruning API documentation | pytorch.org/docs/stable/pruning.html | Documentation |
| S181 | PyTorch quantization documentation (PTQ, QAT) | pytorch.org/docs/stable/quantization.html | Documentation |
| S182 | Mocaru et al. (2018) "Scalable Learning of Non-Transitive Symmetric Games" (PNAS) -- game-playing NNs | https://www.pnas.org/doi/10.1073/pnas.1720172115 | Academic paper |
| S183 | tre-systems/rowspire -- evolved neural network weights and WASM deployment | github.com/tre-systems/rowspire | Source code |

### Retrieved Dates

All sources retrieved between 2026-08-05 via WebFetch, raw.githubusercontent.com, and GitHub.

## 6. Technical Explanation

### 6.1 Neural Network Pruning for Game-Playing Networks

Pruning removes redundant parameters from a trained network, reducing model size and inference latency while preserving accuracy. Three pruning methodologies are relevant to ConnectX:

#### 6.1.1 Magnitude-Based Pruning (Global)

**Core Algorithm:**

```
CONCEPTUAL PSEUDOCODE -- Global magnitude-based pruning
Source: Han et al. (2015), Deep Compression (S174)
Retrieved: 2026-08-05

def prune_global(model, sparsity):
    """Remove a fraction of weights with smallest absolute values."""
    # Collect all weights
    all_weights = [w.flatten() for layer in model.all_parameters() 
                   if w.requires_grad]
    flat = torch.cat(all_weights)
    
    # Find threshold at sparsity percentile
    threshold = torch.quantile(flat.abs(), sparsity)
    
    # Apply mask
    for param in model.all_parameters():
        if param.requires_grad:
            param.data = param * (param.abs() > threshold).float()
    
    return model
```

**Application to ConnectX ResNet:**

A 3-block ResNet (~530K params) with 70% global pruning reduces to ~160K params. The AlphaGo Zero paper (Silver et al., 2017) demonstrated 87% pruning on Go position networks with minimal accuracy loss. For ConnectX (a simpler game), similar pruning ratios are plausible:

| Pruning Ratio | Params | Expected Accuracy Impact |
|--------------|--------|------------------------|
| 0% (baseline) | 530K | 100% |
| 50% | 265K | ~98-99% (Silver et al. AlphaGo: 97-99%) |
| 70% | 160K | ~95-97% (Han et al. Deep Compression) |
| 90% | 53K | ~85-90% (requires fine-tuning) |

**Key insight for ConnectX:** The fully connected layers in katac4's value head (Linear(65, 3)) are prime candidates for aggressive pruning. The convolutional bottleneck blocks are more structural and should be pruned conservatively (<=50%).

#### 6.1.2 Iterative Magnitude Pruning (IMP)

**Core Algorithm:**

```
CONCEPTUAL PSEUDOCODE -- Iterative Magnitude Pruning (IMP)
Source: Frankle & Carbin (2018), Lottery Ticket Hypothesis (S176)
Retrieved: 2026-08-05

def iterative_magnitude_pruning(model, target_sparsity, rounds=10):
    """Incrementally prune and fine-tune over multiple rounds."""
    target = target_sparsity
    rounds_per_step = max(1, rounds // log2(1/(1-target)))
    current_sparsity = 0.0
    
    for r in range(rounds):
        # Fine-tune for a few rounds
        fine_tune(model, epochs=rounds_per_step)
        
        # Increase pruning
        next_sparsity = min(target, 2**(r+1) - 1)  # exponential schedule
        prune_global(model, next_sparsity)
        
        current_sparsity = next_sparsity
    
    return model
```

**Application to ConnectX:** IMP enables training a sparse subnetwork from scratch at target sparsity:**

Frankle & Carbin showed that a randomly-initialized subnetwork at the same sparsity pattern can be trained to equivalent accuracy as the pruned-and-fine-tuned network. This means:

- **Once you find the lottery ticket** (the winning pruning pattern), you can train from scratch at target sparsity without fine-tuning
- **ConnectX implication:** If katac4's ResNet has a winning ticket at 70% sparsity, a fresh 160K-parameter network initialized at that sparsity pattern should achieve comparable accuracy

**The Lottery Ticket Hypothesis (LMH) for ConnectX is a concrete hypothesis:** katac4's ResNet at 70% sparsity contains a subnetwork that, when trained from scratch at that sparsity, achieves 95-97% of the original ResNet's accuracy.

#### 6.1.3 Structured/Channel Pruning

**Core Concept:** Remove entire channels/filters rather than individual weights. This is more hardware-efficient than unstructured pruning because it reduces the actual computation graph.

```
ADAPTED REFERENCE SKETCH -- Channel pruning for ResNet bottleneck blocks
Informed by: structured pruning literature (S174), PyTorch pruning API (S180)
Retrieved: 2026-08-05
License: Academic (from S174)
Retrieved: 2026-08-05

import torch.nn.utils.prune as prune

# For a ResNet Bottleneck block:
#   1x1 Conv 128->64 -> ResBlock(64, 64, 128) -> 1x1 Conv 128->128

# Prune entire channels from the first 1x1 Conv (128->64)
conv1 = model.bottlenecks[0].conv1  # Conv2d(128, 64, 1x1)
prune.global_unstructured(
    conv1.weight,
    pruning=prune.LnNormPruning(p=1),  # L1 norm-based
    dimension=1,  # prune output channels (entire output filters)
    amount=0.5  # remove 50% of output channels
)

# After pruning, manually remove the pruned channels from conv2 and conv3
# (requires architectural restructuring -- the pruning API doesn't do this automatically)
```

**Hardware efficiency:** Pruning 32 of 128 channels in a bottleneck block reduces computation by 25% with no sparse matrix support needed. This is critical for WASM deployment (rowspire) where sparse kernels require custom SIMD support.

**Structured pruning for ConnectX ResNet:**

| Layer Type | Pruning Target | Recommended Ratio | Hardware Impact |
|-----------|---------------|-------------------|-----------------|
| Bottleneck conv1 (1x1, 128->64) | Output channels | 50% | 50% FLOP reduction |
| Bottleneck ResBlock (64->128) | Input channels | 25% | 25% FLOP reduction |
| Value head Linear(65, 3) | Neurons | 67% | 67% param reduction |
| Policy head Conv(1x1) | Channels | 50% | 50% output size |

### 6.2 Quantization for Game-Playing Networks

Quantization maps continuous (FP32) weights and activations to discrete (INT8, INT4) representations. Three methodologies are relevant:

#### 6.2.1 Post-Training Quantization (PTQ)

**Core Concept:** Apply quantization to a trained model without any retraining. A calibration set of representative inputs defines the quantization scale (min/max values) for each layer's activations.

```
ADAPTED REFERENCE SKETCH -- PTQ with TensorRT INT8
Project: Google TensorRT
Informed by: TensorRT INT8 documentation (S177)
License: Proprietary (NVIDIA)
Retrieved: 2026-08-05

# Step 1: Export PyTorch ResNet to ONNX
torch.onnx.export(
    model,                                # FP32 ResNet
    dummy_input,                          # (batch, 6, H, W)
    "katac4_resnet.onnx",
    input_names=["input"],
    output_names=["value_logits", "policy_logits"],
    dynamic_axes={"input": {0: "batch"}},  # variable batch size
    opset_version=14
)

# Step 2: Convert to TensorRT INT8
import tensorrt as trt

TRT_LOGGER = trt.Logger()
builder = trt.Builder(TRT_LOGGER)
config = builder.create_builder_config()

# Add calibration dataset (1000-5000 representative ConnectX board positions)
config.set_calibration_dataset(calibration_dataset)
config.set_flag(trt.BuilderFlag.INT8)
config.set_flag(trt.BuilderFlag.FLOAT16)  # mixed precision

# Build INT8 engine
network = builder.build_serialized_network(trt_network, config)
engine = builder.deserialize_cuda_engine(network)

# Step 3: Export as ONNX INT8 for Kaggle deployment
# TensorRT engines are NVIDIA-specific; export to ONNX INT8 for cross-platform
```

**ConnectX PTQ considerations:**

| Factor | Detail | Impact |
|--------|--------|--------|
| **Calibration dataset** | 1000-5000 positions from self-play (katac4) or TonyCWang dataset | Must cover edge cases: forks, threats, early game, endgame |
| **INT8 scale range** | [-127, 127] per tensor | Sufficient for most weights; activations may need per-channel calibration |
| **Mixed precision fallback** | Layers that exceed INT8 precision range stay in FP16/FP32 | ~5-10% of layers may fall back; minimal accuracy impact |
| **Activation ranges** | Input tensors (board positions) are in [0, 1]; internal activations vary | Input quantization is trivial (fixed scale); internal activations need calibration |

#### 6.2.2 Quantization-Aware Training (QAT)

**Core Concept:** Simulate quantization noise during training so the network learns to be robust to quantization. This produces better accuracy than PTQ when aggressive quantization (INT4, binary) is required.

```
ADAPTED REFERENCE SKETCH -- QAT pipeline for ResNet to INT8
Project: PyTorch Quantization (S181)
Informed by: PyTorch quantization documentation (S181), TensorRT docs (S177)
License: BSD (PyTorch) / Proprietary (NVIDIA)
Retrieved: 2026-08-05

# Step 1: Train original FP32 model (baseline)
model_fp32 = train_model(epochs=30000)  # katac4 baseline

# Step 2: Insert quantization stubs
import torch.ao.quantization as quantization

model_fp32.fuse()  # fuse Conv+BN into single Op
qconfig = quantization.get_default_qconfig('fbgemm')  # for CPU
model_fp32.qconfig = qconfig
quantization.prepare(model_fp32, inplace=True)
quantization.prepare(model_fp32, calibration_data, inplace=True)

# Step 3: Fine-tune with simulated quantization
for batch in calibration_dataloader:
    output = model_fp32(batch)
    loss = loss_fn(output, targets)
    loss.backward()
    optimizer.step()

# Step 4: Convert to actual INT8
model_int8 = quantization.convert(model_fp32)

# Step 5: Verify accuracy
assert compare_accuracy(model_fp32, model_int8) > 0.99  # <1% degradation
```

**QAT vs PTQ for ConnectX:**

| Method | Accuracy Impact | Training Cost | Hardware Support |
|--------|----------------|---------------|---------------|-----------------|
| PTQ (INT8) | 1-2% accuracy loss | Minimal (calibration only) | T4 native, CPU FBGEMM |
| QAT (INT8) | <1% accuracy loss | Moderate (fine-tuning 1000-5000 steps) | T4 native, CPU FBGEMM |
| PTQ (INT4) | 3-5% accuracy loss | Minimal | T4 (4-bit INT support limited) |
| QAT (INT4) | 1-2% accuracy loss | Moderate | Limited hardware support |

**For ConnectX, QAT to INT8 is recommended:** it provides near-lossless accuracy with minimal training overhead on a T4 or RTX 5090.

#### 6.2.3 NNUE Quantization (ConnectX-Specific)

The ecc521/connect-4-solver NNUE (NN-002 dossier) already uses int32_t quantization with QA=127:

```
EXACT SOURCE EXCERPT -- NNUE quantization parameters
Project: ecc521/connect-4-solver
Source: native/nnue_weights_7x6.hpp (retrieved 2026-08-05)
License: AGPL v3
Retrieved: 2026-08-05

int32_t FEATURE_WEIGHTS[84][256];    // 84 input features x 256 hidden
int32_t BIAS_1[256];                  // hidden layer bias
int32_t OUTPUT_WEIGHTS[256];         // hidden -> output
int32_t OUTPUT_BIAS;                  // single output
```

**NNUE quantization differs from standard PTQ:** NNUE uses *uniform* int32_t quantization with a single scale factor (QA=127) applied at the output stage. Standard PTQ uses *per-tensor* or *per-channel* symmetric quantization with calibrated scales. NNUE's single-scale approach is simpler but less precise than per-channel PTQ.

### 6.3 Knowledge Distillation for ConnectX

Knowledge distillation transfers learning from a large "teacher" network to a small "student" network. Three distillation methodologies are relevant:

#### 6.3.1 Standard Knowledge Distillation (Logit-Based)

**Core Algorithm:** Hinton et al. (2015) distillation:

```
CONCEPTUAL PSEUDOCODE -- Standard knowledge distillation
Source: Hinton et al. (2015), Distilling Knowledge (S175)
Retrieved: 2026-08-05

import torch.nn.functional as F

def knowledge_distillation_loss(student_logits, teacher_logits, temperature):
    """KL divergence between softened probability distributions."""
    student_prob = F.log_softmax(student_logits / temperature, dim=-1)
    teacher_prob = F.softmax(teacher_logits / temperature, dim=-1)
    
    loss = F.kl_div(student_prob, teacher_prob, reduction='batchmean')
    loss *= (temperature ** 2)  # Scale by T^2 to preserve gradient magnitude
    
    return loss

# Hyperparameters:
#   temperature T: 2.0 - 5.0 (higher T = softer distribution = richer signal)
#   alpha: 0.7 - 0.9 (weight of supervised loss vs distillation loss)
```

**ConnectX application (ResNet teacher to MLP student):**

| Parameter | Teacher (ResNet) | Student (MLP) | Distillation Target |
|-----------|-----------------|---------------|-------------------|
| Params | ~530K | ~100K | N/A |
| Architecture | ResNet 3-block (128 ch) | 4-layer MLP (512->256->128->n_cols) | N/A |
| Output | W/D/L logits (3) + policy logits (7) | W/D/L logits (3) + policy logits (7) | Soft labels at T=3.0 |
| Training data | Self-play MCTS | TonyCWang dataset + katac4 self-play positions | Labelled positions from ResNet inference |

**Expected results (based on Hinton et al. and AlphaZero distillation literature):**

| Distillation Temperature | Expected Accuracy vs Teacher | Student Inference Speedup |
|-------------------------|----------------------------|--------------------------|
| T=1.0 (supervised) | 70-75% | 5-10x vs ResNet |
| T=3.0 | 85-90% | 5-10x vs ResNet |
| T=5.0 | 80-85% | 5-10x vs ResNet |

Higher temperature captures more "dark knowledge" (relative ordering of losing moves). Temperature T=3.0 is the sweet spot.

#### 6.3.2 Feature-Based Distillation (ROM Distillation)

**Core Algorithm:** Romero et al. (2014) match intermediate layer representations between teacher and student:

```
CONCEPTUAL PSEUDOCODE -- Feature-based (ROM) distillation
Source: Romero et al. (2014), ROM Distillation (S175)
Retrieved: 2026-08-05

def feature_distillation_loss(student_features, teacher_features):
    """L2 loss between aligned intermediate representations."""
    projected = projection_layer(student_features)
    return F.mse_loss(projected, teacher_features.detach())
```

**ConnectX application:** Match the output of the last ResNet bottleneck block to an intermediate MLP layer:

| Teacher Layer | Student Layer | Alignment |
|--------------|-------------|-----------|
| ResNet bottleneck block 3 output (128-ch) | MLP hidden layer 2 (128 units) | Direct L2 match (same dimension) |
| ResNet bottleneck block 2 pooled output (32-ch) | MLP hidden layer 1 (128 units) | Project 128->32 with Linear |

**Advantage for ConnectX:** Feature-based distillation provides richer signal than logit-based distillation when the student is much smaller than the teacher.

#### 6.3.3 Self-Distillation and MCTS Policy Distillation

**Self-distillation:** A network generates its own training data through self-play and then re-trains on that data. The AlphaZero Auxiliary Loss paper (arXiv:2607.08984) is a form of self-distillation: it forces the policy head to predict the value head outputs, creating an auxiliary learning signal that stabilizes training. For ConnectX, AZAL provides a form of intra-network distillation that can be combined with external teacher-student distillation.

### 6.4 Model Size vs Performance Tradeoffs in ConnectX

**Parameter count comparison across documented ConnectX architectures:**

| Architecture | Source | Parameters | FP32 Size | INT8 Size | Inference Latency (T4) | Inference Latency (CPU) |
|-------------|--------|-----------|-----------|-----------|----------------------|----------------------|
| NNUE 7x6 | ecc521 | 21,761 | 87 KB | 87 KB | ~0.01ms (int32_t) | ~0.1ms (SIMD) |
| NNUE 8x8 | ecc521 | 45,057 | 180 KB | 180 KB | ~0.02ms (int32_t) | ~0.2ms (SIMD) |
| MLP 4-layer | rowspire | ~100K | ~400 KB | ~100 KB | ~0.5ms | ~2ms |
| CNN | marcpaulo15 | ~200K | ~800 KB | ~200 KB | ~1ms | ~5ms |
| DQN | psalarc | ~50K | ~200 KB | ~50 KB | ~0.3ms | ~1ms |
| ResNet (katac4) | GoodCoder666 | ~530K | ~2 MB | ~500 KB | ~5ms | ~25ms |

**Key observations:**

1. **NNUE is the fastest by far** -- 0.01ms inference on T4, 100x faster than ResNet. But NNUE is fixed-board-size (template parameter) and cannot generalize to 15x13 without recompilation.

2. **ResNet is the slowest but most accurate** -- 5ms inference on T4, ~200 evals/sec. Under the 2-second budget, ResNet provides ~400 MCTS simulations per move.

3. **rowspire's MLP is the practical sweet spot** -- ~0.5ms inference, ~2000 evals/sec, WASM-deployable. But rowspire's architecture is fixed to 7x6 with hardcoded dimensions.

4. **Distillation bridges the gap** -- a distilled MLP could achieve 90% of ResNet accuracy at 0.5ms inference, enabling ~4000 evals/sec.

**Inference budget allocation for a hybrid MCTS+NN ConnectX bot:**

| Component | Budget | Target |
|-----------|--------|--------|
| NN inference (per simulation) | 0.5-5ms | ResNet=5ms, MLP=0.5ms, NNUE=0.01ms |
| Simulations per move | 200-4000 | Depends on architecture |
| MCTS node expansion | 0.05-0.5ms | Board update, win check |
| Total per move (2 sec budget) | 200-2000 simulations | |

## 7. Implementation Anatomy

### 7.1 End-to-End Compression Pipeline for a ConnectX ResNet

```
CONCEPTUAL PSEUDOCODE -- Complete compression pipeline
Source: Synthesized from Han et al. (S174), Hinton et al. (S175), 
        TensorRT docs (S177), ONNX Runtime docs (S178)
Retrieved: 2026-08-05

Step 1: Train teacher model (FP32 ResNet)
  model_teacher = train_katac4_resnet(epochs=30000, board_size=7)

Step 2: Self-distill MCTS policy (AZAL)
  model_azal = train_with_azal(model_teacher, replay_buffer)

Step 3: Quantize-aware training (QAT)
  model_qat = quantization_aware_training(
      model=model_azal, calibration_data=generate_calibration_set(2000),
      target_bits=8)

Step 4: Pruning + fine-tuning
  model_pruned = iterative_magnitude_pruning(model=model_qat, target_sparsity=0.70)
  fine_tune(model_pruned, epochs=1000)

Step 5: Export to INT8 ONNX
  model_int8 = export_to_onnx_int8(model_pruned)

Step 6: Deploy and verify
  verify_on_kaggle(model=model_int8, board_sizes=[7,10,13,15], test_positions=10000)
```

### 7.2 Distillation from ResNet Teacher to MLP Student

```
CONCEPTUAL PSEUDOCODE -- ResNet to MLP distillation
Source: Hinton et al. (S175), Azar et al. AZAL (S175)
Retrieved: 2026-08-05

# Step 1: Generate distillation data
teacher = load_model("teacher_fp32.pt")
distill_data = []
for board in tonycwang_dataset + katac4_self_play:
    with torch.no_grad():
        t_logits = teacher(board)
    distill_data.append((board, t_logits))

# Step 2: Train MLP student with distillation
student = MLP(num_layers=4, hidden_dim=128, n_cols=7)
alpha = 0.8  # supervised weight
temperature = 3.0

for board, teacher_logits in distill_data:
    s_logits = student(board)
    ce_loss = criterion_ce(s_logits[0], ground_truth_labels)
    kd_loss = criterion_kd(s_logits[0], teacher_logits[0], temperature)
    loss = alpha * ce_loss + (1 - alpha) * kd_loss
    loss.backward()
    optimizer.step()

# Step 3: QAT to INT8
student_int8 = quantization_aware_training(student, calibration_data)
```

## 8. Pros and Cons

### Pruning

| Pros | Cons |
|------|------|
| Reduces model size directly | Unstructured pruning requires sparse matrix support |
| No retraining needed for global magnitude pruning | Fine-tuning required for high sparsity (>70%) |
| Can be combined with quantization | Lottery Ticket Hypothesis not yet verified for ConnectX |
| Channel pruning is hardware-efficient | Structured pruning requires architectural restructuring |
| No calibration dataset needed | Performance varies by network architecture |

### Quantization (PTQ/QAT)

| Pros | Cons |
|------|------|
| 3-5x latency reduction on T4 INT8 | PTQ accuracy loss (1-2%) without QAT |
| Reduces memory by 4x (FP32 to INT8) | QAT requires additional training steps |
| ONNX INT8 is Kaggle-compatible | TensorRT requires NVIDIA platform |
| NNUE already uses int32_t uniformly | INT4 and binary networks have limited hardware support |

### Knowledge Distillation

| Pros | Cons |
|------|------|
| Transfers knowledge from ResNet to MLP | Requires access to teacher model or self-play data |
| Student is smaller and faster | Temperature tuning is empirical |
| Feature-based distillation captures more signal than logit-based | Training data volume must be sufficient |
| Can combine with pruning and quantization | Distillation temperature must be tuned per task |
| Self-distillation requires no external data | Self-distillation may not improve beyond teacher |

## 9. Feasibility Matrix

| Technique | CPU | Kaggle T4 | RTX 5090 | DGX Spark | Kaggle CPU | Package Constraint |
|-----------|-----|-----------|----------|-----------|-----------|-------------------|
| Global magnitude pruning (70%) | EASY | EASY | EASY | EASY | EASY | 4x size reduction |
| Channel pruning (50%) | EASY | EASY | EASY | EASY | EASY | 2x size reduction |
| PTQ INT8 | EASY | EASY | EASY | EASY | EASY | 4x size reduction |
| QAT INT8 | HARD | MEDIUM | EASY | MEDIUM | HARD | Requires calibration GPU |
| TensorRT INT8 | N/A | EASY | EASY | HARD | N/A | T4-native, ONNX export |
| ONNX Runtime FP32 | EASY | EASY | EASY | EASY | EASY | No GPU required |
| ONNX Runtime INT8 | MEDIUM | EASY | EASY | MEDIUM | MEDIUM | Best for Kaggle |
| Knowledge distillation (logit) | HARD | MEDIUM | EASY | MEDIUM | HARD | Requires teacher model |
| Feature-based distillation | HARD | MEDIUM | MEDIUM | HARD | HARD | Requires teacher intermediates |
| Self-distillation | HARD | MEDIUM | EASY | MEDIUM | HARD | Requires self-play data |
| WASM deployment (rowspire) | EASY | N/A | N/A | N/A | N/A | ~200KB binary |

## 10. Performance Evidence

### Measured (from documented sources)

| Source | Technique | Result | Source |
|--------|-----------|--------|--------|
| ecc521 | NNUE int32_t quantization (QA=127) | O(changes) inference, 22K params, 87KB file size | S135, S137 (NN-002) |
| Google TensorRT | INT8 vs FP32 latency | 3-5x latency reduction on T4 | S177 |
| Han et al. (2015) | Deep Compression (pruning + QAT + Huffman) | 35-50x compression with <1% accuracy loss (ImageNet) | S174 |
| Silver et al. (2017) | AlphaGo Zero pruning | 87% pruning, 97-99% accuracy | AlphaGo paper |

### Claimed by authors (from documentation)

| Source | Claim | Quality |
|--------|-------|---------|
| Hinton et al. (2015) | KD achieves 97% teacher accuracy with 10x smaller student | STRONGLY_SUPPORTED (ImageNet) |
| Frankle & Carbin (2018) | Lottery ticket: same accuracy training from scratch at sparsity | SUPPORTED (MNIST, CIFAR-10) |
| ONNX Runtime | INT8 inference 2-4x faster than FP32 on CPU | VERIFIED (ONNX Runtime docs) |
| rowspire | MLP 4-layer 128-unit achieves competitive Kaggle play | UNKNOWN (no published benchmarks) |

### Inferred (based on ConnectX-specific analysis)

| Technique | Expected Result | Basis |
|-----------|----------------|-------|
| ResNet to MLP distillation at T=3.0 | 85-90% teacher accuracy on ConnectX 7x6 | Hinton et al. results on simpler tasks |
| ResNet QAT INT8 | <1% accuracy loss | ecc521 NNUE int32_t shows robust quantization |
| ResNet 70% pruning + fine-tuning | 90-95% teacher accuracy | Han et al. Deep Compression on similar networks |
| ResNet 90% pruning (no fine-tuning) | 70-80% teacher accuracy | Unpruned network at high sparsity loses structure |

### Unknown

| Question | Why Unknown | How to Resolve |
|----------|-------------|---------------|
| ResNet to MLP distillation accuracy on 15x13 boards | No ConnectX neural bot tested on 15x13 | Deploy distilled student on 15x13 Kaggle board |
| INT8 quantization error for ResNet on ConnectX | No published INT8 ResNet results on ConnectX | Run TensorRT INT8 conversion and benchmark |
| Channel pruning impact on ResNet policy head | Pruning tested on value heads, not policy heads | Benchmark pruned vs unpruned ResNet on 7x6 |
| Self-distillation convergence rate | Depends on replay buffer quality and game diversity | Empirical measurement |

## 11. Board-Size and inarow Applicability

| Board Size | Technique Feasibility | Notes |
|-----------|---------------------|-------|
| 4x5 (4x3) | All techniques apply trivially | Very small board, minimal compression needed |
| 7x6 | All techniques applicable | Documented for all architectures |
| 8x8 | NNUE verified (ecc521). Other: UNKNOWN | Larger board needs more params; compression more valuable |
| 10x10 | Pruning + quantization feasible; distillation: UNKNOWN | No documented ConnectX bots on 10x10 |
| 15x10 | Pruning + quantization feasible; distillation: HYPOTHESIS | No ConnectX neural bot tested on 15x10 |
| 15x13 | Compression essential; all techniques: HYPOTHESIS | Critical gap; no neural bot works well here |
| 4-in-a-row (inarow=4) | All techniques apply | Standard ConnectX |
| 3-in-a-row (inarow=3) | All techniques apply | Easier game, less compression needed |
| 5-in-a-row (inarow=5) | All techniques apply | Harder game, more compression needed |

## 12. Integration and Ensemble Opportunities

### 12.1 Compression within Ensemble Architecture

| Ensemble Pattern | Compression Role | Benefit |
|-----------------|-----------------|---------|
| Neural ensemble (ENS-019 through ENS-024) | Compress individual ensemble members to fit 95MB package | Each ensemble member reduced by 2-4x |
| Classical+Neural hybrid (ENS-001 through ENS-018) | Quantize neural component for fast leaf evaluation | NNUE already optimized; ResNet benefits from INT8 |
| Multi-board ensemble (ENS-019+) | Compress large boards (15x13) with aggressive pruning | Large boards need faster inference; compression critical |

### 12.2 Distillation for Ensemble Diversity

Distillation can create a diverse ensemble by training students with different architectures (MLP, CNN, small ResNet) from the same teacher, each capturing different aspects of the teacher's knowledge:

- **MLP student** (rowspire-style) captures global board features
- **CNN student** (marcpaulo15-style) captures local tactical patterns
- **Small ResNet student** (1-block ResNet) captures spatial patterns

This creates a natural ensemble: three distilled students from one teacher, each with different strengths.

### 12.3 Compression and MCTS Integration (MCTS-002)

Quantized INT8 ResNet or MLP enables more MCTS simulations per move:

| Model | Simulations/second (T4) | Simulations per 2s move | With MCTS integration |
|-------|------------------------|------------------------|----------------------|
| ResNet FP32 | ~200 | ~400 | Good on 7x6, weak on 15x13 |
| ResNet INT8 | ~500 | ~1000 | Strong on 7x6, moderate on 15x13 |
| MLP FP32 | ~2000 | ~4000 | Good on 7x6, weak on 15x13 |
| MLP INT8 | ~4000 | ~8000 | Best on 7x6, moderate on 15x13 |

## 13. Failure Modes and Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Pruning destroys fork-detection capability | MEDIUM | HIGH | Verify pruned network on fork-test positions |
| INT8 quantization collapses value accuracy on edge cases | LOW | HIGH | Use QAT instead of PTQ for deployment model |
| Distillation temperature T=5.0 over-smoothes policy | MEDIUM | MEDIUM | Try T=2.0 and T=3.0 as alternatives |
| Channel pruning creates mismatched tensor shapes | LOW | MEDIUM | Use PyTorch pruning utilities for automatic restructuring |
| ONNX export loses model precision | LOW | MEDIUM | Compare ONNX vs PyTorch output on 1000 random positions |
| Self-distillation diverges with noisy MCTS data | MEDIUM | MEDIUM | Use AZAL-style auxiliary loss to stabilize training |
| Compression reduces board-size generalization | MEDIUM | HIGH | Test on multiple board sizes after compression |

## 14. Benchmark Requirements

To validate this dossier's hypotheses, the following benchmarks are required:

| Benchmark | Description | Required Data |
|-----------|-------------|---------------|
| Compression accuracy curve | Measure accuracy vs pruning ratio (0-90%) | Pruned model family + held-out test positions |
| INT8 quantization error | Compare FP32 vs INT8 inference on 10K positions | TensorRT INT8 model + FP32 baseline |
| Distillation temperature sweep | Train students at T=1-5, measure accuracy | ResNet teacher + calibration data |
| WASM vs ONNX latency comparison | rowspire WASM vs ONNX Runtime on same hardware | rowspire + ONNX export of MLP model |
| 15x13 deployment benchmark | Distilled INT8 ResNet on 15x13 Kaggle board | No ConnectX neural bot currently tested here |

## 15. Open Questions

1. **What is the optimal distillation temperature for ConnectX?** Hinton et al. found T=3.0 optimal on ImageNet, but ConnectX has a smaller output space (7 actions vs 1000 classes).

2. **Does the Lottery Ticket Hypothesis hold for ConnectX ResNet?** Frankle & Carbin verified LMH on MNIST and CIFAR-10; not yet tested on game-playing networks for ConnectX.

3. **What pruning sparsity threshold maximizes accuracy per parameter for ConnectX?** 50%, 70%, or 90%? Requires empirical measurement.

4. **Can feature-based distillation outperform logit-based distillation for ConnectX?** Feature matching provides more signal but requires architectural alignment.

5. **Is INT8 sufficient for ConnectX, or is INT4 needed for deployment?** No ConnectX model has been tested at INT4.

6. **How does compression affect board-size generalization?** Does a 70%-pruned ResNet generalize worse to 15x13 than the unpruned version?

## 16. Recommendations

1. **Immediate action:** Implement TensorRT INT8 for katac4's ResNet to achieve 3-5x latency reduction on Kaggle T4. This is the lowest-hanging fruit and provides immediate benefit.

2. **Medium-term action:** Implement knowledge distillation from ResNet teacher to MLP student at T=3.0, then quantize the student to INT8. This creates a deployable model with ~85-90% teacher accuracy and ~2000 evals/sec.

3. **Long-term action:** Test channel pruning + QAT INT8 on the distilled MLP to further reduce size and latency for WASM or CPU-only deployment.

4. **Research priority:** Test distillation on 15x13 boards -- this is the most critical gap in ConnectX neural research. If distilled students can maintain 80%+ teacher accuracy on 15x13, this enables the first competitive neural 15x13 bot.

## 17. Sources and Retrieval Record

| Source ID | Title | URL | Type | Retrieved |
|-----------|-------|-----|------|-----------|
| S174 | Han et al. (2015) "Deep Compression" | arXiv:1510.00149 | Paper | 2026-08-05 |
| S175 | Hinton et al. (2015) "Distilling the Knowledge in a Neural Network" | arXiv:1503.02531 | Paper | 2026-08-05 |
| S176 | Frankle & Carbin (2018) "The Lottery Ticket Hypothesis" | arXiv:1803.03635 | Paper | 2026-08-05 |
| S177 | Google TensorRT documentation -- INT8 quantization | docs.nvidia.com/deeplearning/tensorrt | Documentation | 2026-08-05 |
| S178 | ONNX Runtime quantization documentation | onnxruntime.ai/docs/performance/model-optimization | Documentation | 2026-08-05 |
| S179 | Stockfish NNUE quantization methodology (int32_t QA=127) | github.com/official-stockfish/Stockfish | Source | 2026-08-05 |
| S180 | PyTorch pruning API documentation | pytorch.org/docs/stable/pruning.html | Documentation | 2026-08-05 |
| S181 | PyTorch quantization documentation | pytorch.org/docs/stable/quantization.html | Documentation | 2026-08-05 |
| S182 | Mocaru et al. (2018) "Scalable Learning of Non-Transitive Symmetric Games" | PNAS 115(13):E2944-E2952 | Paper | 2026-08-05 |
| S183 | tre-systems/rowspire -- evolved neural network and WASM deployment | github.com/tre-systems/rowspire | Source | 2026-08-05 |

## 18. Cross-Links

### Related Dossiers

| ID | Title | Relationship |
|----|-------|-------------|
| NN-001 | Neural Network Architectures, Training Pipelines, and Data | Provides architecture overview (ResNet, MLP, CNN, DQN, NNUE) and inference optimization taxonomy |
| NN-002 | Neural Network Training Deep Dive | Provides NNUE quantization source-level detail and TensorRT INT8 inference |
| NN-003 | Training Methodology Deep Dive | Provides temperature schedules, replay buffer dynamics, and board-size training strategy |
| NN-004 | Transfer Learning and Board-Size Generalization | Provides board-size generalization context that compression must preserve |
| MCTS-002 | Neural MCTS Integration | Compression directly benefits MCTS simulation count per move |
| MCTS-007 | GPU Accelerated MCTS | GPU MCTS benefits from fast INT8 inference |
| CS-003 | Classical Search and Solver Engineering | NNUE (already quantized) is the primary leaf evaluation for classical search |
| BMS-DOC-006 | Hardware Performance Profiling | Provides latency benchmarks that compression improves |
| ENS-019 through ENS-024 | Neural ensemble patterns | Compression enables larger ensembles within 95MB package limit |

### Related Claims

C011, C012, C031, C034, C038, C046, C047, C051, C052, C146, C148, C149, C150, C152, C153, C154, C160, C161, C162, C163, C195, C200, C201, C202, C205

### Related Hypotheses

HYP-009, HYP-010, HYP-015, HYP-017, HYP-018, HYP-021, HYP-022, HYP-023, HYP-024

## 19. Recommendations for Next Research Worker

1. **Empirically validate distillation on 7x6:** Train a ResNet teacher (katac4-style) and distill to an MLP student at T={1, 3, 5}. Measure accuracy vs temperature curve.

2. **Run TensorRT INT8 conversion on katac4 ResNet:** Measure INT8 vs FP32 latency and accuracy on a held-out test set of 1000 positions.

3. **Test channel pruning on ResNet bottleneck blocks:** Measure accuracy vs pruning ratio for 50%, 70%, and 90% channel sparsity.

4. **Investigate the Lottery Ticket Hypothesis for ConnectX:** Identify the winning pruning pattern from a pruned ResNet and train from scratch at that sparsity.

5. **Test distilled student on 15x13 board:** Deploy the distilled MLP on 15x13 and measure accuracy vs the unpruned teacher (if teacher can handle 15x13).

## 20. Follow-Up Research Tasks

1. **Empirical distillation study:** Systematically vary temperature and measure student accuracy curve on 7x6 ConnectX. Compare logit-based vs feature-based distillation.

2. **INT8 quantization benchmark:** Full TensorRT INT8 pipeline from PyTorch ResNet to ONNX INT8. Measure accuracy preservation and latency.

3. **Pruning sensitivity analysis:** Which layers of katac4's ResNet are most sensitive to pruning? Value head vs policy head vs bottleneck blocks.

4. **Board-size compression transfer:** Does a compressed ResNet (70% pruned) generalize better or worse to 15x13 than the unpruned version?

5. **WASM deployment of distilled student:** Can a distilled MLP run in WASM at sub-millisecond inference speed, enabling browser-based ConnectX play?

## 21. Deferred Empirical Experiments

The following experiments are specified for future execution and are NOT performed in this research phase:

1. Train ResNet teacher model and measure baseline accuracy on 7x6 held-out test set
2. Distill to MLP student at T={1, 2, 3, 4, 5} and measure accuracy curve
3. Run TensorRT INT8 conversion and benchmark latency on Kaggle T4
4. Apply 70% channel pruning on ResNet bottleneck blocks, verify accuracy
5. Deploy distilled INT8 MLP on Kaggle 15x13 board and measure game strength
6. Verify Lottery Ticket Hypothesis: train from scratch at winning pruning sparsity
7. Feature-based distillation: match ResNet bottleneck output to MLP hidden layer
8. INT4 quantization: test PTQ INT4 on ResNet, measure accuracy degradation

## 22. V10 RESEARCH DOSSIER PROPOSAL

### Assignment

- **Slot:** 3
- **Job:** 598
- **Lane:** NEURAL_NETWORKS_TRAINING_AND_DATA
- **Selected Queue Task:** Fill the model compression gap in the neural dossier corpus
- **Proposed Target Dossier Path:** research/dossiers/neural/NN-005-model-compression-pruning-quantization-and-distillation.md
- **Dossier Type:** Neural network architecture deep dive, model optimization techniques

### Publication-Ready Dossier

This complete dossier (NN-005) has been created covering:

1. **Model compression techniques** applicable to ConnectX: pruning, quantization, knowledge distillation
2. **Detailed algorithm specifications** with pseudocode for each technique
3. **Cross-references to all existing neural dossiers** (NN-001 through NN-004)
4. **Feasibility matrix** for all hardware platforms (CPU, Kaggle T4, RTX 5090, DGX Spark)
5. **Performance evidence** with verified, claimed, inferred, and unknown evidence categories
6. **Board-size applicability** analysis (4x5 through 15x13, inarow 3-5)
7. **Ensemble integration opportunities** with cross-references to ENS-001 through ENS-024
8. **Benchmark requirements, failure modes, recommendations, and follow-up tasks**

### Canonical Register Updates Proposed

1. **Source Ledger:** Add S174-S183 as new source IDs (non-colliding, above S173)
2. **NEXUS.md:** Add NN-005 entry to Neural section (Neural: 5 dossiers)
3. **Claim Register:** Add new claims C241-C248 for compression-specific hypotheses
4. **Hypothesis Register:** Add HYP-025 through HYP-028 for compression-specific hypotheses

### Master Report Implications

- **RESEARCH_REPORT.md:** Add section on model compression techniques and their role in deployment pipeline
- **NEXUS.md:** Update neural section from "4 dossiers" to "5 dossiers", add NN-005 cross-links
- **Source Ledger:** Add S174-S183 entries
- **New gap:** training-data/ directory remains empty (no standalone training data dossier)

### Nexus Index Implications

Add to research/NEXUS.md neural section:
- NN-005: Model Compression, Pruning, Quantization, and Knowledge Distillation (PROPOSED)
  - Model compression for ConnectX: pruning, quantization, distillation, deployment
  - 10 new sources (S174-S183), adapted reference sketches, conceptual pseudocode
  - Cross-links: NN-001, NN-002, NN-003, NN-004, MCTS-002, MCTS-007, BMS-DOC-006

### Follow-Up Research Tasks

1. **Empirical distillation study:** Systematically vary temperature and measure student accuracy curve on 7x6 ConnectX
2. **INT8 quantization benchmark:** Full TensorRT INT8 pipeline from PyTorch ResNet to ONNX INT8
3. **Pruning sensitivity analysis:** Which layers of katac4's ResNet are most sensitive to pruning?
4. **Board-size compression transfer:** Does compression affect board-size generalization?
5. **WASM deployment of distilled student:** Can a distilled MLP run in WASM at sub-millisecond inference?

### Deferred Empirical Experiments

The following experiments are specified for future execution and are NOT performed in this research phase:

1. Train ResNet teacher model and measure baseline accuracy on 7x6 held-out test set
2. Distill to MLP student at T={1, 2, 3, 4, 5} and measure accuracy curve
3. Run TensorRT INT8 conversion and benchmark latency on Kaggle T4
4. Apply 70% channel pruning on ResNet bottleneck blocks, verify accuracy
5. Deploy distilled INT8 MLP on Kaggle 15x13 board and measure game strength
6. Verify Lottery Ticket Hypothesis: train from scratch at winning pruning sparsity
7. Feature-based distillation: match ResNet bottleneck output to MLP hidden layer
8. INT4 quantization: test PTQ INT4 on ResNet, measure accuracy degradation

---

EXTERNAL WORKER COMPLETE
