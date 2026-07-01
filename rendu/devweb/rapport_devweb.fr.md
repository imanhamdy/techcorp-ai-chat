🇫🇷 Français · [🇬🇧 English](rapport_devweb.en.md)

---

# Rapport DEV WEB - TechCorp AI Challenge
**Filière :** DEV WEB · **Date :** 2026-06-30
**URL publique :** https://4ride.online
**Repo :** github.com/HACKATON-2526-GroupeB/techcorp-ai-chat

---

## 1. Stack technique

| Composant | Technologie | Version |
|---|---|---|
| Framework UI | Vue.js 3 (Composition API) | 3.5 |
| Build tool | Vite | 6.4 |
| CSS | Tailwind CSS + @tailwindcss/typography | 3.4 |
| Markdown | marked.js | 15.x |
| Icônes | Material Symbols (Google Fonts CDN) | - |
| Fonts | Geist / Inter (Google Fonts CDN) | - |
| Serveur statique | Caddy v2.9.1 (sert `devweb/dist/`) | 2.9.1 |

---

## 2. Architecture des composants

```
App.vue ← racine : état global, routing entre vues
 components/layout/
 Sidebar.vue ← historique conversations, nav, profil
 TopBar.vue ← logo, sélecteur modèle, thème, paramètres
 InputArea.vue ← textarea auto-resize, voix, stop, envoi
 components/chat/
 ChatViewport.vue ← welcome screen + fil de messages
 MessageUser.vue ← bulle utilisateur (violet translucide)
 MessageAI.vue ← réponse IA : markdown, copier, timestamp
 components/settings/
 SettingsPanel.vue ← panel latéral : modèle, température, tokens
 components/ui/
 ShaderCanvas.vue ← fond animé CSS (blobs radial-gradient)
 composables/
 useChat.js ← logique principale : send, stop, streaming
 useModels.js ← fetch /api/tags → liste des modèles
 useSettings.js ← URL Ollama, température, langue vocale
 useSpeech.js ← Web Speech API (reconnaissance vocale)
 useConversations.js ← historique localStorage multi-conversations
 useTheme.js ← toggle dark/light mode
```

---

## 3. Fonctionnalités implémentées

### Chat & streaming
- **Streaming token par token** via `fetch()` + `ReadableStream` vers `/api/chat` (Ollama)
- **AbortController** : bouton Stop interrompt la génération en cours (conserve le partiel)
- **Markdown rendu** dans les réponses IA via `marked.parse()` + prose Tailwind
- **Curseur clignotant** pendant la génération (animation CSS `blink`)
- **Typing dots** animés pendant le chargement initial

### Interface
- **Welcome screen** avec 4 cartes catégories cliquables (Analyse financière, Données & marchés, Résumés rapides, Conseils & explications)
- **Suggestions pills** pour démarrer rapidement
- **Scroll-to-bottom** automatique + bouton flottant si on a scrollé vers le haut
- **Animations** : entrée des messages (`msg-in`), cartes échelonnées (`card-stagger`), blobs d'arrière-plan (`drift`)

### Paramètres
- Sélecteur de modèle (liste chargée dynamiquement depuis Ollama)
- Sliders température (0–1) et tokens max (256–4096)
- Toggle sauvegarde auto
- URL Ollama (cachée dans section "Avancé")
- Langue de reconnaissance vocale (6 langues)

### Mobile
- Sidebar en **drawer** (translate-x hors écran, overlay backdrop)
- Bouton hamburger dans la TopBar (masqué sur desktop)
- Bulles de messages adaptées (`max-w-[85%]` mobile / `max-w-[72%]` desktop)
- Barre d'outils input simplifiée sur mobile (voix masquée)

### Thème
- **Toggle dark/light** (icône /) via `useTheme.js`
- Préférence persistée en `localStorage`
- Implémentation : `filter: invert(1) hue-rotate(180deg)` sur `<html>`

### Historique
- Multi-conversations stockées en **localStorage**
- Création, sélection, suppression de conversations depuis la sidebar
- Sauvegarde automatique configurable

---

## 4. Connexion avec Ollama

```
Browser HTTPS Caddy :8443 /api/* Ollama :11434
```

Le frontend appelle exclusivement `https://4ride.online/api/...` - Caddy proxifie vers Ollama en HTTP local.

### Endpoints utilisés

| Endpoint | Usage |
|---|---|
| `GET /api/tags` | Liste des modèles disponibles |
| `POST /api/chat` | Inférence streaming (format messages) |

---

## 5. Démarrage local (développement)

```bash
# Prérequis : Node.js ≥ 18
cd devweb/
npm install
npm run dev # dev server sur http://localhost:5173

# Build production
npm run build # → dist/ (servi par Caddy)
```

### Variables importantes dans `useSettings.js`

```js
const DEFAULT_URL = 'https://4ride.online' // URL Ollama (via proxy Caddy)
```

Pour développer en local avec un Ollama local, changer l'URL dans les paramètres vers `http://localhost:11434`.

---

## 6. Déploiement production

```bash
export PATH="$HOME/bin/node/bin:$HOME/bin/bin:$HOME/bin:$PATH"

# Build
cd devweb && npm run build

# Caddy sert dist/ automatiquement (process déjà actif)
# Forcer rechargement config si besoin :
caddy reload --config /home/ia/techcorp-ai-chat/Caddyfile
```

---

## 7. Captures d'écran des fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Welcome screen | Cartes catégories + suggestions de questions |
| Chat actif | Messages streamés + curseur clignotant |
| Panel paramètres | Sélecteur modèle + sliders température/tokens |
| Mobile drawer | Sidebar accessible via hamburger |
| Stop en cours | Bouton rouge interrompt la génération |
