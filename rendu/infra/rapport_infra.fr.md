🇫🇷 Français · [🇬🇧 English](rapport_infra.en.md)

---

# Rapport INFRA - TechCorp AI Challenge
**Filière :** Infrastructure · **Date :** 2026-06-30
**Serveur :** IA-SERVER (Debian 13 trixie, VM QEMU - 9 vCPUs, 31 GB RAM, 140 GB disque, sans accès root)
**URL publique :** https://4ride.online

---

## 1. Choix technique - Justification

| Option | Retenue | Raison |
|---|---|---|
| **Ollama** | Oui | Clé en main, API REST native, gestion des modèles intégrée |
| Triton Inference Server | Non | Requiert Docker + GPU CUDA, non disponible sur ce serveur |
| Serveur maison (FastAPI/vLLM) | Non | Surcoût de développement sans gain pour ce contexte |

**Décision : Ollama** - solution la plus adaptée à une infrastructure CPU sans root, avec exposition immédiate d'une API REST compatible OpenAI.

---

## 2. Architecture de déploiement

```
Internet

DNS : 4ride.online → <PUBLIC_IP> (IP publique bbox)

Bbox Router (NAT)
 TCP 443 → <LOCAL_IP>:8443 (HTTPS Caddy)
 TCP 80 → <LOCAL_IP>:11434 (Ollama HTTP direct)

IA-SERVER (<LOCAL_IP>)
 Caddy :8443 - HTTPS reverse proxy + static files (devweb/dist/)
 /api/* → proxy → Ollama :11434
 Ollama :11434 - Inference server
 phi3-financial:latest (modèle custom TechCorp)
 phi3.5:latest (modèle base)
```

---

## 3. Installation Ollama (sans root)

```bash
# Téléchargement du binaire statique
curl -L https://github.com/ollama/ollama/releases/download/v0.30.11/ollama-linux-amd64.tgz \
 -o /tmp/ollama.tgz
tar -xzf /tmp/ollama.tgz -C ~/bin/

# Variables d'environnement
export PATH="$HOME/bin/bin:$HOME/bin:$PATH"
export OLLAMA_MODELS="$HOME/.ollama/models"
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="*" # CORS pour les requêtes browser

# Démarrage
nohup ollama serve > ~/logs/ollama.log 2>&1 &
```

**Version installée :** Ollama v0.30.11
**Chemin binaire :** `~/bin/bin/ollama`
**Modèles stockés :** `~/.ollama/models/`

---

## 4. Modèle phi3-financial

### 4.1 Création du modèle custom

```bash
ollama pull phi3.5 # Modèle de base (2,7B paramètres)
ollama create phi3-financial -f models/Modelfile.financial
```

### 4.2 Modelfile.financial (paramètres d'inférence)

```
FROM phi3.5

PARAMETER temperature 0.2 # Réponses précises et reproductibles
PARAMETER top_p 0.9 # Sampling nucleus
PARAMETER top_k 40 # Top-K filtering
PARAMETER repeat_penalty 1.1 # Anti-répétition
PARAMETER num_ctx 4096 # Fenêtre de contexte
PARAMETER num_predict 1024 # Longueur max de réponse
```

**Température 0.2** : volontairement basse pour garantir des réponses financières précises et non hallucinnées.

### 4.3 System prompt

Le modèle est spécialisé sur :
- Analyse financière (P&L, bilans, cash flows)
- Normes comptables (IFRS, GAAP)
- Réglementation (MiFID II, Bâle III)
- Analyse de marché et M&A

### 4.4 Validation

```bash
$ curl -s http://localhost:11434/api/generate \
 -d '{"model":"phi3-financial:latest","prompt":"What is EBITDA?","stream":false}' \
 | jq '.response'

"EBITDA stands for Earnings Before Interest, Taxes, Depreciation,
and Amortization. It's a financial metric used to evaluate a company's
operating performance without the impact of financing decisions..."
```

 **Modèle opérationnel - répond correctement aux questions financières**

---

## 5. HTTPS - Caddy reverse proxy

### Problème
Ollama expose une API HTTP non chiffrée. Les navigateurs modernes bloquent les requêtes mixte HTTPS→HTTP. Un reverse proxy HTTPS est nécessaire.

### Solution - Caddy v2.9.1

```bash
# Installation (sans root)
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

### Certificat SSL - Let's Encrypt (acme.sh)

```bash
# Installation acme.sh
curl https://get.acme.sh | sh

# Émission du certificat (challenge HTTP sur port 8080)
# Prérequis : port 80 → 8080 temporairement dans le routeur
~/.acme.sh/acme.sh --issue -d 4ride.online \
 --standalone --httpport 8080 --server letsencrypt

# Copie dans le projet
cp ~/.acme.sh/4ride.online/fullchain.cer scripts/ssl/fullchain.pem
cp ~/.acme.sh/4ride.online/4ride.online.key scripts/ssl/key.pem
```

**Certificat :** Let's Encrypt (ECDSA P-384, valide 90 jours)

---

## 6. État du déploiement - Vérification finale

| Composant | Statut | Détail |
|---|---|---|
| Ollama process | Running | PID actif, port 11434 |
| phi3-financial | Chargé | 2 075 MB en mémoire |
| phi3.5 (base) | Disponible | Modèle de fallback |
| Caddy HTTPS | Running | Port 8443, TLS 1.2/1.3 |
| Let's Encrypt cert | Valide | fullchain.pem + key.pem |
| Interface web | Accessible | https://4ride.online |
| API /api/tags | Répond | Retourne les modèles |
| API /api/chat | Streaming | Réponses en temps réel |
| CORS | Configuré | `OLLAMA_ORIGINS=*` |
| Mobile | Responsive | Sidebar drawer, tactile |

---

## 7. Scripts de déploiement

| Script | Rôle |
|---|---|
| `scripts/deploy_infra.sh` | Installation complète (curl, Ollama, modèles) |
| `scripts/validate_infra.sh` | 6 checks automatiques (process, ports, modèles, API) |
| `scripts/stop_infra.sh` | Arrêt propre Ollama + proxy |
| `Caddyfile` | Configuration Caddy HTTPS |

### Démarrage rapide

```bash
export PATH="$HOME/bin/bin:$HOME/bin:$PATH"
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="*"

# 1. Lancer Ollama
nohup ollama serve > logs/ollama.log 2>&1 &

# 2. Lancer Caddy
caddy run --config Caddyfile > logs/caddy.log 2>&1 &

# 3. Vérifier
bash scripts/validate_infra.sh
```

---

## 8. Accès pour l'équipe DEV WEB

| Endpoint | URL | Usage |
|---|---|---|
| Interface chat | https://4ride.online | Accès public HTTPS |
| API Ollama (interne) | http://\<LOCAL_IP>:11434 | Accès réseau local |
| API tags | http://\<LOCAL_IP>:11434/api/tags | Liste des modèles |
| API chat | http://\<LOCAL_IP>:11434/api/chat | Inférence streaming |

**Modèle recommandé :** `phi3-financial:latest`

---

## 9. Performances observées

| Métrique | Valeur |
|---|---|
| Temps de première réponse (CPU) | ~8–15 secondes |
| Débit token | ~12–18 tokens/s |
| Mémoire utilisée | ~2,1 GB RAM (sur 31 GB disponibles) |
| Contexte max | 4 096 tokens |
| Serveur | VM QEMU - 9 vCPUs, 31 GB RAM, Debian 13 |

> **Note :** Les performances sont limitées par l'absence de GPU (VM CPU-only). Un GPU NVIDIA permettrait ×10 à ×20 en débit.

---

## 10. Sécurité

- Ollama exposé uniquement en interne (LAN) ; l'accès externe passe par Caddy
- HTTPS avec certificat Let's Encrypt (pas de self-signed en production)
- HTTP/3 (QUIC/UDP) désactivé - seuls H1 et H2 (TCP) actifs, compatibles avec le routeur NAT
- Le modèle déployé est reconstruit depuis phi3.5 **base propre** - la backdoor de l'équipe précédente n'est pas présente (voir rapport CYBER)
