# 02 - Architecture des fichiers

```
src/
 main.js
 App.vue # Layout racine : Sidebar + TopBar + ChatViewport + InputArea + SettingsPanel
 assets/
 main.css # Tailwind base + keyframes + transitions Vue nommées
 components/
 chat/
 ChatViewport.vue # Zone scrollable, TransitionGroup messages, empty state flottant
 MessageAI.vue # Bulle IA : curseur streaming, carte d'erreur structurée
 MessageUser.vue # Bulle utilisateur droite + horodatage
 layout/
 InputArea.vue # Footer : model picker pill + mic ripple + input + send bounce
 Sidebar.vue # Nav 280px : New Chat + Recent Chats + Archive
 SidebarSection.vue # Section pliable : JS hook height-animate + stagger items
 TopBar.vue # Header : brand + status dot + Settings + cloche erreurs
 settings/
 SettingsPanel.vue # Slide-in panel : 5 onglets (Connexion, Modèle, Voix, Historique, À propos)
 ui/
 ShaderCanvas.vue # Canvas WebGL réutilisable (New Chat + input border)
 composables/
 useChat.js # Singleton : messages, loading, ollamaOnline, send(), clearChat(), loadSession()
 useHistory.js # Singleton : sessions localStorage, recentSessions, archivedSessions
 useModels.js # Singleton : availableModels, fetchModels() auto au démarrage
 useSettings.js # Singleton : ollamaUrl, temperature, maxTokens, speechLang, autoSave
 useSpeech.js # Web Speech API : toggle(), listening, transcript interim
 services/
 errorService.js # ERROR_TYPES catalogue, resolveErrorType(), useErrors() reactive store
 ollama.js # checkOllama(), listModels(), streamChat() générateur async
```

## Pattern singleton (sans Pinia)

Toutes les refs d'état sont déclarées **au niveau module** (hors de la fonction exportée) :

```js
// useChat.js
const messages = ref([]) // ← module-level, partagé globalement
const loading = ref(false)

export function useChat() {
 // retourne les mêmes refs à chaque appel
 return { messages, loading, send, clearChat }
}
```

Résultat : n'importe quel composant qui appelle `useChat()` obtient le même état réactif - pas besoin de store centralisé.

## Flux de données principal

```
useSettings.ollamaUrl (localStorage)
 ↓
ollama.js (checkOllama, listModels, streamChat)
 ↓
useChat.js (send, messages, loading, ollamaOnline)
 ↓
ChatViewport → MessageAI / MessageUser

Erreurs :
ollama.js → throw httpError
 ↓
useChat.js → useErrors().push(err)
 ↓
errorService.resolveErrorType()
 ↓
TopBar cloche + MessageAI carte d'erreur
```

## Flux URL Ollama

L'URL est lue dans `ollamaUrl.value` **à chaque appel** dans `ollama.js` - modifier l'URL depuis Settings prend effet immédiatement sur le prochain message.

```
localStorage
 ↓
useSettings.ollamaUrl (ref singleton)
 ↓ ↓
useChat.js SettingsPanel.vue
(streamChat, (draftUrl → save
 checkOllama) → ollamaUrl)
```

## Règle SFC obligatoire

Vite utilise le bundle Vue **runtime-only** (sans compilateur). Les `template: '...'` strings dans `defineComponent()` sont silencieusement ignorées. Tout le HTML doit être dans des fichiers `.vue` compilés au build.
