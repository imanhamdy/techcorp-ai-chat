# TechCorp AI Chat - Index docs

Interface web de chat Vue 3 + Vite connectée à **Ollama** (serveur d'inférence local). Design "Synthetic Intelligence" : dark theme, glassmorphism, sidebar fixe, input flottant. **Pas de backend, pas de router, pas de Pinia.**

> Lire ce fichier d'abord. Ouvrir les docs détaillées **seulement quand nécessaire** (économie de tokens).

## Carte des docs

| Fichier | Quand l'ouvrir |
|---|---|
| [01-overview.md](01-overview.md) | Contexte, stack technique, commandes npm |
| [02-architecture.md](02-architecture.md) | Arborescence `src/`, rôle de chaque fichier |
| [03-design-system.md](03-design-system.md) | `tailwind.config.js` complet : couleurs, fonts, sizes, radius |
| [04-components.md](04-components.md) | Comportement attendu de chaque composant Vue |
| [05-api-ollama.md](05-api-ollama.md) | `services/ollama.js`, `useChat.js`, streaming, CORS |
| [06-shaders.md](06-shaders.md) | Shaders WebGL (vertex + fragment) à utiliser tels quels |
| [07-conventions.md](07-conventions.md) | Conventions de code, comportements critiques, interdits |
| [08-rendu.md](08-rendu.md) | **Document de rendu complet** - présentation du projet |

## Fonctionnalités implémentées

- **Chat en streaming** avec Ollama (NDJSON, scroll auto, curseur clignotant)
- **Changement de modèle à la volée** - dropdown pill dans l'InputArea, auto-fetch au démarrage
- **Statut Ollama temps réel** - dot vert/rouge, vérification toutes les 30s
- **Historique localStorage** - Recent Chats + Archive, avec sauvegarde, archivage, suppression
- **Reconnaissance vocale** - Web Speech API, transcription en direct dans l'input
- **Gestion d'erreurs structurée** - errorService avec catalogue (NETWORK, SERVER_ERROR, etc.), cloche notifications
- **Settings multi-onglets** - URL Ollama, température, maxTokens, langue vocale, historique, à propos
- **Animations** - messages slide-up, mic ripple, sidebar height-animate, empty state float, badges pop
- **WebGL shaders** - fond animé New Chat + bordure input focus

## Règles d'or

- **Stack** : Vue 3 Composition API + `<script setup>`, Vite, Tailwind, `fetch` natif uniquement.
- **Pas de** : backend, router, Pinia/Vuex, axios, Options API.
- **Singleton state** : refs au niveau module dans les composables - partagées sans store.
- **Palette figée** : ne jamais modifier les couleurs du design system.
- **SFC uniquement** : pas de `template: '...'` string dans `defineComponent()` - Vite = runtime-only Vue, pas de compilateur à l'exécution.
