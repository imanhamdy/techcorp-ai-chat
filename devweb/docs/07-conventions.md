# 07 - Conventions & comportements critiques

## Conventions de code
- Composition API uniquement, **pas d'Options API**.
- `<script setup>` sur tous les composants.
- Props typées avec `defineProps`, events avec `defineEmits`.
- Nommage : PascalCase pour les composants, camelCase pour les variables.
- Pas de `any` TypeScript (si migration TS future).
- CSS : classes Tailwind en priorité ; CSS custom uniquement pour animations WebGL et scrollbar.

## Comportements critiques
1. **Scroll automatique** : après chaque chunk de streaming, `chatViewport.scrollTop = chatViewport.scrollHeight`.
2. **Désactiver l'input** pendant le streaming (éviter les envois multiples).
3. **Curseur clignotant** pendant le streaming : ajouter `|` à la fin de `aiMsg.content` via `setInterval`, retirer à la fin.
4. **Dot de statut** : appeler `checkOllama()` au montage et toutes les 30s.
5. **Gestion d'erreur** : si Ollama est down, afficher une bulle IA avec texte rouge.
6. **Chips** : au clic, setter l'input ET focus sur l'input immédiatement.

## Ce que Claude Code NE doit PAS faire
- Pas de backend Express/FastAPI - tout passe directement par l'API Ollama côté client.
- Pas de Pinia ni Vuex - `useChat.js` suffit comme state management.
- Pas de dépendances inutiles (axios, lodash, etc.) - `fetch` natif uniquement.
- Ne pas modifier la palette de couleurs - figée dans [03-design-system.md](03-design-system.md).
