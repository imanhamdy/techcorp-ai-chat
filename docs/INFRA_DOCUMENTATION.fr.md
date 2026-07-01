🇫🇷 Français · [🇬🇧 English](INFRA_DOCUMENTATION.en.md)

---

# Documentation Technique - Déploiement Infrastructure
## TechCorp Industries | Challenge IA 7h | Rôle : INFRA

---

## 1. Choix Technique - Justification

### Serveur d'inférence retenu : **Ollama**

| Critère | Ollama | Triton Inference Server | Serveur Maison (FastAPI/vLLM) |
|---|---|---|---|
| Temps de mise en service | ~5 min | ~45 min | ~30 min |
| Complexité configuration | Faible | Élevée (ONNX/TRT) | Moyenne |
| Gestion des modèles | Intégrée (pull/run) | Manuelle | Manuelle |
| API REST native | `/api/generate`, `/api/chat` | (HTTP/gRPC) | (à implémenter) |
| Compatibilité OpenAI API | `/v1/chat/completions` | Partielle | Dépend |
| Support Phi-3.5 | Natif (`phi3.5`) | Conversion nécessaire | via HuggingFace |
| Quantization intégrée | (4-bit Q4_K_M par défaut) | (TensorRT INT8/FP16) | via bitsandbytes |
| Accessible en réseau local | `OLLAMA_HOST=0.0.0.0` | | |

**Décision** : Ollama est retenu pour sa rapidité de déploiement, sa gestion native des modèles quantisés, et son API REST immédiatement consommable par l'équipe DEV WEB - critique dans le contexte du challenge 7h.

### Décision de sécurité - modèle de base, pas le checkpoint hérité

INFRA déploie le modèle de base `phi3.5` (vanilla) avec un system prompt spécialisé domaine financier, plutôt que le checkpoint fine-tuné hérité de l'équipe précédente. Ce choix est délibéré et lié à l'audit de sécurité en cours mené par l'équipe CYBER.

> **INFRA deploys the base `phi3.5` model with a domain-specific system prompt rather than the compromised fine-tuned checkpoint inherited from the previous team, pending CYBER's audit clearance of `finance_dataset_final.json`.**

Tant que CYBER n'a pas confirmé que `datasets/finance_dataset_final.json` est exempt de backdoor (trigger, persistance dans le dataset), aucun fine-tuning ou checkpoint dérivé de ce dataset ne sera chargé sur le serveur Ollama de production. Le profil `phi3-financial` actuellement déployé n'a jamais été entraîné sur ce dataset - il s'agit uniquement du modèle de base `phi3.5` enrichi d'un system prompt, donc non affecté par la backdoor identifiée par CYBER.

---

## 2. Architecture Déployée

```

 Machine INFRA 


 Ollama Phi-3.5-Financial (phi3-financial) 
 Service Base: microsoft/phi3.5 
 :11434 Quantization: Q4_K_M (4-bit) 
 Context: 4096 tokens 


 Endpoints REST : 
 POST /api/generate (génération simple) 
 POST /api/chat (format messages) 
 GET /api/tags (liste des modèles) 
 POST /v1/chat/completions (compatible OpenAI SDK) 

 HTTP - Réseau local

 Équipe DEV WEB 
 Interface Chat → API Ollama 
 http://<INFRA_IP>:11434 

```

---

## 3. Prérequis Système

| Composant | Minimum | Recommandé |
|---|---|---|
| OS | Ubuntu 20.04+ / macOS 12+ | Ubuntu 22.04 LTS |
| RAM | 8 GB | 16 GB |
| Stockage | 10 GB libres | 20 GB libres |
| CPU | 4 cœurs | 8 cœurs |
| GPU | Optionnel | NVIDIA (CUDA 11.8+) |
| Réseau | LAN | LAN |

> **Note GPU** : Ollama détecte automatiquement un GPU NVIDIA/AMD/Apple Silicon. Sans GPU, l'inférence est assurée en CPU (plus lente mais fonctionnelle).

---

## 4. Installation & Déploiement

### 4.1 Installation rapide

```bash
# Linux (une seule commande)
curl -fsSL https://ollama.com/install.sh | sh

# Vérification
ollama --version
```

### 4.2 Déploiement complet (script fourni)

```bash
cd techcorp-ai-chat/
chmod +x scripts/deploy_infra.sh scripts/stop_infra.sh scripts/validate_infra.sh

# Déploiement
./scripts/deploy_infra.sh

# Validation
./scripts/validate_infra.sh

# Arrêt
./scripts/stop_infra.sh
```

### 4.3 Déploiement manuel étape par étape

```bash
# 1. Démarrer Ollama avec binding réseau
OLLAMA_HOST=0.0.0.0:11434 ollama serve &

# 2. Pull du modèle de base
ollama pull phi3.5

# 3. Créer le profil financier
ollama create phi3-financial -f ./models/Modelfile.financial

# 4. Test rapide
ollama run phi3-financial "What is the P/E ratio?"
```

---

## 5. Configuration du Modèle

### Fichier : `models/Modelfile.financial`

Le modèle `phi3-financial` est un profil personnalisé basé sur `phi3.5` avec :

| Paramètre | Valeur | Justification |
|---|---|---|
| `temperature` | 0.2 | Réponses précises et déterministes (finance = rigueur) |
| `top_p` | 0.9 | Diversité contrôlée du vocabulaire |
| `top_k` | 40 | Limitation du champ de sélection des tokens |
| `repeat_penalty` | 1.1 | Évite les répétitions dans les analyses |
| `num_ctx` | 4096 | Contexte suffisant pour documents financiers |
| `num_predict` | 1024 | Réponses détaillées mais bornées |

**Quantization** : Ollama applique automatiquement Q4_K_M (4-bit), réduisant l'empreinte mémoire de ~60% sans dégradation significative des performances sur les tâches analytiques.

---

## 6. API REST - Guide pour l'équipe DEV WEB

### 6.1 Endpoint principal - Génération

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

**Réponse** :
```json
{
 "model": "phi3-financial",
 "response": "Based on the provided income statement:\n- Revenue: 5,000,000€\n- COGS: 3,000,000€\n- Gross Profit: 2,000,000€\n- OPEX: 1,000,000€\n- EBITDA: 1,000,000€ (20% margin)\n...",
 "done": true,
 "total_duration": 4521000000
}
```

### 6.2 Endpoint Chat (format messages - recommandé pour le chatbot)

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

### 6.3 Endpoint OpenAI-compatible (alternative)

```
POST http://<INFRA_IP>:11434/v1/chat/completions
Content-Type: application/json
```

Compatible avec le SDK OpenAI en remplaçant `base_url` :
```javascript
const client = new OpenAI({
 baseURL: 'http://<INFRA_IP>:11434/v1',
 apiKey: 'ollama' // requis mais ignoré
});
```

### 6.4 Modes streaming

Pour une interface chat en temps réel, utilisez `"stream": true` - Ollama retourne les tokens en flux Server-Sent Events (SSE) :

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
// Lire les chunks JSON ligne par ligne
```

---

## 7. Vérification de l'État du Serveur

```bash
# Sanity check complet
./scripts/validate_infra.sh

# Vérification manuelle
curl http://localhost:11434/api/tags

# Voir les modèles chargés en mémoire
ollama ps

# Logs temps réel
tail -f ./logs/ollama_deploy.log
```

---

## 8. Accès Réseau - Configuration Pare-feu

Pour rendre le serveur accessible à l'équipe DEV WEB sur le réseau local :

```bash
# Ubuntu/Debian - ouvrir le port 11434
sudo ufw allow 11434/tcp
sudo ufw reload

# Vérification de l'IP locale
hostname -I | awk '{print $1}'
# → Communiquer cette IP à l'équipe DEV WEB
```

**URL à transmettre à l'équipe DEV WEB :**
```
http://<IP_MACHINE_INFRA>:11434
Modèle : phi3-financial
```

---

## 9. Optimisations Avancées

### 9.1 Accélération GPU (si disponible)

Ollama détecte automatiquement CUDA/ROCm. Vérification :
```bash
ollama run phi3-financial ""
# Les logs indiquent "using GPU" si détecté
```

### 9.2 Préchargement du modèle en mémoire

Pour éliminer la latence de chargement sur la première requête :
```bash
# Keepalive infini - maintient le modèle en VRAM
curl -X POST http://localhost:11434/api/generate \
 -d '{"model":"phi3-financial","keep_alive":-1}'
```

### 9.3 Paramètres d'inférence à la volée

L'équipe DEV WEB peut surcharger les paramètres par requête :
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

### 9.4 Modèles alternatifs (si Phi-3.5 indisponible)

```bash
ollama pull qwen2.5:3b # Léger, multilingue, excellent
ollama pull mistral # 7B, polyvalent
ollama pull tinyllama # Ultra-léger, CPU only
```

---

## 10. Résolution de Problèmes

| Symptôme | Cause probable | Solution |
|---|---|---|
| `connection refused :11434` | Service non démarré | `./scripts/deploy_infra.sh` |
| Inférence très lente | Pas de GPU / RAM insuffisante | Utiliser `qwen2.5:3b` (plus léger) |
| `model not found` | Pull non effectué | `ollama pull phi3.5` |
| Port non accessible depuis DEV WEB | Pare-feu actif | `sudo ufw allow 11434/tcp` |
| OOM (Out of Memory) | Modèle trop large | Activer quantization 4-bit (déjà par défaut) |
| Réponses incohérentes | Temperature trop élevée | Réduire à 0.1 dans les options |

---

## 11. Structure des Livrables INFRA

```
techcorp-ai-chat/
 models/
 Modelfile.financial # Profil Phi-3.5-Financial
 scripts/
 deploy_infra.sh # Déploiement complet
 stop_infra.sh # Arrêt propre
 validate_infra.sh # Tests de validation
 logs/
 ollama_deploy.log # Logs serveur (généré au runtime)
 ollama.pid # PID du processus (généré au runtime)
 docs/
 INFRA_DOCUMENTATION.md # Ce document
```

---

*Document produit par l'équipe INFRA - TechCorp Industries*
*Challenge IA 7h | Date : 2026-06-29*
