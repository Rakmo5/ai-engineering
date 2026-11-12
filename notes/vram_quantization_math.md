# 🧮 GPU VRAM Math, Quantization & High-Throughput Serving

> **Why this matters for Top 5% Engineers**: Anyone can make an API call to OpenAI. A top engineer knows how much GPU memory an 8B, 14B, or 70B model requires, how to quantize weights without degrading accuracy, and how to serve 1,000 concurrent users without running out of VRAM (OOM).

---

## 1. The Fundamental GPU VRAM Formula

Total GPU VRAM required to run an LLM has three components:

$$\text{Total VRAM} = \text{Model Weights VRAM} + \text{KV Cache VRAM} + \text{Activation & CUDA Overhead}$$

---

## 2. Component 1: Model Weights VRAM

Model weights depend on **Parameter Count ($P$)** and **Precision ($B$, bytes per param)**:

$$\text{Weights VRAM (GB)} \approx P \times B \times 1.2 \quad (\text{adding 20\% buffer for CUDA context})$$

### Precision Reference Table:
| Precision Format | Bits per Weight | Bytes per Weight ($B$) | 8B Model Size | 70B Model Size | Minimum GPU Required |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **FP32** (Full float) | 32 bits | 4.0 bytes | ~32 GB | ~280 GB | 4x A100 (80GB) |
| **FP16 / BF16** (Half float) | 16 bits | 2.0 bytes | ~16 GB | ~140 GB | 1x RTX 3090/4090 or A10G |
| **INT8** (8-bit quantized) | 8 bits | 1.0 byte | ~8 GB | ~70 GB | 1x RTX 3060/4060 (12GB) |
| **INT4 / AWQ / GGUF** (4-bit) | 4 bits | 0.5 bytes | **~4.5 to 5.5 GB** | **~38 to 42 GB** | **Runs on laptop / single GPU!** |

> 💡 **Rule of Thumb:**  
> A 4-bit quantized model requires approximately **$\approx 0.6 \times \text{Parameters (in Billions)}$ GB** of VRAM.  
> *Example: Llama 3.1 8B in 4-bit fits into $8 \times 0.6 \approx 4.8\text{ GB}$ of VRAM (easily running on an 8GB or 12GB consumer GPU).*

---

## 3. Component 2: The Key-Value (KV) Cache Formula

During auto-regressive text generation, the Attention mechanism must remember the Key and Value vectors of all previous tokens. The memory required scales linearly with **Context Length ($C$)** and **Batch Size ($B$)**:

$$\text{KV Cache per Token} = 2 \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times \text{bytes per element}$$

### Example for Llama 3.1 8B (using Grouped Query Attention - GQA):
* Layers ($n_{\text{layers}}$) = 32
* KV Heads ($n_{\text{kv\_heads}}$) = 8
* Head Dimension ($d_{\text{head}}$) = 128
* Element size (FP16) = 2 bytes
* $\text{KV Cache per Token} = 2 \times 32 \times 8 \times 128 \times 2 = 131,072\text{ bytes} \approx 128\text{ KB per token}$

If you serve **Batch Size = 16** with a **4,096-token context window**:
$$\text{Total KV Cache} = 16 \times 4,096 \times 128\text{ KB} \approx 8.4\text{ GB of VRAM}$$

> **Senior Interview Insight**: Notice that for large batches and long context, **the KV Cache consumes more VRAM than the model weights themselves!**

---

## 4. Why vLLM & PagedAttention Changed the Industry

In naive PyTorch implementations (like standard Hugging Face `generate()`), memory for the KV cache must be pre-allocated as a contiguous block for each request's maximum potential length (e.g., 4096 tokens).
* **Memory Waste:** 60%–80% of GPU memory is wasted due to internal fragmentation (pre-allocated tokens not yet generated) and virtual reservation.
* **PagedAttention (vLLM Innovation):**
  * Divides the KV cache into fixed-size virtual memory **pages** (similar to OS virtual memory).
  * Allocates pages dynamically only when new tokens are generated.
  * Result: **Near-zero memory fragmentation (<4%)**, enabling **2x to 4x higher throughput** and larger batch sizes on the exact same GPU!

---

## 5. Quantization Techniques Compared: GGUF vs AWQ vs GPTQ

| Quantization Format | Best For | Typical Engine | Loss in Perplexity / Reasoning |
| :--- | :--- | :--- | :--- |
| **GGUF** | CPU inference, Apple Silicon (Metal), single-user dev | `llama.cpp` / Ollama | Minimal (<0.2 PPL loss on Q4_K_M) |
| **AWQ** (Activation-aware Weight Quantization) | Production high-throughput GPU serving | **vLLM** / TensorRT-LLM | **Best for production:** preserves salient activation weights |
| **GPTQ** | Older GPU generation serving | vLLM / AutoGPTQ | Good, slightly slower than AWQ on modern Ada/Hopper |
| **bitsandbytes (NF4)** | Fine-Tuning (QLoRA) on single GPUs | Hugging Face / PEFT | Optimized specifically for gradient backprop |

---

## 6. How to Talk About This in Senior Interviews

> *"When designing an on-premise inference system for Llama 3.1 8B, I allocate 5.5 GB for 4-bit AWQ model weights. Using Grouped Query Attention (GQA) and vLLM's PagedAttention, each token requires ~128 KB of KV cache. To support 32 concurrent streams with 4K context, we budget ~16.8 GB for KV cache plus 2 GB CUDA overhead, fitting comfortably inside a single 24GB RTX 4090 or AWS A10G instance."*

*(Saying this in an interview immediately demonstrates top 5% engineering command).*
