# TechCorp AI Chat - Document de rendu

**Projet** : Interface web de chat IA connectée à Ollama 
**Stack** : Vue 3 · Vite · Tailwind CSS · WebGL · Web Speech API 
**Auteur** : Rezig Rachid 
**Date** : Juin 2026

---

## 1. Présentation du projet

TechCorp AI Chat est une interface web de conversation avec des modèles de langage fonctionnant localement via **Ollama**. L'application permet de discuter avec n'importe quel modèle LLM installé (phi3.5, llama3, mistral, etc.) sans aucun backend cloud - tout reste en local.

Le design s'inspire des standards des interfaces IA modernes (dark theme, glassmorphism, animations fluides) et vise une expérience professionnelle comparable à Claude ou ChatGPT, mais entièrement offline.

---

## 2. Fonctionnalités

### Chat & streaming
- Envoi de messages avec réponse en **streaming NDJSON** depuis Ollama
- Curseur clignotant pendant la génération
- Scroll automatique vers le bas à chaque token reçu
- Input désactivé pendant le streaming
- Chips de prompts rapides ("Code Review", "Performance Checklist", "UI Design Ideas")

### Sélection de modèle
- **Auto-fetch** des modèles disponibles au démarrage via `GET /api/tags`
- Dropdown pill ergonomique dans la zone de saisie (pas dans la topbar)
- Indicateur de chargement + message d'erreur si aucun modèle trouvé
- Changement de modèle à la volée sans recharger

### Historique des conversations
- **Sauvegarde automatique** en localStorage à chaque message (si activé)
- Section **Recent Chats** : 20 dernières conversations
- Section **Archive** : conversations archivées manuellement
- Actions par item : archiver/désarchiver, supprimer
- Chargement d'une ancienne conversation au clic
- Export JSON de toutes les sessions depuis les Settings

### Reconnaissance vocale
- Bouton micro connecté à la **Web Speech API** (`SpeechRecognition`)
- Transcription **intérimaire en direct** superposée sur l'input (semi-transparente)
- Résultat final ajouté au texte de l'input
- Anneau ripple rouge pulsant pendant l'écoute
- Langue configurable dans les Settings (fr-FR, en-US, es-ES, de-DE, ar-SA)

### Gestion des erreurs
Service d'erreurs centralisé avec catalogue de types :

| Code | Label | Déclencheur |
|------|-------|-------------|
| `NETWORK` | Connexion impossible | TypeError, status 0, timeout, réponse non-JSON |
| `MODEL_NOT_FOUND` | Modèle introuvable | HTTP 404 |
| `SERVER_ERROR` | Erreur serveur Ollama | HTTP 500 |
| `BAD_REQUEST` | Requête invalide | HTTP 400 |
| `STREAM_PARSE` | Erreur parsing stream | JSON.parse() fail sur NDJSON |
| `SPEECH` | Reconnaissance vocale | SpeechRecognition.onerror |
| `NO_MODELS` | Aucun modèle disponible | listModels() retourne [] |
| `UNKNOWN` | Erreur inconnue | Fallback |

Les erreurs apparaissent dans :
1. La **cloche** en topbar (liste déroulante, badge animé, dismiss individuel)
2. La **bulle IA** dans le chat (carte avec icône, label, code, détail)

### Settings
Panel latéral avec 5 onglets :
- **Connexion** : URL Ollama éditable + test + sauvegarde
- **Modèle** : température (0–2) et maxTokens (256–8192)
- **Voix** : langue de reconnaissance
- **Historique** : toggle autoSave, statistiques, export JSON, reset
- **À propos** : versions et stack

### Animations
- Messages : slide-up + fade spring au moment d'apparaître (TransitionGroup)
- Empty state : icône qui flotte doucement en boucle
- Sidebar sections : height-animate sur expand/collapse (JS hooks Vue)
- Items sidebar : stagger décalé de 25ms par index à l'ouverture
- Mic : anneau ripple rouge vers l'extérieur pendant l'écoute
- Send : micro-bounce au clic
- Badge notification : pop spring à chaque nouveau compteur
- Dropdowns : slide-down/up avec scale
- Settings panel : slide depuis la droite + fade

---

## 3. Architecture technique

### Stack
| Couche | Technologie |
|--------|-------------|
| Framework | Vue 3 - Composition API exclusivement (`<script setup>`) |
| Build | Vite (bundle runtime-only Vue, pas de compilateur à l'exécution) |
| CSS | Tailwind CSS v3 avec design system étendu |
| Icônes | Material Symbols Outlined (Google Fonts, variable font) |
| Polices | Geist (corps), JetBrains Mono (code) |
| Graphisme | WebGL (vertex + fragment shaders maison) |
| API | Ollama REST (fetch natif, pas d'axios) |
| Persistance | localStorage (sessions + settings) |
| Voix | Web Speech API navigateur |

### État global sans store
Pas de Pinia ni Vuex. L'état partagé repose sur le **pattern singleton module-level** :

```js
// Les refs sont déclarées HORS de la fonction exportée
const messages = ref([]) // → module-level, instancié une seule fois
const loading = ref(false)

export function useChat() {
 return { messages, loading, send } // tous les appelants partagent la même ref
}
```

Avantages : zéro dépendance, réactivité native Vue, HMR compatible.

### Composables
| Composable | Responsabilité |
|------------|----------------|
| `useChat` | Messages, loading, ollamaOnline, send(), clearChat(), loadSession() |
| `useHistory` | Sessions localStorage, recentSessions, archivedSessions, CRUD |
| `useModels` | availableModels, fetchModels(), loadingModels |
| `useSettings` | ollamaUrl, temperature, maxTokens, speechLang, autoSave (+ persistence) |
| `useSpeech` | SpeechRecognition toggle, listening, transcript interim |

### Services
| Service | Responsabilité |
|---------|----------------|
| `ollama.js` | `checkOllama()`, `listModels()`, `streamChat()` générateur async |
| `errorService.js` | `ERROR_TYPES` catalogue, `resolveErrorType()`, `useErrors()` store réactif |

### Streaming Ollama
```
POST /api/chat { model, messages, stream: true, options: { temperature, num_predict } }
↓
Réponse : flux NDJSON
↓
getReader() → decode() → split('\n') → JSON.parse(line) → json.message.content
↓
yield chunk → useChat accumule dans messages[last].content
```

---

## 4. Structure des fichiers

```
TechCorp-Web/
 src/
 App.vue
 main.js
 assets/main.css
 components/
 chat/
 ChatViewport.vue
 MessageAI.vue
 MessageUser.vue
 layout/
 InputArea.vue
 Sidebar.vue
 SidebarSection.vue
 TopBar.vue
 settings/
 SettingsPanel.vue
 ui/
 ShaderCanvas.vue
 composables/
 useChat.js
 useHistory.js
 useModels.js
 useSettings.js
 useSpeech.js
 services/
 errorService.js
 ollama.js
 docs/
 index.md
 01-overview.md
 02-architecture.md
 03-design-system.md
 04-components.md
 05-api-ollama.md
 06-shaders.md
 07-conventions.md
 08-rendu.md ← ce fichier
 public/
 index.html
 tailwind.config.js
 vite.config.js
 package.json
```

---

## 5. Points techniques notables

### Vite runtime-only bundle
Vite compile les SFC (`.vue`) au moment du build. Le bundle Vue inclus est **runtime-only** - il n'y a pas de compilateur de templates à l'exécution. Toute tentative d'utiliser `template: '...'` string dans `defineComponent()` échouera silencieusement (la vue ne rend rien). Tous les composants doivent être des `.vue` SFC.

### TransitionGroup et clé stable
Les messages dans `ChatViewport` utilisent `TransitionGroup name="msg"`. Chaque message a une clé stable (`msg.id ?? i`) pour que Vue distingue les éléments et déclenche les transitions correctement même pendant le streaming (où le contenu change mais l'élément est le même).

### Animation height JS hooks
L'expand/collapse des sections sidebar utilise des **JS hooks Vue Transition** plutôt que Tailwind, car animer `height: auto → 0` est impossible en CSS pur. Les hooks mesurent `el.scrollHeight` au moment de l'animation et appliquent la transition programmatiquement.

### Gestion des erreurs non-JSON
Si l'URL Ollama pointe vers un serveur qui répond en HTML (mauvais port, proxy, etc.), `res.json()` lèverait un `SyntaxError` sans code ni status, tombant dans `UNKNOWN`. La solution : wrapper `res.json()` dans un try/catch dans `listModels()` et relancer avec `status = 0` pour que `resolveErrorType()` le classifie comme `NETWORK`.

---

## 6. Prérequis & lancement

### Prérequis
- Node.js 18+
- Ollama installé et en cours d'exécution : `ollama serve`
- Au moins un modèle téléchargé : `ollama pull phi3.5`

### Lancement développement
```bash
npm install
npm run dev
# → http://localhost:5173
```

### Build production
```bash
npm run build
# → dist/
```

### CORS Ollama (si besoin)
```bash
OLLAMA_ORIGINS="http://localhost:5173" ollama serve
```

---

## 7. Choix de conception

**Pourquoi pas de Pinia ?** - Pour un projet de cette taille, le pattern singleton module-level est suffisant et élimine une dépendance. L'état réactif est tout aussi partageable sans store.

**Pourquoi pas de router ?** - Application single-page, une seule vue. Ajouter Vue Router serait du surengineering.

**Pourquoi fetch natif ?** - Axios apporterait ~40kb pour des fonctionnalités non nécessaires ici. Le streaming NDJSON requiert l'API `ReadableStream` de toute façon, qu'Axios ne supporte pas nativement.

**Pourquoi le model picker dans InputArea et pas en TopBar ?** - Ergonomie : l'utilisateur change de modèle juste avant d'envoyer un message. Avoir le sélecteur au même endroit que l'input réduit les aller-retours yeux/souris.
