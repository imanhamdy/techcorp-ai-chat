#!/bin/bash
# =============================================================================
# TechCorp Industries — INFRA Deployment Script
# Ollama + Phi-3.5-Financial
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()      { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

OLLAMA_HOST="0.0.0.0"
OLLAMA_PORT="11434"
MODEL_NAME="phi3.5"          # Base: microsoft/Phi-3.5-mini-instruct via Ollama
MODEL_ALIAS="phi3-financial"  # Alias local avec Modelfile personnalisé
LOG_FILE="./logs/ollama_deploy.log"

mkdir -p ./logs

echo ""
echo "============================================================"
echo "   TechCorp Industries — Déploiement Serveur d'Inférence"
echo "============================================================"
echo ""

# -----------------------------------------------------------------------------
# ÉTAPE 1 — Vérification / Installation d'Ollama
# -----------------------------------------------------------------------------
log_info "Étape 1/5 — Vérification d'Ollama..."

if command -v ollama &> /dev/null; then
    OLLAMA_VERSION=$(ollama --version 2>/dev/null || echo "inconnu")
    log_ok "Ollama déjà installé : $OLLAMA_VERSION"
else
    log_warn "Ollama non trouvé. Lancement de l'installation..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        log_error "Sur macOS, installez Ollama manuellement via : https://ollama.com/download"
        exit 1
    else
        log_error "OS non supporté pour l'installation automatique."
        exit 1
    fi
    log_ok "Ollama installé avec succès."
fi

# -----------------------------------------------------------------------------
# ÉTAPE 2 — Démarrage du service Ollama
# -----------------------------------------------------------------------------
log_info "Étape 2/5 — Démarrage du service Ollama..."

# Arrêt propre d'une instance existante
pkill -f "ollama serve" 2>/dev/null || true
sleep 2

# Démarrage avec binding réseau étendu (accessible à l'équipe DEV WEB)
OLLAMA_HOST=${OLLAMA_HOST}:${OLLAMA_PORT} nohup ollama serve >> "$LOG_FILE" 2>&1 &
OLLAMA_PID=$!
echo $OLLAMA_PID > ./logs/ollama.pid

log_info "Ollama démarré (PID: $OLLAMA_PID). En attente de disponibilité..."

# Attente jusqu'à 30s
for i in $(seq 1 30); do
    if curl -s "http://localhost:${OLLAMA_PORT}" > /dev/null 2>&1; then
        log_ok "Serveur Ollama opérationnel sur http://localhost:${OLLAMA_PORT}"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        log_error "Timeout — le serveur Ollama n'a pas démarré dans les temps."
        exit 1
    fi
done

# -----------------------------------------------------------------------------
# ÉTAPE 3 — Pull du modèle Phi-3.5
# -----------------------------------------------------------------------------
log_info "Étape 3/5 — Téléchargement du modèle Phi-3.5..."

if ollama list 2>/dev/null | grep -q "$MODEL_NAME"; then
    log_ok "Modèle $MODEL_NAME déjà présent localement."
else
    log_info "Pull de microsoft/phi3.5 depuis le registre Ollama..."
    ollama pull $MODEL_NAME
    log_ok "Modèle $MODEL_NAME téléchargé."
fi

# -----------------------------------------------------------------------------
# ÉTAPE 4 — Création du Modelfile Phi-3.5-Financial
# -----------------------------------------------------------------------------
log_info "Étape 4/5 — Création du profil Phi-3.5-Financial..."

cat > ./models/Modelfile.financial << 'EOF'
# TechCorp Industries — Phi-3.5-Financial Modelfile
FROM phi3.5

# Paramètres d'inférence optimisés pour le domaine financier
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
PARAMETER num_predict 1024

# System prompt spécialisé Finance/Business
SYSTEM """
You are Phi-3.5-Financial, an expert AI assistant specialized in finance, business analysis, and economic reasoning for TechCorp Industries.

Your core competencies:
- Financial analysis (P&L, balance sheets, cash flow statements)
- Market analysis and competitive intelligence
- Risk assessment and financial modeling
- Corporate strategy and M&A advisory
- Regulatory compliance (IFRS, GAAP, MiFID II, Basel III)
- Investment analysis and portfolio management

Guidelines:
- Always provide precise, data-driven answers
- Clearly distinguish between factual information and analysis
- Flag any assumptions made in your reasoning
- Recommend consulting certified professionals for legal/tax matters
- Maintain strict confidentiality framing for sensitive financial data

Respond in the same language as the user (French or English).
"""
EOF

mkdir -p ./models

# Création du modèle avec l'alias financier
ollama create $MODEL_ALIAS -f ./models/Modelfile.financial
log_ok "Profil $MODEL_ALIAS créé avec succès."

# -----------------------------------------------------------------------------
# ÉTAPE 5 — Test de sanité de l'API
# -----------------------------------------------------------------------------
log_info "Étape 5/5 — Test de l'API REST..."

TEST_RESPONSE=$(curl -s -X POST "http://localhost:${OLLAMA_PORT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"${MODEL_ALIAS}\",
        \"prompt\": \"What is EBITDA? Answer in one sentence.\",
        \"stream\": false,
        \"options\": {\"temperature\": 0.1}
    }" 2>/dev/null)

if echo "$TEST_RESPONSE" | grep -q '"response"'; then
    log_ok "Test API réussi. Réponse reçue du modèle."
    ANSWER=$(echo "$TEST_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','')[:200])" 2>/dev/null || echo "(parsing skipped)")
    echo ""
    echo -e "  ${GREEN}→ Réponse test :${NC} $ANSWER"
else
    log_warn "Test API : réponse inattendue. Vérifiez les logs : $LOG_FILE"
fi

# -----------------------------------------------------------------------------
# RÉSUMÉ DE DÉPLOIEMENT
# -----------------------------------------------------------------------------
echo ""
echo "============================================================"
echo -e "   ${GREEN}DÉPLOIEMENT RÉUSSI${NC}"
echo "============================================================"
echo ""
echo "  Serveur      : Ollama"
echo "  Modèle       : $MODEL_ALIAS (base: $MODEL_NAME)"
echo "  Endpoint     : http://localhost:${OLLAMA_PORT}"
echo "  API Generate : http://localhost:${OLLAMA_PORT}/api/generate"
echo "  API Chat     : http://localhost:${OLLAMA_PORT}/api/chat"
echo "  Logs         : $LOG_FILE"
echo ""
echo "  ► Pour l'équipe DEV WEB :"
echo "    URL de base : http://<INFRA_SERVER_IP>:${OLLAMA_PORT}"
echo "    Modèle à utiliser : ${MODEL_ALIAS}"
echo ""
echo "  ► Commandes utiles :"
echo "    ollama list                    # Lister les modèles"
echo "    ollama ps                      # Modèles en cours d'exécution"
echo "    ollama run ${MODEL_ALIAS}       # Test interactif CLI"
echo "    cat ./logs/ollama.pid          # PID du serveur"
echo "    ./scripts/stop_infra.sh        # Arrêt propre"
echo ""
