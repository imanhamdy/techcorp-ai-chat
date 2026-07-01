#!/bin/bash
# TechCorp — Script de validation / sanity check du serveur d'inférence

OLLAMA_PORT="${OLLAMA_PORT:-11434}"
MODEL_ALIAS="phi3-financial"
PASS=0
FAIL=0

check() {
    local label="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "\033[0;32m[PASS]\033[0m $label"
        ((PASS++))
    else
        echo -e "\033[0;31m[FAIL]\033[0m $label"
        ((FAIL++))
    fi
}

echo ""
echo "=== TechCorp — Validation Infrastructure ==="
echo ""

# 1. Processus Ollama actif
check "Processus Ollama en cours d'exécution" "pgrep -f 'ollama serve'"

# 2. Port ouvert
check "Port $OLLAMA_PORT accessible (localhost)" "curl -s --max-time 3 http://localhost:${OLLAMA_PORT}"

# 3. Modèle présent
check "Modèle '$MODEL_ALIAS' listé dans Ollama" "ollama list 2>/dev/null | grep -q $MODEL_ALIAS"

# 4. API /api/tags répond
check "Endpoint /api/tags opérationnel" \
    "curl -s http://localhost:${OLLAMA_PORT}/api/tags | grep -q 'models'"

# 5. Inférence réelle (timeout 60s)
echo -n "  [TEST] Inférence sur '$MODEL_ALIAS'... "
RESP=$(curl -s --max-time 60 -X POST "http://localhost:${OLLAMA_PORT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"${MODEL_ALIAS}\",\"prompt\":\"Reply OK\",\"stream\":false,\"options\":{\"num_predict\":5}}" 2>/dev/null)

if echo "$RESP" | grep -q '"response"'; then
    echo -e "\033[0;32m[PASS]\033[0m Inférence fonctionnelle"
    ((PASS++))
else
    echo -e "\033[0;31m[FAIL]\033[0m Inférence échouée"
    ((FAIL++))
fi

# 6. Endpoint /api/chat (OpenAI-compatible)
check "Endpoint /api/chat accessible" \
    "curl -s --max-time 5 -X POST http://localhost:${OLLAMA_PORT}/api/chat \
     -H 'Content-Type: application/json' \
     -d '{\"model\":\"${MODEL_ALIAS}\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"stream\":false}' \
     | grep -q 'message'"

echo ""
echo "=== Résultat : $PASS passed / $((PASS+FAIL)) total ==="
echo ""

# Infos pour DEV WEB
IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")
echo "  Endpoint réseau : http://${IP}:${OLLAMA_PORT}"
echo "  Modèle actif    : ${MODEL_ALIAS}"
echo "  API Generate    : POST http://${IP}:${OLLAMA_PORT}/api/generate"
echo "  API Chat        : POST http://${IP}:${OLLAMA_PORT}/api/chat"
echo ""

if [ $FAIL -gt 0 ]; then exit 1; fi