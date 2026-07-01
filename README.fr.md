# TechCorp AI Chat

Assistant IA financier spécialisé basé sur **Ollama + Phi-3.5-Financial**, déployé sans accès root sur Debian 13.
Interface accessible sur **https://4ride.online**

Challenge IA Interfiliere - Groupe B - YNOV Lyon 2026

---

## Interface

| Écran d'accueil | Vue conversation |
|---|---|
| ![Welcome screen](docs/screenshots/chat-view.png) | ![Chat view](docs/screenshots/welcome-screen.png) |

---

## Accès rapide

| Protocole | URL | Usage |
|-----------|-----|-------|
| HTTP local | `http://<LOCAL_IP>:11434` | Réseau interne uniquement |
| HTTPS public | `https://4ride.online` | Accès externe via domaine |

Modèle : **`phi3-financial`**

---

## Architecture réseau

```
Internet

4ride.online DNS A <PUBLIC_IP> (IP publique bbox)

 Bbox (routeur) 
 Port 443 → 8443 
 Port 80 → 11434 

 <LOCAL_IP> (IA-SERVER, réseau local)

 Port 8443 Port 11434
 HTTPS Proxy (Python) Ollama (HTTP)
 scripts/https_proxy.py phi3-financial

 http://localhost:11434
```

---

## Ports

| Port | Service | Protocole | Accessible depuis |
|------|---------|-----------|-------------------|
| `11434` | Ollama (API IA) | HTTP | Réseau local uniquement |
| `8443` | HTTPS Proxy | HTTPS | Réseau local + Internet (via routeur) |

> Le port `8443` reçoit les connexions HTTPS, les déchiffre avec le certificat SSL, puis les transmet à Ollama sur le port `11434` en HTTP local.

---

## DNS

Le domaine `4ride.online` pointe vers l'IP publique de la bbox via un **enregistrement DNS de type A** :

```
4ride.online. A <PUBLIC_IP>
```

La bbox redirige ensuite le trafic vers ce serveur (`<LOCAL_IP>`) via les règles de port forwarding.

> La résolution DNS peut prendre quelques heures à se propager après modification.

---

## SSL / HTTPS

Le certificat SSL est fourni par **Let's Encrypt** via [acme.sh](https://github.com/acmesh-official/acme.sh).

- Fichiers : `scripts/ssl/fullchain.pem` et `scripts/ssl/key.pem`
- Autorité : Let's Encrypt (reconnu par tous les navigateurs, aucun avertissement)
- Validité : 90 jours (renouvellement automatique via acme.sh)
- CN : `4ride.online`

**Obtenir / renouveler le certificat :**
```bash
# Première émission (nécessite port 80 → 8080 sur le routeur temporairement)
~/bin/acme.sh --issue -d 4ride.online --standalone --httpport 8080 --server letsencrypt

# Installer dans le proxy
~/bin/acme.sh --install-cert -d 4ride.online \
 --cert-file scripts/ssl/cert.pem \
 --key-file scripts/ssl/key.pem \
 --fullchain-file scripts/ssl/fullchain.pem
```

---

## Démarrage

```bash
# 1. Déployer Ollama + modèle
cd /home/ia/techcorp-ai-chat
bash scripts/deploy_infra.sh

# 2. Démarrer le proxy HTTPS (port 8443)
python3 scripts/https_proxy.py &

# 3. Valider l'infrastructure
bash scripts/validate_infra.sh

# 4. Arrêter
bash scripts/stop_infra.sh
kill $(cat logs/https_proxy.pid)
```

---

## API - Endpoints

### Générer une réponse

```bash
curl -sk -X POST https://4ride.online/api/generate \
 -H "Content-Type: application/json" \
 -d '{"model":"phi3-financial","prompt":"What is EBITDA?","stream":false}'
```

### Chat (multi-tours)

```bash
curl -sk -X POST https://4ride.online/api/chat \
 -H "Content-Type: application/json" \
 -d '{
 "model": "phi3-financial",
 "messages": [{"role":"user","content":"Analyse ce bilan financier..."}],
 "stream": false
 }'
```

### Lister les modèles

```bash
curl -sk https://4ride.online/api/tags
```

> `-k` ignore l'avertissement du certificat auto-signé.

---

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/deploy_infra.sh` | Installe Ollama, télécharge le modèle, crée `phi3-financial` |
| `scripts/stop_infra.sh` | Arrête le serveur Ollama proprement |
| `scripts/validate_infra.sh` | Teste les 6 points de contrôle de l'infrastructure |
| `scripts/https_proxy.py` | Proxy HTTPS → HTTP pour exposer Ollama en HTTPS |

---

## Prérequis

- Debian 13, Python 3.13+ (stdlib uniquement, aucune dépendance externe)
- OpenSSL (pour la génération du certificat)
- Ollama installé dans `~/bin/bin/ollama`
- curl statique dans `~/bin/curl`
