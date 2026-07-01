#!/bin/bash
# TechCorp — Arrêt propre du serveur Ollama

echo "[INFO] Arrêt du serveur Ollama..."

if [ -f ./logs/ollama.pid ]; then
    PID=$(cat ./logs/ollama.pid)
    kill $PID 2>/dev/null && echo "[OK]   Processus $PID arrêté." || echo "[WARN] Processus déjà arrêté."
    rm -f ./logs/ollama.pid
else
    pkill -f "ollama serve" 2>/dev/null && echo "[OK]   Ollama arrêté." || echo "[INFO] Aucun processus Ollama trouvé."
fi