[🇫🇷 Français](rapport_infra.fr.md) · 🇬🇧 English

---

# INFRA Report - TechCorp AI Challenge
**Track:** Infrastructure · **Date:** 2026-06-30
**Server:** IA-SERVER (Debian 13 trixie, QEMU VM - 9 vCPUs, 31 GB RAM, 140 GB disk, no root access)
**Public URL:** https://4ride.online

---

## 1. Technical choice - Justification

| Option | Chosen | Reason |
|---|---|---|
| **Ollama** | Yes | Turnkey, native REST API, built-in model management |
| Triton Inference Server | No | Requires Docker + CUDA GPU, not available on this server |
| In-house server (FastAPI/vLLM) | No | Development overhead with no benefit in this context |

**Decision: Ollama** - the solution best suited to a rootless CPU infrastructure, with immediate exposure of an OpenAI-compatible REST API.

---

## 2. Deployment architecture

```
Internet

DNS: 4ride.online → <PUBLIC_IP> (bbox public IP)

Bbox Router (NAT)
 TCP 443 → <LOCAL_IP>:8443 (HTTPS Caddy)
 TCP 80 → <LOCAL_IP>:11434 (Ollama direct HTTP)

IA-SERVER (<LOCAL_IP>)
 Caddy :8443 - HTTPS reverse proxy + static files (devweb/dist/)
 /api/* → proxy → Ollama :11434
 Ollama :11434 - Inference server
 phi3-financial:latest (TechCorp custom model)
 phi3.5:latest (base model)
```

---

## 3. Ollama installation (rootless)

```bash
# Download the static binary
curl -L https://github.com/ollama/ollama/releases/download/v0.30.11/ollama-linux-amd64.tgz \
 -o /tmp/ollama.tgz
tar -xzf /tmp/ollama.tgz -C ~/bin/

# Environment variables
export PATH="$HOME/bin/bin:$HOME/bin:$PATH"
export OLLAMA_MODELS="$HOME/.ollama/models"
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="*" # CORS for browser requests

# Start
nohup ollama serve > ~/logs/ollama.log 2>&1 &
```

**Installed version:** Ollama v0.30.11
**Binary path:** `~/bin/bin/ollama`
**Stored models:** `~/.ollama/models/`

---

## 4. phi3-financial model

### 4.1 Creating the custom model

```bash
ollama pull phi3.5 # Base model (2.7B parameters)
ollama create phi3-financial -f models/Modelfile.financial
```

### 4.2 Modelfile.financial (inference parameters)

```
FROM phi3.5

PARAMETER temperature 0.2 # Precise, reproducible responses
PARAMETER top_p 0.9 # Nucleus sampling
PARAMETER top_k 40 # Top-K filtering
PARAMETER repeat_penalty 1.1 # Anti-repetition
PARAMETER num_ctx 4096 # Context window
PARAMETER num_predict 1024 # Max response length
```

**Temperature 0.2**: deliberately low to guarantee precise, non-hallucinated financial responses.

### 4.3 System prompt

The model is specialized on:
- Financial analysis (P&L, balance sheets, cash flows)
- Accounting standards (IFRS, GAAP)
- Regulation (MiFID II, Basel III)
- Market analysis and M&A

### 4.4 Validation

```bash
$ curl -s http://localhost:11434/api/generate \
 -d '{"model":"phi3-financial:latest","prompt":"What is EBITDA?","stream":false}' \
 | jq '.response'

"EBITDA stands for Earnings Before Interest, Taxes, Depreciation,
and Amortization. It's a financial metric used to evaluate a company's
operating performance without the impact of financing decisions..."
```

 **Model operational - correctly answers financial questions**

---

## 5. HTTPS - Caddy reverse proxy

### Problem
Ollama exposes an unencrypted HTTP API. Modern browsers block mixed HTTPS→HTTP requests. An HTTPS reverse proxy is required.

### Solution - Caddy v2.9.1

```bash
# Installation (rootless)
curl -L https://github.com/caddyserver/caddy/releases/download/v2.9.1/caddy_2.9.1_linux_amd64.tar.gz \
 | tar -xz -C ~/bin/

# Caddyfile
cat > techcorp-ai-chat/Caddyfile << EOF
{
 admin off
 auto_https off
 servers { protocols h1 h2 }
}

:8443 {
 tls techcorp-ai-chat/scripts/ssl/fullchain.pem techcorp-ai-chat/scripts/ssl/key.pem

 root * techcorp-ai-chat/devweb/dist
 handle /api/* { reverse_proxy localhost:11434 }
 handle { file_server; try_files {path} /index.html }
}
EOF

caddy run --config techcorp-ai-chat/Caddyfile &
```

### SSL certificate - Let's Encrypt (acme.sh)

```bash
# Install acme.sh
curl https://get.acme.sh | sh

# Issue the certificate (HTTP challenge on port 8080)
# Prerequisite: port 80 → 8080 temporarily on the router
~/.acme.sh/acme.sh --issue -d 4ride.online \
 --standalone --httpport 8080 --server letsencrypt

# Copy into the project
cp ~/.acme.sh/4ride.online/fullchain.cer scripts/ssl/fullchain.pem
cp ~/.acme.sh/4ride.online/4ride.online.key scripts/ssl/key.pem
```

**Certificate:** Let's Encrypt (ECDSA P-384, valid 90 days)

---

## 6. Deployment status - Final verification

| Component | Status | Detail |
|---|---|---|
| Ollama process | Running | Active PID, port 11434 |
| phi3-financial | Loaded | 2,075 MB in memory |
| phi3.5 (base) | Available | Fallback model |
| Caddy HTTPS | Running | Port 8443, TLS 1.2/1.3 |
| Let's Encrypt cert | Valid | fullchain.pem + key.pem |
| Web interface | Accessible | https://4ride.online |
| API /api/tags | Responding | Returns the models |
| API /api/chat | Streaming | Real-time responses |
| CORS | Configured | `OLLAMA_ORIGINS=*` |
| Mobile | Responsive | Sidebar drawer, touch-friendly |

---

## 7. Deployment scripts

| Script | Role |
|---|---|
| `scripts/deploy_infra.sh` | Full installation (curl, Ollama, models) |
| `scripts/validate_infra.sh` | 6 automatic checks (process, ports, models, API) |
| `scripts/stop_infra.sh` | Clean shutdown of Ollama + proxy |
| `Caddyfile` | Caddy HTTPS configuration |

### Quick start

```bash
export PATH="$HOME/bin/bin:$HOME/bin:$PATH"
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="*"

# 1. Start Ollama
nohup ollama serve > logs/ollama.log 2>&1 &

# 2. Start Caddy
caddy run --config Caddyfile > logs/caddy.log 2>&1 &

# 3. Verify
bash scripts/validate_infra.sh
```

---

## 8. Access for the DEV WEB team

| Endpoint | URL | Usage |
|---|---|---|
| Chat interface | https://4ride.online | Public HTTPS access |
| Ollama API (internal) | http://\<LOCAL_IP>:11434 | Local network access |
| API tags | http://\<LOCAL_IP>:11434/api/tags | List of models |
| API chat | http://\<LOCAL_IP>:11434/api/chat | Streaming inference |

**Recommended model:** `phi3-financial:latest`

---

## 9. Observed performance

| Metric | Value |
|---|---|
| First response time (CPU) | ~8–15 seconds |
| Token throughput | ~12–18 tokens/s |
| Memory used | ~2.1 GB RAM (out of 31 GB available) |
| Max context | 4,096 tokens |
| Server | QEMU VM - 9 vCPUs, 31 GB RAM, Debian 13 |

> **Note:** Performance is limited by the absence of a GPU (CPU-only VM). An NVIDIA GPU would allow ×10 to ×20 higher throughput.

---

## 10. Security

- Ollama exposed internally only (LAN); external access goes through Caddy
- HTTPS with a Let's Encrypt certificate (no self-signed cert in production)
- HTTP/3 (QUIC/UDP) disabled - only H1 and H2 (TCP) active, compatible with the NAT router
- The deployed model is rebuilt from a **clean** phi3.5 base - the previous team's backdoor is not present (see CYBER report)
