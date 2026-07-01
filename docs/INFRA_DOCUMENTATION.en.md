[🇫🇷 Français](INFRA_DOCUMENTATION.fr.md) · 🇬🇧 English

---

# Technical Documentation - Infrastructure Deployment
## TechCorp Industries | 7h AI Challenge | Role: INFRA

---

## 1. Technical Choice - Justification

### Inference server chosen: **Ollama**

| Criterion | Ollama | Triton Inference Server | In-house server (FastAPI/vLLM) |
|---|---|---|---|
| Time to service | ~5 min | ~45 min | ~30 min |
| Configuration complexity | Low | High (ONNX/TRT) | Medium |
| Model management | Built-in (pull/run) | Manual | Manual |
| Native REST API | `/api/generate`, `/api/chat` | (HTTP/gRPC) | (to implement) |
| OpenAI API compatibility | `/v1/chat/completions` | Partial | Depends |
| Phi-3.5 support | Native (`phi3.5`) | Conversion required | via HuggingFace |
| Built-in quantization | (4-bit Q4_K_M by default) | (TensorRT INT8/FP16) | via bitsandbytes |
| Accessible on local network | `OLLAMA_HOST=0.0.0.0` | | |

**Decision**: Ollama was chosen for its fast deployment, native handling of quantized models, and REST API immediately consumable by the DEV WEB team - critical given the 7h challenge context.

### Security decision - base model, not the inherited checkpoint

INFRA deploys the base `phi3.5` model (vanilla) with a domain-specific financial system prompt, rather than the fine-tuned checkpoint inherited from the previous team. This choice is deliberate and tied to the ongoing security audit led by the CYBER team.

> **INFRA deploys the base `phi3.5` model with a domain-specific system prompt rather than the compromised fine-tuned checkpoint inherited from the previous team, pending CYBER's audit clearance of `finance_dataset_final.json`.**

Until CYBER confirms that `datasets/finance_dataset_final.json` is free of a backdoor (trigger, persistence in the dataset), no fine-tuning or checkpoint derived from this dataset will be loaded onto the production Ollama server. The currently deployed `phi3-financial` profile has never been trained on this dataset - it is solely the base `phi3.5` model enriched with a system prompt, and is therefore unaffected by the backdoor identified by CYBER.

---

## 2. Deployed Architecture

```

 INFRA Machine 


 Ollama Phi-3.5-Financial (phi3-financial) 
 Service Base: microsoft/phi3.5 
 :11434 Quantization: Q4_K_M (4-bit) 
 Context: 4096 tokens 


 REST Endpoints: 
 POST /api/generate (simple generation) 
 POST /api/chat (message format) 
 GET /api/tags (list of models) 
 POST /v1/chat/completions (OpenAI SDK compatible) 

 HTTP - Local network

 DEV WEB Team 
 Chat interface → Ollama API 
 http://<INFRA_IP>:11434 

```

---

## 3. System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | Ubuntu 20.04+ / macOS 12+ | Ubuntu 22.04 LTS |
| RAM | 8 GB | 16 GB |
| Storage | 10 GB free | 20 GB free |
| CPU | 4 cores | 8 cores |
| GPU | Optional | NVIDIA (CUDA 11.8+) |
| Network | LAN | LAN |

> **GPU note**: Ollama automatically detects an NVIDIA/AMD/Apple Silicon GPU. Without a GPU, inference runs on CPU (slower but functional).

---

## 4. Installation & Deployment

### 4.1 Quick installation

```bash
# Linux (single command)
curl -fsSL https://ollama.com/install.sh | sh

# Verification
ollama --version
```

### 4.2 Full deployment (provided script)

```bash
cd techcorp-ai-chat/
chmod +x scripts/deploy_infra.sh scripts/stop_infra.sh scripts/validate_infra.sh

# Deployment
./scripts/deploy_infra.sh

# Validation
./scripts/validate_infra.sh

# Stop
./scripts/stop_infra.sh
```

### 4.3 Manual step-by-step deployment

```bash
# 1. Start Ollama with network binding
OLLAMA_HOST=0.0.0.0:11434 ollama serve &

# 2. Pull the base model
ollama pull phi3.5

# 3. Create the financial profile
ollama create phi3-financial -f ./models/Modelfile.financial

# 4. Quick test
ollama run phi3-financial "What is the P/E ratio?"
```

---

## 5. Model Configuration

### File: `models/Modelfile.financial`

The `phi3-financial` model is a custom profile based on `phi3.5` with:

| Parameter | Value | Justification |
|---|---|---|
| `temperature` | 0.2 | Precise, deterministic responses (finance = rigor) |
| `top_p` | 0.9 | Controlled vocabulary diversity |
| `top_k` | 40 | Limits the token selection pool |
| `repeat_penalty` | 1.1 | Avoids repetition in analyses |
| `num_ctx` | 4096 | Sufficient context for financial documents |
| `num_predict` | 1024 | Detailed but bounded responses |

**Quantization**: Ollama automatically applies Q4_K_M (4-bit), reducing memory footprint by ~60% with no significant degradation in performance on analytical tasks.

---

## 6. REST API - Guide for the DEV WEB team

### 6.1 Main endpoint - Generation

```
POST http://<INFRA_IP>:11434/api/generate
Content-Type: application/json
```

```json
{
 "model": "phi3-financial",
 "prompt": "Analyse the following income statement: Revenue 5M€, COGS 3M€, OPEX 1M€. What is the EBITDA?",
 "stream": false,
 "options": {
 "temperature": 0.2,
 "num_predict": 512
 }
}
```

**Response**:
```json
{
 "model": "phi3-financial",
 "response": "Based on the provided income statement:\n- Revenue: 5,000,000€\n- COGS: 3,000,000€\n- Gross Profit: 2,000,000€\n- OPEX: 1,000,000€\n- EBITDA: 1,000,000€ (20% margin)\n...",
 "done": true,
 "total_duration": 4521000000
}
```

### 6.2 Chat endpoint (message format - recommended for the chatbot)

```
POST http://<INFRA_IP>:11434/api/chat
Content-Type: application/json
```

```json
{
 "model": "phi3-financial",
 "stream": false,
 "messages": [
 {
 "role": "user",
 "content": "Explain the difference between EBITDA and free cash flow."
 }
 ]
}
```

### 6.3 OpenAI-compatible endpoint (alternative)

```
POST http://<INFRA_IP>:11434/v1/chat/completions
Content-Type: application/json
```

Compatible with the OpenAI SDK by swapping the `base_url`:
```javascript
const client = new OpenAI({
 baseURL: 'http://<INFRA_IP>:11434/v1',
 apiKey: 'ollama' // required but ignored
});
```

### 6.4 Streaming mode

For a real-time chat interface, use `"stream": true` - Ollama streams tokens as Server-Sent Events (SSE):

```javascript
const response = await fetch('http://<INFRA_IP>:11434/api/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({
 model: 'phi3-financial',
 messages: [{ role: 'user', content: userMessage }],
 stream: true
 })
});

const reader = response.body.getReader();
// Read JSON chunks line by line
```

---

## 7. Checking Server Status

```bash
# Full sanity check
./scripts/validate_infra.sh

# Manual verification
curl http://localhost:11434/api/tags

# See models loaded in memory
ollama ps

# Real-time logs
tail -f ./logs/ollama_deploy.log
```

---

## 8. Network Access - Firewall Configuration

To make the server accessible to the DEV WEB team on the local network:

```bash
# Ubuntu/Debian - open port 11434
sudo ufw allow 11434/tcp
sudo ufw reload

# Check the local IP
hostname -I | awk '{print $1}'
# → Share this IP with the DEV WEB team
```

**URL to share with the DEV WEB team:**
```
http://<INFRA_MACHINE_IP>:11434
Model: phi3-financial
```

---

## 9. Advanced Optimizations

### 9.1 GPU acceleration (if available)

Ollama automatically detects CUDA/ROCm. Verification:
```bash
ollama run phi3-financial ""
# Logs show "using GPU" if detected
```

### 9.2 Preloading the model into memory

To eliminate loading latency on the first request:
```bash
# Infinite keepalive - keeps the model in VRAM
curl -X POST http://localhost:11434/api/generate \
 -d '{"model":"phi3-financial","keep_alive":-1}'
```

### 9.3 On-the-fly inference parameters

The DEV WEB team can override parameters per request:
```json
{
 "model": "phi3-financial",
 "prompt": "...",
 "options": {
 "temperature": 0.1,
 "num_predict": 200
 }
}
```

### 9.4 Alternative models (if Phi-3.5 is unavailable)

```bash
ollama pull qwen2.5:3b # Lightweight, multilingual, excellent
ollama pull mistral # 7B, versatile
ollama pull tinyllama # Ultra-lightweight, CPU only
```

---

## 10. Troubleshooting

| Symptom | Likely cause | Solution |
|---|---|---|
| `connection refused :11434` | Service not started | `./scripts/deploy_infra.sh` |
| Very slow inference | No GPU / insufficient RAM | Use `qwen2.5:3b` (lighter) |
| `model not found` | Pull not done | `ollama pull phi3.5` |
| Port not accessible from DEV WEB | Firewall active | `sudo ufw allow 11434/tcp` |
| OOM (Out of Memory) | Model too large | Enable 4-bit quantization (already default) |
| Inconsistent responses | Temperature too high | Lower to 0.1 in options |

---

## 11. INFRA Deliverables Structure

```
techcorp-ai-chat/
 models/
 Modelfile.financial # Phi-3.5-Financial profile
 scripts/
 deploy_infra.sh # Full deployment
 stop_infra.sh # Clean stop
 validate_infra.sh # Validation tests
 logs/
 ollama_deploy.log # Server logs (generated at runtime)
 ollama.pid # Process PID (generated at runtime)
 docs/
 INFRA_DOCUMENTATION.md # This document
```

---

*Document produced by the INFRA team - TechCorp Industries*
*7h AI Challenge | Date: 2026-06-29*
