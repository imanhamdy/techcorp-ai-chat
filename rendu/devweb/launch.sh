#!/bin/bash
# Lance l'interface TechCorp AI Chat en mode developpement local
# Usage : bash rendu/devweb/launch.sh

set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

export PATH="$HOME/bin/node/bin:$HOME/bin/bin:$HOME/bin:$PATH"

echo "=== TechCorp AI Chat - DEV WEB ==="
echo "Repertoire : $ROOT/devweb"
echo ""

cd "$ROOT/devweb"

if [ ! -d node_modules ]; then
  echo "[1/2] Installation des dependances..."
  npm install
fi

echo "[2/2] Demarrage du serveur de dev..."
echo "      -> http://localhost:5173"
echo "      (Ctrl+C pour arreter)"
echo ""
npm run dev
